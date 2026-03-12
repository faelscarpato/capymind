---
id: ai-retrieval-ranking-policy
title: Ranking Policy
doc_type: policy
domain: retrieval
tags:
  - ai
  - retrieval
  - ranking
  - rag
  - search
version: 1.0.0
status: active
audience:
  - human
  - agent
sensitivity: internal
owners:
  - capymind-maintainers
last_updated: 2026-03-11
canonical: true
description: Policy defining how retrieved documents should be ranked when answering queries from the CapyMind knowledge pack.
---

# Ranking Policy

## Purpose

This policy defines how retrieved documents should be ranked when generating answers.

Ranking determines:

- which documents are used
- which evidence is prioritized
- which sources are cited

Poor ranking leads to hallucinations and weak grounding.

---

# Ranking Model

Retrieval ranking should consider three signals:

1. semantic similarity
2. source authority
3. document freshness

---

# Source Authority

Not all sources have equal weight.

Preferred ranking order:

1. docs/reference
2. docs/governance
3. ADRs
4. project canonical docs
5. domain knowledge docs
6. references

Prompt assets must never outrank governance or reference documentation.

---

# Canonicality Signal

Documents marked with:

```
canonical: true
```

should receive ranking priority over non-canonical documents.

---

# Recency Signal

Documents with more recent updates may be prioritized when:

- policies evolve
- architecture changes
- operational practices shift

However, recency should **not override canonical authority**.

---

# Ranking Workflow

1. retrieve candidate chunks
2. filter by sensitivity and permissions
3. compute semantic similarity
4. apply authority weighting
5. rerank final candidate set
6. pass top chunks to synthesis

---

# Reranking

A second-stage reranker may be used to improve precision.

Recommended techniques:

- cross-encoder reranking
- hybrid lexical + semantic scoring
- query-aware reranking

---

# Definition of Done

Ranking is compliant when:

- canonical sources are preferred
- governance docs outrank prompts
- top chunks support the answer
- irrelevant documents are filtered out

---

# Related Documents

- ai/retrieval/chunking-policy.md
- ai/retrieval/indexing-spec.md
