# CapyMind

CapyMind é um **knowledge pack docs-as-code** preparado para servir como base de contexto para IAs, automações, MCP servers e consulta humana. O objetivo do repositório é organizar conhecimento de forma **navegável, versionada, segura e testável**, separando claramente:

- documentação canônica;
- conhecimento derivado;
- instruções para agentes;
- contratos de saída e metadados;
- governança, segurança e qualidade;
- camadas MCP e integrações operacionais.

---

## Estado atual

O CapyMind agora contém uma implementação funcional do **CapyMind EngenLab MCP**, um servidor MCP read-only para conectar o ChatGPT, PromptDesk e outros clientes MCP à biblioteca técnica `faelscarpato/engelab_doc`.

### Componentes principais

```txt
capymind/
├── README.md
├── package.json
├── apps/
│   └── capymind-engelab-mcp/
│       ├── package.json
│       ├── tsconfig.json
│       ├── Dockerfile
│       ├── README.md
│       └── src/
│           ├── server.ts
│           └── lib/
│               ├── agent-contexts.ts
│               ├── agent-router.ts
│               ├── engelab-data.ts
│               └── safety.ts
├── projects/
│   └── capymind-engelab-mcp/
│       ├── README.md
│       └── agents/
│           ├── modulo-01-estrutural-context.md
│           ├── modulo-02-eletrico-context.md
│           ├── modulo-03-hidrossanitario-context.md
│           ├── modulo-04-prompts-modulares-context.md
│           ├── modulo-08-revit-prompt-context.md
│           ├── modulo-09-calculo-estrutural-context.md
│           ├── modulo-10-compatibilizacao-context.md
│           ├── modulo-11-orcamentos-quantitativos-context.md
│           ├── modulo-12-planejamento-obra-context.md
│           ├── modulo-13-vistorias-relatorios-context.md
│           ├── modulo-14-seguranca-trabalho-context.md
│           └── modulo-15-estruturas-context.md
├── ai/
├── catalog/
├── docs/
├── knowledge/
├── references/
├── scripts/
├── tests/
└── .github/
```

---

## Arquitetura operacional

```txt
ChatGPT App / PromptDesk / MCP Client
  ↓ HTTPS /mcp
CapyMind EngenLab MCP Server
  ↓
Tool router + safety layer + agent catalog
  ↓
CapyMind canonical agent documents
  ↓
EngenLab Doc corpus: faelscarpato/engelab_doc
  ↓
Resposta estruturada com sourceDocument, sourcePath e aviso técnico
```

O MCP atual é **read-only**. Ele não edita repositórios, não cria documentos executivos e não substitui revisão humana.

---

## CapyMind EngenLab MCP

Local do app:

```txt
apps/capymind-engelab-mcp/
```

### Stack

```txt
Node.js 20+
TypeScript
Express
@modelcontextprotocol/sdk
Streamable HTTP
Zod
```

### Endpoints

```txt
GET  /health
POST /mcp
```

### Rodar localmente

```bash
cd apps/capymind-engelab-mcp
npm install
npm run build
npm run dev
```

Health check:

```bash
curl http://localhost:3000/health
```

Resposta esperada:

```json
{
  "status": "ok",
  "service": "capymind-engelab-mcp",
  "version": "0.1.0"
}
```

### URL no ChatGPT Apps

Depois de publicar via HTTPS, use:

```txt
https://<host>/mcp
```

Para túnel Cloudflare local, a origem deve apontar para:

```txt
http://localhost:3000
```

---

## Tools MCP disponíveis

| Tool | Função |
|---|---|
| `get_safety_notice` | Retorna o aviso técnico obrigatório. |
| `list_engelab_projects` | Lista grupos de projetos-modelo da biblioteca EngenLab Doc. |
| `search_engelab_doc` | Busca metadados curados da biblioteca EngenLab Doc. |
| `get_project_context` | Retorna contexto estruturado de um grupo de projetos. |
| `build_agent_context` | Monta pacote de contexto para outro GPT/agente. |
| `list_agent_catalog` | Lista os agentes PromptDesk disponíveis. |
| `get_agent_context` | Retorna contexto fixo/system prompt por `agent_id`. |
| `route_agent_for_task` | Escolhe automaticamente o melhor agente para uma tarefa. |
| `get_structural_agent_context` | Atalho legado para o agente de Estruturas Módulo 15. |

