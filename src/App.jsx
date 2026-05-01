import { useState } from 'react'
import ToolGrid from './components/ToolGrid'
import InputPanel from './components/InputPanel'
import ResultPanel from './components/ResultPanel'
import { apiCall, checkHealth } from './api'

export const TOOLS = [
  { id: 'resume-analysis',  icon: '📊', title: 'Resume Analysis',  desc: 'Match score + recruiter feedback',    endpoint: '/api/resume/analyze' },
  { id: 'resume-optimizer', icon: '✨', title: 'Resume Optimizer', desc: 'Bullet-point resume improvements',    endpoint: '/api/resume/optimize' },
  { id: 'cover-letter',     icon: '✉️',  title: 'Cover Letter',     desc: 'Tailored 300–400 word letter',        endpoint: '/api/cover-letter' },
  { id: 'interview-prep',   icon: '🎯', title: 'Interview Prep',   desc: 'Technical & behavioral questions',    endpoint: '/api/interview-prep' },
  { id: 'market-position',  icon: '📈', title: 'Market Position',  desc: 'Rank vs. the ideal candidate',        endpoint: '/api/market-position' },
  { id: 'skill-plan',       icon: '🗺️',  title: 'Skill Plan',       desc: '3-month learning roadmap',            endpoint: '/api/skill-plan' },
  { id: 'job-search',       icon: '🔍', title: 'Job Search',       desc: 'Live listings matched to you',        endpoint: '/api/jobs/search' },
]

export default function App() {
  const [tool, setTool]       = useState(TOOLS[0])
  const [result, setResult]   = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError]     = useState(null)
  const [health, setHealth]   = useState(null)

  function selectTool(t) {
    setTool(t)
    setResult(null)
    setError(null)
  }

  async function handleRun(formValues) {
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const data = { job_description: formValues.jobDescription }
      if (tool.id === 'cover-letter') {
        data.company_name    = formValues.companyName    || 'Company'
        data.hiring_manager  = formValues.hiringManager  || 'Hiring Manager'
        data.focus_areas     = formValues.focusAreas     || 'balanced'
      }
      if (tool.id === 'job-search') {
        data.count = String(formValues.jobCount || 5)
      }
      const out = await apiCall(tool.endpoint, formValues.file, data)
      setResult({ toolId: tool.id, data: out })
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  async function handleHealthCheck() {
    try {
      const h = await checkHealth()
      setHealth(`✅ API OK — model: ${h.model}`)
    } catch {
      setHealth('❌ Health check failed')
    }
  }

  return (
    <div className="app">
      <header className="hero">
        <div className="hero-text">
          <h1>ResAI Campus</h1>
          <p>AI career copilot — resume, interviews, and job targeting in one place.</p>
        </div>
        <div className="hero-actions">
          <button className="health-btn" onClick={handleHealthCheck}>Check API</button>
          {health && <span className="health-status">{health}</span>}
        </div>
      </header>

      <ToolGrid tools={TOOLS} selected={tool} onSelect={selectTool} />

      <div className="main-layout">
        <InputPanel tool={tool} onRun={handleRun} loading={loading} />
        <ResultPanel tool={tool} result={result} loading={loading} error={error} />
      </div>
    </div>
  )
}
