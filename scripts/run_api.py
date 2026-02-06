#!/usr/bin/env python3
"""Run the FastAPI application"""

import uvicorn
from src.api import app

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload in development
        log_level="info"
    )
