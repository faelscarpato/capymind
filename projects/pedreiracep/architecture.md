# Architecture — PedreiraCep

## Resumo

O PedreiraCep aparenta ser uma aplicação web leve e orientada a consulta local de dados, construída para permitir a busca de novos CEPs da cidade de Pedreira-SP. A arquitetura percebida é predominantemente **frontend-first**, com uma base de dados local em arquivo JSON e uma interface simples para pesquisa e exibição de resultados.

## Origem

- Repositório original: `https://github.com/faelscarpato/pedreiracep`
- Projeto documentado no CapyMind como representação leve
- O código completo permanece no repositório original e não foi copiado para este repositório

## Detectado

### Estrutura central percebida

O núcleo do projeto parece ser formado por:

- `index.html` como ponto principal de interface
- `style.css` como camada de apresentação visual
- `script.js` e/ou `scripts.js` como camada de interação e lógica de busca
- `Ceps.json` como fonte principal de dados
- `README.md` como documentação geral do projeto

### Modelo arquitetural observado

A arquitetura indica um fluxo simples de aplicação web estática ou semi-estática:

1. o usuário acessa a interface principal
2. a interface recebe um termo de busca
3. a camada de script processa a entrada
4. a aplicação consulta a base local de CEPs
5. os resultados são exibidos dinamicamente na interface

### Papel de cada camada

#### Camada de interface
Responsável por:

- entrada de busca
- renderização de lista ou tabela
- exibição de resultados
- adaptação responsiva para diferentes telas

#### Camada de comportamento
Responsável por:

- capturar eventos de digitação ou pesquisa
- filtrar ou localizar registros compatíveis
- atualizar a interface com os resultados encontrados

#### Camada de dados
Responsável por:

- manter o mapeamento entre logradouro/bairro e CEP
- servir como fonte de verdade do projeto
- permitir consulta textual direta

## Estrutura lógica sugerida

### 1. Presentation Layer
Composta por HTML e CSS, define:

- layout
- componentes visuais
- responsividade
- organização da busca e dos resultados

### 2. Interaction Layer
Composta por JavaScript no cliente, define:

- leitura da entrada do usuário
- busca por rua, bairro ou CEP
- tratamento da lista de resultados
- atualização dinâmica da página

### 3. Data Layer
Composta principalmente por `Ceps.json`, define:

- conjunto de registros consultáveis
- estrutura textual das chaves
- relacionamento entre endereço e CEP

## Fluxo de operação percebido

### Fluxo principal
1. o usuário digita um bairro, rua ou CEP
2. o script interpreta o termo informado
3. a aplicação busca correspondências na base de dados
4. a interface exibe os resultados compatíveis
5. o usuário refina ou altera a consulta

### Fluxo de consulta por CEP
1. o usuário informa um CEP
2. o script tenta localizar correspondência textual ou reversa
3. a aplicação mostra o endereço relacionado, quando disponível

### Fluxo de consulta por endereço
1. o usuário informa nome de rua, bairro ou parte do endereço
2. o script filtra entradas compatíveis
3. o sistema retorna o CEP correspondente ou uma lista de possíveis matches

## Organização semântica dos dados

A base de dados aparenta seguir uma convenção simples:

- chave: `"logradouro - bairro"`
- valor: `"CEP"`

Esse formato favorece uma implementação rápida de busca textual, mas também traz algumas implicações arquiteturais:

- forte dependência de consistência na grafia
- necessidade de normalização para buscas mais tolerantes
- possível dificuldade para consultas estruturadas por campos separados

## Decisões arquiteturais implícitas

O projeto parece ter sido desenhado para privilegiar:

- simplicidade de implementação
- manutenção direta da base
- resposta rápida no frontend
- independência de APIs externas
- facilidade de publicação como site leve

## Inferido

### Arquitetura predominante
Tudo indica que o projeto funciona majoritariamente como uma aplicação de consulta client-side, com baixa complexidade operacional e foco em utilidade pública/local.

### Backend
O README menciona tecnologias como PHP e MySQL, mas, pela estrutura principal conhecida do repositório, isso não se mostra como camada central obrigatória para compreender o funcionamento atual. Pode indicar:

- uma intenção anterior de expansão
- uma base local de desenvolvimento
- ou uma documentação mais ampla do que a implementação mínima realmente necessária

### Escalabilidade
Para o escopo atual, a arquitetura é suficiente. Para crescer, seria interessante separar melhor:

- dados
- mecanismos de normalização
- camada de busca
- regras de correspondência
- administração da base

## Pontos fortes da arquitetura

- simples de entender
- baixa barreira de manutenção
- boa adequação a um projeto utilitário local
- dependência reduzida de infraestrutura complexa
- fonte de dados clara e direta

## Limitações percebidas

- busca textual pode depender demais da grafia exata
- estrutura de dados pouco normalizada
- possível duplicidade de lógica se existirem múltiplos scripts
- ausência aparente de camada explícita de validação de dados
- crescimento futuro pode exigir abstração melhor da base de CEPs

## Direções de evolução

### Curto prazo
- documentar melhor o fluxo de busca
- consolidar a lógica entre `script.js` e `scripts.js`, se houver sobreposição
- explicitar como a base é carregada e filtrada
- registrar limites da busca textual

### Médio prazo
- normalizar a base em campos separados
- criar busca tolerante a acentos, variações e abreviações
- estruturar melhor os dados por bairro, logradouro e CEP
- adicionar camada de utilitários para parsing e matching

### Longo prazo
- disponibilizar API própria de consulta
- criar painel de atualização dos dados
- versionar datasets por data de atualização
- permitir integração com outros projetos locais ou cívicos

## Relevância

A arquitetura do PedreiraCep é relevante no CapyMind como exemplo de:

- utilitário cívico/local de baixo atrito
- aplicação orientada a dataset
- projeto simples com forte valor prático
- base potencial para evoluções futuras em dados públicos, consulta geográfica ou serviços municipais

## Observações finais

O projeto não aparenta exigir uma arquitetura pesada para cumprir seu objetivo principal. Seu valor está na clareza da proposta, no uso direto da base de dados e na facilidade de acesso para o usuário final.

Para o CapyMind, o mais importante é registrar que o PedreiraCep é um projeto de consulta pública orientado por dataset local, com arquitetura simples, frontend dominante e forte dependência da qualidade da base `Ceps.json`.