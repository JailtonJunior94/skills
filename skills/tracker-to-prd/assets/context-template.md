# Contexto da US para PRD: <slug-da-feature>

## Origem
- Ferramenta: <Jira | Azure DevOps>
- Link/ID: <URL canônica ou issue key>
- Tipo: <User Story | Product Backlog Item | Requirement | Epic>
- Epic / Parent: <título do parent ou "não informado">
- Sprint / Iteration: <valor ou "não informado">
- Area Path: <valor — apenas para Azure DevOps>
- Tags / Labels: <lista ou "não informado">

## Resumo
<summary preservado da origem>

## Descrição
<description preservada, sem reescrita>

## Critérios de Aceite
<lista de critérios; em Azure DevOps vem do campo Microsoft.VSTS.Common.AcceptanceCriteria>

## Comentários com Impacto
<apenas comentários que alterem requisito, decisão, restrição, dependência ou exceção>

## Sub-tarefas / Children
<lista com title + descrição curta; para Epic, listar até 20 children diretos>

## Dependências e Referências
<issues relacionadas, links remotos úteis, PRs/branches citados como decisão, páginas Confluence relevantes>

## Confronto com Codebase

Escopo confrontado: <caminho local | repo `owner/repo` | misto | pulado-com-justificativa>

| Requisito | Cobertura | Evidência | Conflito? |
|---|---|---|---|
| <ex.: RF-01 — Validar CPF antes de criar conta> | covered | `internal/auth/cpf.go:42` | não |
| <ex.: RF-02 — Disparar evento Kafka> | partial | `internal/events/publisher.go:88` (publisher existe, tópico ausente) | não |
| <ex.: RF-03 — Bloquear duplicidade> | conflicting | regra atual permite duplicata em `internal/account/create.go:120` | sim — decisão registrada na rodada 2 |

## Categorias do create-prd

| Categoria | Status | Evidência ou Resposta |
|---|---|---|
| 1. Problema e Objetivo | respondido | <resumo + origem> |
| 2. Persona Principal | respondido | <resumo + origem> |
| 3. Escopo Incluído | respondido | <resumo + origem> |
| 4. Escopo Excluído | respondido | <resumo + origem> |
| 5. Restrições e Conformidade | respondido | <resumo + origem> |
| 6. Critérios de Sucesso Mensuráveis | respondido | <resumo + origem> |

## Decisões das Rodadas de Clarificação
<append da síntese de cada rodada; rodadas detalhadas ficam em `.specs/prd-<slug>/clarifications.md`>

## Lacunas Observadas
<campos ausentes, contexto não disponível ou pontos deixados em aberto para o create-prd refinar>

## Próximo Passo
> Use a skill `create-prd` para definir a feature a partir de `.specs/prd-<slug>/context.md`.
