---
id: governance-content-governance
title: Content Governance
doc_type: policy
domain: governance
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
description: Defines governance rules for documentation quality, ownership, lifecycle management, and repository knowledge integrity.
---

# Content Governance

## Purpose

Content governance ensures that CapyMind remains:

- accurate
- trustworthy
- maintainable
- structured
- safe for AI retrieval

Without governance, documentation repositories degrade into:

- duplicated content
- conflicting information
- outdated knowledge
- unclear ownership

---

## Ownership

Every canonical document must have an owner.

Owners are responsible for:

- maintaining accuracy
- reviewing changes
- approving updates
- ensuring metadata correctness

If ownership is unclear, the document should be reviewed by maintainers.

---

## Content Lifecycle

Documents move through lifecycle states.

| Status | Meaning |
|------|------|
| draft | incomplete |
| active | maintained |
| deprecated | replaced |
| archived | historical |

Lifecycle status must appear in metadata.

---

## Canonical Sources

Canonical documents represent the **source of truth**.

Examples:

- repository rules
- taxonomy
- governance policies
- architecture docs

Derived summaries should **never replace canonical documents**.

---

## Avoiding Duplication

Duplicate documents create confusion.

Before adding content:

1. search existing docs
2. update canonical sources instead of duplicating
3. consolidate overlapping material

---

## Quality Standards

Strong documents should be:

- clear
- structured
- traceable
- well-scoped
- maintained

Weak documents often include:

- vague summaries
- duplicated content
- missing metadata
- unclear purpose

---

## Metadata Requirements

Governed documents should include frontmatter metadata such as:

- id
- title
- doc_type
- domain
- status
- owners
- sensitivity
- last_updated

Metadata supports indexing and retrieval.

---

## Governance Reviews

Maintainers periodically review:

- outdated documents
- missing metadata
- structural duplication
- broken links

The goal is to maintain repository integrity over time.

---

## Related Documents

- docs/reference/taxonomy.md
- docs/reference/naming-conventions.md
- docs/reference/document-types.md
