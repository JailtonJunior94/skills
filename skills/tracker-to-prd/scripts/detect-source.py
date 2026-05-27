#!/usr/bin/env python3
"""Detecta a ferramenta de origem (Jira ou Azure DevOps) a partir de um input livre.

Uso:
    python3 detect-source.py "PROJ-123"
    python3 detect-source.py "https://dev.azure.com/org/proj/_workitems/edit/4567"
    python3 detect-source.py "org/proj/4567"

Saída em stdout (uma linha):
    jira <ISSUE_KEY>
    ado <ORG> <PROJECT> <ID>

Sai com código 0 quando detecta, 1 quando o input não casa nenhum formato,
2 quando faltar argumento. Mensagem amigável em stderr na falha.

Sem dependências externas.
"""
from __future__ import annotations

import re
import sys
from urllib.parse import unquote, urlparse

JIRA_KEY_RE = re.compile(r"^[A-Z][A-Z0-9]*-\d+$")
ADO_URL_RE = re.compile(
    r"^https?://dev\.azure\.com/(?P<org>[^/]+)/(?P<project>[^/]+)/"
    r"_workitems/edit/(?P<id>\d+)/?(?:\?.*)?$"
)
ADO_VISUALSTUDIO_RE = re.compile(
    r"^https?://(?P<org>[^.]+)\.visualstudio\.com/(?P<project>[^/]+)/"
    r"_workitems/edit/(?P<id>\d+)/?(?:\?.*)?$"
)
ADO_TRIPLE_RE = re.compile(r"^(?P<org>[^/\s]+)/(?P<project>[^/\s]+)/(?P<id>\d+)$")


def detect(raw: str) -> str | None:
    candidate = raw.strip()
    if not candidate:
        return None

    if JIRA_KEY_RE.match(candidate):
        return f"jira {candidate}"

    for pattern in (ADO_URL_RE, ADO_VISUALSTUDIO_RE):
        match = pattern.match(candidate)
        if match:
            org = unquote(match.group("org"))
            project = unquote(match.group("project"))
            return f"ado {org} {project} {match.group('id')}"

    triple = ADO_TRIPLE_RE.match(candidate)
    if triple:
        return (
            f"ado {triple.group('org')} {triple.group('project')} "
            f"{triple.group('id')}"
        )

    # Tolera URL ADO com path adicional (?ex.: /_backlogs ou ?id=)
    parsed = urlparse(candidate)
    if parsed.netloc.endswith("dev.azure.com") or parsed.netloc.endswith(
        ".visualstudio.com"
    ):
        # Tenta extrair id de query string `?id=<n>`
        from urllib.parse import parse_qs

        qs = parse_qs(parsed.query)
        wid = qs.get("id", [None])[0]
        if wid and wid.isdigit():
            parts = [p for p in parsed.path.split("/") if p]
            if parsed.netloc.endswith("dev.azure.com") and len(parts) >= 2:
                return f"ado {unquote(parts[0])} {unquote(parts[1])} {wid}"
            if parsed.netloc.endswith(".visualstudio.com") and parts:
                org = parsed.netloc.split(".")[0]
                return f"ado {org} {unquote(parts[0])} {wid}"

    return None


def main() -> int:
    if len(sys.argv) < 2:
        print("USO: detect-source.py <input>", file=sys.stderr)
        return 2

    raw = " ".join(sys.argv[1:])
    result = detect(raw)
    if result is None:
        print(
            "FORMATO INVALIDO. Use: 'PROJ-123' (Jira) ou "
            "'https://dev.azure.com/<org>/<project>/_workitems/edit/<id>' "
            "ou '<org>/<project>/<id>' (Azure DevOps).",
            file=sys.stderr,
        )
        return 1

    print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
