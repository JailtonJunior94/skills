# Instalacao e particularidades multiplataforma

Versao estavel de referencia: `v3.51.1`. SEMPRE confirme a ultima estavel com
`python3 scripts/check-task-version.py --latest` e fixe a mesma versao em local
e CI.

## Instalacao por SO

### macOS
```sh
brew install go-task/tap/go-task   # tap oficial (sempre atualizado)
# ou
brew install go-task               # homebrew-core
```

### Linux (Ubuntu)
```sh
# Repositorio oficial (apt) via Cloudsmith:
curl -1sLf 'https://dl.cloudsmith.io/public/task/task/setup.deb.sh' | sudo -E bash
sudo apt install task

# Alternativa reproduzivel pinando versao em ./bin:
sh scripts/install-task.sh v3.51.1
```

### Windows
```powershell
winget install Task.Task
# ou (cross-platform, util em projetos Node):
npm install -g @go-task/cli
```

## Diferencas de shell
- Em Linux/macOS o Task usa `sh` (mvdan/sh, POSIX) por padrao.
- No Windows, comandos que dependem de utilitarios POSIX (`rm`, `find`, `test`)
  podem nao existir. Use uma das estrategias:
  1. `platforms: [linux, darwin]` vs `platforms: [windows]` com comando equivalente.
  2. PowerShell explicito: `powershell -Command "..."`.
  3. Script auxiliar em `taskfiles/scripts/` (`.sh` e `.ps1`) selecionado por `{{OS}}`.

## Padroes portateis
- Extensao de binario: `{{.APP_NAME}}{{exeExt}}` resolve `.exe` no Windows.
- Caminhos: prefira `/` (o Task normaliza); evite `\` cravado.
- Limpeza multiplataforma:
  ```yaml
  cmds:
    - cmd: rm -rf bin .task
      platforms: [linux, darwin]
    - cmd: powershell -Command "Remove-Item -Recurse -Force -ErrorAction SilentlyContinue bin, .task"
      platforms: [windows]
  ```
- Cross-compile com matriz `for`:
  ```yaml
  cmds:
    - for: { matrix: { GOOS: [linux, darwin, windows], GOARCH: [amd64, arm64] } }
      cmd: GOOS={{.ITEM.GOOS}} GOARCH={{.ITEM.GOARCH}} go build ./...
  ```

## Variaveis de ambiente do Task
- `TASK_TEMP_DIR`: muda o diretorio do cache `.task` (ex.: `~/.task`).
- `TASK_X_*`: flags experimentais; evitar em producao.
- Em CI sem TTY, `interactive` é ignorado e variaveis ausentes falham normalmente.
