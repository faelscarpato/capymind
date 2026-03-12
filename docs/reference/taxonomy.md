---
id: reference-taxonomy
title: Taxonomy
doc_type: reference
domain: knowledge-management
tags:
  - taxonomy
  - metadata
  - classification
  - retrieval
  - governance
  - knowledge-pack
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
description: Canonical taxonomy for classifying documents, domains, status, sensitivity, audience, and retrieval behavior in CapyMind.
---

# Taxonomy

## Purpose

This document defines the **canonical classification system** for CapyMind.

Its role is to create a shared vocabulary for:

- organizing repository content
- classifying documents consistently
- improving human navigation
- improving AI retrieval quality
- reducing ambiguity during contribution and review
- supporting governance, auditing, and indexing

Without a common taxonomy, the repository becomes difficult to maintain and unsafe to use at scale. Files may be placed inconsistently, tags become noisy, document types lose meaning, and retrieval systems cannot rank content reliably.

This taxonomy should be treated as a **repository contract**, not as optional guidance.

---

## Scope

This taxonomy applies to all governed content in CapyMind, especially content under:

- `docs/`
- `knowledge/`
- `projects/`
- `references/`
- `ai/`
- `prompts/` when governed as repository assets
- generated catalog metadata where classification is required

It governs classification for:

- document type
- domain
- status
- sensitivity
- audience
- canonicality
- citability
- ownership expectations
- retrieval interpretation

This file does **not** define:

- detailed JSON schemas
- CI implementation
- exact directory structure rules for every folder
- every possible future business domain forever

Those concerns may extend this taxonomy later, but they should not contradict it without an explicit decision record.

---

## Why Taxonomy Matters

CapyMind serves both humans and AI systems.

Humans need:

- predictable navigation
- shared terminology
- fewer duplicate documents
- clear understanding of which file to trust

AI systems need:

- structured classification
- stable ranking signals
- safe interpretation of retrieved material
- consistent document roles

A strong taxonomy improves:

- repository coherence
- retrieval precision
- citation quality
- governance
- maintainability
- onboarding speed

A weak taxonomy causes:

- duplicated content
- misplaced files
- vague metadata
- bad search results
- misleading retrieval
- unsafe authority confusion

---

## Taxonomy Layers

CapyMind classification is divided into the following layers:

1. **Repository area**
2. **Document type**
3. **Domain**
4. **Status**
5. **Sensitivity**
6. **Audience**
7. **Canonicality**
8. **Citability**

These layers work together.

A file is not fully classified when only one field is present. For example, a file marked as `guide` but with no domain, no status, and no sensitivity is still hard to govern and rank correctly.

---

## Layer 1 — Repository Area

Repository area refers to the major structural zone where a document lives.

This is not a replacement for metadata, but it is still a strong signal for navigation and retrieval.

## Controlled repository areas

| Area | Meaning | Typical role |
|---|---|---|
| `root` | top-level repository files | orientation, versioning, contribution, release info |
| `docs` | canonical documentation | guides, references, policies, runbooks, ADRs |
| `knowledge` | domain knowledge | curated thematic understanding |
| `projects` | project dossiers | project-specific facts and context |
| `references` | supporting material | contextual, external, or support evidence |
| `ai` | agent behavior layer | policies, schemas, examples, evals |
| `prompts` | prompt assets | prompt examples, patterns, modules |
| `assets` | non-text artifacts | diagrams, visual references, binary support |
| `scripts` | automation logic | build, validation, generation, migration |
| `catalog` | generated manifests | machine-readable inventory and indexes |
| `tests` | validation logic | checks, evals, regressions |

## Repository area rule

A file’s location must not contradict its declared role.

For example:

- a repository-wide policy should not live only under `knowledge/`
- a project overview should not primarily live in `references/`
- a generated manifest should not be maintained manually in `docs/`

---

## Layer 2 — Document Type

Document type is one of the most important fields in the taxonomy.

It tells humans and machines **what role the document plays**.

A document should have one dominant type.

## Core document types

### `guide`

#### Purpose
Step-by-step explanation or usage-oriented onboarding.

#### Typical questions it answers
- How do I start?
- How do I perform this task?
- How should I use this repository or feature?

#### Typical location
- `docs/guides/`

#### Examples
- getting started
- how to query the knowledge pack
- how to add a document

---

### `reference`

#### Purpose
Precise, stable definition of rules, structures, contracts, or controlled vocabularies.

#### Typical questions it answers
- What is the official rule?
- What are the allowed values?
- Where does this belong?
- What does this field mean?

#### Typical location
- `docs/reference/`

