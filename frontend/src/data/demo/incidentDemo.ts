import type { Incident, IncidentDetail } from '@schemas/incident'
import type { AgentActivity, CollaborativeReasoning } from '@schemas/agent'

// DEMO DATA - Frontend only, not connected to backend
// This data will be replaced with real API calls in later phases

export const recentIncidents: Incident[] = [
  {
    id: 'CC-2026-1042',
    title: 'Possible Lateral Movement',
    severity: 'CRITICAL',
    status: 'INVESTIGATING',
    affectedEntity: 'WS-01',
    mitreTechniques: ['T1021', 'T1078'],
    riskScore: 92,
    updated: '2m ago',
    created: '15m ago',
    assignedTo: 'analyst@cybercortex.ai',
  },
  {
    id: 'CC-2026-1041',
    title: 'Suspicious PowerShell Execution',
    severity: 'HIGH',
    status: 'IN_PROGRESS',
    affectedEntity: 'SRV-03',
    mitreTechniques: ['T1059'],
    riskScore: 78,
    updated: '15m ago',
    created: '1h ago',
    assignedTo: 'analyst@cybercortex.ai',
  },
  {
    id: 'CC-2026-1040',
    title: 'Brute Force Attack Detected',
    severity: 'CRITICAL',
    status: 'INVESTIGATING',
    affectedEntity: 'AUTH-01',
    mitreTechniques: ['T1110'],
    riskScore: 88,
    updated: '45m ago',
    created: '2h ago',
    assignedTo: 'analyst@cybercortex.ai',
  },
  {
    id: 'CC-2026-1039',
    title: 'Unusual Login Activity',
    severity: 'HIGH',
    status: 'OPEN',
    affectedEntity: 'USER-892',
    mitreTechniques: ['T1078'],
    riskScore: 71,
    updated: '1h ago',
    created: '3h ago',
  },
  {
    id: 'CC-2026-1038',
    title: 'Port Scan Detected',
    severity: 'MEDIUM',
    status: 'OPEN',
    affectedEntity: 'FW-EXT-01',
    mitreTechniques: ['T1046'],
    riskScore: 54,
    updated: '2h ago',
    created: '4h ago',
  },
  {
    id: 'CC-2026-1037',
    title: 'Credential Compromise',
    severity: 'CRITICAL',
    status: 'INVESTIGATING',
    affectedEntity: 'DB-ADMIN',
    mitreTechniques: ['T1110', 'T1078'],
    riskScore: 95,
    updated: '30m ago',
    created: '5h ago',
    assignedTo: 'analyst@cybercortex.ai',
  },
]

export const incidentDetail: IncidentDetail = {
  id: 'CC-2026-1042',
  title: 'Possible Lateral Movement',
  severity: 'CRITICAL',
  status: 'INVESTIGATING',
  affectedEntity: 'WS-01',
  mitreTechniques: ['T1021', 'T1078'],
  riskScore: 92,
  updated: '2m ago',
  created: '15m ago',
  assignedTo: 'analyst@cybercortex.ai',
  description: 'Detection of suspicious lateral movement patterns from workstation WS-01 to multiple internal servers. Initial analysis suggests potential credential reuse or pass-the-hash attack.',
  affectedAssets: [
    {
      id: 'WS-01',
      name: 'WORKSTATION-01',
      type: 'DEVICE',
      criticality: 'HIGH',
    },
    {
      id: 'SRV-03',
      name: 'SERVER-03',
      type: 'HOST',
      criticality: 'CRITICAL',
    },
    {
      id: 'SRV-05',
      name: 'SERVER-05',
      type: 'HOST',
      criticality: 'HIGH',
    },
  ],
  indicators: [
    {
      type: 'IP',
      value: '192.168.1.45',
      confidence: 0.92,
    },
    {
      type: 'HASH',
      value: '5d41402abc4b2a76b9719d911017c592',
      confidence: 0.87,
    },
  ],
  timeline: [
    {
      timestamp: '2024-01-15 10:30:00',
      event: 'Authentication Failure',
      description: 'Multiple failed authentication attempts detected',
      severity: 'HIGH',
    },
    {
      timestamp: '2024-01-15 10:32:15',
      event: 'Successful Login',
      description: 'Successful login from unusual IP address',
      severity: 'CRITICAL',
    },
    {
      timestamp: '2024-01-15 10:35:00',
      event: 'Lateral Movement',
      description: 'SMB connection to SRV-03 detected',
      severity: 'CRITICAL',
    },
    {
      timestamp: '2024-01-15 10:40:00',
      event: 'Privilege Escalation',
      description: 'Elevated privileges detected on SRV-03',
      severity: 'CRITICAL',
    },
  ],
  riskAssessment: {
    overallScore: 92,
    factors: [
      {
        factor: 'Credential Compromise',
        impact: 0.35,
        description: 'Evidence of credential theft or reuse',
      },
      {
        factor: 'Lateral Movement',
        impact: 0.30,
        description: 'Active lateral movement to critical servers',
      },
      {
        factor: 'Privilege Escalation',
        impact: 0.25,
        description: 'Successful privilege escalation detected',
      },
      {
        factor: 'Asset Criticality',
        impact: 0.10,
        description: 'Target assets are high-value systems',
      },
    ],
  },
  investigationId: 'INV-2026-0892',
  relatedAlerts: ['ALT-2026-4521', 'ALT-2026-4522', 'ALT-2026-4523'],
  recommendedActions: [
    'Isolate affected workstation WS-01',
    'Investigate credential usage on affected servers',
    'Reset credentials for affected accounts',
    'Review network logs for additional lateral movement',
    'Enable enhanced monitoring on critical servers',
  ],
}

export const agentActivities: AgentActivity[] = [
  {
    id: 'agent-1',
    name: 'Identity Agent',
    task: 'Investigating brute-force pattern',
    state: 'RUNNING',
    duration: '2m',
    icon: 'User',
  },
  {
    id: 'agent-2',
    name: 'Threat Intelligence Agent',
    task: 'Enriching suspicious IP',
    state: 'RUNNING',
    duration: '3m',
    icon: 'Globe',
  },
  {
    id: 'agent-3',
    name: 'Vulnerability Agent',
    task: 'Correlating CVE exposure',
    state: 'COMPLETED',
    duration: '4m',
    icon: 'Shield',
  },
  {
    id: 'agent-4',
    name: 'Investigation Agent',
    task: 'Building attack timeline',
    state: 'RUNNING',
    duration: '1m',
    icon: 'Search',
  },
  {
    id: 'agent-5',
    name: 'Coordinator Agent',
    task: 'Orchestrating investigation',
    state: 'RUNNING',
    duration: 'Now',
    icon: 'Cpu',
  },
]

export const collaborativeReasoning: CollaborativeReasoning = {
  overallConfidence: 0.88,
  keyInsights: [
    'Multiple authentication failures followed by successful login',
    'Source IP has known malicious reputation',
    'Lateral movement to critical assets detected',
    'Similar patterns observed in historical incident CC-2025-0891',
  ],
  conflictingFindings: [
    {
      agent: 'Identity Agent',
      finding: 'Confident in credential compromise (91%)',
      resolution: 'Accepted based on strong evidence',
    },
    {
      agent: 'Threat Intel Agent',
      finding: 'IP reputation moderate (72%)',
      resolution: 'Weighted lower due to conflicting sources',
    },
  ],
  finalAssessment: 'High-confidence lateral movement attack requiring immediate containment. Evidence suggests credential theft with active exploitation against critical servers.',
}
