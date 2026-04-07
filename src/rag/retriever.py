"""
RAG Retriever module
Orchestrates retrieval of relevant context for LLM queries
"""

import logging
from typing import List, Dict, Any, Optional
import numpy as np
from config import settings
from src.core.embedder import get_embeddings_generator
from src.rag.vector_store import get_vector_store

logger = logging.getLogger(__name__)


class RAGRetriever:
    """Retrieves relevant context for queries using embeddings and vector search"""

    def __init__(self, top_k: int = 5, similarity_threshold: float = 0.3):
        """
        Initialize RAG retriever
        
        Args:
            top_k: Number of top results to retrieve
            similarity_threshold: Minimum similarity score threshold
        """
        self.top_k = top_k
        self.similarity_threshold = similarity_threshold
        self.embeddings_gen = get_embeddings_generator()
        self.vector_store = get_vector_store()

    def retrieve(
        self, query: str, top_k: Optional[int] = None, threshold: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant chunks for a query
        
        Args:
            query: User query string
            top_k: Override default top_k
            threshold: Override default threshold
            
        Returns:
            List of relevant chunks with scores
        """
        top_k = top_k or self.top_k
        threshold = threshold or self.similarity_threshold

        try:
            logger.info(f"Retrieving context for query: {query[:100]}...")

            # Generate query embedding
            query_embedding = self.embeddings_gen.encode(query)

            # Search vector store
            results = self.vector_store.search(query_embedding, k=top_k)

            # Filter by threshold
            filtered_results = [
                r for r in results
                if r.get("similarity_score", 0) >= threshold
                and not r.get("deleted", False)
            ]

            logger.info(f"Retrieved {len(filtered_results)} relevant chunks")
            return filtered_results

        except Exception as e:
            logger.error(f"Retrieval failed: {e}")
            raise

    def retrieve_batch(
        self, queries: List[str], top_k: Optional[int] = None
    ) -> List[List[Dict[str, Any]]]:
        """
        Retrieve context for multiple queries
        
        Args:
            queries: List of queries
            top_k: Override default top_k
            
        Returns:
            List of result lists
        """
        results = []
        for query in queries:
            results.append(self.retrieve(query, top_k))
        return results

    def format_context(
        self, chunks: List[Dict[str, Any]], max_chars: int = None
    ) -> str:
        """
        Format retrieved chunks into a context string for LLM
        
        Args:
            chunks: List of relevant chunks
            max_chars: Maximum total characters
            
        Returns:
            Formatted context string
        """
        max_chars = max_chars or settings.CONTEXT_WINDOW_SIZE

        context_parts = []
        total_chars = 0

        for chunk in chunks:
            chunk_text = chunk.get("text", "")
            similarity = chunk.get("similarity_score", 0)

            # Include chunk with metadata
            chunk_str = f"[Relevance: {similarity:.2f}]\n{chunk_text}\n"

            if total_chars + len(chunk_str) <= max_chars:
                context_parts.append(chunk_str)
                total_chars += len(chunk_str)
            else:
                break

        context = "\n---\n".join(context_parts)
        logger.info(f"Formatted context: {len(context)} characters")
        return context

    def rerank_results(
        self, query: str, chunks: List[Dict[str, Any]], method: str = "similarity"
    ) -> List[Dict[str, Any]]:
        """
        Re-rank retrieved results
        
        Args:
            query: Original query
            chunks: Retrieved chunks
            method: Ranking method ('similarity' or 'mmr')
            
        Returns:
            Re-ranked chunks
        """
        if method == "mmr":
            return self._rerank_mmr(query, chunks)
        else:
            # Already ranked by similarity
            return sorted(
                chunks,
                key=lambda x: x.get("similarity_score", 0),
                reverse=True
            )

    def _rerank_mmr(
        self, query: str, chunks: List[Dict[str, Any]], lambda_param: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Maximal Marginal Relevance ranking
        Balances relevance and diversity
        
        Args:
            query: Original query
            chunks: Retrieved chunks
            lambda_param: Balance parameter (0-1)
            
        Returns:
            MMR-ranked chunks
        """
        if not chunks:
            return chunks

        try:
            query_emb = self.embeddings_gen.encode(query)
            chunk_embs = [
                np.array(c.get("embedding", [])) for c in chunks
            ]

            selected_indices = []
            remaining_indices = list(range(len(chunks)))

            while remaining_indices and len(selected_indices) < len(chunks):
                mmr_scores = []

                for i in remaining_indices:
                    # Relevance to query
                    sim_to_query = float(np.dot(query_emb, chunk_embs[i]) / (
                        np.linalg.norm(query_emb) * np.linalg.norm(chunk_embs[i]) + 1e-6
                    ))

                    # Diversity from selected
                    min_sim_to_selected = float('inf')
                    if selected_indices:
                        for j in selected_indices:
                            sim_to_selected = float(np.dot(chunk_embs[i], chunk_embs[j]) / (
                                np.linalg.norm(chunk_embs[i]) * np.linalg.norm(chunk_embs[j]) + 1e-6
                            ))
                            min_sim_to_selected = min(min_sim_to_selected, sim_to_selected)
                    else:
                        min_sim_to_selected = 1.0

                    # MMR score
                    mmr = lambda_param * sim_to_query - (1 - lambda_param) * min_sim_to_selected
                    mmr_scores.append(mmr)

                # Select best MMR score
                best_idx = remaining_indices[np.argmax(mmr_scores)]
                selected_indices.append(best_idx)
                remaining_indices.remove(best_idx)

            # Return in MMR order
            return [chunks[i] for i in selected_indices]

        except Exception as e:
            logger.warning(f"MMR reranking failed: {e}, returning original order")
            return chunks


# Global retriever instance
_retriever = None


def get_retriever(top_k: int = None, threshold: float = None) -> RAGRetriever:
    """Get or create singleton retriever"""
    global _retriever
    if _retriever is None:
        top_k = top_k or settings.RETRIEVAL_TOP_K
        threshold = threshold or settings.SIMILARITY_THRESHOLD
        _retriever = RAGRetriever(top_k=top_k, similarity_threshold=threshold)
    return _retriever
