---
name: epic-story-discovery
description: Conduz descoberta estruturada de épico e user stories para qualquer destino (Azure DevOps, Jira, GitHub Issues, PRD local). Executa pelo menos duas rodadas obrigatórias de perguntas em múltipla escolha cobrindo escopo, personas, KPIs, trade-offs, edge cases, dependências e rollout. Produz um bundle local em PT-BR em discoveries/epic-<slug>/ com épico e user stories preenchidos seguindo templates oficiais, validados por script determinístico sem falso positivo. Use quando o usuário pedir para refinar uma feature, descrever um épico, planejar user stories ou preparar artefatos para criar work items em qualquer ferramenta. Não use para criar work items diretamente em ferramentas externas, editar bundles já consolidados ou apenas gerar PRD sem épico/US.
---

# Descoberta de Épico e User Stories

<critical>Todos os artefatos DEVEM ser escritos em PT-BR.</critical>
<critical>Executar no mínimo DUAS rodadas de clarificação em múltipla escolha antes de materializar qualquer arquivo do bundle. Rodadas adicionais são obrigatórias enquanto houver ambiguidade material em escopo, KPIs ou edge cases críticos.</critical>
<critical>A Rodada 2 DEVE cobrir explicitamente trade-offs e edge cases.</critical>
<critical>O épico DEVE seguir `assets/epic-template.md` e cada US DEVE seguir `assets/user-story-template.md` integralmente.</critical>
<critical>Nenhuma seção crítica pode ser materializada com placeholder não resolvido. Ler `references/content-quality-rules.md` antes de gerar arquivos.</critical>
<critical>O bundle só é considerado pronto quando `scripts/validate-bundle.py` retornar `SUCCESS`.</critical>

## Entrada Obrigatória
- Nome curto da feature (slug). Se ausente, derivar a partir do título proposto pelo usuário.
- Contexto bruto do produto/feature: problema atual, objetivo, restrições conhecidas. Aceita prosa, links ou arquivos locais.

## Saída
Bundle local em `./discoveries/epic-<slug>/`:
- `bundle.json` — índice da descoberta com metadados (slug, título, criado em, US planejadas).
- `epic.md` — épico preenchido a partir do template oficial.
- `us/<num>_<slug>.md` — uma US por arquivo, numeração `01`, `02`, ...
- `transcript.md` — registro das perguntas e respostas das rodadas para auditoria.

## Procedimentos

**Step 1: Validar entrada e inicializar bundle**
1. Identificar o slug da feature a partir do pedido do usuário. Normalizar para kebab-case com `scripts/slugify.py`.
2. Verificar se `./discoveries/epic-<slug>/` já existe. Se sim, perguntar em múltipla escolha se deve "Reaproveitar bundle existente", "Renomear novo bundle com sufixo numérico" ou "Cancelar".
3. Executar `python3 scripts/init-bundle.py <slug>` para criar a estrutura vazia (`bundle.json`, `us/`, `transcript.md`).
4. Encerrar com `blocked` se o script falhar (permissão de escrita, conflito de nome).

**Step 2: Coletar contexto bruto**
1. Pedir ao usuário um descritivo livre do problema, objetivo, personas e restrições caso ainda não tenha sido fornecido.
2. Aceitar arquivos locais, links e prosa. Não pesquisar fora do contexto fornecido.
3. Resumir em até 5 bullets o entendimento inicial e exibir ao usuário antes de iniciar as rodadas.
4. Anexar o resumo ao `transcript.md` como bloco `## Contexto Inicial`.

**Step 3: Rodada 1 de clarificação (múltipla escolha)**
1. Ler `references/clarification-rounds.md` para mapear os eixos obrigatórios da Rodada 1.
2. Formular 3 a 4 perguntas em `AskUserQuestion`, cada uma com 2 a 4 opções mutuamente exclusivas, cobrindo: objetivo macro, persona-alvo, recorte de escopo, KPI principal.
3. Cada `option.description` DEVE explicitar a implicação ou trade-off de escolher essa opção.
4. Registrar perguntas e respostas no `transcript.md` em bloco `## Rodada 1`.
5. Consolidar respostas em rascunho interno do épico antes de avançar.

