"""API endpoint tests"""

import pytest
from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)


class TestHealthEndpoints:
    """Test health check endpoints"""
    
    def test_health_check(self):
        """Test main health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "version" in data
    
    def test_v1_health_check(self):
        """Test v1 health check endpoint"""
        response = client.get("/api/v1/health/")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "services" in data
    
    def test_readiness_check(self):
        """Test readiness check endpoint"""
        response = client.get("/api/v1/health/ready")
        # May return 200 or 503 depending on database
        assert response.status_code in [200, 503]
    
    def test_liveness_check(self):
        """Test liveness check endpoint"""
        response = client.get("/api/v1/health/live")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "alive"


class TestTrendsEndpoints:
    """Test trends API endpoints"""
    
    def test_get_trends_empty(self):
        """Test getting trends (currently returns empty)"""
        response = client.get("/api/v1/trends/")
        assert response.status_code == 200
        data = response.json()
        assert "trends" in data
        assert "total" in data
        assert isinstance(data["trends"], list)
    
    def test_get_trends_with_filters(self):
        """Test getting trends with query parameters"""
        response = client.get(
            "/api/v1/trends/",
            params={
                "platforms": "twitter,tiktok",
                "min_relevance": 0.7,
                "limit": 20
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "trends" in data
    
    def test_get_trend_not_found(self):
        """Test getting non-existent trend"""
        response = client.get("/api/v1/trends/non-existent-id")
        assert response.status_code == 404
    
    def test_get_platform_trends(self):
        """Test getting trends for a specific platform"""
        response = client.get("/api/v1/trends/platforms/twitter/trends")
        assert response.status_code == 200
        data = response.json()
        assert "trends" in data
        assert "platforms" in data
    
    def test_get_platform_trends_invalid_platform(self):
        """Test getting trends for invalid platform"""
        response = client.get("/api/v1/trends/platforms/invalid/trends")
        assert response.status_code == 400
    
    def test_get_platform_status(self):
        """Test getting platform connection status"""
        response = client.get("/api/v1/trends/platforms/status")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestAgentsEndpoints:
    """Test agents API endpoints"""
    
    def test_list_agents(self):
        """Test listing agents"""
        response = client.get("/api/v1/agents/")
        assert response.status_code == 200
        data = response.json()
        assert "agents" in data
        assert "total" in data
    
    def test_get_agent_not_found(self):
        """Test getting non-existent agent"""
        response = client.get("/api/v1/agents/non-existent-id")
        assert response.status_code == 404
    
    def test_agent_heartbeat(self):
        """Test agent heartbeat endpoint"""
        response = client.post("/api/v1/agents/test-agent-id/heartbeat")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "timestamp" in data


class TestAPIDocumentation:
    """Test API documentation endpoints"""
    
    def test_openapi_schema(self):
        """Test OpenAPI schema endpoint"""
        response = client.get("/api/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data
    
    def test_docs_endpoint(self):
        """Test Swagger UI endpoint"""
        response = client.get("/api/docs")
        assert response.status_code == 200
    
    def test_redoc_endpoint(self):
        """Test ReDoc endpoint"""
        response = client.get("/api/redoc")
        assert response.status_code == 200
