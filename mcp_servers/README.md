# MCP Servers

This directory contains MCP (Model Context Protocol) server implementations for external service integration.

## Available MCP Servers

### 1. Social Media MCP (`social_media/`)

Provides access to social media platform APIs:
- **Twitter/X**: Fetch trending topics
- **TikTok**: Fetch trending content
- **Instagram**: Fetch trending hashtags
- **Platform Status**: Check connection status

**Tools:**
- `fetch_twitter_trends` - Get Twitter trends
- `fetch_tiktok_trends` - Get TikTok trends
- `fetch_instagram_trends` - Get Instagram trends
- `get_platform_status` - Check platform connection status

### 2. OpenClaw MCP (`openclaw/`)

Provides integration with the OpenClaw agent network:
- **Agent Registration**: Register agents with capabilities
- **Status Updates**: Publish agent status (online, busy, available, offline)
- **Agent Discovery**: Find agents by capabilities
- **Agent Messaging**: Send messages between agents

**Tools:**
- `register_agent` - Register agent with OpenClaw
- `update_agent_status` - Update agent status
- `discover_agents` - Discover agents by capabilities
- `send_agent_message` - Send message to another agent

## Usage

### Starting MCP Servers

MCP servers can be started independently or integrated into the main application:

```python
from mcp_servers.social_media import server as social_media_server
from mcp_servers.openclaw import server as openclaw_server

# Use servers in your application
```

### Configuration

MCP servers use environment variables for configuration:

```bash
# Social Media APIs (via MCP)
TWITTER_API_KEY=your_key
TIKTOK_API_KEY=your_key
INSTAGRAM_API_KEY=your_key

# OpenClaw Network
OPENCLAW_NETWORK_URL=https://openclaw.network
OPENCLAW_API_KEY=your_key
```

## Implementation Status

⚠️ **Note**: MCP servers are currently **stubs** with tool definitions but not full implementations.

**Completed:**
- ✅ Tool definitions and schemas
- ✅ Server structure
- ✅ Logging framework

**Pending:**
- ❌ Actual API integrations
- ❌ Error handling and retries
- ❌ Rate limiting
- ❌ Authentication

## Development

To add a new MCP server:

1. Create a new directory under `mcp_servers/`
2. Create `__init__.py` with server instance
3. Define tools using `@server.list_tools()`
4. Implement handlers using `@server.call_tool()`
5. Document tools and usage

## Testing

MCP servers can be tested using the mock MCP client in `tests/conftest.py`:

```python
from tests.conftest import mock_mcp_client

client = mock_mcp_client()
result = await client.call_tool("fetch_twitter_trends", {"limit": 10})
```