**Step 4: Rodada 2 de clarificação (múltipla escolha) — trade-offs e edge cases**
1. Ler `references/clarification-rounds.md` para mapear os eixos obrigatórios da Rodada 2.
2. Formular 3 a 4 perguntas em `AskUserQuestion` cobrindo: trade-off arquitetural ou de produto, edge cases relevantes derivados do contexto, dependências externas, estratégia de rollout.
3. Para trade-offs, cada opção compara duas alternativas com custo/benefício explícito.
4. Para edge cases, cada opção descreve um cenário concreto e o usuário decide se cobre, descarta ou trata em iteração futura.
5. Registrar perguntas e respostas no `transcript.md` em bloco `## Rodada 2`.

**Step 5: Rodadas adicionais quando necessário**
1. Avaliar se persistem ambiguidades materiais em: escopo, KPIs, edge cases críticos, dependências bloqueantes.
2. Se sim, abrir Rodada 3 com perguntas focadas apenas nos pontos pendentes. Repetir até estabilizar.
3. Registrar cada rodada no `transcript.md` em bloco numerado sequencial.
4. Não materializar arquivos do bundle enquanto houver ambiguidade em seção crítica do épico ou de qualquer US.

**Step 6: Confirmar materialização**
1. Apresentar ao usuário um sumário consolidado: título do épico, escopo, fora de escopo, KPIs, baseline, lista de US planejadas (título + persona).
2. Perguntar em `AskUserQuestion` se deve "Materializar bundle agora", "Refinar mais" ou "Cancelar".
3. Encerrar com `done` sem materializar se o usuário cancelar.
4. Voltar a Step 5 se o usuário pedir refinamento.

**Step 7: Materializar o épico**
1. Ler `assets/epic-template.md`.
2. Preencher TODAS as seções com base nas respostas registradas no `transcript.md`. Não inventar dados.
3. Ler `references/content-quality-rules.md` para garantir que nenhuma seção crítica fica com placeholder proibido.
4. Escrever em `./discoveries/epic-<slug>/epic.md`.

**Step 8: Materializar cada User Story**
1. Para cada US planejada, ler `assets/user-story-template.md`.
2. Preencher integralmente: Título, Descrição Como/Quero/Para, Contexto/Regras de Negócio, Critérios de Aceite em Gherkin (no mínimo um cenário feliz, um alternativo e um de erro), Dependências, Fora de Escopo, DoD.
3. Escrever em `./discoveries/epic-<slug>/us/<num>_<slug>.md` com numeração de dois dígitos.
4. Atualizar `bundle.json` com a entrada correspondente (id local, título, arquivo).

**Step 9: Validar o bundle inteiro**
1. Executar `python3 scripts/validate-bundle.py ./discoveries/epic-<slug>`.
2. Se retornar erro, ler o stderr, identificar o arquivo e seção, corrigir e revalidar.
3. Encerrar com `blocked` se após uma rodada de correção a validação ainda falhar.

**Step 10: Relatar saída**
1. Listar o caminho do bundle, o número de US criadas e o `bundle.json` resultante.
2. Sugerir próximos passos possíveis: publicar no Azure DevOps via `azure-devops-epic-stories`, abrir PR com o bundle versionado, ou exportar para outra ferramenta.
3. Não publicar em ferramenta externa neste skill.

## Decisões Operacionais
1. Preferir encerrar com `needs_input` a materializar artefatos com seções obrigatórias incompletas.
2. Preservar a terminologia de negócio do usuário em vez de reescrever para jargão genérico.
3. Tratar Rodadas 1 e 2 como inegociáveis. Nunca colapsar em rodada única, mesmo que o usuário forneça contexto extenso.
4. Limitar cada `AskUserQuestion` a no máximo 4 perguntas por chamada.
5. Manter `transcript.md` como fonte de verdade para reconstituir as decisões em qualquer momento.

## Estados Finais
- `done`: bundle materializado e validado.
- `needs_input`: respostas de clarificação ausentes ou seção crítica incompleta.
- `blocked`: falha de I/O ao criar bundle ou erro persistente em `validate-bundle.py`.
- `failed`: erro inesperado de execução após uma tentativa de recuperação.

## Tratamento de Erros
- Se `scripts/init-bundle.py` falhar por conflito de nome, sugerir sufixo `-v2` e perguntar ao usuário antes de prosseguir.
- Se `scripts/validate-bundle.py` apontar placeholder não resolvido, abrir o arquivo indicado, identificar a seção e completar antes de revalidar.
- Se o usuário responder "Outro" com texto vazio em qualquer rodada, repetir a pergunta uma vez antes de encerrar com `needs_input`.
- Se a Rodada 2 não conseguir levantar pelo menos um edge case relevante, abrir Rodada 3 focada exclusivamente em cenários de exceção.
