export default function ToolGrid({ tools, selected, onSelect }) {
  return (
    <div className="tool-grid">
      {tools.map((tool) => (
        <button
          key={tool.id}
          className={`tool-card${selected.id === tool.id ? ' selected' : ''}`}
          onClick={() => onSelect(tool)}
        >
          <span className="tool-icon">{tool.icon}</span>
          <span className="tool-title">{tool.title}</span>
          <span className="tool-desc">{tool.desc}</span>
        </button>
      ))}
    </div>
  )
}
