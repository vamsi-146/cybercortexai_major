# CyberCortex AI - Frontend Architecture

## Technology Stack

- **Framework**: React 18+ with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Routing**: React Router v6
- **State Management**: React Context + hooks (no Redux initially)
- **Graph Visualization**: React Flow
- **Charts**: Recharts
- **HTTP Client**: Axios
- **Form Validation**: React Hook Form + Zod

## Architecture Pattern

### Component Hierarchy

```
App (Root)
├── AuthProvider (Context) - Phase 2: JWT authentication
├── ThemeProvider (Context)
├── QueryClientProvider (React Query) - Phase 3
└── Routes
    ├── Public Routes
    │   ├── LoginPage - Phase 2: Login with JWT
    │   └── ForgotPasswordPage - Phase 4
    └── Protected Routes (ProtectedRoute wrapper - Phase 2)
        ├── Layout (Sidebar + Header)
        ├── Dashboard - Phase 2: Connected to API
        ├── Threat Operations
        │   ├── AlertsPage - Phase 4
        │   ├── IncidentsPage - Phase 4
        │   ├── InvestigationsPage - Phase 5
        │   └── DetectionRulesPage - Phase 4
        ├── AI Operations
        │   ├── AIInvestigatorPage - Phase 5
        │   ├── AgentActivityPage - Phase 5
        │   ├── CollaborativeReasoningPage - Phase 5
        │   └── AIRecommendationsPage - Phase 5
        ├── Intelligence
        │   ├── ThreatIntelPage - Phase 8
        │   ├── IOCExplorerPage - Phase 8
        │   ├── MITREATTACKPage - Phase 8
        │   ├── VulnerabilitiesPage - Phase 8
        │   └── SecurityMemoryPage - Phase 6
        ├── Graph Intelligence
        │   ├── KnowledgeGraphPage - Phase 7
        │   ├── AttackPathsPage - Phase 9
        │   └── BlastRadiusPage - Phase 7
        ├── Analytics
        │   ├── RiskAnalyticsPage
        │   ├── PredictionAnalyticsPage
        │   ├── ModelConfidencePage
        │   └── ReportsPage
        └── Administration
            ├── UsersPage
            ├── DataSourcesPage
            ├── AuditLogsPage
            └── SettingsPage
```

## Component Architecture

### 1. Reusable Components (`components/`)

#### UI Components
- `Button` - Primary, secondary, danger variants
- `Card` - Standard, hover, interactive variants
- `Badge` - Severity, status, role badges
- `Table` - Sortable, filterable, paginated
- `Modal` - Dialogs and forms
- `Drawer` - Side panels
- `Tooltip` - Contextual help
- `Skeleton` - Loading states
- `EmptyState` - No data states
- `ErrorState` - Error display

#### Domain Components
- `SeverityChip` - Critical/High/Medium/Low/Info
- `StatusIndicator` - Live status dots
- `Timeline` - Event timelines
- `EvidenceCard` - Agent findings display
- `AgentStatus` - Agent execution visualization
- `MITRETag` - MITRE ATT&CK technique tags
- `ConfidenceBar` - Confidence score visualization
- `RiskScore` - Risk level display

#### Graph Components
- `GraphView` - Interactive knowledge graph
- `AttackPathView` - Attack path visualization
- `BlastRadiusView` - Impact analysis graph

### 2. Page Components (`pages/`)

Each page follows the pattern:
- Page-level component
- Page-specific hooks
- Page-specific sub-components
- API service integration

### 3. Custom Hooks (`hooks/`)

- `useAuth` - Authentication state and operations
- `useAlerts` - Alert data and operations
- `useIncidents` - Incident data and operations
- `useInvestigations` - Investigation workflow
- `useAgents` - Agent status and results
- `useGraph` - Knowledge graph queries
- `useAnalytics` - Analytics data
- `useWebSocket` - Real-time updates
- `usePagination` - Pagination logic
- `useFilters` - Filter state management

### 4. Services (`services/`)

- `api.ts` - Axios configuration and interceptors
- `authService.ts` - Authentication API calls
- `alertService.ts` - Alert API calls
- `incidentService.ts` - Incident API calls
- `investigationService.ts` - Investigation API calls
- `agentService.ts` - Agent API calls
- `graphService.ts` - Knowledge graph API calls
- `analyticsService.ts` - Analytics API calls

### 5. Types (`types/`)

- `user.ts` - User and role types
- `alert.ts` - Alert types
- `incident.ts` - Incident types
- `agent.ts` - Agent and investigation types
- `graph.ts` - Graph node and relationship types
- `analytics.ts` - Analytics types
- `common.ts` - Common types (severity, status, etc.)

### 6. Context Providers (`context/`)

- `AuthContext` - User authentication and permissions
- `ThemeContext` - Dark mode theme configuration
- `NotificationContext` - Toast notifications
- `WebSocketContext` - Real-time connection management

## Design System

### Color Palette

#### Base Colors
- Background: `#0a0e17` (near-black)
- Surface: `#111827` (dark navy)
- Surface-hover: `#1f2937` (graphite)
- Border: `#374151` (medium gray)

#### Accent Colors
- Primary: `#06b6d4` (electric cyan)
- Secondary: `#3b82f6` (controlled blue)
- Tertiary: `#14b8a6` (subtle teal)

#### Security State Colors
- Critical: `#ef4444` (red)
- High: `#f97316` (orange)
- Medium: `#eab308` (yellow)
- Low: `#22c55e` (green)
- Info: `#06b6d4` (cyan)

### Typography
- Font: Inter or system-ui
- Headings: Bold, tight tracking
- Body: Regular, optimized line-height
- Code: Monospace, syntax-highlighted

### Spacing Scale
- Base unit: 4px
- Scale: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96

### Components Guidelines
- Consistent border-radius: 4px for cards, 2px for inputs
- Subtle shadows for depth
- Grid/network background patterns for cyber feel
- Status indicators for all live data
- Loading states for async operations
- Error boundaries for graceful failures

## State Management Strategy

### Client State
- React Context for global state (auth, theme, notifications)
- Component state for local UI state
- Custom hooks for reusable state logic

### Server State
- React Query for API data caching and synchronization
- Automatic refetching for real-time updates
- Optimistic updates for better UX

### Real-time Updates
- WebSocket connection for live alerts, agent status, incident updates
- Reconnection logic and error handling
- Fallback to polling if WebSocket unavailable

## Performance Considerations

- Code splitting by route
- Lazy loading heavy components (graphs, charts)
- Virtualization for large lists/tables
- Image optimization
- Debounced search inputs
- Efficient re-renders with React.memo where appropriate

## Security

- JWT token storage in httpOnly cookies (preferred) or secure localStorage
- Automatic token refresh
- Request/response interceptors for authentication
- XSS protection (React built-in)
- CSRF protection
- Secure headers via backend
- Role-based UI rendering

## Accessibility

- Semantic HTML
- ARIA labels for interactive elements
- Keyboard navigation support
- Focus management
- Color contrast compliance
- Screen reader friendly

## Testing Strategy

- Unit tests with React Testing Library
- Component integration tests
- E2E tests with Playwright
- Visual regression tests for critical components
- Performance testing for large datasets
