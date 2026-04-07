"""
Core LLM integration module
Handles communication with OpenAI or Gemini APIs
"""

import logging
from typing import Optional, Dict, Any
from config import settings

logger = logging.getLogger(__name__)


class LLMClient:
    """Unified interface for LLM providers"""

    def __init__(self, provider: str = None):
        """
        Initialize LLM client
        
        Args:
            provider: 'openai' or 'gemini'
        """
        self.provider = provider or settings.LLM_PROVIDER
        self._init_client()

    def _init_client(self):
        """Initialize provider-specific client"""
        if self.provider == "openai":
            try:
                import openai
                openai.api_key = settings.OPENAI_API_KEY
                self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
                logger.info("OpenAI client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
                raise

        elif self.provider == "gemini":
            try:
                import google.generativeai as genai
                genai.configure(api_key=settings.GEMINI_API_KEY)
                self.client = genai
                logger.info("Gemini client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini client: {e}")
                raise
        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    def call_llm(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Call LLM with prompt
        
        Args:
            prompt: Main prompt text
            system_prompt: System context
            temperature: Sampling temperature
            max_tokens: Maximum output tokens
            
        Returns:
            LLM response text
        """
        temperature = temperature or settings.TEMPERATURE
        max_tokens = max_tokens or settings.MAX_TOKENS

        try:
            if self.provider == "openai":
                return self._call_openai(
                    prompt, system_prompt, temperature, max_tokens
                )
            elif self.provider == "gemini":
                return self._call_gemini(
                    prompt, system_prompt, temperature, max_tokens
                )
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            raise

    def _call_openai(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
    ) -> str:
        """Call OpenAI API"""
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return response.choices[0].message.content

    def _call_gemini(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
    ) -> str:
        """Call Gemini API"""
        model = self.client.GenerativeModel(
            model_name=settings.GEMINI_MODEL,
            system_instruction=system_prompt,
        )

        response = model.generate_content(
            prompt,
            generation_config=self.client.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            ),
        )

        return response.text


# Global LLM client instance
_llm_client = None


def get_llm_client() -> LLMClient:
    """Get or create singleton LLM client"""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client
