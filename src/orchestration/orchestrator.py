import asyncio
import logging
import time
from uuid import UUID
from typing import Optional, Dict

from src.llm.client import LLMClient
from src.llm import prompts
from src.orchestration.safety import SafetyGuardrails
from src.orchestration.hallucination_controls import HallucinationControls
from src.memory.retrieval import MemoryRetrieval
from src.memory.summarizer import MemorySummarizer
from src.cost.optimizer import CostOptimizer
from src.cost.router import ModelRouter
from src.cost.cache import ResponseCache
from src.database.client import DatabaseClient
from src.monitoring.client import MonitoringClient

logger = logging.getLogger(__name__)

class ConversationOrchestrator:
    def __init__(self):
        self.llm = LLMClient()
        self.db = DatabaseClient()
        self.safety = SafetyGuardrails()
        self.hallucination = HallucinationControls()
        self.memory_retrieval = MemoryRetrieval(self.db)
        self.memory_summarizer = MemorySummarizer(self.llm)
        self.cost_opt = CostOptimizer()
        self.cache = ResponseCache()
        self.monitor = MonitoringClient()
        
    async def process_message(self, user_id: UUID, message: str, session_id: str) -> str:
        start_time = time.time()
        risk_level = "UNKNOWN"
        model_used = "NONE"
        
        try:
            # 1. Input Validation & Budget Check
            if not self.cost_opt.check_budget(str(user_id)):
                return "I'm sorry, I cannot process your request at this time due to usage limits."

            # 2. Layer 1 Safety: Input Risk
            input_safety = self.safety.detect_input_risk(message)
            if not input_safety["is_safe"]:
                response = self.safety.get_hard_refusal(input_safety["risk_type"])
                if input_safety["risk_type"] == "CRISIS":
                    self.monitor.alert_crisis(str(user_id), message)
                    await self.db.log_crisis_event(user_id, message)
                return response

            # 3. Safety Classification
            classification = await self.llm.classify_text(
                message, 
                prompts.get_classification_prompt(message)
            )
            risk_level = classification.get("risk_level", "MEDIUM_RISK")
            
            # 4. Model Routing
            model_name = ModelRouter.get_model_for_risk_level(risk_level)
            model_used = model_name

            # 5. Retrieval
            context = await self.memory_retrieval.get_context(user_id, session_id)

            # 6. Cache Check (Low risk only)
            if risk_level == "LOW_RISK":
                # specific caching logic usually involves hashing prompt + context
                # simplified here to message hash for demo
                msg_hash = str(hash(message + context))
                cached = await self.cache.get_cached_response(msg_hash)
                if cached:
                    logger.info("Cache hit")
                    return cached

            # 7. Select Prompt Variant
            system_prompt = prompts.get_system_prompt()
            user_prompt = prompts.get_response_prompt(risk_level, message, context)
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]

            # 8. Generation
            # Token budget adjustment could happen here
            response_text = await self.llm.generate_response(
                model=model_name,
                messages=messages,
                max_tokens=300 # Strict output limit
            )

            # 9. Layer 2 Safety: Output Validation
            is_valid, reason = self.safety.validate_response(response_text)
            if not is_valid:
                logger.warning(f"Response blocked by Layer 2: {reason}")
                return "I apologize, but I frame my response poorly. Let me try again." # Simplified retry logic

            # 10. Hallucination Control
            final_response = self.hallucination.enforce_epistemic_humility(response_text)

            # 11. Async Memory Update
            # We fire and forget the summary update to reduce latency
            asyncio.create_task(self._async_memory_update(user_id, message, final_response))

            # 12. Cache Update
            if risk_level == "LOW_RISK":
                 await self.cache.cache_response(msg_hash, final_response, risk_level)

            return final_response

        except Exception as e:
            import traceback
            logger.error(f"Orchestrator error: {e}")
            traceback.print_exc()
            self.monitor.log_error("Orchestrator", str(e))
            return "I am currently experiencing technical difficulties. Please try again later."
            
        finally:
            latency = (time.time() - start_time) * 1000
            self.monitor.log_request(latency, risk_level, model_used)

    async def _async_memory_update(self, user_id: UUID, user_msg: str, bot_msg: str):
        """
        Background task to summarize and update DB.
        """
        # Ideally fetch recent history from DB to append
        # Here we just treat single turn for the summarizer demo
        history = [
            {"role": "user", "content": user_msg},
            {"role": "assistant", "content": bot_msg}
        ]
        
        summary = await self.memory_summarizer.generate_summary(history)
        if summary:
            await self.db.update_user_memory(
                user_id=user_id,
                relationship_context=summary.get("1", {}), # Indexing based on prompt requirement
                recurring_themes=summary.get("2", {}),
                emotional_patterns=summary.get("3", {}),
                new_progress_note=summary.get("4", "")
            )
