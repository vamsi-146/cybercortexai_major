# CyberCortex AI - Neo4j Knowledge Graph Model

## Overview

Neo4j serves as the knowledge graph database for CyberCortex AI, modeling relationships between users, devices, vulnerabilities, IOCs, attacks, and MITRE ATT&CK techniques. This enables attack path analysis, blast radius calculation, and context-aware threat detection.

## Graph Schema

### Node Types

#### 1. User

**Purpose**: Represent users in the organization.

**Properties**:
```cypher
{
  user_id: String (unique),
  username: String,
  email: String,
  full_name: String,
  department: String,
  role: String,
  risk_score: Float (0-100),
  is_active: Boolean,
  last_login: DateTime,
  created_at: DateTime
}
```

**Indexes**:
- `user_id` (unique constraint)
- `username`
- `email`
- `risk_score`

---

#### 2. Device

**Purpose**: Represent devices, hosts, and endpoints.

**Properties**:
```cypher
{
  device_id: String (unique),
  hostname: String,
  ip_address: String,
  mac_address: String,
  device_type: Enum["WORKSTATION", "SERVER", "LAPTOP", "MOBILE", "IOT", "NETWORK_DEVICE"],
  os: String,
  os_version: String,
  criticality: Enum["CRITICAL", "HIGH", "MEDIUM", "LOW"],
  risk_score: Float (0-100),
  is_active: Boolean,
  last_seen: DateTime,
  created_at: DateTime
}
```

**Indexes**:
- `device_id` (unique constraint)
- `hostname`
- `ip_address`
- `mac_address`
- `risk_score`

---

#### 3. IP

**Purpose**: Represent IP addresses (internal and external).

**Properties**:
```cypher
{
  address: String (unique),
  type: Enum["INTERNAL", "EXTERNAL", "UNKNOWN"],
  geo_country: String,
  geo_city: String,
  is_malicious: Boolean,
  threat_intel_sources: [String],
  reputation_score: Float (0-100),
  first_seen: DateTime,
  last_seen: DateTime
}
```

**Indexes**:
- `address` (unique constraint)
- `type`
- `is_malicious`
- `reputation_score`

---

#### 4. IOC (Indicator of Compromise)

**Purpose**: Represent indicators of compromise.

**Properties**:
```cypher
{
  ioc_id: String (unique),
  type: Enum["IP", "DOMAIN", "HASH", "EMAIL", "URL", "CERTIFICATE"],
  value: String (unique),
  description: String,
  threat_type: String,
  confidence: Float (0-100),
  sources: [String],
  first_seen: DateTime,
  last_seen: DateTime,
  is_active: Boolean
}
```

**Indexes**:
- `ioc_id` (unique constraint)
- `value` (unique constraint)
- `type`
- `is_active`

---

#### 5. Vulnerability

**Purpose**: Represent security vulnerabilities.

**Properties**:
```cypher
{
  cve_id: String (unique),
  title: String,
  description: String,
  severity: Enum["CRITICAL", "HIGH", "MEDIUM", "LOW"],
  cvss_score: Float,
  cvss_vector: String,
  affected_products: [String],
  exploit_available: Boolean,
  exploit_maturity: Enum["NONE", "POC", "ACTIVE", "WEAPONIZED"],
  patch_available: Boolean,
  patch_url: String,
  published_date: DateTime,
  modified_date: DateTime
}
```

**Indexes**:
- `cve_id` (unique constraint)
- `severity`
- `cvss_score`
- `exploit_available`

---

#### 6. CVE

**Purpose**: Link to external CVE database entries.

**Properties**:
```cypher
{
  cve_id: String (unique),
  url: String,
  references: [String]
}
```

**Indexes**:
- `cve_id` (unique constraint)

---

#### 7. Alert

**Purpose**: Represent security alerts in the graph context.

