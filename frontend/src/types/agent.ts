import { AgentState } from './common'

export interface AgentActivity {
  id: string
  name: string
  task: string
  state: AgentState
  duration: string
  icon: string
}

export interface AgentContribution {
  agentName: string
  confidence: number
  findings: string
  evidence: Evidence[]
}

export interface Evidence {
  type: string
  value: string
  confidence: number
}

export interface CollaborativeReasoning {
  overallConfidence: number
  keyInsights: string[]
  conflictingFindings: Conflict[]
  finalAssessment: string
}

export interface Conflict {
  agent: string
  finding: string
  resolution: string
}
