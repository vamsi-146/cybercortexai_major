import apiClient from './client'

export interface NormalizedEvent {
  timestamp: string
  event_type: string
  category?: string
  severity?: string
  source_ip?: string
  destination_ip?: string
  source_port?: number
  destination_port?: number
  protocol?: string
  user?: string
  host?: string
  process?: string
  file_hash?: string
  url?: string
  domain?: string
  description?: string
}

export interface SecurityEvent {
  id: string
  event_id: string
  source: string
  source_type: string
  raw_event: Record<string, any>
  normalized_event: NormalizedEvent
  received_at: string
  created_at: string
  processed: boolean
  alert_id?: string
}

export interface EventListParams {
  source_type?: string
  severity?: string
  event_type?: string
  src_ip?: string
  dst_ip?: string
  username?: string
  hostname?: string
  skip?: number
  limit?: number
}

export const eventsApi = {
  list: async (params?: EventListParams): Promise<SecurityEvent[]> => {
    const response = await apiClient.get('/events', { params })
    return response.data
  },

  getById: async (id: string): Promise<SecurityEvent> => {
    const response = await apiClient.get(`/events/${id}`)
    return response.data
  },

  create: async (data: any): Promise<SecurityEvent> => {
    const response = await apiClient.post('/events', data)
    return response.data
  },

  createBulk: async (events: any[]): Promise<SecurityEvent[]> => {
    const response = await apiClient.post('/events/bulk', events)
    return response.data
  },
}
