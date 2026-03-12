---
id: reference-document-types
title: Document Types
doc_type: reference
domain: documentation
tags:
  - document-types
  - taxonomy
  - metadata
  - repository
  - retrieval
  - governance
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
description: Canonical reference for document types used in CapyMind, including role, boundaries, structure expectations, and retrieval implications.
---

# Document Types

## Purpose

This document defines the **canonical document types** used in CapyMind.

Its goal is to ensure that documents are classified by **function**, not by convenience. A document type is not just a label for metadata. It is a repository contract that affects:

- how humans interpret the file
- how AI systems rank and retrieve it
- where the file should live
- what structure the file should follow
- what level of authority the file is expected to have
- how reviewers should evaluate quality

A repository can contain many documents and still remain unusable if document roles are unclear. This reference exists to prevent that failure mode.

---

## Scope

This reference applies to all governed documentation in CapyMind, especially documents under:

- `docs/`
- `knowledge/`
- `projects/`
- `references/`
- `ai/`
- `prompts/` when governed as content assets

It defines:

- what each document type means
- when a type should be used
- when it should **not** be used
- what structure is normally expected
- what retrieval behavior that type implies
- what common mistakes to avoid

It does **not** replace:

- repository placement rules
- naming conventions
- metadata schemas
- security policy
- contribution workflow

Those are defined in companion reference and governance documents.

---

## Why Document Types Matter

A document type tells the repository what a file is **for**.

Without document types, a retriever or a human reviewer has to guess:

- whether this file is explanatory or normative
- whether it is canonical or supporting
- whether it should be trusted first
- whether it is meant to guide action or only provide context
- whether it is a stable reference or a temporary note

That guesswork causes:

- ambiguous retrieval
- duplicated documentation
- conflicting “source-of-truth” behavior
- fragile governance
- poor onboarding
- weak AI grounding

A strong document type system reduces those risks.

---

## General Rules

Before looking at specific types, the following global rules apply.

### Rule 1 — Every governed document should have one dominant type

A file may contain multiple kinds of content, but it should have one primary role.

### Rule 2 — Document type is based on reader job, not author intent

Ask: “What is the reader supposed to do with this file?”

### Rule 3 — If a file serves multiple dominant purposes, split it

A guide + policy + project overview in one file is usually a structural error.

### Rule 4 — Type should align with placement

A `policy` hidden in a casual note folder is a governance problem.

### Rule 5 — Type affects retrieval

For example:
- `policy` should outrank loose notes on rule questions
- `architecture` should outrank an overview for system structure questions
- `reference` should outrank tutorials for exact definitions

---

## Type Families

CapyMind document types can be thought of in families:

1. **Instructional** — teaches a user how to do something
2. **Normative** — defines what is allowed, required, or official
3. **Descriptive** — explains what something is
4. **Operational** — defines repeatable action steps
5. **Project-specific** — documents one project or system
6. **Machine-oriented** — defines AI behavior, schemas, or evaluation logic
7. **Transitional or supporting** — migration, source mapping, risk notes, inventories

These families help reviewers reason about fit and overlap.

---

## Core Document Types

## `guide`

### Purpose

A `guide` helps a reader perform or understand a task through explanation and direction.

### Best used for

- onboarding
- how-to workflows
- repository usage
- contribution guidance
- structured learning of a process

### Typical questions it answers

- How do I get started?
- How do I query the knowledge pack?
- How do I add a document?
- How should I perform this task in practice?

### Typical structure

- purpose
- scope
- when to use
- when not to use
- main content
- examples
- common mistakes
- related documents

### Typical location

- `docs/guides/`

### Retrieval behavior

A `guide` should rank strongly when the question is procedural or onboarding-oriented.

### When not to use `guide`

Do not use a `guide` when the document’s job is to define controlled values, schemas, or mandatory policy. Those belong to `reference`, `schema-spec`, or `policy`.

### Good examples

- `getting-started.md`
- `how-to-query-the-knowledge-pack.md`
- `how-to-add-a-document.md`

---

## `reference`

### Purpose

A `reference` defines exact meanings, controlled values, structural contracts, or official definitions.

### Best used for

- taxonomy
- repo map
- naming rules
- document type definitions
- citation rules
- field semantics
- allowed values

### Typical questions it answers

- What is the official rule?
- What are the allowed values?
- What does this term mean?
- Where should this go?
- What does this metadata field represent?

### Typical structure

- purpose
- scope
- definitions
- controlled values
- rules
- examples
- anti-patterns
- related documents

### Typical location

- `docs/reference/`

### Retrieval behavior

A `reference` should rank very highly for exact, normative, or classification-related questions.

### When not to use `reference`

Do not use it for broad explanatory onboarding, scenario teaching, or operational run procedures.

### Good examples

