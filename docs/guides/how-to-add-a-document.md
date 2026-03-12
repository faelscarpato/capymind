---
id: guide-add-document
title: How to Add a Document
doc_type: guide
domain: documentation
tags:
  - docs-as-code
  - contribution
  - documentation
  - metadata
  - governance
  - quality
version: 1.0.0
status: active
audience:
  - human
sensitivity: internal
owners:
  - capymind-maintainers
last_updated: 2026-03-11
citability: excerpt-only
canonical: true
description: Guide for creating, structuring, validating, and submitting new documents to CapyMind without degrading repository quality, retrieval quality, or safety.
---

# How to Add a Document

## Purpose

This guide explains how to add a new document to CapyMind in a way that preserves:

- repository structure
- retrieval quality
- canonical source clarity
- maintainability
- safety for human and AI consumption

Adding a document is not just “creating a markdown file”.

In CapyMind, every new document changes the behavior of the repository as a knowledge system. A bad document creates ambiguity, duplication, retrieval noise, and maintenance cost. A good document improves discoverability, trust, and long-term reuse.

This guide defines:

- when a new document should exist
- where it should live
- how it should be named
- how metadata should be written
- how content should be structured
- what safety and quality checks are required
- how review and submission should work

---

## Scope

This guide applies to all manually created or maintained documentation added to CapyMind, including documents under:

- `docs/`
- `knowledge/`
- `projects/`
- `references/`
- `ai/`
- `prompts/` when they are treated as governed content assets

It applies to:

- new files
- major rewrites
- promoted documents that become canonical
- migrations from legacy content into structured content

It does **not** fully define:

- repository-wide release management
- CI implementation details
- schema design in depth
- automated indexing internals

Those should be handled in dedicated reference and governance documents.

---

## Core Principle

### Add knowledge, not noise

The default question before adding a document should be:

**Does this information deserve a new canonical file, or should an existing file be improved instead?**

A repository grows stronger when new documents add:

- unique value
- clearer ownership
- better retrieval paths
- better structure
- better evidence

A repository gets worse when new documents add:

- duplication
- weak summaries
- ambiguous naming
- speculative content without context
- prompt-like instructions without safety framing

---

## Before Creating a New Document

Before you create a file, answer these questions.

### 1. Does this information already exist?

Search for:

- similar titles
- similar topics
- project-local equivalents
- domain notes covering the same issue
- older docs that should be updated instead of duplicated

If an equivalent canonical document already exists, update it instead of creating a second source of truth.

---

### 2. Is the document necessary?

Create a new document only if at least one of these is true:

- a new concept needs its own stable explanation
- the current document is overloaded and should be split by responsibility
- a project requires a dedicated document type
- a policy or reference needs an explicit canonical home
- the new file will make retrieval or maintenance meaningfully better

Do **not** create a new file only because:

- it feels easier than editing an existing one
- you want to draft something without deciding ownership
- you want a personal variation of an existing explanation
- you want to park raw notes in a canonical area

---

### 3. Who owns this document?

Every meaningful document should have a review owner or owning group.

If ownership is unknown, the file is at high risk of becoming stale.

At minimum, determine:

- who can validate the content
- who should review future changes
- who should be contacted when the document becomes outdated

---

### 4. Is the document canonical or derived?

This decision must be made before writing.

### Canonical document

Use when the document is intended to be a source of truth.

Examples:

- a guide
- a policy
- a project overview
- a runbook
- a reference specification
- an accepted ADR

### Derived document

Use when the document summarizes or transforms other material.

Examples:

- extracted notes
- generated summaries
- migration leftovers
- review queues
- temporary consolidation docs

If the document is derived, it must not pretend to be authoritative.

---

### 5. Is the content safe to store?

Do not add content that includes:

- credentials
- tokens
- private keys
- passwords
- raw personal data
- secrets copied from tools or environments
- sensitive instructions without policy framing
- prompt content that could be confused with active authority

If the material is sensitive, it must be classified, minimized, redacted, or excluded.

---

## Decide the Correct Location

A document should live where a future reader would naturally expect to find it.

Choosing the wrong folder is one of the fastest ways to degrade retrieval quality.

## Use this location model

### `docs/`

Use for canonical documentation about how the repository, policies, processes, and standards work.

Good examples:

- guides
- references
- tutorials
- runbooks
- governance policies
- ADRs

Use `docs/` when the goal is **clarity and repository-level authority**.

