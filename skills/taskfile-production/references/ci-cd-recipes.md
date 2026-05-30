# Receitas de CI/CD com Task

Princípios:
- Pinar `TASK_VERSION` (mesma versao do desenvolvimento local).
- Reaproveitar as tarefas do Taskfile; nao duplicar comandos no YAML do CI.
- Cachear `.task/` e o cache da stack (ex.: modulos Go) quando suportado.

Versao de referencia: `v3.51.1`.

## GitHub Actions

```yaml
name: ci
on:
  push:
    branches: [main]
  pull_request:

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-go@v5
        with:
          go-version: stable
          cache: true

      - name: Instalar Task
        uses: arduino/setup-task@v2
        with:
          version: 3.51.1
          repo-token: ${{ secrets.GITHUB_TOKEN }}

      - name: Cache do Task
        uses: actions/cache@v4
        with:
          path: .task
          key: task-${{ runner.os }}-${{ hashFiles('**/go.sum') }}

      - name: Pipeline
        run: task ci
```

Matriz multiplataforma (macOS, Windows, Ubuntu):

```yaml
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with: { go-version: stable }
      - uses: arduino/setup-task@v2
        with: { version: 3.51.1, repo-token: '${{ secrets.GITHUB_TOKEN }}' }
      - run: task test:unit
```

## GitLab CI

```yaml
stages: [quality]

variables:
  TASK_VERSION: "v3.51.1"

ci:
  stage: quality
  image: golang:1.23
  cache:
    key: "$CI_COMMIT_REF_SLUG"
    paths:
      - .task/
      - .cache/go-build/
  before_script:
    - sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b /usr/local/bin "$TASK_VERSION"
    - task --version
  script:
    - task ci
```

## Azure Pipelines

```yaml
trigger:
  branches: { include: [main] }

pool:
  vmImage: ubuntu-latest

variables:
  TASK_VERSION: v3.51.1

steps:
  - task: GoTool@0
    inputs: { version: '1.23' }

  - script: sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b "$(Build.BinariesDirectory)" $(TASK_VERSION)
    displayName: Instalar Task

  - script: |
      export PATH="$(Build.BinariesDirectory):$PATH"
      task ci
    displayName: Pipeline
```

## Mapeamento de jobs para tarefas
- Lint: `task lint:run`
- Format gate: `task lint:fmt:check`
- Mocks atualizados: `task mocks:verify`
- Testes unitarios: `task test:unit`
- Testes de integracao: `task test:integration`
- Vulnerabilidades: `task security:vulncheck`
- Build: `task build:build`
- Tudo: `task ci`

## Dicas
- Use `task --status build:build` para falhar cedo se algo deveria estar gerado.
- Em PRs, rode `task ci:fast` (lint + unit) e reserve a pipeline completa para a main.
- Evite logica condicional no YAML do CI; mova para `if:`/`preconditions:` nas tarefas.