**Properties**:
```cypher
{
  alert_id: String (unique),
  title: String,
  severity: Enum["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"],
  status: Enum["OPEN", "INVESTIGATING", "RESOLVED", "FALSE_POSITIVE", "CLOSED"],
  confidence: Float (0-100),
  created_at: DateTime,
  resolved_at: DateTime
}
```

**Indexes**:
- `alert_id` (unique constraint)
- `severity`
- `status`
- `created_at`

---

#### 8. Incident

**Purpose**: Represent security incidents.

**Properties**:
```cypher
{
  incident_id: String (unique),
  title: String,
  severity: Enum["CRITICAL", "HIGH", "MEDIUM", "LOW"],
  status: Enum["OPEN", "IN_PROGRESS", "CONTAINED", "ERADICATED", "RECOVERED", "CLOSED"],
  created_at: DateTime,
  closed_at: DateTime
}
```

**Indexes**:
- `incident_id` (unique constraint)
- `severity`
- `status`

---

#### 9. Attack

**Purpose**: Represent cyber attacks and attack patterns.

**Properties**:
```cypher
{
  attack_id: String (unique),
  name: String,
  description: String,
  attack_type: String,
  sophistication: Enum["LOW", "MEDIUM", "HIGH", "APT"],
  motivation: Enum["FINANCIAL", "ESPIONAGE", "SABOTAGE", "ACTIVISM", "UNKNOWN"],
  first_seen: DateTime,
  last_seen: DateTime,
  attribution: String
}
```

**Indexes**:
- `attack_id` (unique constraint)
- `attack_type`
- `sophistication`

---

#### 10. MITRETechnique

**Purpose**: Represent MITRE ATT&CK techniques.

**Properties**:
```cypher
{
  technique_id: String (unique),  // e.g., "T1110"
  technique_name: String,
  tactic: String,  // e.g., "Credential Access"
  sub_techniques: [String],
  description: String,
  detection: String,
  mitigation: String,
  url: String
}
```

**Indexes**:
- `technique_id` (unique constraint)
- `tactic`

---

#### 11. Process

**Purpose**: Represent processes executed on systems.

**Properties**:
```cypher
{
  process_id: String (unique),
  name: String,
  path: String,
  command_line: String,
  hash: String,
  is_malicious: Boolean,
  first_seen: DateTime,
  last_seen: DateTime
}
```

**Indexes**:
- `process_id` (unique constraint)
- `name`
- `hash`
- `is_malicious`

---

#### 12. File

**Purpose**: Represent files on systems.

**Properties**:
```cypher
{
  file_id: String (unique),
  name: String,
  path: String,
  size: Number,
  hash_md5: String,
  hash_sha1: String,
  hash_sha256: String,
  file_type: String,
  is_malicious: Boolean,
  first_seen: DateTime,
  last_seen: DateTime
}
```

**Indexes**:
- `file_id` (unique constraint)
- `hash_sha256`
- `is_malicious`

---

### Relationship Types

#### LOGGED_INTO
**From**: User
**To**: Device
**Properties**:
```cypher
{
  login_time: DateTime,
  logout_time: DateTime,
  session_duration: Number,
  ip_address: String,
  success: Boolean
}
```

---

#### CONNECTED_TO
**From**: Device
**To**: IP
**Properties**:
```cypher
{
  connection_type: Enum["INBOUND", "OUTBOUND", "BIDIRECTIONAL"],
  protocol: String,
  port: Number,
  first_seen: DateTime,
  last_seen: DateTime,
  bytes_transferred: Number,
  connection_count: Number
}
```

---

#### HAS_VULNERABILITY
**From**: Device
**To**: Vulnerability
**Properties**:
```cypher
{
  discovered_date: DateTime,
  patch_status: Enum["VULNERABLE", "PATCHED", "PATCHING_IN_PROGRESS"],
  patch_date: DateTime,
  risk_score: Float
}
```

---

#### EXPLOITS
**From**: Attack
**To**: Vulnerability
**Properties**:
```cypher
{
  exploit_confidence: Float,
  first_seen: DateTime
}
```

