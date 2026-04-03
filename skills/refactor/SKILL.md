---
name: refactor
description: |
  Executa refatoração segura e incremental para projetos Go, preservando comportamento e reduzindo complexidade.
  Use quando o usuário pede para refatorar, simplificar ou melhorar manutenibilidade.
  Não use para correção de bug (usar bugfix) nem para review/auditoria (usar reviewer).
---

# Refatoração Segura

<critical>Preservar comportamento e contratos existentes</critical>
<critical>Aplicar passos pequenos, testáveis e reversíveis</critical>

## Procedimentos

**Etapa 1: Definir Modo de Operação**
1. Identifique o modo solicitado:
   - `advisory`: gere apenas plano e recomendações (padrão).
   - `execution`: aplique refatoração no código.
2. Se o modo não for explícito, assuma `advisory` e confirme com o usuário.

**Etapa 2: Mapear Hotspots**
1. Identifique arquivos e funções que satisfaçam qualquer critério:
   - Alta complexidade ciclomática.
   - Tamanho excessivo (>50 linhas/função ou >300 linhas/arquivo).
   - Violações de regras em `.claude/rules/`.
   - Alto acoplamento entre módulos.
2. Priorize hotspots por impacto na manutenibilidade.

**Etapa 3: Planejar Refatoração**
1. Defina objetivo de refatoração por hotspot.
2. Descreva cada mudança como passo incremental e reversível.
3. Identifique dependências entre passos.

**Etapa 4: Executar (apenas modo `execution`)**
1. Aplique cada passo incremental.
2. Execute `go test ./...` após cada passo.
3. Se testes falharem, reverta o passo e registre como `blocked`.

**Etapa 5: Avaliar Risco**
1. Classifique o risco com critérios objetivos:
   - `Low`: todos os testes passam, sem violações, complexidade mantida ou reduzida.
   - `Medium`: testes passam mas complexidade aumentou ou novas dependências introduzidas. Prossiga com aviso explícito.
   - `High`: falhas de teste, violações de regras ou contratos quebrados. Pare com `blocked`.

**Etapa 6: Gerar Relatório**
1. Persista o relatório no caminho indicado pelo chamador.
   - Contexto de task: `tasks/prd-[feature-name]/refactor_report.md`.
   - Padrão: `./refactor_report.md`.

## Condições de Parada
- `done`: objetivo do modo selecionado completado com evidência.
- `blocked`: risco residual aumentou ou dependência externa bloqueia progresso.
- `failed`: limite de remediação excedido sem convergência.

## Formato de Saída
```markdown
# Relatório de Refatoração
- Modo: advisory | execution
- Hotspots: [lista com critério de seleção]
- Mudanças: [lista de passos aplicados ou recomendados]
- Validação: [evidência de testes]
- Risco residual: Low | Medium | High
```

## Tratamento de Erros
- Se `go test` falhar após um passo, reverta imediatamente e registre o motivo.
- Se o escopo de refatoração for ambíguo, solicite confirmação antes de prosseguir com `needs_input`.
- Se nenhum hotspot for encontrado, informe e encerre com `done`.
