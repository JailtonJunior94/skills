#!/usr/bin/env sh
# Aguarda um host:porta ficar disponivel antes de prosseguir (ex.: banco em
# testes de integracao). Script auxiliar ISOLADO em taskfiles/scripts/ para
# nao poluir o codigo-fonte da aplicacao.
#
# Uso:
#   sh wait-for.sh <host> <porta> [timeout_segundos]
set -eu

HOST="${1:?informe o host}"
PORT="${2:?informe a porta}"
TIMEOUT="${3:-30}"

echo "==> Aguardando ${HOST}:${PORT} (timeout ${TIMEOUT}s)"
i=0
while [ "${i}" -lt "${TIMEOUT}" ]; do
  if nc -z "${HOST}" "${PORT}" 2>/dev/null; then
    echo "==> ${HOST}:${PORT} disponivel."
    exit 0
  fi
  i=$((i + 1))
  sleep 1
done

echo "ERRO: ${HOST}:${PORT} nao respondeu em ${TIMEOUT}s." >&2
exit 1
