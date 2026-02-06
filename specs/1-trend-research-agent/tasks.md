# Tasks: Trend Research Agent

**Input**: Design documents from `/specs/1-trend-research-agent/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are REQUIRED per TDD principle (Constitution Principle II). Write failing tests before implementation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths follow plan.md structure: `src/agents/`, `src/skills/`, `src/mcp_servers/`, `src/models/`, `src/services/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan in plan.md
- [x] T002 Initialize Python project with dependencies from pyproject.toml (FastAPI, pydantic, sqlalchemy, tenacity, MCP SDK)
- [x] T003 [P] Configure linting tools (ruff) and formatting (black) in pyproject.toml
- [x] T004 [P] Setup pytest configuration in pytest.ini with async support
- [x] T005 [P] Create Dockerfile for containerization per constitution requirement
- [x] T006 [P] Create docker-compose.yml with PostgreSQL, Redis, Weaviate services
- [x] T007 [P] Create .env.example with required environment variables
- [x] T008 [P] Setup Alembic for database migrations in alembic.ini

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T009 Setup database schema and migrations framework (Alembic) with PostgreSQL connection
- [x] T010 [P] Create base database models in src/models/__init__.py with SQLAlchemy base
- [x] T011 [P] Configure Redis connection in src/services/redis_client.py
- [x] T012 [P] Configure Weaviate connection in src/services/weaviate_client.py
- [x] T013 [P] Setup MCP client infrastructure in src/services/mcp_client.py for connecting to MCP servers
- [x] T014 [P] Configure error handling and logging infrastructure in src/utils/error_handler.py
- [x] T015 [P] Setup MCP Sense logging integration in src/utils/mcp_sense_logger.py (FR-010 requirement)
- [x] T016 [P] Create environment configuration management in src/config/settings.py using pydantic-settings
- [x] T017 Create database migration for base schema structure in alembic/versions/

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Autonomous Trend Discovery (Priority: P1) 🎯 MVP

**Goal**: Enable agents to discover trending topics from social media platforms with relevance scoring

**Independent Test**: Can be fully tested by providing mock MCP server responses and verifying that the agent identifies trending topics with confidence scores. Delivers value by enabling content planning based on real-time trends.

### Tests for User Story 1 (TDD - Write FIRST, ensure they FAIL) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T018 [P] [US1] Contract test for Twitter MCP server get_trending_topics tool in tests/contract/test_twitter_mcp_server.py
- [ ] T019 [P] [US1] Contract test for TikTok MCP server get_trending_topics tool in tests/contract/test_tiktok_mcp_server.py
- [ ] T020 [P] [US1] Contract test for Instagram MCP server get_trending_topics tool in tests/contract/test_instagram_mcp_server.py
- [ ] T021 [P] [US1] Integration test for trend discovery flow in tests/integration/test_trend_discovery.py (mock MCP servers, verify trend list returned)
- [ ] T022 [P] [US1] Unit test for relevance scorer skill in tests/unit/test_relevance_scorer.py (verify relevance score calculation 0.0-1.0)

### Implementation for User Story 1

- [ ] T023 [P] [US1] Create Trend model in src/models/trend.py with attributes from data-model.md (trend_id, topic_name, platform, engagement_metrics, trend_velocity, timestamp, relevance_score, related_hashtags)
- [ ] T024 [P] [US1] Create PlatformConnection model in src/models/platform_connection.py with attributes (connection_id, platform_name, connection_status, rate_limit_status, last_sync_timestamp)
- [ ] T025 [US1] Create database migration for Trend and PlatformConnection tables in alembic/versions/ (depends on T023, T024)
- [ ] T026 [P] [US1] Implement Twitter MCP server in src/mcp_servers/twitter/server.py exposing get_trending_topics tool per contracts/mcp-twitter-server.yaml
- [ ] T027 [P] [US1] Implement TikTok MCP server in src/mcp_servers/tiktok/server.py exposing get_trending_topics tool
- [ ] T028 [P] [US1] Implement Instagram MCP server in src/mcp_servers/instagram/server.py exposing get_trending_topics tool
- [ ] T029 [P] [US1] Implement relevance_scorer skill in skills/trend_analysis/relevance_scorer.py calculating semantic similarity score 0.0-1.0 (depends on Weaviate connection T012)
- [ ] T030 [US1] Implement trend_discovery service in src/services/trend_discovery.py coordinating MCP server calls and relevance scoring (depends on T026-T029)
- [ ] T031 [US1] Implement trend_research agent orchestrator in src/agents/trend_research/orchestrator.py coordinating platform queries (depends on T030)
- [ ] T032 [US1] Implement main trend_research agent in src/agents/trend_research/agent.py with discover_trends method (depends on T031)
- [ ] T033 [US1] Add MCP Sense logging to all trend discovery activities in src/agents/trend_research/agent.py (FR-010 requirement)
- [ ] T034 [US1] Add error handling and retry logic for API rate limits in src/services/trend_discovery.py using tenacity (FR-009 requirement)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. Agent can discover trends from platforms and calculate relevance scores.

---

## Phase 4: User Story 2 - Multi-Platform Trend Aggregation (Priority: P2)

**Goal**: Enable agents to aggregate trends from multiple platforms and identify cross-platform correlations

**Independent Test**: Can be fully tested by providing trends from multiple platforms and verifying that the agent aggregates and correlates trends across platforms. Delivers value by identifying viral opportunities.

### Tests for User Story 2 (TDD - Write FIRST, ensure they FAIL) ⚠️

