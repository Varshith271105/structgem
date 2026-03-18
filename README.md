# 🎓 StructGem — Smart Syllabus Topic Segregator

An AI-powered tool that parses academic syllabi and extracts structured topic hierarchies using LLM (Groq).

![Tech Stack](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react)
![Tech Stack](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![Tech Stack](https://img.shields.io/badge/Groq-LLM-orange)

## ✨ Features

- **Multi-format Input** — Paste text or upload PDF/TXT files
- **AI Topic Extraction** — Uses Groq LLM (Llama 3.3 70B) to identify topics, subtopics, and concepts
- **Smart Merging** — Deduplicates and merges results from multiple text chunks
- **Logical Ordering** — Arranges topics from basic → advanced
- **Interactive Tree View** — Collapsible topic hierarchy with concept tags
- **Raw JSON View** — Toggle between structured tree and raw JSON
- **Download JSON** — Export results as a JSON file
- **Full Logging** — Logs inputs, LLM prompts, and outputs

## 📁 Project Structure

```
structgem/
├── backend/
│   ├── main.py           # FastAPI app + endpoints
│   ├── parser.py         # PDF/TXT file parsing
│   ├── cleaner.py        # Text preprocessing
│   ├── chunker.py        # Token-based text chunking
│   ├── llm_engine.py     # Groq LLM integration
│   ├── merger.py         # Merge & deduplicate topics
│   ├── structurer.py     # Logical topic ordering
│   ├── logger_config.py  # Logging setup
│   └── requirements.txt
├── frontend/             # React + Vite
│   └── src/
│       ├── App.jsx
│       ├── components/
│       │   ├── InputPanel.jsx
│       │   ├── ResultsPanel.jsx
│       │   └── TopicTree.jsx
│       └── ...
└── README.md
```

## 🚀 Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- Free Groq API key from [console.groq.com](https://console.groq.com)

### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Set API key
set GROQ_API_KEY=your_api_key_here        # Windows CMD
# $env:GROQ_API_KEY="your_api_key_here"   # PowerShell
# export GROQ_API_KEY=your_api_key_here   # macOS/Linux

# Run server
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Then open [http://localhost:5173](http://localhost:5173)

## 📡 API Usage

### POST `/process`

Accepts either text or file upload via `multipart/form-data`.

**Text input:**
```bash
curl -X POST http://localhost:8000/process \
  -F "text=Unit 1: Data Structures - Arrays, Linked Lists, Stacks"
```

**File upload:**
```bash
curl -X POST http://localhost:8000/process \
  -F "file=@syllabus.pdf"
```

**Response:**
```json
{
  "topics": [
    {
      "name": "Data Structures",
      "subtopics": [
        {
          "name": "Linear Data Structures",
          "concepts": ["Arrays", "Linked Lists", "Stacks", "Queues"]
        }
      ]
    }
  ]
}
```

## 🧠 Example Output

Given a Computer Science syllabus, the tool produces:

```json
{
  "topics": [
    {
      "name": "Introduction to Programming",
      "subtopics": [
        {
          "name": "Programming Fundamentals",
          "concepts": ["Variables", "Data Types", "Operators", "Control Flow"]
        },
        {
          "name": "Functions and Modules",
          "concepts": ["Function Definition", "Parameters", "Return Values", "Modules"]
        }
      ]
    },
    {
      "name": "Data Structures",
      "subtopics": [
        {
          "name": "Linear Structures",
          "concepts": ["Arrays", "Linked Lists", "Stacks", "Queues"]
        },
        {
          "name": "Non-Linear Structures",
          "concepts": ["Binary Trees", "Graphs", "Heaps", "Hash Tables"]
        }
      ]
    },
    {
      "name": "Algorithms",
      "subtopics": [
        {
          "name": "Sorting Algorithms",
          "concepts": ["Bubble Sort", "Merge Sort", "Quick Sort"]
        },
        {
          "name": "Graph Algorithms",
          "concepts": ["BFS", "DFS", "Dijkstra's Algorithm"]
        }
      ]
    }
  ]
}
```

## 📝 Sample LLM Prompt

```
System: You are an expert academic curriculum analyst. Given a chunk of syllabus text,
extract and organize the content into a structured hierarchy of topics, subtopics, and concepts.

Rules:
1. Identify distinct TOPICS (broad subject areas).
2. Under each topic, list SUBTOPICS (specific areas within the topic).
3. Under each subtopic, list CONCEPTS (individual terms, theories, methods, or ideas).
4. Maintain a clean hierarchy — no duplicates within the same chunk.
5. If text is unclear, infer the best reasonable structure.

Respond with ONLY valid JSON in this exact format:
{
  "topics": [
    {
      "name": "Topic Name",
      "subtopics": [
        {
          "name": "Subtopic Name",
          "concepts": ["Concept 1", "Concept 2"]
        }
      ]
    }
  ]
}

User: Analyze the following syllabus text and extract topics, subtopics,
and concepts in the required JSON format.

--- SYLLABUS TEXT ---
[your syllabus content here]
--- END ---
```

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 19 + Vite 8 |
| Backend | Python + FastAPI |
| LLM | Groq API (Llama 3.3 70B Versatile) |
| PDF Parsing | pdfplumber |
| Tokenization | tiktoken |

## 📄 License

MIT
