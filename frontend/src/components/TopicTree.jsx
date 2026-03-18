import { useState } from 'react'

function Chevron({ open }) {
  return (
    <svg className={`chevron ${open ? 'open' : ''}`} viewBox="0 0 20 20" fill="currentColor">
      <path d="M7.21 14.77a.75.75 0 01.02-1.06L11.168 10 7.23 6.29a.75.75 0 111.04-1.08l4.5 4.25a.75.75 0 010 1.08l-4.5 4.25a.75.75 0 01-1.06-.02z" />
    </svg>
  )
}

function SubtopicNode({ subtopic, index }) {
  const [open, setOpen] = useState(false)

  return (
    <div className="subtopic-item">
      <div className="subtopic-header" onClick={() => setOpen(!open)}>
        <Chevron open={open} />
        <span className="topic-badge subtopic">{index + 1}</span>
        <span className="subtopic-name">{subtopic.name}</span>
        <span className="topic-count">
          {subtopic.concepts?.length || 0} concepts
        </span>
      </div>
      {open && subtopic.concepts?.length > 0 && (
        <div className="concepts-list">
          {subtopic.concepts.map((concept, i) => (
            <span key={i} className="concept-tag">{concept}</span>
          ))}
        </div>
      )}
    </div>
  )
}

function TopicNode({ topic, index }) {
  const [open, setOpen] = useState(true)

  return (
    <div className="topic-node">
      <div className="topic-header" onClick={() => setOpen(!open)}>
        <Chevron open={open} />
        <span className="topic-badge topic">{index + 1}</span>
        <span className="topic-name">{topic.name}</span>
        <span className="topic-count">
          {topic.subtopics?.length || 0} subtopics
        </span>
      </div>
      {open && topic.subtopics?.length > 0 && (
        <div className="topic-children">
          {topic.subtopics.map((sub, i) => (
            <SubtopicNode key={i} subtopic={sub} index={i} />
          ))}
        </div>
      )}
    </div>
  )
}

export default function TopicTree({ topics }) {
  if (!topics || topics.length === 0) {
    return (
      <div className="empty-state">
        <p>No topics extracted. Try a different syllabus input.</p>
      </div>
    )
  }

  return (
    <div className="topic-tree">
      {topics.map((topic, i) => (
        <TopicNode key={i} topic={topic} index={i} />
      ))}
    </div>
  )
}
