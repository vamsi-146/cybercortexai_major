# CyberCortex AI - Deployment Strategy

## Overview

This document outlines the deployment strategy for CyberCortex AI, including Docker containerization, Docker Compose orchestration, environment configuration, and production deployment considerations.

## Deployment Architecture

### Development Environment
```
Developer Machine
├── Frontend (Vite dev server)
├── Backend (FastAPI with uvicorn)
├── MongoDB (local or Docker)
└── Neo4j (local or Docker)
```

### Production Environment
```
Load Balancer (Nginx)
    ↓
Frontend (Nginx serving static files)
    ↓
Backend (FastAPI with Gunicorn/Uvicorn workers)
    ↓
MongoDB (Replica Set)
    ↓
Neo4j (Cluster)
```

## Docker Configuration

### 1. Frontend Dockerfile

**File**: `docker/Dockerfile.frontend`

```dockerfile
# Multi-stage build for optimization
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY frontend/package*.json ./
RUN npm ci

# Copy source code
COPY frontend/ ./

# Build application
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built assets from builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY docker/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### 2. Backend Dockerfile

**File**: `docker/Dockerfile.backend`

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 3. Docker Compose Configuration

**File**: `docker-compose.yml`

```yaml
version: '3.8'

services:
  # Frontend
  frontend:
    build:
      context: .
      dockerfile: docker/Dockerfile.frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
    networks:
      - cybercortex-network
    environment:
      - VITE_API_URL=http://backend:8000/api/v1

  # Backend
  backend:
    build:
      context: .
      dockerfile: docker/Dockerfile.backend
    ports:
      - "8000:8000"
    depends_on:
      - mongodb
      - neo4j
    networks:
      - cybercortex-network
    environment:
      - MONGODB_URL=mongodb://mongodb:27017/cybercortex
      - NEO4J_URI=bolt://neo4j:7687
      - NEO4J_USER=neo4j
      - NEO4J_PASSWORD=neo4j_password
      - JWT_SECRET_KEY=your_jwt_secret_key_here
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./backend:/app
      - backend-logs:/app/logs

  # MongoDB
  mongodb:
    image: mongo:7.0
    ports:
      - "27017:27017"
    networks:
      - cybercortex-network
    environment:
      - MONGO_INITDB_ROOT_USERNAME=admin
      - MONGO_INITDB_ROOT_PASSWORD=admin_password
      - MONGO_INITDB_DATABASE=cybercortex
    volumes:
      - mongodb-data:/data/db
      - mongodb-config:/data/configdb

  # Neo4j
  neo4j:
    image: neo4j:5.14
    ports:
      - "7474:7474"  # HTTP
      - "7687:7687"  # Bolt
    networks:
      - cybercortex-network
    environment:
      - NEO4J_AUTH=neo4j/neo4j_password
      - NEO4J_PLUGINS=["apoc"]
    volumes:
      - neo4j-data:/data
      - neo4j-logs:/logs
      - neo4j-import:/var/lib/neo4j/import
      - neo4j-plugins:/plugins

networks:
  cybercortex-network:
    driver: bridge

volumes:
  mongodb-data:
  mongodb-config:
  neo4j-data:
  neo4j-logs:
  neo4j-import:
  neo4j-plugins:
  backend-logs:
```

### 4. Production Docker Compose

**File**: `docker-compose.prod.yml`

```yaml
version: '3.8'

services:
  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./docker/nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./docker/nginx/ssl:/etc/nginx/ssl
      - frontend-static:/usr/share/nginx/html
    depends_on:
      - frontend
    networks:
      - cybercortex-network

  # Frontend
  frontend:
    build:
      context: .
      dockerfile: docker/Dockerfile.frontend
    volumes:
      - frontend-static:/usr/share/nginx/html
    networks:
      - cybercortex-network

  # Backend with multiple workers
  backend:
    build:
      context: .
      dockerfile: docker/Dockerfile.backend
    ports:
      - "8000:8000"
    depends_on:
      - mongodb
      - neo4j
    networks:
      - cybercortex-network
    environment:
      - MONGODB_URL=mongodb://mongodb:27017/cybercortex
      - NEO4J_URI=bolt://neo4j:7687
      - NEO4J_USER=neo4j
      - NEO4J_PASSWORD=${NEO4J_PASSWORD}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ENVIRONMENT=production
    command: ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
    restart: unless-stopped

  # MongoDB Replica Set (simplified for production)
  mongodb:
    image: mongo:7.0
    ports:
      - "27017:27017"
    networks:
      - cybercortex-network
    environment:
      - MONGO_INITDB_ROOT_USERNAME=${MONGO_USERNAME}
      - MONGO_INITDB_ROOT_PASSWORD=${MONGO_PASSWORD}
      - MONGO_INITDB_DATABASE=cybercortex
    volumes:
      - mongodb-data:/data/db
      - mongodb-config:/data/configdb
    restart: unless-stopped

  # Neo4j
  neo4j:
    image: neo4j:5.14-enterprise  # Enterprise for clustering
    ports:
      - "7474:7474"
      - "7687:7687"
    networks:
      - cybercortex-network
    environment:
      - NEO4J_AUTH=neo4j/${NEO4J_PASSWORD}
      - NEO4J_ACCEPT_LICENSE_AGREEMENT=yes
      - NEO4J_PLUGINS=["apoc"]
    volumes:
      - neo4j-data:/data
      - neo4j-logs:/logs
    restart: unless-stopped

