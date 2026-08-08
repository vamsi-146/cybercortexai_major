import apiClient from './client'

export interface LoginRequest {
  email: string
  password: string
}

export interface RegisterRequest {
  email: string
  username: string
  full_name?: string
  password: string
}

export interface AuthResponse {
  access_token: string
  refresh_token: string
  token_type: string
}

export interface User {
  id: string
  email: string
  username: string
  full_name?: string
  role: string
  is_active: boolean
  created_at: string
  updated_at: string
}

export const authApi = {
  login: async (credentials: LoginRequest): Promise<AuthResponse> => {
    const response = await apiClient.post('/auth/login', credentials)
    return response.data
  },

  register: async (userData: RegisterRequest): Promise<User> => {
    const response = await apiClient.post('/auth/register', userData)
    return response.data
  },

  logout: async (): Promise<void> => {
    await apiClient.post('/auth/logout')
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await apiClient.get('/auth/me')
    return response.data
  },

  refreshToken: async (refreshToken: string): Promise<AuthResponse> => {
    const response = await apiClient.post('/auth/refresh', { refresh_token: refreshToken })
    return response.data
  },
}
