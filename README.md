<div align="center">

# CapyMind

### Knowledge Pack + MCP Server + Agent Catalog for EngenLab PromptDesk

**Uma camada de contexto, governança e roteamento de agentes para transformar conhecimento técnico em fluxos de IA utilizáveis, rastreáveis e seguros.**

<br />

![Status](https://img.shields.io/badge/status-active-0f766e?style=for-the-badge)
![MCP](https://img.shields.io/badge/MCP-ready-2563eb?style=for-the-badge)
![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178c6?style=for-the-badge)
![Node](https://img.shields.io/badge/Node-20+-16a34a?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT111827?style=for-the-badge)

<br />

[Visão Geral](#visão-geral) · [Arquitetura](#arquitetura) · [MCP Server](#capymind-engenlab-mcp) · [Agentes](#catálogo-de-agentes) · [PromptDesk](#integração-com-promptdesk) · [Segurança Técnica](#segurança-técnica)

</div>

---

## Visão geral

**CapyMind** é um repositório `docs-as-code` desenhado para operar como uma base viva de contexto para IAs, agentes, automações, aplicativos desktop e clientes MCP.

Ele organiza documentação, regras, agentes e metadados de forma versionada, consultável e segura. No estado atual, o foco principal é servir como camada de inteligência para o **EngenLab PromptDesk**, conectando o app desktop e o ChatGPT a um catálogo técnico de agentes de engenharia.

<div align="center">

| Camada | Função |
|---|---|
| **Knowledge Pack** | Documentos canônicos, políticas, schemas, catálogos e contexto técnico. |
| **MCP Server** | Interface HTTP para ChatGPT, PromptDesk e outros clientes MCP. |
| **Agent Catalog** | 12 agentes técnicos educacionais com system prompt, comandos rápidos e limites de uso. |
| **Routing Layer** | Seleção automática do agente mais adequado para cada tarefa. |
| **Safety Layer** | Avisos técnicos, limites de responsabilidade e uso preliminar/revisável. |

</div>

---

## O que o CapyMind entrega

<table>
<tr>
<td width="33%" valign="top">

### Contexto governado

Documentos canônicos em Markdown, com rastreabilidade, status, metadados e uso controlado por agentes.

</td>
<td width="33%" valign="top">

### MCP funcional

Servidor MCP read-only com endpoints `/health` e `/mcp`, pronto para uso via HTTPS.

</td>
<td width="33%" valign="top">

### Agentes operacionais

Catálogo com agentes de engenharia, PromptDesk config, comandos rápidos e prompt fixo por módulo.

</td>
</tr>
<tr>
<td width="33%" valign="top">

### Roteamento inteligente

Seleciona o agente correto com base na tarefa, disciplina, módulo ou caminho de origem.

</td>
<td width="33%" valign="top">

### Segurança técnica

Mantém respostas como apoio educacional, preliminar e revisável, sem promessa executiva.

</td>
<td width="33%" valign="top">

### Integração PromptDesk

Fornece o contexto necessário para gerar prompts, checklists, relatórios e roteiros técnicos.

</td>
</tr>
</table>

---

## Arquitetura

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

O servidor atual é **read-only**. Ele consulta, organiza, roteia e entrega contexto; não edita documentos externos, não cria aprovações técnicas e não substitui revisão humana.

---

## Estrutura principal

```txt
capymind/
├── apps/
│   └── capymind-engelab-mcp/
│       ├── src/server.ts
│       └── src/lib/
│           ├── agent-contexts.ts
│           ├── agent-router.ts
│           ├── engelab-data.ts
│           └── safety.ts
│
├── projects/
│   └── capymind-engelab-mcp/
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
│
├── ai/
├── catalog/
├── docs/
├── knowledge/
├── references/
├── scripts/
└── tests/
```

---

## CapyMind EngenLab MCP

O app MCP fica em:

```txt
apps/capymind-engelab-mcp/
```

### Stack

| Tecnologia | Uso |
|---|---|
| **Node.js 20+** | Runtime do servidor MCP. |
| **TypeScript** | Tipagem e contratos internos. |
| **Express** | Servidor HTTP. |
| **@modelcontextprotocol/sdk** | MCP server e Streamable HTTP. |
| **Zod** | Validação de entrada das tools. |

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

Teste de saúde:

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

### Publicação via HTTPS

Para conectar no ChatGPT Apps ou em outro cliente MCP, publique o servidor e use:

```txt
https://<host>/mcp
```

Em desenvolvimento local, o túnel pode apontar para:

```txt
http://localhost:3000
```

---

## Tools MCP

| Tool | Descrição |
|---|---|
| `get_safety_notice` | Retorna o aviso técnico obrigatório. |
| `list_engelab_projects` | Lista grupos de projetos-modelo da biblioteca EngenLab Doc. |
| `search_engelab_doc` | Busca metadados curados da biblioteca EngenLab Doc. |
| `get_project_context` | Retorna contexto estruturado de um grupo de projetos. |
| `build_agent_context` | Monta pacote de contexto para outro GPT/agente. |
| `list_agent_catalog` | Lista os agentes PromptDesk disponíveis. |
| `get_agent_context` | Retorna contexto fixo/system prompt por `agent_id`. |
| `route_agent_for_task` | Escolhe automaticamente o melhor agente para uma tarefa. |
| `get_structural_agent_context` | Atalho para o agente de Estruturas Módulo 15. |

### Exemplo de roteamento

Entrada:

```json
{
  "task": "montar cronograma preliminar de obra",
  "includeContext": true
}
```

Saída esperada:

```txt
engenlab-planejamento-obra-ia-modulo-12
```

---

## Catálogo de agentes

O CapyMind expõe **12 agentes técnicos educacionais** para o EngenLab PromptDesk.

| # | Agente | Módulo | Especialidade |
|---:|---|---|---|
| 1 | `engenlab-estrutural-projetos-ia-01` | `01_ESTRUTURAL` | Projetos-modelo estruturais, pranchas, memoriais e checklists. |
| 2 | `engenlab-eletrico-projetos-ia-02` | `02_ELETRICO` | Instalações elétricas, circuitos, pontos, quadros e pranchas. |
| 3 | `engenlab-hidrossanitario-projetos-ia-03` | `03_HIDROSSANITARIO` | Água fria, água quente, esgoto, ventilação e compatibilização. |
| 4 | `engenlab-prompts-modulares-ia-04` | `04_PROMPTS_MODULARES` | Criação, melhoria e padronização de prompts técnicos. |
| 5 | `engenlab-revit-prompt-ia-08` | `08_BONUS/PROMPT_REVIT` | Prompts BIM/Revit, famílias, vistas, parâmetros e pranchas. |
| 6 | `engenlab-calculo-estrutural-ia-09` | `09_CALCULO_ESTRUTURAL_IA` | Hipóteses, checklists e apoio educacional ao cálculo estrutural. |
| 7 | `engenlab-compatibilizacao-ia-modulo-10` | `PLUS_MODULOS_10_14 / Módulo 10` | Matriz de interferências e compatibilização técnica. |
| 8 | `engenlab-orcamentos-quantitativos-ia-modulo-11` | `PLUS_MODULOS_10_14 / Módulo 11` | Quantitativos, insumos, orçamento preliminar e lacunas de medição. |
| 9 | `engenlab-planejamento-obra-ia-modulo-12` | `PLUS_MODULOS_10_14 / Módulo 12` | EAP, cronograma conceitual, riscos e sequenciamento. |
| 10 | `engenlab-vistorias-relatorios-ia-modulo-13` | `PLUS_MODULOS_10_14 / Módulo 13` | Vistorias preliminares, evidências e relatórios educacionais. |
| 11 | `engenlab-seguranca-trabalho-obras-ia-modulo-14` | `PLUS_MODULOS_10_14 / Módulo 14` | SST em obras, riscos aparentes, checklists e roteiros. |
| 12 | `engenlab-estruturas-ia-modulo-15` | `PLUS_MODULO_15_ESTRUTURAS` | Estruturas com IA, prompts, relatórios, memoriais e pranchas. |

Cada agente possui:

```txt
agentId
sourceDocument
sourcePath
PromptDesk config
system prompt
quick commands
opening message
mandatory safety notice
```

---

## Documentos canônicos dos agentes

| Agente | Documento |
|---|---|
| Estrutural 01 | `projects/capymind-engelab-mcp/agents/modulo-01-estrutural-context.md` |
| Elétrico 02 | `projects/capymind-engelab-mcp/agents/modulo-02-eletrico-context.md` |
| Hidrossanitário 03 | `projects/capymind-engelab-mcp/agents/modulo-03-hidrossanitario-context.md` |
| Prompts Modulares 04 | `projects/capymind-engelab-mcp/agents/modulo-04-prompts-modulares-context.md` |
| Revit Prompt 08 | `projects/capymind-engelab-mcp/agents/modulo-08-revit-prompt-context.md` |
| Cálculo Estrutural 09 | `projects/capymind-engelab-mcp/agents/modulo-09-calculo-estrutural-context.md` |
| Compatibilização 10 | `projects/capymind-engelab-mcp/agents/modulo-10-compatibilizacao-context.md` |
| Orçamentos 11 | `projects/capymind-engelab-mcp/agents/modulo-11-orcamentos-quantitativos-context.md` |
| Planejamento 12 | `projects/capymind-engelab-mcp/agents/modulo-12-planejamento-obra-context.md` |
| Vistorias 13 | `projects/capymind-engelab-mcp/agents/modulo-13-vistorias-relatorios-context.md` |
| Segurança 14 | `projects/capymind-engelab-mcp/agents/modulo-14-seguranca-trabalho-context.md` |
| Estruturas 15 | `projects/capymind-engelab-mcp/agents/modulo-15-estruturas-context.md` |

---

## Integração com PromptDesk

O EngenLab PromptDesk pode consumir o CapyMind de duas formas.

### Modo local

Ideal para app desktop, MVP e uso offline.

```txt
PromptDesk
  ↓
catálogo local de agentes CapyMind
  ↓
roteamento local
  ↓
prompt final com contexto fixo do agente
```

### Modo MCP

Ideal para sincronização futura e atualizações centralizadas.

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

## Segurança técnica

O CapyMind foi projetado para trabalhar com engenharia de forma responsável. Todas as respostas técnicas devem manter o seguinte limite:

```txt
Este material é um apoio educacional, preliminar e de organização técnica. Não constitui projeto executivo, cálculo estrutural final, laudo, ART/RRT, aprovação legal ou substituição de profissional habilitado.
```

O objetivo é acelerar organização, documentação, prompts, checklists e raciocínio preliminar — sempre com revisão humana obrigatória quando houver impacto técnico, legal, financeiro ou de segurança.

---

## Experiência esperada

<div align="center">

| Antes | Depois com CapyMind |
|---|---|
| Prompt solto | Prompt governado por agente |
| Biblioteca difícil de navegar | Catálogo com roteamento por tarefa |
| Contexto disperso | Documento canônico por módulo |
| Risco de resposta executiva indevida | Limites técnicos obrigatórios |
| Uso manual da biblioteca | Fluxo pronto para PromptDesk e ChatGPT |

</div>

---

## Demonstração rápida

### Listar agentes

```txt
Use o CapyMind EngenLab para listar o catálogo de agentes disponíveis.
```

### Buscar contexto de agente

```txt
Use o CapyMind EngenLab para retornar o contexto do agente engenlab-revit-prompt-ia-08.
```

### Roteamento por tarefa

```txt
Use o CapyMind EngenLab para escolher o melhor agente para: criar checklist de segurança para etapa de concretagem.
```

---

<div align="center">

## CapyMind é a camada de inteligência operacional do EngenLab PromptDesk.

**Organiza conhecimento. Roteia agentes. Entrega contexto. Mantém limites técnicos.**

</div>
