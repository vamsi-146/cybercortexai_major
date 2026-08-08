import { LucideIcon, icons } from 'lucide-react'
import type { KPIMetric } from '@schemas/dashboard'

interface KPICardProps {
  metric: KPIMetric
}

export function KPICard({ metric }: KPICardProps) {
  const IconComponent = icons[metric.icon as keyof typeof icons] as LucideIcon | undefined

  const formatValue = (value: number | string, format?: string): string => {
    if (typeof value === 'string') return value

    switch (format) {
      case 'k':
        return (value / 1000).toFixed(1) + 'K'
      case 'm':
        return (value / 1000000).toFixed(1) + 'M'
      case 'percentage':
        return value + '%'
      default:
        return value.toLocaleString()
    }
  }

  const trendColor = metric.trend > 0 ? 'text-high' : metric.trend < 0 ? 'text-success' : 'text-gray-400'
  const trendIcon = metric.trend > 0 ? '↑' : metric.trend < 0 ? '↓' : '→'

  return (
    <div className="metric-card">
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-primary/10 rounded-sm">
            {IconComponent && <IconComponent className="w-4 h-4 text-primary" />}
          </div>
          <div>
            <p className="text-xs text-gray-400 uppercase tracking-wider">{metric.label}</p>
            <p className="text-2xl font-bold text-gray-100 mt-1">
              {formatValue(metric.value, metric.format)}
            </p>
          </div>
        </div>
        <div className={`text-xs ${trendColor} flex items-center gap-1`}>
          {trendIcon} {Math.abs(metric.trend)}%
        </div>
      </div>
    </div>
  )
}
