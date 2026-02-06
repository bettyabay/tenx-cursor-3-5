"""PlatformConnection model - represents connection status to social media platforms"""

from sqlalchemy import Column, String, DateTime, JSON, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from enum import Enum

from . import Base
from .trend import Platform


class ConnectionStatus(str, Enum):
    """Platform connection status"""
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    RATE_LIMITED = "rate_limited"


class PlatformConnection(Base):
    """PlatformConnection entity - represents connection to social media platform"""
    
    __tablename__ = "platform_connections"
    
    connection_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    platform_name = Column(SQLEnum(Platform), nullable=False, unique=True)
    connection_status = Column(SQLEnum(ConnectionStatus), nullable=False)
    rate_limit_status = Column(JSON, nullable=False)  # {remaining_requests, reset_timestamp, limit_per_window}
    last_sync_timestamp = Column(DateTime(timezone=True))
    last_error = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        UniqueConstraint('platform_name', name='uq_platform_connection_platform_name'),
    )
    
    def __repr__(self):
        return f"<PlatformConnection(platform_name={self.platform_name.value}, status={self.connection_status.value})>"