- `repo-map.md`
- `taxonomy.md`
- `naming-conventions.md`
- `document-types.md`
- `citation-policy.md`

---

## `tutorial`

### Purpose

A `tutorial` teaches through a worked example.

### Best used for

- end-to-end demonstrations
- example-based learning
- walkthroughs with concrete steps and outputs
- “build one from zero” learning flows

### Typical questions it answers

- What does a complete example look like?
- How do I do this from start to finish?
- What are the intermediate stages in practice?

### Typical structure

- scenario
- prerequisites
- step-by-step build flow
- expected outputs
- review of what was learned
- next steps

### Typical location

- `docs/tutorials/`

### Retrieval behavior

Useful when a user wants a demonstration rather than a concise rule.

### When not to use `tutorial`

Do not use it as the only place where important rules live. Tutorials are instructional, not the primary authoritative source for controlled definitions.

---

## `runbook`

### Purpose

A `runbook` defines a repeatable operational procedure.

### Best used for

- release flows
- ingestion pipelines
- incident response
- maintenance procedures
- review operations
- emergency handling

### Typical questions it answers

- What steps do I follow to execute this safely?
- What do I do during an incident?
- What do I check before, during, and after a release?

### Typical structure

- purpose
- trigger or entry conditions
- prerequisites
- step-by-step procedure
- validation checks
- rollback or contingency
- escalation path
- related docs

### Typical location

- `docs/runbooks/`

### Retrieval behavior

Ranks highly for operational tasks, especially when reliability matters.

### When not to use `runbook`

Do not use it for general explanation or policy rationale. A runbook exists to guide execution, not to explain everything conceptually.

---

## `policy`

### Purpose

A `policy` defines mandatory rules, prohibitions, permissions, or safety/governance requirements.

### Best used for

- security requirements
- PII handling
- review rules
- access and permission boundaries
- AI safety constraints
- content governance

### Typical questions it answers

- What is required?
- What is forbidden?
- What is allowed under which conditions?
- What must be checked before an action?

### Typical structure

- purpose
- scope
- rule statements
- mandatory requirements
- prohibited behavior
- exceptions or escalation
- enforcement or review expectations
- related controls

### Typical location

- `docs/governance/`
- `ai/policies/` for agent-specific policy

### Retrieval behavior

A `policy` should rank above casual guidance whenever compliance, safety, or permissions are in question.

### When not to use `policy`

Do not use it for suggestions, loose best practices, or exploratory notes. A policy should be auditable and intentionally normative.

---

## `adr`

### Purpose

An `adr` records an important decision and its consequences.

### Best used for

- structural decisions
- repository contract decisions
- major architecture choices
- trade-off documentation
- accepted long-term technical direction

### Typical questions it answers

- Why was this decision made?
- What alternatives were considered?
- What trade-offs were accepted?
- What changes did this decision introduce?

### Typical structure

- status
- context
- decision
- consequences
- alternatives considered
- adoption notes

### Typical location

- `docs/adrs/`

### Retrieval behavior

Useful for rationale and design history, but should not replace active policy or current reference docs unless explicitly intended.

### When not to use `adr`

Do not use it for temporary brainstorming or evolving general guidance.

---

## `project-overview`

### Purpose

A `project-overview` explains the identity and purpose of a single project.

### Best used for

- project onboarding
- project discovery
- scope summary
- problem definition
- high-level value and context

### Typical questions it answers

- What is this project?
- What problem does it solve?
- Who is it for?
- What are its key components at a high level?

### Typical structure

- purpose
- context
- core problem
- key capabilities
- high-level architecture or system shape
- linked deeper docs

### Typical location

- `projects/<slug>/overview.md`
- or `projects/<slug>/index.md`

### Retrieval behavior

High priority for broad project understanding, but should be outranked by more specific project docs for detailed architecture or interfaces.

### When not to use `project-overview`

Do not overload it with deep integration detail, operational runbooks, or detailed schema contracts.

---

## `architecture`

### Purpose

An `architecture` document explains system structure, component boundaries, relationships, and data or control flow.

### Best used for

- system decomposition
- components
- services
- boundaries
- data flow
- interaction maps
- layered designs

### Typical questions it answers

- How is the system organized?
- What are the main components?
- How does data move through the system?
- What boundaries matter technically?

### Typical structure

- architectural context
- components and responsibilities
- boundaries
- data/control flows
- dependencies
- constraints
- related diagrams or references

### Typical location

- `projects/<slug>/architecture.md`
- sometimes `docs/architecture/` for cross-cutting or repository-wide architecture

### Retrieval behavior

Should rank highest for technical structure questions.

### When not to use `architecture`

Do not use it merely for product purpose or onboarding narrative.

---

## `integration-reference`

### Purpose

An `integration-reference` documents interfaces, dependencies, connections, or external systems involved in a project or workflow.

