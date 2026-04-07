# System Architecture Documentation

## High-Level Architecture

```
┌─────────────────┐
│   Audio Input   │
└────────┬────────┘
         │
    ┌────▼────────────────────────┐
    │  Speech-to-Text (Whisper)    │
    │  ├─ Convert to text          │
    │  ├─ Extract timestamps       │
    │  └─ Multi-language support   │
    └────┬────────────────────────┘
         │
    ┌────▼────────────────────────┐
    │   Text Chunking             │
    │  ├─ By paragraphs           │
    │  ├─ By sentences            │
    │  ├─ Overlapping chunks      │
    │  └─ Preserve context        │
    └────┬────────────────────────┘
         │
    ┌────▼────────────────────────┐
    │  Embeddings Generation      │
    │  ├─ Sentence Transformers   │
    │  ├─ Vectorization           │
    │  └─ Batch processing        │
    └────┬────────────────────────┘
         │
    ┌────▼────────────────────────┐
    │   FAISS Vector Index        │
    │  ├─ Index storage           │
    │  ├─ Metadata tracking       │
    │  └─ Fast retrieval          │
    └────┬────────────────────────┘
         │
    ┌────▼────────────────────────┐
    │   RAG Pipeline              │
    │  ├─ Semantic search         │
    │  ├─ Relevance scoring       │
    │  ├─ MMR reranking          │
    │  └─ Context composition     │
    └────┬────────────────────────┘
         │
    ┌────▼────────────────────────┐
    │   LLM Processing            │
    │  ├─ Query understanding     │
    │  ├─ Context grounding       │
    │  └─ Response generation     │
    └────┬────────────────────────┘
         │
    ┌────▼────────────────────────┐
    │   Analysis Engine           │
    │  ├─ Summarization           │
    │  ├─ Sentiment analysis      │
    │  ├─ Action extraction       │
    │  └─ Q&A answering          │
    └────┬────────────────────────┘
         │
    ┌────▼────────────────────────┐
    │   Output/Response           │
    │  ├─ Insights               │
    │  ├─ Structured data        │
    │  └─ Confidence scores      │
    └─────────────────────────────┘
```

## Component Architecture

### 1. Core Module (`src/core/`)

#### `transcriber.py`
- **Purpose**: Audio-to-text conversion
- **Key Classes**: `AudioTranscriber`
- **Dependencies**: OpenAI Whisper
- **Methods**:
  - `transcribe()` - Basic transcription
  - `transcribe_async()` - Async wrapper
  - `transcribe_with_timestamps()` - Segment timestamps

#### `chunker.py`
- **Purpose**: Text segmentation for embedding
- **Key Classes**: `TextChunker`
- **Chunking Strategies**:
  - Character-based (with smart boundaries)
  - Sentence-based (groups sentences)
  - Paragraph-based (groups paragraphs)
- **Features**: Overlapping windows, minimum size filtering

#### `embedder.py`
- **Purpose**: Text vectorization
- **Key Classes**: `EmbeddingsGenerator`
- **Model**: Sentence-Transformers (all-MiniLM-L6-v2 by default)
- **Methods**:
  - `encode()` - Generate embeddings
  - `embed_chunks()` - Batch embedding
  - `similarity()` - Cosine similarity calculation

### 2. RAG Module (`src/rag/`)

#### `vector_store.py`
- **Purpose**: Vector database management
- **Key Classes**: `FAISSVectorStore`
- **Backend**: FAISS (Facebook AI Similarity Search)
- **Features**:
  - IndexFlatL2 (L2 distance)
  - Metadata tracking
  - Persistence to disk
  - Search operations
- **Methods**:
  - `add_embeddings()` - Index new vectors
  - `search()` - Find similar vectors
  - `delete_by_id()` - Remove documents
  - `clear_index()` - Full reset

#### `retriever.py`
- **Purpose**: Retrieval-Augmented Generation orchestration
- **Key Classes**: `RAGRetriever`
- **Features**:
  - Query embedding
  - Vector similarity search
  - Threshold-based filtering
  - MMR reranking option
  - Context formatting for LLM
- **Methods**:
  - `retrieve()` - Get relevant chunks
  - `retrieve_batch()` - Multiple queries
  - `format_context()` - LLM-ready formatting
  - `rerank_results()` - Reranking strategies

