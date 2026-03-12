---
id: reference-naming-conventions
title: Naming Conventions
doc_type: reference
domain: documentation
tags:
  - naming
  - conventions
  - metadata
  - slugs
  - repository
  - retrieval
  - docs-as-code
version: 1.0.0
status: active
audience:
  - human
  - agent
sensitivity: internal
owners:
  - capymind-maintainers
last_updated: 2026-03-11
citability: excerpt-only
canonical: true
description: Canonical naming conventions for files, folders, document IDs, slugs, manifests, schemas, and repository artifacts in CapyMind.
---

# Naming Conventions

## Purpose

This document defines the **canonical naming rules** for CapyMind.

Its role is to make repository names:

- predictable
- readable
- stable
- searchable
- retrievable
- maintainable

Naming is not cosmetic. In a docs-as-code repository that also serves AI systems, naming directly affects:

- human navigation
- search quality
- retrieval ranking
- linkability
- catalog generation
- automation reliability
- repository governance

A weak naming system creates ambiguity, duplicate concepts, broken expectations, and long-term maintenance cost. A strong naming system reduces friction everywhere.

---

## Scope

These conventions apply to:

- folders
- file names
- document IDs
- project slugs
- metadata keys where naming policy matters
- generated manifests
- schemas
- tests
- scripts
- catalog files
- related repository artifacts

They apply especially to content under:

- `docs/`
- `knowledge/`
- `projects/`
- `references/`
- `ai/`
- `prompts/`
- `scripts/`
- `catalog/`
- `tests/`

This document does **not** define:

- prose style
- taxonomy meanings in depth
- JSON schema field validation
- release numbering policy in detail

Those concerns are handled by other reference or governance documents.

---

## Why Naming Matters

In CapyMind, names do at least five jobs at once.

### 1. Navigation

A reader should be able to infer what a file contains before opening it.

### 2. Retrieval

A search system should get strong lexical signals from the file path and name.

### 3. Governance

Maintainers should be able to tell whether a file belongs in its current place.

### 4. Automation

Scripts, validators, manifests, and CI should be able to apply stable assumptions.

### 5. Citation

When answers cite file paths, those paths should be readable and unambiguous.

If names are vague or inconsistent, every one of these workflows degrades.

---

## Core Principles

All naming rules in this document derive from a small set of principles.

## Principle 1 — Prefer clarity over cleverness

Choose the most obvious accurate name, not the most creative one.

## Principle 2 — Prefer stable names over temporary intent

Do not encode short-lived states into canonical file names.

## Principle 3 — Prefer one meaning per name

A strong name signals one primary responsibility.

## Principle 4 — Prefer consistency over personal style

The repository is a shared system, not a private notebook.

## Principle 5 — Prefer machine-safe names that remain human-readable

Names should be easy to type, parse, link, scan, and retrieve.

---

## Global Naming Standard

Unless explicitly documented otherwise, CapyMind uses:

- **lowercase**
- **kebab-case**
- **ASCII-safe names**
- no spaces
- no decorative punctuation
- no version suffixes in normal canonical file names
- no informal “temporary” suffixes in canonical file names

## Default format

```text
lowercase-kebab-case
```

### Good examples

- `getting-started.md`
- `citation-policy.md`
- `anti-prompt-injection.md`
- `project-overview.md`
- `release-runbook.md`
- `document-meta.schema.json`

### Weak examples

- `GettingStarted.md`
- `getting_started.md`
- `getting started.md`
- `GETTING-STARTED.md`
- `new-doc-final.md`
- `notes-v2-final-real.md`

---

## File Names

File names should describe the **role of the content**, not the emotional state of the author or the history of editing.

## Rules for file names

### Rule 1
Use `kebab-case`.

### Rule 2
Use names that describe the document’s function.

### Rule 3
Avoid generic words unless paired with a specific qualifier.

### Rule 4
Do not include dates in stable canonical file names unless the date is intrinsic to the meaning.

### Rule 5
Do not include version suffixes in canonical file names unless the repository contract explicitly requires versioned filenames.

### Rule 6
Do not encode review state into the name.

Avoid:
- `draft`
- `final`
- `final-final`
- `reviewed`
- `new`
- `old`
- `updated`
- `copy`

