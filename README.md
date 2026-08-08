# CyberCortex AI

An AI-driven Security Operations Center (SOC) platform for intelligent cyber threat detection, analysis, and prediction.

## Overview

CyberCortex AI is a professional, deployable SOC platform that uses a cognitive multi-agent AI framework to analyze security threats, correlate events from multiple data sources, maintain a dynamic knowledge graph, provide explainable AI insights, and predict potential attack paths.

## Core Objectives

1. **Multi-Agent AI Framework**: Cognitive multi-agent system for intelligent threat detection and analysis
2. **Event Analysis**: Real-time security log analysis and event correlation from multiple data sources
3. **Knowledge Graph**: Dynamic graph modeling relationships between users, devices, vulnerabilities, and attacks
4. **Explainable AI**: Transparent threat analysis with actionable security recommendations
5. **Attack Path Prediction**: ML-powered prediction of potential attack paths for faster SOC decision-making

## Technology Stack

### Frontend
- React 18+ with TypeScript
- Vite (build tool)
- Tailwind CSS (styling)
- React Router (navigation)
- React Flow (graph visualization)
- Recharts (analytics charts)

### Backend
- FastAPI (Python 3.12)
- Pydantic (validation)
- MongoDB (document store)
- Neo4j (graph database)
- scikit-learn (ML models)
- OpenAI API (LLM integration)

### Infrastructure
- Docker (containerization)
- Docker Compose (orchestration)
- Nginx (reverse proxy)

## Architecture

```
Security Data Sources → Event Ingestion → Normalization → Correlation
                                                                  ↓
Agent Coordinator → Specialized Agents → Collaborative Reasoning
                                                                  ↓
               Security Memory (MongoDB) ← → Knowledge Graph (Neo4j)
                                                                  ↓
                     Risk Prediction → Attack Path Prediction
                                                                  ↓
                   Explainability Engine → Response Recommender
                                                                  ↓
                         SOC Dashboard (React + TypeScript)
```

## Features

### Threat Operations
- Real-time event ingestion from multiple sources
- Event normalization and correlation
- Alert generation and management
- Incident workflow and investigation

### AI Operations
- Multi-agent threat analysis
- Agent activity monitoring
- Collaborative reasoning
- AI-driven recommendations

### Intelligence
- Threat intelligence integration
- IOC explorer
- MITRE ATT&CK mapping
- Vulnerability intelligence
- Security memory

### Graph Intelligence
- Interactive knowledge graph
- Attack path discovery
- Blast radius analysis
- Asset relationship mapping

### Analytics
- Risk analytics
- Prediction analytics
- Model confidence tracking
- Custom reports

## Documentation

- [Architecture](docs/ARCHITECTURE.md) - High-level system architecture
- [Frontend Architecture](docs/FRONTEND_ARCHITECTURE.md) - Frontend design and components
- [Backend Architecture](docs/BACKEND_ARCHITECTURE.md) - Backend API and services
- [MongoDB Design](docs/MONGODB_DESIGN.md) - Database schema and collections
- [Neo4j Graph Model](docs/NEO4J_GRAPH_MODEL.md) - Knowledge graph schema
- [Multi-Agent Architecture](docs/MULTI_AGENT_ARCHITECTURE.md) - AI agent framework
- [ML Architecture](docs/ML_ARCHITECTURE.md) - Machine learning pipeline
- [Deployment](docs/DEPLOYMENT.md) - Deployment guide and Docker setup
- [Development Plan](docs/DEVELOPMENT_PLAN.md) - 14-phase development roadmap
- [Objective Traceability](docs/OBJECTIVE_TRACEABILITY.md) - Objective-to-implementation mapping

## Development Phases

1. **Phase 0**: Planning and Architecture Foundation ✅
2. **Phase 1**: Frontend Foundation and Design System ✅
3. **Phase 2**: Backend Foundation and Authentication ✅
4. **Phase 3**: Event Ingestion, Normalization, and Correlation ✅
5. **Phase 4**: Alerts, Incidents, and Investigation Workflow
6. **Phase 5**: Multi-Agent AI Framework
7. **Phase 6**: Security Memory
8. **Phase 7**: Neo4j Knowledge Graph
9. **Phase 8**: Threat Intelligence, MITRE, and Vulnerability Intelligence
10. **Phase 9**: ML Risk Prediction and Attack Path Prediction
11. **Phase 10**: Explainable AI and Recommendation Engine
12. **Phase 11**: Real-time Updates and Advanced Analytics
13. **Phase 12**: Testing, Security Hardening, and Performance
14. **Phase 13**: Dockerization and Deployment
15. **Phase 14**: Professional Polish, Final Documentation, and Project Demonstration

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.12+ (for local backend development)
- MongoDB 7.0+
- Neo4j 5.14+

