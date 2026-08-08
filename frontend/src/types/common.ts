// Common types used across the application

export type Severity = 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW' | 'INFO'

export type Status = 'OPEN' | 'IN_PROGRESS' | 'INVESTIGATING' | 'CONTAINED' | 'RESOLVED' | 'CLOSED' | 'FALSE_POSITIVE'

export type AgentState = 'RUNNING' | 'WAITING' | 'COMPLETED' | 'FAILED'

export type SystemHealth = 'OPERATIONAL' | 'DEGRADED' | 'UNAVAILABLE'

export type Role = 'ADMIN' | 'SOC_ANALYST' | 'SECURITY_ENGINEER' | 'VIEWER'

export interface Metric {
  value: string | number
  label: string
  trend?: number
  previousValue?: string | number
}

export interface TimeRange {
  label: string
  value: string
}

export const TIME_RANGES: TimeRange[] = [
  { label: '1H', value: '1h' },
  { label: '24H', value: '24h' },
  { label: '7D', value: '7d' },
  { label: '30D', value: '30d' },
]

export const SEVERITY_ORDER: Record<Severity, number> = {
  CRITICAL: 5,
  HIGH: 4,
  MEDIUM: 3,
  LOW: 2,
  INFO: 1,
}

export const SEVERITY_COLORS: Record<Severity, string> = {
  CRITICAL: '#EF4444',
  HIGH: '#F97316',
  MEDIUM: '#EAB308',
  LOW: '#22C55E',
  INFO: '#06B6D4',
}
