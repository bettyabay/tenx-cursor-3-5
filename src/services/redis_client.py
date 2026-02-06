"""Redis connection and client configuration"""

import redis
from typing import Optional
import logging

logger = logging.getLogger("chimera.redis")


class RedisClient:
    """Redis client wrapper"""
    
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.client: Optional[redis.Redis] = None
    
    def connect(self) -> None:
        """Connect to Redis"""
        try:
            self.client = redis.from_url(self.redis_url, decode_responses=True)
            # Test connection
            self.client.ping()
            logger.info("Redis connection established")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise
    
    def disconnect(self) -> None:
        """Disconnect from Redis"""
        if self.client:
            self.client.close()
            logger.info("Redis connection closed")
    
    def get_client(self) -> redis.Redis:
        """Get Redis client instance"""
        if not self.client:
            self.connect()
        return self.client
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
