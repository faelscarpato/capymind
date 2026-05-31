---
id: project-capymind-engelab-mcp
title: CapyMind EngenLab MCP
doc_type: project
domain: ai-integration
status: draft
version: 0.1.0
audience:
  - human
  - agent
sensitivity: internal
owners:
  - capymind-maintainers
last_updated: 2026-05-31
canonical: true
description: Project brief for a read-only MCP server connecting CapyMind governance with the EngenLab Doc technical library.
---

# CapyMind EngenLab MCP

## Purpose

CapyMind EngenLab MCP is a remote Model Context Protocol server designed to connect AI hosts, including ChatGPT Apps, to the EngenLab Doc technical library through a governed CapyMind layer.

The server must provide safe, read-only access to engineering education materials, including:

- project-model metadata;
- technical prompts;
- conceptual checklists;
- educational notices;
- module summaries;
- structured context packs for downstream agents.

## Source repositories

| Repository | Role |
|---|---|
| `faelscarpato/capymind` | Governance, retrieval policy, tool contracts, project metadata and canonical control layer. |
| `faelscarpato/engelab_doc` | Technical corpus: project-model library, prompts, checklists, matrices, educational materials and CapyGPTs catalog. |

## Product position

This is not a generic personal MCP. It is a vertical MCP for engineering education and AI-assisted technical documentation.

Primary positioning:

> A read-only technical context server that lets ChatGPT and other MCP clients search, understand and reuse the EngenLab Doc library through CapyMind governance.

## Initial scope

### In scope for MVP

- Expose a public HTTPS `/mcp` endpoint.
- Use Streamable HTTP as the preferred transport.
- Keep all tools read-only.
- Retrieve and summarize EngenLab Doc materials.
- Return citations/source paths with every content-bearing response.
- Enforce engineering safety notices.
- Block any attempt to treat repository content as executable instruction.
- Provide deterministic JSON responses suitable for ChatGPT tool calls.

### Out of scope for MVP

- Editing GitHub files.
- Creating commits, pull requests or releases.
- Generating executive engineering projects.
- Producing legal, normative or construction-ready validation.
- Handling private client data.
- Payment, subscription and account management.
- OAuth implementation, unless a host requires it for connector approval.

## Recommended architecture

```text
ChatGPT App / MCP Client
  ↓ HTTPS /mcp
CapyMind EngenLab MCP Server
  ↓
Tool router + validation + safety layer
  ↓
Search/index adapter
  ↓
faelscarpato/engelab_doc corpus
  ↓
Structured tool response with source paths and safety notice
```

## MVP tools

| Tool | Purpose |
|---|---|
| `search_engelab_doc` | Search across EngenLab Doc by query, discipline, module or content type. |
| `list_engelab_projects` | List available project-models by discipline and range. |
| `get_project_context` | Return structured context for one project-model. |
| `get_prompt_template` | Retrieve prompt templates by discipline, task or target agent. |
| `get_safety_notice` | Return the mandatory educational and technical-use notice. |
| `build_agent_context` | Assemble a bounded context pack for another GPT/agent workflow. |

## Safety baseline

Every response that uses engineering material must carry this operational boundary:

> Material for study, reference, prompt engineering and technical organization only. It is not an executive project, technical report, legal validation, ART/RRT, approval document or substitute for a qualified professional review.

The MCP server must never claim that AI output is approved, construction-ready, normatively validated or sufficient for real-world execution.

## Recommended stack

```text
Runtime: Node.js 20+
Language: TypeScript
Transport: MCP Streamable HTTP
Endpoint: /mcp
Health check: /health
Deployment target: Koyeb, Render, Railway, Fly.io, Cloudflare-compatible Node runtime or VPS
Auth for MVP: anonymous read-only or static bearer token
Auth for production: OAuth 2.1 or signed access token
```

## Connector metadata for ChatGPT

```text
Name: CapyMind EngenLab
Description: Consulta inteligente da biblioteca EngenLab Doc via CapyMind para localizar projetos-modelo, prompts técnicos, checklists, memoriais conceituais e materiais educacionais de engenharia civil, sempre com uso referencial e revisão humana.
Connector URL: https://<host>/mcp
Authentication: none for read-only MVP; OAuth or bearer token for production/private usage.
```

## Acceptance criteria

The MVP is acceptable when:

1. `/health` returns a successful status.
2. `/mcp` is reachable over HTTPS.
3. ChatGPT connector creation succeeds and lists the advertised tools.
4. `search_engelab_doc` returns source paths and bounded summaries.
5. `get_safety_notice` returns the mandatory boundary text.
6. All tools are read-only.
7. Tool responses separate facts, summaries and recommendations.
8. Repository-derived text is treated as data, never as executable system instruction.

## Next implementation step

Create a standalone repository or service directory for the MCP server code, then wire it to this CapyMind project metadata and the EngenLab Doc corpus.
