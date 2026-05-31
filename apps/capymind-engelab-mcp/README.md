# CapyMind EngenLab MCP

Servidor MCP remoto, read-only, para consultar a biblioteca `faelscarpato/engelab_doc` por meio de uma camada governada pelo CapyMind.

## Estado

MVP inicial.

Este servidor expõe:

- `GET /health`
- `POST /mcp`

## Tools MCP iniciais

| Tool | Função |
|---|---|
| `get_safety_notice` | Retorna o aviso técnico obrigatório. |
| `list_engelab_projects` | Lista grupos de projetos-modelo por disciplina. |
| `search_engelab_doc` | Busca metadados curados da biblioteca EngenLab Doc. |
| `get_project_context` | Retorna contexto estruturado de um grupo de projetos. |

## Rodar localmente

```bash
cd apps/capymind-engelab-mcp
npm install
npm run dev
```

Health check:

```bash
curl http://localhost:3000/health
```

## Build

```bash
npm run build
npm run start
```

## Docker

```bash
docker build -t capymind-engelab-mcp .
docker run --rm -p 3000:3000 capymind-engelab-mcp
```

## Conectar no ChatGPT Apps

Depois do deploy HTTPS, use:

```text
https://<host>/mcp
```

Configuração sugerida:

```text
Nome: CapyMind EngenLab
Descrição: Consulta inteligente da biblioteca EngenLab Doc via CapyMind para localizar projetos-modelo, prompts técnicos, checklists, memoriais conceituais e materiais educacionais de engenharia civil, sempre com uso referencial e revisão humana.
Autenticação: Sem autenticação no MVP read-only.
```

## Limite operacional

Este MCP é apenas para consulta, estudo, referência, prompt engineering e organização técnica. Não gera projeto executivo, laudo, ART/RRT, aprovação normativa ou validação profissional.

## Próximas melhorias

1. Substituir busca curada por indexação real do `engelab_doc`.
2. Adicionar cache de catálogo.
3. Adicionar `build_agent_context`.
4. Adicionar rate limit.
5. Adicionar autenticação para uso privado ou escrita futura.