### 3. Analysis Module (`src/analysis/`)

#### `llm_client.py`
- **Purpose**: LLM API integration
- **Key Classes**: `LLMClient`
- **Providers**: OpenAI (default), Gemini
- **Methods**:
  - `call_llm()` - Unified LLM interface
  - `_call_openai()` - Provider-specific
  - `_call_gemini()` - Provider-specific

#### `summarizer.py`
- **Purpose**: Conversation summarization
- **Key Classes**: `ConversationSummarizer`
- **Summary Types**:
  - Full comprehensive summary
  - Bullet-point extraction
  - Contextual business summary
  - Theme identification
- **Methods**:
  - `summarize_full()`
  - `summarize_bullet_points()`
  - `summarize_with_context()`
  - `extract_themes()`

#### `sentiment.py`
- **Purpose**: Emotional analysis
- **Key Classes**: `SentimentAnalyzer`
- **Analysis Types**:
  - Overall sentiment (Pos/Neutral/Neg)
  - Per-speaker sentiment
  - Topic-based sentiment
  - Issue detection
  - Satisfaction scoring
- **Methods**:
  - `analyze_overall()`
  - `analyze_by_speaker()`
  - `analyze_by_topic()`
  - `detect_issues()`
  - `detect_satisfaction()`

#### `action_items.py`
- **Purpose**: Task and decision extraction
- **Key Classes**: `ActionItemExtractor`
- **Extraction Types**:
  - Action items with ownership
  - Decision records
  - Deadline identification
  - Risk and blocker detection
  - Action plan generation
- **Methods**:
  - `extract_action_items()`
  - `extract_decisions()`
  - `extract_deadlines()`
  - `extract_risks_and_blockers()`
  - `generate_action_plan()`

#### `qa.py`
- **Purpose**: Question answering with RAG
- **Key Classes**: `ConversationQAEngine`
- **QA Types**:
  - Single question with context
  - Conversational Q&A with history
  - Search and explain
  - Multi-question batch
  - Confidence-weighted answers
- **Methods**:
  - `answer_question()`
  - `ask_follow_up()`
  - `search_and_explain()`
  - `multi_question_qa()`
  - `answer_with_confidence()`

### 4. API Module (`src/api/`)

#### `main.py`
- **Purpose**: FastAPI application
- **Key Features**:
  - RESTful endpoints
  - Async request handling
  - CORS middleware
  - Error handling
  - Health checks
- **Endpoint Groups**:
  - Health checks
  - Transcription
  - Processing
  - Retrieval
  - Analysis (summarization, sentiment, actions, Q&A)
  - Vector store management

#### `models.py`
- **Purpose**: Request/response schemas
- **Pydantic Models**:
  - Request models (validation)
  - Response models (serialization)
  - Error models

## Data Flow

### Processing Pipeline

```
Input Audio File
    ↓
Whisper Transcription (model_name, language)
    ↓ (Text)
Text Chunking (method: char/sentence/paragraph)
    ↓ (Chunks)
Batch Embedding Generation (model, dimension)
    ↓ (Embeddings)
FAISS Indexing (store, metadata)
    ↓ (Index)
Vector Store Ready ✓
```

### RAG Query Pipeline

```
User Query
    ↓
Query Embedding (same model)
    ↓
FAISS Similarity Search
    ↓ (Top-K results)
Result Filtering (threshold, similarity)
    ↓ (Filtered chunks)
Context Formatting (for LLM)
    ↓ (Prompt)
LLM Processing (with retrieval-augmented context)
    ↓ (Response)
Result (grounded in conversation)
```

## Configuration System

```
config.py
├─ Settings (Pydantic)
│  ├─ Application config
│  ├─ API config
│  ├─ Model config
│  ├─ Processing config
│  ├─ LLM parameters
│  ├─ Performance settings
│  └─ Timeout settings
└─ Environment variables (.env)
   ├─ API keys
   ├─ Model selections
   ├─ Path settings
   └─ Feature flags
```

## Singleton Pattern

All major components use singleton pattern for resource efficiency:

