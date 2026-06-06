# 🚀 AI Conversation Intelligence System

A full-stack application that intelligently analyzes conversations using **Speech Recognition**, **Semantic Search (RAG)**, and **LLM-powered Analysis** with a modern React frontend.

## 🎯 Key Features

### 1. **Integrated Conversation Intelligence Dashboard**
- **All-in-One Dashboard**: Summarize, analyze sentiment, extract action items, and ask questions directly from the transcription results page.
- **State Persistence**: Your transcribed conversation and analysis reports are saved to local storage so they remain on your screen even if you switch tabs or reload the browser.
- **Collapsible Layout**: Expand or collapse long transcripts easily with a single toggle.
- **Robust Downloads**: Download full conversations as plain text via standard Blob buffers, avoiding length truncation bugs.

### 2. **Speech-to-Text Transcription**
- Convert audio files to text using OpenAI Whisper
- Support for multiple languages
- Segment-level timing information
- Handles various audio formats (mp3, wav, m4a, flac)

### 3. **Semantic Search (RAG)**
- Store conversation embeddings in FAISS vector database
- Retrieve relevant chunks based on semantic similarity
- Contextual Q&A over conversations
- MMR (Maximal Marginal Relevance) reranking for diversity

### 3. **Intelligent Summarization**
- Full conversation summaries
- Bullet-point key discussion points
- Contextual business-focused summaries
- Theme extraction

### 4. **Sentiment Analysis**
- Overall conversation sentiment (Positive/Neutral/Negative)
- Per-speaker sentiment analysis
- Topic-based sentiment breakdown
- Issue and complaint detection
- Satisfaction level analysis

### 5. **Action Item Extraction**
- Identify tasks and commitments
- Extract deadlines and dates
- Detect decisions made
- Identify risks and blockers
- Generate comprehensive action plans

### 6. **Conversational Q&A**
- Natural language questions about conversations
- Confidence-weighted answers
- Multi-question batch processing
- Search and explain functionality

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | FastAPI + Uvicorn |
| Speech Recognition | OpenAI Whisper |
| LLM | OpenAI (GPT-4 / GPT-3.5) or Gemini |
| Vector Database | FAISS |
| Embeddings | Sentence-Transformers |
| Language | Python 3.10+ |

## 📋 Prerequisites

- Python 3.10 or higher
- OpenAI API key (for GPT models)
- Or Gemini API key (for Gemini models)
- 2GB+ RAM for embedding models
- FFmpeg (for audio processing)

## 🚀 Installation

### 1. Clone and Navigate

```bash
cd "ai conversational"
```

### 2. Create Virtual Environment

```bash
# Using venv
python -m venv venv

# Activate
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables

Create a `.env` file in the project root:

```env
# LLM Configuration
LLM_PROVIDER=openai  # or gemini or groq
OPENAI_API_KEY=sk-xxxxxxxxxxxxx
# GEMINI_API_KEY=xxxxxxxxxxxxx
# GROQ_API_KEY=xxxxxxxxxxxxx
# GROQ_MODEL=llama-3.1-8b-instant

# Application Settings
DEBUG=True
ENVIRONMENT=development
LOG_LEVEL=INFO

# Whisper Model
WHISPER_MODEL=base  # tiny, base, small, medium, large
```

### 5. Install FFmpeg (if needed for audio processing)

```bash
# Windows (using conda or scoop)
scoop install ffmpeg

# macOS
brew install ffmpeg

# Linux (Ubuntu/Debian)
sudo apt-get install ffmpeg
```

## 📖 Usage

### Option 1: Using the FastAPI Server

#### Start the Server

```bash
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

#### API Endpoints

Access the interactive API documentation at: `http://localhost:8000/docs`

**Key Endpoints:**

- `GET /` - API information
- `GET /health` - System health check
- `POST /transcribe` - Transcribe audio
- `POST /process-conversation` - End-to-end processing
- `POST /retrieve` - Retrieve relevant context
- `POST /summarize` - Generate summary
- `POST /sentiment` - Analyze sentiment
- `POST /action-items` - Extract action items
- `POST /qa` - Answer questions
- `POST /analyze` - Comprehensive analysis
- `GET /vector-store/stats` - Vector store statistics

### Option 2: Using Python Directly

```python
from src.core.transcriber import get_transcriber
from src.core.chunker import get_chunker
from src.core.embedder import get_embeddings_generator
from src.rag.vector_store import get_vector_store
from src.rag.retriever import get_retriever
from src.analysis.summarizer import get_summarizer
from src.analysis.sentiment import get_sentiment_analyzer
from src.analysis.action_items import get_action_item_extractor
from src.analysis.qa import get_qa_engine
from pathlib import Path

# Step 1: Transcribe
transcriber = get_transcriber()
result = transcriber.transcribe(Path("path/to/audio.wav"))
text = result["text"]

# Step 2: Summarize
summarizer = get_summarizer()
summary = summarizer.summarize_full(text)
print(summary["summary"])

# Step 3: Sentiment Analysis
analyzer = get_sentiment_analyzer()
sentiment = analyzer.analyze_overall(text)
print(sentiment["analysis"])

# Step 4: Action Items
extractor = get_action_item_extractor()
actions = extractor.extract_action_items(text)
print(actions["action_items"])

# Step 5: Q&A
qa_engine = get_qa_engine()
answer = qa_engine.answer_question("What are the key points?")
print(answer["answer"])
```

### Option 3: Run Example Demo

```bash
# Set your API key first
export OPENAI_API_KEY="sk-xxxxxxxxxxxxx"

# Run demo
python examples/demo.py
```

## 📊 API Examples

### Example 1: Transcribe Audio

