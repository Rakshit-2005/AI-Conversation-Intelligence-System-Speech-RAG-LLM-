"""
FAISS vector database handler
Stores and retrieves embeddings for semantic search
"""

import logging
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
import faiss
from config import settings

logger = logging.getLogger(__name__)


class FAISSVectorStore:
    """Manages FAISS vector index and metadata"""

    def __init__(self, index_path: Path = None, dimension: int = 384):
        """
        Initialize FAISS vector store
        
        Args:
            index_path: Path to store/load index
            dimension: Vector dimension
        """
        self.index_path = index_path or settings.FAISS_INDEX_PATH
        self.metadata_path = settings.FAISS_METADATA_PATH
        self.dimension = dimension
        self.index = None
        self.metadata = []  # List of chunk metadata
        self.id_counter = 0

        # Create index directory if needed
        self.index_path.parent.mkdir(exist_ok=True, parents=True)
        self.metadata_path.parent.mkdir(exist_ok=True, parents=True)

        # Load existing index if available
        self._load_or_create_index()

    def _load_or_create_index(self):
        """Load existing index or create new one"""
        try:
            if self.index_path.exists():
                logger.info(f"Loading FAISS index from {self.index_path}")
                self.index = faiss.read_index(str(self.index_path))

                # Load metadata
                if self.metadata_path.exists():
                    with open(self.metadata_path, "r") as f:
                        self.metadata = json.load(f)
                    self.id_counter = len(self.metadata)
                    logger.info(
                        f"Loaded {len(self.metadata)} entries from metadata"
                    )
                else:
                    logger.warning("Index found but no metadata file")
            else:
                logger.info(
                    f"Creating new FAISS index with dimension {self.dimension}"
                )
                self.index = faiss.IndexFlatL2(self.dimension)

        except Exception as e:
            logger.error(f"Failed to load/create index: {e}")
            raise

    def add_embeddings(
        self, embeddings: List[np.ndarray], metadata: List[Dict[str, Any]]
    ) -> None:
        """
        Add embeddings to index
        
        Args:
            embeddings: List of embedding vectors
            metadata: List of metadata dictionaries
        """
        try:
            if len(embeddings) != len(metadata):
                raise ValueError("Embeddings and metadata length mismatch")

            # Convert embeddings to numpy array
            embeddings_array = np.array(embeddings, dtype=np.float32)

            logger.info(f"Adding {len(embeddings)} embeddings to index")

            # Add to FAISS index
            self.index.add(embeddings_array)

            # Store metadata
            for i, meta in enumerate(metadata):
                meta["id"] = self.id_counter + i
                self.metadata.append(meta)

            self.id_counter += len(metadata)
            logger.info(f"Total entries in index: {len(self.metadata)}")

            # Save to disk
            self._save_index()

        except Exception as e:
            logger.error(f"Failed to add embeddings: {e}")
            raise

    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar embeddings
        
        Args:
            query_embedding: Query vector
            k: Number of results to return
            
        Returns:
            List of similar chunks with scores
        """
        try:
            if self.index.ntotal == 0:
                logger.warning("Index is empty")
                return []

            # Convert to numpy float32
            query_vector = np.array([query_embedding], dtype=np.float32)

            # Search
            distances, indices = self.index.search(query_vector, min(k, self.index.ntotal))

            results = []
            for dist, idx in zip(distances[0], indices[0]):
                if idx >= 0 and idx < len(self.metadata):
                    metadata = self.metadata[idx].copy()
                    # Convert L2 distance to similarity score (0-1)
                    similarity = 1 / (1 + dist)
                    metadata["similarity_score"] = float(similarity)
                    metadata["distance"] = float(dist)
                    results.append(metadata)

            logger.info(f"Search returned {len(results)} results")
            return results

        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise

    def search_multiple(
        self, query_embeddings: List[np.ndarray], k: int = 5
    ) -> List[List[Dict[str, Any]]]:
        """
        Search for multiple query embeddings
        
        Args:
            query_embeddings: List of query vectors
            k: Number of results per query
            
        Returns:
            List of result lists
        """
        results = []
        for emb in query_embeddings:
            results.append(self.search(emb, k))
        return results

    def delete_by_id(self, doc_id: str) -> None:
        """
        Delete entries by document ID (note: FAISS doesn't natively support deletion)
        We mark as deleted in metadata
        
        Args:
            doc_id: Document identifier
        """
        try:
            logger.info(f"Marking document as deleted: {doc_id}")
            for meta in self.metadata:
                if meta.get("doc_id") == doc_id:
                    meta["deleted"] = True
            self._save_index()
        except Exception as e:
            logger.error(f"Failed to delete document: {e}")
            raise

    def clear_index(self) -> None:
        """Clear all data from index"""
        try:
            logger.warning("Clearing FAISS index")
            self.index = faiss.IndexFlatL2(self.dimension)
            self.metadata = []
            self.id_counter = 0

            # Delete from disk
            if self.index_path.exists():
                self.index_path.unlink()
            if self.metadata_path.exists():
                self.metadata_path.unlink()

        except Exception as e:
            logger.error(f"Failed to clear index: {e}")
            raise

    def _save_index(self) -> None:
        """Save index and metadata to disk"""
        try:
            # Save FAISS index
            faiss.write_index(self.index, str(self.index_path))

            # Save metadata
            with open(self.metadata_path, "w") as f:
                json.dump(self.metadata, f, indent=2)

            logger.info("Index saved to disk")

        except Exception as e:
            logger.error(f"Failed to save index: {e}")
            raise

    def get_stats(self) -> Dict[str, Any]:
        """Get index statistics"""
        return {
            "total_entries": len(self.metadata),
            "dimension": self.dimension,
            "index_type": "FlatL2",
            "index_path": str(self.index_path),
            "metadata_path": str(self.metadata_path),
        }


# Global vector store instance
_vector_store = None


def get_vector_store(dimension: int = 384) -> FAISSVectorStore:
    """Get or create singleton vector store"""
    global _vector_store
    if _vector_store is None:
        _vector_store = FAISSVectorStore(dimension=dimension)
    return _vector_store
