import logging
import tiktoken
from config.settings import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

class CostOptimizer:
    def __init__(self):
        self.enc = tiktoken.get_encoding("cl100k_base")
        # In memory tracker for demo purposes. In production, use Redis.
        self._daily_usage = 0 

    def estimate_tokens(self, text: str) -> int:
        return len(self.enc.encode(text))

    def check_budget(self, user_id: str) -> bool:
        """
        Check if system-wide or user-specific budget is exceeded.
        """
        if self._daily_usage > settings.TOKEN_BUDGET_PER_DAY:
            logger.warning("Daily token budget exceeded!")
            # In a real app, we might switch to cheapest model ONLY or stop.
            # For this counseling app, we might degrade to 'unavailable' if strict budget.
            return False
        return True

    def track_usage(self, input_tokens: int, output_tokens: int):
        total = input_tokens + output_tokens
        self._daily_usage += total
