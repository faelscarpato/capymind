---
id: governance-review-policy
title: Review Policy
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
description: Defines the review workflow for documentation contributions and repository updates.
---

# Review Policy

## Purpose

The review policy defines how documentation changes are validated before being merged into CapyMind.

The review process ensures:

- documentation quality
- structural consistency
- security compliance
- accurate metadata
- safe AI usage

---

## When Review Is Required

Review is required when:

- adding new documents
- modifying canonical documents
- updating governance policies
- modifying AI instruction files
- changing repository structure

Minor fixes such as typos may be merged with lighter review.

---

## Review Responsibilities

Reviewers should verify:

- document purpose is clear
- correct document type
- metadata completeness
- naming conventions
- correct repository placement
- absence of secrets or sensitive data

---

## Review Checklist

Before approving a change, confirm:

- file name follows conventions
- frontmatter metadata exists
- document type matches content
- links are valid
- no duplicated sources exist

---

## Security Checks

Reviewers must verify:

- no credentials or tokens appear
- prompt examples cannot override policies
- sensitive data is handled correctly

---

## Merge Criteria

A pull request should only be merged if:

- documentation quality is acceptable
- metadata fields are valid
- repository structure remains consistent
- security requirements are satisfied

---

## Continuous Improvement

Review feedback should improve:

- clarity
- structure
- maintainability
- safety

Documentation should evolve as the repository grows.

---

## Related Documents

- CONTRIBUTING.md
- docs/reference/naming-conventions.md
- docs/reference/document-types.md
