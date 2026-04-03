---
name: jira-tasks
description: |
  Cria tasks no Jira abaixo de uma User Story (US) com base nos arquivos de decomposição
  gerados pelo command create-tasks. Estima horas como dev senior e atribui ao criador.
  Use quando o usuário pede para criar tasks no Jira a partir de uma US, decompor US em tasks no Jira,
  menciona "criar tasks", "tasks no Jira" ou referencia tasks.md para sincronizar com Jira.
  Não use para decomposição local sem Jira (usar create-tasks), leitura de issue (usar us-to-prd)
  ou criação de PRD (usar create-prd ou us-to-prd).
---

# Criação de Tasks no Jira

<critical>Toda task DEVE ser filha da US informada (campo parent)</critical>
<critical>Toda task DEVE ter título no formato: [Backend] Descrição da task</critical>
<critical>Toda task DEVE ter Original Estimate em horas (campo timetracking.originalEstimate)</critical>
<critical>Toda task DEVE ser atribuída ao usuário que está criando (assignee_account_id)</critical>
<critical>Estimar como dev senior conservador — incluir margem para code review, testes e edge cases</critical>
<critical>Descobrir e preencher campos obrigatórios customizados ANTES de criar tasks (ex: Plataforma)</critical>
<critical>Os arquivos de tasks (tasks.md + [num]_task.md) são a FONTE DE VERDADE para criação no Jira</critical>

## Entrada Obrigatória
- Issue key da US no Jira (ex: PROJ-123).
- Arquivos de tasks gerados pelo command create-tasks:
  - `./tasks/prd-[nome-da-feature]/tasks.md` — índice com lista de tasks.
  - `./tasks/prd-[nome-da-feature]/[num]_task.md` — detalhamento de cada task.
- Opcionalmente: cloudId do Atlassian (se não fornecido, será descoberto automaticamente).

## Procedimentos

**Etapa 1: Descoberta do Ambiente Atlassian (paralelo)**
1. Execute em paralelo:
   - `atlassian-getAccessibleAtlassianResources` → cloudId.
   - `atlassian-atlassianUserInfo` → account_id para assignee.
   - Leia `tasks.md` e todos os `[num]_task.md` do diretório de tasks.
2. Se os arquivos de tasks não existirem, informe: "Execute primeiro o command create-tasks para gerar a decomposição local." Retorne `blocked`.

**Etapa 2: Ler e Validar Arquivos de Tasks**
1. Localize os arquivos:
   - Se o usuário informou o nome da feature, busque em `./tasks/prd-[nome-da-feature]/tasks.md`.
   - Caso contrário, liste os diretórios `./tasks/prd-*/` e solicite escolha.
2. Leia o índice (`tasks.md`): extraia lista completa de tasks com títulos, status e dependências.
3. Leia cada task detalhada (`[num]_task.md`): extraia Visão Geral, Requisitos, Subtarefas, Critérios de Sucesso e Testes.

**Etapa 3: Ler US no Jira**
1. Via `atlassian-getJiraIssue`, colete: Summary, Description, Status, Priority, Labels e Project Key.

**Etapa 4: Identificar Tipo de Issue e Campos Obrigatórios**
1. Use `atlassian-getJiraProjectIssueTypesMetadata` para listar tipos disponíveis.
2. Identifique o tipo correto para sub-tarefas (prioridade: Sub-task / Task > Sub-task > Subtask > Sub-tarefa).
3. Use `atlassian-getJiraIssueTypeMetaWithFields` com o issueTypeId para descobrir campos obrigatórios (`required: true`).
4. Para cada campo obrigatório customizado (`customfield_*`):
   - Extraia `allowedValues`.
   - Selecione o valor mais adequado ao contexto.
   - Guarde como `{"customfield_XXXXX": {"id": "<value_id>"}}`.

**Etapa 5: Criar Tasks no Jira (em lote)**
1. Para cada task, use `atlassian-createJiraIssue` com TODOS os campos numa única chamada:
   - `projectKey`: mesmo projeto da US.
   - `issueTypeName`: tipo identificado na Etapa 4.
   - `summary`: `[Backend] <Título descritivo>`.
   - `description`: conteúdo extraído do `[num]_task.md` em markdown.
   - `parent`: issue key da US.
   - `contentFormat`: `markdown`.
   - `assignee_account_id`: account_id do usuário atual.
   - `additional_fields`: campos extras incluindo `timetracking` e custom fields.
2. Crie TODAS as tasks em paralelo para eficiência.

<critical>NÃO usar editJiraIssue após criação — incluir assignee, timetracking e custom fields direto no createJiraIssue</critical>

**Etapa 6: Gerar Relatório**
1. Apresente resumo ao usuário com tabela de tasks criadas.

## Regras de Nomenclatura do Título
```
[Backend] <Componente>: <Ação descritiva da task>
```
Exemplos:
- `[Backend] Config: Adicionar env var CRYPTO_REWARD_REFUND_LOOKBACK_DAYS`
- `[Backend] Repository: Implementar HasUnreversedCryptoReward`
- `[Backend] Service: Branch heurístico no ApplyCryptoRewardRefundService`

## Regras para Descrição da Task
Extraia diretamente do arquivo `[num]_task.md` as seções: Visão Geral, Requisitos, Subtarefas, Critérios de Sucesso, Dependências e Arquivos Relevantes.

<critical>Usar o conteúdo real dos task files — NÃO inventar ou resumir excessivamente</critical>

## Regras de Estimativa (dev senior conservador)
- Task simples (CRUD, config, ajuste pontual): 2h–4h.
- Task média (lógica de negócio, integração simples): 4h–8h.
- Task complexa (algoritmo, múltiplas integrações, testes E2E): 8h–16h.
- Máximo absoluto por task: 16h. Se ultrapassar, divida em sub-tasks.
- Sempre inclua tempo para: testes unitários, code review, edge cases.

## Condições de Parada
- `done`: todas as tasks criadas no Jira com estimativa e assignee.
- `needs_input`: aguardando esclarecimento do usuário.
- `blocked`: sem acesso ao Jira, projeto não encontrado, tipo de issue inválido ou arquivos de tasks ausentes.
- `failed`: erro na criação de alguma task após 3 tentativas.

## Formato de Saída
```markdown
✅ **Tasks criadas com sucesso** como subtasks de [<issue-key>](<url>)

| # | Key | Título | Estimativa |
|---|-----|--------|------------|
| 1 | [PROJ-456](<url>) | [Backend] Descrição | 4h |
| 2 | [PROJ-457](<url>) | [Backend] Descrição | 8h |

**Total estimado:** Xh · Assignee: <nome> · Plataforma: Backend
```

## Tratamento de Erros
- Se a criação falhar por campo obrigatório faltando, use `getJiraIssueTypeMetaWithFields` para descobrir o campo e seus valores permitidos, e refaça a criação.
- Se uma task falhar, informe ao usuário quais foram criadas e quais falharam — não reverta tasks já criadas.
- Se o campo `timetracking` não estiver disponível, informe e continue sem estimativa.
