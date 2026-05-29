#!/usr/bin/env python3
"""Normaliza um título arbitrário em slug kebab-case ASCII.

Uso:
    python3 slugify.py "<titulo>"

Stdout:
    slug normalizado

Stderr:
    mensagem de erro se o slug final ficar vazio
"""
from __future__ import annotations

import re
import sys
import unicodedata


def slugify(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_text.lower()).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)
    return slug


def main() -> int:
    if len(sys.argv) != 2:
        print('USO: python3 slugify.py "<titulo>"', file=sys.stderr)
        return 2

    slug = slugify(sys.argv[1].strip())
    if not slug:
        print("SLUG INVÁLIDO: nenhum caractere alfanumérico útil após normalização.", file=sys.stderr)
        return 1

    print(slug)
    return 0


if __name__ == "__main__":
    sys.exit(main())
