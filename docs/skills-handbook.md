# Handbook de Skills

Guia operacional do repositorio para uso das 15 skills com `Claude Code`, `Codex`, `Gemini` e `Copilot CLI`.

Este handbook nao substitui os `SKILL.md`. Ele resume:
- quando usar cada skill;
- quais entradas sao obrigatorias;
- quais tools e dependencias precisam existir;
- exemplos de prompts `mandatorio`, `eficiente` e `economico`;
- onde a compatibilidade entre agentes e parcial.

## Regras Gerais por Agente

### `Claude Code`

Use quando a skill estiver instalada no ambiente do agente e puder ser descoberta nativamente.

Bootstrap recomendado:

```text
Use a skill <nome-da-skill> e siga integralmente skills/<nome-da-skill>/SKILL.md.
Se a skill exigir perguntas estruturadas, use a ferramenta de perguntas do agente.
Se faltar alguma dependencia externa, pare e informe exatamente o que falta.
```

### `Codex`

Nao ha auto-discovery de skills neste repo. O uso mais seguro e apontar explicitamente para o `SKILL.md`.

Bootstrap recomendado:

```text
Siga skills/<nome-da-skill>/SKILL.md como instrucao canonica.
Use os scripts, assets e references da skill quando ela mandar.
Se a skill mencionar uma tool especifica do Claude, substitua por pergunta em prosa ou pela tool equivalente do ambiente.
```

### `Gemini`

O padrao seguro e o mesmo do Codex: instruir explicitamente o caminho da skill.

Bootstrap recomendado:

```text
Use skills/<nome-da-skill>/SKILL.md como checklist obrigatorio.
Leia os arquivos em assets/, references/ e scripts/ apenas quando a skill pedir.
Se nao existir uma tool citada na skill, mantenha o fluxo e reporte a limitacao sem inventar equivalencia.
```

### `Copilot CLI`

Neste repo a cobertura e parcial. Use `Copilot CLI` como executor manual de prompt e shell. Nao assuma suporte a MCP, skills nativas ou tools nomeadas igual a Claude/Codex/Gemini.

Bootstrap recomendado:

```text
Use skills/<nome-da-skill>/SKILL.md como procedimento manual.
Execute apenas os comandos locais e integracoes realmente disponiveis neste ambiente.
Se a skill depender de MCP, workflow nativo do Claude ou outra integracao ausente, pare e registre a limitacao.
```

## Padroes de Tooling

Use estes mapeamentos antes de adaptar uma skill para outro agente:

| Padrao no repo | O que significa na pratica |
| --- | --- |
| `python3 scripts/...` | Script local obrigatorio de validacao, classificacao ou montagem. |
| `gh ...` | A skill depende de GitHub CLI instalado e autenticado. |
| `atlassian-*` | A skill depende de MCP ou integracao equivalente do Jira/Confluence. |
| `azure-devops-*` ou equivalente MCP | A skill depende de MCP do Azure DevOps. |
| `AskUserQuestion` | Em agentes sem essa tool, substitua por pergunta curta em prosa e aguarde resposta. |
| `.claude/commands/...` | Dependencia especifica de ambiente Claude. Fora dele a compatibilidade e parcial. |
| skills `review` e `bugfix` | Dependencias cruzadas; se nao existirem no ambiente, a skill fica bloqueada. |

## Matriz Rapida de Compatibilidade

| Tipo de skill | Claude Code | Codex | Gemini | Copilot CLI |
| --- | --- | --- | --- | --- |
| Local + scripts | alto | alto | alto | medio |
| GitHub com `gh` | alto | alto | alto | medio |
| Atlassian MCP | alto | medio | medio | baixo |
| Azure DevOps MCP | alto | medio | medio | baixo |
| Dependencia de `.claude/commands` | alto | parcial | parcial | baixo |
| Dependencia de skills externas (`review`, `bugfix`) | medio | medio | medio | baixo |

