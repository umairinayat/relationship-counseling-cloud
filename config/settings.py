from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    """Global application settings."""
    
    # Environment
    ENV: str = "development"
    DEBUG: bool = True
    
    # LLM (OpenAI / Groq)
    OPENAI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    
    # Database (PostgreSQL)
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/relationship_ai"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Safety Thresholds
    MAX_DAILY_CONVERSATIONS: int = 50
    TOKEN_BUDGET_PER_DAY: int = 100000
    
    # Model Configs
    MODEL_CRISIS: str = "gpt-4o"
    MODEL_HIGH_RISK: str = "gpt-4o"
    MODEL_MEDIUM_RISK: str = "gpt-4o-mini"
    MODEL_LOW_RISK: str = "gpt-4o-mini"
    
    # Flask Web Config
    FLASK_SECRET_KEY: str = "dev-secret-key-change-in-prod"
    PORT: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()