```bash
curl -X POST "http://localhost:8000/transcribe" \
  -H "Content-Type: application/json" \
  -d '{
    "audio_path": "data/conversation.wav",
    "language": "en"
  }'
```

### Example 2: Process Conversation

```bash
curl -X POST "http://localhost:8000/process-conversation" \
  -H "Content-Type: application/json" \
  -d '{
    "audio_path": "data/conversation.wav"
  }'
```

### Example 3: Retrieve Context

```bash
curl -X POST "http://localhost:8000/retrieve" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the action items?",
    "top_k": 5,
    "threshold": 0.3
  }'
```

### Example 4: Summarize

```bash
curl -X POST "http://localhost:8000/summarize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Lorem ipsum conversation text...",
    "type": "bullet_points"
  }'
```

### Example 5: Question Answering

```bash
curl -X POST "http://localhost:8000/qa" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What did the client say about pricing?"
  }'
```

### Example 6: Comprehensive Analysis

```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Lorem ipsum conversation text...",
    "include_summary": true,
    "include_sentiment": true,
    "include_action_items": true,
    "include_themes": true,
    "include_risks": true
  }'
```

## 🏗️ Project Structure

```
ai_conversational/
├── PROJECT_BRIEF.md           # Problem statement
├── README.md                  # This file
├── requirements.txt           # Dependencies
├── config.py                  # Configuration
├── src/
│   ├── __init__.py
│   ├── core/                  # Core functionality
│   │   ├── transcriber.py     # Audio → Text
│   │   ├── chunker.py         # Text → Chunks
│   │   └── embedder.py        # Text → Embeddings
│   ├── rag/                   # RAG Pipeline
│   │   ├── vector_store.py    # FAISS management
│   │   └── retriever.py       # Context retrieval
│   ├── analysis/              # Analysis modules
│   │   ├── llm_client.py      # LLM integration
│   │   ├── summarizer.py      # Summarization
│   │   ├── sentiment.py       # Sentiment analysis
│   │   ├── action_items.py    # Action extraction
│   │   └── qa.py             # Question answering
│   ├── api/                   # FastAPI server
│   │   ├── main.py           # API endpoints
│   │   └── models.py         # Request/response models
│   └── utils.py              # Utility functions
├── data/                      # Sample data
├── models/                    # Downloaded models & indices
├── examples/
│   └── demo.py               # Example usage
└── logs/                     # Application logs
```

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Text chunking
CHUNK_SIZE = 500              # Characters per chunk
CHUNK_OVERLAP = 100           # Overlap between chunks

# Embeddings
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384

# RAG
RETRIEVAL_TOP_K = 5           # Top-k results to retrieve
SIMILARITY_THRESHOLD = 0.5    # Minimum similarity score

# LLM
MAX_TOKENS = 2000
TEMPERATURE = 0.7
TOP_P = 0.9
```

## 📚 Supported Analyses

### Summarization Types
- `full` - Comprehensive summary
- `bullet_points` - Key discussion points
- `contextual` - Business-focused summary

### Sentiment Analysis Types
- `overall` - Overall sentiment
- `by_speaker` - Per-speaker sentiment
- `by_topic` - Topic-based sentiment
- `issues` - Issue detection
- `satisfaction` - Satisfaction analysis

### Action Items Types
- `full` - Complete action items
- `decisions_only` - Decisions only
- `deadlines_only` - Deadlines only
- `risks_only` - Risks and blockers

## 🚨 Error Handling

The system includes comprehensive error handling:

```python
{
    "detail": "Error message",
    "error_code": "ERROR_CODE",
    "timestamp": "2026-04-07T10:30:00"
}
```

## 📊 Performance Tips

1. **Chunking**: Use appropriate chunk size for your domain
2. **Batch Processing**: Process multiple items at once when possible
3. **Caching**: Enable caching for frequently accessed queries
4. **Model Selection**: Use smaller Whisper models for faster processing
5. **Vector DB**: Index is automatically cached for fast retrieval

## 🧪 Testing

Run tests with:

```bash
pytest tests/ -v
```

## 🔐 Security

- Store API keys in environment variables (never commit)
- Use `.env` file for local development
- Validate all inputs before processing
- Sanitize outputs before returning

## 📝 Logging

Logs are saved to `logs/` directory. Configure in `config.py`:

```python
LOG_LEVEL = "INFO"
LOG_FORMAT = "json"  # or "standard"
```

## 🤝 Contributing

To extend the system:

1. Add new analysis type to `src/analysis/`
2. Update API models in `src/api/models.py`
3. Add endpoint in `src/api/main.py`
4. Add tests

## 📄 License

This project is provided as-is for educational and commercial use.

## 🆘 Troubleshooting

### Issue: "OPENAI_API_KEY not set"
**Solution**: Set environment variable
```bash
export OPENAI_API_KEY="sk-xxxxx"
```

### Issue: "Audio format not supported"
**Solution**: Convert using FFmpeg
```bash
ffmpeg -i input.m4a -acodec pcm_s16le -ar 16000 output.wav
```

### Issue: "FAISS index empty"
**Solution**: Process conversation first using `/process-conversation` endpoint

### Issue: Slow retrieval
**Solution**: Reduce `RETRIEVAL_TOP_K` or increase `SIMILARITY_THRESHOLD`

## 📚 Further Reading

- [Whisper Documentation](https://github.com/openai/whisper)
- [FAISS Documentation](https://faiss.ai/)
- [Sentence Transformers](https://www.sbert.net/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401)

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review example usage in `examples/demo.py`
3. Check API documentation at `/docs`

---

**Version**: 1.0.0  
**Last Updated**: April 2026  
**Status**: Production Ready
