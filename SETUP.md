# 🚀 AI Conversation Intelligence System - Setup & Run Guide

## 📋 Project Overview

This is a **full-stack AI Conversation Intelligence System** combining:
- **Backend**: FastAPI with OpenAI Whisper, Sentence-Transformers, FAISS, and LLM analysis
- **Frontend**: React with Vite and Tailwind CSS
- **Features**: Transcription, Summarization, Sentiment Analysis, Action Item Extraction, Q&A, and RAG

---

## ⚡ Quick Start (for running existing setup)

```bash
# Terminal 1 - Backend (if not already running)
cd "path/to/ai conversational"
venv\Scripts\python.exe src/api/main.py

# Terminal 2 - Frontend
cd "path/to/ai conversational/frontend"
npm install
npm run dev
```

Then open: **http://localhost:3000**

---

## 📦 Prerequisites

- **Python 3.10+** (with pip)
- **Node.js 16+** with npm
- **OpenAI API Key** (for LLM features)
- **4GB+ RAM** (for models)
- **Internet connection** (for downloading models on first run)

---

## 🔧 Complete Setup Guide

### Step 1: Backend Setup

#### 1.1 Navigate to Project Root
```bash
cd "path/to/ai conversational"
```

#### 1.2 Create & Activate Python Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate (on Windows)
venv\Scripts\activate

# Activate (on macOS/Linux)
source venv/bin/activate
```

#### 1.3 Install Dependencies
```bash
pip install -r requirements.txt
```

#### 1.4 Configure Environment Variables
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

Alternatively, set the environment variable in your terminal:
```bash
# Windows
set OPENAI_API_KEY=your_key

# macOS/Linux
export OPENAI_API_KEY=your_key
```

#### 1.5 Start Backend Server
```bash
# From project root with venv activated
python src/api/main.py
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

✅ **Backend is ready** when you see "Application startup complete"

---

### Step 2: Frontend Setup

#### 2.1 Open New Terminal & Navigate to Frontend
```bash
cd "path/to/ai conversational/frontend"
```

#### 2.2 Install Dependencies
```bash
npm install
```

This installs:
- React 18.2.0
- React Router
- Axios
- Tailwind CSS
- Vite
- React Icons

#### 2.3 Start Development Server
```bash
npm run dev
```

Expected output:
```
  VITE v4.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
  ➜  Press q to quit
```

✅ **Frontend is ready** when you see the local URL

---

### Step 3: Access the Application

Open your browser and go to: **http://localhost:3000**

You should see:
- Navigation sidebar with 6 menu items
- Dashboard with system stats
- Full-featured conversation intelligence interface

---

## 🎯 Features Available

| Feature | URL | Description |
|---------|-----|-------------|
| **Dashboard** | http://localhost:3000/ | System stats & health check |
| **Summarizer** | http://localhost:3000/summarizer | Generate conversation summaries |
| **Sentiment Analysis** | http://localhost:3000/sentiment | Analyze emotional tone |
| **Action Items** | http://localhost:3000/actions | Extract tasks & decisions |
| **Q&A** | http://localhost:3000/qa | Ask questions about conversations |
| **Settings** | http://localhost:3000/settings | Vector store management |

---

## 🔌 API Endpoints (Backend)

Available at `http://localhost:8000`:

### Core Functions
- `POST /transcribe` - Speech to text (Whisper)
- `POST /process` - Full pipeline processing
- `POST /retrieve` - Semantic search
- `POST /summarize` - Generate summaries
- `POST /sentiment` - Sentiment analysis
- `POST /action-items` - Extract action items
- `POST /qa` - Question answering
- `POST /analyze` - Comprehensive analysis

### Vector Store
- `GET /vector-store/stats` - Storage statistics
- `DELETE /vector-store/clear` - Clear all data
- `GET /vector-store/entries` - List entries
- `POST /vector-store/add` - Add vectors

### System
- `GET /health` - Health check
- `GET /docs` - API documentation (Swagger UI)

**Interactive API Docs**: http://localhost:8000/docs

---

## 📁 Project Structure

```
ai conversational/
├── src/                          # Backend source code
│   ├── api/
│   │   └── main.py              # FastAPI server with 13 endpoints
│   ├── core/
│   │   ├── transcriber.py       # Whisper integration
│   │   ├── chunker.py           # Text chunking strategies
│   │   └── embedder.py          # Sentence-Transformers
│   ├── rag/
│   │   ├── vector_store.py      # FAISS operations
│   │   └── retriever.py         # Semantic search & reranking
│   └── analysis/
│       ├── llm_client.py        # OpenAI integration
│       ├── summarizer.py        # 4 summarization types
│       ├── sentiment.py         # 5 sentiment analysis types
│       ├── action_items.py      # Task extraction
│       └── qa.py                # Question answering
│
├── frontend/                     # React frontend
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx    # System overview
│   │   │   ├── Summarizer.jsx   # Summarization UI
│   │   │   ├── SentimentAnalyzer.jsx
│   │   │   ├── ActionItems.jsx
│   │   │   ├── QA.jsx           # Chat interface
│   │   │   └── Settings.jsx     # Configuration
│   │   ├── components/
│   │   │   ├── Header.jsx       # Top navigation
│   │   │   ├── Sidebar.jsx      # Left navigation
│   │   │   └── StatusCard.jsx   # Reusable card
│   │   ├── services/
│   │   │   └── api.js           # API client service
│   │   ├── App.jsx              # Main app component
│   │   ├── main.jsx             # React entry point
│   │   └── index.css            # Global styles
│   ├── vite.config.js           # Vite configuration
│   ├── tailwind.config.js       # Tailwind theme
│   └── package.json             # Dependencies
│
├── requirements.txt             # Python dependencies
├── .env                        # Environment variables
└── README.md                   # Documentation
```

