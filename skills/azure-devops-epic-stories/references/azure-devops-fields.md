# Campos do Azure DevOps para Epic e Child Item

Referência consultada quando o MCP rejeitar um payload por campo obrigatório ausente ou formato inválido. Para o mapeamento de tipos por processo, ver `ado-process-types.md`. Para os nomes de ferramenta MCP por agente, ver `multi-agent-usage.md`.

## Campos Padrão para Epic
- `System.Title` (obrigatório) — espelha `bundle.epic.title`.
- `System.Description` (obrigatório) — conteúdo de `epic.md` (preservar markdown; converter para HTML somente se o MCP exigir).
- `System.AreaPath` — derivado do `board` configurado ou de `default_area_path` em `.ado-epic-stories.yml`.
- `System.IterationPath` — opcional na criação; usar `default_iteration_path` quando definido.
- `System.Tags` — opcional, separar por `;`.
- `Microsoft.VSTS.Common.BusinessValue` — número inteiro, opcional.
- `Microsoft.VSTS.Scheduling.TargetDate` — data ISO 8601 quando o épico tem prazo de release definido na seção `## Releases / Marcos`.

## Campos Padrão para Child (User Story / Product Backlog Item / Requirement)
- `System.Title` (obrigatório) — espelha o título da US no bundle.
- `System.Description` (obrigatório) — conteúdo do arquivo de US até a seção `## Critérios de Aceite` (exclusive), preservando markdown.
- `Microsoft.VSTS.Common.AcceptanceCriteria` (obrigatório na maioria dos projetos) — extraído da seção `## Critérios de Aceite` da US. Manter Gherkin (Dado/Quando/Então) intacto.
- `System.AreaPath` — igual ao do épico.
- `System.IterationPath` — opcional na criação. Em times pequenos (2 a 4 pessoas), normalmente fica no backlog. Em times maiores, perguntar se deve alocar no iteration atual.
- `Microsoft.VSTS.Scheduling.StoryPoints` — opcional. Não inferir, deixar em branco se a discovery não capturou.

## Relacionamento Parent → Epic
- `linkType` único e obrigatório: `System.LinkTypes.Hierarchy-Reverse` (a US/PBI/Requirement aponta para o Epic como Parent).
- Não usar `Hierarchy-Forward` nesta skill para evitar duplicação de links em re-execuções.

## Tratamento de Campos Customizados Obrigatórios
1. Quando a criação falha por campo obrigatório `customfield_*` ou `<Process>.<Field>`, ler o metadado do tipo no projeto.
2. Para cada campo obrigatório sem default seguro:
   - Se `allowedValues` está definido, perguntar ao usuário em `AskUserQuestion` (ou equivalente) entre os valores válidos.
   - Se for texto livre, perguntar diretamente.
3. Reaproveitar valor do bundle quando houver correspondência semântica (ex.: `Risk` ← seção `## Riscos`, `Severity` ← criticidade discutida na discovery).
4. Se nenhum valor puder ser inferido com segurança, encerrar com `needs_input`.

## Boas Práticas de Criação
- Enviar `System.Description` e `AcceptanceCriteria` já preenchidos na criação. Nunca criar work item vazio para editar depois.
- Não vincular child ao épico antes da criação do épico — `epicId` precisa existir e estar persistido.
- Em falha parcial, **não reverter** itens já criados. Audit log captura a falha e permite reconciliação.
- Para times de 2 a 10 pessoas, evitar campos como `Priority`/`Severity` opcionais — deixe a equipe priorizar no board após criação.

## Encoding de Descrição
- Markdown geralmente é aceito em projetos com a opção "Markdown" habilitada para campos rich-text.
- Quando o MCP rejeitar markdown com erro de formato, converter os blocos `##` para `<h2>`, `**` para `<b>`, listas para `<ul><li>` e quebras de linha para `<br/>`. Manter o restante como texto plano.
- Não converter conteúdo de `## Critérios de Aceite` quando ele já estiver indo para o campo dedicado `AcceptanceCriteria`.
