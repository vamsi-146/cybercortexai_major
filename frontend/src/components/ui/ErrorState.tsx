import { AlertCircle, RefreshCw } from 'lucide-react'

interface ErrorStateProps {
  title?: string
  message: string
  onRetry?: () => void
}

export function ErrorState({ title = 'Error', message, onRetry }: ErrorStateProps) {
  return (
    <div className="flex flex-col items-center justify-center p-8 text-center">
      <div className="p-3 bg-critical/10 rounded-full mb-4">
        <AlertCircle className="w-8 h-8 text-critical" />
      </div>
      <h3 className="text-lg font-semibold text-gray-100 mb-2">{title}</h3>
      <p className="text-sm text-gray-400 mb-4 max-w-md">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="flex items-center gap-2 btn-primary"
        >
          <RefreshCw className="w-4 h-4" />
          Retry
        </button>
      )}
    </div>
  )
}
