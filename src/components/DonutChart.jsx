export default function DonutChart({ percentage }) {
  const r = 68
  const cx = 90
  const cy = 90
  const circumference = 2 * Math.PI * r
  const filled = (Math.min(Math.max(percentage, 0), 100) / 100) * circumference

  return (
    <div className="donut-wrap">
      <svg width="180" height="180" viewBox="0 0 180 180">
        <circle cx={cx} cy={cy} r={r} fill="none" stroke="#e2e8f0" strokeWidth="20" />
        <circle
          cx={cx} cy={cy} r={r}
          fill="none"
          stroke="#0ea5e9"
          strokeWidth="20"
          strokeDasharray={`${filled} ${circumference - filled}`}
          strokeLinecap="round"
          transform={`rotate(-90 ${cx} ${cy})`}
          style={{ transition: 'stroke-dasharray 0.6s ease' }}
        />
        <text
          x={cx} y={cy - 8}
          textAnchor="middle" dominantBaseline="middle"
          fontSize="26" fontWeight="700" fill="#0f172a"
        >
          {percentage.toFixed(1)}%
        </text>
        <text
          x={cx} y={cy + 18}
          textAnchor="middle"
          fontSize="11" fill="#64748b"
        >
          match score
        </text>
      </svg>
    </div>
  )
}
