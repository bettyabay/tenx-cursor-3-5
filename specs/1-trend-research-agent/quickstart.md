# Quickstart: Trend Research Agent

**Date**: 2026-02-05  
**Feature**: Trend Research Agent

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- PostgreSQL 14+
- Redis 7+
- Weaviate (vector database)

## Setup

1. **Clone and navigate to project**:
   ```bash
   cd Project-Chimera
   ```

2. **Create virtual environment**:
   ```bash
   uv sync
   source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
   ```

3. **Start infrastructure services**:
   ```bash
   docker-compose up -d postgres redis weaviate
   ```

4. **Run database migrations**:
   ```bash
   alembic upgrade head
   ```

5. **Start MCP servers** (in separate terminals):
   ```bash
   # Terminal 1: Twitter MCP Server
   python -m mcp_servers.twitter.server

   # Terminal 2: TikTok MCP Server
   python -m mcp_servers.tiktok.server

   # Terminal 3: Instagram MCP Server
   python -m mcp_servers.instagram.server
   ```

6. **Start Trend Research Agent**:
   ```bash
   python -m agents.trend_research.agent
   ```

## Environment Variables

Create `.env` file:
```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/chimera

# Redis
REDIS_URL=redis://localhost:6379/0

# Weaviate
WEAVIATE_URL=http://localhost:8080

# MCP Servers
MCP_TWITTER_URL=mcp://localhost:8001
MCP_TIKTOK_URL=mcp://localhost:8002
MCP_INSTAGRAM_URL=mcp://localhost:8003

# MCP Sense (Tenx)
MCP_SENSE_ENABLED=true
MCP_SENSE_SESSION_ID=your-session-id
```

## Running Tests

```bash
# All tests
pytest

# Unit tests only
pytest tests/unit/

# Integration tests
pytest tests/integration/

# Contract tests
pytest tests/contract/
```

## Usage Example

```python
from agents.trend_research import TrendResearchAgent

# Initialize agent
agent = TrendResearchAgent(agent_niche="technology")

# Discover trends
trends = await agent.discover_trends(platforms=["twitter", "tiktok"])

# Filter by relevance
relevant_trends = [t for t in trends if t.relevance_score >= 0.7]

# Get detailed analysis
analysis = await agent.analyze_trend(relevant_trends[0].trend_id)

# Store trends
await agent.store_trends(relevant_trends)
```

## Verification

Run verification script:
```bash
python scripts/verify_trend_research.py
```

This verifies:
- ✅ MCP servers are accessible
- ✅ Database connections work
- ✅ Skills can calculate relevance scores
- ✅ Trend storage and retrieval function
- ✅ MCP Sense logging is active

## Troubleshooting

**MCP servers not connecting**: Check MCP_SERVER_URLs in .env match running servers

**Database errors**: Ensure PostgreSQL is running and migrations applied

**Rate limit errors**: Check rate limit status via PlatformConnection entity

**Vector similarity errors**: Ensure Weaviate is running and schema created
