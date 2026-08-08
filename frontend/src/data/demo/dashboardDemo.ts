import type { KPIMetric, PipelineStage, ThreatActivityPoint, SeverityDistribution, MITRETechnique, EventSource, RiskTrendPoint, SystemService } from '@schemas/dashboard'

// DEMO DATA - Frontend only, not connected to backend
// This data will be replaced with real API calls in later phases

export const dashboardKPIs: KPIMetric[] = [
  {
    id: 'active-threats',
    label: 'Active Threats',
    value: 24,
    trend: 12,
    previousValue: 21,
    icon: 'ShieldAlert',
    format: 'number',
  },
  {
    id: 'critical-incidents',
    label: 'Critical Incidents',
    value: 7,
    trend: -5,
    previousValue: 8,
    icon: 'AlertTriangle',
    format: 'number',
  },
  {
    id: 'events-analyzed',
    label: 'Events Analyzed',
    value: '12.4K',
    trend: 8,
    previousValue: 11480,
    icon: 'Activity',
    format: 'k',
  },
  {
    id: 'ai-investigations',
    label: 'AI Investigations',
    value: 18,
    trend: 25,
    previousValue: 14,
    icon: 'BrainCircuit',
    format: 'number',
  },
  {
    id: 'correlated-alerts',
    label: 'Correlated Alerts',
    value: 156,
    trend: 15,
    previousValue: 135,
    icon: 'Network',
    format: 'number',
  },
  {
    id: 'high-risk-assets',
    label: 'High-Risk Assets',
    value: 31,
    trend: -3,
    previousValue: 32,
    icon: 'Server',
    format: 'number',
  },
]

export const pipelineStages: PipelineStage[] = [
  {
    id: 'observe',
    name: 'OBSERVE',
    description: 'Collect & Monitor',
    status: 'active',
    count: 12400,
    icon: 'Eye',
  },
  {
    id: 'correlate',
    name: 'CORRELATE',
    description: 'Detect Patterns',
    status: 'active',
    count: 156,
    icon: 'GitCompare',
  },
  {
    id: 'investigate',
    name: 'INVESTIGATE',
    description: 'AI Analysis',
    status: 'active',
    count: 18,
    icon: 'Search',
  },
  {
    id: 'reason',
    name: 'REASON',
    description: 'Multi-Agent Fusion',
    status: 'active',
    count: 7,
    icon: 'GitMerge',
  },
  {
    id: 'predict',
    name: 'PREDICT',
    description: 'Attack Prediction',
    status: 'active',
    count: 12,
    icon: 'TrendingUp',
  },
  {
    id: 'explain',
    name: 'EXPLAIN',
    description: 'Explainable AI',
    status: 'active',
    count: 7,
    icon: 'MessageSquare',
  },
]

export const threatActivityData: ThreatActivityPoint[] = [
  { timestamp: '00:00', events: 450, alerts: 12, incidents: 2 },
  { timestamp: '04:00', events: 320, alerts: 8, incidents: 1 },
  { timestamp: '08:00', events: 890, alerts: 24, incidents: 3 },
  { timestamp: '12:00', events: 1200, alerts: 35, incidents: 5 },
  { timestamp: '16:00', events: 980, alerts: 28, incidents: 4 },
  { timestamp: '20:00', events: 750, alerts: 22, incidents: 3 },
  { timestamp: '23:59', events: 620, alerts: 18, incidents: 2 },
]

export const severityDistribution: SeverityDistribution[] = [
  { severity: 'CRITICAL', count: 7, percentage: 4.5 },
  { severity: 'HIGH', count: 23, percentage: 14.7 },
  { severity: 'MEDIUM', count: 45, percentage: 28.8 },
  { severity: 'LOW', count: 58, percentage: 37.2 },
  { severity: 'INFO', count: 23, percentage: 14.7 },
]

export const mitreTechniques: MITRETechnique[] = [
  { id: 'T1110', name: 'Brute Force', count: 24, percentage: 15.4 },
  { id: 'T1078', name: 'Valid Accounts', count: 19, percentage: 12.2 },
  { id: 'T1059', name: 'Command and Scripting Interpreter', count: 17, percentage: 10.9 },
  { id: 'T1021', name: 'Remote Services', count: 15, percentage: 9.6 },
  { id: 'T1047', name: 'Windows Management Instrumentation', count: 13, percentage: 8.3 },
]

export const eventSources: EventSource[] = [
  { name: 'Windows Security', count: 3200, percentage: 25.8 },
  { name: 'Firewall', count: 2800, percentage: 22.6 },
  { name: 'Proxy', count: 1900, percentage: 15.3 },
  { name: 'EDR', count: 1700, percentage: 13.7 },
  { name: 'VPN', count: 1100, percentage: 8.9 },
  { name: 'Cloud', count: 950, percentage: 7.7 },
  { name: 'Identity', count: 750, percentage: 6.0 },
]

export const riskTrendData: RiskTrendPoint[] = [
  { timestamp: 'Day 1', riskScore: 65 },
  { timestamp: 'Day 2', riskScore: 72 },
  { timestamp: 'Day 3', riskScore: 68 },
  { timestamp: 'Day 4', riskScore: 75 },
  { timestamp: 'Day 5', riskScore: 71 },
  { timestamp: 'Day 6', riskScore: 78 },
  { timestamp: 'Day 7', riskScore: 74 },
]

export const systemServices: SystemService[] = [
  { name: 'Event Ingestion', status: 'OPERATIONAL', latency: 12, uptime: '99.9%' },
  { name: 'Correlation Engine', status: 'OPERATIONAL', latency: 8, uptime: '99.8%' },
  { name: 'Agent Engine', status: 'OPERATIONAL', latency: 45, uptime: '99.7%' },
  { name: 'MongoDB', status: 'OPERATIONAL', latency: 3, uptime: '99.9%' },
  { name: 'Neo4j', status: 'OPERATIONAL', latency: 15, uptime: '99.6%' },
  { name: 'Prediction Engine', status: 'DEGRADED', latency: 120, uptime: '98.5%' },
]
