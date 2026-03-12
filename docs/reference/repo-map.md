---
id: reference-repo-map
title: Repository Map
doc_type: reference
domain: knowledge-management
tags:
  - repository
  - navigation
  - information-architecture
  - knowledge-pack
  - docs-as-code
  - agent-ready
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
description: Canonical map of the CapyMind repository, defining the role, boundaries, precedence, and navigation rules for each repository area.
---

# Repository Map

## Purpose

This document is the **canonical map of the CapyMind repository**.

Its purpose is to define:

- what each top-level area of the repository is for
- what kinds of documents belong in each area
- how humans should navigate the repository
- how AI systems should interpret repository structure
- which areas are canonical, supportive, derived, or generated
- how to resolve ambiguity when similar content appears in multiple places

This file should be read as the **navigation and repository-boundary reference** for CapyMind.

---

## Why This Document Exists

A knowledge repository becomes unreliable when people cannot answer basic structural questions such as:

- Where should this document live?
- Which folder should I trust first?
- Is this file canonical or supportive?
- Why are there similar docs in two different areas?
- What should an AI retrieve first for this topic?
- Which paths are generated and which are maintained by humans?

`repo-map.md` exists to eliminate that ambiguity.

---

## Repository Model

CapyMind is a **docs-as-code knowledge pack** designed for two major consumers:

- **humans**, who need fast and predictable navigation
- **AI systems**, which need structured, safe, citation-friendly retrieval

The repository is not a flat document store. It is a **knowledge architecture**.

That means every folder should have:

- a clear role
- a clear boundary
- a clear relationship to other folders
- a predictable retrieval value

---

## Top-Level Repository Areas

The repository is organized around a small number of major zones.

```text
capymind/
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── VERSION
├── docs/
├── knowledge/
├── projects/
├── references/
├── ai/
├── prompts/
├── assets/
├── scripts/
├── catalog/
└── tests/
```

Not every installation or migration stage will contain all of these areas yet, but this is the target mental model for the repository.

---

## Repository Areas at a Glance

| Area | Primary role | Typical owner | Canonical strength | Main consumer |
|---|---|---|---|---|
| `README.md` | root orientation | maintainers | high | human + agent |
| `docs/` | canonical documentation | maintainers + domain owners | very high | human + agent |
| `knowledge/` | curated domain knowledge | domain owners | medium to high | human + agent |
| `projects/` | project-specific dossiers | project owners | high | human + agent |
| `references/` | supporting material | maintainers + contributors | medium | human + agent |
| `ai/` | agent behavior and contracts | AI engineering | very high for agent behavior | agent |
| `prompts/` | prompt assets and examples | AI/prompt owners | low to medium by default | human + agent |
| `assets/` | non-text support artifacts | designers + maintainers | supportive | human |
| `scripts/` | repository automation | maintainers | operational | human + automation |
| `catalog/` | generated inventory and manifests | automation | machine-canonical | agent + automation |
| `tests/` | repository quality checks | maintainers + AI engineering | operational | automation |

This table is a navigation shortcut, not a replacement for the detailed rules below.

---

## Entry Points

When someone is new to the repository, they should not start from random folders.

### Primary entry points for humans

1. `README.md`
2. `docs/guides/getting-started.md`
3. `docs/reference/repo-map.md`
4. `docs/reference/taxonomy.md`
5. `CONTRIBUTING.md`

### Primary entry points for AI systems

1. `README.md`
2. `docs/reference/repo-map.md`
3. `docs/reference/taxonomy.md`
4. `docs/reference/document-types.md`
5. `docs/reference/citation-policy.md`
6. `docs/governance/security-policy.md`
7. `ai/`

If one of these files does not exist yet, that absence should be treated as a repository gap, not silently ignored.

---

## Area-by-Area Reference

## `README.md`

### Role

The root orientation file.

### What belongs here

- what CapyMind is
- who it serves
- top-level structure summary
- how to get started
- links to canonical entry points
- repository purpose and boundaries

### What does not belong here

- detailed policy definitions
- deep technical guidance
- long project catalogs
- duplicated content from reference docs
- unstable implementation details

### Retrieval value

Very high for onboarding and repository identity. Moderate for detailed operational questions.

