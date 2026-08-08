# CyberCortex AI - Backend Architecture

## Technology Stack

- **Framework**: FastAPI (Python 3.12)
- **Async Runtime**: asyncio + uvicorn
- **Data Validation**: Pydantic v2
- **Database (Document)**: MongoDB with Motor (async driver) - Phase 2: Implemented
- **Database (Graph)**: Neo4j with neo4j-driver - Phase 7
- **Authentication**: JWT + bcrypt - Phase 2: Implemented
- **LLM Integration**: OpenAI API (abstracted for provider flexibility) - Phase 5
- **ML**: scikit-learn, pandas, numpy - Phase 9
- **Testing**: pytest, pytest-asyncio - Phase 12
- **API Documentation**: OpenAPI/Swagger (built-in with FastAPI) - Phase 2: Available

## Architecture Pattern

### Layered Architecture

```
main.py (FastAPI Application)
    ↓
API Layer (app/api/)
    ↓
Service Layer (app/services/)
    ↓
Repository Layer (app/db/repositories/)
    ↓
Database Layer (MongoDB / Neo4j)
```

### Alternative Flow for AI Operations

```
API Layer
    ↓
Agent Coordinator (app/agents/coordinator.py)
    ↓
Specialized Agents (app/agents/)
    ↓
Collaborative Reasoning Engine
    ↓
Knowledge Graph + Security Memory
    ↓
Explainability Engine
    ↓
Response Generation
```

## Project Structure

```
backend/
├── app/
│   ├── main.py                    # FastAPI application factory
│   ├── config.py                  # Configuration management
│   ├── dependencies.py            # Dependency injection
│   │
│   ├── core/                      # Core functionality
│   │   ├── security.py            # JWT, password hashing, RBAC
│   │   ├── logging.py             # Structured logging
│   │   ├── llm.py                 # LLM abstraction layer
│   │   └── exceptions.py          # Custom exceptions
│   │
│   ├── models/                    # Pydantic models
│   │   ├── user.py                # User, Role, Permission
│   │   ├── alert.py               # Alert, AlertUpdate
│   │   ├── incident.py            # Incident, IncidentUpdate
│   │   ├── investigation.py       # Investigation, AgentFinding
│   │   ├── event.py               # SecurityEvent, NormalizedEvent
│   │   ├── graph.py               # GraphNode, GraphRelationship
│   │   └── common.py              # Common schemas
│   │
│   ├── api/                       # API routes
│   │   ├── __init__.py
│   │   ├── auth.py                # Login, logout, token refresh
│   │   ├── alerts.py              # Alert CRUD, filtering
│   │   ├── incidents.py           # Incident CRUD, workflow
│   │   ├── investigations.py      # Investigation triggers, status
│   │   ├── agents.py              # Agent status, results
│   │   ├── graph.py               # Graph queries, visualization
│   │   ├── intelligence.py        # Threat intel, IOCs, MITRE
│   │   ├── analytics.py           # Risk analytics, predictions
│   │   └── admin.py               # Users, audit logs, settings
│   │
│   ├── services/                  # Business logic
│   │   ├── ingestion.py           # Event ingestion from data sources
│   │   ├── normalization.py       # Event normalization to standard format
│   │   ├── correlation.py         # Event correlation and alert generation
│   │   ├── explainability.py     # Explainability engine
│   │   ├── recommendation.py      # Response recommendation engine
│   │   └── security_memory.py    # Security memory retrieval
│   │
│   ├── agents/                    # Multi-agent AI framework
│   │   ├── coordinator.py         # Agent coordinator and router
│   │   ├── base_agent.py          # Base agent class
│   │   ├── identity_agent.py      # Identity analysis agent
│   │   ├── threat_intel_agent.py  # Threat intelligence agent
│   │   ├── vulnerability_agent.py # Vulnerability analysis agent
│   │   └── investigation_agent.py # Investigation orchestration agent
│   │
│   ├── db/                        # MongoDB operations
│   │   ├── mongodb.py             # MongoDB connection and client
│   │   └── repositories/
│   │       ├── user_repository.py
│   │       ├── alert_repository.py
│   │       ├── incident_repository.py
│   │       ├── investigation_repository.py
│   │       ├── event_repository.py
│   │       └── security_memory_repository.py
│   │
│   ├── graph/                     # Neo4j operations
│   │   ├── neo4j.py               # Neo4j connection and driver
│   │   ├── graph_queries.py       # Common graph queries
│   │   └── graph_builder.py       # Graph construction logic
│   │
│   ├── ml/                        # ML models and pipeline
│   │   ├── models.py              # ML model definitions
│   │   ├── training.py            # Training pipeline
│   │   ├── prediction.py          # Prediction service
│   │   └── evaluation.py          # Model evaluation
│   │
│   └── utils/                     # Utility functions
│       ├── date_utils.py
│       ├── validation.py
│       └── helpers.py
│
├── tests/                         # Tests
│   ├── conftest.py                # Test fixtures
│   ├── test_api/
│   ├── test_services/
│   ├── test_agents/
│   └── test_ml/
│
├── main.py                        # Application entry point
├── requirements.txt               # Python dependencies
├── pyproject.toml                 # Project configuration
└── .env.example                   # Environment variables template
```

