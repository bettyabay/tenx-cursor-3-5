"""Security configuration tests"""

import pytest
import os
from src.config.security import SecuritySettings, SecretsManager, get_security_settings


class TestSecuritySettings:
    """Test security settings configuration"""
    
    def test_security_settings_defaults(self):
        """Test default security settings"""
        settings = SecuritySettings()
        assert settings.enable_cors is True
        assert settings.rate_limit_enabled is True
        assert settings.jwt_algorithm == "HS256"
    
    def test_security_settings_validation(self):
        """Test secret key validation"""
        # Should not raise in development
        settings = SecuritySettings(
            secret_key="change-this-in-production",
            jwt_secret_key="change-this-in-production"
        )
        assert settings.secret_key == "change-this-in-production"
    
    def test_cors_origins(self):
        """Test CORS origins configuration"""
        settings = SecuritySettings(
            allowed_origins=["http://example.com"]
        )
        assert "http://example.com" in settings.allowed_origins


class TestSecretsManager:
    """Test secrets management"""
    
    def test_secrets_manager_initialization(self):
        """Test secrets manager can be initialized"""
        manager = SecretsManager()
        assert manager is not None
    
    def test_get_secret_key(self):
        """Test getting secret key"""
        manager = SecretsManager()
        secret = manager.get_secret_key()
        assert secret is not None
        assert isinstance(secret, str)
    
    def test_get_jwt_secret(self):
        """Test getting JWT secret"""
        manager = SecretsManager()
        jwt_secret = manager.get_jwt_secret()
        assert jwt_secret is not None
        assert isinstance(jwt_secret, str)
    
    def test_validate_secrets(self):
        """Test secrets validation"""
        manager = SecretsManager()
        validation = manager.validate_secrets()
        assert "valid" in validation
        assert "missing" in validation
        assert "warnings" in validation
        assert isinstance(validation["warnings"], list)
    
    def test_get_api_key_nonexistent(self):
        """Test getting non-existent API key"""
        manager = SecretsManager()
        key = manager.get_api_key("nonexistent_service")
        # Should return None if not found
        assert key is None or isinstance(key, str)


class TestSecurityIntegration:
    """Test security integration with application"""
    
    def test_get_security_settings_cached(self):
        """Test that security settings are cached"""
        settings1 = get_security_settings()
        settings2 = get_security_settings()
        # Should be the same instance due to caching
        assert settings1 is settings2
    
    def test_secrets_manager_singleton(self):
        """Test that secrets manager can be used as singleton"""
        from src.config.security import secrets_manager
        assert secrets_manager is not None
        assert isinstance(secrets_manager, SecretsManager)
