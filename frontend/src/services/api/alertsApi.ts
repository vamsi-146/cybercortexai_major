import apiClient from './client'

export interface Indicator {
  type: string
  value: string
  confidence: number
}

export interface Alert {
  id: string
  alert_id: string
  title: string
  description: string
  severity: string
  status: string
  source: string
  rule_id?: string
  confidence_score?: number
  mitre_techniques: string[]
  iocs: Indicator[]
  related_event_ids: string[]
  assigned_to?: string
  incident_id?: string
  first_seen: string
  last_seen: string
  created_at: string
  updated_at: string
  resolved_at?: string
  resolution_notes?: string
}

export interface AlertListParams {
  severity?: string
  status?: string
  source?: string
  assigned_to?: string
  skip?: number
  limit?: number
}

export interface AlertUpdate {
  status?: string
  assigned_to?: string
  resolution_notes?: string
}

export const alertsApi = {
  list: async (params?: AlertListParams): Promise<Alert[]> => {
    const response = await apiClient.get('/alerts', { params })
    return response.data
  },

  getById: async (id: string): Promise<Alert> => {
    const response = await apiClient.get(`/alerts/${id}`)
    return response.data
  },

  create: async (data: any): Promise<Alert> => {
    const response = await apiClient.post('/alerts', data)
    return response.data
  },

  update: async (id: string, data: AlertUpdate): Promise<Alert> => {
    const response = await apiClient.patch(`/alerts/${id}`, data)
    return response.data
  },
}
