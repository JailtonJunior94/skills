---
name: tracker-to-prd
description: |
  Lê uma User Story ou Épico do Jira (MCP Atlassian) ou Azure DevOps (MCP azure-devops),
  confronta os requisitos com o codebase informado pelo usuário (caminho local ou repositório
  remoto via gh), conduz rodadas ilimitadas de clarificação até cobrir as seis categorias
  exigidas pela skill create-prd (problema, persona, escopo incluído, escopo excluído,
  restrições e métricas) e materializa um bundle de contexto em .specs/prd-<slug>/context.md
  para handoff. Declara explicitamente qual ferramenta de origem está em uso. Use quando o
  usuário informar uma issue do Jira ou um work item do Azure DevOps e pedir PRD, ou
  mencionar 'US para PRD', 'épico para PRD' ou 'história para PRD'. Não use para criar PRD
  sem origem de tracking, para apenas consultar a issue/work item sem gerar contexto para
  PRD, nem para criar work items em ferramentas externas.
---

# US (ou Épico) para PRD — Jira e Azure DevOps

<critical>Detectar a ferramenta de origem (Jira ou Azure DevOps) antes de qualquer leitura externa e declarar explicitamente qual está em uso na primeira mensagem ao usuário.</critical>
<critical>Ler integralmente a US ou o Épico antes de redigir o bundle: descrição, critérios de aceite, comentários relevantes, parent e children quando aplicável.</critical>
<critical>Confrontar cada requisito com o codebase informado e registrar status `covered | partial | absent | conflicting` na tabela do bundle.</critical>
<critical>Conduzir rodadas ilimitadas de clarificação. Encerrar somente quando as seis categorias do create-prd estiverem respondidas E não houver item `conflicting` aberto.</critical>
<critical>NÃO invocar a skill `create-prd` automaticamente. Materializar o bundle e instruir o usuário a executar `create-prd` em seguida.</critical>
<critical>Preservar fatos, decisões, restrições e dependências como aparecem na origem. Sem inferência forte.</critical>

## Entrada Obrigatória
- Identificador da US ou do Épico em um destes formatos:
  - Jira issue key no formato `PROJ-123`.
  - URL do Azure DevOps: `https://dev.azure.com/<org>/<project>/_workitems/edit/<id>`.
  - URL legacy do Azure DevOps: `https://<org>.visualstudio.com/<project>/_workitems/edit/<id>`.
  - Triplo compacto: `<org>/<project>/<id>` (Azure DevOps).
- Opcional: escopo de codebase a confrontar (caminho local ou `owner/repo` no GitHub).
- Opcional para Jira: `cloudId` do Atlassian (auto-descoberto se ausente).

## Saída
- Diretório `.specs/prd-<slug>/` contendo:
  - `context.md` — bundle consolidado para `create-prd`.
  - `clarifications.md` — append-only com cada rodada de perguntas e respostas.

## Procedimentos

**Step 1: Detectar a ferramenta de origem**
1. Executar `python3 scripts/detect-source.py "<input do usuário>"`. Capturar stdout.
2. Encerrar com `needs_input` se o script retornar código 1, citando os formatos aceitos (mensagem do próprio stderr).
3. Persistir `backend` como `jira` ou `ado`. Persistir `org`, `project`, `id` (ADO) ou `issue_key` (Jira).
4. Declarar ao usuário em uma frase: "Ferramenta de origem detectada: <Jira | Azure DevOps>."

