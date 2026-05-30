#!/usr/bin/env python3
"""Valida um Taskfile production-ready e o isolamento da automacao.

Uso:
    python3 validate-taskfile.py <caminho-do-Taskfile.yml>

Verifica:
1. Existencia e parse YAML do Taskfile.
2. version '3' e comentario de schema.
3. Orquestrador fino: presenca de includes apontando para taskfiles/.
4. Cobertura minima de dominios (build, test, lint, security/vulncheck, mocks).
5. Isolamento: nenhum include aponta para diretorios de codigo-fonte.
6. .gitignore com .task/ (quando o .gitignore existe na mesma raiz).

Exit codes:
    0 SUCCESS
    1 falhas de validacao
    2 uso incorreto / arquivo ausente
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None

SOURCE_DIRS = {"internal", "src", "app", "pkg", "cmd", "lib", "api"}
REQUIRED_DOMAINS = {
    "build": ["build"],
    "test": ["test"],
    "lint": ["lint"],
    "security": ["security", "vuln"],
    "mocks": ["mock"],
}


def fail(messages: list[str]) -> int:
    print("\n".join(messages), file=sys.stderr)
    return 1


def collect_include_paths(includes) -> list[str]:
    paths: list[str] = []
    if isinstance(includes, dict):
        for value in includes.values():
            if isinstance(value, str):
                paths.append(value)
            elif isinstance(value, dict) and "taskfile" in value:
                paths.append(str(value["taskfile"]))
    return paths


def main() -> int:
    if len(sys.argv) != 2:
        print("USO: python3 validate-taskfile.py <caminho-do-Taskfile.yml>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"ARQUIVO AUSENTE: {path}", file=sys.stderr)
        return 2

    raw = path.read_text(encoding="utf-8")
    errors: list[str] = []

    if "yaml-language-server: $schema=https://taskfile.dev/schema.json" not in raw:
        errors.append(
            "SCHEMA ERROR: falta o comentario "
            "'# yaml-language-server: $schema=https://taskfile.dev/schema.json' no topo."
        )

    if yaml is None:
        errors.append("DEP ERROR: modulo 'pyyaml' ausente. Instale com 'pip install pyyaml'.")
        return fail(errors)

    try:
        doc = yaml.safe_load(raw) or {}
    except yaml.YAMLError as exc:  # type: ignore[attr-defined]
        return fail([f"YAML ERROR: {exc}"])

    if str(doc.get("version", "")).strip("'\" ") != "3":
        errors.append("VERSION ERROR: o Taskfile deve declarar version '3'.")

    includes = doc.get("includes", {})
    include_paths = collect_include_paths(includes)
    if not include_paths:
        errors.append(
            "STRUCTURE ERROR: orquestrador sem 'includes'. A automacao deve ser isolada em taskfiles/."
        )

    # Isolamento: includes nao podem apontar para diretorios de codigo-fonte.
    for p in include_paths:
        top = re.split(r"[\\/]", p.lstrip("./"))[0]
        if top in SOURCE_DIRS:
            errors.append(
                f"ISOLATION ERROR: include '{p}' aponta para diretorio de codigo-fonte '{top}'. "
                "Mova a automacao para 'taskfiles/'."
            )

    # Cobertura de dominios: nos nomes dos includes ou nas tasks declaradas.
    haystack = raw.lower()
    for domain, keywords in REQUIRED_DOMAINS.items():
        if not any(k in haystack for k in keywords):
            errors.append(
                f"COVERAGE ERROR: dominio '{domain}' nao encontrado "
                f"(esperado include ou task contendo {keywords})."
            )

    gitignore = path.parent / ".gitignore"
    if gitignore.is_file():
        gi = gitignore.read_text(encoding="utf-8")
        if not re.search(r"(?m)^\.task/?\s*$", gi):
            errors.append("GITIGNORE ERROR: adicione '.task/' ao .gitignore.")

    if errors:
        return fail(errors)

    print("SUCCESS: Taskfile valido, isolado do codigo-fonte e production-ready.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
