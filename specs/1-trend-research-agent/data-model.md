# Data Model: Trend Research Agent

**Date**: 2026-02-05  
**Feature**: Trend Research Agent

## Entities

### Trend

Represents a trending topic discovered from social media platforms.

**Attributes**:
- `trend_id` (UUID, Primary Key): Unique identifier for trend
- `topic_name` (String, Required): Name/description of trending topic
- `platform` (Enum: twitter, tiktok, instagram, Required): Source platform
- `engagement_metrics` (JSON, Required): 
  - `likes` (Integer)
  - `shares` (Integer)
  - `comments` (Integer)
  - `views` (Integer, optional)
- `trend_velocity` (Float, Required): Rate of growth (posts per hour)
- `timestamp` (DateTime, Required): When trend was discovered
- `relevance_score` (Float, 0.0-1.0): Relevance to agent niche (calculated)
- `related_hashtags` (Array[String]): Associated hashtags
- `platform_trend_id` (String): Platform-specific trend identifier
- `created_at` (DateTime): Record creation timestamp
- `updated_at` (DateTime): Last update timestamp

**Validation Rules**:
- `relevance_score` must be between 0.0 and 1.0
- `trend_velocity` must be non-negative
- `engagement_metrics` must contain at least one metric
- `topic_name` must be non-empty and max 500 characters

**Relationships**:
- One-to-Many with TrendAnalysis (a trend can have multiple analyses)
- Many-to-One with PlatformConnection (trends belong to a platform)

**State Transitions**: None (immutable after creation)

### TrendAnalysis

Represents analysis results for trends (discovery, aggregation, historical).

**Attributes**:
- `analysis_id` (UUID, Primary Key): Unique identifier for analysis
- `trend_id` (UUID, Foreign Key -> Trend, Required): Related trend
- `analysis_type` (Enum: discovery, aggregation, historical, Required): Type of analysis
- `results_data` (JSON, Required): Analysis-specific results
  - For discovery: trend context, key influencers, engagement patterns
  - For aggregation: correlated trends, platform sequence
  - For historical: trend evolution, pattern matches
- `confidence_score` (Float, 0.0-1.0): Confidence in analysis results
- `analysis_timestamp` (DateTime, Required): When analysis was performed
- `created_at` (DateTime): Record creation timestamp

**Validation Rules**:
- `confidence_score` must be between 0.0 and 1.0
- `results_data` must match structure for `analysis_type`
- `trend_id` must reference existing Trend

**Relationships**:
- Many-to-One with Trend (analyses belong to a trend)

**State Transitions**: None (immutable after creation)

### PlatformConnection

Represents connection status to social media platforms.

**Attributes**:
- `connection_id` (UUID, Primary Key): Unique identifier
- `platform_name` (Enum: twitter, tiktok, instagram, Required, Unique): Platform identifier
- `connection_status` (Enum: connected, disconnected, rate_limited, Required): Current status
- `rate_limit_status` (JSON, Required):
  - `remaining_requests` (Integer)
  - `reset_timestamp` (DateTime)
  - `limit_per_window` (Integer)
- `last_sync_timestamp` (DateTime): Last successful sync with platform
- `last_error` (String, Optional): Last error message if any
- `created_at` (DateTime): Record creation timestamp
- `updated_at` (DateTime): Last update timestamp

**Validation Rules**:
- `platform_name` must be one of supported platforms
- `rate_limit_status.remaining_requests` must be non-negative
- `last_sync_timestamp` must be valid datetime

**Relationships**:
- One-to-Many with Trend (platform has many trends)

**State Transitions**:
- `connected` → `rate_limited`: When rate limit hit
- `rate_limited` → `connected`: When rate limit resets
- `connected` → `disconnected`: On connection failure
- `disconnected` → `connected`: On reconnection

## Data Volume Assumptions

- **Trends**: ~1000 trends per day per platform (3000 total)
- **TrendAnalysis**: ~3 analyses per trend (9000 per day)
- **PlatformConnection**: 3 records (one per platform)
- **Retention**: 90 days historical data (~270,000 trends, ~810,000 analyses)

## Indexes

- `trends.platform, trends.timestamp` (composite): For platform-specific trend queries
- `trends.relevance_score`: For relevance filtering (FR-003)
- `trends.timestamp`: For historical retrieval (FR-006)
- `trend_analysis.trend_id`: For trend analysis lookups
- `platform_connection.platform_name`: For platform status queries

## Constraints

- Unique constraint: `trends(platform, platform_trend_id, timestamp)` - prevent duplicates
- Foreign key: `trend_analysis.trend_id` → `trends.trend_id` (CASCADE on delete)
- Check constraint: `trends.relevance_score BETWEEN 0.0 AND 1.0`
- Check constraint: `trend_analysis.confidence_score BETWEEN 0.0 AND 1.0`
