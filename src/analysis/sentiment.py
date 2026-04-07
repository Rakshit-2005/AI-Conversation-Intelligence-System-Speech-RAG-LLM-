"""
Sentiment analysis module
Analyzes emotional tone and sentiment of conversations
"""

import logging
from typing import Dict, Any, Optional
from src.analysis.llm_client import get_llm_client

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """Analyzes sentiment and emotional tone of conversations"""

    SENTIMENT_LABELS = ["positive", "neutral", "negative"]

    def __init__(self):
        """Initialize sentiment analyzer"""
        self.llm_client = get_llm_client()

    def analyze_overall(self, text: str) -> Dict[str, Any]:
        """
        Analyze overall sentiment of conversation
        
        Args:
            text: Conversation text
            
        Returns:
            Dictionary with sentiment analysis
        """
        try:
            logger.info("Analyzing overall sentiment")

            prompt = f"""Analyze the overall sentiment and emotional tone of this conversation.

CONVERSATION:
{text}

Determine:
1. Overall Sentiment: positive, neutral, or negative (MUST be one of these)
2. Confidence Score: 0.0-1.0
3. Justification: 2-3 sentences explaining why
4. Key Emotional Indicators: Words/phrases that influenced the sentiment
5. Tone: formal, friendly, professional, aggressive, etc.

Format your response as:
SENTIMENT: [positive/neutral/negative]
CONFIDENCE: [0.0-1.0]
JUSTIFICATION: [explanation]
TONE: [tone]
INDICATORS: [list]"""

            response = self.llm_client.call_llm(
                prompt=prompt,
                temperature=0.3,
                max_tokens=500,
            )

            return {
                "analysis": response,
                "type": "overall",
                "generated": True,
            }

        except Exception as e:
            logger.error(f"Overall sentiment analysis failed: {e}")
            raise

    def analyze_by_speaker(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment for each speaker
        
        Args:
            text: Conversation text (ideally with speaker labels)
            
        Returns:
            Dictionary with per-speaker sentiment
        """
        try:
            logger.info("Analyzing per-speaker sentiment")

            prompt = f"""Analyze the sentiment for each speaker in this conversation.

CONVERSATION:
{text}

For each distinct speaker/participant:
1. Identify them (by name or role if available)
2. Their overall sentiment: positive, neutral, or negative
3. How their sentiment changed (if at all)
4. Their attitude toward the topic/other speakers
5. How collaborative or adversarial they were

Format clearly with each speaker as a section."""

            response = self.llm_client.call_llm(
                prompt=prompt,
                temperature=0.5,
                max_tokens=800,
            )

            return {
                "per_speaker_analysis": response,
                "type": "per_speaker",
                "generated": True,
            }

        except Exception as e:
            logger.error(f"Per-speaker sentiment analysis failed: {e}")
            raise

    def analyze_by_topic(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment around different topics
        
        Args:
            text: Conversation text
            
        Returns:
            Dictionary with topic-based sentiment
        """
        try:
            logger.info("Analyzing topic-based sentiment")

            prompt = f"""Analyze sentiment around different topics in this conversation.

CONVERSATION:
{text}

For each major topic discussed:
1. Topic name
2. Sentiment when discussing it: positive/neutral/negative
3. Intensity (Low/Medium/High)
4. Key phrases indicating sentiment
5. Any shifts in sentiment (if topic revisited)

Organize by topic and explain each analysis."""

            response = self.llm_client.call_llm(
                prompt=prompt,
                temperature=0.5,
                max_tokens=800,
            )

            return {
                "topic_sentiment": response,
                "type": "by_topic",
                "generated": True,
            }

        except Exception as e:
            logger.error(f"Topic-based sentiment analysis failed: {e}")
            raise

    def detect_issues(self, text: str) -> Dict[str, Any]:
        """
        Detect potential issues, complaints, or concerns
        
        Args:
            text: Conversation text
            
        Returns:
            Dictionary with detected issues
        """
        try:
            logger.info("Detecting issues and concerns")

            prompt = f"""Identify any issues, complaints, concerns, or problems mentioned in this conversation.

CONVERSATION:
{text}

For each issue found:
1. Issue description
2. Severity: Critical/High/Medium/Low
3. Who raised it
4. Resolution discussed (if any)
5. Ownership (who should resolve it)

If no issues found, state that clearly.
Focus on actionable concerns that need attention."""

            response = self.llm_client.call_llm(
                prompt=prompt,
                temperature=0.4,
                max_tokens=700,
            )

            return {
                "issues_detected": response,
                "type": "issue_detection",
                "generated": True,
            }

        except Exception as e:
            logger.error(f"Issue detection failed: {e}")
            raise

    def detect_satisfaction(self, text: str) -> Dict[str, Any]:
        """
        Analyze customer/attendee satisfaction levels
        
        Args:
            text: Conversation text
            
        Returns:
            Dictionary with satisfaction metrics
        """
        try:
            logger.info("Analyzing satisfaction levels")

            prompt = f"""Analyze satisfaction levels in this conversation.

CONVERSATION:
{text}

Assess:
1. Overall Satisfaction Level: 1-10 (10 being most satisfied)
2. Satisfaction by Participant (if identifiable)
3. Key Satisfaction Drivers (what made them satisfied/dissatisfied)
4. Unmet Expectations (if any)
5. Net Promoter Score indicators (would they recommend)
6. Recommendations to improve satisfaction

Base this on tone, language, and expressed sentiments."""

            response = self.llm_client.call_llm(
                prompt=prompt,
                temperature=0.5,
                max_tokens=700,
            )

            return {
                "satisfaction": response,
                "type": "satisfaction",
                "generated": True,
            }

        except Exception as e:
            logger.error(f"Satisfaction analysis failed: {e}")
            raise


# Global analyzer instance
_analyzer = None


def get_sentiment_analyzer() -> SentimentAnalyzer:
    """Get or create singleton sentiment analyzer"""
    global _analyzer
    if _analyzer is None:
        _analyzer = SentimentAnalyzer()
    return _analyzer
