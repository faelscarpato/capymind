---
id: api-authentication
title: API Authentication
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
description: Guide to authenticating with the CapyMind REST API using API keys.
---

# API Authentication

## Overview

The CapyMind API uses API keys to control access. All requests must include a valid key.

## Key Types

### Service Role Key

- Full access to all endpoints.
- Intended for trusted internal systems.
- Must be kept secret; never expose in client-side code.

### Anon/Public Key

- Read-only access to public endpoints.
- Rate-limited more strictly.
- Safe for limited client-side usage (though not recommended for production).

## How to Send an API Key

Choose one:

```
Authorization: Bearer sk-xxxxx
```
or
```
x-api-key: sk-xxxxx
```

## Obtaining a Key

Contact CapyMind maintainers to issue a key. Provide:

- Application name
- Owner contact
- Expected usage (requests per day)

## Key Lifecycle

- Keys are created with `is_active = true`.
- Misuse can lead to revocation.
- Keys may be rotated periodically. Monitor for `401` responses.

## Environment Variables for Local Development

For local Supabase emulator:

```bash
SUPABASE_URL=http://localhost:54321
SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...
```

## Related

- [Rate Limits](./rate-limits.md)
- [OpenAPI specification](../../openapi.json)
