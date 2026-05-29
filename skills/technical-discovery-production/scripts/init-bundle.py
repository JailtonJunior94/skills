#!/usr/bin/env python3
"""Inicializa a estrutura do bundle de discovery técnico.

Uso:
    python3 init-bundle.py <slug> [--root <diretorio-raiz>]

Cria:
- discoveries/technical-<slug>/bundle.json
- discoveries/technical-<slug>/discovery.md
- discoveries/technical-<slug>/transcript.md

Falha com exit 1 se o diretório já existir ou o slug for inválido.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("slug")
    parser.add_argument("--root", default=".", help="Diretório raiz (default: cwd)")
    args = parser.parse_args()

    slug = args.slug.strip()
    if not SLUG_PATTERN.match(slug):
        print(
            f"SLUG INVÁLIDO: '{slug}'. Use kebab-case lowercase com letras, números e hífen.",
            file=sys.stderr,
        )
        return 1

    root = Path(args.root).resolve()
    bundle_dir = root / "discoveries" / f"technical-{slug}"
    if bundle_dir.exists():
        print(f"DIRETÓRIO JÁ EXISTE: {bundle_dir}", file=sys.stderr)
        return 1

    bundle_dir.mkdir(parents=True, exist_ok=False)

    bundle = {
        "version": 1,
        "slug": slug,
        "title": "",
        "created_at": utc_now_iso(),
        "language": "pt-BR",
        "status": "draft",
        "discovery": {"file": "discovery.md", "title": ""},
        "transcript": {"file": "transcript.md"},
        "readiness": {"status": "draft", "blockers": []},
        "planned_epics": [],
    }
    (bundle_dir / "bundle.json").write_text(
        json.dumps(bundle, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    (bundle_dir / "discovery.md").write_text("", encoding="utf-8")
    (bundle_dir / "transcript.md").write_text(
        "# Transcript do Discovery Técnico\n\n## Contexto Inicial\n\n",
        encoding="utf-8",
    )

    print(str(bundle_dir))
    return 0


if __name__ == "__main__":
    sys.exit(main())