- [ ] T035 [P] [US2] Unit test for trend_aggregator skill in tests/unit/test_trend_aggregator.py (verify cross-platform aggregation)
- [ ] T036 [P] [US2] Integration test for multi-platform trend aggregation in tests/integration/test_trend_aggregation.py (mock multiple platforms, verify correlations)

### Implementation for User Story 2

- [ ] T037 [P] [US2] Implement trend_aggregator skill in skills/trend_analysis/trend_aggregator.py with time-windowed correlation analysis per research.md
- [ ] T038 [US2] Extend trend_discovery service in src/services/trend_discovery.py with aggregate_trends method (depends on T037)
- [ ] T039 [US2] Add trend propagation analysis to trend_aggregator skill in skills/trend_analysis/trend_aggregator.py showing platform sequence (depends on T037)
- [ ] T040 [US2] Extend trend_research agent in src/agents/trend_research/agent.py with aggregate_cross_platform_trends method (depends on T038)
- [ ] T041 [US2] Add MCP Sense logging for aggregation activities in src/services/trend_discovery.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. Agent can discover trends and aggregate across platforms.

---

## Phase 5: User Story 3 - Trend Storage and Retrieval (Priority: P3)

**Goal**: Enable agents to store and retrieve historical trend data for pattern recognition

**Independent Test**: Can be fully tested by storing trend data and verifying retrieval with time-based queries. Delivers value by enabling trend pattern recognition and predictive analysis.

### Tests for User Story 3 (TDD - Write FIRST, ensure they FAIL) ⚠️

- [ ] T042 [P] [US3] Integration test for trend storage in tests/integration/test_trend_storage.py (verify persistence with timestamps)
- [ ] T043 [P] [US3] Integration test for historical trend retrieval in tests/integration/test_trend_storage.py (verify date range queries)

### Implementation for User Story 3

- [ ] T044 [P] [US3] Create TrendAnalysis model in src/models/trend_analysis.py with attributes from data-model.md (analysis_id, trend_id, analysis_type, results_data, confidence_score, analysis_timestamp)
- [ ] T045 [US3] Create database migration for TrendAnalysis table in alembic/versions/ with foreign key to Trend (depends on T044)
- [ ] T046 [US3] Implement trend_storage service in src/services/trend_storage.py with store_trend and retrieve_trends methods (depends on T044, T045)
- [ ] T047 [US3] Add database indexes for trend queries in alembic/versions/ (platform+timestamp, relevance_score, timestamp) per data-model.md
- [ ] T048 [US3] Extend trend_research agent in src/agents/trend_research/agent.py with store_trends and get_historical_trends methods (depends on T046)
- [ ] T049 [US3] Add Redis caching for frequently accessed trends in src/services/trend_storage.py (depends on T011)
- [ ] T050 [US3] Add MCP Sense logging for storage operations in src/services/trend_storage.py

**Checkpoint**: All user stories should now be independently functional. Agent can discover, aggregate, store, and retrieve trends.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T051 [P] Create quickstart.md validation script in scripts/verify_trend_research.py per quickstart.md
- [ ] T052 [P] Add comprehensive error handling for all edge cases from spec.md (rate limits, API failures, conflicting data)
- [ ] T053 [P] Add performance monitoring and metrics collection for SC-001 through SC-006 success criteria
- [ ] T054 [P] Create API documentation in docs/api.md if API endpoints are needed
- [ ] T055 [P] Add Docker health checks for all services in docker-compose.yml
- [ ] T056 [P] Setup CI/CD pipeline in .github/workflows/trend-research.yml with AI governance per constitution
- [ ] T057 [P] Add integration tests for rate limit handling in tests/integration/test_rate_limits.py
- [ ] T058 [P] Add unit tests for velocity_calculator skill in tests/unit/test_velocity_calculator.py
- [ ] T059 Run quickstart.md validation and verify all success criteria (SC-001 through SC-006)
- [ ] T060 Code cleanup and refactoring based on test coverage analysis

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on US1 for trend data structure but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Depends on US1 for Trend model but independently testable

### Within Each User Story

- Tests (TDD) MUST be written and FAIL before implementation
- Models before services
- Services before agent orchestration
- MCP servers can be implemented in parallel
- Skills can be implemented in parallel
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T003-T008)
- All Foundational tasks marked [P] can run in parallel (T010-T016)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All contract tests for US1 marked [P] can run in parallel (T018-T020)
- MCP servers for US1 can be implemented in parallel (T026-T028)
- Skills can be implemented in parallel within each story
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all contract tests for User Story 1 together:
Task T018: "Contract test for Twitter MCP server in tests/contract/test_twitter_mcp_server.py"
Task T019: "Contract test for TikTok MCP server in tests/contract/test_tiktok_mcp_server.py"
Task T020: "Contract test for Instagram MCP server in tests/contract/test_instagram_mcp_server.py"

# Launch all MCP servers for User Story 1 together:
Task T026: "Implement Twitter MCP server in src/mcp_servers/twitter/server.py"
Task T027: "Implement TikTok MCP server in src/mcp_servers/tiktok/server.py"
Task T028: "Implement Instagram MCP server in src/mcp_servers/instagram/server.py"

# Launch all models for User Story 1 together:
Task T023: "Create Trend model in src/models/trend.py"
Task T024: "Create PlatformConnection model in src/models/platform_connection.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (write failing tests first per TDD)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (MCP servers + discovery)
   - Developer B: User Story 2 (aggregation skills)
   - Developer C: User Story 3 (storage service)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- **TDD Workflow**: Write failing tests FIRST, then implement to make them pass
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- All MCP Sense logging must be implemented per FR-010
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
