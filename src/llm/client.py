import asyncio
import logging
from typing import Optional, Dict, Any, List
from openai import AsyncOpenAI, APIError, RateLimitError, APITimeoutError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type, before_sleep_log

from config.settings import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self):
        if settings.OPENAI_API_KEY:
            self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            self.provider = "openai"
            logger.info("Using OpenAI Provider")
        elif settings.GROQ_API_KEY:
            self.client = AsyncOpenAI(
                api_key=settings.GROQ_API_KEY,
                base_url="https://api.groq.com/openai/v1"
            )
            self.provider = "groq"
            logger.info("Using Groq Provider")
        else:
            raise ValueError("No valid LLM API Key found (OpenAI or Groq)")

    def _map_model(self, model: str) -> str:
        """Map OpenAI models to Groq equivalents if needed."""
        if self.provider == "openai":
            return model
        
        # Groq Mapping
        # High intellingence -> Llama 3 70B
        if "gpt-4" in model:
            return "llama3-70b-8192"
        # Low/Medium -> Llama 3 8B or Mixtral
        elif "gpt-3.5" in model or "mini" in model:
            return "llama3-8b-8192" 
        return "llama3-70b-8192" # Default fallback
        
    @retry(
        retry=retry_if_exception_type((RateLimitError, APITimeoutError, APIError)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        before_sleep=before_sleep_log(logger, logging.WARNING)
    )
    async def generate_response(
        self, 
        model: str, 
        messages: List[Dict[str, str]], 
        temperature: float = 0.7,
        max_tokens: int = 500,
        response_format: Optional[Dict[str, str]] = None,
        timeout: float = 15.0
    ) -> str:
        """
        Generate a completion with robust error handling and retries.
        """
        target_model = self._map_model(model)
        try:
            response = await self.client.chat.completions.create(
                model=target_model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                response_format=response_format,
                timeout=timeout
            )
            return response.choices[0].message.content
        except APITimeoutError:
            logger.error(f"LLM Timeout Error (model={model})")
            raise
        except RateLimitError:
            logger.error(f"LLM Rate Limit Error (model={model})")
            raise
        except APIError as e:
            logger.error(f"LLM API Error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected LLM Error: {str(e)}")
            raise

    async def classify_text(self, text: str, prompt: str) -> Dict[str, Any]:
        """
        Specialized method for JSON classification tasks.
        Uses a cheaper model for classification if appropriate, but orchestrator decides.
        """
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ]
        
        # Using 5s timeout for classification as per requirements
        json_str = await self.generate_response(
            model=settings.MODEL_MEDIUM_RISK, # Use mini for classification
            messages=messages,
            temperature=0.0,
            response_format={"type": "json_object"},
            timeout=5.0
        )
        
        logger.info(f"Classification Raw Output: {json_str}")

        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            logger.error("Failed to decode JSON from classification")
            # Fallback safe response
            return {
                "risk_level": "MEDIUM_RISK", 
                "confidence_score": 0.0,
                "recommended_action": "Fallback due to parse error"
            }
            
import json
