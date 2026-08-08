import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts'
import type { SeverityDistribution } from '@schemas/dashboard'

interface SeverityDistributionChartProps {
  data: SeverityDistribution[]
}

const COLORS = {
  CRITICAL: '#EF4444',
  HIGH: '#F97316',
  MEDIUM: '#EAB308',
  LOW: '#22C55E',
  INFO: '#06B6D4',
}

export function SeverityDistributionChart({ data }: SeverityDistributionChartProps) {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          innerRadius={40}
          outerRadius={60}
          paddingAngle={2}
          dataKey="count"
        >
          {data.map((entry) => (
            <Cell key={entry.severity} fill={COLORS[entry.severity as keyof typeof COLORS]} />
          ))}
        </Pie>
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
          verticalAlign="bottom"
          height={60}
        />
      </PieChart>
    </ResponsiveContainer>
  )
}
