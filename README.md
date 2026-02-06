# Project Chimera: Autonomous AI Influencer Factory

**Status**: 🚧 In Development  
**Version**: 0.1.0  
**License**: [To be determined]

---

## Overview

Project Chimera is an **autonomous AI influencer system** that researches trends, generates content, and manages engagement without human intervention. Built using **Spec-Driven Development (SDD)** and monitored via **Tenx MCP Sense**.

### Core Philosophy

- **Spec-Driven Development**: No code without ratified specifications
- **Test-Driven Development**: Failing tests define implementation targets
- **MCP Traceability**: All decisions logged via MCP Sense
- **Agentic Architecture**: Skills-based agent capabilities with clear I/O contracts

---

## Architecture

```mermaid
graph TB
    A[Trend Research Agent] --> B[Content Generation Pipeline]
    B --> C[Engagement Manager]
    C --> D[Safety Layer]
    A --> E[OpenClaw Network]
    B --> E
    C --> E
    D --> E
    
    A --> F[PostgreSQL]
    B --> F
    C --> F
    
    A --> G[Redis Cache]
    B --> G
    
    A --> H[MCP Servers]
    B --> H
    C --> H
```

### Key Components

- **Agents**: Autonomous entities that perform specific tasks
- **Skills**: Reusable capabilities with defined I/O contracts
- **MCP Servers**: External service connectors (social media APIs, OpenClaw)
- **Database**: PostgreSQL for persistent storage, Redis for caching
- **Vector DB**: Weaviate for semantic search and trend analysis

---

## Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd tenx-cursor-3-5
   ```

2. **Install dependencies**
   ```bash
   make setup
   # or manually:
   pip install uv
   uv pip install -r requirements.txt
   ```

3. **Start services**
   ```bash
   make docker-up
   # or manually:
   docker-compose up -d
   ```

4. **Run database migrations**
   ```bash
   make db-migrate
   # or manually:
   alembic upgrade head
   ```

5. **Run tests**
   ```bash
   make test
   # or manually:
   pytest tests/ -v
   ```

---

## Project Structure

```
tenx-cursor-3-5/
├── specs/                    # Source of truth (Spec-Driven Development)
│   ├── 1-trend-research-agent/
│   ├── 2-content-generation-pipeline/
│   ├── 3-engagement-manager/
│   ├── 4-safety-layer/
│   └── 5-openclaw-integration/
├── src/                      # Implementation code
│   ├── agents/              # Agent implementations
│   ├── api/                 # FastAPI routes (to be implemented)
│   ├── config/              # Configuration management
│   ├── models/              # SQLAlchemy models
│   ├── services/            # Business logic
│   ├── skills/              # Agent skills
│   └── utils/               # Utility functions
├── skills/                   # Reusable agent capabilities
│   ├── trend_research/
│   ├── content_generation/
│   └── engagement_management/
├── tests/                    # TDD tests (intentionally failing)
│   └── test_trend_research_agent.py
├── mcp_servers/              # MCP server implementations
├── alembic/                  # Database migrations
├── docker-compose.yml        # Service orchestration
├── Dockerfile               # Container definition
├── Makefile                 # Task automation
└── pyproject.toml           # Python project configuration
```

---

## Development Workflow

### Spec-Driven Development (SDD)

1. **Phase 1**: `/speckit.specify` - Create baseline specifications
2. **Phase 2**: `/speckit.plan` - Generate implementation plan
3. **Phase 3**: `/speckit.tasks` - Create actionable tasks
4. **Phase 4**: `/speckit.implement` - Execute with AI assistance
5. **Phase 5**: Run tests, commit, repeat

### Test-Driven Development (TDD)

1. Write **failing tests** first (they define what we need to build)
2. Run tests (they fail - this is expected!)
3. Implement minimal code to make tests pass
4. Refactor while keeping tests green
5. Repeat

**Current Status**: Tests are intentionally failing. See `tests/README.md` for details.

---

## Available Commands

Run `make help` to see all available commands:

```bash
make setup          # Install dependencies
make test           # Run tests
make test-cov       # Run tests with coverage
make spec-check     # Verify code aligns with specs
make db-migrate     # Run database migrations
make docker-build   # Build Docker image
make docker-up      # Start Docker services
make docker-down    # Stop Docker services
make lint           # Run linters
make format         # Format code
make clean          # Clean temporary files
```

---

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Database
DATABASE_URL=postgresql://chimera:chimera_dev@localhost:5432/chimera

# Redis
REDIS_URL=redis://localhost:6379

# API Keys (via MCP - never hardcode!)
TWITTER_API_KEY=
OPENAI_API_KEY=

# MCP Sense
MCP_SENSE_ENABLED=true
```

