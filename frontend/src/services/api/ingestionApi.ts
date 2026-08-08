import apiClient from './client'

export interface IngestionResult {
  received: number
  parsed: number
  normalized: number
  enriched: number
  stored: number
  rejected: number
  alerts_generated: number
  incidents_created: number
  errors: string[]
  event_id?: string
  detections?: number
}

export interface BulkIngestionResult extends IngestionResult {
  ingestion_id: string
  source_type: string
  processing_time_ms: number
}

export interface IngestionStats {
  total_events: number
  total_alerts: number
  total_incidents: number
  events_by_source: Record<string, number>
}

export const ingestionApi = {
  ingestEvent: async (rawEvent: string, sourceType: string, sourceName?: string): Promise<IngestionResult> => {
    const formData = new FormData()
    formData.append('raw_event', rawEvent)
    formData.append('source_type', sourceType)
    if (sourceName) formData.append('source_name', sourceName)

    const response = await apiClient.post('/ingestion/event', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  ingestBulk: async (rawEvents: string[], sourceType: string, sourceName?: string): Promise<BulkIngestionResult> => {
    const formData = new FormData()
    rawEvents.forEach(event => formData.append('raw_events', event))
    formData.append('source_type', sourceType)
    if (sourceName) formData.append('source_name', sourceName)

    const response = await apiClient.post('/ingestion/bulk', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  uploadFile: async (file: File, sourceType: string, sourceName?: string): Promise<BulkIngestionResult> => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('source_type', sourceType)
    if (sourceName) formData.append('source_name', sourceName)

    const response = await apiClient.post('/ingestion/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  getStats: async (): Promise<IngestionStats> => {
    const response = await apiClient.get('/ingestion/stats')
    return response.data
  },
}