## Catalogo Operacional

### `azure-devops-epic-stories`

- Entradas minimas: `./discoveries/epic-<slug>/`, `organization`, `project`, `board`.
- Dependencias: Python 3, bundle valido de `epic-story-discovery`, MCP do Azure DevOps.
- Uso por agente: `Claude` alto; `Codex` e `Gemini` manuais com substituicao de naming MCP; `Copilot CLI` parcial. Ver `skills/azure-devops-epic-stories/references/multi-agent-usage.md`.

Prompt mandatorio:

```text
Use a skill azure-devops-epic-stories para publicar o bundle em ./discoveries/epic-onboarding-self-service/.
Organizacao: acme-co.
Projeto: Plataforma.
Board: Squad-Aquisicao.
Valide o bundle, detecte o processo do projeto, detecte duplicata de epico e faca dry-run antes de qualquer criacao.
```

Prompt eficiente:

```text
Siga skills/azure-devops-epic-stories/SKILL.md.
Publice o bundle ./discoveries/epic-onboarding-self-service/ no Azure DevOps usando organization=acme-co, project=Plataforma e board=Squad-Aquisicao.
Use .ado-epic-stories.yml se existir, valide com scripts/validate-bundle.py, detecte o child type correto do processo, cheque duplicata por titulo normalizado, limite a 10 US por lote e gere audit log.
Primeiro rode em dry-run; so crie se eu confirmar.
```

Prompt economico:

```text
Use azure-devops-epic-stories no bundle ./discoveries/epic-onboarding-self-service/ para acme-co/Plataforma/Squad-Aquisicao.
Valide, detecte processo e duplicata, e entregue dry-run com audit log.
```

### `confluence-changelog-publisher`

- Entradas minimas: conteudo final, `space`, `title`, `mode`.
- Dependencias: Python 3, Atlassian MCP.
- Uso por agente: `Claude` alto; `Codex` e `Gemini` medio se houver Atlassian MCP; `Copilot CLI` baixo.

Prompt mandatorio:

```text
Use a skill confluence-changelog-publisher.
Publique este changelog no Confluence com:
space=ENG
title=Release 2026.05 - API de Pagamentos
mode=create
location=root
Antes de consultar paginas e antes de escrever, peca minha aprovacao explicita.
```

Prompt eficiente:

```text
Siga skills/confluence-changelog-publisher/SKILL.md.
Padronize o texto com o template da skill apenas se necessario.
Destino: space=ENG, title=Release 2026.05 - API de Pagamentos, mode=decide-after-search, parent-title=Releases Backend.
Valide com scripts/validate-confluence-target.py, mostre preview curto, peca aprovacao antes da busca e depois antes da escrita.
```

Prompt economico:

```text
Use confluence-changelog-publisher para publicar este texto no space ENG com titulo Release 2026.05 - API de Pagamentos.
Mode=create. Peca aprovacao antes de buscar e antes de escrever.
```

### `epic-story-discovery`

- Entradas minimas: nome da feature ou slug, problema atual, objetivo, personas, restricoes.
- Dependencias: Python 3, escrita local no repositorio.
- Uso por agente: `Claude` alto; `Codex` e `Gemini` altos com perguntas em prosa quando necessario; `Copilot CLI` medio.

Prompt mandatorio:

```text
Use a skill epic-story-discovery para refinar a feature onboarding-self-service.
Contexto bruto:
- Problema: 35% dos novos clientes abandonam no passo de validacao documental.
- Objetivo: reduzir abandono sem aumentar fraude.
- Personas: cliente final e time de operacoes.
- Restricoes: rollout com feature flag e sem mudar o provedor de KYC agora.
Conduza no minimo duas rodadas de clarificacao, escreva tudo em PT-BR e so materialize o bundle quando a validacao passar.
```

Prompt eficiente:

