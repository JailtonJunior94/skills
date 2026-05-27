#!/usr/bin/env python3
"""Normaliza um título de work item para detecção determinística de duplicata.

Uso:
    python3 normalize-title.py "Autenticação Self-Service"
    python3 normalize-title.py --json "Autenticação Self-Service"

Aplica:
1. NFKD + remoção de diacríticos (acentos).
2. Lowercase.
3. Remoção de pontuação.
4. Remoção de stopwords PT-BR comuns.
5. Tokens ordenados alfabeticamente para comparação estável.

Saída padrão (stdout):
    autenticacao self service

Saída --json:
    {"normalized": "autenticacao self service", "tokens": ["autenticacao","self","service"], "distinctive_token": "autenticacao"}

`distinctive_token` é o token mais longo, usado para filtrar WIQL.
Sem dependências externas.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata

STOPWORDS_PT = {
    "a", "o", "as", "os", "um", "uma", "uns", "umas",
    "de", "do", "da", "dos", "das",
    "em", "no", "na", "nos", "nas",
    "por", "para", "pelo", "pela", "pelos", "pelas",
    "com", "sem", "sob", "sobre",
    "e", "ou", "mas",
    "que", "se", "ao", "aos",
    "ser", "estar", "ter",
}


def normalize(value: str) -> dict:
    nfkd = unicodedata.normalize("NFKD", value)
    ascii_only = nfkd.encode("ascii", "ignore").decode("ascii")
    lowered = ascii_only.lower()
    no_punct = re.sub(r"[^a-z0-9\s-]", " ", lowered)
    tokens_raw = [t for t in re.split(r"[\s-]+", no_punct) if t]
    tokens = [t for t in tokens_raw if t not in STOPWORDS_PT and len(t) > 1]
    if not tokens:
        tokens = tokens_raw
    sorted_tokens = sorted(tokens)
    distinctive = max(tokens, key=len) if tokens else ""
    return {
        "normalized": " ".join(sorted_tokens),
        "tokens": sorted_tokens,
        "distinctive_token": distinctive,
        "raw_tokens": tokens,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("title")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    raw = args.title.strip()
    if not raw:
        print("TÍTULO VAZIO", file=sys.stderr)
        return 1

    result = normalize(raw)
    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(result["normalized"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