---

#### USES_TECHNIQUE
**From**: Attack
**To**: MITRETechnique
**Properties**:
```cypher
{
  technique_stage: String,
  order: Number
}
```

---

#### GENERATED
**From**: Device
**To**: Alert
**Properties**:
```cypher
{
  generation_time: DateTime,
  event_count: Number
}
```

---

#### TRIGGERED
**From**: User
**To**: Alert
**Properties**:
```cypher
{
  action: String,
  context: String
}
```

---

#### COMMUNICATED_WITH
**From**: IP
**To**: IP
**Properties**:
```cypher
{
  protocol: String,
  port: Number,
  first_seen: DateTime,
  last_seen: DateTime,
  communication_count: Number
}
```

---

#### ASSOCIATED_WITH
**From**: IOC
**To**: Attack
**Properties**:
```cypher
{
  association_type: String,
  confidence: Float,
  source: String
}
```

---

#### TARGETS
**From**: Attack
**To**: Device
**Properties**:
```cypher
{
  attack_stage: String,
  first_targeted: DateTime,
  success: Boolean
}
```

---

#### TARGETS_USER
**From**: Attack
**To**: User
**Properties**:
```cypher
{
  attack_method: String,
  first_targeted: DateTime,
  success: Boolean
}
```

---

#### PART_OF_INCIDENT
**From**: Alert
**To**: Incident
**Properties**:
```cypher
{
  correlation_score: Float,
  added_at: DateTime
}
```

---

#### INDICATES
**From**: IOC
**To**: Alert
**Properties**:
```cypher
{
  detection_method: String,
  confidence: Float
}
```

---

#### EXECUTED_ON
**From**: Process
**To**: Device
**Properties**:
```cypher
{
  execution_time: DateTime,
  user_context: String,
  parent_process: String
}
```

---

#### ACCESSED
**From**: Process
**To**: File
**Properties**:
```cypher
{
  access_type: Enum["READ", "WRITE", "EXECUTE", "DELETE"],
  access_time: DateTime
}
```

---

#### LINKED_TO
**From**: Vulnerability
**To**: CVE
**Properties**:
```cypher
{
  source: String
}
```

---

#### RESIDES_ON
**From**: File
**To**: Device
**Properties**:
```cypher
{
  path: String,
  first_seen: DateTime,
  last_seen: DateTime
}
```

---

## Graph Queries

### 1. Incident Subgraph Retrieval

Retrieve all entities related to an incident.

```cypher
MATCH (i:Incident {incident_id: $incident_id})<-[:PART_OF_INCIDENT]-(a:Alert)
OPTIONAL MATCH (a)<-[:GENERATED]-(d:Device)
OPTIONAL MATCH (a)<-[:TRIGGERED]-(u:User)
OPTIONAL MATCH (d)-[:CONNECTED_TO]->(ip:IP)
OPTIONAL MATCH (d)-[:HAS_VULNERABILITY]->(v:Vulnerability)
OPTIONAL MATCH (a)-[:INDICATES]-(ioc:IOC)
RETURN i, a, d, u, ip, v, ioc
```

---

### 2. Neighborhood Exploration

Explore the neighborhood of a node within N hops.

```cypher
MATCH (n {node_id: $node_id})
CALL apoc.path.subgraphAll(n, {maxLevel: $depth})
YIELD nodes, relationships
RETURN nodes, relationships
```

---

### 3. Candidate Attack Path Discovery

Find potential attack paths from a compromised asset to critical assets.

```cypher
MATCH path = (start:Device {device_id: $start_device_id})-[:CONNECTED_TO*1..5]-(end:Device {criticality: "CRITICAL"})
WHERE all(rel in relationships(path) WHERE rel.protocol IN ["TCP", "SMB", "RDP"])
RETURN path, length(path) as path_length
ORDER BY path_length
LIMIT 10
```

