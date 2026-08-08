import apiClient from './client'

export interface Incident {
  id: string
  incident_id: string
  title: string
  description: string
  severity: string
  status: string
  risk_score: number
  created_at: string
  updated_at: string
  assigned_to?: string
  alert_ids?: string[]
  alert_count?: number
  event_ids?: string[]
  affected_assets?: any[]
  affected_users?: string[]
  affected_ips?: string[]
  mitre_techniques?: string[]
  timeline?: any[]
  indicators?: any[]
  recommendations?: string[]
}

export interface IncidentCreate {
  incident_id: string
  title: string
  description: string
  severity: string
  affected_assets?: Array<{
    type: string
    id: string
    name: string
    criticality: string
  }>
  mitre_techniques?: string[]
  indicators?: Array<{ type: string; value: string; confidence: number }>
  recommended_actions?: string[]
}

export interface IncidentUpdate {
  status?: string
  assigned_to?: string
  timeline?: Array<{
    timestamp: string
    event: string
    description: string
    severity?: string
  }>
  recommended_actions?: string[]
}

export interface IncidentListParams {
  severity?: string
  status?: string
  assigned_to?: string
  search?: string
  skip?: number
  limit?: number
}

export const incidentsApi = {
  list: async (params?: IncidentListParams): Promise<Incident[]> => {
    const response = await apiClient.get('/incidents', { params })
    return response.data
  },

  getById: async (id: string): Promise<Incident> => {
    const response = await apiClient.get(`/incidents/${id}`)
    return response.data
  },

  create: async (data: IncidentCreate): Promise<Incident> => {
    const response = await apiClient.post('/incidents', data)
    return response.data
  },

  update: async (id: string, data: IncidentUpdate): Promise<Incident> => {
    const response = await apiClient.patch(`/incidents/${id}`, data)
    return response.data
  },
}
