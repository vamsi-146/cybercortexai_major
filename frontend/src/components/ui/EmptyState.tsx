import { LucideIcon, icons } from 'lucide-react'

interface EmptyStateProps {
  icon?: string
  title: string
  description: string
  action?: {
    label: string
    onClick: () => void
  }
}

export function EmptyState({ icon, title, description, action }: EmptyStateProps) {
  const IconComponent = icon ? icons[icon as keyof typeof icons] as LucideIcon : null

  return (
    <div className="flex flex-col items-center justify-center p-8 text-center">
      {IconComponent && (
        <div className="p-3 bg-surface-elevated rounded-full mb-4">
          <IconComponent className="w-8 h-8 text-gray-500" />
        </div>
      )}
      <h3 className="text-lg font-semibold text-gray-100 mb-2">{title}</h3>
      <p className="text-sm text-gray-400 mb-4 max-w-md">{description}</p>
      {action && (
        <button
          onClick={action.onClick}
          className="btn-primary"
        >
          {action.label}
        </button>
      )}
    </div>
  )
}