Lifecycle belongs in metadata, not in the file name.

---

## Preferred File Name Patterns

### Guide files

Pattern:

```text
verb-orientation-topic.md
```

Examples:

- `getting-started.md`
- `how-to-query-the-knowledge-pack.md`
- `how-to-add-a-document.md`

---

### Policy files

Pattern:

```text
topic-policy.md
```

Examples:

- `security-policy.md`
- `pii-policy.md`
- `review-policy.md`

If the risk topic itself is the core identifier, a direct pattern is also acceptable:

- `anti-prompt-injection.md`

---

### Reference files

Pattern:

```text
topic.md
topic-reference.md
```

Examples:

- `taxonomy.md`
- `repo-map.md`
- `document-types.md`
- `naming-conventions.md`
- `citation-policy.md`

Prefer the shorter canonical form where ambiguity is low.

---

### Runbooks

Pattern:

```text
task-runbook.md
```

Examples:

- `release-runbook.md`
- `review-runbook.md`
- `ingestion-runbook.md`
- `incident-response-runbook.md`

---

### ADRs

Pattern:

```text
NNNN-short-decision-name.md
```

Examples:

- `0001-knowledge-pack-scope.md`
- `0002-document-frontmatter.md`
- `0003-agent-retrieval-policy.md`

Rules:
- zero-padded numeric prefix
- stable short title
- do not rename accepted ADRs casually

---

### Project files

Pattern depends on role, but preferred names are stable and explicit.

Examples:

- `index.md`
- `overview.md`
- `architecture.md`
- `integrations.md`
- `interfaces.md`
- `dependencies.md`
- `runbook.md`
- `risk-notes.md`
- `source-map.md`
- `project.meta.json`

Avoid project-local names such as:

- `important-files.md`
- `main-notes.md`
- `random-architecture.md`
- `overview-final.md`

If a file exists across many project folders, its role must be even more explicit, not less.

---

### Schema files

Pattern:

```text
entity.schema.json
```

Examples:

- `answer.schema.json`
- `document-meta.schema.json`
- `project-card.schema.json`
- `tool-catalog.schema.json`

Why:
This makes schema purpose immediately visible to humans and tooling.

---

### Manifest files

Pattern:

```text
entity.meta.json
entity-manifest.json
```

Preferred examples:

- `project.meta.json`
- `documents-manifest.json`
- `projects-manifest.json`

Use one pattern consistently by area.

Recommended default:
- singular local metadata → `entity.meta.json`
- larger collection artifact → `entity-manifest.json`

---

### Test files

Pattern:

```text
test_<subject>.py
```

Examples:

- `test_frontmatter.py`
- `test_links.py`
- `test_catalog.py`
- `test_schemas.py`

This follows common Python testing conventions and improves discoverability.

---

## Folder Names

Folder names must also follow `kebab-case` unless a widely accepted tooling convention requires something else.

### Good folder names

- `guides`
- `reference`
- `runbooks`
- `governance`
- `technical`
- `commercial`
- `project-alpha`
- `capyvision-main`

### Weak folder names

- `New Folder`
- `Nova Pasta`
- `misc`
- `random`
- `temp`
- `backup-final`
- `folder2`

A folder name should communicate what belongs inside it.

---

## Folder Naming Rules

### Rule 1
Prefer semantic folder names over organizational leftovers.

### Rule 2
Avoid language mixing inside the same naming system unless there is a repository-level decision for multilingual naming.

### Rule 3
Do not use personal shorthand.

### Rule 4
Avoid numbered duplicates unless the number is part of a governed identifier.

Examples to avoid:
- `project-2`
- `docs-new`
- `folder-3`

### Rule 5
If a duplicate folder exists during migration, classify and resolve it instead of normalizing it as permanent.

---

## Project Slugs

Project slugs are especially important because they appear in:

- folder paths
- catalog indexes
- citations
- automation
- manifests
- retrieval contexts

## Project slug format

```text
lowercase-kebab-case
```

Examples:

- `capyvision-main`
- `capyops-main`
- `capyflow-main`

## Project slug rules

### Rule 1
A slug should be stable over time.

### Rule 2
Use the canonical product or project name as the base.