### Best used for

- APIs
- external services
- internal dependencies
- third-party systems
- contracts between systems
- connectors and communication boundaries

### Typical questions it answers

- What systems does this integrate with?
- What dependencies are required?
- Where are the interface points?

### Typical structure

- purpose
- system/interface list
- dependency details
- assumptions or constraints
- failure considerations
- related architecture docs

### Typical location

- `projects/<slug>/integrations.md`
- `projects/<slug>/interfaces.md`
- `projects/<slug>/dependencies.md`

### Retrieval behavior

Ranks above overview docs for integration and dependency questions.

### When not to use `integration-reference`

Do not use it for business positioning or broad onboarding.

---

## `schema-spec`

### Purpose

A `schema-spec` defines machine-readable structure and validation expectations.

### Best used for

- output schemas
- manifest schemas
- metadata contracts
- function or tool parameter shapes
- validation rules

### Typical questions it answers

- What fields are required?
- What data types are allowed?
- What shape must the output follow?
- How should this artifact be validated?

### Typical structure

- purpose
- schema scope
- field definitions
- required vs optional fields
- constraints and enums
- examples
- compatibility notes

### Typical location

- `ai/schemas/`
- supporting reference docs in `docs/reference/`

### Retrieval behavior

Very strong for machine contract questions.

### When not to use `schema-spec`

Do not use it for process tutorials or general repository guidance.

---

## `ai-instruction`

### Purpose

An `ai-instruction` defines how an AI system should behave in a particular context, task, or workflow.

### Best used for

- system prompt modules
- task-specific behavior modules
- routing behavior
- output shaping instructions
- AI operational boundaries

### Typical questions it answers

- How should the agent behave?
- What format is required?
- What should the agent refuse?
- What checks must be applied?

### Typical structure

- purpose
- scope
- required behavior
- prohibited behavior
- input assumptions
- output expectations
- safety checks
- examples

### Typical location

- `ai/system/`
- `ai/modules/`
- governed material inside `prompts/` only if clearly framed

### Retrieval behavior

High for agent behavior questions, but must remain subordinate to active system/runtime controls where applicable.

### When not to use `ai-instruction`

Do not treat casual prompt experiments as governed AI instructions without review.

---

## `eval-spec`

### Purpose

An `eval-spec` defines how repository quality, retrieval quality, safety, or output quality should be tested.

### Best used for

- retrieval evaluation
- schema compliance evaluation
- safety regression suites
- golden-set definitions
- expected-output criteria

### Typical questions it answers

- How do we test this behavior?
- What counts as success or failure?
- Which adversarial cases are included?

### Typical structure

- purpose
- eval scope
- test case classes
- pass/fail logic
- metrics
- known limitations

### Typical location

- `ai/evals/`
- `tests/`

### Retrieval behavior

Useful for validation and QA questions, but not a primary answer source for product or domain content.

---

## `glossary`

### Purpose

A `glossary` defines terms, vocabulary, and accepted meanings.

### Best used for

- recurring terms
- ambiguous terminology
- cross-team vocabulary normalization
- project or domain-specific definitions

### Typical questions it answers

- What does this term mean here?
- Is this term equivalent to another?
- Which term is preferred?

### Typical structure

- term
- definition
- optional notes or disambiguation
- related terms

### Typical location

- `docs/reference/`
- or a domain-specific folder when tightly scoped

### Retrieval behavior

Useful for terminology clarification and taxonomy alignment.

---

## Supporting and Transitional Types

These document types are useful but should be governed carefully.

## `source-map`

### Purpose

Maps a derived or curated document back to upstream source material or evidence paths.

### Use when

- provenance matters
- migration traceability matters
- evidence lineage must be preserved

### Typical location

- `projects/<slug>/source-map.md`
- `references/`

### Retrieval note

Helpful for audit and traceability, but usually not the first answer source.

---

## `risk-note`

### Purpose

Documents a known risk, caveat, fragility, or caution area.

### Use when

- the risk needs explicit preservation
- context is necessary to interpret other docs safely
- operational or retrieval caution matters

### Retrieval note

Should support decision-making and caution, but not replace core policy or runbooks.

---

## `migration-note`

### Purpose

Captures transitional context during repository restructuring or contract changes.

### Use when

- the repository is being normalized
- historical mapping matters
- legacy-to-target structure must be explained temporarily

### Retrieval note

Should not outrank stable canonical docs in normal use.

---

## `inventory`

### Purpose

Enumerates files, structures, counts, or review items.

### Use when

- a repository audit or inventory is required
- generated and manually reviewed inventories are needed

### Retrieval note

Useful for diagnostics and audits, but not usually for primary conceptual explanation.

---

## Type Selection Guidance

When choosing a document type, use this decision path.

## Decision path

