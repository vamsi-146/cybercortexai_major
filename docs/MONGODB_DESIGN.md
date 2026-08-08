# CyberCortex AI - MongoDB Database Design

## Overview

MongoDB serves as the primary document store for CyberCortex AI, handling structured data, time-series security events, audit trails, and historical security memory.

## Collections

### 1. users

**Purpose**: Store user accounts, authentication credentials, and role assignments.

**Schema**:
```javascript
{
  _id: ObjectId,
  username: String (unique, indexed),
  email: String (unique, indexed),
  password_hash: String (bcrypt),
  role: Enum["ADMIN", "SOC_ANALYST", "SECURITY_ENGINEER", "VIEWER"],
  permissions: [String],  // Derived from role, allows fine-grained control
  full_name: String,
  department: String,
  is_active: Boolean (default: true),
  last_login: DateTime,
  created_at: DateTime (indexed),
  updated_at: DateTime,
  created_by: ObjectId (references users._id),
  mfa_enabled: Boolean (default: false),
  mfa_secret: String (encrypted)
}
```

**Indexes**:
- `username` (unique)
- `email` (unique)
- `role`
- `is_active`
- `created_at`

---

### 2. alerts

**Purpose**: Store security alerts generated from correlated events.

**Schema**:
```javascript
{
  _id: ObjectId,
  alert_id: String (unique, indexed),  // External-friendly ID
  title: String,
  description: String,
  severity: Enum["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"],
  status: Enum["OPEN", "INVESTIGATING", "RESOLVED", "FALSE_POSITIVE", "CLOSED"],
  source: String,  // Event source that generated the alert
  rule_id: String,  // Detection rule that triggered
  confidence_score: Float (0-100),
  mitre_techniques: [String],  // e.g., ["T1110", "T1078"]
  iocs: [{
    type: Enum["IP", "DOMAIN", "HASH", "EMAIL", "URL"],
    value: String,
    confidence: Float
  }],
  related_events: [ObjectId],  // References security_events._id
  assigned_to: ObjectId (references users._id),
  incident_id: ObjectId (references incidents._id, optional),
  metadata: {
    detection_time: DateTime,
    correlation_score: Float,
    agent_contributions: [{
      agent_name: String,
      confidence: Float,
      findings: String
    }]
  },
  created_at: DateTime (indexed),
  updated_at: DateTime,
  resolved_at: DateTime,
  resolution_notes: String
}
```

**Indexes**:
- `alert_id` (unique)
- `severity`
- `status`
- `source`
- `created_at`
- `assigned_to`
- `incident_id`
- Compound: `{ status: 1, severity: 1 }`
- Compound: `{ created_at: -1, severity: 1 }`

---

### 3. incidents

**Purpose**: Store security incidents that may contain multiple related alerts.

**Schema**:
```javascript
{
  _id: ObjectId,
  incident_id: String (unique, indexed),
  title: String,
  description: String,
  severity: Enum["CRITICAL", "HIGH", "MEDIUM", "LOW"],
  status: Enum["OPEN", "IN_PROGRESS", "CONTAINED", "ERADICATED", "RECOVERED", "CLOSED"],
  phase: Enum["IDENTIFICATION", "CONTAINMENT", "ERADICATION", "RECOVERY", "LESSONS_LEARNED"],
  alerts: [ObjectId],  // References alerts._id
  assigned_to: ObjectId (references users._id),
  team_members: [ObjectId],  // References users._id
  affected_assets: [{
    type: Enum["USER", "DEVICE", "HOST", "APPLICATION", "DATABASE"],
    id: String,
    name: String,
    criticality: Enum["CRITICAL", "HIGH", "MEDIUM", "LOW"]
  }],
  mitre_attack_pattern: {
    tactics: [String],
    techniques: [String]
  },
  timeline: [{
    timestamp: DateTime,
    event: String,
    description: String,
    actor: ObjectId (references users._id)
  }],
  containment_actions: [String],
  root_cause_analysis: String,
  lessons_learned: String,
  metrics: {
    detection_time: DateTime,
  containment_time: DateTime,
  eradication_time: DateTime,
  recovery_time: DateTime,
  total_cost: Number,
  impacted_users: Number
  },
  created_at: DateTime (indexed),
  updated_at: DateTime,
  closed_at: DateTime,
  created_by: ObjectId (references users._id)
}
```

**Indexes**:
- `incident_id` (unique)
- `severity`
- `status`
- `assigned_to`
- `created_at`
- Compound: `{ status: 1, created_at: -1 }`

---

### 4. investigations

**Purpose**: Store AI-driven investigations and agent findings.

