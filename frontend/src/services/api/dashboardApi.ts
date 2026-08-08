import apiClient from './client'

export interface DashboardOverview {
  active_threats: {
    id: string
    label: string
    value: number
    trend: number
    available: boolean
  }
  critical_incidents: {
    id: string
    label: string
    value: number
    trend: number
    available: boolean
  }
  events_analyzed: {
    id: string
    label: string
    value: number
    trend: number
    available: boolean
  }
  ai_investigations: {
    id: string
    label: string
    value: number
    trend: number
    available: boolean
  }
  correlated_alerts: {
    id: string
    label: string
    value: number
    trend: number
    available: boolean
  }
  high_risk_assets: {
    id: string
    label: string
    value: number
    trend: number
    available: boolean
  }
  severity_distribution: Array<{
    severity: string
    count: number
    percentage: number
  }>
  events_by_source: Array<{
    name: string
    count: number
    percentage: number
  }>
  recent_incidents: Array<{
    id: string
    incident_id: string
    title: string
    severity: string
    status: string
    risk_score: number
    created_at: string
  }>
  system_health: Array<{
    name: string
    status: string
    latency?: number
    uptime?: string
    available: boolean
  }>
}

export const dashboardApi = {
  getOverview: async (): Promise<DashboardOverview> => {
    const response = await apiClient.get('/dashboard/overview')
    return response.data
  },
}
