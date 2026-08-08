# CyberCortex AI - Repository Structure

## Root Directory Structure

```
CyberCortexAI/
├── frontend/                    # React TypeScript frontend
│   ├── src/
│   │   ├── components/          # Reusable UI components
│   │   ├── pages/              # Page-level components
│   │   ├── services/           # API clients and services
│   │   ├── hooks/              # Custom React hooks
│   │   ├── types/              # TypeScript type definitions
│   │   ├── utils/              # Utility functions
│   │   ├── context/            # React context providers
│   │   └── styles/             # Global styles and theme
│   ├── public/                 # Static assets
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
│
├── backend/                     # FastAPI Python backend
│   ├── app/
│   │   ├── agents/             # Multi-agent AI framework
│   │   │   ├── coordinator.py  # Agent coordinator
│   │   │   ├── identity_agent.py
│   │   │   ├── threat_intel_agent.py
│   │   │   ├── vulnerability_agent.py
│   │   │   └── investigation_agent.py
│   │   ├── api/                # API routes
│   │   │   ├── auth.py
│   │   │   ├── alerts.py
│   │   │   ├── incidents.py
│   │   │   ├── investigations.py
│   │   │   ├── agents.py
│   │   │   ├── graph.py
│   │   │   └── analytics.py
│   │   ├── core/               # Core functionality
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   ├── logging.py
│   │   │   └── llm.py
│   │   ├── db/                 # MongoDB operations
│   │   │   ├── mongodb.py
│   │   │   └── repositories/
│   │   ├── graph/              # Neo4j operations
│   │   │   ├── neo4j.py
│   │   │   └── graph_queries.py
│   │   ├── ml/                 # ML models and pipeline
│   │   │   ├── models.py
│   │   │   ├── training.py
│   │   │   └── prediction.py
│   │   ├── models/             # Pydantic models
│   │   │   ├── user.py
│   │   │   ├── alert.py
│   │   │   ├── incident.py
│   │   │   └── agent.py
│   │   └── services/           # Business logic
│   │       ├── ingestion.py
│   │       ├── normalization.py
│   │       ├── correlation.py
│   │       └── explainability.py
│   ├── tests/                  # Backend tests
│   ├── main.py                 # FastAPI application entry
│   ├── requirements.txt
│   └── pyproject.toml
│
├── tests/                      # Integration tests
│   ├── frontend/
│   └── e2e/
│
├── docker/                     # Docker configurations
│   ├── Dockerfile.frontend
│   ├── Dockerfile.backend
│   └── docker-compose.yml
│
├── docs/                       # Documentation
│   ├── logbook/                # Development logbook entries
│   ├── ARCHITECTURE.md
│   ├── DEVELOPMENT_PLAN.md
│   ├── OBJECTIVE_TRACEABILITY.md
│   ├── API_DOCUMENTATION.md
│   ├── DATABASE_DESIGN.md
│   ├── AI_ARCHITECTURE.md
│   ├── ML_PIPELINE.md
│   ├── KNOWLEDGE_GRAPH.md
│   ├── SECURITY.md
│   ├── DEPLOYMENT.md
│   └── TESTING.md
│
├── .env.example                # Environment variables template
├── .gitignore
├── docker-compose.yml
└── README.md
```

## Key Design Principles

1. **Separation of Concerns**: Frontend and backend are completely independent
2. **Modularity**: Each component has a single, well-defined responsibility
3. **Scalability**: Architecture supports adding new agents, data sources, and models
4. **Testability**: Clear separation enables unit, integration, and e2e testing
5. **Security**: Authentication, authorization, and security best practices throughout