---

## 🛠️ Development

### Backend Development
```bash
# Activate virtual environment
venv\Scripts\activate

# Run with auto-reload
python -m uvicorn src.api.main:app --reload

# Run specific file
python src/api/main.py
```

### Frontend Development
```bash
# Install new packages
npm install package-name

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## 🔍 Environment Variables

```env
# Required
OPENAI_API_KEY=sk-...

# Optional (defaults provided)
EMBEDDING_MODEL=all-MiniLM-L6-v2
CHUNK_SIZE=512
CHUNK_OVERLAP=50
LLM_MODEL=gpt-3.5-turbo
TEMPERATURE=0.7
```

---

## ⚠️ Troubleshooting

### Backend Issues

**"ModuleNotFoundError: No module named..."**
```bash
# Activate virtual environment and reinstall
venv\Scripts\activate
pip install -r requirements.txt
```

**"OPENAI_API_KEY not found"**
- Add API key to `.env` file
- Or set environment variable: `set OPENAI_API_KEY=your_key`

**Models taking too long to load**
- First run downloads models (~500MB)
- Allows offline use after caching
- Check internet connection during first startup

**Port 8000 already in use**
```bash
# Linux/macOS: Find and kill process
lsof -ti:8000 | xargs kill -9

# Windows: Change port in main.py
# Change: uvicorn.run(app, host="0.0.0.0", port=8001)
```

### Frontend Issues

**"npm: command not found"**
- Install Node.js from https://nodejs.org/
- Restart terminal after installation

**"VITE can't resolve '@'"**
```bash
cd frontend
npm install
npm run dev
```

**Port 3000 already in use**
```bash
# Vite will auto-increment port (3001, 3002, etc.)
# Or manually specify: npm run dev -- --port 3001
```

**Backend API not responding**
- Check if backend is running on port 8000
- Verify in vite.config.js proxy settings
- Hard refresh browser (Ctrl+Shift+R)

### Common Issues During First Run

1. **Models downloading slowly** - This is normal for first run (~5 min)
2. **GPU memory error** - Use CPU-only mode (configured by default)
3. **API rate limiting** - Wait before making multiple requests with OpenAI API

---

## 📝 Usage Examples

### Using the Dashboard
1. Open http://localhost:3000
2. View system health and vector store stats
3. Quick-access buttons to all features

### Summarizing a Conversation
1. Go to Summarizer page
2. Paste conversation text
3. Choose summary type (Full, Bullet Points, Contextual)
4. Click "Summarize"
5. Copy or download results

### Analyzing Sentiment
1. Go to Sentiment Analysis page
2. Paste conversation text
3. Choose analysis type (Overall, By Speaker, By Topic, Issues, Satisfaction)
4. Click "Analyze Sentiment"

### Extracting Action Items
1. Go to Action Items page
2. Paste conversation text
3. Choose extraction type (All, Decisions, Deadlines, Risks)
4. Click "Extract Action Items"

### Asking Questions
1. Go to Q&A page
2. Optionally add conversation context
3. Type your question or click quick questions
4. Get AI-powered answers with source references

---

## 🚀 Production Deployment

### Backend Deployment
```bash
# Use production ASGI server (Gunicorn)
pip install gunicorn
gunicorn src.api.main:app -w 4 -b 0.0.0.0:8000

# Docker option
docker build -t ai-conversational-backend .
docker run -p 8000:8000 -e OPENAI_API_KEY=$OPENAI_API_KEY ai-conversational-backend
```

### Frontend Deployment
```bash
# Build production bundle
cd frontend
npm run build

# Deploy dist/ folder to static hosting (Vercel, Netlify, etc.)
# Or serve with Node.js
npm install -g serve
serve -s dist -l 3000
```

---

## 📊 Tech Stack Summary

**Backend**:
- FastAPI (REST API framework)
- OpenAI Whisper (speech recognition)
- Sentence-Transformers (embeddings)
- FAISS (vector database)
- OpenAI API (LLM)
- Pydantic (data validation)
- Uvicorn (ASGI server)

**Frontend**:
- React 18 (UI framework)
- Vite (bundler)
- Tailwind CSS (styling)
- React Router (navigation)
- Axios (HTTP client)
- React Icons (icons)

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review backend logs in terminal
3. Check browser console (F12) for frontend errors
4. Verify API at http://localhost:8000/docs

---

## 📄 License

This project is provided as-is for educational and development purposes.

---

**Happy building! 🎉**