```text
Siga skills/epic-story-discovery/SKILL.md.
Crie discovery para onboarding-self-service em PT-BR.
Use pelo menos duas rodadas obrigatorias: rodada 1 cobrindo objetivo, persona, escopo e KPI; rodada 2 cobrindo trade-offs, edge cases, dependencias e rollout.
Depois materialize ./discoveries/epic-onboarding-self-service/, preencha epic.md, us/, transcript.md e valide com scripts/validate-bundle.py.
```

Prompt economico:

```text
Use epic-story-discovery para a feature onboarding-self-service.
Problema: alto abandono na validacao documental.
Objetivo: reduzir abandono com rollout por feature flag.
Faca 2 rodadas obrigatorias, gere bundle em PT-BR e valide antes de encerrar.
```

### `github-diff-changelog-publisher`

- Entradas minimas: alvo do diff, repositorio e destino (`github`, `confluence` ou `draft-only`).
- Dependencias: Python 3, acesso ao GitHub por MCP, `gh` ou web; Atlassian MCP opcional.
- Uso por agente: `Claude` alto; `Codex` e `Gemini` altos; `Copilot CLI` medio se houver `gh`.

Prompt mandatorio:

```text
Use a skill github-diff-changelog-publisher.
Origem: release v2.4.0 do repositorio acme/payments-api.
Destino: draft-only.
Antes de buscar qualquer dado remoto, peca minha aprovacao.
```

Prompt eficiente:

```text
Siga skills/github-diff-changelog-publisher/SKILL.md.
Gere um changelog publicavel para a release v2.4.0 de acme/payments-api.
Priorize fonte nativa do GitHub, compare contra main com fallback para master, destaque breaking changes e qualidade da evidencia.
Quero preview em draft-only; se faltar acesso nativo, peca aprovacao antes de usar fallback web.
```

Prompt economico:

```text
Use github-diff-changelog-publisher para a release v2.4.0 de acme/payments-api.
Destino=draft-only. Peca aprovacao antes de acessar GitHub ou web.
```

### `github-pr-comment-triage`

- Entradas minimas: numero ou URL da PR, ou branch atual com `gh`.
- Dependencias: `gh` instalado e autenticado, Python 3.
- Uso por agente: `Claude`, `Codex` e `Gemini` altos; `Copilot CLI` medio.

Prompt mandatorio:

```text
Use a skill github-pr-comment-triage para analisar a PR 128 de acme/payments-api.
Modo inicial: analyze-only.
Nao publique comentarios e nao altere codigo sem minha aprovacao por item.
```

Prompt eficiente:

```text
Siga skills/github-pr-comment-triage/SKILL.md.
Colete issue comments e review comments da PR 128 em acme/payments-api, normalize com scripts/normalize_pr_comments.py e gere a fila de decisao em PT-BR.
Classifique cada item, resuma sem copiar o comentario inteiro e me entregue a fila para eu responder com approve, reject ou skip.
Se eu aprovar um item, aplique a menor mudanca local necessaria, valide e rascunhe a resposta com scripts/render_pr_reply.py antes de qualquer publicacao remota.
```

Prompt economico:

```text
Use github-pr-comment-triage na PR 128 de acme/payments-api.
Analise somente, normalize comentarios e monte fila approve/reject/skip sem publicar nada.
```

### `github-release-publication-flow`

- Entradas minimas: origem do GitHub e destino final.
- Dependencias: Python 3, acesso ao GitHub; Atlassian MCP quando destino for Confluence.
- Uso por agente: `Claude` alto; `Codex` e `Gemini` altos; `Copilot CLI` medio.

Prompt mandatorio:

```text
Use a skill github-release-publication-flow.
Origem: compare entre release/2.4 e main em acme/payments-api.
Destino: draft-only.
Peca minha aprovacao antes da analise remota e antes de qualquer publicacao.
```

Prompt eficiente:

