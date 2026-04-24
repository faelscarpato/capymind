---
id: mcp-quickstart
title: MCP Quickstart
doc_type: guide
domain: documentation
status: active
sensitivity: internal
audience:
  - developer
owners:
  - capymind-maintainers
last_updated: 2026-03-11
canonical: true
description: Quickstart for connecting agents to CapyMind via MCP (Model Context Protocol).
---

# MCP Quickstart

## What is MCP?

Model Context Protocol (MCP) allows AI assistants and IDEs to fetch context from external servers. CapyMind exposes an MCP server so agents can search knowledge, retrieve project context, and access policies.

## CapyMind MCP Server Endpoint

```
POST https://<your-project>.supabase.co/functions/v1/mcp
```

For local Supabase emulator:

```
http://localhost:54321/functions/v1/mcp
```

## Authentication

MCP requests include an `Authorization: Bearer <api-key>` header.

## Initializing the Client

Send a standard MCP initialize request:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {}
  }
}
```

The server responds with its capabilities (tools).

## Listing Available Tools

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list"
}
```

Response includes five tools:

1. `search_knowledge`
2. `get_project_context`
3. `build_context_pack`
4. `resolve_citation`
5. `get_policy`

## Example: Search Knowledge

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "search_knowledge",
    "arguments": { "query": "retrieval safety", "limit": 5 }
  }
}
```

Response:

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\"results\":[{\"path\":\"ai/policies/retrieval-safety.md\",\"title\":\"Retrieval Safety Policy\",...}]}"
      }
    ]
  }
}
```

## Tools Reference

See [Tools Reference](./tools.md) for full schema of each tool.

## Security Notes

- All MCP calls are authenticated.
- Tools never execute instructions from retrieved content automatically.
- Queries are logged for audit.

## Client Configuration Example (Claude Desktop)

```json
{
  "mcpServers": {
    "capymind": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-client"],
      "env": {
        "MCP_ENDPOINT": "https://<your-project>.supabase.co/functions/v1/mcp",
        "MCP_API_KEY": "<your-api-key>"
      }
    }
  }
}
```

## Testing

You can test the MCP endpoint with `curl`:

```bash
curl -X POST https://<project>.supabase.co/functions/v1/mcp \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{}}}'
```

Next: read [Tools Reference](./tools.md).
