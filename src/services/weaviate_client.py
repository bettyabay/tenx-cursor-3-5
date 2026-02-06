"""Weaviate connection and client configuration"""

import weaviate
from typing import Optional
import logging

logger = logging.getLogger("chimera.weaviate")


class WeaviateClient:
    """Weaviate client wrapper"""
    
    def __init__(self, weaviate_url: str):
        self.weaviate_url = weaviate_url
        self.client: Optional[weaviate.Client] = None
    
    def connect(self) -> None:
        """Connect to Weaviate"""
        try:
            self.client = weaviate.Client(url=self.weaviate_url)
            # Test connection
            self.client.is_ready()
            logger.info("Weaviate connection established")
        except Exception as e:
            logger.error(f"Failed to connect to Weaviate: {e}")
            raise
    
    def disconnect(self) -> None:
        """Disconnect from Weaviate"""
        # Weaviate client doesn't have explicit close method
        self.client = None
        logger.info("Weaviate connection closed")
    
    def get_client(self) -> weaviate.Client:
        """Get Weaviate client instance"""
        if not self.client:
            self.connect()
        return self.client
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
