<!--
Sync Impact Report:
Version change: 1.0.0 → 1.1.0
Modified principles: N/A
Added sections: Vision Statement, Skills vs MCP Tools Separation (Principle VI), MCP Traceability Requirement, Containerization & CI/CD, Success Metrics, Development Philosophy
Templates requiring updates:
  ✅ plan-template.md - Already aligned with spec-driven development
  ✅ spec-template.md - Already aligned with MCP-first architecture
  ✅ tasks-template.md - Already aligned with TDD workflow
  ⚠️ commands/*.md - Review for Skills vs MCP Tools distinction
Follow-up TODOs: None
-->

# Project Chimera Constitution

## Vision

Project Chimera is an **Autonomous AI Influencer System** that builds autonomous digital entities capable of:
- Researching trends autonomously
- Generating content without human intervention
- Managing engagement independently
- Operating as persistent, goal-directed entities with economic agency

**Ultimate Goal:** A repository so well-architected that a swarm of AI agents can build final features autonomously by Day 3, with minimal human conflict.

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)
Every feature MUST start with a specification in `specs/` before any implementation code is written. Specifications are the source of truth. Implementation code is written only after specs are ratified. This ensures:
- Clear requirements before coding
- Traceability from spec to implementation
- Reduced rework and conflicts
- AI agents can build features autonomously with minimal human conflict

**Rationale:** Project Chimera aims for a repository so well-architected that a swarm of AI agents could build final features by Day 3. Specs enable this by providing unambiguous requirements.

### II. Test-Driven Development (TDD)
Tests MUST be written before implementation. The Red-Green-Refactor cycle is strictly enforced:
1. Write failing tests that define the desired behavior
2. Get user approval for test approach
3. Implement minimum code to make tests pass
4. Refactor while keeping tests green

Tests define "empty slots" for AI to fill, ensuring implementations match specifications exactly.

**Rationale:** TDD ensures implementations match specs, provides regression protection, and enables confident refactoring as the system scales to 1000+ agents.

### III. MCP-First Architecture
All agent capabilities MUST be exposed via Model Context Protocol (MCP) servers. MCP is the standard interface for:
- Agent-to-service communication
- Tool discovery and invocation
- Resource access (data, APIs, databases)
- Inter-agent communication

Custom protocols are allowed only when MCP cannot meet requirements, and must be documented with rationale.

**Rationale:** MCP provides standardization, enables rapid capability expansion, avoids vendor lock-in, and supports the dual-protocol architecture (human-facing + agent-facing).

### IV. Swarm-Centric Design
The system MUST be designed for swarm coordination from the ground up. Swarms are first-class entities with:
- Hierarchical coordination (Planner-Worker-Judge pattern)
- Shared goals and state
- Parallel execution capabilities
- Built-in quality control (Judge layer)

Individual agents operate within swarm contexts, not as isolated entities.

**Rationale:** Project Chimera requires coordinating 1000+ agents. Swarm architecture enables collective intelligence, parallel execution, and scalable coordination patterns proven in Cursor's FastRender experiment.

### V. Economic Agency as Core Capability
Economic transactions are core capabilities, not add-ons. Agents MUST:
- Maintain persistent cryptographic identities (Ed25519)
- Securely manage wallets (HSM for high-value, software for operational)
- Execute transactions autonomously within defined thresholds
- Support both traditional payments (Stripe) and crypto (Base blockchain)

**Rationale:** Project Chimera's value proposition is autonomous influencers with economic agency. This must be built-in from the start, not bolted on later.

### VI. Skills vs MCP Tools Separation
Agent capabilities MUST be clearly separated into two categories:

**Skills** (Internal, Reusable Functions):
- Defined in `skills/` directory
- Self-contained, independently testable functions
- Reusable across agents and swarms
- Examples: `skill_download_youtube`, `skill_transcribe_audio`, `skill_analyze_sentiment`

**MCP Tools** (External Bridges):
- Defined in MCP servers (`mcp-servers/` directory)
- Bridge to external services (APIs, databases, platforms)
- Standardized via MCP protocol
- Examples: `mcp-server-twitter`, `mcp-server-weaviate`, `mcp-server-coinbase`

**Rationale:** Clear separation enables:
- Skills to be reused without external dependencies
- MCP tools to be standardized and shared across projects
- Independent testing and development
- Clear boundaries for AI agents to understand capabilities

## Architecture Constraints

### Dual-Protocol Architecture
The system MUST support two protocol layers:
1. **Human-Facing Protocols:** Standard social media APIs (Twitter/X, Instagram, TikTok)
2. **Agent-Facing Protocols:** MCP + custom protocols for agent-to-agent communication

A bridge layer translates between protocols, enabling agents to interact with human platforms while maintaining agent-native capabilities.

### Model Abstraction Layer
The system MUST NOT lock into a single LLM provider. Requirements:
- Multi-provider support (OpenAI, Anthropic, open-source)
- Cost-based routing (cheaper models where appropriate)
- Provider switching without code changes
- Aggressive caching to reduce API costs

### Data Architecture
Data storage MUST use the right tool for each data type:
- **PostgreSQL:** Structured data, ACID transactions (agent profiles, economic data)
- **Neo4j:** Graph data (social relationships, swarm membership)
- **Redis:** High-volume metrics, task queues, active state
- **Weaviate:** Vector data (agent memory, content similarity)
- **S3:** Media storage (images, videos)

No single database for everything—hybrid approach optimized per use case.

### Security by Design
Security MUST be built into architecture, not added later:
- Defense in depth (multiple security layers)
- Cryptographic agent identities (Ed25519)
- Secure wallet management (HSM + software + multi-signature)
- Audit trails for all economic transactions
- Human-in-the-loop for high-risk operations (threshold-based)

### MCP Traceability (Tenx MCP Sense)
Tenx MCP Sense MUST be always connected and active for full development traceability. Requirements:
- All development activities logged via MCP Sense
- MCP logs show complete development history
- Traceability from spec → test → implementation → deployment
- Logging active throughout all phases (research, architecture, implementation)

**Rationale:** Traceability enables:
- Audit trail for AI swarm collaboration
- Performance analysis and optimization
- Compliance and governance
- Debugging and troubleshooting

### Containerization & CI/CD
The system MUST be containerized and automated:
- **Docker:** All services containerized with Dockerfiles
- **CI/CD Pipelines:** Automated testing, building, and deployment
- **AI Governance:** Code reviewed by AI agents in CI/CD pipelines
- **Makefile:** Standardized commands (`make setup`, `make test`, `make spec-check`)

**Rationale:** Containerization ensures consistent environments, CI/CD enables rapid iteration, and AI governance maintains code quality at scale.

### OpenClaw Integration
The system MUST integrate with the OpenClaw agent network for:
- Agent discovery and registration
- Inter-agent communication protocols
- Reputation and trust systems
- Economic transactions between agents

**Rationale:** OpenClaw provides standardized protocols for agent social networks, enabling Project Chimera agents to participate in the broader agent ecosystem.

## Success Metrics

Project Chimera success is measured by:

1. **Repository Readiness for AI Swarm Collaboration:**
   - Repository structure enables parallel AI agent work by Day 3
   - Clear separation of concerns (specs, tests, skills, MCP servers)
   - Well-documented interfaces and contracts

2. **Test Coverage:**
   - All specs have corresponding failing tests (TDD compliance)
   - Tests define "empty slots" for AI implementation
   - Test suite passes before any feature is considered complete

3. **MCP Traceability:**
   - MCP logs show full development traceability
   - All development phases logged (research → architecture → implementation)
   - Performance metrics tracked via MCP Sense

4. **Skills Architecture:**
   - `skills/` directory with well-defined interfaces
   - Clear I/O contracts for each skill
   - Skills independently testable and reusable

5. **Specification Completeness:**
   - All features have ratified specifications
   - Specs align with implementation
   - No code without corresponding spec

## Development Philosophy

### Velocity vs Distance
Balance speed with engineering depth. Requirements:
- Move fast but maintain quality
- Technical debt must be justified and tracked
- Complexity must be justified (see Complexity Tracking in plan template)
- YAGNI (You Aren't Gonna Need It) - avoid premature optimization

**Rationale:** Project Chimera has aggressive timelines (3-day challenge) but must remain maintainable for long-term AI swarm collaboration.

### AI Governance
Code MUST be reviewed by AI agents in CI/CD pipelines. Requirements:
- Automated AI code review (CodeRabbit or equivalent)
- AI agents verify compliance with constitution
- AI agents check spec alignment
- Human review for high-risk changes (security, economics)

**Rationale:** AI governance enables scalable code review, ensures consistency, and maintains quality as the system scales.

### Git Hygiene
Commit history MUST tell the story of evolving complexity. Requirements:
- Clear, descriptive commit messages
- Logical commit grouping (one logical change per commit)
- Commit history shows progression: spec → test → implementation
- Branch naming follows conventions (`feature/`, `fix/`, `spec/`)

**Rationale:** Clean git history enables:
- AI agents to understand project evolution
- Debugging and troubleshooting
- Onboarding new contributors (human or AI)
- Compliance and audit trails

### Safety First
Human approval layer required for sensitive content. Requirements:
- Human approval for high-risk operations (large transactions, brand partnerships)
- Threshold-based human-in-the-loop (see ADR-002)
- Safety checks before content publication
- Audit trails for all human approvals

**Rationale:** Autonomous systems require safety mechanisms to prevent harm, maintain trust, and ensure compliance.

## Development Workflow

### Specification Process
1. Create specification in `specs/` directory
2. Review and ratify specification (human approval)
3. Write failing tests based on specification
4. Implement feature to pass tests
5. Update specification if implementation reveals gaps

### Code Review Requirements
- All PRs MUST verify compliance with constitution
- Tests MUST pass before merge
- Specifications MUST be updated if requirements change
- Architecture decisions MUST reference relevant ADRs
- AI agents review code in CI/CD pipeline

### Quality Gates
- Tests MUST pass (unit + integration)
- Specifications MUST align with implementation
- MCP servers MUST follow protocol standards
- Security review required for wallet/transaction changes
- MCP Sense traceability verified

## Governance

This constitution supersedes all other development practices. Amendments require:
1. Documentation of rationale
2. Impact assessment (which principles/constraints change)
3. Approval from architecture team
4. Version bump (semantic versioning: MAJOR.MINOR.PATCH)
5. Update of dependent templates and documentation

**Compliance:** All PRs and reviews MUST verify compliance with this constitution. Complexity MUST be justified. Use `Project-Chimera/research/architecture_strategy.md` for detailed architecture guidance.

**Version**: 1.1.0 | **Ratified**: 2026-02-05 | **Last Amended**: 2026-02-05
