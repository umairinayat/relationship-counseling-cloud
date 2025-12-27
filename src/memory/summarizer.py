import logging
import re
from typing import Dict, Any, List
from src.llm.client import LLMClient
from config.settings import get_settings

logger = logging.getLogger(__name__)

class MemorySummarizer:
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    async def generate_summary(self, conversation_history: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Condense conversation into structure: Context, Themes, Emotions, Progress Note.
        """
        prompt = """
        Analyze this conversation. Extract specific updates for:
        1. Relationship Status/Context
        2. Recurring Themes
        3. Emotional Patterns
        4. A brief progress note (max 200 chars).

        SAFETY RULES:
        - REMOVE all PII (names, dates, locations).
        - REMOVE specific details of abuse or crisis (summarize as "reported safety concern").
        - REMOVE medical details.
        
        Output JSON.
        """
        
        # Simplified for brevity in this step, generally you'd pass full history
        history_text = "\n".join([f"{m['role']}: {m['content']}" for m in conversation_history])
        
        try:
            summary_json = await self.llm.generate_response(
                model="gpt-4o-mini", # Cheap model for summarization
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": history_text}
                ],
                response_format={"type": "json_object"}
            )
            # Should stick to a Pydantic model in real life but dict is fine here
            import json
            data = json.loads(summary_json)
            
            # Post-process validation
            if self._contains_prohibited_content(str(data)):
                logger.warning("Summary contained prohibited content. Discarding.")
                return {}
                
            return data
        except Exception as e:
            logger.error(f"Summarization failed: {e}")
            return {}

    def _contains_prohibited_content(self, text: str) -> bool:
        """
        Regex + Keyword blocking for safety in memory.
        """
        prohibited_patterns = [
            r"\d{3}-\d{2}-\d{4}", # SSN like
            r"suicid",
            r"kill myself",
            # Add more patterns
        ]
        
        for p in prohibited_patterns:
            if re.search(p, text, re.IGNORECASE):
                return True
        return False
