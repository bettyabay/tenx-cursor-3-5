"""MCP client infrastructure for connecting to MCP servers"""

from typing import Dict, Optional, Any
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger("chimera.mcp_client")


class MCPClient(ABC):
    """Abstract base class for MCP clients"""
    
    @abstractmethod
    def connect(self) -> None:
        """Connect to MCP server"""
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect from MCP server"""
        pass
    
    @abstractmethod
    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call MCP tool"""
        pass
    
    @abstractmethod
    def get_resource(self, resource_name: str) -> Dict[str, Any]:
        """Get MCP resource"""
        pass


class MCPClientManager:
    """Manages connections to multiple MCP servers"""
    
    def __init__(self):
        self.clients: Dict[str, MCPClient] = {}
        self.server_urls: Dict[str, str] = {}
    
    def register_server(self, name: str, url: str, client: MCPClient) -> None:
        """Register an MCP server"""
        self.server_urls[name] = url
        self.clients[name] = client
        logger.info(f"Registered MCP server: {name} at {url}")
    
    def get_client(self, server_name: str) -> MCPClient:
        """Get MCP client for a server"""
        if server_name not in self.clients:
            raise ValueError(f"MCP server '{server_name}' not registered")
        return self.clients[server_name]
    
    def connect_all(self) -> None:
        """Connect to all registered servers"""
        for name, client in self.clients.items():
            try:
                client.connect()
                logger.info(f"Connected to MCP server: {name}")
            except Exception as e:
                logger.error(f"Failed to connect to MCP server {name}: {e}")
                raise
    
    def disconnect_all(self) -> None:
        """Disconnect from all servers"""
        for name, client in self.clients.items():
            try:
                client.disconnect()
                logger.info(f"Disconnected from MCP server: {name}")
            except Exception as e:
                logger.error(f"Error disconnecting from MCP server {name}: {e}")


# Global MCP client manager
mcp_client_manager = MCPClientManager()
