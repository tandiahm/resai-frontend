import ReactMarkdown from 'react-markdown'
import DonutChart from './DonutChart'

function Empty() {
  return (
    <div className="result-empty">
      <span className="result-empty-icon">✨</span>
      <p>Upload your resume and paste a job description, then hit <strong>Run</strong> to get started.</p>
    </div>
  )
}

function Spinner() {
  return (
    <div className="result-loading">
      <div className="spinner" />
      <p>Generating — this may take a moment…</p>
    </div>
  )
}

export default function ResultPanel({ tool, result, loading, error }) {
  return (
    <div className="panel result-panel">
      <h2 className="result-heading">
        {tool.icon}&nbsp;&nbsp;{tool.title}
      </h2>

      {loading && <Spinner />}

      {!loading && error && (
        <div className="result-error">
          <strong>Request failed</strong>
          <p>{error}</p>
        </div>
      )}

      {!loading && !error && !result && <Empty />}

      {!loading && !error && result && <ResultBody result={result} />}
    </div>
  )
}

function ResultBody({ result }) {
  const { toolId, data } = result

  if (toolId === 'resume-analysis') {
    const pct = parseFloat(data.match_percentage || 0)
    return (
      <>
        <DonutChart percentage={pct} />
        <hr className="divider" />
        <div className="markdown-body">
          <ReactMarkdown>{data.analysis}</ReactMarkdown>
        </div>
      </>
    )
  }

  if (toolId === 'resume-optimizer') {
    return (
      <div className="markdown-body">
        <h3>Suggestions</h3>
        <ReactMarkdown>{data.suggestions}</ReactMarkdown>
        <h3>Target Keywords</h3>
        <div className="keyword-list">
          {(data.keywords || []).map((kw) => (
            <span key={kw} className="keyword-tag">{kw}</span>
          ))}
        </div>
      </div>
    )
  }

  if (toolId === 'cover-letter') {
    return (
      <>
        <div className="markdown-body">
          <ReactMarkdown>{data.content}</ReactMarkdown>
        </div>
        <a
          className="download-btn"
          href={`data:text/plain;charset=utf-8,${encodeURIComponent(data.content)}`}
          download="cover_letter.txt"
        >
          ⬇ Download Cover Letter
        </a>
      </>
    )
  }

  // interview-prep, market-position, skill-plan, job-search
  const content = data.content || data.results_markdown || ''
  return (
    <div className="markdown-body">
      <ReactMarkdown>{content}</ReactMarkdown>
    </div>
  )
}
