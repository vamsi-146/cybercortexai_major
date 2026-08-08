# CyberCortex AI - System Architecture

## Overview

CyberCortex AI is an AI-driven Security Operations Center (SOC) platform that uses a multi-agent AI framework to detect, analyze, and predict cyber threats. The system processes security events from multiple sources, correlates them using a knowledge graph, and provides explainable AI-driven insights to security analysts.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Security Data Sources                    │
│  Windows Logs │ Firewall │ IDS/EDR │ SIEM │ Cloud │ Applications │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            v
┌─────────────────────────────────────────────────────────────────┐
│                        Event Ingestion Layer                     │
│                  (Async Event Processing Pipeline)               │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            v
┌─────────────────────────────────────────────────────────────────┐
│                       Normalization Layer                        │
│            (Standard Event Schema & Enrichment)                  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            v
┌─────────────────────────────────────────────────────────────────┐
│                      Correlation Engine                           │
│         (Event Correlation & Alert Generation)                   │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            v
┌─────────────────────────────────────────────────────────────────┐
│                      Agent Coordinator                           │
│         (Agent Selection & Orchestration)                        │
└──────┬──────────────────────┬──────────────────────┬────────────┘
       │                      │                      │
       v                      v                      v
┌──────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│ Identity     │    │ Threat           │    │ Vulnerability       │
│ Analysis     │    │ Intelligence     │    │ Analysis            │
│ Agent        │    │ Agent            │    │ Agent               │
└──────┬───────┘    └────────┬─────────┘    └──────────┬──────────┘
       │                     │                         │
       └─────────────────────┴─────────────────────────┘
                             │
                             v
                ┌────────────────────────┐
                │ Investigation Agent    │
                │ (Orchestration)        │
                └───────────┬────────────┘
                            │
                            v
┌─────────────────────────────────────────────────────────────────┐
│                  Collaborative Reasoning Engine                 │
│            (Combine & Resolve Agent Findings)                    │
└──────┬──────────────────────────────┬───────────────────────────┘
       │                              │
       v                              v
┌──────────────────┐        ┌──────────────────┐
│ Security Memory  │        │ Knowledge Graph  │
│ (MongoDB)        │        │ (Neo4j)          │
└──────────────────┘        └─────────┬────────┘
                                      │
                                      v