### Rule 3
Add a suffix only if it conveys a meaningful governed distinction.

Examples of meaningful suffixes:
- `-main`
- `-v3` only when versioned identity is truly part of the project identity
- `-legacy` when lifecycle semantics are explicit and governed

### Rule 4
Avoid accidental duplicate suffixes.

Avoid:
- `capyops-main-2`
- `capyuniv2-main-1-capyuniv2-main`
- `nova-pasta-2`

These names signal unresolved migration or duplication, not a stable repository model.

### Rule 5
When two slugs compete, one should become canonical and the others should be archived, redirected, or consolidated.

---

## Document IDs

Document IDs are metadata fields, not file names, but they must follow a naming contract.

IDs should be:

- unique
- stable
- machine-safe
- semantically useful
- not excessively verbose

## Recommended ID format

```text
<doc-type-or-scope>-<topic>
```

Examples:

- `guide-getting-started`
- `guide-query-knowledge-pack`
- `guide-add-document`
- `reference-repo-map`
- `reference-taxonomy`
- `reference-naming-conventions`
- `policy-security`
- `adr-0001-knowledge-pack-scope`

## ID rules

### Rule 1
Use lowercase and hyphens.

### Rule 2
Do not include file extensions.

### Rule 3
Do not use random UUID-like IDs for human-authored docs unless there is a strong systems reason.

### Rule 4
An ID should not change just because the wording of the title improves slightly.

### Rule 5
Two different documents must never share the same ID.

---

## Title vs File Name vs ID

These three things serve different roles and should not be confused.

| Field | Purpose | Example |
|---|---|---|
| file name | filesystem identity | `naming-conventions.md` |
| title | human-facing title | `Naming Conventions` |
| id | stable metadata identifier | `reference-naming-conventions` |

### Rule

Do not force all three to be textually identical. They should be aligned, but each serves a distinct purpose.

---

## Metadata Key Naming

Metadata keys should use a stable convention.

## Preferred metadata key style

```text
snake_case
```

Examples:

- `doc_type`
- `last_updated`
- `source_of_truth`

Why:
Snake case is common in metadata and machine-readable contexts and avoids ambiguity.

## Metadata key rules

### Rule 1
Do not mix styles casually.

Avoid mixing:
- `lastUpdated`
- `last-updated`
- `last_updated`

Choose one system and keep it stable.

### Rule 2
Use concise, descriptive field names.

### Rule 3
Avoid synonyms that refer to the same concept.

For example, choose one:
- `owners`
- not also `owner_list`

### Rule 4
If schema contracts formalize the fields, naming must follow the schema exactly.

---

## Naming for Generated Files

Generated files should be easy to distinguish from manually maintained documents.

## Preferred generated file patterns

- `documents.json`
- `projects.json`
- `sources.json`
- `tags.json`
- `search-index.jsonl`
- `build-summary.json`

If a generated file is an index or manifest, its name should reflect that directly.

## Rules for generated files

### Rule 1
Do not give generated files narrative document names.

### Rule 2
Generated files should live in generated areas such as `catalog/` or another explicitly governed build-output area.

### Rule 3
Do not manually edit generated files unless the repository explicitly defines that behavior.

---

## Naming for Scripts

Scripts should be named by what they do, not by when they were created.

## Preferred script patterns

```text
verb_object.py
verb-object.sh
verb-object.ps1
```

Examples:

- `build.py`
- `validate.py`
- `generate_catalog.py`
- `run_evals.py`
- `organize-repo.sh`
- `organize-repo.ps1`

### Legacy-compatible variation

If the repository already uses underscore-heavy script names for Python, consistency can be preserved temporarily, but the target standard should still be explicit and stable.

Examples:
- `build_capymind.py`
- `rebuild_capymind_markdown.py`

These are acceptable transitional names because they are explicit, even if slightly verbose.

---

## Naming for Catalog Files

Catalog files should be short, explicit, and machine-friendly.

### Preferred examples

- `documents.json`
- `projects.json`
- `sources.json`
- `tags.json`
- `search-index.jsonl`

### Avoid

- `all-data.json`
- `everything.json`
- `repo-output-final.json`
- `manifest-v2-new.json`

