---
id: adr-0004-sensitivity-classification
title: Sensitivity Classification
doc_type: adr
domain: security
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
description: Defines the sensitivity classification model used for documents inside the CapyMind repository.
---

# ADR 0004 — Sensitivity Classification

## Status
Accepted

## Context

Repositories used by AI systems may expose information through retrieval and summarization.

Without classification, sensitive information may be:

- quoted unintentionally
- exposed through AI responses
- indexed by external systems

A sensitivity model is required to guide both:

- humans
- automated systems

---

## Decision

All documents must include a **sensitivity classification** in metadata.

Allowed levels:

| Level | Meaning |
|------|------|
| public | safe for public sharing |
| internal | internal repository content |
| confidential | restricted internal knowledge |
| restricted | highly sensitive material |

AI systems must respect sensitivity classifications when:

- retrieving
- quoting
- summarizing
- exporting content

---

## Consequences

Benefits:

- safer repository usage
- clearer data governance
- easier compliance enforcement

Trade‑offs:

- contributors must classify documents
- tooling may be required to enforce policy

---

## Related Documents

- docs/governance/security-policy.md
- docs/governance/pii-policy.md
- docs/reference/taxonomy.md
