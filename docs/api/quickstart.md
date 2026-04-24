---
id: api-quickstart
title: API Quickstart
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
description: Quickstart guide for using the CapyMind public REST API.
---

# API Quickstart

## Purpose

This guide helps you get started with the CapyMind REST API in minutes.

## Prerequisites

- Node.js 18+ installed
- An API key (request access from CapyMind maintainers)

## Base URL

```
https://<your-project>.supabase.co/functions/v1/capymind-api
```

For local development with Supabase CLI:

```
http://localhost:54321/functions/v1/capymind-api
```

## Authentication

All endpoints require an API key. Pass it via:

**Header:** `Authorization: Bearer <your-api-key>`

or

**Header:** `x-api-key: <your-api-key>`

### Getting an API Key

Contact the CapyMind maintainers to request a key. Keys are rate-limited per minute.

## Endpoints

### Health Check

```
GET /v1/health
```

```json
{
  "status": "ok",
  "timestamp": "2026-04-24T14:20:00.000Z"
}
```

### List Projects

```
GET /v1/projects
```

Returns all active projects.

```json
[
  {
    "id": "...",
    "name": "CapyAI",
    "slug": "capyai-main",
    "status": "active",
    "domain": "ai"
  }
]
```

### Get Project by Slug

```
GET /v1/projects/{slug}
```

Example:

```
GET /v1/projects/capyai-main
```

### Search Documents

```
POST /v1/search
Content-Type: application/json
Authorization: Bearer <key>
```

Body:

```json
{
  "query": "CapyMind",
  "limit": 10,
  "offset": 0
}
```

Response (adheres to AI contracts `search-result`):

```json
{
  "query": "CapyMind",
  "total": 3,
  "limit": 10,
  "offset": 0,
  "results": [
    {
      "path": "README.md",
      "score": 0.95,
      "title": "CapyMind",
      "doc_type": "guide",
      "status": "active",
      "tags": ["knowledge-pack"]
    }
  ]
}
```

### Build Context Pack

```
POST /v1/context-pack
Content-Type: application/json
Authorization: Bearer <key>
```

Body:

```json
{
  "query": "How does CapyMind handle retrieval safety?",
  "limit": 5
}
```

Response (adheres to `context-pack` contract):

```json
{
  "query": "...",
  "pack_version": "1.0.0",
  "generated_at": "2026-04-24T14:20:00.000Z",
  "summary": "...",
  "sources": [
    {
      "path": "ai/policies/retrieval-safety.md",
      "chunk_index": 0,
      "score": 0.98,
      "text": "..."
    }
  ],
  "notes": "MVP context pack — full ranking and embeddings pending"
}
```

### Get Public Index

```
GET /v1/llms.txt
```

Returns plain-text index for LLMs.

### OpenAPI Schema

```
GET /openapi.json
```

Returns the OpenAPI 3.0 specification for this API.

## Error Handling

All errors return JSON:

```json
{
  "error": "Error message"
}
```

HTTP codes:
- 400 – Bad request (missing parameters)
- 401 – Unauthorized (invalid or missing API key)
- 403 – Forbidden (key not active)
- 404 – Not found
- 429 – Rate limited
- 500 – Internal error

## Rate Limits

Default: 120 requests per minute per API key.

If rate-limited, you'll receive HTTP 429 with `Retry-After` header.

## cURL Examples

```bash
# Health
curl https://<project>.supabase.co/functions/v1/capymind-api/v1/health

# Search
curl -X POST https://<project>.supabase.co/functions/v1/capymind-api/v1/search \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"query":"CapyMind","limit":5}'
```

## Next Steps

- Read the [Authentication guide](./authentication.md)
- Read the [Rate Limits guide](./rate-limits.md)
- Explore [MCP integration](../mcp/quickstart.md)
