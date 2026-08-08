import { Severity, Status } from './common'

export interface Incident {
  id: string
  title: string
  severity: Severity
  status: Status
  affectedEntity: string
  mitreTechniques: string[]
  riskScore: number
  updated: string
  created: string
  assignedTo?: string
}

export interface IncidentDetail extends Incident {
  description: string
  affectedAssets: Asset[]
  indicators: Indicator[]
  timeline: TimelineEvent[]
  riskAssessment: RiskAssessment
  investigationId?: string
  relatedAlerts: string[]
  recommendedActions: string[]
}

export interface Asset {
  id: string
  name: string
  type: 'USER' | 'DEVICE' | 'HOST' | 'APPLICATION'
  criticality: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW'
}

export interface Indicator {
  type: 'IP' | 'DOMAIN' | 'HASH' | 'EMAIL' | 'URL'
  value: string
  confidence: number
}

export interface TimelineEvent {
  timestamp: string
  event: string
  description: string
  severity?: Severity
}

export interface RiskAssessment {
  overallScore: number
  factors: RiskFactor[]
}

export interface RiskFactor {
  factor: string
  impact: number
  description: string
}