networks:
  cybercortex-network:
    driver: bridge

volumes:
  mongodb-data:
  mongodb-config:
  neo4j-data:
  neo4j-logs:
  frontend-static:
```

## Environment Configuration

### Environment Variables Template

**File**: `.env.example`

```bash
# Application
APP_NAME=CyberCortexAI
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=INFO

# API Configuration
API_V1_PREFIX=/api/v1
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# Security
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# MongoDB
MONGODB_URL=mongodb://localhost:27017/cybercortex
MONGODB_USERNAME=admin
MONGODB_PASSWORD=admin_password
MONGODB_DATABASE=cybercortex

# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=neo4j_password

# LLM Configuration
LLM_PROVIDER=openai
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=1000

# Alternative: Anthropic
# ANTHROPIC_API_KEY=your-anthropic-api-key
# ANTHROPIC_MODEL=claude-3-opus

# Redis (optional for caching)
REDIS_URL=redis://localhost:6379/0

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60

# ML Model Configuration
ML_MODEL_PATH=./models
RETRAINING_SCHEDULE=weekly

# Monitoring
SENTRY_DSN=  # Optional for error tracking
ENABLE_METRICS=True

# Email (optional for notifications)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

## Nginx Configuration

### Nginx Configuration

**File**: `docker/nginx/nginx.conf`

```nginx
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;

    sendfile on;
    tcp_nopush on;
    keepalive_timeout 65;
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

    server {
        listen 80;
        server_name localhost;

        # Frontend
        location / {
            root /usr/share/nginx/html;
            try_files $uri $uri/ /index.html;
        }

        # Backend API
        location /api/ {
            limit_req zone=api_limit burst=20 nodelay;
            proxy_pass http://backend:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Health check
        location /health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }
    }
}
```

## Deployment Steps

### 1. Local Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/CyberCortexAI.git
cd CyberCortexAI

# Copy environment file
cp .env.example .env

# Edit .env with your configuration
nano .env

# Start services with Docker Compose
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f backend
```

### 2. Production Deployment

#### Prerequisites
- Docker and Docker Compose installed
- SSL certificates (for HTTPS)
- Domain name configured
- Firewall rules configured
- Environment variables set

#### Deployment Steps

```bash
# 1. Prepare environment
cp .env.example .env
nano .env  # Set production values

# 2. Generate SSL certificates (using Let's Encrypt)
certbot certonly --standalone -d yourdomain.com

# 3. Copy SSL certificates to docker/nginx/ssl/
mkdir -p docker/nginx/ssl
cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem docker/nginx/ssl/
cp /etc/letsencrypt/live/yourdomain.com/privkey.pem docker/nginx/ssl/

# 4. Build and start production services
docker-compose -f docker-compose.prod.yml up -d --build

# 5. Verify deployment
docker-compose -f docker-compose.prod.yml ps
curl https://yourdomain.com/health
```

### 3. Database Initialization

```bash
# Run database initialization scripts
docker-compose exec backend python -m app.db.init_db

# Initialize Neo4j with constraints and indexes
docker-compose exec backend python -m app.graph.init_graph
```

## Health Checks

### Backend Health Check

**Endpoint**: `/health`

```python
{
    "status": "healthy",
    "timestamp": "2024-01-15T10:30:00Z",
    "services": {
        "mongodb": "connected",
        "neo4j": "connected",
        "llm": "available"
    },
    "version": "1.0.0"
}
```

### Database Health Checks

```bash
# MongoDB health check
docker-compose exec mongodb mongosh --eval "db.adminCommand('ping')"

# Neo4j health check
docker-compose exec neo4j cypher-shell -u neo4j -p password "RETURN 1"
```

## Backup Strategy

### MongoDB Backup

```bash
# Create backup
docker-compose exec mongodb mongodump --uri="mongodb://admin:password@localhost:27017" --out=/backup/$(date +%Y%m%d)

# Restore backup
docker-compose exec mongodb mongorestore --uri="mongodb://admin:password@localhost:27017" /backup/20240115
```

### Neo4j Backup

```bash
# Create backup
docker-compose exec neo4j neo4j-admin database dump neo4j --to-path=/backup/$(date +%Y%m%d)

# Restore backup
docker-compose exec neo4j neo4j-admin database load neo4j --from-path=/backup/20240115
```

### Automated Backup Script

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backup/cybercortex"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR/$DATE

# MongoDB backup
docker-compose exec -T mongodb mongodump --uri="mongodb://$MONGO_USER:$MONGO_PASSWORD@localhost:27017" --out=/data/backup/$DATE/mongodb

# Neo4j backup
docker-compose exec -T neo4j neo4j-admin database dump neo4j --to-path=/data/backup/$DATE/neo4j

# Compress backup
tar -czf $BACKUP_DIR/cybercortex_$DATE.tar.gz -C /data/backup $DATE

# Remove old backups (keep last 7 days)
find $BACKUP_DIR -name "cybercortex_*.tar.gz" -mtime +7 -delete
```