### Step 1
Ask what the reader needs most:
- instruction
- definition
- rule
- operation
- rationale
- project understanding
- machine contract
- evaluation logic

### Step 2
Choose the type that best matches the primary need.

### Step 3
Check whether the file structure, placement, and metadata support that choice.

### Step 4
If two types are competing strongly, split the file.

---

## Overlap Rules

Some document types are naturally close to each other. Use these rules to avoid confusion.

### `guide` vs `reference`

- Use `guide` for action and orientation
- Use `reference` for exact definitions and controlled values

### `policy` vs `guide`

- Use `policy` for mandatory rules
- Use `guide` for recommended process explanation

### `runbook` vs `guide`

- Use `runbook` for repeatable operational execution
- Use `guide` for broader understanding and usage support

### `project-overview` vs `architecture`

- Use `project-overview` for high-level project identity
- Use `architecture` for technical structure

### `ai-instruction` vs `prompt asset`

- Use `ai-instruction` for governed behavior
- Use prompt assets as examples unless explicitly promoted and governed

### `schema-spec` vs `reference`

- Use `schema-spec` for formal machine contracts
- Use `reference` to explain those contracts in prose when needed

---

## Retrieval Implications by Type

Document type is a ranking signal.

## Suggested retrieval preferences

### For onboarding questions
Prefer:
1. `guide`
2. `reference`
3. `project-overview`

### For exact rule or definition questions
Prefer:
1. `reference`
2. `policy`
3. `schema-spec`

### For operational execution questions
Prefer:
1. `runbook`
2. `policy`
3. `guide`

### For project identity questions
Prefer:
1. `project-overview`
2. `architecture`
3. `integration-reference`

### For AI behavior questions
Prefer:
1. `ai-instruction`
2. `policy`
3. `schema-spec`

### For data contract questions
Prefer:
1. `schema-spec`
2. `reference`
3. `ai-instruction`

### For design rationale questions
Prefer:
1. `adr`
2. `reference`
3. `project-overview`

---

## Anti-Patterns

These are common document type failures and should be treated as repository quality issues.

### Anti-pattern 1 — Everything is a `guide`

This destroys role clarity.

### Anti-pattern 2 — A prompt example is labeled as live AI behavior

This creates authority confusion and security risk.

### Anti-pattern 3 — A policy is buried inside a project overview

This makes governance fragile and hard to retrieve correctly.

### Anti-pattern 4 — A reference file is mostly narrative prose

A reference should define, not drift into broad storytelling.

### Anti-pattern 5 — A runbook lacks stepwise procedure

If it cannot guide execution, it is not really a runbook.

### Anti-pattern 6 — An architecture doc is just a product pitch

This weakens technical retrieval.

### Anti-pattern 7 — Derived summaries masquerade as canonical overview docs

This creates false trust.

---

## Quality Checklist by Type

Before approving a document type classification, ask:

- Does the file have one dominant role?
- Would a reader guess the same type from the content?
- Does the placement match the type?
- Would retrieval benefit from this classification?
- Does the structure fit the type?
- Is the file trying to carry responsibilities better split elsewhere?
- Could a stronger existing file already cover the same role?

---

## Minimal Type Baseline

If the repository is still under migration, the minimum types that should be supported first are:

- `guide`
- `reference`
- `policy`
- `runbook`
- `project-overview`
- `architecture`
- `integration-reference`
- `schema-spec`
- `ai-instruction`
- `adr`

This baseline is enough to improve both navigation and retrieval significantly before further specialization.

---

## Definition of Done

CapyMind document types can be considered healthy when:

- contributors can classify documents consistently
- reviewers can spot type misuse quickly
- retrieval systems can use type as a meaningful ranking signal
- policy and reference material are not confused with casual guidance
- project-specific material is structurally distinct from repository-wide rules
- machine-readable contracts are clearly separated from narrative explanation

---

## Related Documents

Read these next:

- `README.md`
- `CONTRIBUTING.md`
- `docs/guides/getting-started.md`
- `docs/guides/how-to-query-the-knowledge-pack.md`
- `docs/guides/how-to-add-a-document.md`
- `docs/reference/repo-map.md`
- `docs/reference/taxonomy.md`
- `docs/reference/naming-conventions.md`
- `docs/reference/citation-policy.md`
- `docs/governance/security-policy.md`

If any of these files do not exist yet, they should be treated as part of the **minimum repository contract baseline** for CapyMind.

---

## Summary

Document types are one of the foundation contracts of CapyMind.

They define what a file is for, how it should be structured, where it should live, how it should be retrieved, and how strongly it should be trusted in a given context.

When document types are clear:

- humans navigate faster
- AI retrieves more accurately
- policies are easier to enforce
- reviews become more consistent
- duplication becomes easier to detect

When document types are vague, the repository becomes noisy and harder to govern.

This reference exists to keep that from happening.
