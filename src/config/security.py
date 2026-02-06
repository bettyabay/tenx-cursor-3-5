"""Security configuration and secrets management for Project Chimera"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from functools import lru_cache


class SecuritySettings(BaseSettings):
    """Security-related settings loaded from environment variables"""
    
    # Secret keys (should be generated securely in production)
    secret_key: str = Field(
        default="change-this-in-production",
        description="Secret key for cryptographic operations"
    )
    jwt_secret_key: str = Field(
        default="change-this-in-production",
        description="JWT signing secret"
    )
    jwt_algorithm: str = Field(default="HS256", description="JWT algorithm")
    jwt_expiration_hours: int = Field(default=24, description="JWT token expiration")
    
    # API Keys (should be managed via MCP in production)
    # These are placeholders - actual keys should come from MCP servers
    twitter_api_key: Optional[str] = None
    twitter_api_secret: Optional[str] = None
    twitter_bearer_token: Optional[str] = None
    
    tiktok_api_key: Optional[str] = None
    tiktok_api_secret: Optional[str] = None
    
    instagram_api_key: Optional[str] = None
    instagram_api_secret: Optional[str] = None
    
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    
    # CORS settings
    allowed_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        description="Allowed CORS origins"
    )
    enable_cors: bool = Field(default=True, description="Enable CORS")
    
    # Rate limiting
    rate_limit_enabled: bool = Field(default=True, description="Enable rate limiting")
    rate_limit_requests_per_minute: int = Field(
        default=60,
        description="Requests per minute limit"
    )
    
    # Security headers
    enable_security_headers: bool = Field(
        default=True,
        description="Enable security headers"
    )
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    @field_validator("secret_key", "jwt_secret_key")
    @classmethod
    def validate_secret_keys(cls, v: str) -> str:
        """Validate that secret keys are not default values in production"""
        if os.getenv("ENVIRONMENT") == "production":
            if v in ["change-this-in-production", ""]:
                raise ValueError(
                    "Secret keys must be set to secure values in production"
                )
        return v
    
    @field_validator("allowed_origins")
    @classmethod
    def validate_origins(cls, v: List[str]) -> List[str]:
        """Validate CORS origins"""
        if not isinstance(v, list):
            return ["http://localhost:3000"]
        return v


@lru_cache()
def get_security_settings() -> SecuritySettings:
    """Get cached security settings instance"""
    return SecuritySettings()


class SecretsManager:
    """Manages secrets via MCP servers (preferred) or environment variables"""
    
    def __init__(self):
        self._mcp_enabled = os.getenv("MCP_SENSE_ENABLED", "true").lower() == "true"
        self._settings = get_security_settings()
    
    def get_api_key(self, service: str, key_type: str = "api_key") -> Optional[str]:
        """
        Get API key for a service.
        Prefers MCP servers, falls back to environment variables.
        
        Args:
            service: Service name (twitter, tiktok, instagram, openai, etc.)
            key_type: Type of key (api_key, api_secret, bearer_token)
        
        Returns:
            API key or None if not found
        """
        # TODO: Implement MCP server lookup
        # For now, fall back to environment variables
        env_key = f"{service.upper()}_{key_type.upper()}"
        return os.getenv(env_key) or getattr(self._settings, f"{service}_{key_type}", None)
    
    def get_secret_key(self) -> str:
        """Get application secret key"""
        return self._settings.secret_key
    
    def get_jwt_secret(self) -> str:
        """Get JWT secret key"""
        return self._settings.jwt_secret_key
    
    def validate_secrets(self) -> dict:
        """
        Validate that required secrets are present.
        
        Returns:
            Dictionary with validation results
        """
        results = {
            "valid": True,
            "missing": [],
            "warnings": []
        }
        
        # Check secret keys
        if self._settings.secret_key == "change-this-in-production":
            results["warnings"].append("SECRET_KEY is using default value")
        
        if self._settings.jwt_secret_key == "change-this-in-production":
            results["warnings"].append("JWT_SECRET_KEY is using default value")
        
        # Check if MCP is enabled
        if not self._mcp_enabled:
            results["warnings"].append("MCP Sense is disabled - secrets not managed via MCP")
        
        return results


# Global secrets manager instance
secrets_manager = SecretsManager()
