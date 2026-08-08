import type { Severity, SystemHealth } from './common'

export interface KPIMetric {
  id: string
  label: string
  value: number | string
  trend: number
  previousValue?: number
  icon: string
  format?: 'number' | 'percentage' | 'k' | 'm'
}

export interface PipelineStage {
  id: string
  name: string
  description: string
  status: 'active' | 'idle'
  count: number
  icon: string
}

export interface ThreatActivityPoint {
  timestamp: string
  events: number
  alerts: number
  incidents: number
}

export interface SeverityDistribution {
  severity: Severity
  count: number
  percentage: number
}

export interface MITRETechnique {
  id: string
  name: string
  count: number
  percentage: number
}

export interface EventSource {
  name: string
  count: number
  percentage: number
}

export interface RiskTrendPoint {
  timestamp: string
  riskScore: number
}

export interface SystemService {
  name: string
  status: SystemHealth
  latency?: number
  uptime?: string
}
