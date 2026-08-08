import type { Incident } from '@schemas/incident'
import { SeverityBadge } from '@components/ui/SeverityBadge'

interface RecentIncidentsTableProps {
  incidents: Incident[]
}

export function RecentIncidentsTable({ incidents }: RecentIncidentsTableProps) {
  return (
    <div className="overflow-x-auto">
      <table className="table-base">
        <thead>
          <tr>
            <th>Severity</th>
            <th>Incident ID</th>
            <th>Title</th>
            <th>Affected Entity</th>
            <th>MITRE Techniques</th>
            <th>Risk Score</th>
            <th>Status</th>
            <th>Updated</th>
          </tr>
        </thead>
        <tbody>
          {incidents.map((incident) => (
            <tr key={incident.id} className="cursor-pointer hover:bg-surface-elevated">
              <td>
                <SeverityBadge severity={incident.severity} />
              </td>
              <td className="text-mono text-primary">{incident.id}</td>
              <td className="font-medium text-gray-100">{incident.title}</td>
              <td className="text-mono">{incident.affectedEntity}</td>
              <td>
                <div className="flex gap-1 flex-wrap">
                  {incident.mitreTechniques.map((tech) => (
                    <span key={tech} className="text-xs text-mono text-gray-400 bg-surface-elevated px-1.5 py-0.5 rounded">
                      {tech}
                    </span>
                  ))}
                </div>
              </td>
              <td>
                <div className="flex items-center gap-2">
                  <div className="w-16 h-1.5 bg-surface-elevated rounded-full overflow-hidden">
                    <div 
                      className={`h-full ${incident.riskScore >= 80 ? 'bg-critical' : incident.riskScore >= 60 ? 'bg-high' : incident.riskScore >= 40 ? 'bg-medium' : 'bg-low'}`}
                      style={{ width: `${incident.riskScore}%` }}
                    />
                  </div>
                  <span className="text-sm font-medium text-gray-100">{incident.riskScore}</span>
                </div>
              </td>
              <td>
                <span className="text-xs text-gray-300">{incident.status.replace('_', ' ')}</span>
              </td>
              <td className="text-xs text-gray-400">{incident.updated}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