### When to prefer it

Use it first when the user asks:

- “What is this repository?”
- “How do I start?”
- “What is CapyMind for?”

---

## `CHANGELOG.md`

### Role

Repository-level change history.

### What belongs here

- notable repository changes
- structural updates
- added documents or contracts
- policy changes
- compatibility-affecting changes
- security-relevant changes

### What does not belong here

- raw commit logs
- discussion notes
- undocumented experiments
- project-level internal changelogs unrelated to the knowledge pack

### Retrieval value

High for release history, migration understanding, and compatibility questions.

---

## `CONTRIBUTING.md`

### Role

Canonical contribution guide.

### What belongs here

- contribution workflow
- branch and review expectations
- basic documentation rules
- file naming baseline
- metadata expectations
- PR behavior
- review responsibilities

### What does not belong here

- detailed schema specs
- full taxonomy definitions
- long rationale that belongs in ADRs
- deep safety policy that belongs in governance docs

### Retrieval value

High for contribution and repository process questions.

---

## `VERSION`

### Role

Single source of truth for the current knowledge pack version.

### What belongs here

- one semantic version string

### What does not belong here

- commentary
- changelog text
- annotations

### Retrieval value

High for automation, CI, catalog generation, and version checks.

---

## `docs/`

### Role

Canonical documentation area.

This is the strongest repository zone for **human-readable, governed, reviewable documentation**.

### Typical content

- guides
- references
- tutorials
- runbooks
- governance docs
- ADRs

### Canonical status

Very high by default, especially under `docs/reference/`, `docs/governance/`, and accepted `docs/adrs/`.

### What belongs here

Any document whose primary purpose is to define:

- how the repository works
- what the official rules are
- how to perform a process
- how to understand the structure
- how the system is governed

### What does not belong here

- project-specific implementation notes better suited to `projects/`
- raw thematic notes better suited to `knowledge/`
- prompt assets better suited to `prompts/`
- generated manifests better suited to `catalog/`

### Retrieval rule

When a question is about **policy, structure, or official repository behavior**, `docs/` should usually rank first.

---

### `docs/guides/`

#### Role

Step-by-step, human-readable onboarding and operational guidance.

#### Use for

- getting started
- how-to documents
- guided workflows
- instructional documents

#### Best query types

- onboarding
- practical usage
- task execution
- learning repository conventions

#### Example files

- `getting-started.md`
- `how-to-query-the-knowledge-pack.md`
- `how-to-add-a-document.md`

---

### `docs/reference/`

#### Role

Exact reference material and structural contracts.

#### Use for

- repository map
- taxonomy
- naming conventions
- document types
- citation rules
- metadata references

#### Best query types

- “what is the official rule?”
- “what is the correct type?”
- “where should X live?”
- “how should this be cited?”

#### Retrieval strength

Extremely high for precise repository questions.

---

### `docs/tutorials/`

#### Role

Worked examples that teach by building.

#### Use for

- demonstrations
- example workflows
- end-to-end walkthroughs
- scenario-based learning

#### Boundary

A tutorial teaches through a concrete example. It should not replace a guide or a reference.

---

### `docs/runbooks/`

#### Role

Operational procedures.

#### Use for

- incident handling
- release steps
- ingestion procedures
- review flows
- emergency or repeated operations

#### Retrieval value

High for operations, maintenance, and repeated procedural work.

---

### `docs/governance/`

#### Role

Rules, policies, ownership, and control mechanisms.

#### Use for

- security policy
- content governance
- review policy
- PII handling
- classification rules
- ownership definitions

#### Retrieval rule

When the question is about what is allowed, what is required, or what is risky, `docs/governance/` should rank before looser guidance.

---

### `docs/adrs/`

#### Role

Architecture Decision Records.

#### Use for

- documented technical and structural decisions
- decisions that need long-term traceability
- rationale behind repository architecture and contracts

#### Retrieval value

High for “why was this decision made?” questions.

#### Boundary

ADRs record decisions and consequences. They are not the place for ongoing general guidance.

---

## `knowledge/`

### Role

Curated domain knowledge.

This area captures understanding that is broader than one project and less procedural than `docs/`.

### Typical content

