---
id: sdk-typescript
title: TypeScript SDK
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
description: TypeScript SDK for CapyMind API.
---

# TypeScript SDK

## Installation

```bash
npm install @capymind/sdk
```

## Basic Usage

```typescript
import { CapyMind } from '@capymind/sdk';

const client = new CapyMind({
  baseUrl: 'https://<your-project>.supabase.co/functions/v1/capymind-api',
  apiKey: process.env.CAPYMIND_API_KEY!
});

// Search
const results = await client.search('CapyMind');
console.log(results.results);

// Get project
const project = await client.getProject('capymind');
console.log(project);

// Build context pack
const pack = await client.contextPack('What is retrieval safety?', 5);
console.log(pack.sources);
```

## Methods

### `search(query: string, limit?: number): Promise<SearchResult>`

Search the knowledge base.

- `query`: search string
- `limit`: max results (default 10, max 50)

Returns `SearchResult` per `ai/contracts/search-result.schema.json`.

### `contextPack(query: string, limit?: number): Promise<ContextPack>`

Retrieve chunks for grounding.

Returns `ContextPack` per `ai/contracts/context-pack.schema.json`.

### `getProject(slug: string): Promise<Project>`

Fetch project metadata and overview.

### `getDocument(id: string): Promise<Document>`

Fetch a document by UUID.

### `health(): Promise<{status: string; timestamp: string}>`

Health check.

## Error Handling

All methods throw on non-2xx responses:

```typescript
try {
  const results = await client.search('something');
} catch (err) {
  if (err instanceof Error) {
    console.error('API error:', err.message);
  }
}
```

## TypeScript Support

The SDK exports types for responses:

- `SearchResult`, `SearchResultItem`
- `ContextPack`, `ContextSource`
- `Project`
- `Document`

These types align with the official AI contracts.

## Environment Variables

Example `.env`:

```
CAPYMIND_API_KEY=sk-xxxxx
CAPYMIND_BASE_URL=https://<project>.supabase.co/functions/v1/capymind-api
```

You may also construct the client from these:

```typescript
const client = new CapyMind({
  baseUrl: process.env.CAPYMIND_BASE_URL!,
  apiKey: process.env.CAPYMIND_API_KEY!
});
```

## Next Steps

- Read the [REST API quickstart](../api/quickstart.md)
- Explore the [OpenAPI spec](../../openapi.json)
- See [MCP integration](../mcp/quickstart.md) if building an AI agent.