┌─────────────────────────────────────────────────────────────────┐
│                    Risk Prediction Engine                        │
│              (ML Models for Risk & Attack Paths)                 │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            v
┌─────────────────────────────────────────────────────────────────┐
│                 Attack Path Prediction Engine                   │
│            (Graph Analysis + ML Prediction)                      │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            v
┌─────────────────────────────────────────────────────────────────┐
│                   Explainability Engine                          │
│        (Evidence, MITRE Mapping, Rationale Generation)           │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            v
┌─────────────────────────────────────────────────────────────────┐
│                  Response Recommender                            │
│           (Actionable Security Recommendations)                  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            v
┌─────────────────────────────────────────────────────────────────┐
│                      SOC Dashboard                               │
│         (React + TypeScript Frontend)                            │
└─────────────────────────────────────────────────────────────────┘
```

## Architecture Layers

### 1. Data Layer

**Purpose**: Store and manage all data for the system.

**Components**:
- **MongoDB**: Document store for structured data
  - Users, alerts, incidents, investigations
  - Security events, agent findings
  - Security memory, recommendations
  - Audit logs, detection rules

- **Neo4j**: Graph database for relationships
  - Users, devices, IPs, IOCs
  - Vulnerabilities, attacks, MITRE techniques
  - Relationships for attack path analysis

**Key Design Decisions**:
- MongoDB for high-volume event storage and flexible document schema
- Neo4j for complex relationship queries and graph traversals
- Async drivers for both databases (Motor, neo4j-driver)
- Connection pooling for performance

---

### 2. Ingestion Layer

**Purpose**: Ingest security events from multiple data sources.

**Components**:
- **Event Ingestion Service**: Accept events from various sources
- **Normalization Service**: Convert events to standard schema
- **Enrichment Service**: Add context (geo-location, threat intel)
- **Correlation Engine**: Correlate related events
- **Alert Generation**: Generate alerts from correlations

**Key Design Decisions**:
- Async processing for high throughput
- Standard event schema for consistency
- Pluggable data source connectors
- Real-time correlation where possible

---

### 3. AI Layer

**Purpose**: Multi-agent AI framework for threat analysis.

**Components**:
- **Agent Coordinator**: Route and orchestrate agents
- **Specialized Agents**:
  - Identity Analysis Agent
  - Threat Intelligence Agent
  - Vulnerability Analysis Agent
  - Investigation Agent
- **Collaborative Reasoning Engine**: Combine agent findings
- **LLM Integration**: Generate explanations and narratives

**Key Design Decisions**:
- Base agent class for consistency
- Parallel execution for independent agents
- Collaborative reasoning with conflict resolution
- LLM abstraction for provider flexibility

---

### 4. Intelligence Layer

**Purpose**: Provide context and historical knowledge.

**Components**:
- **Security Memory**: Store and retrieve historical context
- **Knowledge Graph**: Model security relationships
- **Threat Intelligence**: IOC and threat feed integration
- **MITRE ATT&CK**: Technique mapping and reference
- **Vulnerability Intelligence**: CVE and exploit data

**Key Design Decisions**:
- Security memory for analyst learning
- Knowledge graph for relationship analysis
- MITRE ATT&CK for standardization
- Enrichment from external threat intel

---

### 5. Prediction Layer

**Purpose**: Predict risk and attack progression.

**Components**:
- **Feature Engineering**: Extract features from events and graph
- **Risk Prediction Model**: Predict risk scores
- **Attack Path Prediction**: Predict attack progression
- **Model Training Pipeline**: Train and evaluate models
- **Model Monitoring**: Track model performance and drift

**Key Design Decisions**:
- Traditional ML for interpretability
- Feature engineering from multiple sources
- Model versioning and monitoring
- Scheduled retraining

---

### 6. Explainability Layer

**Purpose**: Make AI decisions transparent and explainable.

**Components**:
- **Explainability Engine**: Generate explanations
- **Evidence Aggregator**: Collect and structure evidence
- **MITRE Mapper**: Map findings to MITRE techniques
- **Response Recommender**: Generate actionable recommendations
- **Explanation Generator**: Natural language explanations

**Key Design Decisions**:
- Evidence-based explanations
- MITRE ATT&CK mapping for standardization
- Confidence scores for transparency
- Rationale for all recommendations

---

### 7. Application Layer

**Purpose**: Business logic and API endpoints.

**Components**:
- **FastAPI Application**: RESTful API
- **Authentication**: JWT-based auth with RBAC
- **Authorization**: Role-based access control
- **API Endpoints**: Organized by domain
- **Middleware**: Logging, validation, error handling

**Key Design Decisions**:
- FastAPI for async performance
- JWT for stateless authentication
- RBAC for authorization
- Pydantic for validation
- OpenAPI for documentation

---

### 8. Presentation Layer

**Purpose**: User interface for SOC analysts.

**Components**:
- **React Application**: Modern SPA
- **TypeScript**: Type safety
- **Tailwind CSS**: Styling with CyberCortex theme
- **React Router**: Navigation
- **React Flow**: Graph visualization
- **Recharts**: Analytics charts

**Key Design Decisions**:
- Component-based architecture
- Custom hooks for reusable logic
- Context for global state
- Real-time updates with WebSocket
- Professional cyber-defense UI

---

## Data Flow

### Event Processing Flow

```
1. Event Ingestion
   Security Event → Ingestion Service → Raw Event

2. Normalization
   Raw Event → Normalization Service → Normalized Event

3. Enrichment
   Normalized Event → Enrichment Service → Enriched Event