The more important a generated artifact is, the more boring and obvious its name should be.

---

## Naming for Temporary and Migration Artifacts

Temporary states should not leak into long-lived canonical names.

## Temporary artifact guidance

Use clearly non-canonical locations or prefixes for transitional material.

Examples:
- `_migration/`
- `_review/`
- `_staging/`

For files:
- `_review-items.md`
- `_migration-notes.md`

### Why underscore prefixes help

They signal:
- transitional role
- non-canonical status
- lower retrieval priority
- maintenance action required

### Rule

Do not let temporary names become permanent without deliberate review.

---

## Reserved and Special Names

Some names have structural meaning and should be used consistently.

## Recommended special file names

### `README.md`
Root or folder-level orientation.

### `index.md`
Primary entry point for a folder or project.

### `_index.md`
Curated or transitional folder index when `index.md` is reserved, unavailable, or migration-specific.

### `_featured.md`
Curated subset or highlighted listing.

### `VERSION`
Repository version source of truth.

### `CHANGELOG.md`
Notable repository changes.

### `CONTRIBUTING.md`
Contribution rules.

### `project.meta.json`
Project metadata source of truth.

### Rule for special names

Use these names only when the file truly plays that role.

Do not create an `index.md` that is actually a random note dump.

---

## Language Policy for Names

CapyMind documentation may be multilingual in content, but naming should remain predictable.

## Default naming language

Use **English** for:

- folder names
- canonical file names
- metadata keys
- schema names
- script names
- manifest names

### Why

This improves:
- consistency
- tooling compatibility
- cross-team readability
- AI retrieval stability
- interoperability across systems

### Exception rule

A project slug may reflect an established product or business name if that name is already canonical, even if it is not English.

Example:
- `petala-decor`

The repository should not rename a real product identity just to force English.

---

## Abbreviations

Abbreviations should be used carefully.

## Good abbreviation rules

### Use common industry abbreviations only when they are broadly understood

Examples:
- `api`
- `pii`
- `adr`
- `ui`
- `ux`

### Avoid team-local shorthand

Avoid names such as:
- `opsx`
- `kt-ctx`
- `bizrefs2`

If a reader outside the immediate author context cannot infer the meaning, the name is too compressed.

---

## Plural vs Singular

Use singular or plural intentionally.

## Preferred guidance

### Use singular for one document or one schema
Examples:
- `document-meta.schema.json`
- `project.meta.json`

### Use plural for collections
Examples:
- `projects.json`
- `documents.json`
- `tags.json`

### Rule

The name should reflect whether the artifact describes **one entity** or **many entities**.

---

## Numbers in Names

Numbers are allowed only when they are meaningful.

## Acceptable uses

- ADR sequence numbers
- version identifiers when they are truly part of the canonical artifact identity
- structured standards that intrinsically include numbers

Examples:
- `0001-knowledge-pack-scope.md`
- `api-v2-migration.md` only if the domain genuinely distinguishes v2 as a stable concept

## Unacceptable uses

- `doc2.md`
- `new-file-3.md`
- `project-main-2`
- `notes-v7-final.md`

These usually signal uncontrolled duplication.

---

## Extension Rules

Use extensions consistently by artifact type.

| Artifact type | Preferred extension |
|---|---|
| human-authored documentation | `.md` |
| structured schema | `.json` |
| JSON schema | `.schema.json` |
| newline-delimited machine index | `.jsonl` |
| comma-separated table export | `.csv` |
| Python script | `.py` |
| shell script | `.sh` |
| PowerShell script | `.ps1` |

Avoid inventing custom extensions when standard ones already fit.

---

## Path Design Principles

A path is part of the name.

Good paths should communicate both **context** and **role**.

## Strong path examples

- `docs/reference/naming-conventions.md`
- `docs/guides/getting-started.md`
- `projects/capyvision-main/architecture.md`
- `ai/policies/anti-prompt-injection.md`
- `catalog/projects.json`

These paths are readable without opening the file.

## Weak path examples

- `docs/misc/file.md`
- `knowledge/random/notes.md`
- `projects/project-2/important.md`

---

## Naming Anti-Patterns

These are repository-level naming failures.

### Anti-pattern 1 — Generic placeholders

