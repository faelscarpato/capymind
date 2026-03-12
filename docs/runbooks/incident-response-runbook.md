---
id: runbook-incident-response
title: Incident Response Runbook
doc_type: runbook
domain: operations
status: active
version: 1.0.0
audience: [human]
sensitivity: internal
owners: [capymind-maintainers]
last_updated: 2026-03-11
canonical: true
description: Procedure for responding to security, repository integrity, or AI safety incidents affecting CapyMind.
---

# Incident Response Runbook

## Purpose
Provides the steps for handling incidents affecting repository integrity or security.

## Incident Types

Examples:

- exposed credentials
- prompt injection discovered in docs
- corrupted repository structure
- unsafe AI instructions
- sensitive data leakage

## Initial Response

1. identify the issue
2. isolate affected files
3. notify repository maintainers

## Containment

Depending on severity:

- remove affected files
- revoke credentials
- disable unsafe automation

## Investigation

Determine:

- root cause
- affected documents
- exposure impact

Check:

- commit history
- pull requests
- contributor activity

## Remediation

Actions may include:

- document correction
- security policy update
- improved validation rules
- additional governance controls

## Documentation

Record:

- incident summary
- cause
- remediation steps
- lessons learned

## Post-Incident Review

After resolution:

- update policies if needed
- improve runbooks
- strengthen automation checks

## Related Docs
- docs/governance/security-policy.md
- docs/governance/review-policy.md
