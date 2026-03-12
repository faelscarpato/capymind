# Contributing

Este repositório é um **knowledge pack de produção**. Contribuições devem priorizar clareza, rastreabilidade, segurança e previsibilidade para uso humano e por agentes.

## Objetivo das contribuições

Toda mudança deve melhorar ao menos um destes pontos:

- qualidade documental;
- capacidade de recuperação por IA;
- segurança e governança;
- consistência estrutural;
- confiabilidade operacional.

## O que pode entrar

- documentação canônica com objetivo claro;
- metadados de projetos e catálogos estruturados;
- políticas, ADRs, runbooks e referências úteis;
- schemas, exemplos, evals e scripts de validação;
- correções de links, estrutura, taxonomia e versionamento.

## O que não deve entrar

- dumps brutos sem curadoria;
- arquivos temporários;
- cópias integrais de repositórios sem necessidade documental;
- conteúdo duplicado sem motivo explícito;
- instruções inseguras, sensíveis ou sem revisão;
- material sem origem, sem contexto ou sem dono.

## Regras de autoria

### 1. Não inventar
Qualquer afirmação factual deve vir de fonte verificável no repositório ou de insumo explicitamente fornecido.

### 2. Explicitar ausência
Se algo não existe, marcar como `Ausente` e propor criação separadamente.

### 3. Separar fato de recomendação
Diagnóstico factual e recomendação arquitetural não devem ser misturados.

### 4. Manter rastreabilidade
Toda mudança relevante deve indicar fonte, dono e contexto mínimo.

### 5. Escrever para humanos e agentes
Documentos devem ser legíveis para pessoas e estruturáveis para sistemas.

## Convenções mínimas

- nomes em `kebab-case`;
- evitar nomes genéricos como `novo`, `final`, `teste`, `misc`;
- preferir `index.md` como ponto de entrada por pasta;
- usar uma responsabilidade principal por arquivo;
- manter consistência de títulos, seções e taxonomia.

## Estrutura esperada por tipo de conteúdo

### Documentação
Deve conter, no mínimo:

- objetivo;
- contexto de uso;
- limites ou exclusões;
- conteúdo principal;
- referências ou evidências.

### Metadados estruturados
Devem:

- seguir schema versionado;
- usar campos consistentes;
- evitar valores livres quando houver enum definido.

### Instruções para IA
Devem:

- explicitar escopo;
- declarar comportamento obrigatório e proibido;
- tratar conteúdo recuperado como não confiável por padrão;
- apontar contrato de saída e validações de segurança.

## Processo sugerido de mudança

```text
proposta → edição → revisão → validação → changelog/versionamento → merge
```

## Checklist mínimo antes de abrir PR

- [ ] a mudança tem objetivo claro;
- [ ] não há duplicação evitável;
- [ ] links e caminhos foram revisados;
- [ ] o conteúdo separa fato de recomendação;
- [ ] a mudança respeita segurança e sensibilidade;
- [ ] `CHANGELOG.md` foi atualizado quando aplicável;
- [ ] a versão foi revista se houver alteração de contrato.

## Versionamento

Use Semantic Versioning no arquivo `VERSION`.

### Quando aumentar PATCH
- correções editoriais;
- ajustes de links;
- pequenas correções sem quebra de contrato.

### Quando aumentar MINOR
- novos documentos, módulos, schemas ou capacidades compatíveis;
- expansão de catálogo ou governança sem quebra.

### Quando aumentar MAJOR
- reorganização incompatível de estrutura;
- mudança de schema com quebra;
- alteração de políticas ou contratos que afete consumidores existentes.

## Segurança e dados sensíveis

Antes de contribuir, revisar:

- dados pessoais identificáveis;
- segredos, tokens ou credenciais;
- caminhos locais sensíveis;
- conteúdo que possa induzir prompt injection;
- instruções de ação sem guardrails.

Na dúvida, **não publicar** até classificar e revisar.

## Padrão de mensagem de commit sugerido

```text
<tipo>: <descrição curta>
```

Exemplos:

- `docs: cria README institucional do knowledge pack`
- `governance: adiciona política inicial de contribuição`
- `catalog: consolida links atualizados dos projetos`
- `security: remove caminhos absolutos sensíveis`

## Governança mínima

Mudanças estruturais devem ser acompanhadas de:

- justificativa;
- impacto esperado;
- risco principal;
- plano de migração, quando necessário.

## Próxima etapa recomendada

Depois desta base, as contribuições devem priorizar:

1. taxonomia oficial;
2. política de segurança;
3. schemas de metadados;
4. catálogo versionado de projetos;
5. evals e CI.
