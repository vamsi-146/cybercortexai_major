import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import type { ThreatActivityPoint } from '@schemas/dashboard'

interface ThreatActivityChartProps {
  data: ThreatActivityPoint[]
}

export function ThreatActivityChart({ data }: ThreatActivityChartProps) {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <LineChart data={data} margin={{ top: 5, right: 5, bottom: 5, left: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" vertical={false} />
        <XAxis 
          dataKey="timestamp" 
          stroke="#64748B" 
          fontSize={11}
          tickLine={false}
        />
        <YAxis 
          stroke="#64748B" 
          fontSize={11}
          tickLine={false}
        />
        <Tooltip 
          contentStyle={{ 
            backgroundColor: '#0D1219', 
            border: '1px solid #1E293B',
            borderRadius: '4px',
            fontSize: '12px',
          }}
          itemStyle={{ color: '#E2E8F0' }}
        />
        <Legend 
          wrapperStyle={{ fontSize: '11px', color: '#94A3B8' }}
          iconType="circle"
        />
        <Line 
          type="monotone" 
          dataKey="events" 
          stroke="#06B6D4" 
          strokeWidth={2}
          dot={false}
          name="Events"
        />
        <Line 
          type="monotone" 
          dataKey="alerts" 
          stroke="#F97316" 
          strokeWidth={2}
          dot={false}
          name="Alerts"
        />
        <Line 
          type="monotone" 
          dataKey="incidents" 
          stroke="#EF4444" 
          strokeWidth={2}
          dot={false}
          name="Incidents"
        />
      </LineChart>
    </ResponsiveContainer>
  )
}
