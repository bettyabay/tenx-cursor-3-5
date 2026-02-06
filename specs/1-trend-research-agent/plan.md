# Implementation Plan: Trend Research Agent

**Branch**: `1-trend-research-agent` | **Date**: 2026-02-05 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/1-trend-research-agent/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

The Trend Research Agent enables autonomous influencer agents to discover, analyze, and store trending topics across multiple social media platforms (Twitter/X, TikTok, Instagram). The system uses MCP servers for platform access, Skills for reusable analysis capabilities, and provides relevance scoring to filter trends by agent niche. Technical approach: MCP-first architecture with Skills separation, PostgreSQL for trend storage, and MCP Sense for full traceability.

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: FastAPI, pydantic, requests, sqlalchemy, tenacity (retry logic), MCP SDK  
**Storage**: PostgreSQL (trend data), Redis (caching, rate limit tracking), Weaviate (vector similarity for relevance scoring)  
**Testing**: pytest, pytest-asyncio, pytest-mock  
**Target Platform**: Linux server (containerized with Docker)  
**Project Type**: Single project (backend service)  
**Performance Goals**: Discover trends from 3 platforms within 5 minutes, retrieve historical trends within 2 seconds for 30-day ranges  
**Constraints**: MCP-First architecture (no direct API calls), Skills vs MCP Tools separation, TDD workflow, Docker containerization, CI/CD with AI governance  
**Scale/Scope**: Support 1000+ agents, handle API rate limits gracefully, process trends from 3+ platforms simultaneously

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ Spec-Driven Development
- Specification exists and is ratified: `specs/1-trend-research-agent/spec.md`
- All requirements traceable to spec

### ✅ Test-Driven Development
- Failing tests will be written before implementation
- Test structure defined in spec acceptance scenarios

### ✅ MCP-First Architecture
- All platform access via MCP servers (FR-007)
- No direct API calls to social media platforms
- MCP servers: `mcp-server-twitter`, `mcp-server-tiktok`, `mcp-server-instagram`

### ✅ Skills vs MCP Tools Separation
- Skills: `skill_calculate_relevance_score`, `skill_aggregate_trends`, `skill_analyze_trend_velocity`
- MCP Tools: Platform access via MCP servers (external bridges)

### ✅ MCP Traceability
- All activities logged via MCP Sense (FR-010)
- Full traceability from discovery to storage

### ✅ Containerization & CI/CD
- Docker containerization required
- CI/CD pipeline with AI governance

**Status**: ✅ All gates pass. Ready for Phase 0 research.

## Project Structure

### Documentation (this feature)

```text
specs/1-trend-research-agent/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
src/
├── agents/
│   └── trend_research/
│       ├── __init__.py
│       ├── agent.py              # Main trend research agent
│       └── orchestrator.py       # Coordinates platform queries
├── skills/
│   └── trend_analysis/
│       ├── __init__.py
│       ├── relevance_scorer.py   # Calculate relevance scores
│       ├── trend_aggregator.py   # Cross-platform aggregation
│       └── velocity_calculator.py # Trend velocity analysis
├── mcp_servers/
│   ├── twitter/
│   │   ├── __init__.py
│   │   └── server.py             # Twitter MCP server
│   ├── tiktok/
│   │   ├── __init__.py
│   │   └── server.py             # TikTok MCP server
│   └── instagram/
│       ├── __init__.py
│       └── server.py             # Instagram MCP server
├── models/
│   ├── __init__.py
│   ├── trend.py                  # Trend entity model
│   ├── trend_analysis.py         # TrendAnalysis entity model
│   └── platform_connection.py   # PlatformConnection entity model
├── services/
│   ├── __init__.py
│   ├── trend_discovery.py        # Trend discovery service
│   ├── trend_storage.py          # Trend storage service
│   └── relevance_filter.py       # Relevance filtering service
└── api/
    ├── __init__.py
    └── routes.py                 # API endpoints (if needed)

tests/
├── contract/
│   └── test_mcp_servers.py       # MCP server contract tests
├── integration/
│   ├── test_trend_discovery.py   # Integration tests
│   └── test_trend_storage.py     # Storage integration tests
└── unit/
    ├── test_relevance_scorer.py  # Unit tests for skills
    ├── test_trend_aggregator.py  # Unit tests for aggregation
    └── test_velocity_calculator.py # Unit tests for velocity
```

**Structure Decision**: Single project structure chosen because this is a backend service component. Skills are separated into `skills/` directory, MCP servers in `mcp_servers/`, and core agent logic in `agents/`. This aligns with Skills vs MCP Tools separation principle.

## Complexity Tracking

> **No violations** - Architecture aligns with constitution principles.
