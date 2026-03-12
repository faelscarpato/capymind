---
id: tutorial-building-project-card
title: Building a Project Card
doc_type: tutorial
domain: documentation
tags:
  - tutorial
  - projects
  - metadata
  - project-card
  - catalog
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
description: Step-by-step tutorial showing how to create a standardized project card for a project inside CapyMind.
---

# Building a Project Card

## Purpose

This tutorial demonstrates how to create a **Project Card**, a structured representation of a project that allows CapyMind to:

- catalog projects consistently
- enable fast discovery
- support AI retrieval
- generate project listings automatically
- provide quick context for humans

A project card acts as a **structured metadata layer** for projects in the repository.

---

## What a Project Card Is

A **Project Card** is a small structured metadata file describing a project.

Typical characteristics:

- machine-readable
- short but descriptive
- stable
- used by catalog and retrieval pipelines

The standard location is:

```
projects/<project-slug>/project.meta.json
```

---

## When to Create a Project Card

Create a project card when:

- a new project folder is added
- a project is being migrated into CapyMind
- a project needs to appear in catalogs or dashboards
- a project requires machine-readable metadata
- the repository is normalizing project structure

Do **not** create a project card for:

- temporary experiments
- incomplete drafts
- folders that are not real projects

---

## Step 1 — Create the Project Folder

Every project should live in:

```
projects/<project-slug>/
```

Example:

```
projects/capyvision-main/
```

Inside that folder you may later add:

```
overview.md
architecture.md
integrations.md
project.meta.json
```

---

## Step 2 — Create the Metadata File

Create:

```
project.meta.json
```

inside the project folder.

Example:

```
projects/capyvision-main/project.meta.json
```

---

## Step 3 — Basic Schema Example

Example minimal project card:

```json
{
  "id": "capyvision-main",
  "name": "CapyVision",
  "type": "application",
  "status": "active",
  "description": "AI-powered project discovery and knowledge indexing system.",
  "repository": "https://github.com/example/capyvision",
  "domains": ["ai", "knowledge-management"],
  "tags": ["ai", "catalog", "retrieval"]
}
```

---

## Step 4 — Recommended Fields

Common fields include:

| Field | Purpose |
|-----|-----|
| id | project slug |
| name | human-readable project name |
| description | short explanation |
| type | application / library / service |
| repository | source repository |
| status | active / archived |
| domains | taxonomy domains |
| tags | discovery hints |

---

## Step 5 — Validate the Card

Before committing, verify:

- valid JSON
- required fields exist
- slug matches project folder
- naming conventions follow repository rules
- no secrets or sensitive data are present

Example validation tools:

```
python scripts/validate_project_cards.py
```

---

## Step 6 — Link Supporting Documents

A project card should usually link to documentation such as:

- `overview.md`
- `architecture.md`
- `integrations.md`

This creates a structured project dossier.

---

## Step 7 — Commit the Card

Example commit:

```
docs: add project card for capyvision-main
```

Open a pull request and request review from repository maintainers.

---

## Result

Once merged, the project card enables:

- catalog generation
- search indexing
- AI retrieval context
- project dashboards
- structured project discovery

---

## Common Mistakes

### Missing slug alignment

Project slug must match folder name.

### Missing description

Projects should always have a short explanation.

### Excessive metadata

Project cards should remain concise.

### Secrets or credentials

Never store secrets in metadata files.

---

## Next Steps

After creating a project card you may want to:

- write `overview.md`
- add architecture documentation
- create integration references
- register the project in the catalog

---

## Related Documents

- docs/reference/repo-map.md
- docs/reference/taxonomy.md
- docs/reference/naming-conventions.md
- docs/reference/document-types.md
