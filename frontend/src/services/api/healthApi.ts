import apiClient from './client'

export interface HealthCheck {
  status: string
  service: string
  version: string
  environment: string
}

export interface ReadinessCheck {
  status: string
  database: string
}

export const healthApi = {
  check: async (): Promise<HealthCheck> => {
    const response = await apiClient.get('/health/')
    return response.data
  },

  readiness: async (): Promise<ReadinessCheck> => {
    const response = await apiClient.get('/health/ready')
    return response.data
  },
}
