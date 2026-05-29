#!/usr/bin/env python3
"""Valida o bundle do discovery técnico production-ready.

Uso:
    python3 validate-bundle.py <caminho-do-bundle>

Verifica:
1. Estrutura de diretório.
2. bundle.json mínimo e consistente.
3. discovery.md com seções obrigatórias.
4. Seções críticas sem placeholder proibido.
5. Campos estruturais mínimos nas seções críticas.
6. Decomposição com ao menos um Epic e uma Feature.

Exit 0: SUCCESS
Exit 1: erros estruturais ou de conteúdo
Exit 2: uso incorreto
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    "## Título",
    "## Resumo Executivo",
    "## Necessidade e Objetivos",
    "## Materiais de Apoio",
    "## Escopo",
    "## Premissas e Restrições",
    "## Viabilidade Técnica",
    "## Arquitetura Atual",
    "## Arquitetura Proposta",
    "## Dados e Integrações",
    "## Volumetria e Capacidade",
    "## Segurança e Compliance",
    "## Confiabilidade e Resiliência",
    "## Observabilidade e Operação",
    "## Performance e Escalabilidade",
    "## Custos e Orçamento",
    "## Riscos e Mitigações",
    "## Trade-offs e Decisões",
    "## Plano de Entrega e Rollout",
    "## Decomposição em Épicos e Features",
    "## Itens em Aberto",
]

CRITICAL_SECTIONS = {
    "## Título",
    "## Necessidade e Objetivos",
    "## Escopo",
    "## Viabilidade Técnica",
    "## Arquitetura Proposta",
    "## Volumetria e Capacidade",
    "## Segurança e Compliance",
    "## Confiabilidade e Resiliência",
    "## Observabilidade e Operação",
    "## Custos e Orçamento",
    "## Riscos e Mitigações",
    "## Decomposição em Épicos e Features",
}

MANDATORY_MARKERS = {
    "## Resumo Executivo": ["Contexto:", "Recomendação:", "Status de viabilidade:"],
    "## Necessidade e Objetivos": ["Problema atual:", "Objetivos de negócio:", "Objetivos técnicos:"],
    "## Escopo": ["Inclui:", "Exclui:"],
    "## Premissas e Restrições": ["Premissas:", "Restrições:"],
    "## Viabilidade Técnica": ["Status:", "Justificativa:", "Bloqueadores:"],
    "## Arquitetura Proposta": ["Componentes:", "Fluxo de alto nível:", "Decisão arquitetural:"],
    "## Dados e Integrações": ["Domínios de dados:", "Integrações:", "Consistência requerida:"],
    "## Volumetria e Capacidade": [
        "Volume atual:",
        "Pico esperado:",
        "Taxa de crescimento:",
        "SLO alvo:",
        "Gargalos conhecidos:",
    ],
    "## Segurança e Compliance": [
        "Classificação dos dados:",
        "Autenticação e autorização:",
        "Gestão de segredos:",
        "Criptografia:",
        "Auditoria e rastreabilidade:",
        "Compliance/LGPD:",
    ],
    "## Confiabilidade e Resiliência": [
        "SLA/SLO:",
        "RTO/RPO:",
        "Estratégia de retry/idempotência:",
        "Degradação/contingência:",
        "Rollback:",
    ],
    "## Observabilidade e Operação": [
        "Métricas:",
        "Logs:",
        "Traces:",
        "Alertas:",
        "Dashboards/Runbooks:",
    ],
    "## Performance e Escalabilidade": [
        "Latência alvo:",
        "Estratégia de escala:",
        "Limites conhecidos:",
        "Teste de carga:",
    ],
    "## Custos e Orçamento": [
        "Orçamento estimado:",
        "Drivers de custo:",
        "Guardrails de custo:",
        "Plano de otimização:",
    ],
    "## Trade-offs e Decisões": [
        "Alternativas consideradas:",
        "Decisão tomada:",
        "Trade-off aceito:",
    ],
    "## Plano de Entrega e Rollout": [
        "Fases:",
        "Migração:",
        "Feature flags/canary:",
        "Critério de rollback:",
    ],
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
EPIC_PATTERN = re.compile(r"(?m)^### Epic \d{2} - .+$")
FEATURE_PATTERN = re.compile(r"(?m)^Feature \d{2}: .+$")


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


def validate_bundle_json(path: Path) -> list[str]:
    if not path.is_file():
        return ["bundle.json: arquivo ausente"]

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"bundle.json: JSON inválido - {exc}"]

    errors: list[str] = []
    required_top = {
        "version",
        "slug",
        "title",
        "created_at",
        "language",
        "status",
        "discovery",
        "transcript",
        "readiness",
        "planned_epics",
    }
    missing = required_top - data.keys()
    if missing:
        return [f"bundle.json: campos ausentes - {sorted(missing)}"]

    if data["version"] != 1:
        errors.append(f"bundle.json: versão não suportada - {data['version']}")
    if data["language"] != "pt-BR":
        errors.append("bundle.json: language deve ser 'pt-BR'")
    if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", str(data.get("slug", ""))):
        errors.append(f"bundle.json: slug inválido - '{data.get('slug')}'")
    if not str(data.get("title", "")).strip():
        errors.append("bundle.json: title vazio")

    discovery = data.get("discovery", {})
    if discovery.get("file") != "discovery.md":
        errors.append("bundle.json: discovery.file deve ser 'discovery.md'")
    if not str(discovery.get("title", "")).strip():
        errors.append("bundle.json: discovery.title vazio")

    transcript = data.get("transcript", {})
    if transcript.get("file") != "transcript.md":
        errors.append("bundle.json: transcript.file deve ser 'transcript.md'")

    readiness = data.get("readiness", {})
    if "status" not in readiness or "blockers" not in readiness:
        errors.append("bundle.json: readiness deve conter 'status' e 'blockers'")
    if not isinstance(readiness.get("blockers", []), list):
        errors.append("bundle.json: readiness.blockers deve ser lista")

    planned_epics = data.get("planned_epics", [])
    if not isinstance(planned_epics, list) or not planned_epics:
        errors.append("bundle.json: planned_epics vazio ou inválido")

    return errors


def validate_discovery(path: Path) -> list[str]:
    if not path.is_file():
        return ["discovery.md: arquivo ausente"]

    text = path.read_text(encoding="utf-8")
    if not text.strip():
        return ["discovery.md: arquivo vazio"]

    sections = split_sections(text)
    errors: list[str] = []

    for required in REQUIRED_SECTIONS:
        if required not in sections:
            errors.append(f"discovery.md: seção ausente '{required}'")
            continue

        body = sections[required]
        if required in CRITICAL_SECTIONS:
            if not body:
                errors.append(f"discovery.md: seção crítica vazia '{required}'")
                continue
            for issue in detect_placeholders(body):
                errors.append(f"discovery.md -> {required}: {issue}")

        for marker in MANDATORY_MARKERS.get(required, []):
            if marker not in body:
                errors.append(f"discovery.md -> {required}: marcador obrigatório ausente '{marker}'")

    decomposition = sections.get("## Decomposição em Épicos e Features", "")
    if decomposition:
        if not EPIC_PATTERN.search(decomposition):
            errors.append("discovery.md -> ## Decomposição em Épicos e Features: nenhum Epic detectado")
        if not FEATURE_PATTERN.search(decomposition):
            errors.append("discovery.md -> ## Decomposição em Épicos e Features: nenhuma Feature detectada")

    return errors


def validate_transcript(path: Path) -> list[str]:
    if not path.is_file():
        return ["transcript.md: arquivo ausente"]
    text = path.read_text(encoding="utf-8")
    if "## Contexto Inicial" not in text:
        return ["transcript.md: seção obrigatória '## Contexto Inicial' ausente"]
    return []


def main() -> int:
    if len(sys.argv) != 2:
        print("USO: validate-bundle.py <caminho-do-bundle>", file=sys.stderr)
        return 2

    bundle_dir = Path(sys.argv[1]).resolve()
    if not bundle_dir.is_dir():
        print(f"DIRETÓRIO INVÁLIDO: {bundle_dir}", file=sys.stderr)
        return 1

    errors: list[str] = []
    errors += validate_bundle_json(bundle_dir / "bundle.json")
    errors += validate_discovery(bundle_dir / "discovery.md")
    errors += validate_transcript(bundle_dir / "transcript.md")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    print("SUCCESS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
