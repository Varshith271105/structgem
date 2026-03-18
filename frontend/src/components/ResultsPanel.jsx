import { useState } from 'react'
import TopicTree from './TopicTree'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function ResultsPanel({ data }) {
  const [viewMode, setViewMode] = useState('structured')
  const [pdfLoading, setPdfLoading] = useState(false)

  const handleDownloadJSON = () => {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'syllabus_topics.json'
    a.click()
    URL.revokeObjectURL(url)
  }

  const handleDownloadPDF = async () => {
    setPdfLoading(true)
    try {
      const res = await fetch(`${API_URL}/export-pdf`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      })
      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.detail || 'PDF generation failed')
      }
      const blob = await res.blob()
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'syllabus_topics.pdf'
      a.click()
      URL.revokeObjectURL(url)
    } catch (err) {
      alert('PDF download failed: ' + err.message)
    } finally {
      setPdfLoading(false)
    }
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
          <button className="action-btn" onClick={handleDownloadJSON} id="download-json-btn">
            ⬇️ JSON
          </button>
          <button
            className="action-btn pdf-btn"
            onClick={handleDownloadPDF}
            disabled={pdfLoading}
            id="download-pdf-btn"
          >
            {pdfLoading ? '⏳ Generating...' : '📄 PDF'}
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
