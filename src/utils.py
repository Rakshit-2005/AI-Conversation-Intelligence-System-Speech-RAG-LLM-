"""
Utility functions
"""

import logging
from pathlib import Path
from typing import List, Dict, Any
import json

logger = logging.getLogger(__name__)


def read_text_file(file_path: str) -> str:
    """Read text file"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"Failed to read file {file_path}: {e}")
        raise


def save_text_file(file_path: str, content: str) -> None:
    """Save text file"""
    try:
        Path(file_path).parent.mkdir(exist_ok=True, parents=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        logger.info(f"Saved file: {file_path}")
    except Exception as e:
        logger.error(f"Failed to save file {file_path}: {e}")
        raise


def save_json_file(file_path: str, data: Dict[str, Any]) -> None:
    """Save JSON file"""
    try:
        Path(file_path).parent.mkdir(exist_ok=True, parents=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        logger.info(f"Saved JSON file: {file_path}")
    except Exception as e:
        logger.error(f"Failed to save JSON file {file_path}: {e}")
        raise


def load_json_file(file_path: str) -> Dict[str, Any]:
    """Load JSON file"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load JSON file {file_path}: {e}")
        raise


def format_timestamp(timestamp: float) -> str:
    """Format timestamp to readable format"""
    from datetime import datetime
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to max length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def extract_key_words(text: str, num_keywords: int = 10) -> List[str]:
    """Extract key words from text (simple approach)"""
    import re
    
    # Remove special characters and convert to lowercase
    text = re.sub(r"[^a-zA-Z\s]", "", text.lower())
    
    # Split into words
    words = text.split()
    
    # Filter common stop words
    stop_words = {
        "the", "a", "an", "and", "or", "but", "is", "are", "was", "were",
        "be", "been", "being", "have", "has", "had", "do", "does", "did",
        "will", "would", "could", "should", "may", "might", "must", "can",
        "in", "on", "at", "to", "from", "of", "for", "with", "by", "as",
        "it", "its", "that", "this", "these", "those", "which", "who",
        "what", "when", "where", "why", "how"
    }
    
    # Count word frequency
    word_freq = {}
    for word in words:
        if word not in stop_words and len(word) > 2:
            word_freq[word] = word_freq.get(word, 0) + 1
    
    # Sort by frequency and return top keywords
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return [word[0] for word in sorted_words[:num_keywords]]


def calculate_text_statistics(text: str) -> Dict[str, Any]:
    """Calculate statistics about text"""
    words = text.split()
    sentences = text.split(".")
    
    return {
        "character_count": len(text),
        "word_count": len(words),
        "sentence_count": len([s for s in sentences if s.strip()]),
        "average_word_length": sum(len(w) for w in words) / len(words) if words else 0,
        "average_sentence_length": len(words) / len(sentences) if sentences else 0,
    }
