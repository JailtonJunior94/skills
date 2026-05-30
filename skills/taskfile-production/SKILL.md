---
name: taskfile-production
description: Configura e operacionaliza o Taskfile (go-task) de forma robusta e production-ready em projetos novos e existentes, padronizando tarefas de build, geracao de mocks, testes unitarios, testes de integracao, lint, verificacao de vulnerabilidades (vulncheck) e automacao em esteiras CI/CD. Cobre instalacao multiplataforma em macOS, Windows e Linux (Ubuntu), fixacao da ultima versao estavel, validacao de Taskfile.yml e receitas para GitHub Actions, GitLab CI e Azure Pipelines. Use quando o pedido envolver criar, padronizar, revisar ou versionar Taskfile, migrar de Makefile ou scripts, ou integrar Task na pipeline. Nao use para escrever a logica de negocio da aplicacao, configurar ferramentas de build sem Task, ou gerenciar pipelines que nao usam Taskfile.
---

# Taskfile Production-Ready

<critical>Todos os artefatos e mensagens DEVEM ser escritos em PT-BR.</critical>
<critical>A automacao do Task DEVE ficar isolada do codigo-fonte: o `Taskfile.yml` da raiz atua como orquestrador fino e toda a logica vai para `taskfiles/` (Taskfiles incluidos por dominio) e `taskfiles/scripts/` (scripts auxiliares). NUNCA misturar scripts de automacao com diretorios de codigo da aplicacao (`internal/`, `src/`, `app/`, `pkg/`, `cmd/`).</critical>
<critical>SEMPRE fixar a ultima versao estavel do Task. A versao de referencia desta skill e `v3.51.1`. Antes de gerar artefatos, confirmar a ultima estavel com `python3 scripts/check-task-version.py --latest`.</critical>
<critical>Todo Taskfile gerado DEVE declarar `version: '3'`, o comentario de schema `# yaml-language-server: $schema=https://taskfile.dev/schema.json` e ter `.task/` no `.gitignore`.</critical>
<critical>O Taskfile so e considerado pronto quando `python3 scripts/validate-taskfile.py <caminho>` retornar `SUCCESS`.</critical>
<critical>Seguir o styleguide oficial (https://taskfile.dev/styleguide): ordem de secoes `version` → `includes` → configs → `vars` → `env` → `tasks`, 2 espacos de indentacao, linha em branco entre secoes e entre tarefas, variaveis em MAIUSCULO, tarefas em kebab-case com `:` para namespace, interpolacao sem espacos (`{{.VAR}}`). Arquivos incluidos em minusculo kebab-case; a raiz permanece `Taskfile.yml`.</critical>
<critical>O comportamento DEVE ser identico em macOS, Windows e Linux (Ubuntu) e agnostico de agente (Claude Code, Codex CLI e outros seguem os mesmos passos, gates e saidas).</critical>

## Entrada Obrigatoria
- Projeto alvo: novo ou existente, e o caminho da raiz.
- Stack principal (Go, Node, Python, etc.) e gerenciador de dependencias.

## Entrada Recomendavel
- Ferramentas ja adotadas: linter, mock generator, scanner de vulnerabilidades, runner de testes.
- Plataforma de CI/CD em uso (GitHub Actions, GitLab CI, Azure Pipelines).
- Convencoes de diretorio existentes e arquivos de automacao legados (Makefile, shell scripts).

## Saida
- `Taskfile.yml` na raiz (orquestrador fino, somente `version`, `includes`, `vars` e `tasks` de alto nivel).
- `taskfiles/` com Taskfiles por dominio: `build.yml`, `test.yml`, `lint.yml`, `security.yml`, `mocks.yml`, `ci.yml`.
- `taskfiles/scripts/` com scripts auxiliares isolados do codigo-fonte.
- `.taskrc.yml` com configuracao de execucao.
- `.env.example` documentando variaveis necessarias.
- Workflow de CI/CD pinando a versao do Task.
- Bloco de `.gitignore` com `.task/`.

## Layout Isolado (obrigatorio)
```
.
├── Taskfile.yml            # orquestrador fino (nome canonico do Task)
├── .taskrc.yml             # config de execucao
├── .env.example            # contrato de variaveis
├── taskfiles/              # automacao isolada do codigo-fonte
│   ├── build.yml
│   ├── test.yml
│   ├── lint.yml
│   ├── security.yml
│   ├── mocks.yml
│   ├── ci.yml
│   └── scripts/            # scripts auxiliares (sh/ps1/py)
│       └── wait-for.sh
├── cmd/ internal/ src/ ... # codigo-fonte: NUNCA recebe scripts de automacao
└── .task/                  # cache do Task (gitignored)
```

## Procedimentos

**Step 1: Confirmar versao e instalacao do Task**
1. Executar `python3 scripts/check-task-version.py --latest` para descobrir a ultima estavel publicada.
2. Executar `python3 scripts/check-task-version.py --installed` para detectar a versao local (ou ausencia).
3. Se o Task nao estiver instalado ou estiver desatualizado, orientar a instalacao com o gerenciador nativo da plataforma. Ler `references/cross-platform.md` para os comandos exatos por SO. Para automacao reproduzivel, usar `scripts/install-task.sh <versao>`.
4. Registrar a versao pinada (`TASK_VERSION`) para uso identico em local e CI/CD.

**Step 2: Mapear o projeto e a stack**
1. Inspecionar a raiz para identificar a stack, o gerenciador de dependencias e ferramentas ja presentes (linter, mocks, scanner, runner de testes).
2. Em projeto existente, localizar automacao legada (Makefile, scripts soltos) para migrar comandos para tarefas equivalentes do Task.
3. Confirmar que nenhum script de automacao novo sera colocado dentro de diretorios de codigo-fonte. Todo helper vai para `taskfiles/scripts/`.

**Step 3: Gerar a estrutura isolada de Taskfiles**
1. Copiar `assets/Taskfile.yml` para a raiz como orquestrador fino (apenas `includes`, `vars` globais e atalhos de alto nivel como `default`, `ci`, `check`).
2. Criar o diretorio `taskfiles/` e copiar os Taskfiles por dominio a partir de `assets/`. Use nomes de arquivo em minusculo kebab-case (padrao recomendado); o `Taskfile.yml` da raiz mantem o nome canonico que o Task procura:
   - `assets/build.yml` → `taskfiles/build.yml` (build multiplataforma com `exeExt`, `sources`/`generates`).
   - `assets/test.yml` → `taskfiles/test.yml` (unit e integration separados, com `dotenv` e `preconditions`).
   - `assets/lint.yml` → `taskfiles/lint.yml` (lint e format).
   - `assets/security.yml` → `taskfiles/security.yml` (vulncheck e auditoria de dependencias).
   - `assets/mocks.yml` → `taskfiles/mocks.yml` (geracao de mocks com fingerprint de `sources`).
   - `assets/ci.yml` → `taskfiles/ci.yml` (pipeline agregada para a esteira).
3. Copiar scripts auxiliares de `assets/wait-for.sh` para `taskfiles/scripts/` e marca-los como executaveis.
4. Adaptar comandos de cada dominio para a stack real. Ler `references/taskfile-reference.md` para a sintaxe correta de cada chave (`includes`, `requires`, `sources`, `status`, `preconditions`, `platforms`, `dotenv`).
5. Para diferencas de SO (shell, extensoes de binario, paths), ler `references/cross-platform.md` e aplicar `platforms:`, `{{OS}}`, `{{exeExt}}`.

**Step 4: Configurar variaveis, ambiente e cache**
1. Copiar `assets/taskrc.yml` para `.taskrc.yml` na raiz.
2. Copiar `assets/env.example` para `.env.example` e documentar cada variavel exigida pelas tarefas.
3. Declarar variaveis sensiveis via `dotenv`/`env` e proteger tarefas perigosas com `requires.vars`.
4. Garantir `.task/` no `.gitignore` usando o trecho de `assets/gitignore-snippet.txt`.

**Step 5: Integrar na esteira CI/CD**
1. Identificar a plataforma de CI/CD alvo.
2. Ler `references/ci-cd-recipes.md` e copiar a receita correspondente (GitHub Actions, GitLab CI ou Azure Pipelines), sempre pinando `TASK_VERSION`.
3. Mapear os jobs para tarefas existentes (`task ci`, `task lint`, `task test:unit`, `task test:integration`, `task security:vulncheck`), evitando duplicar comandos no YAML do CI.
4. Garantir cache de `.task/` e do cache de dependencias da stack quando suportado.

**Step 6: Validar e verificar**
1. Executar `python3 scripts/validate-taskfile.py Taskfile.yml` e corrigir ate retornar `SUCCESS`.
2. Executar `task --list-all` para confirmar que todas as tarefas resolvem sem erro de include.
3. Executar localmente o caminho critico (`task check` ou `task ci`) para validar o comportamento de ponta a ponta.
4. Confirmar que nenhum script de automacao foi gravado em diretorio de codigo-fonte.

## Error Handling
* Se `scripts/check-task-version.py --latest` falhar por ausencia de rede, usar a versao de referencia `v3.51.1` e registrar que a checagem online ficou pendente.
* Se `scripts/validate-taskfile.py` retornar erro, ler a mensagem de `stderr`, corrigir a chave/secao indicada e revalidar ate `SUCCESS`.
* Se `task --list-all` acusar include ausente, conferir caminhos relativos em `includes` (resolvidos a partir do diretorio do Taskfile que inclui) e a existencia dos arquivos em `taskfiles/`.
* Se uma tarefa falhar apenas em Windows, revisar shell e quoting em `references/cross-platform.md` e isolar o comando com `platforms:` ou um script equivalente em `taskfiles/scripts/`.
* Se houver conflito com automacao legada (Makefile), manter o Makefile apenas como camada fina que chama `task`, evitando logica duplicada.