**Step 2: Ler a fonte (Jira)**
1. Aplicável apenas quando `backend = jira`. Caso `backend = ado`, pular para Step 3.
2. Executar `python3 scripts/validate-issue-key.py "<issue-key>"`. Encerrar com `needs_input` se falhar.
3. Descobrir `cloudId` com `atlassian-getAccessibleAtlassianResources` se não informado. Encerrar com `blocked` se nenhum recurso Jira válido.
4. Ler a issue principal via `atlassian-getJiraIssue`. Extrair `summary`, `description`, `status`, `priority`, `labels`, `reporter`, `assignee`, `epic link`, `sprint`, `Acceptance Criteria` e campos customizados não vazios que alterem escopo, regra ou critério de aceite. Ler comentários.
5. Coletar sub-tarefas via `atlassian-searchJiraIssuesUsingJql` com `parent = <issue-key>`.
6. Obter links via `atlassian-getJiraIssueRemoteIssueLinks` e campos de link da issue.
7. Ler `references/jira-context-rules.md` para decidir o que incluir.
8. Se a entrada for um Epic Jira, listar US filhas via `atlassian-searchJiraIssuesUsingJql` com `"Epic Link" = <issue-key>`.
9. Encerrar com `blocked` se a issue não existir ou estiver inacessível.

**Step 3: Ler a fonte (Azure DevOps)**
1. Aplicável apenas quando `backend = ado`. Caso `backend = jira`, pular para Step 4.
2. Ler o work item via `mcp__azure-devops__wit_get_work_item` com `project=<project>`, `id=<id>` e `fields=System.Title,System.Description,System.WorkItemType,System.State,Microsoft.VSTS.Common.AcceptanceCriteria,System.Tags,System.AreaPath,System.IterationPath,System.Parent`.
3. Ler comentários via `mcp__azure-devops__wit_list_work_item_comments`.
4. Se `System.Parent` estiver presente, ler o parent uma única vez via `mcp__azure-devops__wit_get_work_item` para entender o Epic/Feature em volta. Não recursar além desse nível.
5. Se o tipo retornado for `Epic`, listar children diretos via `mcp__azure-devops__wit_query_by_wiql` com WIQL `SELECT [System.Id], [System.Title] FROM WorkItemLinks WHERE [Source].[System.Id] = <id> AND [System.Links.LinkType] = 'System.LinkTypes.Hierarchy-Forward' MODE (Recursive)` limitado a 20 resultados. Para cada child relevante, ler Title e Description.
6. Ler `references/ado-context-rules.md` para decidir inclusão.
7. Compor a URL canônica do work item para o bundle: `https://dev.azure.com/<org>/<project>/_workitems/edit/<id>`.
8. Encerrar com `blocked` se o MCP não responder após uma tentativa de recuperação, ou se o work item não existir.

**Step 4: Coletar escopo de codebase**
1. Perguntar via `AskUserQuestion` (multiSelect=true) o escopo de confronto: "Caminho local", "Repo remoto via gh (informe `owner/repo`)", "Pular confronto (não recomendado)".
2. Para "Caminho local", pedir o path se não informado. Default aceito: `cwd` (`.`).
3. Para "Repo remoto", pedir `owner/repo`. Validar com `gh repo view <owner>/<repo> --json name -q .name`.
4. Para "Pular", exigir justificativa textual e registrar em `Lacunas Observadas`.

**Step 5: Confrontar requisitos com o codebase**
1. Ler `references/codebase-confrontation.md`.
2. Extrair lista preliminar de requisitos da Description, Acceptance Criteria e comentários incluídos. Numerar internamente como `R1, R2, ...` (sem RF- ainda; create-prd numera depois).
3. Para cada requisito, derivar até 3 termos buscáveis e executar buscas:
   - Local: `Grep` com `output_mode=files_with_matches` ou `content`.
   - Remoto: `gh search code "<termo> repo:<owner>/<repo>" --limit 10` ou `gh api repos/<owner>/<repo>/contents/<path>` quando o path é conhecido.
4. Respeitar o limite de 15 chamadas por rodada. Registrar `status` por requisito e até 2 evidências (`path:linha` ou URL).
5. Salvar a tabela de confronto em memória; será serializada no bundle no Step 7.

