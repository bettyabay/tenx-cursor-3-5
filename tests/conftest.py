"""Pytest configuration and fixtures"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from typing import Generator

from src.models import Base
from src.config.settings import settings


@pytest.fixture(scope="function")
def db_engine():
    """Create in-memory SQLite database for testing"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(db_engine) -> Generator[Session, None, None]:
    """Create database session for testing"""
    SessionLocal = sessionmaker(bind=db_engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def sample_trend_data():
    """Sample trend data for testing"""
    return {
        "topic_name": "AI Agents",
        "platform": "twitter",
        "engagement_metrics": {
            "likes": 15000,
            "shares": 3200,
            "comments": 890,
            "views": 125000
        },
        "trend_velocity": 245.5,
        "relevance_score": 0.85,
        "related_hashtags": ["#AIAgents", "#MachineLearning"],
        "platform_trend_id": "twitter_trend_12345"
    }


@pytest.fixture
def sample_platform_connection_data():
    """Sample platform connection data for testing"""
    return {
        "platform_name": "twitter",
        "connection_status": "connected",
        "rate_limit_status": {
            "remaining_requests": 100,
            "reset_timestamp": "2026-02-05T12:00:00Z",
            "limit_per_window": 300
        }
    }


@pytest.fixture
def mock_mcp_client():
    """Mock MCP client for testing"""
    class MockMCPClient:
        def __init__(self):
            self.calls = []
        
        async def call_tool(self, tool_name: str, **kwargs):
            self.calls.append({"tool": tool_name, "kwargs": kwargs})
            return {"status": "success", "data": {}}
        
        def get_logs(self):
            return self.calls
    
    return MockMCPClient()


@pytest.fixture
def api_client():
    """FastAPI test client"""
    from fastapi.testclient import TestClient
    from src.api import app
    
    return TestClient(app)
