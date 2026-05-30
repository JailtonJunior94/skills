#!/usr/bin/env sh
# Instala uma versao especifica do Task de forma reproduzivel (macOS e Linux).
#
# Uso:
#   sh install-task.sh <versao>      # ex.: sh install-task.sh v3.51.1
#   sh install-task.sh               # usa a versao de referencia
#
# Estrategia:
#   1. Se Homebrew existir, usa o tap oficial (macOS/Linux).
#   2. Caso contrario, usa o instalador oficial fixando a versao em ./bin.
#
# Windows: usar "winget install Task.Task" ou "npm install -g @go-task/cli".
# Ver references/cross-platform.md.
set -eu

REFERENCE_VERSION="v3.51.1"
VERSION="${1:-$REFERENCE_VERSION}"
INSTALL_DIR="${TASK_INSTALL_DIR:-./bin}"

echo "==> Instalando Task ${VERSION}"

if command -v brew >/dev/null 2>&1; then
  echo "==> Homebrew detectado; instalando via tap oficial."
  brew install go-task/tap/go-task
  task --version
  exit 0
fi

echo "==> Homebrew ausente; usando instalador oficial em ${INSTALL_DIR}."
mkdir -p "${INSTALL_DIR}"
# O instalador oficial aceita -b (dir) e a tag de versao como argumento.
curl -fsSL https://taskfile.dev/install.sh | sh -s -- -d -b "${INSTALL_DIR}" "${VERSION}"

echo "==> Task instalado em ${INSTALL_DIR}. Adicione ao PATH:"
echo "    export PATH=\"\$PWD/${INSTALL_DIR#./}:\$PATH\""
"${INSTALL_DIR}/task" --version