**Step 6: Rodadas de clarificação**
1. Ler `references/clarification-checklist.md`.
2. Marcar cada uma das 6 categorias como `respondido` quando a US/Épico já contém evidência textual suficiente. Caso contrário, gerar pergunta de múltipla escolha da rodada atual.
3. Cada item `conflicting` da tabela de confronto vira uma pergunta na próxima rodada com opções: "Ajustar requisito", "Tratar em outra US", "Aceitar incompatibilidade explícita".
4. Limitar cada chamada `AskUserQuestion` a no máximo 4 perguntas.
5. Após coletar respostas, atualizar a tabela de categorias e a tabela de confronto. Anexar bloco `## Rodada <n>` em `.specs/prd-<slug>/clarifications.md`.
6. **Critério de parada**: encerrar as rodadas quando todas as 6 categorias estiverem `respondido` E nenhum item permanecer em `conflicting` sem decisão.
7. Não há cap rígido de rodadas. Cap honesto: se a mesma categoria ficar pendente após 3 rodadas consecutivas sem progresso, encerrar com `needs_input` listando os pontos travados.

**Step 7: Materializar o bundle**
1. Derivar `slug` com `python3 scripts/slugify.py "<título da US ou Épico>"`. Capturar stdout.
2. Criar `.specs/prd-<slug>/` se não existir.
3. Ler `assets/context-template.md` e preencher TODAS as seções com base no que foi coletado nos passos 2-6. Não inventar conteúdo ausente; deixar em `Lacunas Observadas`.
4. Escrever em `.specs/prd-<slug>/context.md`.
5. Garantir que `clarifications.md` contém todas as rodadas (append-only).

**Step 8: Handoff explícito**
1. NÃO invocar `create-prd` diretamente.
2. Exibir ao usuário:
   - Caminho do bundle: `.specs/prd-<slug>/context.md`.
   - Resumo em 3 a 5 linhas (ferramenta de origem, escopo, número de rodadas, conflitos pendentes).
   - Instrução literal: `Use a skill create-prd para definir a feature a partir de .specs/prd-<slug>/context.md`.
3. Encerrar com `done`.

## Decisões Operacionais
1. Ler a fonte completa antes de resumir qualquer parte. Sem leitura parcial.
2. Tratar o work item alvo (US ou Epic) como fonte de verdade. Comentários, parent e children apenas complementam.
3. Preferir ausência explícita em `Lacunas Observadas` a inferência fraca.
4. Preservar termos de negócio, nomes próprios, siglas, IDs e regras exatamente como aparecem na origem.
5. Confronto de codebase é determinístico (busca textual). Sem heurística de similaridade fuzzy.
6. Bundle é fiel e curto. Nada de dump cru de JSON ou HTML do work item.

## Estados Finais
- `done`: bundle gerado em `.specs/prd-<slug>/context.md`, instrução de handoff exibida.
- `needs_input`: input ausente/inválido; ou pendência travada na mesma categoria após 3 rodadas sem progresso; ou `Outro` vazio repetido em pergunta de clarificação.
- `blocked`: MCP indisponível, issue/work item inexistente, sem acesso ao backend, ou repo remoto inacessível.
- `failed`: erro repetido em escrita do bundle após uma tentativa de recuperação.

## Tratamento de Erros
- Se `scripts/detect-source.py` falhar, exibir formatos aceitos e encerrar com `needs_input`.
- Se `scripts/validate-issue-key.py` rejeitar a key, informar o formato `PROJ-123`.
- Se o MCP Atlassian ou Azure DevOps não responder, tentar uma vez. Persistindo a falha, encerrar com `blocked` indicando verificação do MCP no agente.
- Se `gh` não estiver autenticado ao consultar repo remoto, encerrar com `blocked` orientando `gh auth status`.
- Se o usuário responder `Outro` com texto vazio em qualquer rodada, repetir a pergunta uma vez antes de encerrar com `needs_input`.
- Se o limite de 15 buscas por rodada for atingido com requisitos restantes, registrar os requisitos não cobertos como `absent` com nota explícita e seguir para clarificação.
- Se o agente em uso nomear as ferramentas MCP do Azure DevOps de forma diferente das esperadas, mapear pelo sufixo (`wit_get_work_item`, `wit_list_work_item_comments`, `wit_query_by_wiql`).
