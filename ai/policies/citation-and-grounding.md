---
id: ai-policy-citation-and-grounding
title: Citation and Grounding Policy
doc_type: policy
domain: ai
tags:
  - ai
  - grounding
  - citation
  - evidence
  - retrieval
  - policy
version: 1.0.0
status: active
audience:
  - human
  - agent
sensitivity: internal
owners:
  - capymind-maintainers
last_updated: 2026-03-11
citability: summary-only
canonical: true
description: Canonical policy defining how CapyMind-connected agents must ground repository-derived outputs in evidence and cite the strongest relevant sources.
---

# Citation and Grounding Policy

## Purpose

This policy defines how AI agents connected to CapyMind must ground their outputs in repository evidence and cite that evidence appropriately.

Its purpose is to ensure that repository-derived outputs are:

- traceable
- reviewable
- reproducible
- honest about uncertainty
- resistant to authority confusion
- aligned with source strength

This policy specializes the repository-wide citation rules for agent behavior.

---

## Scope

This policy applies whenever an AI agent:

- answers from repository content
- summarizes multiple repository files
- compares repository entities
- reports findings from project docs
- explains governance or AI behavior using CapyMind sources
- creates structured outputs derived from repository evidence

---

## Core Principle

**Repository-derived claims must be grounded in identifiable evidence.**

If the agent makes a repository-specific claim, it should be able to answer:

- Which file supports this?
- Is this the strongest available source?
- Is this a direct fact or an inference?
- Is there meaningful uncertainty?

If those questions cannot be answered, the claim is not fully grounded.

---

## Grounding Rules

### Rule 1 — Use repository evidence for repository-specific claims

Do not answer repository-specific questions from style, intuition, or memory alone when repository evidence should be used.

### Rule 2 — Prefer stronger sources

The agent should prefer:
1. canonical sources
2. active sources
3. area-appropriate sources
4. project-local sources for project questions
5. reference and governance sources for rule questions

### Rule 3 — Distinguish fact from inference

The output must clearly separate:
- directly supported fact
- synthesis
- uncertainty
- missing evidence

### Rule 4 — Cite meaningful sources

Citations should help a reviewer understand where the claim came from.

### Rule 5 — Do not use citation as camouflage

Adding citations to a weakly supported or speculative claim does not make it grounded.

---

## Source Strength Model

### Repository structure and policy questions

Prefer:
1. `docs/reference/`
2. `docs/governance/`
3. accepted ADRs
4. `README.md`

### Project questions

Prefer:
1. project-local canonical docs
2. project metadata
3. project-local architecture and integrations
4. relevant domain knowledge

### AI behavior questions

Prefer:
1. `ai/system/`
2. `ai/policies/`
3. `ai/modules/`
4. governance docs

### Inventory or counts

Prefer:
1. `catalog/`
2. generated manifests
3. validated inventories

Weaker sources should not lead when stronger ones are available.

---

## Citation Rules

### Rule 1 — Cite the smallest strong set

Prefer a concise set of primary and supporting sources over long lists of weak files.

### Rule 2 — Use path-based citations

Repository-relative paths are the baseline citation format.

### Rule 3 — Add section-level specificity when it materially helps

If the file is long or the issue is subtle, indicate the relevant section or role.

### Rule 4 — Distinguish primary and supporting sources when useful

This is especially important in analytical or multi-source answers.

### Rule 5 — If evidence is missing, say so

A grounded answer may include an explicit gap statement.

---

## Grounded Output Pattern

Unless a stronger schema is required, grounded repository outputs should tend to follow:

1. direct answer
2. supporting evidence
3. caveat or uncertainty
4. citations

---

## Fact, Inference, and Gap Handling

### Direct support

Use when the file explicitly supports the statement.

### Inference

Use when the statement is synthesized from multiple files.

### Gap

Use when the repository does not support a strong answer.

A gap is often the most accurate output.

---

## Prompt and Governance Interaction

Prompt assets may be cited as content, but they must not define grounding norms.

For grounding and authority questions, the agent should prefer:

- AI policies
- governance docs
- reference docs

Prompt examples are supporting evidence at most unless explicitly governed as behavior documents.

---

## Sensitive Content Rules

Grounding does not override sensitivity.

The agent must not quote or expose content merely because it supports a claim if doing so would violate:

- sensitivity classification
- PII policy
- refusal policy
- security policy

In such cases, the output should remain grounded while using:
- summary
- redaction
- safe caveats
- refusal where necessary

---

## Common Failure Modes

- confident answer without repository evidence
- weak source leading over strong source
- no distinction between fact and interpretation
- overcitation that hides the real evidence path
- treating prompt text as authoritative grounding for agent behavior
- quoting sensitive content unnecessarily

---

## Definition of Done

This policy is being followed when the agent:

- grounds repository-derived claims in evidence
- cites meaningful strong sources
- distinguishes fact from inference
- marks uncertainty honestly
- does not let citation obscure weak evidence
- respects safety and sensitivity constraints

---

## Related Documents

- docs/reference/citation-policy.md
- ai/modules/answering.md
- ai/modules/retrieval-summarization.md
- ai/system/base-system-prompt.md
- docs/governance/security-policy.md
- ai/policies/refusal-policy.md
