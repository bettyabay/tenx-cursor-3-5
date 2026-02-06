# Skill: Content Generation

**Status**: 🚧 Specification Complete, Implementation Pending  
**Feature**: `2-content-generation-pipeline`  
**Spec**: `specs/2-content-generation-pipeline/spec.md`

---

## Overview

The Content Generation skill enables autonomous agents to create engaging content (text, images, videos) based on trending topics and agent persona.

## Input Contract

```typescript
interface ContentGenerationInput {
  trend_id: string;              // UUID of trend to create content for
  content_type: "text" | "image" | "video";
  platform: "twitter" | "tiktok" | "instagram";
  agent_persona: {
    tone: string;                 // "professional", "casual", "humorous"
    style: string;                // "informative", "entertaining", "educational"
  };
  constraints?: {
    max_length?: number;
    include_hashtags?: boolean;
    include_media?: boolean;
  };
}
```

---

## Output Contract

```typescript
interface ContentGenerationOutput {
  content_id: string;             // UUID
  content_type: "text" | "image" | "video";
  platform: string;
  content: {
    text?: string;
    media_url?: string;
    hashtags?: string[];
  };
  metadata: {
    trend_id: string;
    generation_timestamp: string;
    model_used: string;
    confidence_score: number;
  };
}
```

---

## Functional Requirements

- **FR-001**: Generate text content for Twitter/X, TikTok, Instagram
- **FR-002**: Generate images using AI image generation
- **FR-003**: Generate video content (to be implemented)
- **FR-004**: Match agent persona and tone
- **FR-005**: Include relevant hashtags
- **FR-006**: Validate content against safety guidelines
- **FR-007**: Use MCP servers for AI model access
- **FR-008**: Log generation activities via MCP Sense

---

## Implementation Status

### ✅ Completed
- [x] Specification document

### 🚧 Pending
- [ ] Skill implementation
- [ ] AI model integration (via MCP)
- [ ] Content validation
- [ ] Safety layer integration

---

## Related Documentation

- **Spec**: `specs/2-content-generation-pipeline/spec.md`
- **Safety Layer**: `specs/4-safety-layer/spec.md`
