import { Loader2 } from 'lucide-react'

interface LoadingStateProps {
  message?: string
}

export function LoadingState({ message = 'Loading...' }: LoadingStateProps) {
  return (
    <div className="flex flex-col items-center justify-center p-8">
      <Loader2 className="w-8 h-8 text-primary animate-spin mb-3" />
      <p className="text-sm text-gray-400">{message}</p>
    </div>
  )
}
