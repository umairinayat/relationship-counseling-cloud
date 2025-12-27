import asyncpg
import json
import logging
from typing import Optional, Dict, Any, List
from uuid import UUID
from datetime import datetime

from config.settings import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

class DatabaseClient:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        if not self.pool:
            try:
                self.pool = await asyncpg.create_pool(
                    dsn=settings.DATABASE_URL,
                    min_size=2,
                    max_size=10
                )
                logger.info("Connected to Database")
            except Exception as e:
                logger.error(f"Database connection failed: {e}")
                raise

    async def close(self):
        if self.pool:
            await self.pool.close()

    async def get_user_memory(self, user_id: UUID) -> Optional[Dict[str, Any]]:
        """Retrieve user memory summaries."""
        if not self.pool:
            await self.connect()
            
        row = await self.pool.fetchrow(
            """
            SELECT * FROM user_memory WHERE user_id = $1
            """,
            user_id
        )
        return dict(row) if row else None

    async def create_user_memory(self, user_id: UUID):
        """Initialize a new user record."""
        if not self.pool:
            await self.connect()
            
        await self.pool.execute(
            """
            INSERT INTO user_memory (user_id) 
            VALUES ($1) 
            ON CONFLICT (user_id) DO NOTHING
            """,
            user_id
        )

    async def update_user_memory(
        self, 
        user_id: UUID, 
        relationship_context: Optional[dict] = None,
        recurring_themes: Optional[dict] = None,
        emotional_patterns: Optional[dict] = None,
        new_progress_note: Optional[str] = None
    ):
        """
        Update memory fields safely.
        """
        if not self.pool:
            await self.connect()
            
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                # 1. Update JSON fields if provided
                if relationship_context:
                    await conn.execute(
                        "UPDATE user_memory SET relationship_context = $2, updated_at = NOW() WHERE user_id = $1",
                        user_id, json.dumps(relationship_context) # asyncpg handles dict to jsonb auto? usually needs json.dumps or type codec
                    )
                
                if recurring_themes:
                    await conn.execute(
                        "UPDATE user_memory SET recurring_themes = $2, updated_at = NOW() WHERE user_id = $1",
                        user_id, json.dumps(recurring_themes)
                    )
                    
                if emotional_patterns:
                    await conn.execute(
                        "UPDATE user_memory SET emotional_patterns = $2, updated_at = NOW() WHERE user_id = $1",
                        user_id, json.dumps(emotional_patterns)
                    )
                
                # 2. Append progress note (sliding window logic done in DB or App? Doing simple append here)
                if new_progress_note:
                    # Enforce max 10 via array slicing in update
                    await conn.execute(
                        """
                        UPDATE user_memory 
                        SET progress_notes = (progress_notes || $2)[1:10], 
                            updated_at = NOW() 
                        WHERE user_id = $1
                        """,
                        user_id, new_progress_note
                    )
                
                # 3. Log Audit
                await conn.execute(
                    """
                    INSERT INTO memory_audit_log (user_id, action, details)
                    VALUES ($1, 'UPDATE', $2)
                    """,
                    user_id, json.dumps({"updated_fields": list(filter(None, [
                        "relationship_context" if relationship_context else None,
                        "recurring_themes" if recurring_themes else None,
                        "progress_notes" if new_progress_note else None
                    ]))})
                )

    async def log_crisis_event(self, user_id: UUID, details: str):
        if not self.pool:
            await self.connect()
            
        await self.pool.execute(
            """
            INSERT INTO memory_audit_log (user_id, action, details)
            VALUES ($1, 'CRISIS_ALERT', $2)
            """,
            user_id, json.dumps({"note": details})
        )