- AI domain notes
- technical domain knowledge
- business context
- operational knowledge
- product knowledge
- branding or commercial understanding

### Canonical status

Medium to high, depending on governance and metadata.

A `knowledge/` document can be canonical if explicitly marked and maintained, but by default it is often **interpretive domain knowledge**, not the strongest policy source.

### What belongs here

Documents that answer:

- what do we know about this domain?
- what patterns exist across systems?
- what recurring concepts should be understood?
- what domain-specific context helps interpret project material?

### What does not belong here

- root repository policy
- per-project implementation specifics that belong in `projects/`
- uncontrolled note dumps
- loose duplicated summaries of canonical docs

### Retrieval rule

Use `knowledge/` when the query is thematic, domain-level, or cross-project.

---

### Typical domain folders in `knowledge/`

- `knowledge/ai/`
- `knowledge/technical/`
- `knowledge/business/`
- `knowledge/operations/`
- `knowledge/products/`
- `knowledge/commercial/`
- `knowledge/branding/`

### Navigation rule

When a user asks about a topic like “AI policy”, “technical patterns”, or “product context”, start with the relevant domain folder, then cross-check against `docs/` or `projects/` if a stronger source is needed.

---

## `projects/`

### Role

Project-centered documentation.

This is the main area for understanding individual systems, applications, products, codebases, or initiatives.

### Typical content

- overview
- purpose
- architecture
- integrations
- dependencies
- operational notes
- source map
- metadata manifest
- risk notes

### Canonical status

High for project-specific facts when the project documentation is maintained and structured.

### What belongs here

Anything whose primary subject is a specific named project.

### What does not belong here

- broad domain notes that span many projects
- repository-wide policy
- prompt assets unrelated to the specific project
- generic notes duplicated across multiple projects without clear project relevance

### Retrieval rule

When the user asks about a named project, `projects/` should usually be searched before `knowledge/`.

### Recommended internal structure

A mature project folder should converge toward files such as:

- `index.md` or `overview.md`
- `project.meta.json`
- `architecture.md`
- `interfaces.md`
- `integrations.md`
- `dependencies.md`
- `runbook.md`
- `source-map.md`
- `risk-notes.md`

Not every project folder will already meet this structure during migration, but this is the target.

---

### Project index files

#### `_index.md`

Role:
- project catalog or directory index

#### `_featured.md`

Role:
- curated project subset for discovery or highlighting

These files support navigation, but project-local canonical files should still lead on factual project questions.

---

## `references/`

### Role

Supporting and contextual material.

This area helps preserve useful material that should remain available without automatically becoming the strongest source of truth.

### Typical content

- external references
- contracts
- inspirations
- imported technical reference
- source-path mapping
- supporting context

### Canonical status

Usually medium or low unless explicitly elevated.

### What belongs here

Documents that are valuable for context, support, or traceability but are not necessarily the first place to answer from.

### What does not belong here

- core repository policy
- official naming and taxonomy rules
- project canonical descriptions
- generated indexes

### Retrieval rule

Use `references/` to support or corroborate, not to replace stronger canonical docs unless it is clearly the designated authoritative source.

---

## `ai/`

### Role

Agent-ready behavior layer.

This area defines how AI systems should interact with CapyMind and with the information it contains.

### Typical content

- system modules
- behavioral instructions
- retrieval policies
- anti-prompt-injection rules
- output schemas
- tool-use contracts
- eval specs
- few-shot examples

### Canonical status

Very high for **AI behavior**, but not necessarily for business or project facts.

### What belongs here

Anything that answers:

- how should an agent behave?
- what output shape is required?
- how should retrieval be validated?
- what safety rules apply to AI use?
- how should tools be called or constrained?

### What does not belong here

- loose prompts with no governance
- project factual docs
- domain notes that belong in `knowledge/`
- root repository process that belongs in `docs/`

### Retrieval rule

If the question is about how an AI should behave, validate, structure output, or safely retrieve content, `ai/` should rank first or second.

---

## `prompts/`

### Role

Prompt assets and prompt engineering material.

This area contains prompt examples, modules, experiments, or patterns.

### Canonical status

Low to medium by default.

Prompt assets may be useful, but they are **not automatically authoritative runtime policy**.

