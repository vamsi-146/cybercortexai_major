import { useState } from 'react'
import { Shield, Lock, Eye, EyeOff, Loader2 } from 'lucide-react'
import { useAuth } from '@contexts/AuthContext'
import { useNavigate } from 'react-router-dom'

export function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await login(email, password)
      navigate('/')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed. Please check your credentials.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-background bg-grid flex items-center justify-center">
      <div className="w-full max-w-md p-8">
        {/* Brand */}
        <div className="flex items-center justify-center gap-3 mb-8">
          <div className="p-3 bg-primary/20 rounded-sm">
            <Shield className="w-8 h-8 text-primary" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-100">CyberCortex</h1>
            <p className="text-sm text-gray-400">AI Security Operations</p>
          </div>
        </div>

        {/* Login Card */}
        <div className="card-base p-6">
          <div className="panel-header border-b-0 mb-6">
            <h2 className="panel-title">
              <Lock className="w-4 h-4 text-primary" />
              Sign In
            </h2>
            <p className="text-sm text-gray-400 mt-1">
              Enter your credentials to access the SOC dashboard
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Email */}
            <div>
              <label className="block text-sm text-gray-300 mb-2">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="input-base w-full"
                placeholder="admin@cybercortex.ai"
                required
                disabled={loading}
              />
            </div>

            {/* Password */}
            <div>
              <label className="block text-sm text-gray-300 mb-2">Password</label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="input-base w-full pr-10"
                  placeholder="••••••••••"
                  required
                  disabled={loading}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-300"
                  disabled={loading}
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>

            {/* Error Message */}
            {error && (
              <div className="p-3 bg-critical/10 border border-critical/20 rounded-sm">
                <p className="text-sm text-critical">{error}</p>
              </div>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              className="btn-primary w-full flex items-center justify-center gap-2"
              disabled={loading}
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  Signing in...
                </>
              ) : (
                'Sign In'
              )}
            </button>
          </form>

          {/* Demo Credentials Hint */}
          <div className="mt-6 p-3 bg-surface-elevated border border-border rounded-sm">
            <p className="text-xs text-gray-400 mb-1">Demo Credentials:</p>
            <p className="text-xs text-mono text-gray-300">Email: admin@cybercortex.ai</p>
            <p className="text-xs text-mono text-gray-300">Password: AdminPass123!</p>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-6">
          <p className="text-xs text-gray-500">
            CyberCortex AI v0.1.0 | Phase 2 Development
          </p>
        </div>
      </div>
    </div>
  )
}
