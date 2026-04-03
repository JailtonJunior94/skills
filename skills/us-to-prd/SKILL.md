---
name: us-to-prd
description: |
  Lê uma User Story (US) completa do Jira via MCP Atlassian e inicia a criação de um PRD
  usando o fluxo definido em .claude/commands/create-prd.md.
  Use quando o usuário fornece um ID de issue do Jira e pede PRD, ou menciona "US para PRD", "história para PRD".
  Não use para criação de PRD sem referência a issue do Jira (usar create-prd diretamente)
  nem para leitura de issue sem criação de PRD.
---

# US para PRD

<critical>Ler TODO o conteúdo da US antes de chamar o command create-prd — incluindo description, comments, sub-tasks e links</critical>
<critical>Preservar fielmente o conteúdo da US — não inventar nem omitir informações</critical>
<critical>Após extrair o conteúdo, DEVE chamar o command .claude/commands/create-prd.md passando todo o contexto como entrada</critical>

## Entrada Obrigatória
- Issue key do Jira (ex: PROJ-123).
- Opcionalmente: cloudId do Atlassian (se não fornecido, será descoberto automaticamente).

## Procedimentos

**Etapa 1: Descobrir Ambiente Atlassian**
1. Se cloudId não fornecido, use `atlassian-getAccessibleAtlassianResources` para descobrir.
2. Confirme que o recurso está acessível. Se não, retorne `blocked`.

**Etapa 2: Extrair Dados Principais da US**
1. Via `atlassian-getJiraIssue`, colete:
   - Summary, Description, Status, Priority, Labels.
   - Reporter, Assignee, Epic link, Sprint.
   - Acceptance Criteria (campo customizado, se disponível).
   - Campos customizados relevantes.
2. Extraia todos os comentários da issue (expand comments) para contexto adicional.

**Etapa 3: Coletar Relações e Contexto Externo**
1. Busque sub-tarefas via `atlassian-searchJiraIssuesUsingJql` com JQL: `parent = <issue-key>`.
2. Colete summary e description de cada sub-tarefa.
3. Via `atlassian-getJiraIssueRemoteIssueLinks` e campos de links, identifique issues vinculadas e links externos.
4. Se houver links para Confluence, leia o conteúdo via `atlassian-getConfluencePage`.

**Etapa 4: Consolidar Contexto**
1. Organize todas as informações no formato estruturado:
   ```markdown
   # Contexto da US: <issue-key>

   ## Rastreabilidade
   - **Issue de Origem**: [PROJ-123](link)
   - **Tipo**: User Story
   - **Sprint/Epic**: <se disponível>
   - **Data de Extração**: <timestamp>

   ## Resumo
   <summary>

   ## Descrição Completa
   <description formatada>

   ## Critérios de Aceite
   <acceptance criteria se disponível>

   ## Comentários Relevantes
   <comentários que adicionam contexto ou requisitos>

   ## Sub-tarefas
   <lista de sub-tarefas com descrições>

   ## Issues Relacionadas
   <links e relações com outras issues>

   ## Contexto Adicional (Confluence)
   <conteúdo de páginas vinculadas, se houver>
   ```

**Etapa 5: Invocar create-prd**
1. Chame o command `.claude/commands/create-prd.md` passando todo o contexto consolidado como entrada.
2. Esta skill encerra aqui — o restante do fluxo é responsabilidade do create-prd.

## Condições de Parada
- `done`: contexto extraído e command create-prd invocado com sucesso.
- `blocked`: issue não encontrada, sem acesso ao Jira ou cloudId inválido.
- `failed`: limite de tentativas de acesso ao MCP excedido.

## Tratamento de Erros
- Se a issue não for encontrada, verifique a grafia da key e informe o formato esperado (ex: `PROJ-123`).
- Se o MCP Atlassian não responder, informe ao usuário para verificar a configuração do MCP e retorne `blocked`.
- Se campos opcionais (Acceptance Criteria, Confluence) não estiverem disponíveis, prossiga sem eles e registre a ausência no contexto consolidado.
