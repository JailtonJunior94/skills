---
name: azure-devops-epic-stories
description: Consome um bundle de descoberta produzido por epic-story-discovery e cria épico mais user stories no Azure DevOps via MCP oficial. Detecta automaticamente o processo do projeto (Scrum, Agile, CMMI) e os tipos válidos de work item, valida o bundle, normaliza títulos para detectar épicos duplicados de forma determinística, vincula as US ao épico pelo link Parent e gera audit log em PT-BR. Lê configuração opcional .ado-epic-stories.yml na raiz do repositório para defaults de organização, projeto, board e processo. Use quando o usuário pedir para publicar um bundle de discovery no Azure DevOps, criar épico e user stories no ADO ou sincronizar artefatos locais com o backlog. Não use para criar tasks técnicas, editar work items existentes, criar em outras ferramentas ou rodar discovery do zero.
---

# Publicação de Épico e User Stories no Azure DevOps

<critical>O bundle de entrada DEVE ter sido produzido por `epic-story-discovery` e validado por `scripts/validate-bundle.py` antes de qualquer chamada MCP.</critical>
<critical>Organização, projeto e board são obrigatórios. Encerrar com `needs_input` se ausentes após verificar `.ado-epic-stories.yml` e perguntar ao usuário.</critical>
<critical>Detectar o processo do projeto (Scrum, Agile, CMMI) antes de criar work items. Não assumir `User Story` sem confirmação.</critical>
<critical>Detectar duplicata de épico de forma determinística via título normalizado. Sem heurísticas de "X% similar".</critical>
<critical>Toda US criada DEVE ficar atrelada ao épico via `System.LinkTypes.Hierarchy-Reverse` (Parent). Direção única, sem variação por execução.</critical>
<critical>Limite máximo de 10 US por execução. Acima disso, dividir em lotes e confirmar com o usuário a cada lote.</critical>
<critical>Gerar audit log em `./discoveries/epic-<slug>/audit-<timestamp>.json` ao final, independente do resultado.</critical>

## Entrada Obrigatória
- Caminho do bundle local: `./discoveries/epic-<slug>/`.
- Triplo `organização` + `projeto` + `board` (Area Path / Team), via arquivo de config ou pergunta interativa.

## Procedimentos

**Step 1: Resolver configuração de destino**
1. Procurar `.ado-epic-stories.yml` na raiz do repositório (cwd e até 3 níveis acima).
2. Executar `python3 scripts/load-ado-config.py` para carregar defaults caso o arquivo exista.
3. Mesclar com o que o usuário informou na mensagem inicial (mensagem do usuário tem prioridade sobre o arquivo).
4. Para cada campo ainda ausente (`organization`, `project`, `board`), perguntar em `AskUserQuestion` com header curto (`Organização`, `Projeto`, `Board`).
5. Encerrar com `needs_input` se algum permanecer indefinido após uma rodada de perguntas.

**Step 2: Validar acesso e bundle**
1. Localizar o bundle. Se o usuário não informou caminho, listar diretórios em `./discoveries/epic-*` e perguntar em múltipla escolha.
2. Executar `python3 scripts/validate-bundle.py <caminho-do-bundle>`. Encerrar com `blocked` se falhar.
3. Listar projetos com o equivalente MCP de `core_list_projects` para a organização configurada. Confirmar que `project` existe na listagem.
4. Listar times do projeto com o equivalente MCP de `core_list_project_teams`. Confirmar que `board` mapeia para Area Path válido.

**Step 3: Detectar processo do projeto e tipos de work item**
1. Ler `references/ado-process-types.md` para entender mapeamento processo → tipos.
2. Listar tipos de work item válidos no projeto com o equivalente MCP de `wit_get_work_item_type`.
3. Identificar o tipo de épico (`Epic` em Scrum/Agile/CMMI).
4. Identificar o tipo de child item:
   - `User Story` em projetos Agile.
   - `Product Backlog Item` em projetos Scrum.
   - `Requirement` em projetos CMMI.
5. Se nenhum tipo conhecido for encontrado, perguntar em `AskUserQuestion` qual usar entre os disponíveis. Encerrar com `blocked` se nenhuma opção for selecionada.
6. Persistir `epicType` e `childType` para os passos seguintes.

**Step 4: Detectar épico duplicado de forma determinística**
1. Ler `bundle.json` e extrair `epic.title`.
2. Executar `python3 scripts/normalize-title.py "<título>"` para obter título normalizado (lowercase, sem acentos, tokens stop-words removidas).
3. Ler `references/wiql-duplicate-detection.md` para construir a query WIQL.
4. Executar a query via o equivalente MCP de `wit_query_by_wiql` filtrando por `WorkItemType = '<epicType>'`, `State <> 'Closed'`, e `[System.Title] CONTAINS <token-mais-distintivo>`.
5. Comparar o título normalizado do bundle com o título normalizado de cada épico retornado.
6. Se houver match exato (igualdade após normalização), perguntar em `AskUserQuestion` se deve "Reutilizar épico existente", "Criar novo épico mesmo assim" ou "Cancelar".
7. Persistir `epicId` (existente ou pendente de criação).

