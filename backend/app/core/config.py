from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""
    
    # Force reload to pick up new CORS origins

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    # Application
    APP_NAME: str = "CyberCortexAI"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8000,http://localhost:3001,http://localhost:3002"

    # Security
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # MongoDB
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DATABASE: str = "cybercortex"
    MONGODB_USERNAME: str = ""
    MONGODB_PASSWORD: str = ""

    # Neo4j (Not used in Phase 2, but defined for consistency)
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = ""

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    @property
    def mongodb_connection_string(self) -> str:
        """Construct MongoDB connection string with auth if provided."""
        if self.MONGODB_USERNAME and self.MONGODB_PASSWORD:
            # If URL already includes protocol, extract host
            if self.MONGODB_URL.startswith("mongodb://"):
                host = self.MONGODB_URL.replace("mongodb://", "")
                return f"mongodb://{self.MONGODB_USERNAME}:{self.MONGODB_PASSWORD}@{host}/{self.MONGODB_DATABASE}"
            return f"mongodb://{self.MONGODB_USERNAME}:{self.MONGODB_PASSWORD}@{self.MONGODB_URL}/{self.MONGODB_DATABASE}"
        return f"{self.MONGODB_URL}/{self.MONGODB_DATABASE}"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
