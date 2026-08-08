import { useState } from 'react'
import { icons, type LucideIcon } from 'lucide-react'
import { Link, useLocation } from 'react-router-dom'

interface NavItem {
  icon: string
  label: string
  path: string
  children?: NavItem[]
}

interface NavSection {
  title: string
  items: NavItem[]
}

const navSections: NavSection[] = [
  {
    title: 'OVERVIEW',
    items: [
      { icon: 'LayoutDashboard', label: 'Dashboard', path: '/' },
    ],
  },
  {
    title: 'THREAT OPERATIONS',
    items: [
      { icon: 'AlertTriangle', label: 'Alerts', path: '/alerts' },
      { icon: 'FileText', label: 'Incidents', path: '/incidents' },
      { icon: 'Search', label: 'Investigations', path: '/investigations' },
      { icon: 'Shield', label: 'Detection Rules', path: '/detection-rules' },
    ],
  },
  {
    title: 'AI OPERATIONS',
    items: [
      { icon: 'BrainCircuit', label: 'AI Investigator', path: '/ai-investigator' },
      { icon: 'Cpu', label: 'Agent Activity', path: '/agent-activity' },
      { icon: 'GitMerge', label: 'Collaborative Reasoning', path: '/collaborative-reasoning' },
      { icon: 'Lightbulb', label: 'AI Recommendations', path: '/ai-recommendations' },
    ],
  },
  {
    title: 'INTELLIGENCE',
    items: [
      { icon: 'Globe', label: 'Threat Intelligence', path: '/threat-intel' },
      { icon: 'Target', label: 'IOC Explorer', path: '/ioc-explorer' },
      { icon: 'Network', label: 'MITRE ATT&CK', path: '/mitre-attack' },
      { icon: 'Bug', label: 'Vulnerabilities', path: '/vulnerabilities' },
      { icon: 'Database', label: 'Security Memory', path: '/security-memory' },
    ],
  },
  {
    title: 'GRAPH INTELLIGENCE',
    items: [
      { icon: 'Share2', label: 'Knowledge Graph', path: '/knowledge-graph' },
      { icon: 'Route', label: 'Attack Paths', path: '/attack-paths' },
      { icon: 'Zap', label: 'Blast Radius', path: '/blast-radius' },
      { icon: 'GitBranch', label: 'Asset Relationships', path: '/asset-relationships' },
    ],
  },
  {
    title: 'ANALYTICS',
    items: [
      { icon: 'BarChart3', label: 'Risk Analytics', path: '/risk-analytics' },
      { icon: 'TrendingUp', label: 'Prediction Analytics', path: '/prediction-analytics' },
      { icon: 'LineChart', label: 'Model Confidence', path: '/model-confidence' },
      { icon: 'FileBarChart', label: 'Reports', path: '/reports' },
    ],
  },
  {
    title: 'ADMINISTRATION',
    items: [
      { icon: 'Users', label: 'Users', path: '/users' },
      { icon: 'Server', label: 'Data Sources', path: '/data-sources' },
      { icon: 'ScrollText', label: 'Audit Logs', path: '/audit-logs' },
      { icon: 'Settings', label: 'Settings', path: '/settings' },
    ],
  },
]

export function Sidebar() {
  const [collapsed, setCollapsed] = useState(false)
  const location = useLocation()

  return (
    <aside 
      className={`fixed left-0 top-0 h-screen bg-surface border-r border-border transition-all duration-300 z-50 ${
        collapsed ? 'w-16' : 'w-64'
      }`}
    >
      {/* Brand */}
      <div className="flex items-center gap-3 px-4 py-4 border-b border-border">
        <div className="p-2 bg-primary/20 rounded-sm">
          <icons.Shield className="w-6 h-6 text-primary" />
        </div>
        {!collapsed && (
          <div>
            <h1 className="text-lg font-bold text-gray-100">CyberCortex</h1>
            <p className="text-xs text-gray-400">AI Security Operations</p>
          </div>
        )}
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto py-4">
        {navSections.map((section) => (
          <div key={section.title} className="mb-4">
            {!collapsed && (
              <p className="px-4 mb-2 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                {section.title}
              </p>
            )}
            {section.items.map((item) => {
              const IconComponent = icons[item.icon as keyof typeof icons] as LucideIcon
              const isActive = location.pathname === item.path

              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center gap-3 px-4 py-2.5 mx-2 rounded-sm transition-colors duration-200 ${
                    isActive 
                      ? 'bg-primary/10 text-primary border border-primary/20' 
                      : 'text-gray-400 hover:text-gray-100 hover:bg-surface-elevated'
                  }`}
                  title={collapsed ? item.label : undefined}
                >
                  <IconComponent className="w-4 h-4 flex-shrink-0" />
                  {!collapsed && <span className="text-sm">{item.label}</span>}
                </Link>
              )
            })}
          </div>
        ))}
      </nav>

      {/* Collapse Toggle */}
      <div className="border-t border-border p-4">
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="w-full flex items-center justify-center gap-2 px-3 py-2 text-sm text-gray-400 hover:text-gray-100 hover:bg-surface-elevated rounded-sm transition-colors duration-200"
        >
          <icons.Menu className="w-4 h-4" />
          {!collapsed && <span>Collapse</span>}
        </button>
      </div>
    </aside>
  )
}
