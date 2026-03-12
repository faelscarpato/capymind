---
id: adr-0002-document-frontmatter
title: Document Frontmatter Standard
doc_type: adr
domain: documentation
status: accepted
version: 1.0.0
audience:
  - human
  - agent
sensitivity: internal
owners:
  - capymind-maintainers
last_updated: 2026-03-11
canonical: true
description: Establishes the requirement that governed documents must include structured frontmatter metadata.
---

# ADR 0002 — Document Frontmatter

## Status
Accepted

## Context

In a knowledge repository used by AI systems, documents must be machine‑interpretable.

Without structured metadata, retrieval systems cannot reliably determine:

- document purpose
- canonical status
- sensitivity level
- ownership
- lifecycle stage

Frontmatter metadata enables:

- indexing
- validation
- governance automation
- safer retrieval

---

## Decision

All canonical documents must include **YAML frontmatter** containing core metadata fields.

Minimum required fields:

- id
- title
- doc_type
- domain
- status
- owners
- sensitivity
- last_updated

Example:

```yaml
id: reference-taxonomy
title: Taxonomy
doc_type: reference
domain: knowledge-management
status: active
owners:
  - capymind-maintainers
```

Frontmatter must appear at the **top of the document**.

---

## Consequences

Benefits:

- consistent document classification
- machine-readable repository structure
- better AI retrieval signals

Trade‑offs:

- additional contributor responsibility
- metadata validation tooling required

---

## Related Documents

- docs/reference/taxonomy.md
- docs/reference/document-types.md
- docs/reference/naming-conventions.md
