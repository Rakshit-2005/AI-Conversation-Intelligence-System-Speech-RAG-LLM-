# 🚀 QUICK RUN GUIDE - AI Conversation Intelligence System

## 30-Second Setup (Windows)

```cmd
:: 1. One-time setup
setup.bat

:: 2. Terminal 1 - Backend
run-backend.bat

:: 3. Terminal 2 - Frontend  
run-frontend.bat

:: 4. Open browser
http://localhost:3000
```

## 30-Second Setup (macOS/Linux)

```bash
# 1. One-time setup
bash setup.sh

# 2. Terminal 1 - Backend
bash run-backend.sh

# 3. Terminal 2 - Frontend
bash run-frontend.sh

# 4. Open browser
http://localhost:3000
```

---

## URLs When Running

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3000 | Main React UI |
| Backend API | http://localhost:8000 | REST API |
| API Docs | http://localhost:8000/docs | Swagger UI |

---

## What You'll See

### Dashboard
- System health status ✓
- Vector store size ✓
- Quick action buttons ✓

### Summarizer
- Paste conversation → Generate summary
- 3 summary types
- Copy/download results

### Sentiment
- Analyze emotional tone
- 5 analysis types
- View sentiment breakdown

### Action Items
- Extract tasks & decisions
- Identify deadlines
- Spot risks & blockers

### Q&A
- Ask natural language questions
- Get AI answers with sources
- Chat-style interface

### Settings
- Vector store management
- API configuration
- Feature overview

---

## File Locations

```
Frontend: frontend/src/pages/
  - Dashboard.jsx
  - Summarizer.jsx
  - SentimentAnalyzer.jsx  
  - ActionItems.jsx
  - QA.jsx
  - Settings.jsx

Backend: src/api/
  - main.py (← Run this)

Config:
  - .env (← Add API key here)
```

---

## Common Commands

```bash
# Backend only (if already have venv)
venv\Scripts\activate  # Activate virtual env
python src/api/main.py  # Start backend

# Frontend only
cd frontend
npm install  # First time only
npm run dev  # Start dev server

# Production build
cd frontend
npm run build
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| "Port already in use" | Change port in src/api/main.py or wait a minute |
| "Module not found" | Run `pip install -r requirements.txt` |
| "npm command not found" | Install Node.js from nodejs.org |
| "API connection failed" | Make sure backend is running on port 8000 |
| "API key error" | Add OPENAI_API_KEY to .env file |

---

## Environment Setup

Create `.env` file with:
```env
OPENAI_API_KEY=sk-your_key_here
```

---

## Backend Endpoints

```
POST /summarize - Generate summary
POST /sentiment - Analyze sentiment  
POST /action-items - Extract tasks
POST /qa - Answer questions
POST /retrieve - Semantic search
GET /health - Health check
GET /vector-store/stats - Storage info
DELETE /vector-store/clear - Clear data
```

Full API docs at: http://localhost:8000/docs

---

## Tech Used

- **Frontend**: React + Vite + Tailwind CSS
- **Backend**: FastAPI + Python
- **Database**: FAISS vector store
- **LLM**: OpenAI API
- **Speech**: Whisper (offline, first run only)

---

## First Time?

1. ✅ Run setup script (5 min - downloads models)
2. ✅ Start backend (see "Application startup complete")
3. ✅ Start frontend (see "Local: http://localhost:3000")
4. ✅ Open http://localhost:3000
5. ✅ Try Dashboard → See system health
6. ✅ Try Summarizer → Paste text → Get summary

---

## Need Help?

- Full guide: `SETUP.md`
- Project info: `README.md`  
- Quick start: `QUICKSTART.md`
- API docs: http://localhost:8000/docs (when running)

---

## Pro Tips

💡 **First run takes 5-10 minutes** - Downloading AI models (~500MB)
💡 **Check terminal output** - Error messages show what's wrong
💡 **API costs** - Each request to OpenAI costs money, be mindful
💡 **Dev mode** - React hot-reloads on file changes (Frontend)
💡 **API hot-reload** - Backend auto-reloads on code changes

---

**Ready? Run: `setup.bat` (or `bash setup.sh`) then open http://localhost:3000** 🎉
