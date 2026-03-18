import { useState } from 'react'
import TopicTree from './TopicTree'

export default function ResultsPanel({ data }) {
  const [viewMode, setViewMode] = useState('structured')

  const handleDownload = () => {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'syllabus_topics.json'
    a.click()
    URL.revokeObjectURL(url)
  }

  const topicCount = data?.topics?.length || 0
  const subtopicCount = data?.topics?.reduce((acc, t) => acc + (t.subtopics?.length || 0), 0) || 0

  return (
    <div className="results-panel">
      <div className="results-header">
        <h2 className="results-title">
          📊 Results — {topicCount} topics, {subtopicCount} subtopics
        </h2>
        <div className="results-actions">
          <button
            className={`action-btn ${viewMode === 'structured' ? 'active' : ''}`}
            onClick={() => setViewMode('structured')}
            id="view-structured-btn"
          >
            🌳 Tree View
          </button>
          <button
            className={`action-btn ${viewMode === 'raw' ? 'active' : ''}`}
            onClick={() => setViewMode('raw')}
            id="view-raw-btn"
          >
            { '{ }' } Raw JSON
          </button>
          <button className="action-btn" onClick={handleDownload} id="download-btn">
            ⬇️ Download
          </button>
        </div>
      </div>

      <div className="results-body">
        {viewMode === 'structured' ? (
          <TopicTree topics={data?.topics || []} />
        ) : (
          <div className="raw-json">
            <pre>{JSON.stringify(data, null, 2)}</pre>
          </div>
        )}
      </div>
    </div>
  )
}