Examples:
- `teste.txt`
- `nova-pasta`
- `notes.md`
- `important-files.md`

### Anti-pattern 2 — State encoded in the file name

Examples:
- `overview-final.md`
- `doc-new.md`
- `ready-review.md`

### Anti-pattern 3 — Duplicate lineage in names

Examples:
- `capyops-main-2`
- `capyuniv2-main-1-capyuniv2-main`

### Anti-pattern 4 — Mixed naming styles

Examples:
- `how_to_query.md`
- `How-To-Query.md`
- `how-to-query.md`

### Anti-pattern 5 — Folder names with unclear semantics

Examples:
- `misc`
- `temp`
- `other`
- `backup`

### Anti-pattern 6 — Overcompressed shorthand

Examples:
- `kg-ctx.md`
- `retrv-pol.md`

### Anti-pattern 7 — Naming without lifecycle control

If many duplicate names exist with numeric suffixes, the repository is signaling unresolved governance debt.

---

## Recommended Naming Review Checklist

Before adding or renaming a file, check:

- Is the name in lowercase kebab-case?
- Does it describe the file’s role clearly?
- Would a new contributor understand the file before opening it?
- Does the name avoid temporary-state words?
- Does the name align with document type and location?
- Is there already a stronger existing file with the same meaning?
- Will the path help or hurt retrieval?
- Is the slug stable enough for future citations and automation?

---

## Examples of Good Naming Decisions

## Example 1 — Guide

Bad:
- `start-here-now.md`

Good:
- `getting-started.md`

Why:
The name is conventional, stable, and immediately understandable.

---

## Example 2 — Policy

Bad:
- `security-rules-important.md`

Good:
- `security-policy.md`

Why:
The file name reflects the document’s actual role.

---

## Example 3 — Schema

Bad:
- `document-schema-final.json`

Good:
- `document-meta.schema.json`

Why:
The artifact type and subject are both explicit.

---

## Example 4 — Project folder

Bad:
- `capyvision-main-2`

Good:
- `capyvision-main`

Why:
The duplicate suffix says nothing useful and signals unresolved migration.

---

## Example 5 — Generated inventory

Bad:
- `everything-output.json`

Good:
- `documents.json`

Why:
Generated artifacts should be boring and exact.

---

## Rename Guidance

Renaming is sometimes necessary, but it should be done carefully because names are part of:

- links
- citations
- manifests
- indexes
- automation
- user habits

## Rename when

- the current name is ambiguous
- the file is misplaced and being normalized
- the name conflicts with the taxonomy
- the name blocks retrieval quality
- duplicate lineage must be resolved

## Do not rename casually when

- the change is only stylistic
- many dependencies already point to the file
- the current name is acceptable and stable
- the rename will create unnecessary churn without real clarity gains

### Rename rule

If a rename changes canonical structure, related links, catalogs, and references should be updated together.

---

## Definition of Done

A naming system can be considered healthy when:

- most files follow one clear convention
- folder names are semantically meaningful
- document roles are inferable from names
- project slugs are stable
- IDs are unique and consistent
- generated artifacts are clearly distinct from authored docs
- duplicate lineage suffixes are rare or being actively resolved
- humans and AI systems can use names as reliable structural signals

---

## Related Documents

Read these next:

- `README.md`
- `CONTRIBUTING.md`
- `docs/guides/getting-started.md`
- `docs/guides/how-to-add-a-document.md`
- `docs/reference/repo-map.md`
- `docs/reference/taxonomy.md`
- `docs/reference/document-types.md`
- `docs/reference/citation-policy.md`
- `docs/governance/security-policy.md`

If any of these files do not exist yet, they should be treated as part of the **minimum structural governance baseline** for CapyMind.

---

## Summary

Naming conventions in CapyMind are structural contracts.

They define how to name:

- files
- folders
- project slugs
- document IDs
- schemas
- manifests
- generated artifacts
- scripts and tests

These rules exist to improve:

- readability
- retrieval
- governance
- automation
- citation quality
- long-term maintainability

A repository with weak naming becomes harder to search, harder to trust, and harder to evolve.

A repository with strong naming becomes easier for both humans and AI systems to navigate correctly.