```text
Siga skills/github-release-publication-flow/SKILL.md.
Conduza o fluxo completo para o compare release/2.4...main de acme/payments-api.
Valide target e destination, gere o changelog usando a skill github-diff-changelog-publisher, mostre preview, revise comigo e pare em draft-only.
Se eu trocar o destino para confluence, reaproveite a skill confluence-changelog-publisher e mantenha as duas aprovacoes obrigatorias.
```

Prompt economico:

```text
Use github-release-publication-flow para o compare release/2.4...main de acme/payments-api.
Destino=draft-only. Analise so com aprovacao previa.
```

### `jira-tasks`

- Entradas minimas: issue key da US e bundle local `./tasks/prd-<feature>/`.
- Dependencias: Python 3, Jira/Atlassian MCP.
- Uso por agente: `Claude` alto; `Codex` e `Gemini` medio; `Copilot CLI` baixo.

Prompt mandatorio:

```text
Use a skill jira-tasks para criar tasks filhas da US PAY-142.
Bundle local: ./tasks/prd-checkout/.
Valide o bundle antes de criar e pare se algum campo obrigatorio nao puder ser inferido com seguranca.
```

Prompt eficiente:

```text
Siga skills/jira-tasks/SKILL.md.
Crie tasks filhas da US PAY-142 a partir de ./tasks/prd-checkout/.
Use tasks.md como indice, os arquivos [num]_task.md como fonte de verdade, valide com scripts/validate-task-bundle.py, descubra o tipo de subtask correto, resolva assignee e campos obrigatorios antes do create, estime horas pelas regras da skill e entregue rastreabilidade por task criada.
```

Prompt economico:

```text
Use jira-tasks para publicar ./tasks/prd-checkout/ abaixo da US PAY-142.
Valide o bundle e so crie tasks com parent, assignee, estimativa e campos obrigatorios completos.
```

### `otel-grafana-dashboards`

- Entradas minimas: raiz de um projeto Go com OpenTelemetry.
- Dependencias: Python 3, codebase Go com instrumentacao OTel.
- Uso por agente: `Claude`, `Codex` e `Gemini` altos; `Copilot CLI` medio.

Prompt mandatorio:

```text
Use a skill otel-grafana-dashboards na raiz deste projeto Go.
Descubra a instrumentacao OpenTelemetry e gere dashboards Grafana importaveis.
Valide todos os JSONs antes de encerrar.
```

Prompt eficiente:

```text
Siga skills/otel-grafana-dashboards/SKILL.md.
Analise esta codebase Go instrumentada com OpenTelemetry e gere:
- observability/dashboards/*.json
- observability/docker-compose.observability.yml
- observability/provisioning/
Cubra metricas, traces e logs para ambiente local otel-lgtm e producao Coralogix, usando apenas queries portaveis e validando cada dashboard com scripts/validate-dashboard.py.
```

Prompt economico:

```text
Use otel-grafana-dashboards neste projeto Go.
Descubra metricas OTel, gere dashboards em observability/ e valide os JSONs.
```

### `otel-hybrid-dashboard-blueprint`

- Entradas minimas: nome do servico e formulario de contexto do Passo 1.
- Dependencias: Python 3, contexto de observabilidade do servico.
- Uso por agente: `Claude` alto; `Codex` e `Gemini` altos com coleta manual do formulario; `Copilot CLI` medio.

Prompt mandatorio:

```text
Use a skill otel-hybrid-dashboard-blueprint.
Antes de gerar qualquer saida, apresente exatamente o formulario do Passo 1 e aguarde minhas respostas.
Nao tente converter JSON Grafana diretamente para Coralogix.
```

Prompt eficiente:

```text
Siga skills/otel-hybrid-dashboard-blueprint/SKILL.md.
Contexto ja preenchido:
- service_name=payments-api
- tipo=API REST
- ambientes=dev,staging,prod
- regioes=sa-east-1,us-east-1
- volume=medio
- SLO disponibilidade=99.9
- SLO latencia P95=<300ms
- dependencias=banco relacional,redis,API upstream
- endpoints criticos=POST /payments,POST /refunds,GET /payments/:id
Gere o blueprint hibrido com estrutura identica entre Grafana e Coralogix, PromQL portavel, duas versoes de logs e traces, alertas explicitos e validacao do JSON Grafana.
```