---

### `knowledge/`

Use for domain-level knowledge that is broader than one project.

Good examples:

- technical domain notes
- AI patterns
- business context
- operations knowledge
- product themes

Use `knowledge/` when the goal is **curated understanding across topics or systems**.

---

### `projects/`

Use for documents tied to one specific project, system, product, or codebase.

Good examples:

- project overview
- architecture
- integrations
- dependencies
- runbook
- risk notes
- project metadata

Use `projects/` when the answer to “what is this about?” is a specific project name.

---

### `references/`

Use for supporting material that is useful but not necessarily the first canonical source.

Good examples:

- external references
- source mapping
- commercial references
- inspiration archives
- technical notes imported for context

Use `references/` carefully. It should not silently become the main source of truth.

---

### `ai/`

Use for documents that define agent behavior or machine-readable contracts.

Good examples:

- system modules
- retrieval policy
- anti-injection policy
- output schemas
- eval guidance
- tool-use contracts

Use `ai/` when the document is about **how AI should behave or validate repository knowledge**.

---

### `prompts/`

Use for prompt assets and examples.

This area is useful but high-risk. Prompt documents often contain imperative language. They should be handled as content assets, not automatically active instructions.

---

## Decide the Document Type

A file should have one dominant document type.

Common document types include:

- `guide`
- `reference`
- `tutorial`
- `runbook`
- `policy`
- `adr`
- `project-overview`
- `architecture`
- `integration-reference`
- `ai-instruction`
- `schema-spec`
- `glossary`

The document type affects:

- structure
- expectations
- retrieval ranking
- how AI systems interpret relevance

If a file is trying to be a guide, a policy, a project overview, and a brainstorming note all at once, it should probably be split.

---

## Naming Conventions

Naming is part of retrieval quality.

## File names should be:

- specific
- stable
- readable
- predictable
- written in `kebab-case`

### Good examples

- `getting-started.md`
- `citation-policy.md`
- `project-overview.md`
- `anti-prompt-injection.md`
- `release-runbook.md`

### Weak examples

- `final-doc.md`
- `notes-new.md`
- `important-info.md`
- `random.md`
- `draft-v2-final-ok.md`

### Why naming matters

A strong file name helps:

- search
- linkability
- indexing
- human scanning
- retrieval ranking

Ambiguous names create long-term confusion.

---

## Metadata Requirements

CapyMind documents should use structured frontmatter.

Metadata is not optional decoration. It is part of the document contract.

## Minimum frontmatter example

```yaml
---
id: guide-add-document
title: How to Add a Document
doc_type: guide
domain: documentation
tags:
  - docs-as-code
  - contribution
version: 1.0.0
status: active
audience:
  - human
sensitivity: internal
owners:
  - capymind-maintainers
last_updated: 2026-03-11
citability: excerpt-only
canonical: true
description: Guide for adding new documents to CapyMind.
---
```

## Minimum expected fields

### `id`
A unique identifier. It should be stable and unambiguous.

### `title`
Human-readable title.

### `doc_type`
What kind of document this is.

### `domain`
The thematic or operational domain.

### `tags`
Controlled descriptors to improve indexing and discovery.

### `version`
Document version.

### `status`
Typical values include:

- `draft`
- `active`
- `deprecated`
- `archived`

### `audience`
Who the document is for.

Examples:

- `human`
- `agent`

### `sensitivity`
Expected classification, such as:

- `public`
- `internal`
- `confidential`
- `restricted`

### `owners`
The person or group responsible for maintenance.

### `last_updated`
Most recent meaningful update date.

### `citability`
How the document should be quoted or summarized.

### `canonical`
Whether the document is intended as a source of truth.

### `description`
Short summary for humans and indexing systems.

---

## Writing the Document

Once location, type, and metadata are decided, write the content.

## Core writing rules

### 1. One clear responsibility per file

A document should solve one primary problem.

### 2. Write for future readers

Assume the reader does **not** share your immediate context.

### 3. Prefer explicit statements

Avoid vague phrases such as:

- “this thing”
- “the usual flow”
- “as discussed before”
- “the default way”
- “obvious setup”

### 4. State limits clearly

A good document says both:

- when it should be used
- when it should not be used

### 5. Prefer structured sections

A predictable structure improves scanning and retrieval.

### 6. Avoid padded narrative

Do not write long intros that add no operational value.

### 7. Separate fact from interpretation

If something is inferred rather than directly supported, say so.

