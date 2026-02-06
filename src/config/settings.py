"""Environment configuration management using pydantic-settings"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database
    database_url: str = "postgresql://chimera:chimera_dev@localhost:5432/chimera"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # Weaviate
    weaviate_url: str = "http://localhost:8080"
    
    # MCP Servers
    mcp_twitter_url: str = "mcp://localhost:8001"
    mcp_tiktok_url: str = "mcp://localhost:8002"
    mcp_instagram_url: str = "mcp://localhost:8003"
    
    # MCP Sense (Tenx)
    mcp_sense_enabled: bool = True
    mcp_sense_session_id: Optional[str] = None
    
    # Logging
    log_level: str = "INFO"
    
    # Agent Configuration
    agent_niche: str = "technology"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


# Global settings instance
settings = Settings()