```python
# Get or create (first call creates, subsequent calls reuse)
transcriber = get_transcriber()
chunker = get_chunker()
embeddings_gen = get_embeddings_generator()
vector_store = get_vector_store()
retriever = get_retriever()
summarizer = get_summarizer()
analyzer = get_sentiment_analyzer()
extractor = get_action_item_extractor()
qa_engine = get_qa_engine()
```

## Performance Considerations

### Optimization Areas

1. **Model Loading**
   - Models loaded once and cached
   - Lazy loading on first use
   - Preloading possible in initialization

2. **Batch Processing**
   - Embeddings processed in batches
   - Configurable batch size
   - Async support for I/O operations

3. **Vector Search**
   - FAISS provides O(1) search complexity
   - Index persisted to disk
   - Incremental updates supported

4. **Context Window**
   - Max context size configurable
   - Smart context selection
   - MMR reranking for relevance + diversity

5. **Caching**
   - Can be enabled for repeated queries
   - TTL configuration
   - Optional Redis integration ready

## Scalability Strategy

### Horizontal Scaling

```
                    ┌─────────────┐
                    │ Load Balancer
                    └────┬────────┘
                         │
        ┌────────────────┼─────────────────┐
        │                │                 │
    ┌───▼──────┐    ┌───▼──────┐    ┌───▼──────┐
    │FastAPI 1 │    │FastAPI 2 │    │FastAPI 3 │
    └───┬──────┘    └───┬──────┘    └───┬──────┘
        │                │                 │
        └────────────────┼─────────────────┘
                         │
            ┌────────────▼──────────────┐
            │ Shared Vector Store (S3) │
            │ Shared Cache (Redis)     │
            │ Shared Models (NFS)      │
            └──────────────────────────┘
```

### Vertical Scaling

- Increase worker threads (MAX_WORKERS)
- Larger batch sizes for embeddings
- GPU support for FAISS (FAISS_ENABLE_GPU)
- Model size optimization (smaller Whisper)

## Error Handling Strategy

```python
Try:
    Process Request
        │
        ├─ Validation Error → 400 Bad Request
        ├─ File Not Found → 404 Not Found
        ├─ Processing Error → 500 Internal Server Error
        └─ Success → 200 OK with Result
        
Catch:
    Log Error with Context
    Return Formatted Error Response
    Maintain System State
```

## Security Considerations

1. **API Key Management**
   - Environment variables only
   - Never commit keys
   - Validation at startup

2. **Input Validation**
   - Pydantic schemas
   - Type checking
   - Size limits

3. **Error Messages**
   - Avoid exposing internals
   - Generic error messages
   - Detailed logging

4. **Access Control**
   - CORS configured
   - Rate limiting (ready)
   - Authentication (extensible)

## Monitoring & Logging

```
Logging Levels:
- DEBUG: Detailed flow information
- INFO: Important milestones
- WARNING: Recoverable issues
- ERROR: Failures and exceptions

Metrics to Track:
- Request latency
- Vector index size
- Cache hit rate
- Error frequency
- API usage
```

## Extension Points

### Adding New Analysis

1. Create new class in `src/analysis/`
2. Inherit from base pattern
3. Implement analysis method
4. Add to FastAPI in `src/api/main.py`
5. Add Pydantic models in `src/api/models.py`

### Adding New LLM Provider

1. Update `config.py` with provider
2. Implement in `llm_client.py`
3. Add provider-specific method
4. Test with new provider

### Custom Embeddings Model

1. Update `config.py` EMBEDDING_MODEL
2. Update EMBEDDING_DIMENSION
3. Regenerate vector index

## Deployment Considerations

### Docker

```dockerfile
FROM python:3.10
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0"]
```

### Environment Variables (Production)

```
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-xxxxx
DEBUG=False
ENVIRONMENT=production
WHISPER_MODEL=large  # Trade speed for accuracy
MAX_WORKERS=8
ENABLE_ASYNC_PROCESSING=True
CACHE_TTL=7200
```

### Performance Tuning (Production)

```python
# config.py
CHUNK_SIZE=1000          # Larger chunks = fewer vectors
RETRIEVAL_TOP_K=10       # Get more context
SIMILARITY_THRESHOLD=0.6  # Higher threshold
BATCH_SIZE=64            # Larger batches
MAX_TOKENS=3000          # More comprehensive answers
```

---

**Architecture Version**: 1.0.0  
**Last Updated**: April 2026
