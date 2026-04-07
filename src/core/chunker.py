"""
Text chunking module for splitting large texts into manageable pieces
Implements overlapping chunks to maintain context
"""

import logging
from typing import List, Dict, Any
from config import settings

logger = logging.getLogger(__name__)


class TextChunker:
    """Splits text into overlapping chunks for embedding and retrieval"""

    def __init__(
        self,
        chunk_size: int = None,
        chunk_overlap: int = None,
        min_chunk_size: int = None,
    ):
        """
        Initialize chunker with specified parameters
        
        Args:
            chunk_size: Characters per chunk
            chunk_overlap: Overlap between chunks
            min_chunk_size: Minimum chunk size
        """
        self.chunk_size = chunk_size or settings.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP
        self.min_chunk_size = min_chunk_size or settings.MIN_CHUNK_SIZE

    def chunk_by_characters(self, text: str) -> List[Dict[str, Any]]:
        """
        Split text into chunks by character count
        
        Args:
            text: Input text to chunk
            
        Returns:
            List of chunks with metadata
        """
        if not text or len(text) < self.min_chunk_size:
            logger.warning("Text too short, returning as single chunk")
            return [{"id": 0, "text": text, "start": 0, "end": len(text)}]

        chunks = []
        start = 0

        while start < len(text):
            # Calculate end position
            end = min(start + self.chunk_size, len(text))

            # Try to end at sentence or word boundary
            if end < len(text):
                # Look for last period or newline
                last_period = text.rfind(".", start, end)
                last_newline = text.rfind("\n", start, end)
                last_boundary = max(last_period, last_newline)

                if last_boundary > start:
                    end = last_boundary + 1

            chunk_text = text[start:end].strip()

            if len(chunk_text) >= self.min_chunk_size:
                chunks.append(
                    {
                        "id": len(chunks),
                        "text": chunk_text,
                        "start": start,
                        "end": end,
                    }
                )

            # Move start for next chunk with overlap
            start = end - self.chunk_overlap

        logger.info(f"Created {len(chunks)} chunks from text")
        return chunks

    def chunk_by_sentences(self, text: str) -> List[Dict[str, Any]]:
        """
        Split text into chunks by sentences
        Groups sentences to maintain chunk_size target
        
        Args:
            text: Input text to chunk
            
        Returns:
            List of chunks with metadata
        """
        # Split by sentences (simple approach)
        sentences = [s.strip() for s in text.split(".") if s.strip()]

        if not sentences:
            return [{"id": 0, "text": text, "start": 0, "end": len(text)}]

        chunks = []
        current_chunk = []
        current_length = 0
        start_pos = 0

        for sentence in sentences:
            sentence_with_period = sentence + "."
            sentence_length = len(sentence_with_period)

            if (
                current_length + sentence_length > self.chunk_size
                and current_chunk
            ):
                # Save current chunk
                chunk_text = " ".join(current_chunk)
                chunks.append(
                    {
                        "id": len(chunks),
                        "text": chunk_text,
                        "start": start_pos,
                        "end": start_pos + len(chunk_text),
                    }
                )

                # Start overlap
                start_pos += (
                    len(chunk_text) - self.chunk_overlap
                )
                current_chunk = [sentence]
                current_length = sentence_length
            else:
                current_chunk.append(sentence)
                current_length += sentence_length

        # Don't forget last chunk
        if current_chunk:
            chunk_text = " ".join(current_chunk)
            chunks.append(
                {
                    "id": len(chunks),
                    "text": chunk_text,
                    "start": start_pos,
                    "end": start_pos + len(chunk_text),
                }
            )

        logger.info(f"Created {len(chunks)} chunks from sentences")
        return chunks

    def chunk_by_paragraphs(self, text: str) -> List[Dict[str, Any]]:
        """
        Split text into chunks by paragraphs
        Groups paragraphs intelligently
        
        Args:
            text: Input text to chunk
            
        Returns:
            List of chunks with metadata
        """
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

        if not paragraphs:
            return [{"id": 0, "text": text, "start": 0, "end": len(text)}]

        chunks = []
        current_chunk = []
        current_length = 0
        start_pos = 0

        for paragraph in paragraphs:
            para_length = len(paragraph)

            if (
                current_length + para_length > self.chunk_size
                and current_chunk
            ):
                # Save current chunk
                chunk_text = "\n\n".join(current_chunk)
                chunks.append(
                    {
                        "id": len(chunks),
                        "text": chunk_text,
                        "start": start_pos,
                        "end": start_pos + len(chunk_text),
                    }
                )

                # Start overlap
                start_pos += (
                    len(chunk_text) - self.chunk_overlap
                )
                current_chunk = [paragraph]
                current_length = para_length
            else:
                current_chunk.append(paragraph)
                current_length += para_length

        # Don't forget last chunk
        if current_chunk:
            chunk_text = "\n\n".join(current_chunk)
            chunks.append(
                {
                    "id": len(chunks),
                    "text": chunk_text,
                    "start": start_pos,
                    "end": start_pos + len(chunk_text),
                }
            )

        logger.info(f"Created {len(chunks)} chunks from paragraphs")
        return chunks

    def chunk(
        self,
        text: str,
        method: str = "characters",
    ) -> List[Dict[str, Any]]:
        """
        Chunk text using specified method
        
        Args:
            text: Input text
            method: 'characters', 'sentences', or 'paragraphs'
            
        Returns:
            List of chunks
        """
        if method == "sentences":
            return self.chunk_by_sentences(text)
        elif method == "paragraphs":
            return self.chunk_by_paragraphs(text)
        else:
            return self.chunk_by_characters(text)


# Global chunker instance
_chunker = None


def get_chunker() -> TextChunker:
    """Get or create singleton chunker"""
    global _chunker
    if _chunker is None:
        _chunker = TextChunker()
    return _chunker