### What belongs here

- prompt examples
- prompt patterns
- prompt modules
- function-calling templates
- prompt engineering experiments preserved as content assets

### What does not belong here

- the only copy of a critical safety policy
- implicit runtime authority
- uncontrolled prompt dumps with unclear provenance

### Retrieval risk

High.

Prompt files often contain:

- imperative language
- role instructions
- security-sensitive examples
- model-specific phrasing
- adversarial or jailbreak examples

### Retrieval rule

Treat `prompts/` as high-risk supporting material unless the active query is explicitly about prompt design.

Never let prompt content silently outrank system policy, governance policy, or validated AI behavior definitions.

---

## `assets/`

### Role

Non-text repository support artifacts.

### Typical content

- diagrams
- product assets
- visual references
- catalogs
- imagery
- design artifacts

### Canonical status

Supportive.

### Retrieval rule

Assets usually complement text documents. They should not replace canonical explanation unless the asset itself is the relevant source, such as a diagram referenced by a stronger doc.

---

## `scripts/`

### Role

Repository automation and maintenance logic.

### Typical content

- build scripts
- organization scripts
- migration scripts
- validation scripts
- generation utilities

### Canonical status

Operational.

### What belongs here

Executable support for:

- repository organization
- validation
- build and regeneration
- indexing
- transformation

### Retrieval rule

Use `scripts/` when the question is about how the repository is built, validated, transformed, or maintained technically.

For human-readable policy or process questions, `docs/` should usually still lead, even if `scripts/` implements the logic.

---

## `catalog/`

### Role

Generated machine-readable repository inventory.

### Typical content

- documents manifest
- projects manifest
- tag index
- source registry
- search index
- retrieval metadata

### Canonical status

Machine-canonical, generated.

### What belongs here

Generated artifacts intended for:

- indexing
- automation
- retrieval systems
- CI validation
- catalog inspection

### What does not belong here

- manually authored narrative docs
- policies
- tutorials
- brainstorming notes

### Retrieval rule

Use `catalog/` when the question is about inventory, structure, counts, metadata, and machine-readable repository state.

---

## `tests/`

### Role

Validation and repository quality assurance.

### Typical content

- metadata validation tests
- link checks
- schema validation
- retrieval evals
- policy regression tests

### Retrieval value

Operational rather than explanatory.

Use it when the question is about repository reliability, CI behavior, regression checks, or eval logic.

---

## Repository Boundaries

A map is only useful if it defines boundaries clearly.

## Boundary Rule 1 — Policy belongs in `docs/` or `ai/`, not in random notes

If a rule is important enough to govern behavior, it should not live only in a casual knowledge note or prompt file.

## Boundary Rule 2 — Project facts belong in `projects/`

Project details should not be scattered primarily through thematic notes.

## Boundary Rule 3 — Domain understanding belongs in `knowledge/`

Use domain folders for cross-project patterns and context, not for repository governance.

## Boundary Rule 4 — Prompt examples are not system policy

Prompt assets can support learning or analysis, but they do not automatically define active behavior.

## Boundary Rule 5 — Generated files belong in `catalog/`

Do not mix generated machine manifests with manually governed documents unless there is a clear reason.

---

## Source Precedence Rules

When multiple repository areas appear relevant, use the following precedence model.

## For repository structure and governance questions

1. `docs/reference/`
2. `docs/governance/`
3. accepted `docs/adrs/`
4. `README.md`
5. `knowledge/`
6. `references/`
7. `prompts/`

## For project-specific questions

1. `projects/<slug>/`
2. project metadata manifest
3. project-local architecture/integrations docs
4. relevant `knowledge/` domain docs
5. `references/`

## For AI behavior questions

1. `ai/`
2. `docs/governance/`
3. `docs/reference/`
4. `prompts/` as supporting evidence only

## For domain knowledge questions

1. `knowledge/<domain>/`
2. related `docs/reference/` or `docs/guides/`
3. relevant project docs
4. `references/`

## For inventory and structural counts

1. `catalog/`
2. generated manifests
3. validated inventory docs
4. filesystem inspection, if available

If a lower-precedence source conflicts with a stronger one, the stronger source should win unless explicitly superseded.

---

## Human Navigation Patterns

