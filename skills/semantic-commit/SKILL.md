---
name: semantic-commit
description: |
  Gera mensagem de Conventional Commit a partir de git diff. Opcionalmente gera resumo conciso de PR.
  Use quando o usuário pede mensagem de commit semântico/convencional ou sugestão de commit a partir de diff.
  Não use para execução de bugfix, QA ou review.
---

# Commit Semântico

<critical>Inferir tipo de commit a partir de evidência do diff</critical>
<critical>Usar formato Conventional Commit: <type>(scope-opcional): <descrição></critical>

## Procedimentos

**Etapa 1: Coletar Diff**
1. Execute `git diff --staged` para obter as mudanças staged.
2. Se não houver mudanças staged, execute `git diff` para mudanças unstaged.
3. Se ambos estiverem vazios, retorne `needs_input` com a mensagem "Nenhuma mudança detectada para gerar commit".

**Etapa 2: Analisar Mudanças**
1. Agrupe mudanças por intenção (nova funcionalidade, correção, refatoração, etc.).
2. Identifique o módulo ou componente mais impactado para definir o scope.

**Etapa 3: Inferir Tipo e Gerar Mensagem**
1. Infira o tipo principal com base no diff:
   - Tipos permitidos: `feat`, `fix`, `refactor`, `perf`, `docs`, `test`, `chore`, `build`, `ci`, `style`.
2. Gere a mensagem no formato: `<type>(<scope>): <descrição concisa>`.
3. Se houver breaking change, adicione `!` após o tipo/scope.

**Etapa 4: Avaliar Necessidade de Divisão**
1. Se o diff contiver mudanças com intenções independentes e sem objetivo dominante, sugira divisão em commits separados (obrigatório).
2. Para cada commit sugerido, gere mensagem individual.

**Etapa 5: Resumo de PR (Opcional)**
1. Se solicitado, gere resumo curto para PR com base nos commits analisados.

## Regras de Desempate
- Múltiplas intenções com objetivo dominante: priorize `feat` > `fix` > `refactor` > `perf` > `docs` > `test` > `chore` > `build` > `ci` > `style`.
- Mudanças independentes sem objetivo dominante: sugira divisão (obrigatório).

## Condições de Parada
- `done`: commit semântico (e opcionalmente divisão/resumo) gerado a partir do diff.
- `needs_input`: diff ausente ou ilegível.

## Formato de Saída
```
Commit:
<commit semântico>

Divisão opcional:
- <commit 1>
- <commit 2>

Resumo de PR opcional:
- [resumo curto]
```

## Tratamento de Erros
- Se `git diff` retornar erro, verifique se o diretório é um repositório Git válido e informe.
- Se o diff for excessivamente grande (>5000 linhas), agrupe por arquivo e gere commit por grupo lógico.
