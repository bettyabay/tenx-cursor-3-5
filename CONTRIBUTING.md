# Contributing to Project Chimera

Thank you for your interest in contributing to Project Chimera! This document provides guidelines for contributing.

## Development Workflow

### 1. Spec-Driven Development (SDD)

**CRITICAL**: We follow Spec-Driven Development. No code should be written without a ratified specification.

1. Check `specs/` directory before writing any code
2. If spec doesn't exist, create it first using GitHub Spec Kit
3. Ensure spec includes:
   - User stories with acceptance criteria
   - Functional requirements
   - Success criteria
   - Data models (if applicable)

### 2. Test-Driven Development (TDD)

1. Write **failing tests** first
2. Run tests (they should fail - this is expected!)
3. Implement minimal code to make tests pass
4. Refactor while keeping tests green

### 3. Git Workflow

- Commit early, commit often (minimum 2x/day)
- Use conventional commits:
  - `feat:` - New feature
  - `fix:` - Bug fix
  - `docs:` - Documentation changes
  - `test:` - Test additions/changes
  - `refactor:` - Code refactoring
  - `chore:` - Maintenance tasks

Example:
```bash
git commit -m "feat: add trend filtering by relevance score"
```

## Code Standards

### Python Code Style

- **Type hints**: All functions must have type hints
- **Docstrings**: Google-style docstrings for all functions/classes
- **Async/await**: Use async/await for I/O operations
- **Error handling**: Comprehensive error handling with logging

Example:
```python
async def fetch_trends(
    platform: str,
    limit: int = 10
) -> List[Trend]:
    """
    Fetch trending topics from a social media platform.
    
    Args:
        platform: Platform name (twitter, tiktok, instagram)
        limit: Maximum number of trends to return
    
    Returns:
        List of Trend objects
    
    Raises:
        ValueError: If platform is invalid
        APIError: If API call fails
    """
    pass
```

### Running Linters

```bash
make lint      # Run ruff and mypy
make format    # Format code with black and ruff
```

## Testing

### Running Tests

```bash
make test           # Run all tests
make test-cov      # Run with coverage
pytest tests/ -v   # Run specific tests
```

### Test Requirements

- All new features must have tests
- Tests should be independent and isolated
- Use fixtures from `tests/conftest.py`
- Mock external dependencies (MCP servers, APIs)

## MCP Integration

### Adding MCP Servers

1. Create directory under `mcp_servers/`
2. Define tools using `@server.list_tools()`
3. Implement handlers using `@server.call_tool()`
4. Document tools in `mcp_servers/README.md`

### MCP Traceability

- All agent decisions must be logged via MCP Sense
- Use `@mcp_log` decorator on key functions
- Never hardcode API keys - use MCP for secrets

## Database Changes

### Migrations

1. Create migration:
   ```bash
   alembic revision --autogenerate -m "description"
   ```

2. Review generated migration
3. Apply migration:
   ```bash
   make db-migrate
   ```

4. Test migration rollback:
   ```bash
   make db-downgrade
   ```

## API Development

### Adding API Endpoints

1. Create route file in `src/api/v1/routes/`
2. Define Pydantic models for request/response
3. Add endpoint with proper error handling
4. Document endpoint in docstring
5. Add tests in `tests/test_api_endpoints.py`

### API Versioning

- Current version: v1 (`/api/v1/`)
- Breaking changes require new version
- Maintain backward compatibility when possible

## Security

### Secrets Management

- **Never** commit API keys or secrets
- Use MCP servers for secrets in production
- Use `.env` file for local development (not committed)
- Validate secrets on application startup

### Input Validation

- Validate all user inputs
- Use Pydantic models for request validation
- Sanitize inputs before processing
- Return clear error messages

## Documentation

### Updating Documentation

- Update README.md for user-facing changes
- Update CHANGELOG.md for all releases
- Update skill READMEs when I/O contracts change
- Keep API documentation in sync with code

### Documentation Standards

- Use Markdown format
- Include code examples
- Link to related specs
- Keep documentation up-to-date

## Pull Request Process

1. Create feature branch from `main`
2. Make changes following guidelines
3. Write/update tests
4. Update documentation
5. Run `make all` (setup, test, lint)
6. Create pull request with:
   - Clear description
   - Link to related spec
   - Test results
   - Screenshots (if UI changes)

## Questions?

- Check `specs/` directory for project specifications
- Review `.cursorrules` for project context
- Open an issue for questions or clarifications

Thank you for contributing to Project Chimera! 🚀
