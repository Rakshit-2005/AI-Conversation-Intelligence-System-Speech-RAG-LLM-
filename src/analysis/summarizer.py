"""
Conversation summarization module
Generates concise summaries of conversations
"""

import logging
from typing import Dict, Any, Optional
from src.analysis.llm_client import get_llm_client

logger = logging.getLogger(__name__)


class ConversationSummarizer:
    """Generates intelligent summaries of conversations"""

    def __init__(self):
        """Initialize summarizer"""
        self.llm_client = get_llm_client()

    def summarize_full(self, text: str) -> Dict[str, Any]:
        """
        Generate full summary of conversation
        
        Args:
            text: Full conversation text
            
        Returns:
            Dictionary with summary and key points
        """
        try:
            logger.info("Generating full conversation summary")

            prompt = f"""Provide a comprehensive summary of this conversation.

CONVERSATION:
{text}

Generate:
1. Executive Summary (2-3 sentences)
2. Key Discussion Points (bullet points)
3. Main Outcomes
4. Follow-up Items (if any)

Format your response clearly with these sections."""

            response = self.llm_client.call_llm(
                prompt=prompt,
                temperature=0.5,
                max_tokens=1000,
            )

            return {
                "summary": response,
                "type": "full",
                "generated": True,
            }

        except Exception as e:
            logger.error(f"Full summarization failed: {e}")
            raise

    def summarize_bullet_points(self, text: str) -> Dict[str, Any]:
        """
        Extract key discussion points as bullet points
        
        Args:
            text: Conversation text
            
        Returns:
            Dictionary with bullet-point summary
        """
        try:
            logger.info("Extracting bullet-point summary")

            prompt = f"""Extract the key discussion points from this conversation.

CONVERSATION:
{text}

Provide a concise list of bullet points (max 10) covering:
- Main topics discussed
- Important decisions made
- Notable proposals or ideas
- Any concerns raised

Format as a clean bullet-point list."""

            response = self.llm_client.call_llm(
                prompt=prompt,
                temperature=0.3,
                max_tokens=500,
            )

            return {
                "bullet_points": response,
                "type": "bullet_points",
                "generated": True,
            }

        except Exception as e:
            logger.error(f"Bullet-point summarization failed: {e}")
            raise

    def summarize_with_context(
        self, text: str, context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate summary with optional context
        
        Args:
            text: Conversation text
            context: Optional context about conversation
            
        Returns:
            Dictionary with contextual summary
        """
        try:
            logger.info("Generating contextual summary")

            context_section = f"\nCONTEXT:\n{context}" if context else ""

            prompt = f"""Summarize the following conversation focusing on business value and outcomes.{context_section}

CONVERSATION:
{text}

Provide:
1. One-liner summary
2. Business Impact
3. Key Stakeholder Actions
4. Success Metrics (if discussed)

Be concise and action-oriented."""

            response = self.llm_client.call_llm(
                prompt=prompt,
                temperature=0.5,
                max_tokens=800,
            )

            return {
                "contextual_summary": response,
                "type": "contextual",
                "generated": True,
            }

        except Exception as e:
            logger.error(f"Contextual summarization failed: {e}")
            raise

    def extract_themes(self, text: str) -> Dict[str, Any]:
        """
        Extract main themes from conversation
        
        Args:
            text: Conversation text
            
        Returns:
            Dictionary with identified themes
        """
        try:
            logger.info("Extracting conversation themes")

            prompt = f"""Identify and categorize the main themes in this conversation.

CONVERSATION:
{text}

Identify:
1. Primary Theme (main topic)
2. Secondary Themes (supporting topics)
3. Sentiment/Tone (overall and per topic)
4. Urgency Level (Low/Medium/High)
5. Domain/Category (e.g., Sales, Support, Technical)

Explain briefly why you categorized it this way."""

            response = self.llm_client.call_llm(
                prompt=prompt,
                temperature=0.3,
                max_tokens=600,
            )

            return {
                "themes": response,
                "type": "themes",
                "generated": True,
            }

        except Exception as e:
            logger.error(f"Theme extraction failed: {e}")
            raise


# Global summarizer instance
_summarizer = None


def get_summarizer() -> ConversationSummarizer:
    """Get or create singleton summarizer"""
    global _summarizer
    if _summarizer is None:
        _summarizer = ConversationSummarizer()
    return _summarizer
