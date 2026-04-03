---
name: reviewer
description: |
  Executa review técnico e funcional de código. Valida arquitetura, correção, segurança,
  manutenibilidade e conformidade funcional contra PRD/TechSpec/Tasks.
  Use quando o usuário pede review, auditoria, validação técnica ou QA, ou quando uma tarefa precisa de gate de aprovação.
  Não use para corrigir bugs documentados (usar bugfix).
---

# Review Técnico e Funcional

<critical>Usar `.claude/rules/` como fonte de verdade</critical>
<critical>Não aprovar quando qualquer regra hard for violada</critical>
<critical>Validar requisitos com evidência objetiva</critical>

## Procedimentos

**Etapa 1: Carregar Contexto**
1. Leia as regras relevantes em `.claude/rules/`.
2. Se PRD, TechSpec ou Tasks estiverem disponíveis, leia-os para validação funcional.

**Etapa 2: Inspecionar Mudanças**
1. Colete o diff via `git diff` e liste os arquivos impactados.
2. Analise cada arquivo contra as dimensões: arquitetura, tratamento de erros, segurança, testes e manutenibilidade.

**Etapa 3: Classificar Achados**
1. Classifique cada achado por severidade:
   - `Critical`: violação de regra `hard`, falha de segurança ou bug de correção.
   - `Major`: violação de regra `guideline` com impacto significativo, falta de teste para caso relevante.
   - `Minor`: estilo, nomenclatura ou melhoria opcional.
2. Referencie o Rule ID específico para cada achado (ex: `R-ARCH-001`).

**Etapa 4: Validar Conformidade Funcional**
1. Se PRD/TechSpec/Tasks estiverem disponíveis, verifique se cada requisito funcional foi atendido.
2. Registre evidência por requisito: arquivo, teste ou comportamento observável.

**Etapa 5: Executar Validações Automatizadas**
1. Execute `go test ./...` e `golangci-lint run`.
2. Documente falhas como bugs no formato canônico: `{ id, severity, file, line, reproduction, expected, actual }`.

**Etapa 6: Produzir Veredito**
1. Aplique a política de decisão:
   - `REJECTED`: qualquer achado `Critical` não resolvido ou violação de regra `hard`.
   - `APPROVED_WITH_REMARKS`: sem `Critical`/`Major` não resolvidos, apenas `Minor` residuais.
   - `APPROVED`: sem achados não resolvidos.
   - `BLOCKED`: evidências ou inputs obrigatórios ausentes para veredito determinístico.

**Etapa 7: Gerar Relatório**
1. Persista o relatório no caminho indicado pelo chamador.
   - Contexto de task: `tasks/prd-[feature-name]/review_report.md`.
   - Padrão: `./review_report.md`.

## Condições de Parada
- Veredito `APPROVED`, `APPROVED_WITH_REMARKS`, `REJECTED` ou `BLOCKED` é obrigatório.
- Se evidência obrigatória estiver ausente, pare com `BLOCKED`.
- Máximo de ciclos de remediação para re-review: padrão de governança.

## Formato de Saída
```markdown
# Relatório de Review

**Veredito**: APPROVED | APPROVED_WITH_REMARKS | REJECTED | BLOCKED

## Achados Técnicos
### Critical
- [achado + Rule ID]

### Major
- [achado + Rule ID]

### Minor
- [achado]

## Verificação Funcional
- Requisitos verificados: X/Y
- Bugs encontrados: Z
- [evidência por requisito quando aplicável]

## Riscos Residuais
- [risco]
```

## Tratamento de Erros
- Se `go test` ou `golangci-lint` falharem por erro de ambiente (não de código), registre e prossiga com aviso.
- Se o diff estiver vazio, retorne `BLOCKED` com a mensagem "Nenhuma mudança para revisar".
- Se regras referenciadas não existirem no diretório, informe e continue com as regras disponíveis.