Prompt economico:

```text
Use otel-hybrid-dashboard-blueprint para payments-api.
Se faltarem campos obrigatorios, reapresente o formulario do Passo 1.
Depois gere blueprint Grafana + Coralogix sem conversao direta entre plataformas.
```

### `postman-collection-generator`

- Entradas minimas: raiz do projeto HTTP suportado em Go, C# ou TypeScript.
- Dependencias: Bash, Python 3.
- Uso por agente: `Claude`, `Codex` e `Gemini` altos; `Copilot CLI` medio.

Prompt mandatorio:

```text
Use a skill postman-collection-generator na raiz deste projeto.
Detecte a linguagem suportada, descubra todas as rotas HTTP e gere postman-collection.json validado.
```

Prompt eficiente:

```text
Siga skills/postman-collection-generator/SKILL.md.
Analise esta API, detecte a linguagem com scripts/detect-language.sh, descubra rotas, handlers, DTOs, regras de validacao, auth e base_url, e gere postman-collection.json com cenarios de sucesso, validacao, not found e unauthorized.
Valide a saida com scripts/validate-collection.py e reporte quantidade de folders, requests e cenarios.
```

Prompt economico:

```text
Use postman-collection-generator neste projeto.
Descubra rotas HTTP, gere postman-collection.json e valide o arquivo final.
```

### `prompt-enricher`

- Entradas minimas: prompt bruto e objetivo de otimizacao.
- Dependencias: Python 3.
- Uso por agente: `Claude`, `Codex` e `Gemini` altos; `Copilot CLI` medio.

Prompt mandatorio:

```text
Use a skill prompt-enricher para reescrever este prompt bruto.
Modo principal: execution.
Pressao principal: economy.
Retorne o prompt enriquecido e uma justificativa curta.
Prompt bruto:
<cole aqui o prompt original>
```

Prompt eficiente:

```text
Siga skills/prompt-enricher/SKILL.md.
Reescreva o prompt abaixo para um agente de codigo.
Modo=execution.
Pressao=robustness.
Restricoes obrigatorias: nao inventar fatos, pedir esclarecimento so se faltar dado critico, limitar resposta a 10 bullets.
Valide a estrutura com scripts/validate-prompt.py se isso ajudar.
Prompt bruto:
<cole aqui o prompt original>
```

Prompt economico:

```text
Use prompt-enricher neste prompt bruto com pressao=economy.
Preserve so objetivo, restricoes rigidas e contrato de saida.
```

### `pull-request`

- Entradas minimas: branch atual valida e modo (`draft-only`, `create`, `update`, `create-or-update`).
- Dependencias: Git; `gh` autenticado se houver escrita remota; Python 3.
- Uso por agente: `Claude`, `Codex` e `Gemini` altos; `Copilot CLI` medio.

Prompt mandatorio:

```text
Use a skill pull-request para gerar um rascunho de PR em PT-BR a partir da branch atual.
Modo: draft-only.
Nao faca git push nem escrita remota.
```

Prompt eficiente:

```text
Siga skills/pull-request/SKILL.md.
Use a branch atual para gerar titulo e body de PR em PT-BR.
Resolva a base com scripts/resolve_pr_base.py, valide com evidencia do repositorio, colete commits e diff, nao invente testes nem contexto e entregue em modo draft-only.
Se a branch estiver larga demais para uma PR coesa, aponte isso explicitamente.
```

Prompt economico:

```text
Use pull-request na branch atual em modo draft-only.
Resolva base, leia commits e diff, e entregue titulo + body objetivos em PT-BR.
```

### `recursive-review-bugfix`

