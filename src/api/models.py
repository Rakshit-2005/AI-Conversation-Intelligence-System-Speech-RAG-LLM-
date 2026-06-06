"""
FastAPI request and response models
"""

from pydantic import BaseModel
from typing import List, Dict, Any, Optional


# Transcription Models
class TranscriptionRequest(BaseModel):
    """Request for audio transcription"""
    audio_path: str
    language: Optional[str] = None


class TranscriptionResponse(BaseModel):
    """Response from transcription"""
    text: str
    language: str
    duration: float
    segments: List[Dict[str, Any]] = []


# Processing Models
class ProcessConversationRequest(BaseModel):
    """Request to process full conversation"""
    audio_path: str
    language: Optional[str] = None


class ProcessConversationResponse(BaseModel):
    """Response from conversation processing"""
    id: str
    transcription: str
    embedding_status: str
    vector_index_size: int
    processing_time_seconds: float


# RAG/Retrieval Models
class RetrievalRequest(BaseModel):
    """Request to retrieve relevant chunks"""
    query: str
    top_k: int = 5
    threshold: float = 0.3


class ChunkResponse(BaseModel):
    """Response for a single chunk"""
    id: int
    text: str
    similarity_score: float
    distance: float


class RetrievalResponse(BaseModel):
    """Response from retrieval"""
    query: str
    chunks: List[ChunkResponse]
    total_retrieved: int


# Analysis Models
class SummarizationRequest(BaseModel):
    """Request for conversation summarization"""
    text: str
    type: str = "full"  # full, bullet_points, contextual


class SummarizationResponse(BaseModel):
    """Response from summarization"""
    summary: str
    type: str


class SentimentAnalysisRequest(BaseModel):
    """Request for sentiment analysis"""
    text: str
    analysis_type: str = "overall"  # overall, by_speaker, by_topic, issues, satisfaction


class SentimentAnalysisResponse(BaseModel):
    """Response from sentiment analysis"""
    analysis: str
    type: str


class ActionItemsRequest(BaseModel):
    """Request for action item extraction"""
    text: str
    extraction_type: str = "full"  # full, decisions_only, deadlines_only, risks_only


class ActionItemsResponse(BaseModel):
    """Response from action item extraction"""
    items: str
    type: str
    item_count: int = 0


class QARequest(BaseModel):
    """Request for Q&A"""
    question: str
    context: Optional[str] = None


class QAResponse(BaseModel):
    """Response from Q&A"""
    question: str
    answer: str
    confidence: float
    sources: List[ChunkResponse] = []


class MultiQuestionRequest(BaseModel):
    """Request for multiple questions"""
    questions: List[str]


class MultiQuestionResponse(BaseModel):
    """Response for multiple questions"""
    answers: List[QAResponse]
    total_questions: int


# Comprehensive Analysis Request
class ComprehensiveAnalysisRequest(BaseModel):
    """Request for comprehensive conversation analysis"""
    text: str
    include_summary: bool = True
    include_sentiment: bool = True
    include_action_items: bool = True
    include_themes: bool = True
    include_risks: bool = True


class ComprehensiveAnalysisResponse(BaseModel):
    """Response with comprehensive analysis"""
    summary: Optional[str] = None
    sentiment: Optional[str] = None
    action_items: Optional[str] = None
    themes: Optional[str] = None
    risks: Optional[str] = None
    analysis_time_seconds: float
    success: bool


# Health Check Models
class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    llm_provider: str
    vector_store_ready: bool
    embeddings_ready: bool


# Audio Upload Models
class AudioUploadResponse(BaseModel):
    """Response from audio file upload"""
    filename: str
    filepath: str
    size_bytes: int
    status: str


# Error Response Model
class ErrorResponse(BaseModel):
    """Error response"""
    detail: str
    error_code: Optional[str] = None
    timestamp: Optional[str] = None