4. Correlation
   Enriched Event → Correlation Engine → Correlated Events

5. Alert Generation
   Correlated Events → Alert Generation → Alert

6. Agent Analysis
   Alert → Agent Coordinator → Specialized Agents → Agent Findings

7. Collaborative Reasoning
   Agent Findings → Collaborative Reasoning → Combined Findings

8. Knowledge Graph Update
   Event Data → Graph Builder → Neo4j Graph

9. Security Memory Update
   Incident/Findings → Security Memory → MongoDB

10. Explanation Generation
    Combined Findings → Explainability Engine → Explanation

11. Recommendation Generation
    Combined Findings → Response Recommender → Recommendations

12. UI Display
    Alert/Incident/Explanation → Frontend → SOC Dashboard
```

### Investigation Flow

```
1. Trigger Investigation
   Alert/Manual → Investigation API → Investigation Created

2. Agent Coordination
   Investigation → Agent Coordinator → Agents Selected

3. Agent Execution
   Agent Coordinator → Parallel Agent Execution → Agent Results

4. Collaborative Reasoning
   Agent Results → Collaborative Reasoning Engine → Unified Findings

5. Context Retrieval
   Investigation → Security Memory → Historical Context
   Investigation → Knowledge Graph → Graph Context

6. Explanation Generation
   Findings + Context → Explainability Engine → Explanation

7. Prediction
   Investigation Context → ML Models → Risk/Attack Path Predictions

8. Recommendation
   Findings + Predictions → Response Recommender → Recommendations

9. Update Investigation
   All Results → Investigation Updated → Investigation Complete

10. Update Security Memory
    Investigation Results → Security Memory → New Memory Entry
