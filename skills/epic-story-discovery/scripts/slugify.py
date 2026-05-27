#!/usr/bin/env python3
"""Converte um título PT-BR em slug kebab-case determinístico.

Uso:
    python3 slugify.py "Autenticação Self-Service para Clientes Finais"

Saída em stdout: slug (ex.: `autenticacao-self-service-para-clientes-finais`).

Sem dependências externas. Funciona idêntico em qualquer máquina com Python 3.
"""
from __future__ import annotations

import re
import sys
import unicodedata


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_only = normalized.encode("ascii", "ignore").decode("ascii")
    lowered = ascii_only.lower()
    cleaned = re.sub(r"[^a-z0-9]+", "-", lowered)
    return cleaned.strip("-")


def main() -> int:
    if len(sys.argv) < 2:
        print("USO: slugify.py <texto>", file=sys.stderr)
        return 2

    raw = " ".join(sys.argv[1:]).strip()
    if not raw:
        print("TEXTO VAZIO", file=sys.stderr)
        return 1

    slug = slugify(raw)
    if not slug:
        print("SLUG VAZIO APÓS NORMALIZAÇÃO", file=sys.stderr)
        return 1

    print(slug)
    return 0


if __name__ == "__main__":
    sys.exit(main())
