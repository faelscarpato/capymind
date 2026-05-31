# Old audits archive

This directory records cleanup decisions for legacy root-level audit and migration files that were removed from the active repository root.

The original files remain available in Git history. They were removed from the active root because the current canonical structure is now defined by:

- `README.md`
- `apps/capymind-engelab-mcp/`
- `projects/capymind-engelab-mcp/`
- `projects/capymind-engelab-mcp/agents/`
- `ai/`, `catalog/`, `docs/`, `knowledge/`, `references/`, `scripts/`, `tests/`

Moved/retired root-level historical files:

- `IMPLEMENTATION_AUDIT.md`
- `CLEANUP_PLAN.md`
- `HEAVY_CONTENT_REPORT.md`
- `MIGRATION_PLAN.md`
- `FINAL_TREE.txt`
- `PROPOSED_TREE.txt`
- `FILE_MANIFEST.csv`
- `INGESTION_LOG.md`

Operational note: these files described earlier migration and heavy-content sanitization work. They are no longer the active source of truth for the CapyMind EngenLab MCP or the PromptDesk agent catalog.