**Step 5: Confirmar plano de criação**
1. Apresentar ao usuário um resumo: organização, projeto, board, `epicType`, `childType`, título do épico, decisão sobre duplicata, número de US a criar.
2. Se número de US > 10, dividir em lotes de 10 e apresentar o plano de lotes.
3. Perguntar em `AskUserQuestion`: "Executar criação agora", "Apenas exibir payload (dry-run)", "Refinar bundle antes" ou "Cancelar".
4. Em dry-run, montar os payloads e exibir cada um sem chamar criação. Encerrar com `done`.
5. Em refinar, orientar o usuário a rodar `epic-story-discovery` novamente. Encerrar com `done`.
6. Em cancelar, encerrar com `done` sem criação.

**Step 6: Criar (ou reutilizar) o épico**
1. Se `epicId` está marcado como pendente, montar payload do épico:
   - `workItemType = epicType`
   - `title = bundle.epic.title`
   - `description = conteúdo de epic.md` (preservar markdown; converter para HTML somente se o MCP exigir).
   - `areaPath = board configurado`.
2. Ler `references/azure-devops-fields.md` para confirmar campos obrigatórios do projeto.
3. Criar via o equivalente MCP de `wit_create_work_item` e capturar o `id` retornado em `epicId`.
4. Se a criação falhar por campo obrigatório customizado, ler o metadado do tipo, perguntar valores em `AskUserQuestion` apenas para campos sem inferência segura, reconstruir payload e tentar uma vez.

**Step 7: Criar User Stories e vincular ao épico**
1. Para cada US no `bundle.json` (até o limite do lote atual):
   - Ler `us/<num>_<slug>.md`.
   - Montar payload: `workItemType = childType`, `title`, `description` (conteúdo do arquivo), `areaPath` igual ao do épico, e `Microsoft.VSTS.Common.AcceptanceCriteria` extraído da seção `## Critérios de Aceite`.
   - Criar via o equivalente MCP de `wit_create_work_item`. Capturar `id`.
   - Vincular ao épico via o equivalente MCP de `wit_work_items_link` com `linkType = System.LinkTypes.Hierarchy-Reverse` (a US recebe o épico como Parent).
   - Registrar resultado por US em estrutura local (`id`, `status`, `link_status`).
2. Não paralelizar. Criar em série para preservar rastreabilidade de falhas.
3. Em falha de uma US, registrar e seguir para a próxima. Não reverter o que já foi criado.
4. Em falha de vínculo, não recriar a US. Registrar `link_status = failed` e seguir.

**Step 8: Gerar audit log**
1. Executar lógica de audit log conforme `assets/audit-log.schema.json`.
2. Escrever em `./discoveries/epic-<slug>/audit-<UTC-timestamp>.json` contendo:
   - Timestamp UTC ISO 8601.
   - Configuração efetiva (org, projeto, board, epicType, childType).
   - `epicId` final + URL (se MCP retornar).
   - Lista de US criadas com `local_id`, `ado_id`, `link_status`, `error` (quando aplicável).
   - Lotes executados quando houve divisão.
3. O audit log persiste mesmo em falhas parciais ou totais para reconciliação posterior.

**Step 9: Relatar resultado**
1. Exibir o caminho do audit log.
2. Listar `epicId` e cada US criada com `ado_id` e status de link.
3. Separar criados com sucesso de falhas.
4. Em caso de lote pendente (>10 US), perguntar se deve continuar com o próximo lote.

## Decisões Operacionais
1. Preferir abortar criação a publicar work item com tipo, parent ou campos obrigatórios incorretos.
2. Preservar a terminologia do bundle. Não traduzir títulos nem reescrever descrição.
3. Tratar `.ado-epic-stories.yml` como fonte autoritativa de defaults. Não sobrescrever sem aprovação do usuário.
4. Manter `Hierarchy-Reverse` como direção única do link Parent. Nunca alternar.
5. Limitar a 10 US por execução para evitar throttle no ADO e perda de rastreabilidade.

## Estados Finais
- `done`: épico e US criados, vinculados e audit log emitido. Inclui dry-run completo.
- `needs_input`: organização, projeto, board ou tipo de child sem definição segura.
- `blocked`: MCP indisponível, projeto inexistente, área inválida, bundle reprovado em validação.
- `failed`: erro repetido na criação após uma rodada de reconstrução de payload.

## Tratamento de Erros
- Se `validate-bundle.py` falhar, orientar o usuário a rodar `epic-story-discovery` para corrigir e reabrir.
- Se a equivalente MCP de `core_list_projects` falhar, encerrar com `blocked` indicando verificação do MCP do Azure DevOps no agente.
- Se o projeto não constar na listagem, mostrar os projetos disponíveis e encerrar com `needs_input`.
- Se nenhum tipo de child compatível existir (`User Story`, `Product Backlog Item`, `Requirement`), listar tipos do projeto e perguntar qual usar.
- Se `wit_create_work_item` rejeitar campo obrigatório customizado, ler metadado do tipo, resolver com `AskUserQuestion` apenas o que faltar, reconstruir payload e tentar uma vez.
- Se `wit_work_items_link` falhar, registrar `link_status = failed` e seguir. Audit log captura.
- Se o agente em uso (Codex, Gemini, outro) nomear as ferramentas MCP de forma diferente das esperadas pelo Claude Code, ler `references/multi-agent-usage.md` para mapeamento.
