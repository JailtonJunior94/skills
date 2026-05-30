# Referencia de Taskfile (go-task) para uso production-ready

Versao de schema: `version: '3'`. Versao estavel de referencia: `v3.51.1`.
Comentario de schema obrigatorio no topo de cada arquivo:

```yaml
# yaml-language-server: $schema=https://taskfile.dev/schema.json
version: '3'
```

## Chaves de tarefa essenciais

| Chave | Uso |
| --- | --- |
| `desc` | Descricao curta exibida em `task --list`. |
| `cmds` | Lista de comandos. Cada item pode ser string ou `{ cmd, platforms, if, ignore_error }`. |
| `deps` | Dependencias executadas em paralelo antes da tarefa. |
| `dir` | Diretorio de execucao. Usar `{{.USER_WORKING_DIR}}` em monorepos. |
| `sources` / `generates` | Fingerprint para pular tarefa quando nada mudou. Aceita globs e `exclude:`. |
| `method` | `checksum` (default), `timestamp` ou `none`. |
| `status` | Comandos que, se retornarem 0, marcam a tarefa como up-to-date. |
| `preconditions` | Comandos que DEVEM retornar 0; com `msg` para feedback. Falham a tarefa. |
| `if` | Pula a tarefa/comando quando a condicao falha (nao falha a pipeline). |
| `requires.vars` | Exige variaveis setadas; suporta `enum` para valores validos. |
| `platforms` | Restringe a tarefa/comando a `GOOS`/`GOARCH` (ex.: `[windows/amd64, darwin]`). |
| `env` / `dotenv` | Variaveis de ambiente; `dotenv` carrega arquivos `.env`. |
| `internal: true` | Esconde a tarefa de `--list` (uso apenas interno). |
| `run` | `always` (default), `once` ou `when_changed`. |
| `watch: true` + `sources` | Reexecuta ao alterar arquivos (`task <tarefa> --watch`). |
| `vars` | Variaveis locais; `{{.VAR | default "x"}}` para tornar sobrescrevivel. |
| `aliases` | Nomes alternativos para a tarefa. |

## Includes e isolamento

```yaml
includes:
  build:
    taskfile: ./taskfiles/build.yml   # caminho relativo ao Taskfile que inclui
  ci:
    taskfile: ./taskfiles/ci.yml
    internal: true                     # esconde o namespace
```

- Tarefas incluidas ganham namespace: `task build:build`.
- Para chamar uma tarefa do Taskfile raiz a partir de um incluido, usar prefixo `:`: `task: :lint:run`.
- `optional: true` evita erro quando o arquivo incluido nao existe.
- `flatten: true` remove o namespace (cuidado com colisao de nomes).
- `vars:` no include parametriza o mesmo Taskfile reutilizado varias vezes.
- Variaveis declaradas no Taskfile incluido tem precedencia; use `default` para permitir override.

## Variaveis e precedencia (mais forte primeiro)
1. Variaveis na definicao da tarefa.
2. Variaveis passadas ao chamar outra tarefa (`vars:`).
3. Variaveis do Taskfile incluido.
4. Variaveis da inclusao (`includes.*.vars`).
5. Variaveis globais (`vars:`).
6. Variaveis de ambiente.

Tipos suportados: `string`, `bool`, `int`, `float`, `array`, `map` (use subchave `map:`).
Variavel dinamica via shell: `VERSION: { sh: git describe --tags --always }`.

## Funcoes de template uteis
- `{{OS}}` e `{{ARCH}}`: sistema e arquitetura.
- `{{exeExt}}`: `.exe` no Windows, vazio nos demais.
- `{{.USER_WORKING_DIR}}`: diretorio de onde o `task` foi chamado.
- `{{.TASK}}`: nome da tarefa atual.
- `{{.CHECKSUM}}` / `{{.TIMESTAMP}}`: fingerprint das `sources`.
- Funcoes Sprig (https://sprig.taskfile.dev): `default`, `splitLines`, `fromJson`, etc.

## Loops com `for`
```yaml
cmds:
  - for: { matrix: { GOOS: [linux, darwin], GOARCH: [amd64, arm64] } }
    cmd: GOOS={{.ITEM.GOOS}} GOARCH={{.ITEM.GOARCH}} go build ./...
  - for: ['a', 'b', 'c']
    cmd: echo {{.ITEM}}
```

## CLI relevante
- `task --list` / `--list-all`: lista tarefas.
- `task --status <t>`: exit != 0 se desatualizada (uso em CI).
- `task --force` / `-f`: ignora fingerprint.
- `task --parallel <a> <b>`: roda em paralelo.
- `task --dry`: mostra os comandos sem executar.
- `task -t -`: le Taskfile do stdin.
- `task -g`: usa o Taskfile global em `$HOME`.

## Styleguide oficial (semantica recomendada do .yml)
Ref: https://taskfile.dev/styleguide
- Ordem das secoes: `version` → `includes` → configs opcionais (`silent`, `output`, `method`, `run`) → `vars` → `env`/`dotenv` → `tasks`.
- Indentacao com 2 espacos.
- Linha em branco separando as secoes principais e separando cada tarefa.
- Nomes de variaveis em MAIUSCULO (`BINARY_NAME`).
- Sem espacos ao interpolar: `{{.VAR}}` (nao `{{ .VAR }}`).
- Nomes de tarefa em kebab-case; `:` separa namespace e nome (`docker:build`).
- Arquivos incluidos em minusculo kebab-case (`taskfiles/build.yml`); a raiz permanece `Taskfile.yml` (nome canonico que o Task procura).
- Preferir scripts externos a comandos multi-linha complexos.

## Boas praticas production-ready
- Manter o `Taskfile.yml` raiz como orquestrador; logica em `taskfiles/`.
- Scripts auxiliares apenas em `taskfiles/scripts/` (nunca em `internal/`, `src/`, `cmd/`).
- Usar `requires.vars` em tarefas perigosas (deploy, migracoes).
- Usar `sources`/`generates` para builds e geracao de mocks idempotentes.
- Usar `preconditions` para checar ferramentas e dependencias antes de rodar.
- Fixar a versao do Task em local e CI (mesma `TASK_VERSION`).
- Manter `.task/` no `.gitignore`.
