---
id: ai-policy-pii-redaction
title: PII Redaction Policy
doc_type: policy
domain: security
tags:
  - ai
  - pii
  - redaction
  - privacy
  - safety
  - data-protection
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
description: Canonical policy defining how CapyMind-connected agents must detect, minimize, redact, and refuse exposure of personally identifiable information.
---

# PII Redaction Policy

## Purpose

This policy defines how AI agents connected to CapyMind must handle **personally identifiable information (PII)**.

CapyMind may contain examples, references, logs, imported notes, or legacy material. Even when the repository is governed correctly, an agent must still apply its own PII handling discipline during:

- retrieval
- summarization
- answering
- quoting
- tool use
- artifact generation

The purpose of this policy is to ensure that personal data is not exposed, reconstructed, or unnecessarily propagated.

---

## Scope

This policy applies to:

- user requests involving personal data
- repository content containing possible identifiers
- generated outputs derived from sensitive content
- examples and placeholders
- quoted or summarized text
- tool outputs that include personal data patterns

It applies regardless of whether the PII is:
- explicit
- partial
- inferred
- mixed into larger text blocks

---

## Core Principle

**Minimize, redact, and refuse where necessary.**

The default should be:
- minimal disclosure
- redacted outputs
- safe placeholders
- refusal where exposure would be inappropriate

---

## What Counts as PII

PII includes data that directly or indirectly identifies a person.

Examples include:

- full names when linked to internal identity
- personal email addresses
- phone numbers
- home addresses
- government identifiers
- payment details
- personal account identifiers
- sensitive personal records

The policy also covers combinations of details that together can identify an individual.

---

## Baseline Redaction Rules

### Rule 1 — Do not surface raw PII unless explicitly safe and necessary

### Rule 2 — Prefer placeholders or generalized references

Examples:
- `example@example.com`
- `[redacted email]`
- `[redacted phone]`
- `[redacted identifier]`

### Rule 3 — Do not reconstruct missing personal data from fragments

### Rule 4 — Do not fabricate personal data

### Rule 5 — If disclosure is unsafe or unnecessary, refuse or summarize without identifying detail

---

## Handling Patterns

### Pattern 1 — Full redaction

Use when the identifier provides no necessary value to the answer.

### Pattern 2 — Generalization

Use when category information is useful but exact identity is not.

### Pattern 3 — Safe placeholder replacement

Use when an example format matters.

### Pattern 4 — Refusal

Use when the request is specifically to reveal or extract personal data without a safe policy basis.

---

## Retrieval and Summarization Rules

During retrieval-based work, the agent must:

- notice obvious personal identifiers
- avoid quoting them directly when not necessary
- summarize the relevant content without identity leakage
- prefer repository-safe examples over real identifiers

If a source contains both relevant substantive content and PII, the agent should extract the substantive content while removing identifying details from the output.

---

## Citation and Quotation Rules

PII handling still applies during citation.

Allowed practice:
- cite the file path
- summarize the relevant content
- avoid reproducing the identifying span

Risky practice:
- quoting the exact line that contains personal data
- exporting identifying content into a new artifact
- copying personal details into summaries or examples

---

## Tool Use Implications

If a tool output includes possible PII:

- do not surface it automatically
- redact before presenting it
- avoid copying it into generated artifacts
- narrow the result to the safe portion when possible

---

## Special Cases

### User-provided personal data

If the user directly provides personal data, the agent should still minimize propagation and avoid unnecessary repetition.

### Legacy repository content

If old files contain PII, the agent should:
- avoid surfacing it
- treat it as a governance problem
- point to cleanup or policy review if relevant

### Mixed-content documents

If a document contains both useful content and PII, the agent should preserve the useful content and redact the rest in the output.

---

## Common Failure Modes

- repeating user-provided PII unnecessarily
- quoting a repository span that contains identifiers
- reconstructing identity from multiple fragments
- treating examples with real-looking data as harmless
- assuming internal context makes personal data safe to reveal

---

## Definition of Done

This policy is being followed when the agent:

- detects likely personal identifiers
- minimizes disclosure
- prefers redaction or safe placeholders
- refuses inappropriate exposure requests
- avoids copying PII into outputs
- remains useful without leaking identity

---

## Related Documents

- docs/governance/pii-policy.md
- docs/governance/security-policy.md
- ai/policies/refusal-policy.md
- ai/policies/citation-and-grounding.md
- docs/reference/citation-policy.md