---

## Recommended Structure by Default

Not every document uses the same sections, but this is a strong baseline for many guides and references.

```md
# Title

## Purpose
What problem this document solves.

## Scope
What is included and excluded.

## When to Use
Where this document applies.

## When Not to Use
Limits and boundaries.

## Main Content
The actual guidance, reference, or explanation.

## Examples
Concrete examples.

## Risks or Common Mistakes
Pitfalls and failure modes.

## Related Documents
Where to go next.
```

For project docs, the structure may differ.

For policy docs, safety boundaries may need to appear earlier.

For runbooks, operational steps and preconditions may need to lead.

---

## Writing for AI Consumption

CapyMind is designed to be used by AI systems as well as humans.

That means your document should be understandable to a retriever, not just to a teammate who already knows the context.

## Good AI-friendly writing traits

- direct titles
- explicit headings
- clearly named entities
- consistent terminology
- explicit relationships
- minimal ambiguity
- scannable structure
- traceable claims

## Weak AI-friendly writing traits

- vague aliases
- mixed concepts in one section
- unexplained references
- inconsistent naming
- hidden assumptions
- imperative language without context

---

## Safety Requirements

Every new document must be reviewed for safety.

## Never include

- credentials
- secrets
- API tokens
- access keys
- passwords
- private personal data
- copied internal secrets from tools or logs

## Use caution with

- prompt content
- system instructions
- sensitive architecture details
- internal customer data
- copied transcripts
- environment-specific filesystem paths
- operational notes that imply privileged actions

## Prompt-like content rule

If the document contains prompt material, explicitly frame it as:

- example content
- reference content
- archived content
- analysis content

Do not let it look like globally valid runtime authority.

---

## Canonical vs Derived Writing Rules

### If the document is canonical

It should:

- be reviewed
- have complete metadata
- avoid unresolved placeholders
- avoid speculative language unless clearly marked
- establish source-of-truth status

### If the document is derived

It should:

- identify its source inputs when possible
- avoid pretending to be the source of truth
- clearly state that it is a summary, extract, or temporary synthesis
- link readers toward the stronger canonical source

---

## Avoiding Duplication

Duplication is one of the biggest repository quality problems.

## Before you add a new document, check for:

- another file with the same topic
- older files with similar purpose
- project docs that already cover the issue
- domain docs that already define the concept
- outdated summaries that should be merged or retired

## Acceptable reasons to split content

- one file has too many responsibilities
- a project needs a dedicated operational doc
- a policy needs its own canonical page
- a reference has become too large and should be modularized

## Unacceptable reasons to split content

- avoiding edits to an existing file
- creating personal preference versions
- temporary uncertainty about document ownership
- not wanting to resolve contradictions

---

## Examples of Good Document Decisions

### Example 1 — Add a guide

Situation:
There is no canonical onboarding guide for the repository.

Correct action:
Create `docs/guides/getting-started.md`.

Why:
The repository needs a stable onboarding entry point.

---

### Example 2 — Update instead of creating

Situation:
A project overview exists but is missing one integration detail.

Correct action:
Update the existing overview or integration file.

Why:
A new file would create competing project descriptions.

---

### Example 3 — Split an overloaded file

Situation:
A single document mixes naming rules, metadata schema, and contribution workflow.

Correct action:
Split into:
- naming conventions
- metadata reference
- contribution guide

Why:
Each document gets a clear purpose and retrieval improves.

---

### Example 4 — Do not add unsafe content

Situation:
You have a raw prompt dump copied from an experiment with imperative instructions and sensitive examples.

Correct action:
Do not store it as canonical documentation.
Redact, classify, move to a governed area, or exclude it.

Why:
It creates safety and retrieval risk.

---

## Review Your Document Before Submission

Use this checklist before opening a pull request.

## Structural review

- Is the file in the correct folder?
- Is the file name specific and in kebab-case?
- Is the document type clear?
- Does the content have one dominant responsibility?

## Metadata review

- Is frontmatter present?
- Is `id` unique?
- Is `title` clear?
- Is `doc_type` correct?
- Is `domain` correct?
- Are tags useful and not noisy?
- Is `status` correct?
- Is `sensitivity` correct?
- Is ownership declared?
- Is `last_updated` accurate?

## Content review

- Does the document solve a real problem?
- Is it easy to scan?
- Does it define scope and limitations?
- Does it avoid unsupported claims?
- Does it avoid duplication?
- Does it point to related stronger sources when needed?

