# IMPLEMENTATION_AUDIT — Fase 0

**Repositório**: CapyMind  
**Data**: 2026-04-24  
**Agente**: Kilo (implementation agent)  
**Status**: auditoria concluída — escopo definido

---

## Objetivo desta fase

Entender o estado real do repositório antes de implementar, evitando "achismo de IA".

---

## Estrutura encontrada (árvore real)

```
capymind-main/
├── Agent.md                           (arquivo de instrução do agente)
├── README.md                          (visão geral, princípios, escopo)
├── PROJECT_CATALOG.md                 (catalogo textual de projetos)
├── INVENTORY.md                       (inventário resumido)
├── MCP_GUIDE.md                       (guia de navegação para agentes)
├── llms.txt                           (índice público de navegação)
├── llms-full.txt                      (índice expandido)
├── CHANGELOG.md
├── CONTRIBUTING.md
├── VERSION
├── REPO_RULES.md
├── REVIEW_QUEUE.md
├── HEAVY_CONTENT_REPORT.md
├── INGESTION_LOG.md
├── KNOWLEDGE_MAP.md
├── FINAL_TREE.txt
├── PROPOSED_TREE.txt
├── FILE_MANIFEST.csv
├── MIGRATION_PLAN.md
├── CLEANUP_PLAN.md
├── architectures (diretório)
├── ai/
│   ├── evals/                         (golden-set, retrieval-set, safety-set, schema-set)
│   ├── modules/                       (answering, project-navigation, repo-analysis, retrieval-summarization, tool-use)
│   ├── policies/                      (anti-prompt-injection.md, citation-and-grounding.md, pii-redaction.md, refusal-policy.md, sensitive-actions.md)
│   ├── retrieval/                     (chunking-policy.md, indexing-spec.md, query-rewrite-policy.md, ranking-policy.md)
│   ├── schemas/                       (answer.schema.json, document-meta.schema.json, project-card.schema.json, retrieval-result.schema.json, tool-catalog.schema.json)
│   └── system/                        (base-system-prompt.md, routing-policy.md)
├── catalog/
│   ├── projects.json                  (catálogo机器可读 — minimal, apenas CapyMind)
│   ├── documents.json                 (catálogo de documentos — minimal)
│   ├── search-index.jsonl
│   ├── sources.json
│   └── tags.json
├── docs/
│   ├── adrs/                          (0001-knowledge-pack-scope, 0002-document-frontmatter, 0003-agent-retrieval-policy, 0004-sensitivity-classification)
│   ├── api/                           (integration-signals.md)
│   ├── architecture/                  (capy-project-patterns.md)
│   ├── flows/                         (ingestion-and-governance.md)
│   ├── governance/                    (content-governance.md, ownership.md, pii-policy.md, review-policy.md, security-policy.md)
│   ├── guides/                        (getting-started.md, how-to-add-a-document.md, how-to-query-the-knowledge-pack.md)
│   ├── reference/                     (citation-policy.md, document-types.md, naming-conventions.md, repo-map.md, taxonomy.md)
│   ├── runbooks/                      (incident-response-runbook.md, ingestion-runbook.md, release-runbook.md, review-runbook.md)
│   ├── systems/                       (operational-systems-overview.md)
│   ├── tutorials/                     (building-a-project-card.md, creating-an-ai-instruction-page.md)
│   ├── ui-ux/                         (design-system-signals.md)
│   └── _index.md
├── knowledge/                         (conhecimento domínio: ai, branding, business, commercial, operations, products, technical)
├── projects/                          (60+ projetos com documentação por slug — overview.md, purpose.md, stack.md, architecture.md, integrations.md, manifest.json, etc.)
├── references/                        (índices e catálogos de assets visuais, diagramas, produtos)
├── indexes/                           (light-source-index.md, review-items.md)
├── datasets/                          (candidates, extracted, structured; com README.md)
├── prompts/                           (índice e possíveis prompts)
├── assets/                            (catalogs, diagrams, product-assets, visual-assets)
├── archive/                           (material arquivado)
├── scripts/                           (build_capymind.py, rebuild_capymind_markdown.py, organize_repo.sh, organize_repo.ps1)
├── data/                              (build-summary.json, README.md)
└── supabase/                          ❌ NÃO EXISTE
```

---

## Verificação item a item (Fase 0 checklist)

