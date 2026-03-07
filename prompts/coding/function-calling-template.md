# Function Calling Template

Resumo curto: prompt catalogado como ativo de conhecimento.

## Origem
- Caminho original: `D:\novosproj\knowledge\prompt-engineering\prompt-engineering-2026\Templates & Exemplos\function-calling-template.md`

## Detectado
- Categoria: coding
- Objetivo: Padronizar prompts com chamadas de ferramenta e estrutura de funcoes.
- Ferramenta-alvo percebida: Agentes com tools

## Prompt Original Consolidado
```md
# Function Calling Template (OpenAI Format)
## Exemplo Estruturado para Produção

Este template demonstra o padrão **consolidado em 2026** para definir ferramentas (tools/functions) com OpenAI API usando JSON Schema completo.

---

## 📋 O QUE É FUNCTION CALLING?

**Function Calling** permite que o LLM:
1. Reconheça que precisa usar uma ferramenta
2. Descreva qual ferramenta usar (sem executar)
3. Forneça os parâmetros estruturados em JSON

Você (desenvolvedor) é responsável por:
1. Validar o JSON
2. Executar a função de verdade
3. Retornar o resultado para o modelo

---
```

## Inferido
- O prompt pode ser reutilizado como base ou adaptado para pipelines internos.

## Relevancia
- Mantem a biblioteca de prompts navegavel para IA e consulta humana.

## Observacoes
- O texto foi mantido em versao leve; revisar o original para contexto completo quando necessario.