#### Examples
- taxonomy
- naming conventions
- document types
- citation policy
- repository map

---

### `tutorial`

#### Purpose
Teaching through a worked example or guided scenario.

#### Typical questions it answers
- How do I do this from start to finish?
- What does a complete example look like?

#### Typical location
- `docs/tutorials/`

#### Boundary
A tutorial teaches through an example. It should not replace the authoritative reference.

---

### `runbook`

#### Purpose
Operational procedure for repeated or sensitive work.

#### Typical questions it answers
- What are the steps to execute this safely?
- What do I do during an incident or release?

#### Typical location
- `docs/runbooks/`

#### Examples
- ingestion runbook
- release runbook
- incident response runbook

---

### `policy`

#### Purpose
Mandatory rule set, governance requirement, or safety control.

#### Typical questions it answers
- What is allowed?
- What is forbidden?
- What must be checked?
- What rule governs this behavior?

#### Typical location
- `docs/governance/`
- `ai/policies/` for agent-specific policy

#### Examples
- security policy
- PII policy
- anti-prompt-injection policy

---

### `adr`

#### Purpose
Architecture Decision Record documenting an important decision and its consequences.

#### Typical questions it answers
- Why was this decision made?
- What alternatives were considered?
- What trade-offs were accepted?

#### Typical location
- `docs/adrs/`

---

### `project-overview`

#### Purpose
Canonical summary of a single project.

#### Typical questions it answers
- What is this project?
- What problem does it solve?
- What are its main components?

#### Typical location
- `projects/<slug>/`

---

### `architecture`

#### Purpose
System structure, components, boundaries, and relationships.

#### Typical questions it answers
- How is this system organized?
- What are its major components and data flows?

#### Typical location
- `projects/<slug>/`
- occasionally `docs/architecture/` for repository-wide or cross-cutting architecture

---

### `integration-reference`

#### Purpose
Interfaces, integrations, dependencies, and external connections.

#### Typical questions it answers
- What does this integrate with?
- Which services, APIs, or systems are involved?

#### Typical location
- `projects/<slug>/`

---

### `schema-spec`

#### Purpose
Defines machine-readable data contracts, field meanings, and validation expectations.

#### Typical questions it answers
- What fields are required?
- What are the accepted values?
- How should this output be validated?

#### Typical location
- `ai/schemas/`
- supporting docs in `docs/reference/`

---

### `ai-instruction`

#### Purpose
Defines how an AI system should behave in a specific context or task.

#### Typical questions it answers
- How should the agent respond?
- What checks are required?
- What format must be returned?

#### Typical location
- `ai/`
- sometimes governed supporting material in `prompts/`

#### Boundary
Prompt assets and AI instructions are not automatically the same thing.

---

### `eval-spec`

#### Purpose
Defines evaluation cases, acceptance logic, or evaluation methodology.

#### Typical questions it answers
- How do we verify retrieval quality?
- What failure modes are tested?
- What counts as a pass?

#### Typical location
- `ai/evals/`
- `tests/`

---

### `glossary`

#### Purpose
Defines terms, vocabulary, and controlled meanings.

#### Typical questions it answers
- What does this term mean here?
- Is this term equivalent to another term?

#### Typical location
- `docs/reference/`
- occasionally inside a domain folder if domain-specific

---

## Secondary document types

These may be used when needed, but they should be introduced carefully and with consistent governance.

| Type | Use case |
|---|---|
| `checklist` | concise operational verification |
| `playbook` | strategic or tactical response guidance |
| `source-map` | source traceability and provenance |
| `risk-note` | documented risk or caution area |
| `migration-note` | temporary or transitional migration context |
| `inventory` | enumerated repository contents or counts |
| `catalog-entry` | generated or curated structured listing |

When adding new document types, prefer a small controlled set over uncontrolled proliferation.

---

## Document Type Selection Rules

Use these rules when selecting a type.

### Rule 1
Choose the type based on **the primary reader job**, not on how the writer feels.

### Rule 2
A document should not try to be a guide, policy, and project overview at the same time.

### Rule 3
If a file has more than one dominant purpose, split it.

### Rule 4
A `reference` file should define, not narrate.

### Rule 5
A `guide` file should teach action, not merely list allowed values.

### Rule 6
A `policy` file should be normative and auditable.

---

## Layer 3 — Domain

Domain identifies the thematic, functional, or operational context of a document.

This field improves:

- retrieval filtering
- repository discoverability
- ownership reasoning
- cross-linking
- catalog organization

## Core domain values

### `knowledge-management`

Use for documents about the repository as a knowledge system.

Examples:
- repo map
- taxonomy
- contribution structure
- retrieval discipline