### Quick Start with Docker

```bash
# Clone the repository
git clone https://github.com/yourusername/CyberCortexAI.git
cd CyberCortexAI

# Copy environment files
cp .env.example .env
cp frontend/.env.example frontend/.env

# Edit .env with your configuration
nano .env

# Start MongoDB (Phase 2/3)
docker-compose up -d

# Create database indexes (from backend directory)
cd backend
python -m app.database.indexes

# Seed demo data (optional)
python scripts/seed_demo_data.py

# Start backend
uvicorn app.main:app --reload

# In another terminal, start frontend
cd ../frontend
npm install
npm run dev

## Phase 3 - Security Analytics Pipeline

Phase 3 implements the core security analytics pipeline with multi-source log ingestion, normalization, correlation, and deterministic threat detection.

### Ingestion API

```bash
# Upload a log file via API
curl -X POST "http://localhost:8000/api/v1/ingestion/upload" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@data/samples/attack_scenario.jsonl" \
  -F "source_type=json"

# Get ingestion statistics
curl -X GET "http://localhost:8000/api/v1/ingestion/stats" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Sample Datasets

Located in `data/samples/`:
- `normal_activity.jsonl` - Normal user activity (10 events)
- `attack_scenario.jsonl` - Synthetic attack scenario (24 events)

### Detection Rules Implemented

1. **Brute Force Detection** (T1110) - Detects repeated failed authentication
2. **Success After Failures** (T1078, T1110) - Detects successful login after failures
3. **Port Scan Detection** (T1046, T1018) - Detects port scanning activity
4. **Multiple Host Scan** (T1018) - Detects scanning across multiple hosts
5. **Suspicious PowerShell** (T1059.001) - Detects obfuscated PowerShell
6. **Privileged Group Modification** (T1098) - Detects sensitive group changes
7. **New Account + Privilege Escalation** (T1136, T1098) - Detects account creation followed by privilege escalation
8. **Account Lockout Burst** (T1110) - Detects unusual lockout patterns
```

### Local Development

#### Backend (Phase 2 - FastAPI + MongoDB)
```bash
cd backend
pip install -r requirements.txt
# Create .env file from .env.example
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
# Create .env file with VITE_API_BASE_URL=http://localhost:8000
npm run dev
```

## Project Status

**Current Phase**: Phase 4 - Alerts, Incidents, and Investigation Workflow (Ready to Start)

**Progress**: 35% (Phases 0, 1, 2, and 3 complete: Planning, Frontend Foundation, Backend Foundation, and Security Analytics Pipeline)

**Estimated Timeline**: 60-90 days

### Completed Phases
- **Phase 0**: Planning and Architecture Foundation ✅
- **Phase 1**: Frontend Foundation and Design System ✅
- **Phase 2**: Backend Foundation and Authentication ✅
- **Phase 3**: Event Ingestion, Normalization, and Correlation ✅

### Phase 3 Status
- ✅ Log parsers for Windows, Linux, Firewall, JSON
- ✅ Event normalizers for all source types
- ✅ Event enrichment (IP classification, entity extraction)
- ✅ Correlation engine (time-window, entity-based)
- ✅ Detection engine with 8 deterministic rules
- ✅ Alert generation with deduplication
- ✅ Incident grouping service
- ✅ Ingestion API endpoints
- ✅ MongoDB indexes for correlation
- ✅ Sample datasets (normal and attack scenarios)
- ⏳ Frontend Events page integration
- ⏳ Frontend Alerts page integration
- ⏳ Alert Evidence UI
- ⏳ Log Ingestion UI
- ⏳ Unit and integration tests

### Current Focus
- Phase 4: Alerts, Incidents, and Investigation Workflow (Next)

## Contributing

This is an academic project for B.Tech final year. Contributions are currently limited to the project team.

## License

This project is developed for academic purposes. Please contact the authors for permission to use.

## Authors

- [Your Name] - B.Tech Final Year Student
- [Academic Guide] - Project Guide

## Acknowledgments

- AiSOC - Architectural reference for multi-agent security systems
- MITRE ATT&CK - Cybersecurity knowledge base
- Open Source Community - Tools and frameworks used

---

**Last Updated**: 2026-08-01
