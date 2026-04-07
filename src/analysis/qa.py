"""
Q&A Engine module
Answers natural language questions about conversations using RAG
"""

import logging
from typing import Dict, Any, Optional
from src.analysis.llm_client import get_llm_client
from src.rag.retriever import get_retriever

logger = logging.getLogger(__name__)


class ConversationQAEngine:
    """Answers questions about conversations using RAG"""

    def __init__(self):
        """Initialize Q&A engine"""
        self.llm_client = get_llm_client()
        self.retriever = get_retriever()

    def answer_question(self, question: str, context: str = None) -> Dict[str, Any]:
        """
        Answer a natural language question about the conversation
        
        Args:
            question: User's question
            context: Optional pre-retrieved context
            
        Returns:
            Dictionary with answer and sources
        """
        try:
            logger.info(f"Answering question: {question[:100]}...")

            # Retrieve relevant context if not provided
            if context is None:
                retrieved_chunks = self.retriever.retrieve(question, top_k=5)
                context = self.retriever.format_context(retrieved_chunks)
            else:
                retrieved_chunks = []

            # Generate answer using LLM
            prompt = f"""Based on the provided conversation context, answer this question directly and accurately.

QUESTION: {question}

CONTEXT FROM CONVERSATION:
{context}

Instructions:
- Answer directly and concisely
- Use only information from the context
- If the question cannot be answered from context, say "This information is not available in the conversation"
- Be specific and provide relevant details
- If asking about people, mention names when known

ANSWER:"""

            answer = self.llm_client.call_llm(
                prompt=prompt,
                temperature=0.3,
                max_tokens=500,
            )

            return {
                "question": question,
                "answer": answer.strip(),
                "sources": retrieved_chunks,
                "success": True,
            }

        except Exception as e:
            logger.error(f"Question answering failed: {e}")
            raise

    def ask_follow_up(
        self, question: str, conversation_history: list = None
    ) -> Dict[str, Any]:
        """
        Ask follow-up questions with conversation history
        
        Args:
            question: Current question
            conversation_history: List of previous exchanges
            
        Returns:
            Answer with conversation context
        """
        try:
            logger.info("Processing follow-up question")

            # Build conversation context
            history_text = ""
            if conversation_history:
                for i, exchange in enumerate(conversation_history):
                    history_text += f"Q{i+1}: {exchange.get('question', '')}\nA{i+1}: {exchange.get('answer', '')}\n"

            retrieved_chunks = self.retriever.retrieve(question, top_k=5)
            context = self.retriever.format_context(retrieved_chunks)

            prompt = f"""Based on the conversation context and previous Q&A history, answer this question.

PREVIOUS CONVERSATION:
{history_text}

CURRENT QUESTION: {question}

CONTEXT FROM CONVERSATION:
{context}

Maintain consistency with previous answers and provide context-aware response.

ANSWER:"""

            answer = self.llm_client.call_llm(
                prompt=prompt,
                temperature=0.3,
                max_tokens=500,
            )

            return {
                "question": question,
                "answer": answer.strip(),
                "sources": retrieved_chunks,
                "success": True,
            }

        except Exception as e:
            logger.error(f"Follow-up question failed: {e}")
            raise

    def search_and_explain(self, query: str) -> Dict[str, Any]:
        """
        Search for information and provide explanation
        
        Args:
            query: Search query
            
        Returns:
            Dictionary with search results and explanation
        """
        try:
            logger.info(f"Searching and explaining: {query}")

            # Search for relevant chunks
            chunks = self.retriever.retrieve(query, top_k=10)

            if not chunks:
                return {
                    "query": query,
                    "found": False,
                    "message": "No relevant information found",
                    "results": [],
                }

            # Generate explanation
            context = self.retriever.format_context(chunks)

            prompt = f"""Explain the following query based on the conversation context.

QUERY: {query}

CONTEXT:
{context}

Provide:
1. Direct Answer: Directly answer the query
2. Supporting Evidence: Key quotes or facts from context
3. Related Points: Additional relevant information
4. Caveats: Any limitations or uncertainties

Structure your response for clarity."""

            explanation = self.llm_client.call_llm(
                prompt=prompt,
                temperature=0.4,
                max_tokens=800,
            )

            return {
                "query": query,
                "found": True,
                "explanation": explanation.strip(),
                "sources": chunks,
                "result_count": len(chunks),
            }

        except Exception as e:
            logger.error(f"Search and explain failed: {e}")
            raise

    def multi_question_qa(self, questions: list) -> Dict[str, Any]:
        """
        Answer multiple questions about a conversation
        
        Args:
            questions: List of question strings
            
        Returns:
            Dictionary with answers to all questions
        """
        try:
            logger.info(f"Answering {len(questions)} questions")

            answers = []
            for question in questions:
                result = self.answer_question(question)
                answers.append(result)

            return {
                "total_questions": len(questions),
                "answers": answers,
                "success": True,
            }

        except Exception as e:
            logger.error(f"Multi-question QA failed: {e}")
            raise

    def answer_with_confidence(
        self, question: str, context: str = None, threshold: float = 0.3
    ) -> Dict[str, Any]:
        """
        Answer with confidence scoring
        
        Args:
            question: User question
            context: Optional context
            threshold: Minimum similarity threshold
            
        Returns:
            Answer with confidence metrics
        """
        try:
            logger.info("Answering with confidence scoring")

            # Retrieve context
            if context is None:
                retrieved_chunks = self.retriever.retrieve(
                    question, top_k=5, threshold=threshold
                )
                context = self.retriever.format_context(retrieved_chunks)
            else:
                retrieved_chunks = []

            # Check if we have enough context
            confidence = min(1.0, len(retrieved_chunks) / 3.0)  # Simple heuristic

            # Generate answer
            prompt = f"""Answer this question based on the provided context.
If uncertain, acknowledge the uncertainty.

QUESTION: {question}

CONTEXT:
{context}

ANSWER:"""

            answer = self.llm_client.call_llm(
                prompt=prompt,
                temperature=0.3,
                max_tokens=500,
            )

            return {
                "question": question,
                "answer": answer.strip(),
                "confidence": confidence,
                "context_relevance": [
                    chunk.get("similarity_score", 0) for chunk in retrieved_chunks
                ],
                "sources": retrieved_chunks,
            }

        except Exception as e:
            logger.error(f"Confidence-based QA failed: {e}")
            raise


# Global Q&A engine instance
_qa_engine = None


def get_qa_engine() -> ConversationQAEngine:
    """Get or create singleton Q&A engine"""
    global _qa_engine
    if _qa_engine is None:
        _qa_engine = ConversationQAEngine()
    return _qa_engine
