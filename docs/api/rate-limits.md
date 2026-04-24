---
id: api-rate-limits
title: API Rate Limits
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
description: Rate limiting policy for the CapyMind public API.
---

# Rate Limits

## Purpose

This document defines the rate limiting behavior of the CapyMind API to ensure fair usage and system stability.

## Default Limits

| Plan   | Requests per minute | Burst |
|--------|---------------------|-------|
| Free   | 60                  | 10    |
| Standard | 120               | 20    |
| Enterprise | custom          | custom |

The default for most API keys is **120 requests per minute**.

## How It Works

Rate limit counters are maintained per API key (in-memory by default; in production a Redis store may be used).

When you exceed your limit, you'll receive:

- Status: `429 Too Many Requests`
- Header: `Retry-After: <seconds>` tells when the window resets.

## Getting Unblocked

- Wait for the window to reset.
- Contact maintainers to request a higher limit if needed.

## Monitoring

Each request logs:
- API key id
- Endpoint
- Timestamp
- Response status

This allows auditing and anomaly detection.

## Best Practices

- Implement exponential backoff on 429 responses.
- Batch requests where possible.
- Cache results (search results are cacheable for 60 seconds by default).

## Related

- [Quickstart](./quickstart.md)
- [OpenAPI](../../openapi.json)