## Monitoring

### Application Monitoring

#### Metrics Collection
- API response times
- Request rates
- Error rates
- Agent execution times
- Database query times

#### Logging
- Structured JSON logging
- Log aggregation (ELK stack or Loki)
- Centralized log management

#### Alerting
- Service downtime alerts
- High error rate alerts
- Performance degradation alerts
- Security incident alerts

### Database Monitoring

#### MongoDB Monitoring
- Connection pool status
- Query performance
- Index usage
- Replication lag
- Disk usage

#### Neo4j Monitoring
- Query performance
- Memory usage
- Transaction rates
- Graph size

## Scaling Strategy

### Horizontal Scaling

#### Backend Scaling
```bash
# Scale backend to 4 instances
docker-compose up -d --scale backend=4
```

#### Load Balancing
- Use Nginx as load balancer
- Round-robin or least-connections algorithm
- Health checks for backend instances

### Vertical Scaling

#### Resource Allocation
- Increase CPU cores for ML model training
- Increase memory for graph operations
- Optimize database connections

### Database Scaling

#### MongoDB
- Use replica sets for high availability
- Shard collections for large datasets
- Use read replicas for reporting queries

#### Neo4j
- Use Neo4j clustering for high availability
- Partition large graphs
- Optimize queries and indexes

## Security Hardening

### 1. Network Security
- Use private networks for database communication
- Configure firewall rules
- Use TLS/SSL for all communications
- Implement network segmentation

### 2. Application Security
- Enable HTTPS with valid SSL certificates
- Implement rate limiting
- Use secure headers (CSP, HSTS, X-Frame-Options)
- Regular security updates

### 3. Database Security
- Enable authentication
- Use strong passwords
- Implement role-based access control
- Regular backups
- Encrypt sensitive data at rest

### 4. Secret Management
- Use environment variables for secrets
- Consider using HashiCorp Vault for production
- Rotate secrets regularly
- Never commit secrets to version control

## CI/CD Pipeline

### GitHub Actions Example

**File**: `.github/workflows/deploy.yml`

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Build and push frontend
        uses: docker/build-push-action@v4
        with:
          context: .
          file: ./docker/Dockerfile.frontend
          push: true
          tags: yourusername/cybercortex-frontend:latest
      
      - name: Build and push backend
        uses: docker/build-push-action@v4
        with:
          context: .
          file: ./docker/Dockerfile.backend
          push: true
          tags: yourusername/cybercortex-backend:latest
      
      - name: Deploy to server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /opt/CyberCortexAI
            docker-compose -f docker-compose.prod.yml pull
            docker-compose -f docker-compose.prod.yml up -d
```

## Troubleshooting

### Common Issues

#### 1. Container won't start
```bash
# Check logs
docker-compose logs backend

# Check resource usage
docker stats

# Restart service
docker-compose restart backend
```

#### 2. Database connection failed
```bash
# Check database status
docker-compose ps mongodb
docker-compose ps neo4j

# Verify connectivity
docker-compose exec backend python -c "from app.db.mongodb import mongo_client; print(mongo_client.admin.command('ping'))"
```

#### 3. High memory usage
```bash
# Check memory usage
docker stats

# Limit container memory
# Add to docker-compose.yml:
# mem_limit: 2g
```

#### 4. Slow performance
```bash
# Check database indexes
docker-compose exec mongodb mongosh --eval "db.alerts.getIndexes()"

# Check slow queries
docker-compose exec mongodb mongosh --eval "db.currentOp()"

# Optimize queries
# Add appropriate indexes
```

## Performance Optimization

### 1. Frontend Optimization
- Enable code splitting
- Lazy load components
- Optimize images
- Use CDN for static assets
- Enable compression

### 2. Backend Optimization
- Use async operations
- Implement caching
- Optimize database queries
- Use connection pooling
- Enable response compression

### 3. Database Optimization
- Create appropriate indexes
- Use connection pooling
- Implement query optimization
- Use read replicas
- Archive old data

## Maintenance

### Regular Tasks

1. **Daily**
   - Monitor system health
   - Check error logs
   - Review security alerts

2. **Weekly**
   - Review performance metrics
   - Check backup integrity
   - Review system logs

3. **Monthly**
   - Apply security updates
   - Review and optimize indexes
   - Test disaster recovery
   - Review storage capacity

4. **Quarterly**
   - Review and update documentation
   - Conduct security audit
   - Review and update dependencies
   - Capacity planning

## Disaster Recovery

### Recovery Procedures

1. **Data Recovery**
   - Restore from backups
   - Verify data integrity
   - Test application functionality

2. **Service Recovery**
   - Restart services
   - Verify connectivity
   - Monitor performance

3. **Complete System Recovery**
   - Restore from full backup
   - Reconfigure services
   - Test all functionality
   - Update documentation

## Documentation Maintenance

Keep this deployment document updated with:
- Architecture changes
- New deployment procedures
- Troubleshooting solutions
- Security updates
- Performance optimizations
