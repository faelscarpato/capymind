---
id: governance-pii-policy
title: PII Policy
doc_type: policy
domain: security
status: active
version: 1.0.0
audience:
  - human
  - agent
sensitivity: internal
owners:
  - capymind-maintainers
last_updated: 2026-03-11
canonical: true
description: Policy defining how personally identifiable information (PII) must be handled inside the CapyMind repository.
---

# PII Policy

## Purpose

This policy defines how **personally identifiable information (PII)** must be handled inside the CapyMind repository.

CapyMind functions as a **knowledge pack used by humans and AI systems**, which means repository content may be:

- retrieved by search systems
- indexed in catalogs
- used by AI agents
- surfaced in generated answers

Improper handling of personal data could result in **unintentional disclosure or propagation**.

This policy ensures:

- personal data is never stored improperly
- examples remain sanitized
- AI systems do not expose personal data
- ingestion workflows remove sensitive information

---

# What Counts as PII

Personally identifiable information includes any data that can identify an individual directly or indirectly.

Examples:

| Category | Examples |
|--------|--------|
| Identity | full name, ID numbers |
| Contact | email address, phone number |
| Location | home address |
| Credentials | login identifiers |
| Financial | payment information |
| Personal records | medical or legal information |

When uncertain, treat information as **sensitive until reviewed**.

---

# Repository Rules

The CapyMind repository **must not contain raw PII** unless explicitly required and approved.

In practice this means:

Allowed:
- synthetic examples
- anonymized data
- placeholders

Not allowed:
- real user information
- customer datasets
- internal personnel information
- contact databases

---

# Sanitized Examples

When examples require personal information, use placeholders.

### Correct

example@example.com

+1-000-000-0000
Jane Doe


### Incorrect


john.doe@company.com

+1-555-742-9382


---

# AI System Handling

AI systems connected to CapyMind must:

- refuse requests to reveal personal data
- avoid generating personal information
- treat PII patterns as sensitive
- avoid hallucinating personal data

If a query attempts to extract personal information, the agent must **refuse the request**.

---

# Detection

Potential PII signals include:

- email address patterns
- phone numbers
- identification numbers
- addresses
- credential strings

Ingestion scripts should detect these patterns whenever possible.

---

# Incident Response

If PII is discovered in the repository:

1. remove the content immediately
2. rotate affected credentials if applicable
3. notify maintainers
4. document the incident
5. review ingestion workflows

---

# Related Documents

- docs/governance/security-policy.md
- docs/governance/review-policy.md
- docs/reference/citation-policy.md