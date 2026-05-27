#!/usr/bin/env python3
"""Carrega `.ado-epic-stories.yml` da raiz do repositório (ou cwd para cima).

Uso:
    python3 load-ado-config.py [--start <diretório>] [--max-depth N]

Faz parsing minimalista de YAML chave-valor flat (sem dependência externa).
Suporta apenas:
- chaves de primeiro nível com valores string
- comentários `#`
- chaves esperadas: organization, project, board, process, default_area_path,
  default_iteration_path, child_type_override

Saída JSON em stdout:
    {"path": "/abs/path/.ado-epic-stories.yml", "config": {"organization": "..."}}

Se não encontrar arquivo, retorna `{"path": null, "config": {}}` com exit 0.
Erros de parsing vão para stderr com exit 1.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ALLOWED_KEYS = {
    "organization",
    "project",
    "board",
    "process",
    "default_area_path",
    "default_iteration_path",
    "child_type_override",
    "epic_type_override",
}

LINE_PATTERN = re.compile(r"^([a-z_]+)\s*:\s*(.+?)\s*$")


def find_config(start: Path, max_depth: int) -> Path | None:
    current = start.resolve()
    for _ in range(max_depth + 1):
        candidate = current / ".ado-epic-stories.yml"
        if candidate.is_file():
            return candidate
        if current.parent == current:
            break
        current = current.parent
    return None


def parse_config(path: Path) -> dict:
    config: dict[str, str] = {}
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        match = LINE_PATTERN.match(line)
        if not match:
            raise ValueError(f"linha {lineno}: formato inválido — '{raw}'")
        key, value = match.group(1), match.group(2)
        if key not in ALLOWED_KEYS:
            raise ValueError(f"linha {lineno}: chave não suportada — '{key}'")
        value = value.strip().strip('"').strip("'")
        if not value:
            raise ValueError(f"linha {lineno}: valor vazio para '{key}'")
        config[key] = value
    return config


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", default=".")
    parser.add_argument("--max-depth", type=int, default=5)
    args = parser.parse_args()

    start = Path(args.start)
    config_path = find_config(start, args.max_depth)
    if config_path is None:
        print(json.dumps({"path": None, "config": {}}))
        return 0

    try:
        config = parse_config(config_path)
    except ValueError as exc:
        print(f"ERRO em {config_path}: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"path": str(config_path), "config": config}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
