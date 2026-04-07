# Quick Start Guide

## 5-Minute Setup

### Step 1: Clone and Setup (2 min)

```bash
# Navigate to project
cd "ai conversational"

# Create virtual environment
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure (1 min)

```bash
# Copy example config
cp .env.example .env

# Edit .env with your API key
# Windows (PowerShell):
notepad .env
# macOS/Linux:
nano .env
```

Add your OpenAI key:
```
OPENAI_API_KEY=sk-xxxxxxxxxxxxx
```

### Step 3: Run Server (1 min)

```bash
# Start the FastAPI server
python -m uvicorn src.api.main:app --reload
```

Visit: http://localhost:8000/docs

### Step 4: Test (1 min)

#### Option A: Using the Interactive API Docs
1. Go to http://localhost:8000/docs
2. Click "Try it out" on any endpoint
3. Fill in parameters and execute

#### Option B: Using cURL

```bash
# Test Q&A
curl -X POST "http://localhost:8000/qa" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is this system about?",
    "context": "This is a conversation intelligence system for analyzing audio conversations."
  }'

# Test summarization
curl -X POST "http://localhost:8000/summarize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Customer called about product issues. They mentioned slow performance. We discussed solutions and scheduled a follow-up.",
    "type": "bullet_points"
  }'

# Test health
curl http://localhost:8000/health
```

## Common Workflows

### Workflow 1: Transcribe and Analyze

```bash
# 1. Transcribe audio
curl -X POST "http://localhost:8000/transcribe" \
  -H "Content-Type: application/json" \
  -d '{
    "audio_path": "data/meeting.wav"
  }'

# 2. Process conversation
curl -X POST "http://localhost:8000/process-conversation" \
  -H "Content-Type: application/json" \
  -d '{
    "audio_path": "data/meeting.wav"
  }'

# 3. Ask questions
curl -X POST "http://localhost:8000/qa" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What action items were assigned?"
  }'
```

### Workflow 2: Comprehensive Analysis

```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your conversation text here...",
    "include_summary": true,
    "include_sentiment": true,
    "include_action_items": true,
    "include_themes": true,
    "include_risks": true
  }'
```

### Workflow 3: Python Script

```python
from pathlib import Path
from src.analysis.qa import get_qa_engine
from src.analysis.summarizer import get_summarizer

# Get components
qa_engine = get_qa_engine()
summarizer = get_summarizer()

conversation = "Your conversation text..."

# Ask a question
answer = qa_engine.answer_question("What were the key points?")
print(answer["answer"])

# Generate summary
summary = summarizer.summarize_full(conversation)
print(summary["summary"])
```

## API Endpoints Cheat Sheet

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | Check system status |
| POST | `/transcribe` | Audio → Text |
| POST | `/process-conversation` | Full pipeline |
| POST | `/retrieve` | Semantic search |
| POST | `/summarize` | Generate summary |
| POST | `/sentiment` | Analyze sentiment |
| POST | `/action-items` | Extract tasks |
| POST | `/qa` | Answer questions |
| POST | `/analyze` | Full analysis |

## Parameter Guide

### Summarization Type
- `full` - Complete summary
- `bullet_points` - Key points
- `contextual` - Business summary

### Sentiment Types
- `overall` - Overall tone
- `by_speaker` - Per participant
- `by_topic` - By topic
- `issues` - Problems found
- `satisfaction` - Satisfaction level

### Action Item Types
- `full` - All items
- `decisions_only` - Decisions
- `deadlines_only` - Dates/deadlines
- `risks_only` - Risks/blockers

## Troubleshooting

### Port 8000 already in use?
```bash
# Use different port
python -m uvicorn src.api.main:app --port 8001
```

### Module not found?
```bash
# Ensure you're in venv and project root
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### API key error?
```bash
# Check .env file exists and has key
cat .env | grep OPENAI_API_KEY

# Or set directly (temporary)
export OPENAI_API_KEY="sk-xxxxx"
```

### Import errors?
```bash
# Add project to path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Then run
python -m uvicorn src.api.main:app --reload
```

## Next Steps

1. **Add your audio file**: Place audio in `data/` folder
2. **Customize config**: Edit `config.py` for your needs
3. **Explore API docs**: Visit http://localhost:8000/docs
4. **Run examples**: `python examples/demo.py`
5. **Build integrations**: Use REST API or Python library

## Performance Tips

- Use `tiny` or `base` Whisper for real-time applications
- Adjust `CHUNK_SIZE` based on your domain (smaller = faster, larger = more context)
- Set `SIMILARITY_THRESHOLD` higher if getting too many results
- Use `RETRIEVAL_TOP_K=3` for speed, `=10` for comprehensiveness

## Common Questions

**Q: How much does this cost to run?**
A: Costs depend on OpenAI API usage. Typical conversation: $0.01-0.05

**Q: Can I use it without API keys in testing?**
A: First 3 demos don't need API keys. Analysis requires OpenAI/Gemini.

**Q: How long does it take to process an audio?**
A: ~1-2 minutes for 30-min audio (base Whisper), varies by duration and model.

**Q: Can I run this locally without cloud APIs?**
A: Yes, use Llama 2, Mistral, or other local LLMs (replace LLM client).

**Q: Is it scalable for production?**
A: Yes, FastAPI supports async. Use horizontal scaling with load balancer.

---

**Ready to go!** 🚀

For more details, see README.md