| Item | Estado | Observação |
|------|--------|------------|
| **Estrutura do repositório** | ✅ Analisada | 60+ projetos catalogados, docs extensas, schemas em ai/schemas/ |
| **README.md** | ✅ Existe | Conteúdo completo, princípios claros |
| **MCP_GUIDE.md** | ✅ Existe | Navegação para agentes MCP definida |
| **llms.txt** | ✅ Existe | Índice público de navegação |
| **PROJECT_CATALOG.md** | ✅ Existe | Catalogo textual rico |
| **INVENTORY.md** | ✅ Existe | Panorama do conteúdo |
| **schemas/** | ⚠️ Parcial | Diretório `schemas/` existe mas contém apenas README.md. Schemas estão em `ai/schemas/` |
| **schemas/document-meta.schema.json** | ✅ Existe (em `ai/schemas/`) | Completo, com required id, title, doc_type, status, sensibilidade, etc. |
| **schemas/project-meta.schema.json** | ❌ Não existe | **Precisa criar** (ou usar `project-card.schema.json` existente e adequar) |
| **catalog/projects.json** | ✅ Existe | Mas contém apenas entrada do CapyMind — **precisa popular** com os 60+ projetos |
| **catalog/documents.json** | ✅ Existe | Minimal — apenas 2 docs inventariados |
| **docs/reference/taxonomy.md** | ✅ Existe | Extenso (1179 linhas), fully featured |
| **docs/governance/security-policy.md** | ✅ Existe | Conteúdo completo |
| **ai/policies/anti-prompt-injection.md** | ✅ Existe | Conteúdo completo (233 linhas) |
| **ai/policies/retrieval-safety.md** | ❌ Não existe | **Precisa criar** |
| **ai/contracts/** | ❌ Diretório não existe | **Precisa criar** (estrutura ai/contracts/) |
| **ai/contracts/context-pack.schema.json** | ❌ Não existe | **Precisa criar** |
| **ai/contracts/search-result.schema.json** | ❌ Não existe | **Precisa criar** |
| **scripts/validate-knowledge-pack.ts** | ❌ Não existe | **Precisa criar** |
| **scripts/build-index.ts** | ❌ Não existe | **Precisa criar** |
| **scripts/check-links.ts** | ❌ Não existe | **Precisa criar** |
| **scripts/check-secrets.ts** | ❌ Não existe | **Precisa criar** |
| **scripts/generate-llms.ts** | ❌ Não existe | **Precisa criar** |
| **scripts/generate-manifest.ts** | ❌ Não existe | **Precisa criar** |
| **package.json** | ❌ Não existe | **Precisa criar** |
| **tsconfig.json** | ❌ Não existe | **Precisa criar** |
| **supabase/** | ❌ Não existe | **Precisa criar** (migrations, functions) |
| **sdk/** | ❌ Não existe | **Precisa criar** (TypeScript SDK) |
| **tests/** | ❌ Não existe | **Precisa criar** (validação, evals) |
| **scripts/ingest-documents.ts** | ❌ Não existe | Fase 3 — cria posteriormente |
| **scripts/chunk-documents.ts** | ❌ Não existe | Fase 3 — cria posteriormente |
| **supabase/migrations/001_init_capymind.sql** | ❌ Não existe | Fase 3 — cria posteriormente |
| **supabase/functions/capymind-api/** | ❌ Não existe | Fase 4 — cria posteriormente |
| **supabase/functions/mcp/** | ❌ Não existe | Fase 5 — cria posteriormente |
| **sdk/typescript/** | ❌ Não existe | Fase 6 — cria posteriormente |

---

## Lacunas reais identificadas (críticas)

### Fase 1 — Estrutura canônica
1. `schemas/project-meta.schema.json` ausente (existe `project-card.schema.json` em `ai/schemas/` — precisa decidir: unificar ou duplicar com nome canônico)
2. `catalog/projects.json` não populado (apenas CapyMind)
3. `catalog/documents.json` com apenas 2 entries — precisa ser gerado
4. `ai/policies/retrieval-safety.md` ausente
5. `ai/contracts/` diretório não existe
6. `ai/contracts/context-pack.schema.json` ausente
7. `ai/contracts/search-result.schema.json` ausente (mas existe em `ai/schemas/` — possível duplicação de propósito)

**Nota**: Há dois conjuntos de schemas:
- `ai/schemas/` — contém answer, document-meta, project-card, retrieval-result, tool-catalog
- `schemas/` (root) — vazio, apenas README

O plano do agente pede `schemas/document-meta.schema.json` e `schemas/project-meta.schema.json` na raiz. O arquivo `document-meta.schema.json` já existe em `ai/schemas/` — decisão necessária: copiar para `schemas/` ou symlink/criar link? Decisão conservadora: **criar cópia em `schemas/`** para atender contrato canônico.

### Fase 2 — Scripts de validação
1. Sem `package.json` — ambiente Node/TypeScript não configurado
2. Sem `tsconfig.json` — sem configuração TypeScript
3. Sem scripts TypeScript em `scripts/` — apenas Python e shell
4. Sem `tests/` — sem evals ou validação estrutura além dos evals em `ai/evals/`

### Fase 3 — Dados e busca
1. Sem `supabase/` — sem migrations, semEdge Functions
2. Sem tabelas definidas (documents, document_chunks, projects, api_keys, usage_events, mcp_sessions, eval_runs)
3. Sem scripts de ingestão ou chunking

### Fase 4 — API
1. Sem `supabase/functions/capymind-api/` — API REST não implementada
2. Sem `openapi.json`
3. Sem docs de API

### Fase 5 — MCP
1. Sem `supabase/functions/mcp/` — servidor MCP não implementado
2. Sem docs MCP específicas (MCP_GUIDE.md existe mas é geral)

### Fase 6 — SDK
1. Sem `sdk/` — SDK TypeScript não existe

---

## Critério de aceite da Fase 0

✅ Estado real mapeado  
✅ Lacunas listadas sem suposição  
✅ Arquivos-alvo definidos com paths exatos  
✅ Nenhum arquivo listado como existente sem verificação real (todos lidos ou listados)  
✅ Decisões de congruência anotadas (ex: schemas duplicados em ai/schemas vs schemas/)

---

## Arquivos que serão criados (por fase)

### Fase 1 — Estrutura canônica (9 arquivos)
```
schemas/document-meta.schema.json          (cópia de ai/schemas/ para raiz)
schemas/project-meta.schema.json           (novo, baseado em ai/schemas/project-card.schema.json mas com sensibilidade/status)
catalog/projects.json                      (populado com 60+ projetos do PROJECT_CATALOG.md)
catalog/documents.json                     (gerado a partir de escaneamento)
docs/reference/taxonomy.md                 ✅ existe
docs/governance/security-policy.md         ✅ existe
ai/policies/anti-prompt-injection.md       ✅ existe
ai/policies/retrieval-safety.md            (novo)
ai/contracts/context-pack.schema.json      (novo)
ai/contracts/search-result.schema.json     (novo — ou adaptar de ai/schemas/retrieval-result.schema.json)
```

### Fase 2 — Scripts de validação (8 arquivos + package.json)
```
package.json                              (novo)
tsconfig.json                             (novo)
scripts/validate-knowledge-pack.ts        (novo)
scripts/build-index.ts                    (novo)
scripts/check-links.ts                    (novo)
scripts/check-secrets.ts                  (novo)
scripts/generate-llms.ts                  (novo)
scripts/generate-manifest.ts              (novo)
```

### Fase 3 — Dados e busca (3 arquivos + estrutura)
```
supabase/migrations/001_init_capymind.sql   (novo)
scripts/ingest-documents.ts                (novo)
scripts/chunk-documents.ts                 (novo)
supabase/                                   (diretório criado)
```

### Fase 4 — API (4 arquivos + docs)
```
supabase/functions/capymind-api/index.ts   (novo)
openapi.json                               (novo)
docs/api/quickstart.md                     (novo)
docs/api/authentication.md                 (novo)
docs/api/rate-limits.md                    (novo)
```

### Fase 5 — MCP (3 arquivos + docs)
```
supabase/functions/mcp/index.ts            (novo)
docs/mcp/quickstart.md                     (novo)
docs/mcp/tools.md                          (novo)
docs/mcp/security.md                       (novo)
```

### Fase 6 — SDK (estrutura completa)
```
sdk/typescript/package.json               (novo)
sdk/typescript/tsconfig.json              (novo)
sdk/typescript/src/index.ts               (novo)
sdk/typescript/examples/search.ts         (novo)
sdk/typescript/examples/context-pack.ts   (novo)
docs/sdk/typescript.md                     (novo)
```

### Fase 7 — Deploy (configuração)
```
.env.example                               (novo — se necessário)
deploy/                                    (novo — scripts de deploy)
```

---

## Riscos e dependências

1. **Node.js/TypeScript toolchain ausente** — Fase 2 depende de instalar dependências (tsx, zod, ajv, etc.)
2. **Supabase não configurado** — Fase 3 e 4 exigem CLI ou configuração local de Supabase. Se não for possível rodar local, entregar SQL/functions para deploy manual.
3. **População de catalog/projects.json automatizada?** — Pode ser scriptada a partir de PROJECT_CATALOG.md. Vou criar script para isso em Fase 2.
4. **LLMs.txt já existe** — scripts `generate-llms.ts` devem respeitar o formato atual e apenas atualizar, não reescrever radicalmente.

---

## Decisões tomadas

1. **schemas/ vs ai/schemas/**: O agente pede `schemas/` na raiz. Como a estrutura atual usa `ai/schemas/`, vou **criar os schemas canônicos em `schemas/`** e manter os de `ai/` separados (são para agent behavior contracts). Contratos de API/MCP (`ai/contracts/`) serão criados separadamente.
2. **project-meta.schema.json**: Não existe. Vou criar baseado em `project-card.schema.json` (que já tem campos necessários), mas adicionando `sensitivity` e `status` (como em document-meta.schema.json) para alinhar com taxonomy.
3. **retrieval-safety.md**: não existe em ai/policies/. Vou criar como `ai/policies/retrieval-safety.md` — política complementar à anti-prompt-injection.
4. **ai/contracts/**: diretório novo. Conterá contratos de resposta para API/MCP pública (context-pack e search-result). O `ai/schemas/retrieval-result.schema.json` já define resultado de busca; posso reutilizar como base e criar `context-pack.schema.json` novo.
5. **scripts existentes**: Os scripts Python atuais (`build_capymind.py`, `rebuild_capymind_markdown.py`) são de construção do próprio repositório — vou preservar e **adicionar scripts TypeScript** paralelos para validação do knowledge pack. Não vou reescrever os scripts Python existentes sem necessidade.

---

## Próximas fases (ordem)

1. **Fase 1** — Criar estrutura canônica (schemas, contracts, catalog, retrieval-safety)
2. **Fase 2** — Configurar Node.js + scripts de validação (package.json, tsconfig, scripts TypeScript, rodar npm run build)
3. **Fase 3** — Preparar dados e ingestão (Supabase migrations, scripts de ingestão/chunking)
4. **Fase 4** — API REST (Edge Functions, OpenAPI, docs)
5. **Fase 5** — MCP server
6. **Fase 6** — SDK TypeScript
7. **Fase 7** — Deploy e validação final

---

## Critério de aceite por bloco (resumo)

| Bloco | Existe? | Precisa criar? | Precisa corrigir? |
|-------|---------|----------------|------------------|
| schemas/ (root com JSONs) | ⚠️ parcial | ✅ sim (document-meta, project-meta) | ❌ não |
| catalog/projects.json | ✅ sim | ✅ sim (popular) | ❌ não |
| catalog/documents.json | ✅ sim | ✅ sim (gerar) | ❌ não |
| docs/reference/taxonomy.md | ✅ sim | ❌ não | ❌ não |
| docs/governance/security-policy.md | ✅ sim | ❌ não | ❌ não |
| ai/policies/anti-prompt-injection.md | ✅ sim | ❌ não | ❌ não |
| ai/policies/retrieval-safety.md | ❌ não | ✅ sim | ❌ não |
| ai/contracts/context-pack.schema.json | ❌ não | ✅ sim | ❌ não |
| ai/contracts/search-result.schema.json | ❌ não | ✅ sim | ❌ não |
| package.json | ❌ não | ✅ sim | ❌ não |
| scripts TS de validação | ❌ não | ✅ sim (6 scripts) | ❌ não |
| supabase/ + migrations | ❌ não | ✅ sim | ❌ não |
| supabase/functions/api | ❌ não | ✅ sim | ❌ não |
| supabase/functions/mcp | ❌ não | ✅ sim | ❌ não |
| sdk/typescript/ | ❌ não | ✅ sim | ❌ não |

---

## Resumo final da auditoria

**Estado atual**: repositório **rico em documentação canônica** (taxonomy, policies, ADRs, guides, reference) mas **desprovido de camada executável** (Node config, scripts de validação, Supabase DB, API, MCP, SDK).

**Prontidão para Fase 1**: alta — estrutura de diretórios e políticas já bem avançada. Basta criar os arquivos canônicos faltantes (schemas de projeto, retrieval-safety, contracts) e popular catalog.

**Risco principal**: Supabase pode exigir infra que não está disponível no ambiente local. Se for o caso, entrego SQL e funções para deploy manual.

**Próxima ação**: iniciar Fase 1 — criar/ajustar arquivos canônicos.
