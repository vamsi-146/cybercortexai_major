import { useState, useEffect } from 'react'
import { Link, useParams } from 'react-router-dom'
import { ArrowLeft, Clock, Shield, Target, FileText, Network, MessageSquare, Activity, ChevronRight } from 'lucide-react'
import { SeverityBadge } from '@components/ui/SeverityBadge'
import { LoadingState } from '@components/ui/LoadingState'
import { AlertEvidence } from '@components/alerts/AlertEvidence'
import { incidentsApi } from '@services/api/incidentsApi'
import { alertsApi, Alert } from '@services/api/alertsApi'

export function IncidentDetail() {
  const { id } = useParams<{ id: string }>()
  const [activeTab, setActiveTab] = useState('overview')
  const [incident, setIncident] = useState<any>(null)
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (id) {
      loadIncident(id)
    }
  }, [id])

  const loadIncident = async (incidentId: string) => {
    try {
      setLoading(true)
      const data = await incidentsApi.getById(incidentId)
      setIncident(data)
      
      // Load related alerts if alert_ids exist
      if (data.alert_ids && data.alert_ids.length > 0) {
        try {
          const alertPromises = data.alert_ids.map((alertId: string) => 
            alertsApi.getById(alertId).catch(() => null)
          )
          const loadedAlerts = await Promise.all(alertPromises)
          setAlerts(loadedAlerts.filter((a: Alert | null): a is Alert => a !== null))
        } catch (err) {
          console.error('Failed to load alerts:', err)
        }
      }
    } catch (err) {
      console.error('Failed to load incident:', err)
      setError('Failed to load incident')
    } finally {
      setLoading(false)
    }
  }

  const tabs = [
    { id: 'overview', label: 'Overview', icon: FileText },
    { id: 'evidence', label: 'Evidence', icon: Shield },
    { id: 'reasoning', label: 'Agent Reasoning', icon: Network },
    { id: 'graph', label: 'Knowledge Graph', icon: Network },
    { id: 'attack-path', label: 'Attack Path', icon: ChevronRight },
    { id: 'explainability', label: 'Explainability', icon: MessageSquare },
    { id: 'timeline', label: 'Timeline', icon: Clock },
  ]

  if (loading) {
    return (
      <div className="min-h-screen bg-background bg-grid">
        <div className="flex">
          <main className="flex-1 ml-64 p-4">
            <LoadingState message="Loading incident..." />
          </main>
        </div>
      </div>
    )
  }

  if (error || !incident) {
    return (
      <div className="min-h-screen bg-background bg-grid">
        <div className="flex">
          <main className="flex-1 ml-64 p-4">
            <div className="card-base p-8 text-center">
              <p className="text-critical mb-4">Failed to load incident</p>
              <Link to="/" className="btn-primary inline-block">
                Back to Dashboard
              </Link>
            </div>
          </main>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background bg-grid">
      <div className="flex">
        {/* Main Content */}
        <main className="flex-1 ml-64 p-4">
          {/* Header */}
          <div className="mb-4">
            <Link to="/" className="flex items-center gap-2 text-sm text-gray-400 hover:text-gray-100 mb-3">
              <ArrowLeft className="w-4 h-4" />
              Back to Dashboard
            </Link>
            <div className="flex items-start justify-between">
              <div>
                <div className="flex items-center gap-3 mb-2">
                  <h1 className="text-2xl font-bold text-gray-100">{incident.title}</h1>
                  <SeverityBadge severity={incident.severity} />
                </div>
                <div className="flex items-center gap-4 text-sm text-gray-400">
                  <span className="text-mono text-primary">{incident.incident_id}</span>
                  <span>•</span>
                  <span>Created {new Date(incident.created_at).toLocaleString()}</span>
                  <span>•</span>
                  <span>Updated {new Date(incident.updated_at).toLocaleString()}</span>
                  {incident.assigned_to && (
                    <>
                      <span>•</span>
                      <span>Assigned to {incident.assigned_to}</span>
                    </>
                  )}
                </div>
              </div>
              <div className="flex items-center gap-2">
                <div className="text-right">
                  <p className="text-xs text-gray-400">Risk Score</p>
                  <p className="text-3xl font-bold text-critical">{incident.risk_score}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Tabs */}
          <div className="card-base mb-4">
            <div className="flex border-b border-border">
              {tabs.map((tab) => {
                const Icon = tab.icon
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex items-center gap-2 px-4 py-3 text-sm font-medium transition-colors border-b-2 ${
                      activeTab === tab.id
                        ? 'text-primary border-primary'
                        : 'text-gray-400 border-transparent hover:text-gray-100'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    {tab.label}
                  </button>
                )
              })}
            </div>
          </div>

          {/* Tab Content */}
          <div className="space-y-4">
            {activeTab === 'overview' && (
              <div className="grid grid-cols-12 gap-4">
                {/* Left Column - 8 columns */}
                <div className="col-span-8 space-y-4">
                  {/* Description */}
                  <div className="card-base p-4">
                    <div className="panel-header border-b-0 mb-3">
                      <h2 className="panel-title">
                        <FileText className="w-4 h-4 text-primary" />
                        Incident Summary
                      </h2>
                    </div>
                    <p className="text-sm text-gray-300 leading-relaxed">{incident.description}</p>
                  </div>

                  {/* Affected Assets */}
                  {incident.affected_assets && incident.affected_assets.length > 0 && (
                    <div className="card-base p-4">
                      <div className="panel-header border-b-0 mb-3">
                        <h2 className="panel-title">
                          <Target className="w-4 h-4 text-primary" />
                          Affected Assets
                        </h2>
                      </div>
                      <div className="space-y-2">
                        {incident.affected_assets.map((asset: any) => (
                          <div key={asset.id} className="flex items-center justify-between p-3 bg-surface-elevated border border-border rounded-sm">
                            <div className="flex items-center gap-3">
                              <div className="p-2 bg-primary/10 rounded-sm">
                                <Activity className="w-4 h-4 text-primary" />
                              </div>
                              <div>
                                <p className="text-sm font-medium text-gray-100">{asset.name}</p>
                                <p className="text-xs text-gray-400">{asset.type}</p>
                              </div>
                            </div>
                            <span className={`badge badge-${asset.criticality.toLowerCase()}`}>
                              {asset.criticality}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Timeline */}
                  {incident.timeline && incident.timeline.length > 0 && (
                    <div className="card-base p-4">
                      <div className="panel-header border-b-0 mb-3">
                        <h2 className="panel-title">
                          <Clock className="w-4 h-4 text-primary" />
                          Timeline Preview
                        </h2>
                      </div>
                      <div className="space-y-3">
                        {incident.timeline.slice(0, 4).map((event: any, index: number) => (
                          <div key={index} className="flex gap-3">
                            <div className="flex flex-col items-center">
                              <div className={`w-2 h-2 rounded-full ${
                                event.severity === 'CRITICAL' ? 'bg-critical' : 
                                event.severity === 'HIGH' ? 'bg-high' : 'bg-primary'
                              }`} />
                              {index < incident.timeline.slice(0, 4).length - 1 && (
                                <div className="w-0.5 h-full bg-border mt-1" />
                              )}
                            </div>
                          <div className="flex-1 pb-3">
                            <div className="flex items-center justify-between mb-1">
                              <p className="text-sm font-medium text-gray-100">{event.event}</p>
                              <span className="text-xs text-gray-400">{event.timestamp}</span>
                            </div>
                            <p className="text-xs text-gray-400">{event.description}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                  )}
                </div>

                {/* Right Column - 4 columns */}
                <div className="col-span-4 space-y-4">
                  {/* Observed Indicators */}
                  {incident.indicators && incident.indicators.length > 0 && (
                    <div className="card-base p-4">
                      <div className="panel-header border-b-0 mb-3">
                        <h2 className="panel-title">
                          <Shield className="w-4 h-4 text-primary" />
                          Observed Indicators
                        </h2>
                      </div>
                      <div className="space-y-2">
                        {incident.indicators.map((indicator: any, index: number) => (
                          <div key={index} className="p-2 bg-surface-elevated border border-border rounded-sm">
                            <div className="flex items-center justify-between mb-1">
                              <span className="text-xs text-gray-400">{indicator.type}</span>
                              <span className="text-xs text-primary">{(indicator.confidence * 100).toFixed(0)}%</span>
                            </div>
                            <p className="text-mono text-xs text-gray-300 truncate">{indicator.value}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* MITRE Techniques */}
                  {incident.mitre_techniques && incident.mitre_techniques.length > 0 && (
                    <div className="card-base p-4">
                      <div className="panel-header border-b-0 mb-3">
                        <h2 className="panel-title">
                          <Target className="w-4 h-4 text-primary" />
                          MITRE Techniques
                        </h2>
                      </div>
                      <div className="flex flex-wrap gap-2">
                        {incident.mitre_techniques.map((tech: string) => (
                          <span key={tech} className="text-mono text-xs text-primary bg-primary/10 px-2 py-1 rounded-sm border border-primary/20">
                            {tech}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Risk Assessment */}
                  {(incident as any).risk_assessment && (incident as any).risk_assessment.factors && (
                    <div className="card-base p-4">
                      <div className="panel-header border-b-0 mb-3">
                        <h2 className="panel-title">
                          <Shield className="w-4 h-4 text-primary" />
                          Risk Assessment
                        </h2>
                      </div>
                      <div className="space-y-3">
                        {(incident as any).risk_assessment.factors.map((factor: any, index: number) => (
                          <div key={index}>
                            <div className="flex items-center justify-between mb-1">
                              <span className="text-xs text-gray-300">{factor.factor}</span>
                              <span className="text-xs text-primary">{(factor.impact * 100).toFixed(0)}%</span>
                            </div>
                            <div className="w-full h-1.5 bg-surface-elevated rounded-full overflow-hidden">
                              <div 
                                className="h-full bg-primary" 
                                style={{ width: `${factor.impact * 100}%` }}
                              />
                            </div>
                            <p className="text-xs text-gray-400 mt-1">{factor.description}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Recommended Actions */}
                  {incident.recommendations && incident.recommendations.length > 0 && (
                    <div className="card-base p-4">
                      <div className="panel-header border-b-0 mb-3">
                        <h2 className="panel-title">
                          <Activity className="w-4 h-4 text-primary" />
                          Recommended Actions
                        </h2>
                      </div>
                      <div className="space-y-2">
                        {incident.recommendations.map((action: string, index: number) => (
                          <div key={index} className="flex items-start gap-2 p-2 bg-surface-elevated border border-border rounded-sm">
                            <div className="w-5 h-5 bg-primary/20 rounded-sm flex items-center justify-center flex-shrink-0 mt-0.5">
                              <span className="text-xs text-primary font-medium">{index + 1}</span>
                            </div>
                            <p className="text-xs text-gray-300">{action}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}

            {activeTab === 'reasoning' && (
              <div className="card-base p-8 text-center">
                <Activity className="w-12 h-12 text-gray-500 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-100 mb-2">Agent Reasoning Coming Soon</h3>
                <p className="text-sm text-gray-400">Multi-agent collaborative reasoning will be available in Phase 5</p>
              </div>
            )}

            {activeTab === 'graph' && (
              <div className="card-base p-8 text-center">
                <Network className="w-12 h-12 text-gray-500 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-100 mb-2">Knowledge Graph Coming Soon</h3>
                <p className="text-sm text-gray-400">Dynamic knowledge graph visualization will be available in Phase 7</p>
              </div>
            )}

            {activeTab === 'attack-path' && (
              <div className="card-base p-8 text-center">
                <ChevronRight className="w-12 h-12 text-gray-500 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-100 mb-2">Attack Path Prediction Coming Soon</h3>
                <p className="text-sm text-gray-400">ML-based attack path prediction will be available in Phase 9</p>
              </div>
            )}

            {activeTab === 'explainability' && (
              <div className="card-base p-8 text-center">
                <MessageSquare className="w-12 h-12 text-gray-500 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-100 mb-2">Explainability Engine Coming Soon</h3>
                <p className="text-sm text-gray-400">Natural language explanations will be available in Phase 5</p>
              </div>
            )}

            {activeTab === 'timeline' && (
              <div className="card-base p-8 text-center">
                <Clock className="w-12 h-12 text-gray-500 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-100 mb-2">Full Timeline Coming Soon</h3>
                <p className="text-sm text-gray-400">Full incident timeline will be available in Phase 4</p>
              </div>
            )}

            {activeTab === 'evidence' && (
              <div className="space-y-4">
                {alerts.length > 0 ? (
                  alerts.map((alert) => (
                    <div key={alert.id} className="card-base p-4">
                      <div className="panel-header border-b-0 mb-3">
                        <h2 className="panel-title">
                          <Shield className="w-4 h-4 text-primary" />
                          Alert: {alert.title}
                        </h2>
                        <span className="text-xs text-gray-400">{alert.alert_id}</span>
                      </div>
                      <AlertEvidence 
                        detectionEvidence={(alert as any).detection_evidence}
                        correlationData={(alert as any).correlation_data}
                      />
                    </div>
                  ))
                ) : (
                  <div className="card-base p-8 text-center">
                    <Shield className="w-12 h-12 text-gray-500 mx-auto mb-4" />
                    <h3 className="text-lg font-semibold text-gray-100 mb-2">No Alerts Found</h3>
                    <p className="text-sm text-gray-400">This incident has no associated alerts with detection evidence</p>
                  </div>
                )}
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  )
}
