from typing import List, Dict, Any
from src.database.client import DatabaseClient

class MemoryRetrieval:
    def __init__(self, db_client: DatabaseClient):
        self.db = db_client

    async def get_context(self, user_id, session_id: str) -> str:
        """
        Constructs a context string from user memory for the LLM.
        Budgets tokens to ~500.
        """
        memory = await self.db.get_user_memory(user_id)
        if not memory:
            return ""

        # Format context
        # We prioritize: 
        # 1. Immediate relationship context
        # 2. Recent progress notes
        # 3. Recurring themes
        
        context_parts = []
        
        # 1. Context
        rel_ctx = memory.get("relationship_context", {})
        if rel_ctx:
            context_parts.append(f"Relationship Context: {rel_ctx}")

        # 2. Themes
        themes = memory.get("recurring_themes", {})
        if themes:
            context_parts.append(f"Recurring Themes: {themes}")

        # 3. Notes (Last 3 only to save tokens)
        notes = memory.get("progress_notes", [])
        if notes:
            recent_notes = notes[-3:]
            context_parts.append(f"Recent Progress: {'; '.join(recent_notes)}")
            
        return "\n".join(context_parts)