- Entradas minimas: caminho da pasta de PRD/TechSpec/tasks.
- Dependencias: skills `review` e `bugfix` disponiveis no ambiente.
- Uso por agente: `Claude`, `Codex` e `Gemini` medios; `Copilot CLI` baixo. Sem `review` e `bugfix`, a skill fica bloqueada.

Prompt mandatorio:

```text
Use a skill recursive-review-bugfix.
Antes de qualquer outra etapa, peca o caminho da pasta com PRD, TechSpec e tasks.
Nao assuma stack, riscos ou comandos fora do que estiver nos artefatos.
```

Prompt eficiente:

```text
Siga skills/recursive-review-bugfix/SKILL.md.
Analise recursivamente a pasta ./docs/specs/payments-refund/.
Extraia RFs, criterios de aceite, invariantes e comandos de validacao apenas dos artefatos dessa pasta.
Depois acione review e bugfix com os templates da skill, repetindo o ciclo ate veredito aprovado ou ate duas iteracoes sem convergencia.
Recuse achados sem evidencia em codigo e sem referencia ao artefato fonte.
```

Prompt economico:

```text
Use recursive-review-bugfix em ./docs/specs/payments-refund/.
Extraia contexto dos artefatos e rode o ciclo review/bugfix ate aprovado ou bloqueio por falta das skills dependentes.
```

### `semantic-commit`

- Entradas minimas: diff staged, diff unstaged ou descricao objetiva das mudancas.
- Dependencias: Git, Python 3.
- Uso por agente: `Claude`, `Codex` e `Gemini` altos; `Copilot CLI` medio.

Prompt mandatorio:

```text
Use a skill semantic-commit para sugerir uma mensagem de commit para as mudancas atuais.
Priorize git diff --staged; se estiver vazio, use git diff.
Entregue em Conventional Commits com cabecalho em ingles e descricao em PT-BR.
```

Prompt eficiente:

```text
Siga skills/semantic-commit/SKILL.md.
Classifique o diff atual, determine a intencao dominante, sugira scope so se houver centro claro e recomende split em multiplos commits se o conjunto misturar objetivos independentes.
Valide o cabecalho final com scripts/validate-commit-header.py.
```

Prompt economico:

```text
Use semantic-commit no diff atual.
Infera tipo pelo diff, sugira mensagem final e aponte se precisa split.
```

### `tracker-to-prd`

- Entradas minimas: identificador de US ou epico — `PROJ-123` (Jira) ou URL/triplo `org/project/id` (Azure DevOps).
- Dependencias: Python 3, MCP Atlassian ou MCP azure-devops conforme o backend, `gh` quando o codebase a confrontar for repo remoto.
- Uso por agente: `Claude` alto; `Codex` e `Gemini` parciais (dependem de paridade nos nomes MCP); `Copilot CLI` baixo.
- Saida: bundle em `.specs/prd-<slug>/context.md` mais `clarifications.md` append-only. A skill nao invoca `create-prd` automaticamente; instrui o handoff explicito ao final.

Prompt mandatorio:

```text
Use a skill tracker-to-prd para a issue PAY-142 (ou para o work item https://dev.azure.com/<org>/<proj>/_workitems/edit/4567).
Leia description, comments, subtasks e links relevantes, confronte os requisitos com o codebase informado e conduza rodadas de clarificacao ate cobrir as seis categorias do create-prd.
Ao final, materialize o bundle em .specs/prd-<slug>/context.md e instrua o handoff para create-prd.
```

Prompt eficiente:

```text
Siga skills/tracker-to-prd/SKILL.md.
Detecte o backend pelo input, leia a US/epico completo, confronte os requisitos com o codebase (caminho local ou owner/repo no GitHub) respeitando o cap de 15 buscas por rodada, conduza clarificacao ate as 6 categorias estarem respondidas e nenhum conflito aberto, grave o bundle e exiba a instrucao literal para create-prd.
```

Prompt economico:

