"""
Embeddings generation module
Converts text into vector embeddings for semantic search
"""

import logging
import asyncio
from typing import List, Dict, Any, Union
import numpy as np
from sentence_transformers import SentenceTransformer
from config import settings

logger = logging.getLogger(__name__)


class EmbeddingsGenerator:
    """Generates embeddings for text chunks"""

    def __init__(self, model_name: str = None):
        """
        Initialize embeddings generator
        
        Args:
            model_name: Sentence-transformers model name
        """
        self.model_name = model_name or settings.EMBEDDING_MODEL
        self.model = None
        self.dimension = settings.EMBEDDING_DIMENSION
        self._load_model()

    def _load_model(self):
        """Load sentence-transformers model"""
        try:
            logger.info(f"Loading embeddings model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            logger.info(f"Model loaded successfully, dimension: {self.dimension}")
        except Exception as e:
            logger.error(f"Failed to load embeddings model: {e}")
            raise

    def encode(self, texts: Union[str, List[str]]) -> np.ndarray:
        """
        Generate embeddings for text(s)
        
        Args:
            texts: Single text or list of texts
            
        Returns:
            NumPy array of embeddings
        """
        if isinstance(texts, str):
            texts = [texts]

        try:
            embeddings = self.model.encode(
                texts,
                batch_size=settings.BATCH_SIZE,
                convert_to_numpy=True,
                show_progress_bar=False,
            )

            if len(texts) == 1:
                return embeddings[0]

            return embeddings

        except Exception as e:
            logger.error(f"Failed to generate embeddings: {e}")
            raise

    def embed_chunks(
        self, chunks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Generate embeddings for text chunks
        
        Args:
            chunks: List of chunk dictionaries with 'text' key
            
        Returns:
            List of chunks with 'embedding' added
        """
        try:
            logger.info(f"Generating embeddings for {len(chunks)} chunks")

            # Extract texts
            texts = [chunk["text"] for chunk in chunks]

            # Generate embeddings
            embeddings = self.encode(texts)

            # Add embeddings to chunks
            for i, chunk in enumerate(chunks):
                chunk["embedding"] = embeddings[i].tolist()

            logger.info(f"Generated embeddings for {len(chunks)} chunks")
            return chunks

        except Exception as e:
            logger.error(f"Failed to embed chunks: {e}")
            raise

    async def embed_chunks_async(
        self, chunks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Async wrapper for embedding chunks
        
        Args:
            chunks: List of chunk dictionaries
            
        Returns:
            List of chunks with embeddings
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.embed_chunks, chunks)

    def get_dimension(self) -> int:
        """Get embedding vector dimension"""
        return self.dimension

    def similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Calculate cosine similarity between embeddings
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Similarity score (0-1)
        """
        # Convert to numpy if needed
        if isinstance(embedding1, list):
            embedding1 = np.array(embedding1)
        if isinstance(embedding2, list):
            embedding2 = np.array(embedding2)

        # Normalize vectors
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        # Calculate cosine similarity
        return float(
            np.dot(embedding1, embedding2) / (norm1 * norm2)
        )

    def batch_similarity(
        self,
        embedding1: np.ndarray,
        embeddings2: List[np.ndarray],
    ) -> List[float]:
        """
        Calculate similarity between one embedding and multiple embeddings
        
        Args:
            embedding1: Query embedding
            embeddings2: List of embeddings to compare
            
        Returns:
            List of similarity scores
        """
        similarities = []
        for emb2 in embeddings2:
            sim = self.similarity(embedding1, emb2)
            similarities.append(sim)
        return similarities


# Global embeddings generator instance
_embeddings_generator = None


def get_embeddings_generator() -> EmbeddingsGenerator:
    """Get or create singleton embeddings generator"""
    global _embeddings_generator
    if _embeddings_generator is None:
        _embeddings_generator = EmbeddingsGenerator()
    return _embeddings_generator