## Safety review

- Are secrets absent?
- Is sensitive content handled correctly?
- Is prompt-like content framed safely?
- Could an AI misread any section as runtime authority?
- Are unsafe examples clearly labeled?

---

## Criteria for “Ready to Merge”

A document should be considered ready when:

- its location is correct
- its purpose is clear
- metadata is complete
- content is structurally sound
- duplication risk is low
- safety review is acceptable
- related docs are referenced where useful
- the change improves repository quality rather than just increasing file count

A document is **not** ready if it is merely “written”.

It must also be:

- classifiable
- reviewable
- retrievable
- maintainable
- safe

---

## Submission Workflow

Once the document is ready:

1. create or update the file in the correct location
2. validate formatting and metadata
3. review links and related document references
4. commit with a clear message
5. open a pull request
6. request review from the relevant owner or maintainer
7. incorporate review feedback
8. merge only after quality and safety concerns are resolved

## Example commit messages

- `docs: add getting started guide for capymind`
- `docs: add citation policy reference`
- `docs: create project overview for capyvision`
- `docs: split contribution guidance from metadata reference`

Avoid vague commit messages such as:

- `update docs`
- `fix file`
- `new stuff`
- `changes`

---

## What to Do After Merge

After the document is merged:

- verify it is discoverable from the expected entry points
- update related docs if navigation changed
- update changelog if the change affects repository behavior
- check whether an index, manifest, or catalog should be regenerated
- monitor whether the new file created confusion or improved clarity

A merged file that nobody can find is not a successful addition.

---

## Common Failure Modes

These are the most common mistakes when adding documents.

### 1. Creating a new file instead of updating the canonical one

This creates competing source-of-truth paths.

### 2. Using weak or generic titles

This hurts search and indexing.

### 3. Missing metadata

This breaks classification and ranking.

### 4. Mixing multiple responsibilities

This makes the file hard to maintain and hard to retrieve accurately.

### 5. Writing for insiders only

This makes the document unreadable to future readers and AI systems.

### 6. Including prompt-like language without safety framing

This creates injection risk.

### 7. Adding derived summaries that look canonical

This creates false authority.

### 8. Leaving the file disconnected

A document with no incoming navigation path is often effectively invisible.

---

## Suggested Document Quality Standard

A strong CapyMind document should be:

- **specific** in scope
- **structured** in layout
- **owned** by someone
- **traceable** to a source or domain
- **safe** for retrieval
- **easy to cite**
- **easy to update**
- **easy to find**

If a file fails most of these tests, it should be reworked before becoming canonical.

---

## Decision Tree

Use this simplified decision tree before adding a document.

```text
Do I need a new file?
  ├─ No -> improve an existing canonical file
  └─ Yes
      ├─ Is the location clear?
      │   ├─ No -> resolve folder and document type first
      │   └─ Yes
      ├─ Is ownership known?
      │   ├─ No -> identify an owner before making it canonical
      │   └─ Yes
      ├─ Is the content safe and non-duplicative?
      │   ├─ No -> redact, merge, or reframe
      │   └─ Yes
      └─ Add metadata, write clearly, review, submit
```

---

## Definition of Done

A new document can be considered successfully added when:

- it lives in the correct folder
- the filename is stable and specific
- metadata is complete
- its role in the repository is clear
- it does not duplicate a stronger source
- it is safe for human and AI consumption
- it is linked from the appropriate entry points when needed
- it passed review and is maintainable over time

---

## Related Documents

Read these next:

- `README.md`
- `CONTRIBUTING.md`
- `docs/guides/getting-started.md`
- `docs/guides/how-to-query-the-knowledge-pack.md`
- `docs/reference/repo-map.md`
- `docs/reference/naming-conventions.md`
- `docs/reference/document-types.md`
- `docs/reference/citation-policy.md`
- `docs/governance/security-policy.md`
- `ai/policies/anti-prompt-injection.md`

If one or more of these files do not exist yet, they should be treated as part of the **minimum documentation governance baseline** for CapyMind.

---

## Summary

Adding a document to CapyMind is a repository design decision, not just a writing task.

A good addition:

- solves a real information problem
- lives in the correct place
- uses clear metadata
- avoids duplication
- improves retrieval
- respects governance
- is safe for AI consumption

That is the standard required to keep CapyMind coherent as a real knowledge pack rather than a growing pile of markdown files.
