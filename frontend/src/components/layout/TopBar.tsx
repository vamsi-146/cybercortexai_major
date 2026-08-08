import { Search, Bell, User, Clock, RefreshCw, LogOut } from 'lucide-react'
import { useAuth } from '@contexts/AuthContext'

export function TopBar() {
  const { user, logout } = useAuth()

  const handleLogout = async () => {
    await logout()
  }

  return (
    <header className="h-14 bg-surface border-b border-border flex items-center justify-between px-4">
      {/* Left - Page Title */}
      <div className="flex items-center gap-4">
        <div>
          <h1 className="text-lg font-semibold text-gray-100">SOC Dashboard</h1>
          <p className="text-xs text-gray-400">Real-time overview of your security operations</p>
        </div>
      </div>

      {/* Center - Search and Controls */}
      <div className="flex items-center gap-3">
        {/* Search */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
          <input
            type="text"
            placeholder="Search incidents, alerts, IPs, users, IOCs..."
            className="input-base pl-10 w-80"
          />
          <span className="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-gray-500 bg-surface-elevated px-1.5 py-0.5 rounded">
            CTRL + K
          </span>
        </div>

        {/* Time Range */}
        <div className="flex items-center gap-2 px-3 py-2 bg-surface-elevated border border-border rounded-sm">
          <Clock className="w-4 h-4 text-gray-400" />
          <select className="bg-transparent text-sm text-gray-300 focus:outline-none">
            <option>Last 24 hours</option>
            <option>Last 7 days</option>
            <option>Last 30 days</option>
          </select>
        </div>

        {/* Refresh */}
        <button className="p-2 text-gray-400 hover:text-gray-100 hover:bg-surface-elevated rounded-sm transition-colors">
          <RefreshCw className="w-4 h-4" />
        </button>
      </div>

      {/* Right - Notifications and User */}
      <div className="flex items-center gap-3">
        {/* System Status */}
        <div className="flex items-center gap-2 px-3 py-1.5 bg-success/10 border border-success/20 rounded-sm">
          <div className="w-2 h-2 bg-success rounded-full animate-pulse" />
          <span className="text-xs text-success font-medium">Operational</span>
        </div>

        {/* Notifications */}
        <button className="relative p-2 text-gray-400 hover:text-gray-100 hover:bg-surface-elevated rounded-sm transition-colors">
          <Bell className="w-4 h-4" />
          <span className="absolute top-1 right-1 w-2 h-2 bg-critical rounded-full" />
        </button>

        {/* User */}
        <div className="flex items-center gap-2 px-3 py-1.5 bg-surface-elevated border border-border rounded-sm">
          <div className="w-6 h-6 bg-primary/20 rounded-sm flex items-center justify-center">
            <User className="w-4 h-4 text-primary" />
          </div>
          <span className="text-sm text-gray-300">{user?.full_name || user?.username || 'User'}</span>
          <button
            onClick={handleLogout}
            className="ml-2 p-1 text-gray-400 hover:text-gray-100 hover:bg-surface-elevated rounded-sm transition-colors"
            title="Logout"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </header>
  )
}
