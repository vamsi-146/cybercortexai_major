from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from app.database.mongodb import get_database
from app.repositories.user_repository import UserRepository
from app.repositories.audit_repository import AuditLogRepository
from app.schemas.user import UserCreate, UserLogin, Token, User
from app.core.security import verify_password, create_access_token, create_refresh_token, decode_token
from app.schemas.audit import AuditAction, ResourceType
from app.api.dependencies.auth import get_current_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db = Depends(get_database)):
    """Register a new user."""
    user_repo = UserRepository(db)
    
    # Check if email already exists
    existing_user = await user_repo.get_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username already exists
    existing_username = await user_repo.get_by_username(user_data.username)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create user
    user = await user_repo.create(user_data)
    
    # Log audit
    audit_repo = AuditLogRepository(db)
    await audit_repo.create({
        "username": user["username"],
        "action": AuditAction.CREATE,
        "resource_type": ResourceType.USER,
        "resource_id": user["id"],
        "result": "SUCCESS"
    })
    
    return User(**user)


@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db = Depends(get_database)):
    """Authenticate user and return tokens."""
    user_repo = UserRepository(db)
    audit_repo = AuditLogRepository(db)
    
    # Find user by email
    user = await user_repo.get_by_email(user_credentials.email)
    if not user:
        # Log failed attempt
        await audit_repo.create({
            "username": user_credentials.email,
            "action": AuditAction.LOGIN,
            "resource_type": ResourceType.USER,
            "resource_id": "unknown",
            "result": "FAILURE"
        })
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not verify_password(user_credentials.password, user["password_hash"]):
        # Log failed attempt
        await audit_repo.create({
            "username": user["username"],
            "action": AuditAction.LOGIN,
            "resource_type": ResourceType.USER,
            "resource_id": user["id"],
            "result": "FAILURE"
        })
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Check if user is active
    if not user.get("is_active"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )
    
    # Update last login
    await user_repo.update_last_login(user["id"])
    
    # Create tokens
    access_token = create_access_token({
        "sub": user["id"],
        "email": user["email"],
        "role": user["role"]
    })
    refresh_token = create_refresh_token({
        "sub": user["id"],
        "email": user["email"],
        "role": user["role"]
    })
    
    # Log successful login
    await audit_repo.create({
        "user_id": user["id"],
        "username": user["username"],
        "action": AuditAction.LOGIN,
        "resource_type": ResourceType.USER,
        "resource_id": user["id"],
        "result": "SUCCESS"
    })
    
    logger.info(f"User logged in: {user['email']}")
    return Token(access_token=access_token, refresh_token=refresh_token)


from pydantic import BaseModel


class RefreshTokenRequest(BaseModel):
    refresh_token: str


@router.post("/refresh", response_model=Token)
async def refresh_token(token_request: RefreshTokenRequest, db = Depends(get_database)):
    """Refresh access token using refresh token."""
    payload = decode_token(token_request.refresh_token)
    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user_id = payload.get("sub")
    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(user_id)
    
    if not user or not user.get("is_active"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Create new access token
    access_token = create_access_token({
        "sub": user["id"],
        "email": user["email"],
        "role": user["role"]
    })
    
    # Create new refresh token (token rotation)
    new_refresh_token = create_refresh_token({
        "sub": user["id"],
        "email": user["email"],
        "role": user["role"]
    })
    
    return Token(access_token=access_token, refresh_token=new_refresh_token)


@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user), db = Depends(get_database)):
    """Logout user (client-side token invalidation)."""
    # In a production system, you might want to invalidate tokens in a blacklist
    # For Phase 2, we just log the logout action
    audit_repo = AuditLogRepository(db)
    await audit_repo.create({
        "user_id": current_user["id"],
        "username": current_user["username"],
        "action": AuditAction.LOGOUT,
        "resource_type": ResourceType.USER,
        "resource_id": current_user["id"],
        "result": "SUCCESS"
    })
    
    logger.info(f"User logged out: {current_user['email']}")
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=User)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information."""
    return User(**current_user)
