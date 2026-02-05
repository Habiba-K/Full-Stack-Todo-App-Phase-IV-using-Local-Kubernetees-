from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Attributes:
        database_url: PostgreSQL connection string for Neon database
        groq_api_key: Groq API key for agent orchestration
        groq_model: Model to use for the agent (default: llama-3.3-70b-versatile)
        chat_context_messages: Number of recent messages to load for agent context (default: 50)
    """
    database_url: str
    groq_api_key: str
    groq_model: str = "llama-3.3-70b-versatile"
    chat_context_messages: int = 50

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields in .env file


settings = Settings()
