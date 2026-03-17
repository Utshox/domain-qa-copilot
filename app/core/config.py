from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Domain Q&A Copilot"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "REPLACE_ME"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # Databases
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/domain_qa"
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION: str = "documents"

    # Observability
    PHOENIX_HOST: str = "localhost"
    PHOENIX_PORT: int = 6006
    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_API_KEY: Optional[str] = None
    LANGCHAIN_PROJECT: str = "domain-qa-copilot"

    # OpenAI
    OPENAI_API_KEY: Optional[str] = None

    # Google Cloud
    GOOGLE_CLOUD_PROJECT: Optional[str] = None

    # App Config
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()
