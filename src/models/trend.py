"""Trend model - represents trending topics from social media platforms"""

from sqlalchemy import Column, String, Float, DateTime, JSON, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from enum import Enum

from . import Base


class Platform(str, Enum):
    """Supported social media platforms"""
    TWITTER = "twitter"
    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"


class Trend(Base):
    """Trend entity - represents a trending topic"""
    
    __tablename__ = "trends"
    
    trend_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    topic_name = Column(String(500), nullable=False)
    platform = Column(SQLEnum(Platform), nullable=False)
    engagement_metrics = Column(JSON, nullable=False)  # {likes, shares, comments, views?}
    trend_velocity = Column(Float, nullable=False)  # Rate of growth (posts per hour)
    timestamp = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    relevance_score = Column(Float)  # 0.0-1.0, calculated
    related_hashtags = Column(JSON)  # Array of strings
    platform_trend_id = Column(String, nullable=False)  # Platform-specific identifier
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Trend(trend_id={self.trend_id}, topic_name={self.topic_name}, platform={self.platform.value})>"