---

### `documentation`

Use for documents about writing, organizing, and maintaining docs.

Examples:
- how to add a document
- style conventions
- document templates

---

### `ai`

Use for content about AI behavior, prompt design, retrieval policy, schemas, evals, or agent systems.

Examples:
- anti-prompt-injection guidance
- retrieval rules
- prompt engineering notes
- output schema docs

---

### `technical`

Use for engineering, architecture, implementation, or systems knowledge that is broader than a single project.

Examples:
- technical domain patterns
- architectural styles
- infrastructure notes

---

### `operations`

Use for operational workflows, support processes, maintenance, release practice, or internal operations.

Examples:
- operational procedures
- governance operations
- incident handling

---

### `business`

Use for strategy, internal business context, organizational logic, or positioning that is not purely commercial collateral.

---

### `commercial`

Use for sales-facing, proposal-facing, or commercial support knowledge.

---

### `products`

Use for product understanding, feature models, product strategy, and cross-product concepts.

---

### `branding`

Use for brand identity, visual language, narrative framing, and brand assets.

---

### `security`

Use for security policy, sensitive-data handling, access control, threat model, or governance with a security focus.

---

### `governance`

Use for ownership, policy, review discipline, standards enforcement, and repository control structures.

---

### `project`

Use only when a document is project-scoped but does not fit a narrower domain and still needs an explicit domain value.

This value should be used carefully. Prefer a more specific domain if available.

---

## Domain usage rules

### Rule 1
Domain should reflect the content, not merely the folder.

### Rule 2
Do not use many domains for one file unless multi-domain classification is formally supported.

### Rule 3
Use the smallest meaningful domain that preserves clarity.

### Rule 4
If a project doc is deeply about security or AI behavior, the `doc_type` may remain project-oriented while the `domain` can reflect the actual focus.

---

## Layer 4 — Status

Status defines the lifecycle state of a document.

This is essential for governance and retrieval ranking.

## Controlled status values

### `draft`

The document exists but is not yet considered fully reliable.

Use when:
- the document is incomplete
- it still needs review
- it is undergoing migration or initial creation

Retrieval guidance:
- may be used cautiously
- should rank lower than active canonical sources

---

### `active`

The document is currently maintained and valid for normal use.

Use when:
- the file is intended for active consumption
- ownership exists
- the content is sufficiently stable

Retrieval guidance:
- normal ranking

---

### `deprecated`

The document is still present for reference, but should not be the preferred source going forward.

Use when:
- a newer canonical replacement exists
- the process or structure changed
- historical access is still useful

Retrieval guidance:
- rank below active replacements
- should explicitly point to the successor when possible

---

### `archived`

The document is retained for history but should not guide current behavior.

Use when:
- historical preservation matters
- active use is not intended

Retrieval guidance:
- exclude from default retrieval when possible
- use only for historical questions or migration forensics

---

### `superseded`

The document has been replaced by a better source.

Use when:
- a direct successor exists
- keeping the record matters

Retrieval guidance:
- do not prefer unless the question is explicitly historical

---

## Status rules

### Rule 1
Every governed document should have a status.

### Rule 2
A deprecated or superseded file should point to the preferred replacement when possible.

### Rule 3
An archived file should not silently participate in normal retrieval ranking.

### Rule 4
Draft does not mean disposable; it still requires safe handling.

---

## Layer 5 — Sensitivity

Sensitivity classifies how carefully the content must be handled.

This matters for:

- retrieval
- quoting
- sharing
- indexing
- AI summarization
- governance and review

## Controlled sensitivity values

### `public`

Content is safe for public disclosure.

Examples:
- intentionally public documentation
- sanitized examples
- publishable general guidance

---

### `internal`

Content is intended for internal use but is not highly restricted.

Examples:
- internal process docs
- repository structure docs
- general operational knowledge

---

### `confidential`

Content requires stronger control and should not be broadly exposed.

Examples:
- sensitive commercial context
- internal strategic documents
- non-public operational detail

---

### `restricted`

Content requires strict handling and minimal exposure.

Examples:
- highly sensitive security detail
- highly restricted customer context
- privileged operational procedures
- material requiring explicit approval to access or quote

---

## Sensitivity rules

### Rule 1
If there is doubt, classify conservatively until reviewed.

### Rule 2
Sensitivity affects retrieval behavior, not only storage.

### Rule 3
A system may retrieve restricted material internally but still must not quote or expose it without authorization.

### Rule 4
Prompt-like content with operational secrets should never be normalized as harmless examples.

---

## Layer 6 — Audience

Audience indicates who the document is meant to serve directly.

