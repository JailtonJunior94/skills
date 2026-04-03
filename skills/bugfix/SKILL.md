---
name: bugfix
description: |
  Corrige bugs pela causa raiz com testes de regressão obrigatórios.
  Use quando o usuário pede para corrigir bugs ou referencia bugs.md.
  Não use para review/auditoria (usar reviewer) nem para refatoração (usar refactor).
---

# Correção de Bugs

<critical>Todo bug corrigido deve ter um teste de regressão</critical>
<critical>Não finalizar com bugs pendentes no escopo acordado</critical>

## Procedimentos

**Etapa 1: Validar Entrada**
1. Receba a lista de bugs no formato canônico: `{ id, severity, file, line, reproduction, expected, actual }` (compatível com saída da skill reviewer).
2. Se a lista estiver ausente ou incompleta, retorne `needs_input` com os campos faltantes.
3. Confirme o escopo de bugs a corrigir com o usuário antes de prosseguir.

**Etapa 2: Priorizar e Planejar**
1. Ordene os bugs por severidade: `critical` > `major` > `minor`.
2. Para cada bug, identifique a causa raiz antes de propor qualquer correção.
3. Se um bug depender de contexto externo não disponível, marque como `blocked` e prossiga com os demais.

**Etapa 3: Corrigir e Testar**
1. Aplique a correção focada na causa raiz — evite patches superficiais.
2. Crie um teste de regressão que reproduza o cenário descrito em `reproduction` e valide `expected`.
3. Execute `go test ./...` e `golangci-lint run` após cada correção.
4. Se a validação falhar, ajuste a correção e reexecute — máximo de 2 tentativas por bug.

**Etapa 4: Atualizar Status**
1. Registre evidência de correção para cada bug: arquivo alterado, teste adicionado, resultado da validação.
2. Atualize o status do bug: `fixed`, `blocked` ou `skipped`.

**Etapa 5: Gerar Relatório**
1. Persista o relatório no caminho indicado pelo chamador.
   - Contexto de task: `tasks/prd-[feature-name]/bugfix_report.md`.
   - Padrão: `./bugfix_report.md`.

## Condições de Parada
- `done`: escopo acordado corrigido e validado com testes de regressão.
- `blocked`: bug crítico depende de contexto externo não resolvido.
- `needs_input`: dados obrigatórios de reprodução ou escopo ausentes.
- `failed`: limite de remediação excedido (ver padrão de governança).

## Formato de Saída
```markdown
# Relatório de Bugfix
- Total de bugs no escopo: X
- Corrigidos: Y
- Testes de regressão adicionados: Z
- Pendentes: [lista com motivo]
```

## Tratamento de Erros
- Se `go test` falhar após a correção, analise o log de falha e ajuste — não reexecute cegamente.
- Se o formato de entrada não corresponder ao canônico, solicite ao usuário a conversão antes de prosseguir.
- Se o limite de 2 tentativas por bug for excedido, registre como `failed` com diagnóstico e prossiga.
