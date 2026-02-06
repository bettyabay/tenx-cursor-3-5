"""MCP Sense logging integration for traceability (FR-010 requirement)"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger("chimera.mcp_sense")


class MCPSenseLogger:
    """Logger for MCP Sense telemetry"""
    
    def __init__(self, enabled: bool = True, session_id: Optional[str] = None):
        self.enabled = enabled
        self.session_id = session_id
        self._logger = logging.getLogger("chimera.mcp_sense")
    
    def log_activity(
        self,
        activity_type: str,
        component: str,
        details: Optional[Dict[str, Any]] = None,
        trace_id: Optional[str] = None
    ) -> None:
        """Log activity to MCP Sense"""
        if not self.enabled:
            return
        
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "session_id": self.session_id,
            "trace_id": trace_id,
            "activity_type": activity_type,
            "component": component,
            "details": details or {}
        }
        
        # Log in structured format for MCP Sense
        self._logger.info(
            f"MCP_SENSE: {activity_type} | {component} | {trace_id or 'N/A'}",
            extra={"mcp_sense": log_entry}
        )
    
    def log_trend_discovery(
        self,
        platform: str,
        trends_found: int,
        trace_id: Optional[str] = None
    ) -> None:
        """Log trend discovery activity"""
        self.log_activity(
            "trend_discovery",
            "trend_research_agent",
            {"platform": platform, "trends_found": trends_found},
            trace_id
        )
    
    def log_relevance_scoring(
        self,
        trends_scored: int,
        avg_relevance: float,
        trace_id: Optional[str] = None
    ) -> None:
        """Log relevance scoring activity"""
        self.log_activity(
            "relevance_scoring",
            "relevance_scorer",
            {"trends_scored": trends_scored, "avg_relevance": avg_relevance},
            trace_id
        )
    
    def log_trend_storage(
        self,
        trends_stored: int,
        trace_id: Optional[str] = None
    ) -> None:
        """Log trend storage activity"""
        self.log_activity(
            "trend_storage",
            "trend_storage_service",
            {"trends_stored": trends_stored},
            trace_id
        )


# Global MCP Sense logger instance
# Will be initialized with settings when config is loaded
mcp_sense_logger: Optional[MCPSenseLogger] = None
