# Regras de Contexto Azure DevOps

## Fonte de Verdade
- Tratar o work item alvo (User Story, Product Backlog Item ou Requirement) como fonte de verdade.
- Quando a entrada for um Epic, tratar o Epic como fonte de verdade e cada child item como contexto funcional adicional.
- Comentários, links relacionados, Parent e Children apenas complementam, esclarecem ou registram exceções.
- Não promover contexto secundário a requisito central sem evidência textual no work item ou em comentário.

## Campos Obrigatórios a Extrair
- `System.Title`
- `System.Description`
- `System.WorkItemType`
- `System.State`
- `Microsoft.VSTS.Common.AcceptanceCriteria` (quando preenchido)
- `System.Tags`
- `System.AreaPath`
- `System.IterationPath`
- `System.Parent` (id do parent quando existir)

## Relações a Explorar
- Parent (`System.LinkTypes.Hierarchy-Reverse`): ler o work item pai uma vez para entender o épico ou feature em volta.
- Children (`System.LinkTypes.Hierarchy-Forward`): listar via `wit_query_by_wiql` quando a entrada for um Epic. Limitar a 20 children diretos por execução.
- Related (`System.LinkTypes.Related`): ler apenas títulos e estado, não puxar descrição completa de cada um.
- Hyperlink, Pull Request, Branch, Commit: incluir somente quando aparecem em comentários como justificativa de decisão.

## Critérios de Inclusão
- Incluir comentários que alterem requisito, escopo, regra de negócio, prioridade técnica, dependência ou exceção.
- Incluir tags que sinalizem compliance, risco, segmento de cliente ou rollout.
- Incluir links de PR/branch citados em comentários quando explicarem decisão.
- Incluir conteúdo do Parent (Epic ou Feature) quando ele acrescentar objetivo, persona ou métrica não declarada na US.

## Critérios de Exclusão
- Ignorar revisões mecânicas (state changes, troca de assignee, mudança de área).
- Ignorar comentários puramente operacionais (links de daily, agendamento, lembretes de status).
- Ignorar discussões de board e referências a sprint sem impacto funcional.
- Ignorar atalhos para painéis, dashboards ou backlogs sem evidência de requisito.

## Consolidação
- Preservar termos de negócio, nomes próprios, siglas, IDs internos e regras exatamente como aparecem na origem.
- Registrar ausência de campos opcionais em `Lacunas Observadas` em vez de inferir.
- Preferir bloco curto e fiel a um dump cru do JSON do work item.
- Sempre incluir a URL canônica do work item: `https://dev.azure.com/<org>/<project>/_workitems/edit/<id>`.