**Schema**:
```javascript
{
  _id: ObjectId,
  investigation_id: String (unique, indexed),
  alert_id: ObjectId (references alerts._id),
  incident_id: ObjectId (references incidents._id, optional),
  status: Enum["PENDING", "RUNNING", "COMPLETED", "FAILED"],
  trigger_type: Enum["ALERT", "MANUAL", "SCHEDULED"],
  investigation_type: String,
  agents_executed: [String],  // ["identity_agent", "threat_intel_agent", ...]
  agent_findings: [{
    agent_name: String,
    execution_time: DateTime,
    duration_ms: Number,
    confidence: Float,
    findings: String,
    evidence: [{
      type: String,
      value: String,
      source: String,
      timestamp: DateTime
    }],
    mitre_techniques: [String],
    recommended_actions: [String]
  }],
  collaborative_reasoning: {
    overall_confidence: Float,
    key_insights: [String],
    conflicting_findings: [{
      agent: String,
      finding: String,
      resolution: String
    }],
    final_assessment: String
  },
  security_memory_context: {
    similar_incidents: [ObjectId],
    historical_patterns: [String],
    retrieved_at: DateTime
  },
  graph_analysis: {
    nodes_analyzed: Number,
    relationships_traversed: Number,
    attack_paths_found: Number,
    blast_radius: Number
  },
  explanation: {
    what_detected: String,
    evidence_used: [String],
    why_critical: String,
    recommended_response: [String]
  },
  recommendations: [{
    action: String,
    priority: Enum["IMMEDIATE", "HIGH", "MEDIUM", "LOW"],
    estimated_impact: String,
    automation_possible: Boolean
  }],
  created_at: DateTime (indexed),
  updated_at: DateTime,
  completed_at: DateTime,
  created_by: ObjectId (references users._id)
}
```

**Indexes**:
- `investigation_id` (unique)
- `alert_id`
- `incident_id`
- `status`
- `created_at`
- Compound: `{ status: 1, created_at: -1 }`

---

### 5. security_events

**Purpose**: Store raw and normalized security events from various data sources.

**Schema**:
```javascript
{
  _id: ObjectId,
  event_id: String (unique, indexed),
  source: String,  // e.g., "windows_logs", "firewall", "siem"
  source_type: Enum["WINDOWS_LOGS", "LINUX_LOGS", "FIREWALL", "IDS", "WAF", "EDR", "SIEM", "CLOUD"],
  raw_event: Object,  // Original event data
  normalized_event: {
    timestamp: DateTime (indexed),
    event_type: String,
    category: String,
    severity: String,
    source_ip: String,
    destination_ip: String,
    source_port: Number,
    destination_port: Number,
    protocol: String,
    user: String,
    host: String,
    process: String,
    file_hash: String,
    url: String,
    domain: String,
    description: String
  },
  enrichment: {
    geo_location: {
      country: String,
      city: String,
      latitude: Number,
      longitude: Number
    },
    threat_intel: {
      malicious: Boolean,
      confidence: Float,
      sources: [String]
    },
    user_context: {
      department: String,
      role: String,
      risk_score: Float
    },
    asset_context: {
      criticality: String,
      vulnerabilities: [String]
    }
  },
  correlation_id: String,  // Links related events
  alert_id: ObjectId (references alerts._id, optional),
  processed: Boolean (default: false, indexed),
  created_at: DateTime (indexed)
}
```

**Indexes**:
- `event_id` (unique)
- `normalized_event.timestamp`
- `source`
- `source_type`
- `processed`
- `correlation_id`
- `alert_id`
- Compound: `{ normalized_event.timestamp: -1, processed: 1 }`
- TTL index: 90 days on `created_at` (configurable)

---

### 6. security_memory

**Purpose**: Store historical security context, patterns, and analyst decisions for AI retrieval.

**Schema**:
```javascript
{
  _id: ObjectId,
  memory_id: String (unique, indexed),
  memory_type: Enum["INCIDENT_PATTERN", "AGENT_FINDING", "ANALYST_DECISION", "THREAT_PATTERN", "LESSON_LEARNED"],
  title: String,
  description: String,
  content: Object,  // Flexible structure based on memory_type
  tags: [String],
  related_incidents: [ObjectId],  // References incidents._id
  related_alerts: [ObjectId],  // References alerts._id
  related_iocs: [String],
  mitre_context: {
    tactics: [String],
    techniques: [String]
  },
  effectiveness_metrics: {
    times_retrieved: Number (default: 0),
    times_helpful: Number (default: 0),
    last_retrieved: DateTime
  },
  feedback: [{
    user_id: ObjectId,
    rating: Number (1-5),
    comment: String,
    timestamp: DateTime
  }],
  created_at: DateTime (indexed),
  updated_at: DateTime,
  expires_at: DateTime (optional)  // For time-sensitive memories
}
```

**Indexes**:
- `memory_id` (unique)
- `memory_type`
- `tags`
- `created_at`
- Text index on `title`, `description`, `content`
- Compound: `{ memory_type: 1, created_at: -1 }`

---

### 7. detection_rules

**Purpose**: Store detection rules for alert generation.

**Schema**:
```javascript
{
  _id: ObjectId,
  rule_id: String (unique, indexed),
  name: String,
  description: String,
  rule_type: Enum["CORRELATION", "THRESHOLD", "ANOMALY", "ML_MODEL", "AGENT_TRIGGERED"],
  severity: Enum["CRITICAL", "HIGH", "MEDIUM", "LOW"],
  enabled: Boolean (default: true),
  conditions: Object,  // Rule-specific conditions
  sources: [String],  // Applicable data sources
  mitre_techniques: [String],
  false_positive_rate: Float,
  tuning_parameters: Object,
  created_by: ObjectId (references users._id),
  created_at: DateTime (indexed),
  updated_at: DateTime,
  last_triggered: DateTime,
  trigger_count: Number (default: 0)
}
```

