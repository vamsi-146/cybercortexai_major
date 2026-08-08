import { cn } from '@utils/cn'

interface SkeletonProps {
  className?: string
}

export function Skeleton({ className }: SkeletonProps) {
  return (
    <div
      className={cn('animate-pulse bg-surface-elevated rounded-sm', className)}
      role="status"
      aria-label="Loading"
    />
  )
}

export function MetricCardSkeleton() {
  return (
    <div className="metric-card">
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-3">
          <Skeleton className="w-8 h-8" />
          <div className="space-y-2">
            <Skeleton className="h-3 w-24" />
            <Skeleton className="h-6 w-16" />
          </div>
        </div>
        <Skeleton className="h-4 w-12" />
      </div>
    </div>
  )
}

export function TableRowSkeleton() {
  return (
    <tr>
      <td><Skeleton className="h-4 w-16" /></td>
      <td><Skeleton className="h-4 w-24" /></td>
      <td><Skeleton className="h-4 w-32" /></td>
      <td><Skeleton className="h-4 w-20" /></td>
      <td><Skeleton className="h-4 w-16" /></td>
      <td><Skeleton className="h-4 w-12" /></td>
      <td><Skeleton className="h-4 w-16" /></td>
      <td><Skeleton className="h-4 w-12" /></td>
    </tr>
  )
}