```

---

## Technology Stack

### Frontend
- **Framework**: React 18+ with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Routing**: React Router v6
- **State**: React Context + React Query
- **Graph**: React Flow
- **Charts**: Recharts
- **HTTP**: Axios

### Backend
- **Framework**: FastAPI (Python 3.12)
- **Async**: asyncio + uvicorn
- **Validation**: Pydantic v2
- **MongoDB**: Motor (async driver)
- **Neo4j**: neo4j-driver
- **ML**: scikit-learn, pandas, numpy
- **LLM**: OpenAI API (abstracted)

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **Web Server**: Nginx
- **Process Manager**: Gunicorn

---

## Key Architectural Patterns

### 1. Layered Architecture
Clear separation of concerns across layers (data, ingestion, AI, application, presentation).

### 2. Event-Driven Architecture
Async event processing pipeline for high throughput and real-time analysis.

### 3. Multi-Agent Architecture
Specialized agents that collaborate to analyze complex security scenarios.

### 4. Repository Pattern
Data access abstraction for MongoDB and Neo4j.

### 5. Service Layer Pattern
Business logic separated from API controllers.

### 6. Dependency Injection
Components receive dependencies through constructor injection.

### 7. Strategy Pattern
Pluggable algorithms for correlation, reasoning, and prediction.

### 8. Observer Pattern
WebSocket updates for real-time UI synchronization.

---

## Security Architecture

### Authentication
- JWT-based stateless authentication
- Access tokens (15 min) + Refresh tokens (7 days)
- bcrypt password hashing
- Optional MFA support

### Authorization
- Role-Based Access Control (RBAC)
- Roles: ADMIN, SOC_ANALYST, SECURITY_ENGINEER, VIEWER
- Permission-based endpoint protection
- User context injection

### Data Security
- MongoDB authentication enabled
- Neo4j authentication enabled
- TLS for database connections
- Input validation with Pydantic
- SQL/NoSQL injection prevention
- XSS prevention

### Audit
- Audit logging for all security operations
- Immutable audit trail
- Log aggregation readiness

---

## Scalability Architecture

### Horizontal Scaling
- Stateless API servers (can add more instances)
- Load balancer (Nginx)
- Database read replicas (MongoDB)
- Neo4j clustering (Enterprise)

### Vertical Scaling
- Resource allocation based on workload
- ML model training on dedicated resources
- Graph operations optimized with indexing

### Performance Optimization
- Async operations throughout
- Connection pooling
- Query optimization
- Caching (Redis optional)
- CDN for static assets

---

## Extensibility Architecture

### Adding New Agents
1. Inherit from BaseAgent class
2. Implement analyze() method
3. Register with Agent Coordinator
4. Add routing rules
5. No changes to existing agents

### Adding New Data Sources
1. Implement source connector
2. Add normalization logic
3. Register with ingestion service
4. Add to detection rules
5. No changes to existing sources

### Adding New ML Models
1. Implement model class
2. Add to training pipeline
3. Register with prediction service
4. Add to monitoring
5. No changes to existing models

---

## Monitoring Architecture

### Application Monitoring
- Structured JSON logging
- API response time metrics
- Error rate tracking
- Agent execution metrics

### Database Monitoring
- MongoDB query performance
- Neo4j query performance
- Connection pool status
- Storage usage

### System Monitoring
- CPU, memory, disk usage
- Network metrics
- Container health
- Service uptime

---

## Deployment Architecture

### Development
- Local development with Docker Compose
- Hot reload for frontend and backend
- Local MongoDB and Neo4j instances

### Production
- Containerized deployment
- Nginx reverse proxy
- Multiple backend workers
- Database replicas
- SSL/TLS encryption
- Automated backups
- CI/CD pipeline

---

## Integration Points

### External Integrations
- **Threat Intelligence Feeds**: VirusTotal, AlienVault, etc.
- **MITRE ATT&CK**: MITRE ATT&CK database
- **CVE Database**: NVD (National Vulnerability Database)
- **LLM Provider**: OpenAI, Anthropic (abstracted)

### Internal Integrations
- **Frontend ↔ Backend**: REST API + WebSocket
- **Backend ↔ MongoDB**: Motor async driver
- **Backend ↔ Neo4j**: neo4j-driver
- **Agents ↔ Security Memory**: MongoDB queries
- **Agents ↔ Knowledge Graph**: Neo4j queries
- **ML Models ↔ Prediction Service**: Python function calls

---

## Failure Handling

### Graceful Degradation
- LLM unavailability: Use template-based explanations
- Neo4j unavailability: Use MongoDB-only analysis
- ML model failure: Use rule-based fallback
- WebSocket failure: Fallback to polling

### Error Handling
- Comprehensive exception handling
- User-friendly error messages
- Error logging and monitoring
- Automatic retry for transient failures

### Data Consistency
- Transactions for multi-document operations
- Optimistic concurrency for updates
- Data validation on all writes
- Periodic consistency checks

---

## Architecture Principles

1. **Modularity**: Components are independent and loosely coupled
2. **Scalability**: Architecture supports horizontal and vertical scaling
3. **Extensibility**: New features can be added without modifying existing code
4. **Security**: Security is built into every layer
5. **Performance**: Async operations and optimization throughout
6. **Observability**: Comprehensive logging and monitoring
7. **Testability**: Clear separation enables comprehensive testing
8. **Documentation**: Architecture is well-documented and maintainable

---

## Related Documentation

- [Frontend Architecture](FRONTEND_ARCHITECTURE.md)
- [Backend Architecture](BACKEND_ARCHITECTURE.md)
- [MongoDB Design](MONGODB_DESIGN.md)
- [Neo4j Graph Model](NEO4J_GRAPH_MODEL.md)
- [Multi-Agent Architecture](MULTI_AGENT_ARCHITECTURE.md)
- [ML Architecture](ML_ARCHITECTURE.md)
- [Deployment](DEPLOYMENT.md)
- [Development Plan](DEVELOPMENT_PLAN.md)
- [Objective Traceability](OBJECTIVE_TRACEABILITY.md)

---

**Last Updated**: 2026-08-01 (Phase 0 - Planning)