---

## Catálogo de agentes PromptDesk

O catálogo atual possui **12 agentes técnicos educacionais**:

| # | agentId | Módulo | Documento canônico |
|---:|---|---|---|
| 1 | `engenlab-estrutural-projetos-ia-01` | `01_ESTRUTURAL` | `projects/capymind-engelab-mcp/agents/modulo-01-estrutural-context.md` |
| 2 | `engenlab-eletrico-projetos-ia-02` | `02_ELETRICO` | `projects/capymind-engelab-mcp/agents/modulo-02-eletrico-context.md` |
| 3 | `engenlab-hidrossanitario-projetos-ia-03` | `03_HIDROSSANITARIO` | `projects/capymind-engelab-mcp/agents/modulo-03-hidrossanitario-context.md` |
| 4 | `engenlab-prompts-modulares-ia-04` | `04_PROMPTS_MODULARES` | `projects/capymind-engelab-mcp/agents/modulo-04-prompts-modulares-context.md` |
| 5 | `engenlab-revit-prompt-ia-08` | `08_BONUS/PROMPT_REVIT` | `projects/capymind-engelab-mcp/agents/modulo-08-revit-prompt-context.md` |
| 6 | `engenlab-calculo-estrutural-ia-09` | `09_CALCULO_ESTRUTURAL_IA` | `projects/capymind-engelab-mcp/agents/modulo-09-calculo-estrutural-context.md` |
| 7 | `engenlab-compatibilizacao-ia-modulo-10` | `PLUS_MODULOS_10_14 / Módulo 10` | `projects/capymind-engelab-mcp/agents/modulo-10-compatibilizacao-context.md` |
| 8 | `engenlab-orcamentos-quantitativos-ia-modulo-11` | `PLUS_MODULOS_10_14 / Módulo 11` | `projects/capymind-engelab-mcp/agents/modulo-11-orcamentos-quantitativos-context.md` |
| 9 | `engenlab-planejamento-obra-ia-modulo-12` | `PLUS_MODULOS_10_14 / Módulo 12` | `projects/capymind-engelab-mcp/agents/modulo-12-planejamento-obra-context.md` |
| 10 | `engenlab-vistorias-relatorios-ia-modulo-13` | `PLUS_MODULOS_10_14 / Módulo 13` | `projects/capymind-engelab-mcp/agents/modulo-13-vistorias-relatorios-context.md` |
| 11 | `engenlab-seguranca-trabalho-obras-ia-modulo-14` | `PLUS_MODULOS_10_14 / Módulo 14` | `projects/capymind-engelab-mcp/agents/modulo-14-seguranca-trabalho-context.md` |
| 12 | `engenlab-estruturas-ia-modulo-15` | `PLUS_MODULO_15_ESTRUTURAS` | `projects/capymind-engelab-mcp/agents/modulo-15-estruturas-context.md` |

Cada agente contém:

- `agentId`;
- nome e display name;
- módulo e source path;
- contexto fixo/system prompt;
- comandos rápidos;
- mensagem de abertura;
- limites obrigatórios;
- aviso técnico;
- documento canônico CapyMind.

---

## Roteamento automático de agentes

O arquivo:

```txt
apps/capymind-engelab-mcp/src/lib/agent-router.ts
```

expõe a lógica usada pela tool:

```txt
route_agent_for_task
```

Ela recebe uma tarefa textual e seleciona o agente mais provável com base em:

- texto da tarefa;
- módulo informado;
- disciplina informada;
- `sourcePath` informado;
- palavras-chave técnicas.

Exemplo:

```json
{
  "task": "montar cronograma preliminar de obra",
  "includeContext": true
}
```

Resultado esperado:

