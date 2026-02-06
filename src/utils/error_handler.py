"""Error handling and logging infrastructure"""

import logging
from typing import Optional, Dict, Any
from enum import Enum


class ErrorCode(Enum):
    """Error codes for different error types"""
    MCP_SERVER_ERROR = "MCP_SERVER_ERROR"
    RATE_LIMIT_ERROR = "RATE_LIMIT_ERROR"
    DATABASE_ERROR = "DATABASE_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    NETWORK_ERROR = "NETWORK_ERROR"
    UNKNOWN_ERROR = "UNKNOWN_ERROR"


class ChimeraError(Exception):
    """Base exception for Project Chimera"""
    
    def __init__(
        self,
        message: str,
        error_code: ErrorCode = ErrorCode.UNKNOWN_ERROR,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)


class MCPServerError(ChimeraError):
    """Error communicating with MCP server"""
    
    def __init__(self, message: str, server_name: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message,
            ErrorCode.MCP_SERVER_ERROR,
            {"server_name": server_name, **(details or {})}
        )


class RateLimitError(ChimeraError):
    """Rate limit exceeded"""
    
    def __init__(self, message: str, platform: str, retry_after: Optional[int] = None):
        super().__init__(
            message,
            ErrorCode.RATE_LIMIT_ERROR,
            {"platform": platform, "retry_after": retry_after}
        )


class DatabaseError(ChimeraError):
    """Database operation error"""
    
    def __init__(self, message: str, operation: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message,
            ErrorCode.DATABASE_ERROR,
            {"operation": operation, **(details or {})}
        )


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """Setup application logging"""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    return logging.getLogger("chimera")
