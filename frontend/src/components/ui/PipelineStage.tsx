import { LucideIcon, icons } from 'lucide-react'
import type { PipelineStage } from '@schemas/dashboard'

interface PipelineStageProps {
  stage: PipelineStage
  isLast: boolean
}

export function PipelineStage({ stage, isLast }: PipelineStageProps) {
  const IconComponent = icons[stage.icon as keyof typeof icons] as LucideIcon | undefined

  return (
    <div className="flex items-center gap-2">
      <div className={`pipeline-stage ${stage.status === 'active' ? 'pipeline-stage-active' : ''}`}>
        <div className="flex items-center gap-3">
          <div className={`p-2 rounded-sm ${stage.status === 'active' ? 'bg-primary/20' : 'bg-surface-elevated'}`}>
            {IconComponent && <IconComponent className={`w-4 h-4 ${stage.status === 'active' ? 'text-primary' : 'text-gray-500'}`} />}
          </div>
          <div>
            <p className="text-xs font-semibold text-gray-100">{stage.name}</p>
            <p className="text-xs text-gray-400">{stage.description}</p>
          </div>
          <div className="ml-auto">
            <p className="text-sm font-bold text-gray-100">{stage.count.toLocaleString()}</p>
          </div>
        </div>
      </div>
      {!isLast && (
        <div className="flex items-center">
          <div className={`w-8 h-px ${stage.status === 'active' ? 'bg-primary' : 'bg-border'}`} />
          <div className={`w-2 h-2 rounded-full ${stage.status === 'active' ? 'bg-primary' : 'bg-border'}`} />
        </div>
      )}
    </div>
  )
}