```text
Use tracker-to-prd para PAY-142, confronto pulado.
Materialize o bundle minimo viavel e instrua a invocar create-prd em seguida.
```

### `tech-debt-register`

- Entradas minimas: descricao livre do debito em PT-BR.
- Dependencias: Python 3 para `slugify.py`; `gh` apenas quando confrontar repo remoto. Sem MCP externo.
- Uso por agente: `Claude` alto; `Codex`, `Gemini` e `Copilot CLI` viaveis desde que ofereçam equivalente a `AskUserQuestion` ou aceitem perguntas iterativas em texto.
- Saida: `.specs/tech-debt-<slug>/debt.md` (12 secoes) e `.specs/tech-debt-<slug>/clarifications.md` append-only.

Prompt mandatorio:

```text
Use a skill tech-debt-register para o debito: "preciso criar autenticacao na minha API".
Confronte com o path local internal/ e conduza clarificacao ate os oito eixos estarem respondidos.
Materialize o debt.md em .specs/tech-debt-<slug>/ com problema, localizacao, severidade x urgencia, estrategia, esforco e plano de acao.
```

Prompt eficiente:

```text
Siga skills/tech-debt-register/SKILL.md.
Identifique a natureza pela debt-taxonomy, derive 2-4 termos buscaveis, confronte com Grep ou gh respeitando o cap de 15 buscas por rodada, conduza no maximo 4 perguntas por chamada ate os 8 eixos estarem fechados e nenhum candidato em conflicting, e materialize debt.md + clarifications.md.
```

Prompt economico:

```text
Use tech-debt-register para o debito X. Confronte com cwd, conduza apenas as perguntas estritamente necessarias, materialize debt.md minimo viavel.
```

## Excecoes e Cuidados

- `azure-devops-epic-stories`: ja possui referencia explicita de naming MCP multi-agente. Use-a como padrao para adaptar outras skills com MCP.
- `confluence-changelog-publisher` e `jira-tasks`: dependem de integracao Atlassian real; sem isso, a skill deve parar em vez de inventar respostas.
- `tracker-to-prd`: depende de MCP Atlassian ou MCP azure-devops conforme o backend detectado; sem o MCP correspondente, encerra com `blocked`.
- `github-pr-comment-triage` e `pull-request`: exigem `gh` instalado e autenticado para escrita remota.
- `recursive-review-bugfix`: depende de duas skills externas que este repo nao define.
- `tracker-to-prd`: nao invoca `create-prd` automaticamente. Materializa o bundle e instrui o usuario a executar `create-prd` no orchestrator em seguida — quem chamar a skill precisa garantir a presenca do `create-prd` upstream.
- `tech-debt-register`: independente de MCP externo. Funciona offline desde que `Grep`/`Read` ou `gh` estejam disponiveis. Nao auto-invoca skill de tracker; cabe ao usuario decidir o destino.
- `Copilot CLI`: trate como executor manual. O repositorio nao documenta equivalentes nativos para MCP, `AskUserQuestion` ou auto-discovery de skill.

## Escolha Rapida

- Use `prompt-enricher` quando o problema principal for qualidade do prompt.
- Use `semantic-commit` e `pull-request` para camada Git local.
- Use `github-pr-comment-triage` quando a revisao ja esta publicada.
- Use `epic-story-discovery` antes de `azure-devops-epic-stories`.
- Use `jira-tasks` depois que a decomposicao local ja existir.
- Use `tracker-to-prd` quando a origem da verdade estiver no Jira ou no Azure DevOps e o destino for PRD.
- Use `tech-debt-register` quando precisar documentar debito tecnico com confronto de codebase e clarificacao iterativa antes de levar ao tracker ou ao planejamento.
- Use `otel-grafana-dashboards` para gerar artefatos Grafana prontos.
- Use `otel-hybrid-dashboard-blueprint` para desenhar estrutura portavel entre Grafana e Coralogix.
