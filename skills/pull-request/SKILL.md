---
name: pull-request
description: |
  Cria ou atualiza um Pull Request no GitHub para a branch atual usando convenções de commit semântico.
  Analisa git diff e commits para gerar título e body descritivos.
  Use quando o usuário pede para criar, abrir ou atualizar PR, ou menciona "pull request" ou "PR".
  Não use para commit semântico (usar semantic-commit), review de código (usar reviewer) ou análise de release.
---

# Pull Request

<critical>Título da PR DEVE seguir formato Conventional Commit</critical>
<critical>Body da PR DEVE ter no mínimo 50 caracteres e descrever EXATAMENTE o que foi feito</critical>
<critical>Verificar se já existe PR aberta para a branch antes de criar nova</critical>
<critical>Título e body da PR DEVEM estar em português BR</critical>

## Procedimentos

**Etapa 1: Coletar Contexto**
1. Obtenha a branch atual: `git branch --show-current`.
2. Infira a base branch pelo prefixo:
   - `feat/`, `fix/`, `refactor/`, `chore/` → `develop`.
   - `release-candidate` → `main`.
   - `hotfix/*` → `main`.
   - Se não inferível → retorne `needs_input`.
3. Verifique se a branch está atualizada com remote: `git status -sb`.
4. Se houver push pendente, execute: `git push -u origin <branch>`.

**Etapa 2: Verificar PR Existente**
1. Busque PR aberta para a branch atual:
   ```bash
   gh pr list --head <branch> --state open --json number,title,body,url
   ```
2. Se PR existente encontrada → prossiga para Etapa 4 (Atualização).
3. Se nenhuma PR encontrada → prossiga para Etapa 3 (Criação).

**Etapa 3: Analisar Mudanças**
1. Colete dados:
   ```bash
   git log <base>..HEAD --oneline --no-merges
   git diff <base>...HEAD --stat
   ```
2. Infira o tipo principal: priorize `feat` > `fix` > `refactor` > `perf` > `docs` > `test` > `chore` > `build` > `ci` > `style`.
3. Identifique o scope: módulo ou componente mais impactado.
4. Gere o título no formato: `<type>(<scope>): <descrição concisa>`.
5. Gere o body seguindo o template do repositório (ver Formato de Body).

**Etapa 4: Criar ou Atualizar PR**
1. Para nova PR:
   ```bash
   gh pr create --base <base-branch> --title "<título>" --body "<body>"
   ```
2. Para PR existente:
   ```bash
   gh pr edit <number> --title "<novo-título>" --body "<novo-body>"
   ```
   Recalcule título e body com base nos commits atuais.

**Etapa 5: Confirmar**
1. Exiba a URL da PR ao usuário.
2. Informe se foi criada ou atualizada.

## Regras de Validação do Repositório
- Tipos permitidos no título: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.
- Scope: opcional.
- Descrição mínima no body: 50 caracteres.
- Source branches para main: `develop|release-candidate|hotfix/*`.
- Target branches válidas: `develop`, `release-candidate`, `main`.

## Formato de Body
```markdown
## Descrição

<resumo conciso do que esse PR faz, descrevendo o "o quê" e "por quê">

## Tipo de mudança
Marque com um x todas as opções que se aplicam ao seu PR:
- [ ] Correção (non-breaking change, corrigindo um recurso)
- [ ] Nova funcionalidade (non-breaking change, adicionando novos recursos)
- [ ] Breaking change (correção ou nova funcionalidade que impacta recursos existentes)

## Checklist
Antes de submeter o PR, realize todas as atividades requeridas pelo checklist e marque com um x:
- [ ] <itens de verificação relevantes para as mudanças>

## Outras informações
<número de ticket do Jira, contexto técnico adicional, ou outras informações relevantes>
```

## Condições de Parada
- `done`: PR criada ou atualizada com URL retornada.
- `needs_input`: base branch não inferível ou branch sem commits ahead.
- `blocked`: `gh` CLI não autenticado ou branch não encontrada no remote.

## Formato de Saída
```
PR <criada|atualizada>: <URL>

Título: <tipo>(<scope>): <descrição>
Base: <base-branch>
Commits: <N> commits analisados
```

## Tratamento de Erros
- Se `gh` não estiver autenticado, informe o comando de login: `gh auth login`.
- Se a branch não tiver commits ahead da base, retorne `needs_input` com diagnóstico.
- Se `gh pr create` falhar por branch policy, informe a regra violada e sugira correção.
