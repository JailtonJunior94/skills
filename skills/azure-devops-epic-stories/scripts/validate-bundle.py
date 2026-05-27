#!/usr/bin/env python3
"""Valida um bundle de discovery de épico + user stories.

Uso:
    python3 validate-bundle.py <caminho-do-bundle>

Verifica:
1. Estrutura de diretório (epic.md, us/, bundle.json, transcript.md).
2. bundle.json válido contra a especificação v1.
3. epic.md contém todas as seções obrigatórias.
4. Seções críticas do épico sem placeholder proibido.
5. Cada US.md em us/ contém todas as seções obrigatórias.
6. Seções críticas de cada US sem placeholder proibido.
7. Descrição da US contém bloco Como/Quero/Para.
8. Critérios de aceite de cada US contêm Gherkin (Dado que / Quando / Então).
9. Cada US tem pelo menos um cenário de exceção/erro.

Regras de detecção sem falso positivo conforme references/content-quality-rules.md.

Exit 0: SUCCESS.
Exit 1: erros (stderr lista cada um com arquivo:seção).
Exit 2: uso incorreto.

Sem dependências externas. Stdlib only.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

EPIC_REQUIRED_SECTIONS = [
    "## Título",
    "## Objetivo do Negócio",
    "## Hipótese de Valor",
    "## Escopo",
    "## Fora de Escopo",
    "## Stakeholders",
    "## Personas Impactadas",
    "## Critérios de Aceite do Épico",
    "## KPIs / Métricas de Sucesso",
    "## Dependências",
    "## Riscos",
    "## Releases / Marcos",
    "## User Stories Relacionadas",
]

EPIC_CRITICAL_SECTIONS = {
    "## Título",
    "## Objetivo do Negócio",
    "## Hipótese de Valor",
    "## Escopo",
    "## Critérios de Aceite do Épico",
    "## KPIs / Métricas de Sucesso",
}

US_REQUIRED_SECTIONS = [
    "## Título",
    "## Descrição",
    "## Contexto / Regras de Negócio",
    "## Critérios de Aceite",
    "## Dependências",
    "## Fora de Escopo",
    "## Definition of Done (referência do time)",
]

US_CRITICAL_SECTIONS = {
    "## Título",
    "## Descrição",
    "## Contexto / Regras de Negócio",
    "## Critérios de Aceite",
}

PLACEHOLDER_EXACT = {
    "TBD",
    "A DEFINIR",
    "A CONFIRMAR",
    "PENDENTE",
    "N/A",
    "?",
    "-",
    "...",
}

BULLET_STRIP = re.compile(r"^\s*(?:[-*+]|\d+\.)?\s*")
BRACKET_ONLY = re.compile(r"^\s*(?:[-*+]|\d+\.)?\s*\[(?![ xX]?\s*\]).+\]\s*$")

DESCRIPTION_KEYWORDS = ["Como", "Quero", "Para"]
GHERKIN_KEYWORDS = ["Dado que", "Quando", "Então"]
EXCEPTION_HINTS = re.compile(r"\b(Exce[çc][ãa]o|Erro|Inv[áa]lid|Falha)\b", re.IGNORECASE)


def split_sections(text: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    current: str | None = None
    buffer: list[str] = []
    for line in text.splitlines():
        if line.startswith("## "):
            if current is not None:
                sections[current] = "\n".join(buffer).strip()
            current = line.strip()
            buffer = []
        else:
            buffer.append(line)
    if current is not None:
        sections[current] = "\n".join(buffer).strip()
    return sections


def detect_placeholders(body: str) -> list[str]:
    """Retorna lista de linhas que violam regras de placeholder."""
    issues: list[str] = []
    for line in body.splitlines():
        if not line.strip():
            continue
        stripped = BULLET_STRIP.sub("", line).strip()
        if stripped.upper() in PLACEHOLDER_EXACT:
            issues.append(f"placeholder proibido: '{line.strip()}'")
            continue
        if BRACKET_ONLY.match(line):
            issues.append(f"bracket-only não preenchido: '{line.strip()}'")
    return issues


def validate_epic(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.is_file():
        return [f"{path.name}: arquivo ausente"]
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        return [f"{path.name}: arquivo vazio"]
    sections = split_sections(text)
    for required in EPIC_REQUIRED_SECTIONS:
        if required not in sections:
            errors.append(f"{path.name}: seção ausente '{required}'")
            continue
        body = sections[required]
        if required in EPIC_CRITICAL_SECTIONS:
            if not body:
                errors.append(f"{path.name}: seção crítica vazia '{required}'")
                continue
            for issue in detect_placeholders(body):
                errors.append(f"{path.name} → {required}: {issue}")
    return errors


def validate_user_story(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.is_file():
        return [f"{path.name}: arquivo ausente"]
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        return [f"{path.name}: arquivo vazio"]
    sections = split_sections(text)

    for required in US_REQUIRED_SECTIONS:
        if required not in sections:
            errors.append(f"{path.name}: seção ausente '{required}'")
            continue
        body = sections[required]
        if required in US_CRITICAL_SECTIONS:
            if not body:
                errors.append(f"{path.name}: seção crítica vazia '{required}'")
                continue
            for issue in detect_placeholders(body):
                errors.append(f"{path.name} → {required}: {issue}")

    descricao = sections.get("## Descrição", "")
    for keyword in DESCRIPTION_KEYWORDS:
        if keyword not in descricao:
            errors.append(
                f"{path.name} → ## Descrição: falta palavra-chave '{keyword}' do bloco Como/Quero/Para"
            )

    criterios = sections.get("## Critérios de Aceite", "")
    for keyword in GHERKIN_KEYWORDS:
        if keyword not in criterios:
            errors.append(
                f"{path.name} → ## Critérios de Aceite: falta keyword Gherkin '{keyword}'"
            )
    if not EXCEPTION_HINTS.search(criterios):
        errors.append(
            f"{path.name} → ## Critérios de Aceite: nenhum cenário de exceção/erro detectado"
        )

    return errors


def validate_bundle_json(path: Path, expected_us_files: list[Path]) -> list[str]:
    errors: list[str] = []
    if not path.is_file():
        return ["bundle.json: arquivo ausente"]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"bundle.json: JSON inválido — {exc}"]

    required_top = {"version", "slug", "title", "created_at", "language", "epic", "user_stories"}
    missing = required_top - data.keys()
    if missing:
        errors.append(f"bundle.json: campos ausentes — {sorted(missing)}")
        return errors

    if data["version"] != 1:
        errors.append(f"bundle.json: versão não suportada — {data['version']}")
    if data["language"] != "pt-BR":
        errors.append(f"bundle.json: language deve ser 'pt-BR'")
    if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", str(data.get("slug", ""))):
        errors.append(f"bundle.json: slug inválido — '{data.get('slug')}'")
    if not str(data.get("title", "")).strip():
        errors.append("bundle.json: title vazio")
    epic = data.get("epic", {})
    if epic.get("file") != "epic.md":
        errors.append("bundle.json: epic.file deve ser 'epic.md'")
    if not str(epic.get("title", "")).strip():
        errors.append("bundle.json: epic.title vazio")

    us_entries = data.get("user_stories", [])
    if not isinstance(us_entries, list) or not us_entries:
        errors.append("bundle.json: user_stories vazio ou inválido")
        return errors

    declared_files = set()
    for entry in us_entries:
        for key in ("local_id", "slug", "title", "file"):
            if not entry.get(key):
                errors.append(f"bundle.json: US '{entry}' faltando '{key}'")
        if not re.match(r"^\d{2}$", str(entry.get("local_id", ""))):
            errors.append(f"bundle.json: local_id deve ter 2 dígitos — '{entry.get('local_id')}'")
        declared_files.add(entry.get("file"))

    actual_files = {f"us/{p.name}" for p in expected_us_files}
    only_declared = declared_files - actual_files
    only_actual = actual_files - declared_files
    if only_declared:
        errors.append(f"bundle.json declara US sem arquivo: {sorted(only_declared)}")
    if only_actual:
        errors.append(f"Arquivos US sem entrada em bundle.json: {sorted(only_actual)}")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("USO: validate-bundle.py <caminho-do-bundle>", file=sys.stderr)
        return 2

    bundle_dir = Path(sys.argv[1]).resolve()
    if not bundle_dir.is_dir():
        print(f"DIRETÓRIO INVÁLIDO: {bundle_dir}", file=sys.stderr)
        return 1

    errors: list[str] = []

    us_dir = bundle_dir / "us"
    us_files = sorted(us_dir.glob("*.md")) if us_dir.is_dir() else []

    errors += validate_bundle_json(bundle_dir / "bundle.json", us_files)
    errors += validate_epic(bundle_dir / "epic.md")

    if not us_files:
        errors.append("us/: nenhum arquivo .md encontrado")
    for path in us_files:
        if not re.match(r"^\d{2}_[a-z0-9]+(?:-[a-z0-9]+)*\.md$", path.name):
            errors.append(f"{path.name}: nome de arquivo inválido (esperado NN_slug.md)")
            continue
        errors += validate_user_story(path)

    transcript = bundle_dir / "transcript.md"
    if not transcript.is_file() or not transcript.read_text(encoding="utf-8").strip():
        errors.append("transcript.md: ausente ou vazio")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    print(f"SUCCESS: bundle válido — {bundle_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
