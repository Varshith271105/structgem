import { useState, useRef } from 'react'

export default function InputPanel({ onSubmit, loading }) {
  const [mode, setMode] = useState('text')
  const [text, setText] = useState('')
  const [file, setFile] = useState(null)
  const [dragover, setDragover] = useState(false)
  const fileRef = useRef()

  const handleSubmit = () => {
    if (mode === 'text' && text.trim()) {
      onSubmit({ text, file: null })
    } else if (mode === 'file' && file) {
      onSubmit({ text: null, file })
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setDragover(false)
    const f = e.dataTransfer.files[0]
    if (f && (f.name.endsWith('.pdf') || f.name.endsWith('.txt'))) {
      setFile(f)
    }
  }

  const canSubmit = (mode === 'text' && text.trim()) || (mode === 'file' && file)

  return (
    <div className="input-panel">
      <h2 className="panel-title">Analyze Syllabus</h2>
      <p className="panel-description">
        Paste your syllabus text or upload a PDF/TXT file to extract structured topics.
      </p>

      <div className="input-tabs">
        <button
          className={`tab-btn ${mode === 'text' ? 'active' : ''}`}
          onClick={() => setMode('text')}
        >
          ✏️ Paste Text
        </button>
        <button
          className={`tab-btn ${mode === 'file' ? 'active' : ''}`}
          onClick={() => setMode('file')}
        >
          📄 Upload File
        </button>
      </div>

      {mode === 'text' ? (
        <textarea
          className="text-input"
          placeholder="Paste your syllabus content here...&#10;&#10;Example:&#10;Unit 1: Introduction to Data Structures&#10;- Arrays, Linked Lists, Stacks, Queues&#10;Unit 2: Trees and Graphs&#10;- Binary Trees, BST, AVL Trees, Graph Traversals"
          value={text}
          onChange={(e) => setText(e.target.value)}
          id="syllabus-textarea"
        />
      ) : (
        <div>
          <div
            className={`file-upload-area ${dragover ? 'dragover' : ''}`}
            onClick={() => fileRef.current?.click()}
            onDragOver={(e) => { e.preventDefault(); setDragover(true) }}
            onDragLeave={() => setDragover(false)}
            onDrop={handleDrop}
          >
            <input
              type="file"
              ref={fileRef}
              accept=".pdf,.txt"
              onChange={(e) => setFile(e.target.files[0])}
              id="file-upload-input"
            />
            <div className="upload-icon">
              <svg viewBox="0 0 48 48" fill="none" stroke="currentColor" strokeWidth="1.5">
                <path d="M24 32V16M24 16l-8 8M24 16l8 8" strokeLinecap="round" strokeLinejoin="round" />
                <rect x="4" y="4" width="40" height="40" rx="8" strokeLinecap="round" />
              </svg>
            </div>
            <p className="upload-text">Click to browse or drag & drop</p>
            <p className="upload-hint">Supports PDF and TXT files</p>
          </div>

          {file && (
            <div className="file-selected">
              <span>📎 {file.name}</span>
              <button className="file-remove" onClick={() => setFile(null)}>×</button>
            </div>
          )}
        </div>
      )}

      <button
        className="submit-btn"
        onClick={handleSubmit}
        disabled={!canSubmit || loading}
        id="submit-btn"
      >
        {loading ? '⏳ Analyzing...' : '🚀 Analyze Syllabus'}
      </button>
    </div>
  )
}
