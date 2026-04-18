# Agent Skills

Colecao open source de skills reutilizaveis para agentes de IA focados em fluxo real de engenharia de software.

Este repositorio organiza instrucoes operacionais em formato `SKILL.md` para que agentes consigam executar tarefas com mais consistencia, menos ambiguidade e melhor rastreabilidade. Em vez de depender apenas de prompts livres, cada skill encapsula objetivo, quando usar, quando nao usar, passos obrigatorios, regras de decisao e, quando necessario, arquivos de apoio como `assets/`, `references/` e `scripts/`.

Repositorio: `https://github.com/JailtonJunior94/skills`

## Sumario

- [Por que este projeto existe](#por-que-este-projeto-existe)
- [Para quem este repositorio e util](#para-quem-este-repositorio-e-util)
- [O que voce encontra aqui](#o-que-voce-encontra-aqui)
- [Skills disponiveis](#skills-disponiveis)
- [Como instalar](#como-instalar)
- [Como usar](#como-usar)
- [Exemplos por perfil de usuario](#exemplos-por-perfil-de-usuario)
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

## Skills disponiveis

| Skill | O que faz | Casos de uso tipicos |
| --- | --- | --- |
| `confluence-changelog-publisher` | Publica changelogs e resumos tecnicos no Confluence com confirmacoes obrigatorias. | Release notes, resumo tecnico de mudancas, publicacao controlada em wiki. |
| `github-diff-changelog-publisher` | Gera changelog a partir de diff de release, PR, branch ou compare no GitHub. | Release notes baseadas em evidencias, resumos de PR, analise de impacto. |
| `github-pr-comment-triage` | Coleta e classifica comentarios de PR no GitHub, propondo fila de decisao. | Triagem de review comments, organizacao de feedback, resposta rastreavel. |
| `github-release-publication-flow` | Orquestra leitura de diffs, geracao de changelog e publicacao aprovada. | Fluxo completo de release notes do GitHub ate GitHub ou Confluence. |
| `jira-tasks` | Cria tasks no Jira a partir de bundles locais de decomposicao. | Publicar decomposicao tecnica, sincronizar `tasks.md` com Jira. |
| `otel-grafana-dashboards` | Gera dashboards Grafana prontos para producao a partir de codebases Go com OpenTelemetry. | Observabilidade, painis para metricas, traces e logs. |
| `postman-collection-generator` | Monta collections Postman a partir da analise do codigo da API. | Documentacao de endpoints, testes exploratorios, onboarding de APIs. |
| `prompt-enricher` | Reescreve prompts brutos em prompts mais robustos, compactos e operacionais. | Melhorar prompts para chatbots, agentes e automacoes. |
| `pull-request` | Gera, revisa, cria ou atualiza PRs com base no diff e no contexto do repositorio. | Rascunho de PR, revisao de titulo e body, publicacao via GitHub. |
| `semantic-commit` | Sugere mensagens de commit semantico em pt-BR com Conventional Commits. | Commits mais consistentes, escolha de tipo e scope. |
| `us-to-prd` | Le uma User Story no Jira e prepara contexto consolidado para PRD. | Transformar US em insumo estruturado para PRD. |

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
- ferramentas externas especificas em alguns casos, como `gh`, integracoes com Jira/Confluence ou MCPs correspondentes.

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

## Estrutura do repositorio

Estrutura atual, em alto nivel:

```text
skills/
├── confluence-changelog-publisher/
├── github-diff-changelog-publisher/
├── github-pr-comment-triage/
├── github-release-publication-flow/
├── jira-tasks/
├── otel-grafana-dashboards/
├── postman-collection-generator/
├── prompt-enricher/
├── pull-request/
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
- Algumas skills dependem de ferramentas externas como `gh`, Jira, Confluence, MCPs ou scripts Python locais.
- Nem toda skill e universalmente portavel sem ajustes de integracao.
- O README documenta a estrutura e o uso pretendido do repositorio; a compatibilidade exata depende do agente, do ambiente e das integracoes disponiveis.

## Licenca

No momento, este repositorio nao possui um arquivo `LICENSE` versionado na raiz. Se voce pretende reutilizar este conteudo em ambiente aberto ou comercial, o ideal e adicionar uma licenca explicita antes da redistribuicao formal.