**Indexes**:
- `rule_id` (unique)
- `enabled`
- `rule_type`
- `severity`

---

### 8. audit_logs

**Purpose**: Store audit trail for compliance and security monitoring.

**Schema**:
```javascript
{
  _id: ObjectId,
  timestamp: DateTime (indexed),
  user_id: ObjectId (references users._id, optional for system events),
  username: String,
  action: String,
  resource_type: Enum["USER", "ALERT", "INCIDENT", "INVESTIGATION", "RULE", "SETTING"],
  resource_id: String,
  changes: Object,  // Before/after state for modifications
  ip_address: String,
  user_agent: String,
  result: Enum["SUCCESS", "FAILURE"],
  session_id: String,
  created_at: DateTime (indexed)
}
```

**Indexes**:
- `timestamp`
- `user_id`
- `action`
- `resource_type`
- `resource_id`
- Compound: `{ user_id: 1, timestamp: -1 }`
- TTL index: 365 days on `created_at` (configurable)

---

### 9. agent_results

**Purpose**: Store cached agent results for performance and historical analysis.

**Schema**:
```javascript
{
  _id: ObjectId,
  agent_name: String,
  execution_id: String (unique, indexed),
  input_data: Object,
  output_data: Object,
  confidence: Float,
  execution_time_ms: Number,
  error: String (optional),
  timestamp: DateTime (indexed),
  investigation_id: ObjectId (references investigations._id, optional)
}
```

**Indexes**:
- `execution_id` (unique)
- `agent_name`
- `timestamp`
- TTL index: 30 days on `timestamp`

---

### 10. recommendations

**Purpose**: Store AI-generated security recommendations and their adoption status.

**Schema**:
```javascript
{
  _id: ObjectId,
  recommendation_id: String (unique, indexed),
  title: String,
  description: String,
  recommendation_type: Enum["IMMEDIATE_ACTION", "HARDENING", "MONITORING", "INVESTIGATION", "CONFIGURATION"],
  priority: Enum["CRITICAL", "HIGH", "MEDIUM", "LOW"],
  context: {
    alert_id: ObjectId (references alerts._id),
    incident_id: ObjectId (references incidents._id),
    investigation_id: ObjectId (references investigations._id)
  },
  rationale: String,
  implementation_steps: [String],
  estimated_effort: String,
  risk_reduction: String,
  status: Enum["PENDING", "ACCEPTED", "REJECTED", "IMPLEMENTED", "DEFERRED"],
  accepted_by: ObjectId (references users._id),
  accepted_at: DateTime,
  implemented_at: DateTime,
  feedback: String,
  created_at: DateTime (indexed),
  expires_at: DateTime (optional)
}
```

**Indexes**:
- `recommendation_id` (unique)
- `status`
- `priority`
- `created_at`
- Compound: `{ status: 1, priority: 1 }`

---

## Database Design Principles

### 1. Embedding vs Referencing
- **Embed**: Data that is always accessed together (e.g., agent findings within investigation)
- **Reference**: Data that may be accessed independently (e.g., users, alerts)

### 2. Indexing Strategy
- Index all foreign key fields
- Index all query filter fields
- Index all timestamp fields for time-based queries
- Use compound indexes for common query patterns
- Monitor index performance and remove unused indexes

### 3. Data Lifecycle
- **security_events**: TTL after 90 days (configurable)
- **audit_logs**: TTL after 365 days (configurable)
- **agent_results**: TTL after 30 days
- **security_memory**: Long-term retention
- **alerts/incidents**: Long-term retention for compliance

### 4. Scalability Considerations
- Use sharding for high-volume collections (security_events)
- Consider read replicas for reporting queries
- Archive old data to cold storage
- Implement pagination for all list queries

### 5. Data Consistency
- Use transactions for multi-document operations
- Implement optimistic concurrency for updates
- Validate all writes with Pydantic models
- Use atomic operations for counters

### 6. Security
- Enable MongoDB authentication
- Use TLS for connections
- Implement field-level encryption for sensitive data
- Regular backups with point-in-time recovery
- Network isolation (database in private subnet)

## Migration Strategy

1. **Initial Schema**: Create all collections with defined schemas
2. **Index Creation**: Create indexes after initial data load
3. **Data Validation**: Enable schema validation in MongoDB
4. **Backward Compatibility**: Use version field for schema evolution
5. **Rollback Plan**: Keep previous schema versions for rollback

## Performance Optimization

1. **Query Optimization**
   - Use projection to limit returned fields
   - Implement pagination (skip/limit or cursor-based)
   - Use aggregation pipeline for complex queries
   - Cache frequent queries

2. **Write Optimization**
   - Bulk write operations for batch inserts
   - Use unordered bulk operations for speed
   - Implement write concern based on data criticality

3. **Connection Management**
   - Use connection pooling
   - Configure appropriate pool size
   - Monitor connection metrics
