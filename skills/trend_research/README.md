# Skill: Trend Research

**Status**: 🚧 Specification Complete, Implementation Pending  
**Feature**: `1-trend-research-agent`  
**Spec**: `specs/1-trend-research-agent/spec.md`

---

## Overview

The Trend Research skill enables autonomous agents to discover, analyze, and track trending topics across multiple social media platforms (Twitter/X, TikTok, Instagram).

## Input Contract

```typescript
interface TrendResearchInput {
  platforms: string[];           // ["twitter", "tiktok", "instagram"]
  niche?: string;                 // Optional: filter by niche (e.g., "technology")
  min_relevance?: number;         // Optional: minimum relevance score (0.0-1.0, default: 0.7)
  date_range?: {                  // Optional: historical trend query
    start: string;                // ISO 8601 datetime
    end: string;                  // ISO 8601 datetime
  };
  limit?: number;                 // Optional: max results (default: 50)
}
```

### Example Input

```json
{
  "platforms": ["twitter", "tiktok"],
  "niche": "technology",
  "min_relevance": 0.7,
  "limit": 20
}
```

---

## Output Contract

```typescript
interface TrendResearchOutput {
  trends: Trend[];
  metadata: {
    total_found: number;
    filtered: number;
    platforms_queried: string[];
    timestamp: string;            // ISO 8601 datetime
    query_duration_ms: number;
  };
}

interface Trend {
  trend_id: string;               // UUID
  topic_name: string;
  platform: "twitter" | "tiktok" | "instagram";
  engagement_metrics: {
    likes: number;
    shares: number;
    comments: number;
    views?: number;
  };
  trend_velocity: number;         // Posts per hour
  relevance_score: number;        // 0.0-1.0
  related_hashtags: string[];
  timestamp: string;              // ISO 8601 datetime
  platform_trend_id: string;      // Platform-specific identifier
}
```

### Example Output

```json
{
  "trends": [
    {
      "trend_id": "550e8400-e29b-41d4-a716-446655440000",
      "topic_name": "AI Agents",
      "platform": "twitter",
      "engagement_metrics": {
        "likes": 15000,
        "shares": 3200,
        "comments": 890,
        "views": 125000
      },
      "trend_velocity": 245.5,
      "relevance_score": 0.85,
      "related_hashtags": ["#AIAgents", "#MachineLearning", "#TechTrends"],
      "timestamp": "2026-02-05T10:00:00Z",
      "platform_trend_id": "twitter_trend_12345"
    }
  ],
  "metadata": {
    "total_found": 45,
    "filtered": 12,
    "platforms_queried": ["twitter", "tiktok"],
    "timestamp": "2026-02-05T10:05:23Z",
    "query_duration_ms": 2847
  }
}
```

---

## Functional Requirements

- **FR-001**: Discover trending topics from Twitter/X, TikTok, Instagram
- **FR-002**: Provide trend metadata (engagement, velocity, relevance)
- **FR-003**: Filter trends by agent niche and relevance
- **FR-004**: Aggregate trends across platforms
- **FR-005**: Store trend data with timestamps
- **FR-006**: Retrieve historical trends by date range
- **FR-007**: Access platforms via MCP servers (not direct API calls)
- **FR-008**: Use Skills directory structure
- **FR-009**: Handle API rate limits with exponential backoff
- **FR-010**: Log all activities via MCP Sense

---

## Success Criteria

- **SC-001**: Discover trends from 3 platforms within 5 minutes
- **SC-002**: 80% accuracy for relevance scores > 0.7
- **SC-003**: Cross-platform aggregation within 10 minutes
- **SC-004**: Historical retrieval within 2 seconds (30-day range)
- **SC-005**: 100% data retention during rate limit periods
- **SC-006**: 100% logging coverage via MCP Sense

---

## Error Handling

### Rate Limit Errors
- **Behavior**: Exponential backoff with jitter
- **Retry**: Up to 3 attempts with increasing delays
- **Fallback**: Return cached data if available

### Platform Unavailable
- **Behavior**: Skip unavailable platform, continue with others
- **Logging**: Log error via MCP Sense
- **Response**: Return partial results with error metadata

### Invalid Input
- **Behavior**: Return validation error immediately
- **Status Code**: 400 Bad Request
- **Response**: Detailed error message

---

## Implementation Status

### ✅ Completed
- [x] Specification document
- [x] Data model (SQLAlchemy)
- [x] Database migrations
- [x] TDD tests (failing - as expected)

### 🚧 In Progress
- [ ] Skill implementation (`skills/trend_research/__init__.py`)
- [ ] MCP server for social media APIs
- [ ] Trend analysis algorithms
- [ ] Relevance scoring logic

### 📋 Pending
- [ ] OpenClaw integration
- [ ] Performance optimization
- [ ] Caching layer
- [ ] Monitoring and metrics

---

## Usage Example

```python
from skills.trend_research import research_trends, TrendResearchInput

# Initialize input
input_data = TrendResearchInput(
    platforms=["twitter", "tiktok", "instagram"],
    niche="technology",
    min_relevance=0.7,
    limit=20
)

# Execute skill
result = await research_trends(input_data)

# Process results
for trend in result.trends:
    print(f"{trend.topic_name} on {trend.platform}: {trend.relevance_score}")
```

---

## Dependencies

- **MCP Servers**: Social Media MCP (Twitter, TikTok, Instagram)
- **Database**: PostgreSQL (trends table)
- **Cache**: Redis (trend caching)
- **Vector DB**: Weaviate (semantic trend analysis)

---

## Related Documentation

- **Spec**: `specs/1-trend-research-agent/spec.md`
- **Data Model**: `specs/1-trend-research-agent/data-model.md`
- **Tests**: `tests/test_trend_research_agent.py`
- **Database Models**: `src/models/trend.py`

---

## Notes

- This skill MUST use MCP servers for platform access (FR-007)
- All activities MUST be logged via MCP Sense (FR-010)
- Relevance scoring uses semantic similarity (Weaviate)
- Historical trends are stored in PostgreSQL with indexes for fast retrieval
