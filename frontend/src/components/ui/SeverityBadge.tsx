import type { Severity } from '@schemas/common'

interface SeverityBadgeProps {
  severity: Severity
}

export function SeverityBadge({ severity }: SeverityBadgeProps) {
  const badgeClass = `badge badge-${severity.toLowerCase()}`

  return (
    <span className={badgeClass}>
      <span className={`status-dot status-dot-${severity.toLowerCase()}`} />
      {severity}
    </span>
  )
}
