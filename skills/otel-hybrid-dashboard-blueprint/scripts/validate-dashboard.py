#!/usr/bin/env python3
"""Valida JSON de dashboard Grafana gerado pelo blueprint híbrido OTel.

Uso:
    python3 validate-dashboard.py --file <caminho>

Saída:
    stdout: relatório de sucesso
    stderr: lista de erros encontrados (sai com código != 0)
"""

import argparse
import json
import sys


REQUIRED_VARS = {"service", "env", "region"}
REQUIRED_DATASOURCE_VARS = {"DS_PROMETHEUS", "DS_LOKI", "DS_TEMPO"}


def validate(path: str) -> list[str]:
    errors: list[str] = []
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        return [f"FILE ERROR: arquivo não encontrado: {path}"]
    except json.JSONDecodeError as exc:
        return [f"JSON ERROR: {exc.msg} (linha {exc.lineno}, col {exc.colno})"]

    if "title" not in data or not data["title"]:
        errors.append("STRUCTURE ERROR: campo 'title' ausente ou vazio.")
    if "uid" not in data or not data["uid"]:
        errors.append("STRUCTURE ERROR: campo 'uid' ausente ou vazio.")

    templating = data.get("templating", {}).get("list", [])
    var_names = {v.get("name") for v in templating}
    missing_vars = REQUIRED_VARS - var_names
    if missing_vars:
        errors.append(
            f"VARIABLE ERROR: variáveis obrigatórias ausentes: {sorted(missing_vars)}"
        )
    missing_ds = REQUIRED_DATASOURCE_VARS - var_names
    if missing_ds:
        errors.append(
            f"DATASOURCE ERROR: variáveis de datasource ausentes: {sorted(missing_ds)}"
        )

    panels = data.get("panels", [])
    ids = [p.get("id") for p in panels if "id" in p]
    if len(ids) != len(set(ids)):
        errors.append("PANEL ERROR: IDs de painéis duplicados.")

    for p in panels:
        gp = p.get("gridPos") or {}
        x = gp.get("x", 0)
        w = gp.get("w", 0)
        if x + w > 24:
            errors.append(
                f"GRID ERROR: painel id={p.get('id')} excede 24 colunas (x={x}, w={w})."
            )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Grafana dashboard JSON.")
    parser.add_argument("--file", required=True, help="Caminho do arquivo JSON.")
    args = parser.parse_args()

    errors = validate(args.file)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"SUCCESS: dashboard {args.file} válido.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
