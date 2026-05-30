#!/usr/bin/env python3
"""Detecta a versao do Task instalada e/ou a ultima estavel publicada.

Uso:
    python3 check-task-version.py --installed
    python3 check-task-version.py --latest
    python3 check-task-version.py --installed --latest

Stdout:
    Linhas no formato "INSTALLED: vX.Y.Z" e/ou "LATEST: vX.Y.Z".
    Quando ambos forem solicitados, imprime tambem "STATUS: up-to-date|outdated|not-installed".

Stderr:
    Mensagens de erro (Task ausente, falha de rede).

Exit codes:
    0 sucesso
    1 desatualizado ou nao instalado (quando ambos os modos sao usados)
    2 uso incorreto
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import urllib.request

REFERENCE_VERSION = "v3.51.1"
LATEST_URL = "https://api.github.com/repos/go-task/task/releases/latest"


def normalize(version: str) -> str:
    version = version.strip()
    return version if version.startswith("v") else f"v{version}"


def get_installed() -> str | None:
    binary = shutil.which("task")
    if not binary:
        return None
    try:
        out = subprocess.run(
            [binary, "--version"], capture_output=True, text=True, timeout=15
        )
    except (subprocess.SubprocessError, OSError):
        return None
    match = re.search(r"v?\d+\.\d+\.\d+", out.stdout + out.stderr)
    return normalize(match.group(0)) if match else None


def get_latest() -> str | None:
    req = urllib.request.Request(LATEST_URL, headers={"User-Agent": "taskfile-skill"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.load(resp)
    except Exception:  # noqa: BLE001 - rede indisponivel ou rate limit
        return None
    tag = data.get("tag_name")
    return normalize(tag) if tag else None


def main() -> int:
    parser = argparse.ArgumentParser(description="Checa versoes do Task.")
    parser.add_argument("--installed", action="store_true", help="Mostra a versao local.")
    parser.add_argument("--latest", action="store_true", help="Mostra a ultima estavel.")
    args = parser.parse_args()

    if not (args.installed or args.latest):
        print("USO: --installed e/ou --latest", file=sys.stderr)
        return 2

    installed = get_installed() if args.installed else None
    latest = None
    if args.latest:
        latest = get_latest()
        if latest is None:
            print(
                f"AVISO: nao foi possivel consultar a ultima estavel; usando referencia {REFERENCE_VERSION}.",
                file=sys.stderr,
            )
            latest = REFERENCE_VERSION

    if args.installed:
        print(f"INSTALLED: {installed or 'none'}")
    if args.latest:
        print(f"LATEST: {latest}")

    if args.installed and args.latest:
        if installed is None:
            print("STATUS: not-installed")
            return 1
        if installed == latest:
            print("STATUS: up-to-date")
            return 0
        print("STATUS: outdated")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
