"""
Action items extraction module
Identifies tasks, decisions, and follow-ups from conversations
"""

import logging
from typing import Dict, Any, List
from src.analysis.llm_client import get_llm_client

logger = logging.getLogger(__name__)


class ActionItemExtractor:
    """Extracts action items and decisions from conversations"""

    def __init__(self):
        """Initialize action item extractor"""
        self.llm_client = get_llm_client()

    def extract_action_items(self, text: str) -> Dict[str, Any]:
        """
        Extract all action items from conversation
        
        Args:
            text: Conversation text
            
        Returns:
            Dictionary with extracted action items
        """
        try:
            logger.info("Extracting action items")

            prompt = f"""Extract all action items, tasks, and commitments from this conversation.

CONVERSATION:
{text}

For each action item found, provide:
1. Task Description: What needs to be done
2. Owner: Who is responsible (name or role)
3. Due Date: When it's due (if mentioned)
4. Priority: High/Medium/Low
5. Dependencies: Other items that must be completed first
6. Status: New/In Progress/Blocked/etc.
7. Context: Why this action item exists

Format each action item clearly and number them.
If no action items found, state that clearly."""

            response = self.llm_client.call_llm(
                prompt=prompt,
                temperature=0.3,
                max_tokens=1200,
            )

            return {
                "action_items": response,
                "type": "extraction",
                "generated": True,
            }

        except Exception as e:
            logger.error(f"Action item extraction failed: {e}")
            raise

    def extract_decisions(self, text: str) -> Dict[str, Any]:
        """
        Extract important decisions made
        
        Args:
            text: Conversation text
            
        Returns:
            Dictionary with extracted decisions
        """
        try:
            logger.info("Extracting decisions")

            prompt = f"""Extract all key decisions and commitments made in this conversation.

CONVERSATION:
{text}

For each decision, provide:
1. Decision: What was decided (be specific)
2. Made By: Who made the decision
3. Agreed By: Who agreed/acknowledged it
4. Rationale: Why this decision was made
5. Impact: What this decision affects
6. Implementation Status: How/when will it be implemented
7. Risks: Any identified risks

Format clearly and list each decision separately.
Focus on concrete decisions, not just discussions."""

            response = self.llm_client.call_llm(
                prompt=prompt,
                temperature=0.4,
                max_tokens=1000,
            )

            return {
                "decisions": response,
                "type": "decisions",
                "generated": True,
            }

        except Exception as e:
            logger.error(f"Decision extraction failed: {e}")
            raise

    def extract_deadlines(self, text: str) -> Dict[str, Any]:
        """
        Extract mentioned deadlines and dates
        
        Args:
            text: Conversation text
            
        Returns:
            Dictionary with extracted deadlines
        """
        try:
            logger.info("Extracting deadlines")

            prompt = f"""Extract all mentioned deadlines, dates, and time commitments from this conversation.

CONVERSATION:
{text}

For each deadline/date mentioned:
1. Date/Deadline: The actual date or timeframe
2. Related To: What needs to be completed by this date
3. Owner: Who is responsible
4. Flexibility: Is this date fixed or flexible
5. Consequences: What happens if deadline is missed

Also identify:
- Items with implied urgency but no explicit date
- Critical path items (dependencies between deadlines)
- Any date conflicts or over-commitments

Format with dates in YYYY-MM-DD format where possible."""

            response = self.llm_client.call_llm(
                prompt=prompt,
                temperature=0.3,
                max_tokens=800,
            )

            return {
                "deadlines": response,
                "type": "deadlines",
                "generated": True,
            }

        except Exception as e:
            logger.error(f"Deadline extraction failed: {e}")
            raise

    def extract_risks_and_blockers(self, text: str) -> Dict[str, Any]:
        """
        Extract identified risks and potential blockers
        
        Args:
            text: Conversation text
            
        Returns:
            Dictionary with extracted risks/blockers
        """
        try:
            logger.info("Extracting risks and blockers")

            prompt = f"""Identify all risks, blockers, and potential issues discussed or implied.

CONVERSATION:
{text}

For each risk/blocker:
1. Risk/Blocker Description: What could go wrong
2. Severity: Critical/High/Medium/Low
3. Likelihood: High/Medium/Low (estimated)
4. Affected Items: Which action items or goals are affected
5. Mitigation: Any mitigation strategies discussed
6. Owner: Who should monitor/address this
7. Status: Identified/Monitoring/Mitigating

Also identify:
- Implicit risks (things that could go wrong even if not mentioned)
- Dependencies that could become blockers
- Resource constraints

Be thorough but realistic."""

            response = self.llm_client.call_llm(
                prompt=prompt,
                temperature=0.5,
                max_tokens=1000,
            )

            return {
                "risks_and_blockers": response,
                "type": "risks",
                "generated": True,
            }

        except Exception as e:
            logger.error(f"Risk extraction failed: {e}")
            raise

    def generate_action_plan(self, text: str) -> Dict[str, Any]:
        """
        Generate a comprehensive action plan
        
        Args:
            text: Conversation text
            
        Returns:
            Dictionary with structured action plan
        """
        try:
            logger.info("Generating action plan")

            prompt = f"""Create a comprehensive, prioritized action plan from this conversation.

CONVERSATION:
{text}

Generate an action plan with:
1. Executive Summary: What needs to happen
2. Phase 1 (Immediate - Next 1 week): Critical items
3. Phase 2 (Short-term - Next 2-4 weeks): Important items
4. Phase 3 (Long-term - Next month+): Nice-to-have items
5. Critical Path: Sequence of dependent tasks
6. Resource Requirements: Who/what is needed
7. Success Metrics: How to measure completion/success
8. Risk Management: Top 3 risks and mitigation
9. Stakeholder Communication: Who needs updates and when
10. Follow-up Meeting: When to review progress

Format as a formal action plan document."""

            response = self.llm_client.call_llm(
                prompt=prompt,
                temperature=0.5,
                max_tokens=1500,
            )

            return {
                "action_plan": response,
                "type": "comprehensive_plan",
                "generated": True,
            }

        except Exception as e:
            logger.error(f"Action plan generation failed: {e}")
            raise


# Global extractor instance
_extractor = None


def get_action_item_extractor() -> ActionItemExtractor:
    """Get or create singleton action item extractor"""
    global _extractor
    if _extractor is None:
        _extractor = ActionItemExtractor()
    return _extractor
