import { useState, useEffect } from 'react'
import { KPICard } from '@components/ui/KPICard'
import { PipelineStage } from '@components/ui/PipelineStage'
import { ThreatActivityChart } from '@components/charts/ThreatActivityChart'
import { SeverityDistributionChart } from '@components/charts/SeverityDistributionChart'
import { RecentIncidentsTable } from '@components/dashboard/RecentIncidentsTable'
import { AgentActivityCard } from '@components/ui/AgentActivityCard'
import { LoadingState } from '@components/ui/LoadingState'
import { 
  pipelineStages, 
  threatActivityData, 
  mitreTechniques,
  riskTrendData,
} from '@data/demo/dashboardDemo'
import { agentActivities } from '@data/demo/incidentDemo'
import { dashboardApi } from '@services/api/dashboardApi'
import { LineChart, Line, ResponsiveContainer, CartesianGrid, XAxis, YAxis, Tooltip } from 'recharts'
import { Activity, Shield, Server, AlertTriangle, TrendingUp } from 'lucide-react'

export function Dashboard() {
  const [loading, setLoading] = useState(true)
  const [dashboardData, setDashboardData] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    try {
      setLoading(true)
      const data = await dashboardApi.getOverview()
      setDashboardData(data)
    } catch (err) {
      console.error('Failed to load dashboard data:', err)
      setError('Failed to load dashboard data')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background bg-grid">
        <div className="flex">
          <main className="flex-1 ml-64 p-4">
            <LoadingState message="Loading dashboard..." />
          </main>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-background bg-grid">
        <div className="flex">
          <main className="flex-1 ml-64 p-4">
            <div className="card-base p-8 text-center">
              <p className="text-critical mb-4">Failed to load dashboard</p>
              <button onClick={loadDashboardData} className="btn-primary">
                Retry
              </button>
            </div>
          </main>
        </div>
      </div>
    )
  }

  // Use API data when available, otherwise use demo data
  const kpiData = dashboardData ? [
    dashboardData.active_threats,
    dashboardData.critical_incidents,
    dashboardData.events_analyzed,
    dashboardData.ai_investigations,
    dashboardData.correlated_alerts,
    dashboardData.high_risk_assets,
  ] : []

  const severityDist = dashboardData?.severity_distribution || []
  const eventSources = dashboardData?.events_by_source || []
  const recentIncidents = dashboardData?.recent_incidents || []
  const systemHealth = dashboardData?.system_health || []
  const mitreTrends = dashboardData?.mitre_trends || []

  return (
    <div className="min-h-screen bg-background bg-grid">
      <div className="flex">
        {/* Main Content */}
        <main className="flex-1 ml-64 p-4">
          {/* KPI Row */}
          <div className="grid grid-cols-6 gap-3 mb-4">
            {kpiData.map((kpi) => (
              <KPICard key={kpi.id} metric={kpi} />
            ))}
          </div>

          {/* CyberCortex AI Pipeline */}
          <div className="card-base p-4 mb-4">
            <div className="panel-header border-b-0 mb-3">
              <h2 className="panel-title">
                <Activity className="w-4 h-4 text-primary" />
                CyberCortex AI Pipeline
              </h2>
            </div>
            <div className="flex items-center gap-2 overflow-x-auto pb-2">
              {pipelineStages.map((stage, index) => (
                <PipelineStage 
                  key={stage.id} 
                  stage={stage} 
                  isLast={index === pipelineStages.length - 1} 
                />
              ))}
            </div>
          </div>

          {/* Analytics Row */}
          <div className="grid grid-cols-12 gap-4 mb-4">
            {/* Threat Activity - 6 columns */}
            <div className="col-span-6 card-base p-4">
              <div className="panel-header border-b-0 mb-3">
                <h2 className="panel-title">
                  <TrendingUp className="w-4 h-4 text-primary" />
                  Threat Activity Over Time
                </h2>
              </div>
              <div className="chart-container">
                <ThreatActivityChart data={threatActivityData} />
              </div>
            </div>

            {/* Severity Distribution - 3 columns */}
            <div className="col-span-3 card-base p-4">
              <div className="panel-header border-b-0 mb-3">
                <h2 className="panel-title">
                  <Shield className="w-4 h-4 text-primary" />
                  Severity Distribution
                </h2>
              </div>
              <div className="chart-container">
                <SeverityDistributionChart data={severityDist} />
              </div>
            </div>

            {/* MITRE ATT&CK - 3 columns */}
            <div className="col-span-3 card-base p-4">
              <div className="panel-header border-b-0 mb-3">
                <h2 className="panel-title">
                  <AlertTriangle className="w-4 h-4 text-primary" />
                  Top MITRE Techniques
                </h2>
              </div>
              <div className="space-y-2">
                {mitreTechniques.map((technique) => (
                  <div key={technique.id} className="flex items-center gap-2">
                    <span className="text-mono text-xs text-primary w-12">{technique.id}</span>
                    <div className="flex-1 min-w-0">
                      <p className="text-xs text-gray-300 truncate">{technique.name}</p>
                      <div className="flex items-center gap-2 mt-1">
                        <div className="flex-1 h-1.5 bg-surface-elevated rounded-full overflow-hidden">
                          <div 
                            className="h-full bg-primary" 
                            style={{ width: `${technique.percentage}%` }}
                          />
                        </div>
                        <span className="text-xs text-gray-400">{technique.count}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Bottom Row */}
          <div className="grid grid-cols-12 gap-4">
            {/* Recent Incidents - 7 columns */}
            <div className="col-span-7 card-base p-4">
              <div className="panel-header border-b-0 mb-3">
                <h2 className="panel-title">
                  <AlertTriangle className="w-4 h-4 text-primary" />
                  Recent Incidents
                </h2>
              </div>
              <RecentIncidentsTable incidents={recentIncidents} />
            </div>

            {/* Right Column - 5 columns */}
            <div className="col-span-5 space-y-4">
              {/* Live Agent Activity */}
              <div className="card-base p-4">
                <div className="panel-header border-b-0 mb-3">
                  <h2 className="panel-title">
                    <Activity className="w-4 h-4 text-primary" />
                    Live Agent Activity
                  </h2>
                </div>
                <div className="space-y-2">
                  {agentActivities.map((activity) => (
                    <AgentActivityCard key={activity.id} activity={activity} />
                  ))}
                </div>
              </div>

              {/* Top MITRE Techniques */}
              <div className="card-base p-4">
                <div className="panel-header border-b-0 mb-3">
                  <h2 className="panel-title">
                    <Shield className="w-4 h-4 text-primary" />
                    Top MITRE Techniques
                  </h2>
                </div>
                <div className="space-y-2">
                  {mitreTrends.length > 0 ? (
                    mitreTrends.map((item: any, index: number) => (
                      <div key={index} className="flex items-center justify-between p-2 bg-surface-elevated border border-border rounded-sm">
                        <span className="text-mono text-xs text-primary">{item.technique}</span>
                        <span className="text-xs text-gray-400">{item.count}</span>
                      </div>
                    ))
                  ) : (
                    <div className="text-center text-xs text-gray-400 py-4">
                      No MITRE data available
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* Very Bottom Row */}
          <div className="grid grid-cols-12 gap-4 mt-4">
            {/* Events by Source - 4 columns */}
            <div className="col-span-4 card-base p-4">
              <div className="panel-header border-b-0 mb-3">
                <h2 className="panel-title">
                  <Server className="w-4 h-4 text-primary" />
                  Events by Source
                </h2>
              </div>
              <div className="space-y-2">
                {eventSources.map((source: any) => (
                  <div key={source.name} className="flex items-center gap-2">
                    <span className="text-xs text-gray-300 w-32 truncate">{source.name}</span>
                    <div className="flex-1 h-1.5 bg-surface-elevated rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-primary" 
                        style={{ width: `${source.percentage}%` }}
                      />
                    </div>
                    <span className="text-xs text-gray-400 w-12 text-right">{source.count}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Risk Trend - 4 columns */}
            <div className="col-span-4 card-base p-4">
              <div className="panel-header border-b-0 mb-3">
                <h2 className="panel-title">
                  <TrendingUp className="w-4 h-4 text-primary" />
                  Risk Trend
                </h2>
              </div>
              <div className="chart-container">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={riskTrendData} margin={{ top: 5, right: 5, bottom: 5, left: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" vertical={false} />
                    <XAxis 
                      dataKey="timestamp" 
                      stroke="#64748B" 
                      fontSize={11}
                      tickLine={false}
                    />
                    <YAxis 
                      stroke="#64748B" 
                      fontSize={11}
                      tickLine={false}
                    />
                    <Tooltip 
                      contentStyle={{ 
                        backgroundColor: '#0D1219', 
                        border: '1px solid #1E293B',
                        borderRadius: '4px',
                        fontSize: '12px',
                      }}
                      itemStyle={{ color: '#E2E8F0' }}
                    />
                    <Line 
                      type="monotone" 
                      dataKey="riskScore" 
                      stroke="#06B6D4" 
                      strokeWidth={2}
                      dot={false}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* System Health - 4 columns */}
            <div className="col-span-4 card-base p-4">
              <div className="panel-header border-b-0 mb-3">
                <h2 className="panel-title">
                  <Shield className="w-4 h-4 text-primary" />
                  System Health
                </h2>
              </div>
              <div className="space-y-2">
                {systemHealth.map((service: any) => (
                  <div key={service.name} className="flex items-center justify-between p-2 bg-surface-elevated rounded-sm">
                    <div className="flex items-center gap-2">
                      <div className={`w-2 h-2 rounded-full ${
                        service.status === 'OPERATIONAL' ? 'bg-success' : 
                        service.status === 'DEGRADED' ? 'bg-medium' : 'bg-critical'
                      }`} />
                      <span className="text-xs text-gray-300">{service.name}</span>
                    </div>
                    <div className="flex items-center gap-3">
                      {service.latency && (
                        <span className="text-xs text-gray-400">{service.latency}ms</span>
                      )}
                      {service.uptime && (
                        <span className="text-xs text-gray-400">{service.uptime}</span>
                      )}
                      <span className={`text-xs ${
                        service.status === 'OPERATIONAL' ? 'text-success' : 
                        service.status === 'DEGRADED' ? 'text-medium' : 'text-critical'
                      }`}>
                        {service.status}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}
