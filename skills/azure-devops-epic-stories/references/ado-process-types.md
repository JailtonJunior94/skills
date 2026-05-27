# Tipos de Work Item por Processo do Azure DevOps

Mapeamento determinístico entre processo do projeto e tipos de work item esperados. Usado para evitar tentativa-e-erro na criação.

## Processos Padrão

### Scrum
- Épico: `Epic`
- Pai intermediário: `Feature`
- Child: **`Product Backlog Item`**
- Hierarquia típica: Epic → Feature → Product Backlog Item → Task

### Agile
- Épico: `Epic`
- Pai intermediário: `Feature`
- Child: **`User Story`**
- Hierarquia típica: Epic → Feature → User Story → Task

### CMMI
- Épico: `Epic`
- Pai intermediário: `Feature`
- Child: **`Requirement`**
- Hierarquia típica: Epic → Feature → Requirement → Task

### Basic (Azure DevOps Boards Basic)
- Não suporta `Epic` nativamente. Usa `Epic` apenas com extensão. Child é `Issue`.
- Se o projeto for Basic, encerrar com `blocked` e orientar migração de processo, salvo se o usuário confirmar uso de `Issue`.

## Processos Customizados

Processos derivados (custom inheriting from Scrum/Agile/CMMI) costumam manter os nomes dos tipos. Validar sempre via listagem de tipos do projeto. Quando o nome do tipo customizado divergir, perguntar ao usuário qual usar.

## Estratégia de Detecção

1. Listar tipos de work item do projeto.
2. Procurar `Epic` para o nível do épico. Se ausente, perguntar ao usuário entre os tipos disponíveis.
3. Procurar child na ordem: `User Story` → `Product Backlog Item` → `Requirement`. Usar o primeiro encontrado.
4. Se nenhum estiver presente, perguntar ao usuário qual tipo usar como child.

## Override Manual

O arquivo `.ado-epic-stories.yml` aceita as chaves:
- `epic_type_override` — substitui o tipo do épico.
- `child_type_override` — substitui o tipo do child.

Quando presentes, ignoram a detecção automática.

## Campos Padrão Esperados

Em todos os processos:
- `System.Title` (obrigatório).
- `System.Description` (obrigatório).
- `System.AreaPath` (necessário para alocação no board).
- `Microsoft.VSTS.Common.AcceptanceCriteria` (obrigatório em US/PBI/Requirement na maioria dos projetos).

Campos específicos do tipo (Story Points, Business Value, Risk) ficam opcionais na criação inicial.
