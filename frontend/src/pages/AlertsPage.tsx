import { useState, useEffect } from 'react'
import { alertsApi, Alert } from '../services/api/alertsApi'
import { SEVERITY_COLORS } from '../types/common'

export function AlertsPage() {
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [filters, setFilters] = useState({
    severity: '',
    status: '',
    source: '',
    assigned_to: '',
  })

  useEffect(() => {
    loadAlerts()
  }, [filters])

  const loadAlerts = async () => {
    try {
      setLoading(true)
      const data = await alertsApi.list({
        ...filters,
        skip: 0,
        limit: 100,
      })
      setAlerts(data)
      setError(null)
    } catch (err) {
      setError('Failed to load alerts')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleFilterChange = (key: string, value: string) => {
    setFilters(prev => ({ ...prev, [key]: value }))
  }

  const getSeverityColor = (severity: string) => {
    return SEVERITY_COLORS[severity as keyof typeof SEVERITY_COLORS] || '#6B7280'
  }

  const getStatusColor = (status: string) => {
    const colors: Record<string, string> = {
      OPEN: '#EF4444',
      IN_PROGRESS: '#F97316',
      INVESTIGATING: '#EAB308',
      RESOLVED: '#22C55E',
      CLOSED: '#6B7280',
      FALSE_POSITIVE: '#8B5CF6',
    }
    return colors[status] || '#6B7280'
  }

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString()
  }

  const handleStatusUpdate = async (alertId: string, newStatus: string) => {
    try {
      await alertsApi.update(alertId, { status: newStatus })
      loadAlerts()
    } catch (err) {
      console.error('Failed to update alert status:', err)
    }
  }

  if (loading) {
    return (
      <div className="p-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-6"></div>
          <div className="space-y-4">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="h-24 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="p-6">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800">{error}</p>
          <button
            onClick={loadAlerts}
            className="mt-2 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-4">Security Alerts</h1>
        
        {/* Filters */}
        <div className="flex flex-wrap gap-4 mb-4">
          <select
            value={filters.severity}
            onChange={(e) => handleFilterChange('severity', e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Severities</option>
            <option value="CRITICAL">Critical</option>
            <option value="HIGH">High</option>
            <option value="MEDIUM">Medium</option>
            <option value="LOW">Low</option>
            <option value="INFO">Info</option>
          </select>

          <select
            value={filters.status}
            onChange={(e) => handleFilterChange('status', e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Statuses</option>
            <option value="OPEN">Open</option>
            <option value="IN_PROGRESS">In Progress</option>
            <option value="INVESTIGATING">Investigating</option>
            <option value="RESOLVED">Resolved</option>
            <option value="CLOSED">Closed</option>
            <option value="FALSE_POSITIVE">False Positive</option>
          </select>

          <input
            type="text"
            placeholder="Source"
            value={filters.source}
            onChange={(e) => handleFilterChange('source', e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />

          <input
            type="text"
            placeholder="Assigned to"
            value={filters.assigned_to}
            onChange={(e) => handleFilterChange('assigned_to', e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div className="text-sm text-gray-600">
          Showing {alerts.length} alerts
        </div>
      </div>

      {/* Alerts Table */}
      <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Alert ID
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Title
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Severity
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Source
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                MITRE Techniques
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                First Seen
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {alerts.map((alert) => (
              <tr key={alert.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {alert.alert_id}
                </td>
                <td className="px-6 py-4 text-sm text-gray-900">
                  <div className="font-medium">{alert.title}</div>
                  <div className="text-xs text-gray-500 truncate max-w-xs">{alert.description}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span
                    className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                    style={{
                      backgroundColor: `${getSeverityColor(alert.severity)}20`,
                      color: getSeverityColor(alert.severity),
                    }}
                  >
                    {alert.severity}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span
                    className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                    style={{
                      backgroundColor: `${getStatusColor(alert.status)}20`,
                      color: getStatusColor(alert.status),
                    }}
                  >
                    {alert.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {alert.source}
                </td>
                <td className="px-6 py-4 text-sm text-gray-900">
                  {alert.mitre_techniques.length > 0 ? (
                    <div className="flex flex-wrap gap-1">
                      {alert.mitre_techniques.slice(0, 3).map((tech, i) => (
                        <span key={i} className="text-xs bg-purple-100 text-purple-800 px-2 py-0.5 rounded">
                          {tech}
                        </span>
                      ))}
                      {alert.mitre_techniques.length > 3 && (
                        <span className="text-xs text-gray-500">+{alert.mitre_techniques.length - 3}</span>
                      )}
                    </div>
                  ) : (
                    '-'
                  )}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {formatTimestamp(alert.first_seen)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm">
                  <select
                    value={alert.status}
                    onChange={(e) => handleStatusUpdate(alert.id, e.target.value)}
                    className="px-2 py-1 border border-gray-300 rounded text-xs focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="OPEN">Open</option>
                    <option value="IN_PROGRESS">In Progress</option>
                    <option value="INVESTIGATING">Investigating</option>
                    <option value="RESOLVED">Resolved</option>
                    <option value="CLOSED">Closed</option>
                    <option value="FALSE_POSITIVE">False Positive</option>
                  </select>
                </td>
              </tr>
            ))}
            {alerts.length === 0 && (
              <tr>
                <td colSpan={8} className="px-6 py-12 text-center text-gray-500">
                  No alerts found
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