**⚠️ Important**: Never commit `.env` files. Use MCP servers for secrets management.

---

## Testing

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test file
pytest tests/test_trend_research_agent.py -v
```

### Test Status

**All tests are INTENTIONALLY FAILING** - This proves we're following TDD!

Tests will pass once we implement:
- `skills/trend_research/` modules
- MCP server integrations
- OpenClaw network client

See `tests/README.md` for more details.

---

## Database

### Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
make db-migrate

# Rollback last migration
make db-downgrade
```

### Database Schema

See `specs/1-trend-research-agent/data-model.md` for detailed schema documentation.

Key tables:
- `trends` - Trending topics from social media platforms
- `platform_connections` - Connection status to social media platforms

---

## MCP Integration

### MCP Servers

MCP (Model Context Protocol) servers provide external service connectors:

- **Social Media MCP**: Twitter, TikTok, Instagram API access
- **OpenClaw MCP**: Agent network registration and communication
- **Secrets MCP**: Secure API key management

### MCP Sense

All agent decisions are logged via **Tenx MCP Sense** for traceability.

**Requirement**: Keep MCP Sense connected to your IDE at all times.

---

## Contributing

### Development Rules

1. **ALWAYS check `specs/` directory before writing code**
2. **Write failing tests before implementation** (TDD)
3. **Maintain MCP traceability** - log all decisions
4. **Follow code quality standards**:
   - Type hints for all functions
   - Google-style docstrings
   - Async/await for I/O operations
   - Comprehensive error handling

### Git Workflow

- Commit early, commit often (minimum 2x/day)
- Commit messages should tell a story
- Use conventional commits: `feat:`, `fix:`, `docs:`, etc.

---

## CI/CD

GitHub Actions automatically:
- ✅ Run tests on push/PR
- ✅ Check code formatting
- ✅ Run security scans
- ✅ Build Docker images
- ✅ Verify spec alignment

See `.github/workflows/main.yml` for details.

---

## Documentation

- **Specifications**: `specs/` directory
- **API Documentation**: [To be generated via OpenAPI]
- **Architecture**: See `Project-Chimera/research/architecture_strategy.md`
- **Research Notes**: `Project-Chimera/analysis-*.md`

---

## Roadmap

### Phase 1: Foundation ✅
- [x] Spec-driven development setup
- [x] Database schema and migrations
- [x] Basic project structure
- [x] TDD test framework

### Phase 2: Core Agents 🚧
- [ ] Trend Research Agent implementation
- [ ] Content Generation Pipeline
- [ ] Engagement Manager
- [ ] Safety Layer

### Phase 3: Integration 🚧
- [ ] MCP server implementations
- [ ] OpenClaw network integration
- [ ] API endpoints
- [ ] Frontend dashboard

### Phase 4: Production 🚧
- [ ] Performance optimization
- [ ] Monitoring and observability
- [ ] Deployment automation
- [ ] Documentation completion

---

## License

[To be determined]

---

## Contact

For questions or issues, please open an issue on GitHub.

---

## Acknowledgments

- **GitHub Spec Kit** - Spec-Driven Development framework
- **Tenx MCP Sense** - Agent traceability and monitoring
- **OpenClaw** - Agent social network protocol
