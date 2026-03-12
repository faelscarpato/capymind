---
id: runbook-release
title: Release Runbook
doc_type: runbook
domain: operations
status: active
version: 1.0.0
audience: [human]
sensitivity: internal
owners: [capymind-maintainers]
last_updated: 2026-03-11
canonical: true
description: Procedure for publishing a new version of the CapyMind knowledge pack.
---

# Release Runbook

## Purpose
Defines the procedure for creating and publishing a new repository release.

## When to Run
Execute when:

- major documentation updates are merged
- repository structure changes
- taxonomy updates occur
- AI instruction modules change

## Procedure

### 1. Review Pending Changes
Check:

- merged PRs
- changelog updates
- governance updates

### 2. Update Version File

Update:

VERSION

Example:

0.2.0

### 3. Update Changelog

Add a new section describing:

- new docs
- structural updates
- policy changes

### 4. Validate Repository

Run validation scripts:

python scripts/build.py

Check:

- links
- metadata
- schema compliance

### 5. Tag Release

Example:

git tag v0.2.0

### 6. Publish Release

Push tag and release notes to repository hosting platform.

### 7. Regenerate Catalog

If catalog generation exists:

python scripts/generate_catalog.py

## Rollback

If release is faulty:

1. revert version tag
2. correct repository issues
3. publish patch release

## Related Docs
- CHANGELOG.md
- docs/reference/taxonomy.md
