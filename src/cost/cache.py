import json
import logging
from typing import Optional
import redis.asyncio as redis # type: ignore

from config.settings import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

class ResponseCache:
    def __init__(self):
        self.redis = redis.from_url(settings.REDIS_URL, decode_responses=True)

    async def get_cached_response(self, prompt_hash: str) -> Optional[str]:
        try:
            return await self.redis.get(f"resp:{prompt_hash}")
        except Exception:
            # Fail open if cache is down
            return None

    async def cache_response(self, prompt_hash: str, response: str, risk_level: str):
        """
        Cache rules:
        - LOW_RISK: Cache for 1 hour (common general advice)
        - MEDIUM/HIGH/CRISIS: DO NOT CACHE (Unique context matters)
        """
        if risk_level == "LOW_RISK":
            try:
                # 1 hour TTL
                await self.redis.setex(f"resp:{prompt_hash}", 3600, response)
            except Exception as e:
                logger.warning(f"Failed to cache response: {e}")

    async def close(self):
        await self.redis.close()
