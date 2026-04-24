---
id: mcp-tools
title: MCP Tools Reference
doc_type: reference
domain: ai
status: active
sensitivity: internal
audience:
  - agent
owners:
  - capymind-maintainers
last_updated: 2026-03-11
canonical: true
description: Reference for MCP tools exposed by the CapyMind server.
---

# MCP Tools Reference

This document describes each tool available via the CapyMind MCP server endpoint.

All tools are called using the `tools/call` JSON-RPC method.

---

## Tool: search_knowledge

Searches the knowledge base for documents matching a query.

### Arguments

| Field | Type   | Required? | Description                    |
|-------|--------|-----------|--------------------------------|
| query | string | yes       | Search query text              |
| limit | number | no        | Max results (default 10, max 50) |

### Example

```json
{
  "name": "search_knowledge",
  "arguments": { "query": "CapyMind security policy", "limit": 5 }
}
```

### Result

Returns:

```json
{
  "results": [
    {
      "path": "docs/governance/security-policy.md",
      "title": "Security Policy",
      "doc_type": "policy",
      "status": "active",
      "sensitivity": "internal",
      "canonical": true,
      "tags": ["security"],
      "score": 0.98
    }
  ]
}
```

---

## Tool: get_project_context

Returns project metadata and its overview document.

### Arguments

| Field | Type   | Required? | Description      |
|-------|--------|-----------|------------------|
| slug  | string | yes       | Project slug     |

### Example

```json
{
  "name": "get_project_context",
  "arguments": { "slug": "capymind" }
}
```

### Result

```json
{
  "project": { "slug": "capymind", "name": "CapyMind", ... },
  "overview": "Full markdown content of projects/capymind/overview.md..."
}
```

---

## Tool: build_context_pack

Creates a ranked set of retrieved chunks for grounding an answer.

### Arguments

| Field | Type   | Required? | Description            |
|-------|--------|-----------|------------------------|
| query | string | yes       | Query text             |
| limit | number | no        | Max chunks (default 5) |

### Result

Returns a `context-pack` contract object:

```json
{
  "query": "...",
  "pack_version": "1.0.0",
  "generated_at": "2026-04-24T14:25:00.000Z",
  "summary": "...",
  "sources": [
    { "path": "...", "chunk_index": 0, "score": 0.95, "text": "..." }
  ],
  "notes": "..."
}
```

---

## Tool: resolve_citation

Given a document ID and optional section, retrieves the original text to allow verification.

### Arguments

| Field        | Type   | Required? | Description        |
|--------------|--------|-----------|--------------------|
| document_id  | string | yes       | Document UUID      |
| section      | string | no        | Heading or section |

### Result

```json
{
  "document": {
    "path": "docs/reference/taxonomy.md",
    "title": "Taxonomy",
    "section": "Layer 4 — Status"
  }
}
```

The caller can then read the full document content.

---

## Tool: get_policy

Returns a specific policy document's content by short name.

### Arguments

| Field         | Type   | Required? | Description                        |
|---------------|--------|-----------|------------------------------------|
| policy_name   | string | yes       | One of: anti-prompt-injection,   retrieval-safety, security, citation, taxonomy |

### Example

```json
{
  "name": "get_policy",
  "arguments": { "policy_name": "anti-prompt-injection" }
}
```

### Result

```json
{
  "policy": "anti-prompt-injection",
  "path": "ai/policies/anti-prompt-injection.md",
  "content": "# Anti-Prompt-Injection Policy\n\n..."
}
```

---

## Error Format

If a tool call fails, the MCP response contains an error object, e.g.:

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "error": { "code": -32602, "message": "Invalid arguments: slug is required" }
}
```

---

## Related

- [MCP Quickstart](./quickstart.md)
- [Security](../../ai/policies/anti-prompt-injection.md)
