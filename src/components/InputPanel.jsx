import { useState, useEffect } from 'react'

export default function InputPanel({ tool, onRun, loading }) {
  const [jobDescription, setJobDescription] = useState('')
  const [file, setFile]                     = useState(null)
  const [companyName, setCompanyName]       = useState('')
  const [hiringManager, setHiringManager]   = useState('')
  const [focusAreas, setFocusAreas]         = useState('')
  const [jobCount, setJobCount]             = useState(5)

  // Reset conditional fields when tool changes
  useEffect(() => {
    setCompanyName('')
    setHiringManager('')
    setFocusAreas('')
    setJobCount(5)
  }, [tool.id])

  function handleSubmit(e) {
    e.preventDefault()
    if (!file || !jobDescription.trim()) return
    onRun({ file, jobDescription, companyName, hiringManager, focusAreas, jobCount })
  }

  const canRun = file && jobDescription.trim() && !loading

  return (
    <div className="panel">
      <form onSubmit={handleSubmit}>
        <div className="field">
          <label>Job Description</label>
          <textarea
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            rows={9}
            placeholder="Paste the job description here..."
          />
        </div>

        <div className="field">
          <label>Resume (PDF)</label>
          <div className="file-upload">
            <input
              id="resume-upload"
              type="file"
              accept=".pdf"
              onChange={(e) => setFile(e.target.files[0] || null)}
            />
            <label htmlFor="resume-upload" className="file-label">
              {file ? `📄 ${file.name}` : '📄 Choose PDF file'}
            </label>
          </div>
        </div>

        {tool.id === 'cover-letter' && (
          <>
            <div className="field">
              <label>Company Name</label>
              <input
                value={companyName}
                onChange={(e) => setCompanyName(e.target.value)}
                placeholder="e.g. Google"
              />
            </div>
            <div className="field">
              <label>Hiring Manager <span className="optional">(optional)</span></label>
              <input
                value={hiringManager}
                onChange={(e) => setHiringManager(e.target.value)}
                placeholder="e.g. Jane Smith"
              />
            </div>
            <div className="field">
              <label>Focus Areas <span className="optional">(comma-separated)</span></label>
              <input
                value={focusAreas}
                onChange={(e) => setFocusAreas(e.target.value)}
                placeholder="e.g. leadership, technical skills"
              />
            </div>
          </>
        )}

        {tool.id === 'job-search' && (
          <div className="field">
            <label>Number of Results: <strong>{jobCount}</strong></label>
            <input
              type="range"
              min={1}
              max={10}
              value={jobCount}
              onChange={(e) => setJobCount(Number(e.target.value))}
              className="range-input"
            />
          </div>
        )}

        <button type="submit" className="run-btn" disabled={!canRun}>
          {loading ? <span className="btn-spinner" /> : null}
          {loading ? 'Generating…' : 'Run'}
        </button>
      </form>
    </div>
  )
}