## API Design Principles

### RESTful Conventions
- Use HTTP verbs appropriately (GET, POST, PUT, PATCH, DELETE)
- Resource-based URLs (e.g., `/api/v1/alerts/{alert_id}`)
- Consistent response formats
- Proper status codes
- Pagination for list endpoints
- Filtering and sorting support

### Response Format
```python
{
    "success": true,
    "data": {...},
    "message": "Operation successful",
    "metadata": {
        "total": 100,
        "page": 1,
        "per_page": 20
    }
}
```

### Error Response Format
```python
{
    "success": false,
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid input data",
        "details": [...]
    }
}
```

### Versioning
- URL-based versioning: `/api/v1/...`
- Maintain backward compatibility within major versions

## Security Architecture

### Authentication
- JWT-based authentication
- Access tokens (short-lived: 15 minutes)
- Refresh tokens (long-lived: 7 days)
- Token rotation on refresh
- Secure token storage (httpOnly cookies preferred)

### Authorization
- Role-Based Access Control (RBAC)
- Roles: ADMIN, SOC_ANALYST, SECURITY_ENGINEER, VIEWER
- Permission-based endpoint protection
- User-context injection via dependencies

### Input Validation
- Pydantic models for all inputs
- SQL injection prevention (parameterized queries)
- NoSQL injection prevention
- XSS prevention (output encoding)
- CSRF protection (token validation)

### Rate Limiting
- Per-endpoint rate limits
- Per-user rate limits
- IP-based blocking for abuse

### Audit Logging
- Log all authentication events
- Log all authorization changes
- Log all data modifications
- Log all admin actions
- Immutable audit trail

## Database Architecture

### MongoDB (Document Store)
- Used for: structured documents, time-series events, audit trails
- Collections: users, alerts, incidents, investigations, events, security_memory
- Indexes: strategic indexes for query performance
- Connection pooling: Motor async driver

### Neo4j (Graph Database)
- Used for: relationships, attack paths, blast radius, knowledge graph
- Nodes: User, Device, IP, IOC, Vulnerability, CVE, Attack, MITRETechnique
- Relationships: LOGGED_INTO, CONNECTED_TO, HAS_VULNERABILITY, EXPLOITS, etc.
- Queries: Cypher queries for graph traversals
- Connection pooling: neo4j-driver

## LLM Integration

### Abstraction Layer
```python
class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        pass

class OpenAIProvider(LLMProvider):
    # OpenAI implementation

class AnthropicProvider(LLMProvider):
    # Anthropic implementation
```

### Configuration-Based Selection
- Provider selected via environment configuration
- Easy to switch providers without code changes
- Support for different models per use case

### Use Cases
- Investigation narrative generation
- Explanation generation
- Recommendation justification
- Threat intelligence summarization

## Async Architecture

### Async I/O Strategy
- Use FastAPI's async capabilities
- Async database drivers (Motor, neo4j-async)
- Async HTTP client (httpx)
- Concurrent agent execution

### Background Tasks
- Event ingestion
- Agent execution
- ML model training
- Report generation

### Task Queue (if needed)
- Celery or Dramatiq for heavy background tasks
- Redis as message broker
- Task result storage

## Performance Considerations

### Database Optimization
- Connection pooling
- Query optimization
- Index strategy
- Caching frequent queries (Redis optional)

### API Performance
- Response compression
- Pagination
- Field selection (sparse fieldsets)
- Async operations

### Caching Strategy
- Cache user permissions
- Cache frequently accessed reference data
- Cache ML model predictions
- TTL-based cache invalidation

## Monitoring and Observability

### Logging
- Structured JSON logging
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Contextual logging (request ID, user ID)
- Log aggregation readiness

### Metrics
- API response times
- Database query times
- Agent execution times
- Error rates
- System health checks

### Health Checks
- `/health` endpoint
- Database connectivity checks
- External service availability
- Dependency health

## Testing Strategy

### Unit Tests
- Service layer logic
- Repository layer
- Agent logic
- ML model training/inference

### Integration Tests
- API endpoints
- Database operations
- Graph operations
- Agent coordination

### E2E Tests
- Complete workflows
- Multi-agent scenarios
- Real-time updates

## Deployment Considerations

### Environment Configuration
- Development, staging, production environments
- Environment-specific settings
- Secret management (environment variables, vault)

### Scalability
- Horizontal scaling (multiple API instances)
- Database read replicas
- Graph database clustering
- Load balancing

### Backup and Recovery
- MongoDB backups
- Neo4j backups
- Point-in-time recovery
- Disaster recovery plan
