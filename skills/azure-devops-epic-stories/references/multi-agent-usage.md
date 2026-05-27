# Uso Multi-Agente da Skill

Esta skill é nativa no Claude Code. Em Codex CLI e Gemini CLI, o servidor MCP do Azure DevOps funciona, mas o naming das ferramentas difere. Este documento mapeia as operações.

## Operações Genéricas vs Nomes de Ferramenta MCP

| Operação Lógica                        | Claude Code                                          | Codex CLI                                | Gemini CLI                               |
|----------------------------------------|------------------------------------------------------|------------------------------------------|------------------------------------------|
| Listar projetos                        | `mcp__azure-devops__core_list_projects`              | `azure-devops.core_list_projects`        | `azure-devops__core_list_projects`       |
| Listar times do projeto                | `mcp__azure-devops__core_list_project_teams`         | `azure-devops.core_list_project_teams`   | `azure-devops__core_list_project_teams`  |
| Tipos de work item do projeto          | `mcp__azure-devops__wit_get_work_item_type`          | `azure-devops.wit_get_work_item_type`    | `azure-devops__wit_get_work_item_type`   |
| Criar work item                        | `mcp__azure-devops__wit_create_work_item`            | `azure-devops.wit_create_work_item`      | `azure-devops__wit_create_work_item`     |
| Vincular work items                    | `mcp__azure-devops__wit_work_items_link`             | `azure-devops.wit_work_items_link`       | `azure-devops__wit_work_items_link`      |
| Query WIQL                             | `mcp__azure-devops__wit_query_by_wiql`               | `azure-devops.wit_query_by_wiql`         | `azure-devops__wit_query_by_wiql`        |

Os naming acima são exemplos. Cada agente pode aplicar uma convenção própria conforme a versão da CLI. Validar a forma exata na configuração local do MCP.

## Como Cada Agente Descobre a Skill

### Claude Code
- Caminho: `~/.claude/skills/azure-devops-epic-stories/` (global) ou `.claude/skills/azure-devops-epic-stories/` (projeto).
- Descoberta automática via frontmatter `name` e `description`.

### Codex CLI
- Sem auto-discovery de skills. O usuário cria um `AGENTS.md` na raiz do repositório apontando para o SKILL.md desta skill com instrução do tipo:
  > "Para criar épico e user stories no Azure DevOps, seguir as instruções em `<caminho>/azure-devops-epic-stories/SKILL.md` substituindo nomes de ferramentas MCP conforme `references/multi-agent-usage.md`."

### Gemini CLI
- Sem auto-discovery. O usuário cria um `GEMINI.md` (ou `.gemini/context.md`) com o mesmo apontamento descrito acima para Codex.

## Substituição de Nomes de Ferramenta

A skill descreve as operações como "o equivalente MCP de `wit_create_work_item`". O agente substitui pelo nome exato do MCP no ambiente em uso.

Se a ferramenta com o naming esperado não existir, o agente pesquisa por uma equivalente usando o sufixo (`wit_create_work_item`) como termo de busca antes de encerrar com `blocked`.

## Limitações Conhecidas

- `AskUserQuestion` é um tool específico do Claude Code. Em Codex/Gemini, o agente apresenta as opções em prosa numerada e aguarda a resposta do usuário.
- Audit log JSON em `discoveries/epic-<slug>/audit-<timestamp>.json` funciona igual em qualquer agente que tenha permissão de escrita em arquivo local.
- O contrato do bundle (`bundle.json` versão 1) é o mesmo entre os três agentes, garantindo portabilidade da discovery → publicação.
