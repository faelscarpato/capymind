# Agent System Prompt

Resumo curto: prompt catalogado como ativo de conhecimento.

## Origem
- Caminho original: `D:\novosproj\knowledge\prompt-engineering\prompt-engineering-2026\Templates & Exemplos\agent-system-prompt.md`

## Detectado
- Categoria: analysis
- Objetivo: Modelar prompts-base para agentes especializados.
- Ferramenta-alvo percebida: Sistemas multiagente

## Prompt Original Consolidado
```md
# Agent System Prompt Template
## Exemplo Multi-Agent para Produção

Este template demonstra a **melhor prática consolidada em 2026** para construir agentes autônomos usando padrão **ReAct** com múltiplos roles (Planner, Executor, Critic).

---

## 📋 ARQUITETURA DO AGENTE

```
User Query
    ↓
Planner Agent → gera plano estruturado
    ↓
Executor Agent → executa cada passo
    ↓
Critic Agent → valida resultado
    ↓
Response ao usuário
```
```

## Inferido
- O prompt pode ser reutilizado como base ou adaptado para pipelines internos.

## Relevancia
- Mantem a biblioteca de prompts navegavel para IA e consulta humana.

## Observacoes
- O texto foi mantido em versao leve; revisar o original para contexto completo quando necessario.