```txt
engenlab-planejamento-obra-ia-modulo-12
```

---

## Integração com EngenLab PromptDesk

A versão aprovada do PromptDesk pode usar os agentes de duas formas:

### 1. Catálogo local embutido

Mais indicado para desktop, MVP e uso offline.

```txt
PromptDesk
  ↓
catálogo local de agentes CapyMind
  ↓
roteamento local
  ↓
prompt final com contexto fixo do agente
```

### 2. Sincronização futura via MCP

Mais indicado quando o produto precisar puxar atualizações diretamente do CapyMind.

```txt
PromptDesk
  ↓
CapyMind EngenLab MCP /mcp
  ↓
list_agent_catalog / get_agent_context / route_agent_for_task
  ↓
catálogo atualizado
```

---

## Política de segurança técnica

Todo conteúdo técnico de engenharia deve respeitar este limite:

```txt
Este material é um apoio educacional, preliminar e de organização técnica. Não constitui projeto executivo, cálculo estrutural final, laudo, ART/RRT, aprovação legal ou substituição de profissional habilitado.
```

O CapyMind e o MCP não devem afirmar:

- aprovação técnica;
- conformidade normativa definitiva;
- cálculo final;
- documento executivo;
- laudo;
- autorização de obra;
- ART/RRT;
- responsabilidade técnica.

---

## O que deve permanecer no repositório

Mantenha:

```txt
README.md
package.json
VERSION
CHANGELOG.md
CONTRIBUTING.md
apps/capymind-engelab-mcp/
projects/capymind-engelab-mcp/
ai/
catalog/
docs/
knowledge/
references/
scripts/
tests/
.github/
```

Também mantenha qualquer arquivo usado por validação, indexação, manifesto, schema, política de segurança ou catálogo canônico.

---

## O que não deve entrar no repositório

Não versionar:

```txt
node_modules/
dist/
build/
.next/
.vite/
.env
.env.local
.env.production
*.log
*.zip
*.rar
*.7z
*.tmp
*.bak
*.old
.DS_Store
Thumbs.db
cloudflared/certs locais
exports temporários
prints soltos sem uso documental
arquivos baixados do ChatGPT sem revisão
```

Se algum desses arquivos já estiver no repositório, ele pode ser removido após confirmar que não é fonte canônica.

---

## O que pode ser arquivado ou removido após revisão

Candidatos à limpeza:

1. arquivos experimentais duplicados fora de `projects/capymind-engelab-mcp/agents/`;
2. contextos antigos de agentes que não apontam para os `.md` canônicos;
3. zips de entrega do PromptDesk;
4. builds gerados localmente;
5. dumps temporários de testes MCP;
6. arquivos de túnel, token, log ou configuração local;
7. qualquer documento sem frontmatter, sem dono, sem status ou sem relação com catálogo, política, schema, MCP ou agente.

Regra prática:

```txt
Se o arquivo não é canônico, não é código-fonte, não é política, não é schema, não é teste e não é documentação rastreável, ele deve sair do repo ou ir para archive/.
```

---

## Versionamento

O repositório usa **Semantic Versioning** para o knowledge pack:

- `MAJOR`: mudanças incompatíveis em estrutura, contratos ou políticas;
- `MINOR`: novos documentos, módulos, schemas, MCP tools ou agentes compatíveis;
- `PATCH`: correções, ajustes editoriais e hardening sem quebra de contrato.

A versão corrente está em [`VERSION`](./VERSION).

---

## Próximos passos recomendados

1. criar uma tool de sincronização do PromptDesk com `list_agent_catalog` e `get_agent_context`;
2. transformar `AGENT_DEFINITIONS` em JSON externo versionado;
3. implementar busca real nos arquivos do `engelab_doc`;
4. criar testes automatizados para roteamento de agentes;
5. adicionar rate limit e autenticação opcional para produção;
6. consolidar `.gitignore` para impedir zips, builds, logs e segredos;
7. criar `archive/` apenas se houver conteúdo histórico que não deve ser apagado.