## Controlled audience values

### `human`

The file is primarily written for human readers.

### `agent`

The file is intended for AI systems, retrieval pipelines, automated consumers, or machine-validated workflows.

### `human, agent`

The file is intentionally written to support both.

---

## Audience rules

### Rule 1
Audience is not a quality label. A human-facing document may still be useful to agents.

### Rule 2
Documents intended for agents should be especially explicit, structured, and policy-aware.

### Rule 3
Prompt assets should not be marked `agent` unless they are actually governed for that use.

---

## Layer 7 — Canonicality

Canonicality tells whether a document should be treated as a source of truth.

This is one of the most important retrieval signals.

## Controlled canonicality values

### `true`

The document is intended as a maintained source of truth for its topic.

### `false`

The document is supportive, derived, temporary, or otherwise not the primary authority.

If your metadata model uses a boolean field such as `canonical: true|false`, that is sufficient.

If a more expressive model is later needed, it must remain backward compatible or be documented through an ADR.

---

## Canonicality rules

### Rule 1
A canonical document should have ownership, status, and clear scope.

### Rule 2
A derived summary should not be marked canonical merely because it is convenient.

### Rule 3
If multiple files are canonical for the same topic, their boundaries must be made explicit to avoid conflict.

### Rule 4
Canonicality must align with repository placement. A canonical security policy hidden in a random note is a governance failure.

---

## Layer 8 — Citability

Citability defines how the document may be quoted or summarized.

This is important for AI usage, especially where sensitivity or misinterpretation risk exists.

## Controlled citability values

### `full`

The document can be quoted more freely, subject to normal sensitivity constraints.

### `excerpt-only`

Only limited excerpts should be quoted directly; summarization is preferred outside short cited spans.

### `summary-only`

The document should generally be summarized rather than directly quoted.

### `restricted`

The document should not be quoted directly without explicit authorization or special handling.

---

## Citability rules

### Rule 1
Citability does not override sensitivity. A restricted document is still restricted.

### Rule 2
High-risk prompt assets and security policies may require more conservative citability.

### Rule 3
If direct quotes create operational or legal risk, prefer `summary-only` or `restricted`.

---

## Controlled Metadata Field Summary

The taxonomy supports the following high-value metadata fields.

| Field | Purpose | Example |
|---|---|---|
| `id` | unique stable identifier | `reference-taxonomy` |
| `title` | human-readable title | `Taxonomy` |
| `doc_type` | document role | `reference` |
| `domain` | thematic context | `knowledge-management` |
| `tags` | controlled descriptors | `retrieval`, `governance` |
| `version` | document version | `1.0.0` |
| `status` | lifecycle state | `active` |
| `audience` | intended consumer | `human`, `agent` |
| `sensitivity` | handling classification | `internal` |
| `owners` | maintenance responsibility | `capymind-maintainers` |
| `last_updated` | update date | `2026-03-11` |
| `citability` | quoting rule | `excerpt-only` |
| `canonical` | source-of-truth flag | `true` |
| `description` | concise description | `Canonical taxonomy for CapyMind.` |

Not every field needs to carry equal operational weight in every workflow, but the classification model should remain consistent.

---

## Tags

Tags are useful, but only when controlled.

## Tagging principles

### 1. Tags should improve discovery
Use tags that help a real future query.

### 2. Tags should not duplicate obvious metadata
If the title already says “taxonomy” and `doc_type` is `reference`, adding ten redundant tags adds little value.

### 3. Prefer a small, stable vocabulary
Uncontrolled tags degrade search and indexing.

### 4. Use tags for meaningful retrieval hints
Examples:
- `retrieval`
- `prompt-injection`
- `project-index`
- `metadata`
- `governance`

### 5. Avoid vanity or vague tags
Avoid:
- `important`
- `misc`
- `stuff`
- `general`
- `random`

---

## Examples of Correct Classification

## Example 1 — Repository map

```yaml
doc_type: reference
domain: knowledge-management
status: active
sensitivity: internal
audience: [human, agent]
canonical: true
citability: excerpt-only
```

Why:
This file defines a structural repository contract and should be treated as a canonical reference.

---

## Example 2 — How-to guide

```yaml
doc_type: guide
domain: documentation
status: active
sensitivity: internal
audience: [human]
canonical: true
citability: excerpt-only
```

Why:
This file teaches a contribution workflow and is canonical for that task.

---

## Example 3 — Anti-prompt-injection policy

```yaml
doc_type: policy
domain: security
status: active
sensitivity: internal
audience: [human, agent]
canonical: true
citability: summary-only
```

