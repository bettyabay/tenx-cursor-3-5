# Test-Driven Development (TDD) Tests

## Purpose

These tests follow the **Test-Driven Development** approach mandated by Project Chimera's Spec-Driven Development workflow.

## TDD Workflow

1. **Write failing tests first** - Tests define what we need to build
2. **Run tests** - They fail (as expected)
3. **Implement minimal code** - Just enough to make tests pass
4. **Refactor** - Improve code while keeping tests green
5. **Repeat**

## Running Tests

### Prerequisites

```bash
pip install pytest pytest-cov
```

### Run all tests

```bash
pytest tests/ -v
```

### Run specific test file

```bash
pytest tests/test_trend_research_agent.py -v
```

### Run with coverage

```bash
pytest tests/ --cov=skills --cov-report=html
```

## Current Test Status

**All tests are INTENTIONALLY FAILING** - This proves we're following TDD!

Tests will pass once we implement:
- `skills/trend_research/__init__.py`
- `skills/trend_research/agent.py`
- MCP server integrations
- OpenClaw network client

## Test Structure

- `test_trend_research_agent.py` - Tests for Trend Research Agent
  - Initialization tests
  - Trend discovery tests
  - OpenClaw integration tests
  - MCP integration tests
  - Error handling tests

## Expected Failures

When you run `pytest tests/`, you should see failures like:

```
ImportError: cannot import name 'TrendResearchAgent' from 'skills.trend_research'
```

This is **expected** and **correct** - it proves we're writing tests before implementation!
