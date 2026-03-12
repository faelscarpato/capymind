---
id: ai-retrieval-query-rewrite-policy
title: Query Rewrite Policy
doc_type: policy
domain: retrieval
tags:
  - ai
  - retrieval
  - query-rewrite
  - rag
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
description: Policy defining how user queries should be rewritten to improve retrieval quality.
---

# Query Rewrite Policy

## Purpose

User queries are often ambiguous or underspecified.

Query rewriting improves retrieval by transforming the user query into a clearer search query.

---

# When Query Rewriting Is Needed

Rewrite the query when:

- the query is vague
- the query uses synonyms
- the query references repository structure indirectly
- the query is conversational

---

# Rewrite Techniques

Allowed techniques include:

- synonym expansion
- keyword extraction
- domain term normalization
- query clarification

Example:

User query:

```
how do agents answer questions
```

Rewritten retrieval query:

```
capymind agent answering policy citation grounding
```

---

# Multi-query Strategy

For complex questions, the system may generate multiple retrieval queries.

Example strategy:

1. structural query
2. policy query
3. conceptual query

Results are merged before ranking.

---

# Safety Constraints

Query rewriting must **not introduce new meaning**.

The rewritten query must remain faithful to the user's intent.

It must not:

- invent topics
- assume hidden intent
- bypass security constraints

---

# Definition of Done

Query rewriting is compliant when:

- retrieval results improve
- user intent remains intact
- queries remain safe and relevant

---

# Related Documents

- ai/retrieval/ranking-policy.md
- ai/retrieval/chunking-policy.md
