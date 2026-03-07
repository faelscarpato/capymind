
---

## `projects/pedreiracep/roadmap-notes.md`

```md
# Roadmap Notes — PedreiraCep

## Resumo

O PedreiraCep já aparenta cumprir bem seu objetivo principal como utilitário de consulta local. As evoluções mais interessantes não exigem uma reinvenção do projeto, mas sim refinamentos na experiência, na modelagem dos dados e na robustez da busca.

## Detectado

O projeto já demonstra uma base funcional composta por:

- interface web simples
- dataset local de CEPs
- documentação inicial
- foco claro em consulta pública

Isso indica que o produto tem um núcleo definido e não está partindo do zero.

## Inferido

As notas abaixo representam possibilidades de evolução inferidas a partir da estrutura e do propósito percebidos do projeto. Elas não devem ser tratadas como funcionalidades já implementadas.

## Evoluções de curto prazo

### 1. Clarificar a lógica entre `script.js` e `scripts.js`
Objetivo:
- reduzir ambiguidade
- evitar duplicidade
- facilitar manutenção

Impacto:
- melhora a legibilidade técnica
- torna a base mais confiável para evolução futura

---

### 2. Documentar melhor o fluxo de busca
Objetivo:
- explicar como a pesquisa funciona
- registrar o comportamento esperado para rua, bairro e CEP
- facilitar manutenção e leitura por IA

Impacto:
- reduz dúvidas de uso e entendimento técnico
- melhora navegabilidade documental

---

### 3. Melhorar estados de interface
Objetivo:
- tratar melhor buscas sem resultado
- mostrar mensagens mais claras
- reforçar retorno visual para o usuário

Impacto:
- melhora a experiência de uso
- reduz confusão em consultas ambíguas

---

### 4. Validar consistência da base
Objetivo:
- revisar grafias
- detectar entradas inconsistentes
- padronizar formatação

Impacto:
- melhora qualidade dos resultados
- reduz erros de busca

## Evoluções de médio prazo

### 5. Normalizar a estrutura dos dados
Objetivo:
- separar logradouro, bairro e CEP em campos distintos
- reduzir dependência de parsing textual
- facilitar filtros e integrações

Impacto:
- abre caminho para API
- melhora organização do dataset
- facilita manutenção e crescimento

---

### 6. Criar busca tolerante a variações
Objetivo:
- aceitar diferenças de acentuação
- aceitar abreviações
- melhorar matching parcial
- reduzir impacto de grafias imperfeitas

Impacto:
- melhora muito a experiência prática
- aumenta a utilidade do sistema para o público real

---

### 7. Criar uma camada de utilitários de busca
Objetivo:
- separar regras de matching
- melhorar organização do código
- permitir testes e evolução mais segura

Impacto:
- melhora arquitetura
- facilita manutenção futura

---

### 8. Adicionar exemplos de consulta e ajuda contextual
Objetivo:
- orientar melhor o usuário
- reduzir atrito na primeira utilização
- mostrar formas esperadas de entrada

Impacto:
- melhora adoção
- diminui erro de uso

## Evoluções de longo prazo

### 9. Criar API própria de consulta
Objetivo:
- permitir reaproveitamento dos dados em outros sistemas
- abrir integração com formulários, apps ou painéis
- transformar o projeto em serviço de consulta

Impacto:
- aumenta valor do dataset
- expande potencial do projeto além do site

---

### 10. Criar painel administrativo para atualização da base
Objetivo:
- facilitar manutenção dos CEPs
- permitir revisão estruturada
- registrar alterações com mais segurança

Impacto:
- reduz manutenção manual do JSON
- melhora governança dos dados

---

### 11. Versionar datasets por data
Objetivo:
- registrar evolução da base
- permitir rastrear atualizações
- diferenciar revisão de conteúdo e estrutura

Impacto:
- melhora histórico de dados
- fortalece uso institucional

---

### 12. Expandir o projeto para dados urbanos relacionados
Objetivo:
- usar a mesma base para outros tipos de consulta territorial
- explorar bairros, áreas, regiões e organização local
- servir como semente para outros serviços cívicos

Impacto:
- transforma um utilitário simples em núcleo de informação local mais amplo

## Priorização sugerida

### Prioridade alta
- consolidar lógica de scripts
- revisar qualidade da base
- melhorar feedback da busca
- documentar melhor o comportamento do sistema

### Prioridade média
- normalizar dados
- melhorar matching textual
- separar melhor a lógica de busca

### Prioridade futura
- API
- painel administrativo
- versionamento de dados
- expansão para outros serviços urbanos

## Riscos de evolução

### Crescimento sem normalização
Se o projeto crescer mantendo o dado totalmente textual e compacto, a manutenção pode ficar mais difícil.

### Evolução de interface sem clareza de estados
Melhorias visuais sem um bom tratamento de casos de erro podem aumentar complexidade sem resolver a experiência real.

### Expansão sem separar responsabilidades
Adicionar novas funções sem reorganizar a lógica pode gerar acoplamento excessivo.

## Relevância

As evoluções sugeridas mantêm o projeto alinhado ao seu maior valor: resolver rapidamente um problema concreto da população local. O melhor roadmap para o PedreiraCep é aquele que aumenta utilidade e confiabilidade sem descaracterizar a simplicidade que hoje é uma de suas forças.

## Observações finais

O PedreiraCep não precisa virar um sistema grande para ganhar valor. O caminho mais inteligente parece ser:

- preservar simplicidade
- melhorar qualidade da base
- refinar busca
- documentar melhor
- evoluir apenas o que aumenta utilidade real