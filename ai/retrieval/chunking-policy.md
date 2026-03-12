---
id: ai-retrieval-chunking-policy
title: Chunking Policy
doc_type: policy
domain: retrieval
tags:
  - ai
  - retrieval
  - rag
  - chunking
  - indexing
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
description: Policy defining how repository documents should be segmented into chunks for retrieval and embedding pipelines.
---

# Chunking Policy

## Purpose

This document defines how CapyMind documents must be segmented into **retrieval chunks** for use in:

- vector search
- hybrid search
- RAG pipelines
- semantic retrieval systems

Correct chunking is essential to ensure that:

- context is preserved
- embeddings remain meaningful
- retrieval precision stays high
- answers remain grounded in the correct document sections

---

# Core Principles

## Preserve semantic boundaries

Chunks should respect:

- headings
- sections
- lists
- tables
- code blocks

Do **not split in the middle of a logical unit** when avoidable.

---

## Maintain contextual coherence

Each chunk must contain enough context to stand on its own.

Ideal chunk should include:

- heading
- supporting paragraph
- relevant list or explanation

Chunks without context degrade retrieval quality.

---

## Avoid oversized chunks

Very large chunks reduce retrieval precision.

Recommended chunk size:

- **400–900 tokens**
- target around **600 tokens**

Hard upper limit:

- **1200 tokens**

---

# Chunk Boundary Rules

Chunk boundaries should align with:

1. section headings
2. subsection headings
3. paragraph groups
4. list groups
5. table blocks
6. code blocks

Never split:

- code blocks
- tables
- schema definitions

These must remain intact.

---

# Metadata Requirements

Each chunk must store metadata fields:

- document_id
- path
- section_title
- chunk_index
- token_count
- document_type
- sensitivity

Example metadata:

```json
{
  "path": "docs/reference/repo-map.md",
  "section": "Repository Structure",
  "chunk_index": 2
}
```

---

# Chunk Overlap

Small overlaps improve retrieval continuity.

Recommended overlap:

- **60–120 tokens**

Overlap should occur only between adjacent chunks.

---

# Special Document Handling

## Policies and ADRs

Policy and governance documents should prioritize **section-level chunking**.

## Tutorials

Tutorials should preserve **step groups** within the same chunk.

## Schemas

Schema blocks should remain intact as a single chunk.

---

# Definition of Done

Chunking is considered correct when:

- chunks preserve semantic structure
- context is understandable without previous chunks
- token limits are respected
- metadata fields are present
- no code blocks or tables are fragmented

---

# Related Documents

- ai/retrieval/indexing-spec.md
- ai/retrieval/ranking-policy.md
- ai/policies/citation-and-grounding.md
