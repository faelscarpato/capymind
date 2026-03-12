---
id: runbook-review
title: Review Runbook
doc_type: runbook
domain: governance
status: active
version: 1.0.0
audience: [human]
sensitivity: internal
owners: [capymind-maintainers]
last_updated: 2026-03-11
canonical: true
description: Operational workflow for reviewing documentation changes in CapyMind.
---

# Review Runbook

## Purpose
Defines the practical steps for reviewing pull requests affecting documentation.

## Trigger Conditions
Run this when:

- a contributor opens a pull request
- governance docs change
- AI instruction pages are modified

## Review Steps

### 1. Inspect File Structure
Confirm files are in correct directories.

### 2. Verify Naming Conventions
Check:

- kebab-case filenames
- proper project slugs

### 3. Validate Metadata
Confirm frontmatter includes:

- id
- doc_type
- domain
- status
- owners

### 4. Validate Content Quality
Look for:

- duplication
- unclear scope
- unsupported claims

### 5. Security Check
Ensure:

- no secrets
- no unsafe prompt instructions
- sensitive content properly classified

### 6. Verify Links
Ensure references point to valid repository files.

### 7. Approve or Request Changes

If requirements are satisfied:

approve PR

Otherwise:

request revisions

## Merge Criteria

A PR should merge only when:

- metadata valid
- structure consistent
- security requirements satisfied

## Related Docs
- CONTRIBUTING.md
- docs/governance/review-policy.md
