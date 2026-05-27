# Agent Skills

Colecao open source de skills reutilizaveis para agentes de IA focados em fluxo real de engenharia de software.

Este repositorio organiza instrucoes operacionais em formato `SKILL.md` para que agentes consigam executar tarefas com mais consistencia, menos ambiguidade e melhor rastreabilidade. Em vez de depender apenas de prompts livres, cada skill encapsula objetivo, quando usar, quando nao usar, passos obrigatorios, regras de decisao e, quando necessario, arquivos de apoio como `assets/`, `references/` e `scripts/`.

Repositorio: `https://github.com/JailtonJunior94/skills`

## Sumario

- [Por que este projeto existe](#por-que-este-projeto-existe)
- [Para quem este repositorio e util](#para-quem-este-repositorio-e-util)
- [O que voce encontra aqui](#o-que-voce-encontra-aqui)
- [Organizacao por perfil](#organizacao-por-perfil)
- [Skills disponiveis](#skills-disponiveis)
- [Catalogo detalhado](#catalogo-detalhado)
- [Como instalar](#como-instalar)
- [Guia operacional por agente](#guia-operacional-por-agente)
- [Como usar](#como-usar)
- [Exemplos por perfil de usuario](#exemplos-por-perfil-de-usuario)
- [Fluxo composto: discovery + publicacao no Azure DevOps](#fluxo-composto-discovery--publicacao-no-azure-devops)
- [Estrutura do repositorio](#estrutura-do-repositorio)
- [Como criar uma nova skill](#como-criar-uma-nova-skill)
- [Boas praticas para escrever skills](#boas-praticas-para-escrever-skills)
- [Contribuindo](#contribuindo)
- [Compatibilidade e observacoes](#compatibilidade-e-observacoes)
- [Licenca](#licenca)

## Por que este projeto existe

Agentes de IA costumam ter desempenho irregular quando a tarefa exige processo, criterio tecnico e disciplina operacional. Este repositorio reduz essa variacao ao transformar workflows recorrentes em skills reaproveitaveis.

Na pratica, uma skill deste repositorio ajuda o agente a:

- entender rapidamente o objetivo da tarefa;
- validar entradas obrigatorias antes de executar algo caro ou destrutivo;
- seguir uma sequencia de passos clara;
- aplicar regras de decisao consistentes;
- gerar saidas mais previsiveis para usuarios e times.

## Para quem este repositorio e util

Este projeto foi pensado para qualquer pessoa que trabalhe com agentes de IA no ciclo de desenvolvimento de software:

- desenvolvedores que querem padronizar tarefas como commits, PRs, Jira e changelogs;
- product managers e analistas que precisam estruturar discovery, backlog e PRD;
- tech leads que precisam de mais consistencia entre diferentes agentes e times;
- equipes de plataforma ou enablement que desejam compartilhar workflows internos de forma reutilizavel;
- mantenedores de repositorios de prompts e automacoes que querem evoluir de instrucoes soltas para artefatos mais estruturados;
- usuarios iniciantes que precisam de exemplos concretos para entender como uma skill e organizada.

## O que voce encontra aqui

Cada skill fica em um diretorio proprio dentro de `skills/` e normalmente contem:

- `SKILL.md`: definicao principal da skill, com frontmatter e instrucoes operacionais;
- `assets/`: templates, esquemas e artefatos usados pela skill;
- `references/`: regras auxiliares, guias e material de suporte;
- `scripts/`: scripts locais usados para validacao, classificacao ou montagem de contexto.

Isso permite manter as instrucoes mais modulares: o `SKILL.md` descreve o comportamento, enquanto os arquivos auxiliares guardam detalhes operacionais reaproveitaveis.

## Organizacao por perfil

O repositorio agora oferece duas formas de descoberta:

- `skills/` continua sendo a estrutura canonica e a fonte oficial de cada skill;
- `product-manager/`, `devteam/` e `geral/` funcionam como catalogos de navegacao por perfil de uso.

Essa classificacao nao move nem duplica skills. Ela apenas organiza a descoberta para reduzir atrito na hora de escolher a skill certa.

### `product-manager`

Foco em discovery, backlog, refinamento de escopo e consolidacao de insumos de produto.

- `epic-story-discovery`
- `us-to-prd`
- `azure-devops-epic-stories`

### `devteam`

Foco em execucao tecnica, entrega, revisao, observabilidade e artefatos operacionais de engenharia.

- `jira-tasks`
- `github-pr-comment-triage`
- `pull-request`
- `semantic-commit`
- `recursive-review-bugfix`
- `postman-collection-generator`
- `otel-grafana-dashboards`
- `otel-hybrid-dashboard-blueprint`

### `geral`

Skills transversais, uteis tanto para PM quanto para dev team.

- `prompt-enricher`
- `github-diff-changelog-publisher`
- `github-release-publication-flow`
- `confluence-changelog-publisher`

## Skills disponiveis

Atualmente o catalogo contem 15 skills ativas no workspace.

| Skill | Perfil | Objetivo principal | Casos de uso tipicos |
| --- | --- | --- | --- |
| `azure-devops-epic-stories` | `product-manager` | Publicar bundles de discovery como epico e user stories no Azure DevOps com validacao, deduplicacao e audit log. | Criacao de backlog estruturado no ADO, publicacao de epicos, sincronizacao discovery -> board. |
| `confluence-changelog-publisher` | `geral` | Publicar changelogs e resumos tecnicos no Confluence com confirmacao humana antes de consultar e antes de escrever. | Release notes, resumos de PR, changelog em wiki interna. |
| `epic-story-discovery` | `product-manager` | Conduzir discovery estruturada de epico e user stories com perguntas obrigatorias e bundle local validado. | Refinamento de feature, pre-backlog, estruturacao de US antes de Jira ou ADO. |
| `github-diff-changelog-publisher` | `geral` | Ler diffs do GitHub e gerar changelogs ou resumos publicaveis baseados em evidencia. | Release notes, resumo de PR, comparacao entre branches. |
| `github-pr-comment-triage` | `devteam` | Classificar comentarios de PR e transformar review em fila rastreavel de decisao e resposta. | Triagem de review comments, preparacao de respostas, follow-up de feedback tecnico. |
| `github-release-publication-flow` | `geral` | Orquestrar analise de diff, geracao de changelog e publicacao aprovada em GitHub ou Confluence. | Fluxo completo de release publication. |
| `jira-tasks` | `devteam` | Criar tasks no Jira a partir de decomposicao tecnica local. | Publicacao de `tasks.md`, criacao de subtarefas, sincronizacao de task bundle. |
| `otel-grafana-dashboards` | `devteam` | Gerar dashboards Grafana prontos para producao a partir de codebases Go com OpenTelemetry. | Painis de metricas, traces e logs para servicos instrumentados. |
| `otel-hybrid-dashboard-blueprint` | `devteam` | Montar blueprint de observabilidade hibrida para Grafana e Coralogix com OTel. | Padronizacao de dashboards, desenho inicial de observabilidade, planejamento SRE. |
| `postman-collection-generator` | `devteam` | Gerar collections Postman realistas a partir do codigo da API. | Onboarding de APIs, colecoes para testes exploratorios e integracao. |
| `prompt-enricher` | `geral` | Reescrever prompts brutos em prompts mais robustos, compactos e operacionais. | Hardening de prompts, economia de tokens, melhoria de confiabilidade de agentes. |
| `pull-request` | `devteam` | Gerar, revisar, criar ou atualizar PRs com base em diff, commits e contexto do repositorio. | Rascunho de PR, publicacao via GitHub, revisao de titulo e body. |
| `recursive-review-bugfix` | `devteam` | Orquestrar um ciclo iterativo de review e bugfix ate atingir veredito aprovado. | Validacao final pre-merge, reducao de achados criticos, fechamento de lacunas de qualidade. |
| `semantic-commit` | `devteam` | Sugerir ou revisar mensagens de commit semantico com Conventional Commits. | Commit message generation, classificacao de tipo, split de commits. |
| `us-to-prd` | `product-manager` | Ler uma user story no Jira e consolidar o contexto necessario para iniciar um PRD. | Transformar US em insumo para PRD, consolidar requisitos e dependencias do Jira. |

## Catalogo detalhado

### `azure-devops-epic-stories`

Objetivo: consumir um bundle produzido por `epic-story-discovery` e publicar epico mais user stories no Azure DevOps com processo detectado automaticamente, checagem de duplicata deterministica, batching e audit log.

Entradas esperadas:
- bundle local em `./discoveries/epic-<slug>/`;
- `organization`, `project` e `board`, informados pelo usuario ou por `.ado-epic-stories.yml`.

Saida principal:
- work items criados no Azure DevOps;
- `audit-<timestamp>.json` no bundle.

Use quando:
- voce ja concluiu a discovery e quer materializar backlog no ADO;
- precisa de dry-run antes de criar work items;
- quer reconciliar criacoes por audit log.

Nao use quando:
- a discovery ainda nao foi feita;
- o objetivo e criar tasks tecnicas detalhadas;
- o destino nao e Azure DevOps.

Dependencias:
- Azure DevOps MCP;
- Python 3;
- bundle valido de `epic-story-discovery`.

### `confluence-changelog-publisher`

Objetivo: publicar changelogs e resumos tecnicos em paginas do Confluence com confirmacao explicita antes da consulta e antes da escrita.

Entradas esperadas:
- conteudo final ou texto-base aprovado;
- `space`, `title` e modo de publicacao;
- opcionalmente ID, URL, pagina-pai ou publicacao na raiz.

Saida principal:
- pagina criada ou atualizada no Confluence;
- conteudo final pronto para uso manual quando a publicacao nao acontecer.

Use quando:
- precisa publicar release notes ou resumo tecnico em wiki;
- precisa de rastreabilidade e confirmacao humana.

Nao use quando:
- quer publicacao automatica sem revisao;
- o destino nao e Confluence;
- o texto final ainda nao existe.

Dependencias:
- Atlassian MCP;
- Python 3.

### `epic-story-discovery`

Objetivo: conduzir discovery estruturada de epico e user stories em PT-BR, com pelo menos duas rodadas obrigatorias de perguntas e validacao sem falso positivo.

Entradas esperadas:
- nome curto ou contexto da feature;
- descricao do problema, objetivo, personas e restricoes.

Saida principal:
- bundle local em `discoveries/epic-<slug>/` com `bundle.json`, `epic.md`, `us/` e `transcript.md`.

Use quando:
- precisa refinar uma feature antes de criar backlog;
- quer padronizar discovery com KPIs, trade-offs e edge cases;
- precisa de um bundle reutilizavel para ADO, Jira, GitHub Issues ou PRD local.

Nao use quando:
- quer criar work items diretamente sem etapa de discovery;
- quer apenas um PRD sem epico e US.

Dependencias:
- Python 3;
- escrita local no repositorio.

### `github-diff-changelog-publisher`

Objetivo: ler diffs do GitHub para releases, PRs, branches ou compares e produzir um changelog claro, objetivo e publicavel.

Entradas esperadas:
- repositorio no GitHub;
- origem do diff, como release, PR, branch ou compare;
- confirmacao do destino de publicacao, quando houver.

Saida principal:
- changelog estruturado;
- opcionalmente publicacao no GitHub ou handoff para Confluence.

Use quando:
- precisa de release notes baseadas em evidencia;
- quer resumir impacto de uma comparacao de branches;
- precisa preparar conteudo antes de publicar.

Nao use quando:
- o repositorio nao esta no GitHub;
- o changelog e puramente de marketing sem diff de origem.

Dependencias:
- GitHub;
- ferramentas nativas do GitHub e possivel fallback web;
- opcionalmente Atlassian MCP para Confluence.

### `github-pr-comment-triage`

Objetivo: transformar comentarios ja publicados em uma PR em uma fila clara de decisao, resposta e possivel implementacao.

Entradas esperadas:
- identificador da PR;
- acesso ao GitHub via `gh`;
- opcionalmente politica de resposta ou idioma.

Saida principal:
- classificacao dos comentarios;
- resposta sugerida por item;
- plano de acao rastreavel.

Use quando:
- quer consolidar feedback de code review;
- precisa responder comentarios em pt-BR;
- quer decidir o que implementar e o que apenas justificar.

Nao use quando:
- nao existem comentarios publicados;
- o objetivo e abrir PR ou fazer review do zero.

Dependencias:
- `gh`;
- acesso ao GitHub.

### `github-release-publication-flow`

Objetivo: orquestrar de ponta a ponta a leitura de diffs do GitHub, a geracao de changelog e a publicacao aprovada pelo usuario.

Entradas esperadas:
- origem do diff no GitHub;
- destino final, GitHub ou Confluence;
- confirmacoes obrigatorias do usuario.

Saida principal:
- changelog final;
- publicacao concluida ou conteudo pronto para uso manual.

Use quando:
- precisa de um fluxo unico entre analise e publicacao;
- quer reduzir etapas manuais em release notes.

Nao use quando:
- o conteudo ja esta pronto e voce so precisa publicar;
- nao ha aprovacao humana para escrita.

Dependencias:
- GitHub;
- opcionalmente Atlassian MCP.

### `jira-tasks`

Objetivo: publicar decomposicao tecnica local como tasks abaixo de uma user story no Jira, resolvendo tipo, campos obrigatorios, estimativa e assignee.

Entradas esperadas:
- user story de destino;
- arquivos locais de task ou bundle de decomposicao;
- acesso ao Jira.

Saida principal:
- tasks criadas e vinculadas abaixo da US.

Use quando:
- a discovery ja virou plano tecnico;
- quer sincronizar `tasks.md` ou bundle local com Jira.

Nao use quando:
- precisa fazer discovery do zero;
- quer criar PRD;
- nao existe uma US pai clara.

Dependencias:
- Jira MCP ou integracao equivalente;
- arquivos locais de decomposicao.

### `otel-grafana-dashboards`

Objetivo: gerar dashboards Grafana prontos para producao com base em uma codebase Go instrumentada com OpenTelemetry.

Entradas esperadas:
- codebase Go com instrumentacao OTel;
- metricas, traces e logs acessiveis pelos padroes esperados.

Saida principal:
- arquivos JSON de dashboard Grafana;
- opcionalmente artefatos de suporte para ambiente local.

Use quando:
- precisa criar paineis para servicos ja instrumentados;
- quer acelerar observabilidade padronizada para Grafana.

Nao use quando:
- a aplicacao nao usa OTel;
- o foco e apenas infraestrutura;
- o objetivo e configurar collectors ou ingestao.

Dependencias:
- codebase Go;
- OpenTelemetry;
- Grafana.

### `otel-hybrid-dashboard-blueprint`

Objetivo: desenhar um blueprint de observabilidade hibrida para Grafana e Coralogix com padronizacao de metricas, logs, traces, SLOs e variaveis.

Entradas esperadas:
- contexto do servico;
- definicao minima de ambiente, sinais e necessidades de observabilidade.

Saida principal:
- JSON Grafana importavel;
- estrutura equivalente para Coralogix.

Use quando:
- precisa padronizar dashboards entre local e producao;
- quer um blueprint antes de gerar dashboards definitivos.

Nao use quando:
- o servico nao e baseado em OTel;
- quer apenas configuracao de ingestao;
- quer conversao direta de um dashboard ja pronto.

Dependencias:
- OTel;
- Grafana;
- Coralogix.

### `postman-collection-generator`

Objetivo: analisar handlers, DTOs, modelos e middlewares para montar uma collection Postman realista e util para onboarding ou integracao.

Entradas esperadas:
- codebase HTTP em Go, C# ou TypeScript;
- rotas e contratos no codigo.

Saida principal:
- collection Postman com cenarios de sucesso e erro.

Use quando:
- precisa documentar endpoints a partir do codigo;
- quer uma collection para onboard ou testes exploratorios.

Nao use quando:
- o objetivo e gerar OpenAPI;
- o servico nao e HTTP;
- quer testes unitarios.

Dependencias:
- codebase suportada;
- schema/validacao local da collection.

### `prompt-enricher`

Objetivo: transformar um prompt bruto em um prompt mais robusto, objetivo e economico em tokens, com contrato de saida e restricoes explicitas.

Entradas esperadas:
- prompt bruto;
- opcionalmente contexto, restricoes e criterio de aceite.

Saida principal:
- prompt reescrito e operacionalizado.

Use quando:
- um prompt esta fragil, vago ou prolixo;
- quer melhorar latencia e confiabilidade de um agente ou chamada de API.

Nao use quando:
- quer selecionar modelo;
- quer avaliar output;
- quer escrever requisitos amplos de produto.

Dependencias:
- nenhuma integracao externa obrigatoria.

### `pull-request`

Objetivo: gerar, revisar, criar ou atualizar PRs com base em diff, commits e contexto do repositorio, produzindo titulo e body em pt-BR.

Entradas esperadas:
- branch atual;
- diff local ou remoto;
- opcionalmente modo de publicacao.

Saida principal:
- titulo e body da PR;
- opcionalmente PR criada ou atualizada no GitHub.

Use quando:
- precisa abrir PR com melhor qualidade editorial;
- quer revisar se a PR atual representa corretamente as mudancas;
- quer rascunho antes de publicar.

Nao use quando:
- o objetivo e code review profundo;
- precisa apenas de mensagem de commit;
- nao existe delta util entre base e `HEAD`.

Dependencias:
- Git;
- `gh` para escrita remota.

### `recursive-review-bugfix`

Objetivo: executar um ciclo iterativo de review critica e bugfix guiado por artefatos de PRD, TechSpec e tasks ate obter aprovacao sem achados criticos ou importantes.

Entradas esperadas:
- caminho da pasta com os artefatos de referencia;
- diff atual a ser revisado.

Saida principal:
- rodadas sucessivas de review e correcao;
- resumo executivo com achados resolvidos e comandos de validacao executados.

Use quando:
- quer uma validacao final rigorosa antes de merge;
- precisa eliminar achados importantes com base em requisitos explicitamente documentados.

Nao use quando:
- precisa apenas de uma revisao pontual;
- nao existem artefatos de contexto suficientes;
- o objetivo e abrir PR.

Dependencias:
- skills `review` e `bugfix` disponiveis no ambiente;
- artefatos locais de produto e implementacao.

### `semantic-commit`

Objetivo: sugerir, revisar ou refinar mensagens de commit semantico com Conventional Commits e criterio explicito de classificacao.

Entradas esperadas:
- `git diff --staged`, `git diff` ou descricao clara das mudancas.

Saida principal:
- cabecalho de commit validado;
- opcionalmente sugestao de split em multiplos commits.

Use quando:
- quer padronizar commit messages;
- precisa decidir tipo, scope e breaking change;
- quer resumo curto alinhado a um commit ou PR.

Nao use quando:
- quer criar o commit automaticamente;
- precisa de revisao tecnica detalhada do codigo.

Dependencias:
- Git;
- Python 3 para o validador do cabecalho.

### `us-to-prd`

Objetivo: ler uma user story completa no Jira e consolidar o contexto necessario para iniciar a criacao de um PRD.

Entradas esperadas:
- issue key no formato `PROJ-123`;
- opcionalmente `cloudId`.

Saida principal:
- contexto consolidado para invocar o fluxo de criacao de PRD.

Use quando:
- a US ja existe no Jira e voce quer subir o nivel para PRD;
- precisa preservar comentarios, dependencias e contexto funcional relevante.

Nao use quando:
- nao existe issue de origem;
- o objetivo e apenas consultar Jira sem preparar PRD.

Dependencias:
- Atlassian MCP;
- Python 3;
- fluxo `.claude/commands/create-prd.md`.

## Como instalar

Nao existe um unico modo universal de instalacao, porque diferentes agentes carregam skills de formas diferentes. A abordagem correta depende do ambiente em que voce pretende consumir este repositorio.

### Opcao 1: instalar via comando do seu ambiente

Se o seu runtime de agentes suporta adicionar skills diretamente a partir de um repositorio Git, use a URL publica do projeto:

```bash
npx skills add https://github.com/JailtonJunior94/skills
```

Use esta opcao quando seu ambiente ja entende a convencao de pastas e o formato `SKILL.md`.

### Opcao 2: clonar o repositorio localmente

Esta e a opcao mais universal para exploracao, contribuicao e uso manual.

```bash
git clone https://github.com/JailtonJunior94/skills.git
cd skills
```

Depois disso, voce pode:

- apontar sua ferramenta para este diretorio;
- copiar apenas as skills que interessam;
- criar links simbolicos para uma pasta de skills do seu agente.

### Opcao 3: copiar uma skill especifica

Se voce quer testar apenas uma skill, copie somente o diretorio desejado:

```bash
mkdir -p ~/.claude/skills
cp -R skills/semantic-commit ~/.claude/skills/semantic-commit
```

Esse mesmo padrao pode ser adaptado para qualquer pasta de skills usada pelo seu agente.

### Opcao 4: link simbolico para desenvolvimento local

Durante desenvolvimento, o link simbolico costuma ser a opcao mais pratica porque evita copiar arquivos a cada mudanca:

```bash
mkdir -p ~/.claude/skills
ln -s "$(pwd)/skills" ~/.claude/skills/custom-skills
```

Se o seu ambiente usar outro diretorio-base, troque `~/.claude/skills` pelo caminho equivalente.

### Requisitos minimos

Os requisitos variam por skill, mas em geral voce vai precisar de:

- Git para clonar e atualizar o repositorio;
- um agente ou runtime que reconheca skills baseadas em `SKILL.md`;
- Python 3 para skills que dependem de scripts locais de validacao;
- ferramentas externas especificas em alguns casos, como `gh`, integracoes com Jira/Confluence, Azure DevOps ou MCPs correspondentes.

## Guia operacional por agente

Se voce quer um material mais pratico, com prompts `mandatorio`, `eficiente` e `economico` para cada skill e notas de uso em `Claude Code`, `Codex`, `Gemini` e `Copilot CLI`, use o handbook central:

- [Handbook de Skills](docs/skills-handbook.md)

Ele nao substitui os `SKILL.md`; funciona como guia de invocacao, compatibilidade e economia de tokens.

## Como usar

Depois de instalar a skill no ambiente correto, voce normalmente a invoca pelo nome no prompt ou no fluxo do agente.

### Exemplo basico

```text
Use a skill semantic-commit para sugerir uma mensagem de commit para as mudancas atuais.
```

### Exemplo com contexto operacional

```text
Use a skill pull-request para gerar um rascunho de PR em pt-BR a partir da branch atual.
```

### Exemplo com destino externo

```text
Use a skill jira-tasks para criar tasks filhas da US PAY-142 a partir do bundle local em ./tasks/prd-checkout/.
```

### Exemplo de reescrita de prompt

```text
Use a skill prompt-enricher para transformar este prompt bruto em uma versao mais robusta e economica em tokens.
```

### Exemplo de discovery e publicacao no Azure DevOps

```text
Use a skill epic-story-discovery para refinar um epico de onboarding self-service. Hoje 35% dos novos clientes abandonam no passo de validacao de documentos.
```

```text
Use a skill azure-devops-epic-stories para publicar o bundle em ./discoveries/epic-onboarding-self-service/ na organizacao acme-co, projeto Plataforma, board Squad-Aquisicao. Faca dry-run antes de criar.
```

## Exemplos por perfil de usuario

### 1. Pessoa desenvolvedora que quer produtividade imediata

Objetivo: reaproveitar skills prontas sem mexer na estrutura interna.

Exemplos:

```text
Use a skill semantic-commit para classificar meu diff atual e sugerir uma mensagem de commit.
```

```text
Use a skill pull-request para montar titulo e body da PR com base na branch atual.
```

```text
Use a skill github-pr-comment-triage para analisar os comentarios da PR 128 e montar uma fila de decisao.
```

### 2. Maintainer ou tech lead que quer padronizar o time

Objetivo: adotar um conjunto de workflows previsiveis para reduzir variacao entre agentes e pessoas.

Exemplos:

```text
Use a skill github-release-publication-flow para gerar e revisar o changelog da release antes de publicar.
```

```text
Use a skill jira-tasks para transformar esta decomposicao local em tasks filhas no Jira, preservando assignee e estimativa.
```

```text
Use a skill us-to-prd para consolidar a US PROJ-231 e preparar o contexto do PRD.
```

```text
Use a skill epic-story-discovery para refinar a feature de portal de assinaturas com pelo menos duas rodadas de clarificacao, e em seguida a skill azure-devops-epic-stories para publicar o bundle resultante no projeto Plataforma do Azure DevOps.
```

### 3. Pessoa autora de novas skills

Objetivo: usar este repositorio como referencia de estrutura e estilo.

Exemplos:

```text
Leia a skill semantic-commit e use o padrao dela para criar uma nova skill de release review.
```

```text
Use a skill prompt-enricher como referencia para separar SKILL.md, assets, references e scripts na minha nova skill.
```

### 4. Equipe de plataforma ou enablement

Objetivo: manter skills versionadas, revisaveis e distribuidas em um repositorio unico.

Exemplos:

- versionar workflows internos como codigo revisavel;
- compartilhar templates e regras auxiliares em `assets/` e `references/`;
- centralizar automacoes com scripts pequenos e de responsabilidade clara;
- reaproveitar o mesmo desenho de skill em multiplos agentes, com pequenas adaptacoes de integracao.

## Fluxo composto: discovery + publicacao no Azure DevOps

As skills `epic-story-discovery` e `azure-devops-epic-stories` foram desenhadas para trabalhar em pipeline. A primeira faz a descoberta de produto/feature com rigor metodologico e gera um bundle local versionavel; a segunda consome o bundle e publica o epico mais as user stories no Azure DevOps. Esta separacao traz quatro ganhos praticos:

- **Reutilizacao** do mesmo bundle em outros destinos, como Jira, GitHub Issues, Confluence ou PRD interno, sem repetir a discovery.
- **Retomada** sem perda de contexto se a publicacao no ADO falhar parcialmente ou se o usuario quiser revisar antes de criar.
- **Auditoria** clara via `transcript.md` na discovery e `audit-<timestamp>.json` na publicacao.
- **Portabilidade entre agentes**: a discovery roda 100% local em qualquer agente que suporte `SKILL.md`; a publicacao depende apenas de um MCP do Azure DevOps configurado.

### Diagrama do pipeline

```text
                ┌─────────────────────────────┐
  pedido do  →  │   epic-story-discovery      │  →  ./discoveries/epic-<slug>/
   usuario      │  - coleta contexto          │       ├── bundle.json
                │  - Rodada 1 obrigatoria     │       ├── epic.md
                │  - Rodada 2 obrigatoria     │       ├── transcript.md
                │  - rodadas extras se ambiguo│       └── us/
                │  - valida sem falso positivo│           ├── 01_<slug>.md
                └─────────────────────────────┘           └── 02_<slug>.md
                              │
                              ▼
                ┌─────────────────────────────┐
                │ azure-devops-epic-stories   │  →  Work items no ADO
                │  - le .ado-epic-stories.yml │       + audit-<timestamp>.json
                │  - detecta processo         │
                │  - normaliza titulo (dedup) │
                │  - cria epico + US          │
                │  - vincula via Parent       │
                │  - batching 10 por execucao │
                └─────────────────────────────┘
```

### Quando usar cada skill isoladamente

- Use **apenas** `epic-story-discovery` quando voce ainda nao decidiu o destino, vai publicar em outra ferramenta, quer revisar o bundle em PR antes de publicar, ou precisa apenas materializar um artefato local.
- Use **apenas** `azure-devops-epic-stories` quando voce ja tem um bundle pronto produzido em sessao anterior, quer republicar apos correcao, ou esta consumindo um bundle gerado por outro membro do time.

### Exemplo end-to-end

Cenario: time de 6 pessoas quer criar um epico de autenticacao self-service e quatro user stories no Azure DevOps de uma organizacao chamada `acme-co` no projeto `Plataforma`, board `Squad-Acesso`.

**Passo 1: registrar defaults do time (opcional, uma unica vez por repositorio)**

Crie `.ado-epic-stories.yml` na raiz do repositorio para evitar reinformar organizacao, projeto e board a cada execucao:

```yaml
organization: acme-co
project: Plataforma
board: Squad-Acesso
# process: Agile
# child_type_override:
```

**Passo 2: rodar a discovery**

```text
Use a skill epic-story-discovery para refinar um epico de autenticacao self-service de clientes finais. Hoje o suporte recebe cerca de 1200 tickets/mes de acesso. Queremos reduzir esse volume oferecendo recuperacao de senha, desbloqueio de conta e MFA opcional.
```

**Passo 3: revisar o bundle (opcional, mas recomendado para times maiores)**

Os arquivos sao markdown puro em PT-BR. Versione em git, abra PR e use `transcript.md` como trilha de decisao da discovery.

**Passo 4: publicar no Azure DevOps**

```text
Use a skill azure-devops-epic-stories para publicar o bundle em ./discoveries/epic-auth-self-service/ no Azure DevOps.
```

O agente vai:

1. Carregar defaults do `.ado-epic-stories.yml`.
2. Detectar o processo do projeto e escolher o tipo de child correto.
3. Normalizar o titulo do epico e consultar WIQL para detectar duplicata.
4. Apresentar o plano final e perguntar se voce quer criar agora, fazer dry-run ou cancelar.
5. Criar o epico, criar cada US, vincular via `System.LinkTypes.Hierarchy-Reverse` e gravar `audit-<timestamp>.json`.

## Estrutura do repositorio

Estrutura atual, em alto nivel:

```text
devteam/
├── README.md
geral/
├── README.md
product-manager/
├── README.md
skills/
├── azure-devops-epic-stories/
├── confluence-changelog-publisher/
├── epic-story-discovery/
├── github-diff-changelog-publisher/
├── github-pr-comment-triage/
├── github-release-publication-flow/
├── jira-tasks/
├── otel-grafana-dashboards/
├── otel-hybrid-dashboard-blueprint/
├── postman-collection-generator/
├── prompt-enricher/
├── pull-request/
├── recursive-review-bugfix/
├── semantic-commit/
└── us-to-prd/
```

Exemplo de estrutura interna de uma skill:

```text
skills/semantic-commit/
├── SKILL.md
├── assets/
├── references/
└── scripts/
```

## Como criar uma nova skill

O formato basico e simples, mas o valor real esta em escrever instrucoes testaveis, especificas e orientadas a fluxo.

### Passo 1: criar o diretorio

```bash
mkdir -p skills/minha-skill
```

### Passo 2: criar o `SKILL.md`

```yaml
---
name: minha-skill
description: Descreva de forma objetiva o que a skill faz, quando usar e quando nao usar.
---

# Minha Skill

## Procedimentos
1. Validar a entrada obrigatoria.
2. Coletar o contexto minimo necessario.
3. Executar a tarefa principal com regras claras.
4. Retornar um resultado verificavel.
```

### Passo 3: adicionar arquivos auxiliares quando fizer sentido

Use:

- `assets/` para templates, schemas e modelos de saida;
- `references/` para regras detalhadas e criterios de decisao;
- `scripts/` para validacoes locais, classificacoes e utilitarios pequenos.

### Passo 4: testar a skill no agente alvo

Valide pelo menos:

- se o nome da skill esta claro e coerente com a tarefa;
- se a descricao explica bem quando usar e quando nao usar;
- se o fluxo nao depende de inferencias fracas;
- se os passos sao executaveis no ambiente real;
- se a saida final e util para o usuario final.

## Boas praticas para escrever skills

Se voce pretende contribuir ou criar skills inspiradas neste repositorio, estes principios ajudam bastante:

- prefira instrucoes operacionais a texto promocional;
- declare entradas obrigatorias e estados de erro cedo;
- diferencie claramente "usar" de "nao usar";
- preserve fatos observaveis e evite que a skill invente contexto;
- mantenha scripts pequenos e com responsabilidade unica;
- use `references/` para regras extensas, em vez de inflar o `SKILL.md`;
- escreva outputs que possam ser auditados por uma pessoa.

Exemplo de descricao ruim:

```yaml
description: Ajuda com Jira.
```

Exemplo de descricao melhor:

```yaml
description: Cria tasks no Jira abaixo de uma User Story com base em arquivos locais de decomposicao, resolvendo campos obrigatorios, assignee e estimativas antes da criacao.
```

## Contribuindo

Contribuicoes sao bem-vindas, especialmente para:

- adicionar novas skills reutilizaveis;
- melhorar clareza e seguranca de skills existentes;
- incluir `assets`, `references` e `scripts` que reduzam ambiguidade operacional;
- corrigir exemplos, documentacao e instrucoes obsoletas.

Fluxo sugerido:

1. Faca um fork do repositorio.
2. Crie uma branch para sua alteracao.
3. Adicione ou atualize a skill com foco em comportamento verificavel.
4. Revise o README e a estrutura da skill para manter consistencia.
5. Abra um Pull Request explicando o problema resolvido e o impacto esperado.

Se a sua contribuicao introduzir uma nova skill, inclua no PR:

- objetivo da skill;
- quando usar e quando nao usar;
- exemplos de prompt ou invocacao;
- dependencias externas relevantes;
- riscos ou limitacoes conhecidas.

## Compatibilidade e observacoes

- Este repositorio nao assume um unico agente. A mesma skill pode exigir pequenas adaptacoes dependendo do runtime que a consome.
- Algumas skills dependem de ferramentas externas como `gh`, Jira, Confluence, Azure DevOps, MCPs ou scripts Python locais.
- Nem toda skill e universalmente portavel sem ajustes de integracao.
- Os diretorios `product-manager/`, `devteam/` e `geral/` sao catalogos de navegacao. A fonte oficial continua sendo `skills/`.

## Licenca

No momento, este repositorio nao possui um arquivo `LICENSE` versionado na raiz. Se voce pretende reutilizar este conteudo em ambiente aberto ou comercial, o ideal e adicionar uma licenca explicita antes da redistribuicao formal.
