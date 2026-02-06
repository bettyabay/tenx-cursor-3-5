# Research: Trend Research Agent

**Date**: 2026-02-05  
**Feature**: Trend Research Agent  
**Purpose**: Resolve technical unknowns and establish implementation patterns

## Technology Decisions

### MCP Server Implementation

**Decision**: Use MCP SDK (Python) for implementing platform-specific MCP servers

**Rationale**:
- MCP SDK provides standardized protocol implementation
- Enables consistent interface across all platform servers
- Supports tool, resource, and prompt patterns required by spec
- Aligns with MCP-First Architecture principle

**Alternatives Considered**:
- Direct API wrappers: Rejected - violates MCP-First principle
- Custom protocol: Rejected - unnecessary complexity, MCP provides standardization

### Relevance Score Calculation

**Decision**: Semantic similarity using vector embeddings (0.0-1.0 range), threshold 0.7+ for high relevance

**Rationale**:
- Semantic similarity captures meaning beyond keyword matching
- Vector embeddings enable nuanced relevance calculation
- 0.0-1.0 range aligns with SC-002 (scores above 0.7)
- Weaviate provides vector similarity search capabilities

**Alternatives Considered**:
- Keyword frequency matching: Rejected - too simplistic, misses semantic relationships
- Engagement metrics only: Rejected - doesn't capture niche alignment

### Trend Storage Strategy

**Decision**: PostgreSQL for structured trend data, Redis for caching active trends, Weaviate for vector similarity

**Rationale**:
- PostgreSQL: ACID transactions, complex queries, historical data (FR-005, FR-006)
- Redis: Fast access to active trends, rate limit tracking (FR-009)
- Weaviate: Vector similarity for relevance scoring (FR-003)
- Aligns with Hybrid Data Architecture constraint

**Alternatives Considered**:
- Single database: Rejected - violates hybrid data architecture principle
- NoSQL only: Rejected - lacks ACID guarantees for trend data integrity

### Rate Limit Handling

**Decision**: Exponential backoff with jitter, queue-based retry system, graceful degradation

**Rationale**:
- Exponential backoff prevents API hammering
- Jitter reduces thundering herd problem
- Queue system ensures no data loss during rate limits (SC-005)
- Graceful degradation maintains partial functionality

**Alternatives Considered**:
- Simple retry: Rejected - doesn't handle rate limits effectively
- Fail fast: Rejected - violates SC-005 (100% data retention requirement)

### Trend Aggregation Algorithm

**Decision**: Time-windowed correlation analysis with platform sequence detection

**Rationale**:
- Time windows enable trend propagation analysis (US-2)
- Correlation identifies cross-platform trends
- Sequence detection shows which platform trended first
- Supports SC-003 (10-minute aggregation target)

**Alternatives Considered**:
- Simple merge: Rejected - doesn't identify correlations or propagation
- Complex ML model: Rejected - overkill for MVP, can be added later

## Integration Patterns

### MCP Server Pattern

**Pattern**: One MCP server per platform (Twitter, TikTok, Instagram)

**Tools Exposed**:
- `get_trending_topics`: Returns trending topics for platform
- `get_trend_details`: Returns detailed trend analysis
- `get_engagement_metrics`: Returns engagement data for trend

**Resources Exposed**:
- `trending_topics`: Read-only trending topics feed
- `platform_status`: Platform connection and rate limit status

**Rationale**: Aligns with Microservices MCP Topology (ADR-004), enables independent scaling per platform

### Skills Pattern

**Skills Defined**:
- `skill_calculate_relevance_score(trend, agent_niche) -> float`: Calculates relevance score 0.0-1.0
- `skill_aggregate_trends(platform_trends) -> aggregated_trends`: Cross-platform aggregation
- `skill_analyze_trend_velocity(trend_history) -> velocity_metrics`: Calculates trend growth rate

**Rationale**: Skills are internal, reusable functions. Separated from MCP tools per Skills vs MCP Tools principle.

## Best Practices

### Error Handling
- All MCP server calls wrapped in try-except with specific error types
- Rate limit errors trigger exponential backoff
- Network errors trigger retry with circuit breaker pattern
- Invalid data errors logged but don't crash agent

### Logging
- All activities logged via MCP Sense (FR-010)
- Log levels: DEBUG (detailed flow), INFO (key decisions), ERROR (failures)
- Include trace IDs for request correlation

### Testing Strategy
- Contract tests for MCP server interfaces
- Integration tests with mock MCP servers
- Unit tests for Skills (relevance scoring, aggregation, velocity)
- Performance tests for SC-001 through SC-006

## Open Questions Resolved

1. **Relevance score range**: 0.0-1.0 (semantic similarity)
2. **Trend storage location**: PostgreSQL (structured), Redis (cache), Weaviate (vectors)
3. **Rate limit strategy**: Exponential backoff with queue system
4. **Aggregation method**: Time-windowed correlation analysis

## Next Steps

Proceed to Phase 1: Design & Contracts
- Create data-model.md with Trend, TrendAnalysis, PlatformConnection entities
- Generate API contracts for MCP server interfaces
- Create quickstart.md for development setup