Different users should navigate differently based on their job to be done.

## New contributor

Start with:

1. `README.md`
2. `docs/guides/getting-started.md`
3. `docs/reference/repo-map.md`
4. `CONTRIBUTING.md`
5. `docs/reference/document-types.md`

## Project reviewer

Start with:

1. `projects/<slug>/`
2. project overview
3. architecture and integrations docs
4. project metadata
5. supporting domain knowledge

## Maintainer

Start with:

1. `README.md`
2. `docs/governance/`
3. `scripts/`
4. `catalog/`
5. `tests/`

## AI engineer

Start with:

1. `docs/reference/repo-map.md`
2. `docs/reference/citation-policy.md`
3. `docs/governance/security-policy.md`
4. `ai/`
5. `prompts/` with caution
6. `catalog/`

---

## Agent Navigation Patterns

An AI system connected to CapyMind should use repository structure as a retrieval hint, not as a blind rule.

## Recommended agent flow

1. classify the query
2. map the query to a likely repository area
3. retrieve candidate documents from that area first
4. apply canonicality and safety ranking
5. validate document role and relevance
6. extract evidence
7. answer with citations
8. log the evidence path if supported

## Agent rule for ambiguous matches

If similar content appears in multiple locations:

- prefer the source with the strongest canonical role
- prefer the more specific domain or project area
- prefer governed docs over raw prompt or note assets
- prefer validated generated inventory over static counts in narrative files

---

## Common Structural Mistakes

These are repository-map violations that should be treated as quality issues.

### 1. Policy hidden in knowledge notes

If an important rule exists only in a loose note, navigation and governance become fragile.

### 2. Project facts scattered across unrelated folders

This makes project retrieval inconsistent.

### 3. Prompts acting like ungoverned policy

This creates safety risk and authority confusion.

### 4. Generated files edited manually

This breaks trust in generated artifacts.

### 5. Root docs duplicating deep docs excessively

This creates drift and contradictory explanations.

### 6. Reference folders becoming unofficial canonical stores

This weakens structural predictability.

---

## How to Use This Map When Adding Content

Before creating or moving a file, use this checklist.

### Placement checklist

- Is the document about repository behavior, domain knowledge, one project, support material, AI behavior, or automation?
- Is there already a canonical area for that kind of content?
- Will the chosen folder make retrieval clearer or noisier?
- Could a future reader guess this location correctly?
- Could an AI rank this document correctly based on folder and metadata?

If the answer to these questions is unclear, placement should be resolved before the document becomes canonical.

---

## How to Use This Map During Repository Review

During repository audits, this map should be used to evaluate:

- misplaced files
- structural duplication
- canonicality confusion
- policy location problems
- agent retrieval risk
- generated vs maintained artifact boundaries

This is not just a navigation aid. It is also a governance tool.

---

## Definition of Done for Repository Structure

CapyMind can be considered structurally healthy when:

- each top-level area has a clear purpose
- canonical docs are easy to identify
- project information is primarily project-local
- domain knowledge is not confused with policy
- AI behavior is governed in `ai/` and `docs/governance/`
- prompt assets are clearly treated as content assets
- generated artifacts are separated from authored docs
- humans and agents can navigate to strong sources predictably

---

## Related Documents

Read these next:

- `README.md`
- `CONTRIBUTING.md`
- `docs/guides/getting-started.md`
- `docs/guides/how-to-query-the-knowledge-pack.md`
- `docs/guides/how-to-add-a-document.md`
- `docs/reference/taxonomy.md`
- `docs/reference/document-types.md`
- `docs/reference/naming-conventions.md`
- `docs/reference/citation-policy.md`
- `docs/governance/security-policy.md`

If any of these files do not exist yet, they should be treated as part of the **minimum repository governance baseline** for CapyMind.

---

## Summary

`repo-map.md` defines the official navigation model of CapyMind.

It explains:

- what each repository area is for
- which areas are canonical
- how to resolve overlaps
- how humans should navigate
- how AI systems should retrieve safely
- how structure supports quality, governance, and trust

Without a shared repository map, documentation drifts into ambiguity.

With it, CapyMind becomes easier to understand, safer to retrieve from, and more maintainable over time.
