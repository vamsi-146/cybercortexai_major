interface DetectionEvidence {
  triggering_event_id: string
  triggering_event_timestamp: string
  reason: string
  evidence: any[]
  correlated_event_ids: string[]
  threshold_used?: any
  time_window_seconds?: number
}

interface CorrelationData {
  correlation_score: number
  correlated_event_ids: string[]
  entity_matches: Record<string, any>
  time_window_seconds: number
}

interface AlertEvidenceProps {
  detectionEvidence?: DetectionEvidence
  correlationData?: CorrelationData
}

export function AlertEvidence({ detectionEvidence, correlationData }: AlertEvidenceProps) {
  if (!detectionEvidence && !correlationData) {
    return (
      <div className="text-sm text-gray-500 italic">
        No detection evidence available
      </div>
    )
  }

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString()
  }

  return (
    <div className="space-y-4">
      {/* Detection Evidence */}
      {detectionEvidence && (
        <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
          <h3 className="text-sm font-semibold text-gray-900 mb-3 flex items-center gap-2">
            <span className="w-2 h-2 bg-blue-500 rounded-full"></span>
            Detection Evidence
          </h3>
          
          <div className="space-y-3 text-sm">
            <div className="grid grid-cols-2 gap-2">
              <div>
                <span className="text-gray-500">Triggering Event ID:</span>
                <div className="font-mono text-gray-900">{detectionEvidence.triggering_event_id}</div>
              </div>
              <div>
                <span className="text-gray-500">Timestamp:</span>
                <div className="text-gray-900">{formatTimestamp(detectionEvidence.triggering_event_timestamp)}</div>
              </div>
            </div>

            <div>
              <span className="text-gray-500">Reason:</span>
              <div className="text-gray-900 mt-1">{detectionEvidence.reason}</div>
            </div>

            {detectionEvidence.threshold_used && (
              <div className="grid grid-cols-2 gap-2">
                <div>
                  <span className="text-gray-500">Threshold:</span>
                  <div className="text-gray-900">{String(detectionEvidence.threshold_used)}</div>
                </div>
                {detectionEvidence.time_window_seconds && (
                  <div>
                    <span className="text-gray-500">Time Window:</span>
                    <div className="text-gray-900">{detectionEvidence.time_window_seconds}s</div>
                  </div>
                )}
              </div>
            )}

            {detectionEvidence.evidence && detectionEvidence.evidence.length > 0 && (
              <div>
                <span className="text-gray-500">Evidence Details:</span>
                <div className="mt-2 bg-white rounded border border-gray-200 p-3">
                  <pre className="text-xs text-gray-800 whitespace-pre-wrap overflow-auto max-h-48">
                    {JSON.stringify(detectionEvidence.evidence, null, 2)}
                  </pre>
                </div>
              </div>
            )}

            {detectionEvidence.correlated_event_ids && detectionEvidence.correlated_event_ids.length > 0 && (
              <div>
                <span className="text-gray-500">Correlated Events ({detectionEvidence.correlated_event_ids.length}):</span>
                <div className="mt-1 flex flex-wrap gap-1">
                  {detectionEvidence.correlated_event_ids.slice(0, 10).map((eventId, idx) => (
                    <span key={idx} className="text-xs bg-blue-100 text-blue-800 px-2 py-0.5 rounded font-mono">
                      {eventId}
                    </span>
                  ))}
                  {detectionEvidence.correlated_event_ids.length > 10 && (
                    <span className="text-xs text-gray-500">
                      +{detectionEvidence.correlated_event_ids.length - 10} more
                    </span>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Correlation Data */}
      {correlationData && (
        <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
          <h3 className="text-sm font-semibold text-gray-900 mb-3 flex items-center gap-2">
            <span className="w-2 h-2 bg-purple-500 rounded-full"></span>
            Correlation Analysis
          </h3>
          
          <div className="space-y-3 text-sm">
            <div className="grid grid-cols-2 gap-2">
              <div>
                <span className="text-gray-500">Correlation Score:</span>
                <div className="flex items-center gap-2">
                  <div className="text-2xl font-bold text-gray-900">{correlationData.correlation_score}</div>
                  <div className="text-xs text-gray-500">/ 100</div>
                </div>
              </div>
              <div>
                <span className="text-gray-500">Time Window:</span>
                <div className="text-gray-900">{correlationData.time_window_seconds}s</div>
              </div>
            </div>

            {correlationData.entity_matches && Object.keys(correlationData.entity_matches).length > 0 && (
              <div>
                <span className="text-gray-500">Entity Matches:</span>
                <div className="mt-1 space-y-1">
                  {Object.entries(correlationData.entity_matches).map(([entity, count]) => (
                    <div key={entity} className="flex justify-between text-xs">
                      <span className="text-gray-700">{entity}:</span>
                      <span className="font-medium text-gray-900">{String(count)}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {correlationData.correlated_event_ids && correlationData.correlated_event_ids.length > 0 && (
              <div>
                <span className="text-gray-500">Total Correlated Events:</span>
                <div className="text-gray-900 font-medium">{correlationData.correlated_event_ids.length}</div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