Why:
It is normative, security-relevant, and should be handled carefully in AI contexts.

---

## Example 4 — Project architecture

```yaml
doc_type: architecture
domain: technical
status: active
sensitivity: internal
audience: [human, agent]
canonical: true
citability: excerpt-only
```

Why:
The file explains a project’s technical structure and should rank strongly for architecture questions.

---

## Example 5 — Prompt experiment

```yaml
doc_type: ai-instruction
domain: ai
status: draft
sensitivity: internal
audience: [human]
canonical: false
citability: summary-only
```

Why:
It may be useful as a prompt asset, but should not silently act as live runtime policy.

---

## Anti-Patterns

These classification patterns should be treated as quality problems.

### Anti-pattern 1 — Everything is `guide`
This destroys document role clarity.

### Anti-pattern 2 — Everything is `internal`
This removes meaningful sensitivity distinctions.

### Anti-pattern 3 — Missing status
Without lifecycle state, stale documents look current.

### Anti-pattern 4 — Prompt asset marked canonical without policy review
This creates high retrieval risk.

### Anti-pattern 5 — Domain equals folder name with no thought
This creates weak semantics.

### Anti-pattern 6 — Hundreds of free-form tags
This turns tags into noise.

### Anti-pattern 7 — Canonical documents without owners
This creates governance failure.

---

## Taxonomy and Retrieval

Taxonomy is not only for organization. It directly affects retrieval behavior.

## Retrieval signals improved by taxonomy

- document ranking
- filtering by domain
- filtering by status
- suppression of archived content
- protection for sensitive content
- preference for canonical documents
- routing of policy questions to stronger sources
- better citation choices

## Example retrieval behavior

When answering a security question, prefer:

1. `doc_type: policy`
2. `domain: security`
3. `status: active`
4. `canonical: true`

When answering a project architecture question, prefer:

1. `doc_type: architecture`
2. project-local files
3. `status: active`
4. `canonical: true`

A retrieval system that ignores taxonomy will behave less reliably.

---

## Taxonomy and Governance

Taxonomy also supports governance.

It helps answer:

- Which active docs lack owners?
- Which confidential docs are still directly quotable?
- Which deprecated docs are still retrieved too often?
- Which domains are under-documented?
- Which prompt assets are incorrectly treated as canonical?

Without taxonomy, these questions become expensive and inconsistent to answer.

---

## Change Management for the Taxonomy

This taxonomy should be stable but not frozen.

## Change rules

### Rule 1
Do not add new controlled values casually.

### Rule 2
If a new value is needed, explain:
- why existing values are insufficient
- what repository problem it solves
- how it affects retrieval and governance

### Rule 3
Significant taxonomy changes should be recorded in:
- `CHANGELOG.md`
- an ADR if the change alters repository contracts materially

### Rule 4
Backwards compatibility should be considered whenever automation depends on taxonomy values.

---

## Recommended Minimal Taxonomy Baseline

If the repository is in early migration, the minimum practical baseline is:

- `doc_type`
- `domain`
- `status`
- `sensitivity`
- `audience`
- `canonical`
- `owners`
- `last_updated`

This baseline is enough to improve retrieval and governance meaningfully before more advanced contracts are fully implemented.

---

## Definition of Done

CapyMind taxonomy can be considered operationally healthy when:

- controlled values are documented and stable
- contributors can classify files consistently
- retrieval systems can rank based on taxonomy
- governance workflows use taxonomy fields meaningfully
- active canonical documents are distinguishable from drafts and derived material
- sensitive content can be handled according to classification
- document types remain specific and not overloaded

---

## Related Documents

Read these next:

- `README.md`
- `CONTRIBUTING.md`
- `docs/guides/getting-started.md`
- `docs/guides/how-to-query-the-knowledge-pack.md`
- `docs/guides/how-to-add-a-document.md`
- `docs/reference/repo-map.md`
- `docs/reference/document-types.md`
- `docs/reference/naming-conventions.md`
- `docs/reference/citation-policy.md`
- `docs/governance/security-policy.md`

If any of these files do not exist yet, they should be treated as part of the **minimum metadata and governance baseline** for CapyMind.

---

## Summary

The CapyMind taxonomy defines the shared classification language for the repository.

It standardizes:

- where documents fit conceptually
- what role each document type plays
- how domains are assigned
- how lifecycle and sensitivity are represented
- how canonicality is signaled
- how humans and AI systems interpret repository content safely

This taxonomy is one of the foundation contracts of the knowledge pack.

Without it, the repository becomes harder to navigate, harder to govern, and less reliable for retrieval.

With it, CapyMind gains structure, predictability, and long-term maintainability.
