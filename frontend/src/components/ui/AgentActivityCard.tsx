import { LucideIcon, icons } from 'lucide-react'
import type { AgentActivity } from '@schemas/agent'

interface AgentActivityCardProps {
  activity: AgentActivity
}

export function AgentActivityCard({ activity }: AgentActivityCardProps) {
  const IconComponent = icons[activity.icon as keyof typeof icons] as LucideIcon | undefined

  const stateColors = {
    RUNNING: 'text-primary',
    WAITING: 'text-medium',
    COMPLETED: 'text-success',
    FAILED: 'text-critical',
  }

  const stateDot = {
    RUNNING: 'status-dot-info',
    WAITING: 'status-dot-medium',
    COMPLETED: 'status-dot-success',
    FAILED: 'status-dot-critical',
  }

  return (
    <div className={`agent-card ${activity.state === 'RUNNING' ? 'agent-card-running' : ''}`}>
      <div className={`p-2 rounded-sm ${activity.state === 'RUNNING' ? 'bg-primary/20' : 'bg-surface-elevated'}`}>
        {IconComponent && <IconComponent className={`w-4 h-4 ${stateColors[activity.state]}`} />}
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-gray-100 truncate">{activity.name}</p>
        <p className="text-xs text-gray-400 truncate">{activity.task}</p>
      </div>
      <div className="flex items-center gap-2">
        <span className={`status-dot ${stateDot[activity.state]} ${activity.state === 'RUNNING' ? 'animate-pulse' : ''}`} />
        <span className="text-xs text-gray-400">{activity.duration}</span>
      </div>
    </div>
  )
}