---

### 4. Blast Radius Analysis

Calculate the blast radius of a compromised device.

```cypher
MATCH (compromised:Device {device_id: $device_id})
CALL apoc.path.subgraphAll(compromised, {maxLevel: 3, relationshipFilter: "CONNECTED_TO|LOGGED_INTO"})
YIELD nodes, relationships
WITH compromised, nodes, relationships
UNWIND nodes as node
MATCH (node)-[:HAS_VULNERABILITY]->(v:Vulnerability)
WHERE v.severity IN ["CRITICAL", "HIGH"]
RETURN compromised, count(DISTINCT node) as affected_assets, 
       count(DISTINCT v) as critical_vulnerabilities,
       relationships
```

---

### 5. Lateral Movement Detection

Detect potential lateral movement patterns.

```cypher
MATCH (u:User)-[:LOGGED_INTO]->(d1:Device)
MATCH (d1)-[:CONNECTED_TO]->(d2:Device)
MATCH (u)-[:LOGGED_INTO]->(d2)
WHERE d1 <> d2
  AND d2.criticality IN ["CRITICAL", "HIGH"]
  AND d1.risk_score > 50
RETURN u, d1, d2, count(*) as login_count
ORDER BY login_count DESC
LIMIT 20
```

---

### 6. IOC Propagation Tracking

Track how an IOC has propagated through the network.

```cypher
MATCH (ioc:IOC {value: $ioc_value})
MATCH (ioc)-[:INDICATES]->(a:Alert)
MATCH (a)<-[:GENERATED]-(d:Device)
MATCH (d)-[:CONNECTED_TO]->(other:Device)
OPTIONAL MATCH (other)-[:HAS_VULNERABILITY]->(v:Vulnerability)
RETURN ioc, a, d, other, v
ORDER BY a.created_at DESC
```

---

### 7. Risk Aggregation

Aggregate risk scores across the graph.

```cypher
MATCH (d:Device)
OPTIONAL MATCH (d)-[:HAS_VULNERABILITY]->(v:Vulnerability)
WITH d, sum(CASE WHEN v.severity = "CRITICAL" THEN 1 ELSE 0 END) as crit_vulns,
     sum(CASE WHEN v.severity = "HIGH" THEN 1 ELSE 0 END) as high_vulns
RETURN d.device_id, d.hostname, d.risk_score, crit_vulns, high_vulns
ORDER BY d.risk_score DESC
LIMIT 50
```

---

## Graph Construction Strategy

### 1. Incremental Updates
- Nodes and relationships are created as events are ingested
- Batch updates for bulk operations
- Periodic graph consistency checks

### 2. Data Enrichment
- Enrich nodes with threat intelligence
- Add MITRE ATT&CK mappings automatically
- Calculate risk scores dynamically

### 3. Graph Maintenance
- Remove stale nodes and relationships
- Archive old data to secondary storage
- Rebuild indexes periodically

### 4. Performance Optimization
- Use appropriate indexes on frequently queried properties
- Implement query result caching
- Use APOC procedures for complex traversals
- Monitor query performance and optimize slow queries

## Graph Security

### 1. Access Control
- Role-based access to graph data
- Query restrictions based on user permissions
- Audit logging for graph queries

### 2. Data Privacy
- Mask sensitive user data in graph queries
- Implement data retention policies
- Secure graph database connections

### 3. Integrity
- Validate all graph updates
- Implement conflict resolution for concurrent updates
- Maintain graph consistency

## Integration with MongoDB

### 1. Synchronization
- MongoDB documents as source of truth
- Neo4j graph derived from MongoDB data
- Event-driven synchronization

### 2. Cross-Database Queries
- Use MongoDB for document retrieval
- Use Neo4j for relationship queries
- Combine results in application layer

### 3. Consistency
- Transactional updates where possible
- Eventual consistency for high-volume data
- Reconciliation processes for data alignment
