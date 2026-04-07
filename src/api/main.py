"""
FastAPI main server
Endpoints for AI Conversation Intelligence System
"""

import logging
import time
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from config import settings
from src.api.models import (
    TranscriptionRequest,
    TranscriptionResponse,
    RetrievalRequest,
    RetrievalResponse,
    SummarizationRequest,
    SummarizationResponse,
    SentimentAnalysisRequest,
    SentimentAnalysisResponse,
    ActionItemsRequest,
    ActionItemsResponse,
    QARequest,
    QAResponse,
    ComprehensiveAnalysisRequest,
    ComprehensiveAnalysisResponse,
    HealthResponse,
)
from src.core.transcriber import get_transcriber
from src.core.chunker import get_chunker
from src.core.embedder import get_embeddings_generator
from src.rag.retriever import get_retriever
from src.rag.vector_store import get_vector_store
from src.analysis.summarizer import get_summarizer
from src.analysis.sentiment import get_sentiment_analyzer
from src.analysis.action_items import get_action_item_extractor
from src.analysis.qa import get_qa_engine

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered conversation intelligence system with speech recognition and RAG",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Health Check Endpoints
# ============================================================================

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Check system health"""
    try:
        vector_store = get_vector_store()
        embeddings_gen = get_embeddings_generator()

        return HealthResponse(
            status="healthy",
            version=settings.APP_VERSION,
            llm_provider=settings.LLM_PROVIDER,
            vector_store_ready=vector_store.index is not None,
            embeddings_ready=embeddings_gen.model is not None,
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Transcription Endpoints
# ============================================================================

@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe(request: TranscriptionRequest):
    """Transcribe audio file to text"""
    try:
        logger.info(f"Transcribing: {request.audio_path}")
        audio_path = Path(request.audio_path)

        transcriber = get_transcriber()
        result = transcriber.transcribe(
            audio_path,
            language=request.language,
        )

        return TranscriptionResponse(
            text=result["text"],
            language=result["language"],
            duration=result.get("duration", 0),
            segments=result.get("segments", []),
        )

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Transcription failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Processing Endpoints
# ============================================================================

@app.post("/process-conversation")
async def process_conversation(request: TranscriptionRequest):
    """End-to-end conversation processing"""
    try:
        start_time = time.time()
        logger.info(f"Processing conversation: {request.audio_path}")

        audio_path = Path(request.audio_path)

        # Step 1: Transcribe
        transcriber = get_transcriber()
        transcription_result = transcriber.transcribe(audio_path)
        text = transcription_result["text"]

        # Step 2: Chunk
        chunker = get_chunker()
        chunks = chunker.chunk(text, method="paragraphs")

        # Step 3: Generate embeddings
        embeddings_gen = get_embeddings_generator()
        chunks_with_embeddings = embeddings_gen.embed_chunks(chunks)

        # Step 4: Store in vector database
        vector_store = get_vector_store()
        embeddings_array = [
            chunk.pop("embedding") for chunk in chunks_with_embeddings
        ]
        vector_store.add_embeddings(embeddings_array, chunks_with_embeddings)

        processing_time = time.time() - start_time

        return {
            "id": audio_path.stem,
            "transcription": text[:500] + "..." if len(text) > 500 else text,
            "embedding_status": "success",
            "vector_index_size": vector_store.index.ntotal,
            "processing_time_seconds": processing_time,
            "chunks_created": len(chunks),
        }

    except Exception as e:
        logger.error(f"Conversation processing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# RAG Retrieval Endpoints
# ============================================================================

@app.post("/retrieve", response_model=RetrievalResponse)
async def retrieve(request: RetrievalRequest):
    """Retrieve relevant chunks for a query"""
    try:
        logger.info(f"Retrieving context for: {request.query[:100]}...")

        retriever = get_retriever()
        chunks = retriever.retrieve(
            request.query,
            top_k=request.top_k,
            threshold=request.threshold,
        )

        response_chunks = [
            {
                "id": chunk["id"],
                "text": chunk["text"],
                "similarity_score": chunk["similarity_score"],
                "distance": chunk.get("distance", 0),
            }
            for chunk in chunks
        ]

        return RetrievalResponse(
            query=request.query,
            chunks=response_chunks,
            total_retrieved=len(response_chunks),
        )

    except Exception as e:
        logger.error(f"Retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Analysis Endpoints
# ============================================================================

@app.post("/summarize", response_model=SummarizationResponse)
async def summarize(request: SummarizationRequest):
    """Generate conversation summary"""
    try:
        logger.info(f"Summarizing conversation: {request.type}")

        summarizer = get_summarizer()

        if request.type == "bullet_points":
            result = summarizer.summarize_bullet_points(request.text)
        elif request.type == "contextual":
            result = summarizer.summarize_with_context(request.text)
        else:  # full
            result = summarizer.summarize_full(request.text)

        return SummarizationResponse(
            summary=result.get("summary", result.get("bullet_points", "")),
            type=request.type,
        )

    except Exception as e:
        logger.error(f"Summarization failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/sentiment", response_model=SentimentAnalysisResponse)
async def analyze_sentiment(request: SentimentAnalysisRequest):
    """Analyze conversation sentiment"""
    try:
        logger.info(f"Analyzing sentiment: {request.analysis_type}")

        analyzer = get_sentiment_analyzer()

        if request.analysis_type == "by_speaker":
            result = analyzer.analyze_by_speaker(request.text)
        elif request.analysis_type == "by_topic":
            result = analyzer.analyze_by_topic(request.text)
        elif request.analysis_type == "issues":
            result = analyzer.detect_issues(request.text)
        elif request.analysis_type == "satisfaction":
            result = analyzer.detect_satisfaction(request.text)
        else:  # overall
            result = analyzer.analyze_overall(request.text)

        return SentimentAnalysisResponse(
            analysis=result.get("analysis", ""),
            type=request.analysis_type,
        )

    except Exception as e:
        logger.error(f"Sentiment analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/action-items", response_model=ActionItemsResponse)
async def extract_action_items(request: ActionItemsRequest):
    """Extract action items from conversation"""
    try:
        logger.info(f"Extracting action items: {request.extraction_type}")

        extractor = get_action_item_extractor()

        if request.extraction_type == "decisions_only":
            result = extractor.extract_decisions(request.text)
        elif request.extraction_type == "deadlines_only":
            result = extractor.extract_deadlines(request.text)
        elif request.extraction_type == "risks_only":
            result = extractor.extract_risks_and_blockers(request.text)
        else:  # full
            result = extractor.extract_action_items(request.text)

        return ActionItemsResponse(
            items=result.get("action_items", ""),
            type=request.extraction_type,
        )

    except Exception as e:
        logger.error(f"Action item extraction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Q&A Endpoints
# ============================================================================

@app.post("/qa", response_model=QAResponse)
async def ask_question(request: QARequest):
    """Answer a question about the conversation"""
    try:
        logger.info(f"Answering question: {request.question[:100]}...")

        qa_engine = get_qa_engine()
        result = qa_engine.answer_question(request.question, context=request.context)

        response_sources = [
            {
                "id": src["id"],
                "text": src["text"],
                "similarity_score": src["similarity_score"],
                "distance": src.get("distance", 0),
            }
            for src in result.get("sources", [])
        ]

        return QAResponse(
            question=result["question"],
            answer=result["answer"],
            confidence=0.8,
            sources=response_sources,
        )

    except Exception as e:
        logger.error(f"Q&A failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search-explain")
async def search_and_explain(request: RetrievalRequest):
    """Search and explain query results"""
    try:
        logger.info(f"Searching and explaining: {request.query}")

        qa_engine = get_qa_engine()
        result = qa_engine.search_and_explain(request.query)

        if not result.get("found"):
            return JSONResponse(
                status_code=404,
                content={"message": "No relevant information found"},
            )

        return result

    except Exception as e:
        logger.error(f"Search and explain failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Comprehensive Analysis Endpoint
# ============================================================================

@app.post("/analyze", response_model=ComprehensiveAnalysisResponse)
async def comprehensive_analysis(request: ComprehensiveAnalysisRequest):
    """Perform comprehensive conversation analysis"""
    try:
        start_time = time.time()
        logger.info("Starting comprehensive analysis")

        result = {
            "summary": None,
            "sentiment": None,
            "action_items": None,
            "themes": None,
            "risks": None,
        }

        # Summarization
        if request.include_summary:
            summarizer = get_summarizer()
            summary_result = summarizer.summarize_full(request.text)
            result["summary"] = summary_result.get("summary", "")

        # Sentiment Analysis
        if request.include_sentiment:
            analyzer = get_sentiment_analyzer()
            sentiment_result = analyzer.analyze_overall(request.text)
            result["sentiment"] = sentiment_result.get("analysis", "")

        # Action Items
        if request.include_action_items:
            extractor = get_action_item_extractor()
            action_result = extractor.extract_action_items(request.text)
            result["action_items"] = action_result.get("action_items", "")

        # Themes
        if request.include_themes:
            summarizer = get_summarizer()
            themes_result = summarizer.extract_themes(request.text)
            result["themes"] = themes_result.get("themes", "")

        # Risks
        if request.include_risks:
            extractor = get_action_item_extractor()
            risks_result = extractor.extract_risks_and_blockers(request.text)
            result["risks"] = risks_result.get("risks_and_blockers", "")

        analysis_time = time.time() - start_time

        return ComprehensiveAnalysisResponse(
            **result,
            analysis_time_seconds=analysis_time,
            success=True,
        )

    except Exception as e:
        logger.error(f"Comprehensive analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Vector Store Management Endpoints
# ============================================================================

@app.get("/vector-store/stats")
async def get_vector_store_stats():
    """Get vector store statistics"""
    try:
        vector_store = get_vector_store()
        return vector_store.get_stats()
    except Exception as e:
        logger.error(f"Failed to get vector store stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/vector-store/clear")
async def clear_vector_store():
    """Clear vector store (use with caution)"""
    try:
        logger.warning("Clearing vector store")
        vector_store = get_vector_store()
        vector_store.clear_index()
        return {"status": "cleared"}
    except Exception as e:
        logger.error(f"Failed to clear vector store: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Root Endpoint
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "endpoints": {
            "health": "/health",
            "transcribe": "/transcribe",
            "process": "/process-conversation",
            "retrieve": "/retrieve",
            "summarize": "/summarize",
            "sentiment": "/sentiment",
            "action_items": "/action-items",
            "qa": "/qa",
            "analyze": "/analyze",
        },
    }


# ============================================================================
# Error Handlers
# ============================================================================

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "timestamp": datetime.now().isoformat(),
        },
    )


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD and settings.DEBUG,
    )
