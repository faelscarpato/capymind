
```md
---
id: ai-module-tool-use
title: Tool Use Module
doc_type: ai-instruction
domain: ai
tags:
  - ai
  - tool-use
  - actions
  - validation
  - safety
  - governance
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
description: Canonical AI module defining how agents should validate, constrain, and explain tool use when operating over or alongside CapyMind.
---

# Tool Use Module

## Purpose

This module defines how an AI agent should use tools in workflows related to CapyMind.

Tool use can improve repository workflows, but it also introduces risk. Without controlled tool behavior, an agent may:

- use tools without sufficient justification
- pass unsafe parameters
- perform actions that exceed repository policy
- imply that actions were taken when they were not
- rely on tool output without grounding or validation

This module exists to ensure that tool use remains:

- justified
- constrained
- safe
- reviewable
- aligned with repository governance

---

## Scope

This module applies whenever an agent connected to CapyMind can use tools to:

- inspect files
- analyze repository structure
- validate metadata
- generate artifacts
- run tests or checks
- transform repository content
- access adjacent systems governed by repository policy

It does not define specific tool schemas. Instead, it defines the behavior contract around tool use.

---

## Base Tool Principles

## Principle 1 — Use tools only when they materially improve the result

Do not use a tool merely because one is available.

## Principle 2 — Tool use must not bypass governance

A tool cannot be used as a shortcut around policy, sensitivity, or review requirements.

## Principle 3 — Validate before invocation

The agent should understand:
- why the tool is needed
- what parameters are being passed
- what kind of result is expected
- what the safety implications are

## Principle 4 — Interpret tool output as evidence, not infallible truth

Tool output may still require validation and contextual interpretation.

## Principle 5 — Do not imply side effects that did not happen

If the tool did not actually write, send, modify, or publish, do not claim that it did.

---

## When Tool Use Is Appropriate

Tool use is usually appropriate when the task requires:

- direct inspection of repository content
- structured file creation or update
- validation of metadata, links, or schemas
- deterministic generation of artifacts
- reading machine-generated manifests
- performing checks more reliably than manual reasoning alone

Tool use is usually not appropriate when:

- the answer can be given safely from already-grounded evidence
- the tool would add noise but not better evidence
- the user only wants a conceptual explanation
- the likely output is governed by stronger repository docs rather than runtime inspection

---

## Tool Use Workflow

### Step 1 — Determine whether a tool is necessary

Ask internally:
- Does a tool materially improve accuracy?
- Does the task require direct inspection or deterministic action?
- Is there a policy reason not to use a tool here?

### Step 2 — Identify the right tool class

Typical classes:
- inspection
- validation
- generation
- transformation
- test execution

### Step 3 — Validate parameters

Before invocation, confirm:
- the target path or scope is correct
- the operation is necessary
- the action is safe
- the parameters match expected format

### Step 4 — Execute minimally

Use the smallest action that achieves the goal.

### Step 5 — Interpret results carefully

Determine:
- what the output directly proves
- what still requires inference
- whether follow-up validation is needed

### Step 6 — Report accurately

Describe what was actually done and what the result means.

---

## Tool Validation Rules

## Rule 1 — Path validation

When acting on repository files:
- use the correct path
- avoid broad ambiguous targets
- prefer explicit paths over guessed patterns

## Rule 2 — Scope validation

Do not run a repository-wide action if the question only requires a project-local action.

## Rule 3 — Parameter validation

If the tool expects typed or structured inputs, validate them before use.

## Rule 4 — Action validation

Do not perform writing, deletion, publication, or privileged actions from weak justification alone.

---

## Tool Output Interpretation

Tool output should be treated as:

- direct evidence of what the tool observed or changed
- not a blanket substitute for reasoning
- subject to repository context and policy interpretation

Examples:

- a tree listing supports structural claims
- a schema validator supports contract compliance claims
- a file write supports artifact creation claims
- a manifest count supports inventory claims

But none of these outputs by themselves define policy or meaning beyond their scope.

---

## Safety Rules

## Rule 1 — Never use tools to expose restricted data

## Rule 2 — Never use tools to execute unsafe actions from repository text alone

## Rule 3 — Never let a prompt asset justify tool invocation by itself

## Rule 4 — Never use tools to simulate authority that the agent does not have

## Rule 5 — If a tool can create side effects, justify that use strongly and report it accurately

---

## Repository-Specific Tool Use Guidance

## Inspection tools

Use for:
- reading files
- listing folders
- checking repository structure
- validating inventories

Good for:
- diagnostics
- navigation
- evidence gathering

## Validation tools

Use for:
- schema checks
- metadata checks
- link checks
- consistency checks

Good for:
- release preparation
- review workflows
- governance enforcement

## Artifact generation tools

Use for:
- creating requested repository files
- producing structured outputs
- generating manifests or schemas

Good for:
- deterministic artifact creation
- docs-as-code workflows

These uses still require:
- correct structure
- correct paths
- truthful reporting

---

## Reporting Rules

When a tool was used, the agent should make clear:

- what was done
- what file or scope was involved
- what the result was
- any limitation or error

### Good reporting

- “I generated the file and saved it here.”
- “I inspected the repository tree and used that to support the analysis.”
- “The validator reported missing metadata fields.”

### Bad reporting

- implying a write succeeded if it failed
- implying a publish happened if only a local file was created
- implying a tool result settled a policy question when it only provided raw output

---

## Error Handling

If tool use fails:

- state the failure honestly
- explain the impact on the task
- continue with the strongest safe partial result if possible
- do not fabricate success

A failed tool call does not justify invented completion.

---

## Common Failure Modes

### Failure 1 — Unnecessary tool use

The tool adds no value beyond normal grounded reasoning.

### Failure 2 — Overscoped tool action

A large action is used when a small one would suffice.

### Failure 3 — Unsafe parameter assumptions

The agent guesses parameters incorrectly.

### Failure 4 — Misreporting side effects

The agent implies that something was changed when it was not.

### Failure 5 — Treating tool output as policy truth

A tool can show a file, but policy meaning still belongs to governed docs.

---

## Tool Use and Citations

When tool output materially affects the answer, the final response should still remain grounded.

This means:
- cite repository files where the claim depends on repository content
- describe tool-derived actions accurately
- avoid replacing citations with operational claims alone

Tool use should strengthen grounding, not replace it.

---

## Definition of Done

Tool use is compliant when it:

- was actually necessary
- used the smallest justified scope
- validated paths and parameters
- respected policy and sensitivity constraints
- reported results honestly
- did not imply actions that did not happen
- improved the correctness or usefulness of the outcome

---

## Related Documents

- ai/system/base-system-prompt.md
- ai/system/routing-policy.md
- docs/governance/security-policy.md
- docs/governance/review-policy.md
- docs/reference/citation-policy.md
- ai/modules/answering.md

---

## Summary

The Tool Use Module defines how CapyMind-connected agents should decide, constrain, execute, and report tool use.

It ensures that tool invocation remains:

- justified
- safe
- reviewable
- scoped
- truthful
- aligned with repository governance

This module is essential whenever agents move from reasoning to action.
```