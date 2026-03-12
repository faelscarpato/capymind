---
id: governance-ownership
title: Ownership
doc_type: policy
domain: governance
status: active
version: 1.0.0
audience:
  - human
sensitivity: internal
owners:
  - capymind-maintainers
last_updated: 2026-03-11
canonical: true
description: Defines ownership responsibilities for documentation, projects, and governance artifacts inside the CapyMind repository.
---

# Ownership

## Purpose

Ownership ensures that every part of the CapyMind repository has **clear responsibility**.

Without ownership, documentation quickly becomes:

- outdated
- inconsistent
- duplicated
- difficult to maintain

This policy defines how ownership is assigned and maintained.

---

# Ownership Model

CapyMind uses a **distributed ownership model**.

Responsibility is shared between:

- maintainers
- domain owners
- project owners
- contributors

However, every canonical document must have **at least one accountable owner**.

---

# Maintainers

Repository maintainers are responsible for:

- repository structure
- governance enforcement
- approving pull requests
- security oversight
- release management

Maintainers act as the final authority for structural changes.

---

# Domain Owners

Domain owners are responsible for knowledge areas such as:

- AI
- technical architecture
- operations
- business knowledge

Responsibilities include:

- maintaining domain documentation
- reviewing updates
- ensuring domain accuracy

---

# Project Owners

Each project under:

projects/<project-slug>/


should have an assigned owner.

Project owners maintain:

- overview documentation
- architecture documentation
- integrations and dependencies
- project metadata

---

# Document Ownership

Canonical documents must include an **owners field** in their metadata.

Example:

```yaml
owners:
  - capymind-maintainers

Owners are responsible for:

reviewing updates

ensuring accuracy

maintaining documentation over time

Ownership Changes

If ownership changes:

update metadata

notify maintainers

update governance records if needed

Ownership transitions should remain traceable.

Escalation

If a document becomes outdated and no owner responds:

maintainers may assume temporary ownership

governance review may assign a new owner

Benefits of Clear Ownership

Clear ownership improves:

documentation quality

review speed

accountability

long-term repository health

Related Documents

docs/governance/review-policy.md

docs/governance/content-governance.md

CONTRIBUTING.md