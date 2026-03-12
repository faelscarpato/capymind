---
id: runbook-ingestion
title: Ingestion Runbook
doc_type: runbook
domain: operations
status: active
version: 1.0.0
audience: [human, agent]
sensitivity: internal
owners: [capymind-maintainers]
last_updated: 2026-03-11
canonical: true
description: Operational procedure for ingesting new documents, projects, or datasets into the CapyMind repository and knowledge pack.
---

# Ingestion Runbook

## Purpose
Defines the operational steps for safely ingesting new content into CapyMind while preserving structure, metadata quality, and security.

## Trigger Conditions
Run this process when:
- adding a new project
- importing external documentation
- migrating legacy content
- ingesting new datasets or references

## Prerequisites
- contributor access to repository
- metadata templates available
- taxonomy reference available
- naming conventions followed

## Procedure

### 1. Prepare Content
- ensure files are markdown or structured formats
- remove credentials or secrets
- normalize file names using kebab-case

### 2. Classify Documents
Determine:
- document type
- domain
- sensitivity level
- canonical status

### 3. Add Metadata
Ensure frontmatter fields exist:
- id
- title
- doc_type
- domain
- status
- owners
- sensitivity

### 4. Place Files in Correct Location
Example structure:

docs/
knowledge/
projects/
references/

### 5. Validate Structure
Run repository validation tools if available:

python scripts/validate_docs.py

### 6. Commit Changes
Example commit:

docs: ingest new project documentation

### 7. Submit Pull Request
Request review from maintainers.

## Validation Checks
Before finishing ingestion confirm:

- metadata exists
- naming rules followed
- no duplicated documents
- links resolve correctly

## Rollback
If ingestion introduces structural issues:

1. revert commit
2. correct metadata
3. re-run ingestion

## Related Docs
- docs/reference/repo-map.md
- docs/reference/taxonomy.md
