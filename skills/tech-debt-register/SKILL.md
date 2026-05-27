---
name: tech-debt-register
description: |
  Registra débito técnico de forma estruturada em PT-BR a partir de uma descrição livre
  fornecida pelo usuário, confronta a descrição com o codebase informado (caminho local via
  Grep/Read ou repositório remoto via gh) para localizar onde o débito mora, conduz rodadas
  de clarificação em múltipla escolha cobrindo oito eixos fixos (natureza, sintoma,
  localização, blast radius, severidade, urgência, estratégia de pagamento, esforço) e
  materializa um documento detalhado em .specs/tech-debt-<slug>/debt.md com problema e
  plano de ação. Use quando o usuário quiser registrar débito técnico, mapear gap de
  qualidade, descrever refactor pendente ou documentar risco arquitetural. Não use para
  criar PRD de feature nova, abrir bug ativo em produção, planejar arquitetura completa,
  nem para publicar tickets diretamente em tracker externo.
---

# Registro de Débito Técnico

<critical>Confrontar a descrição do débito com o codebase antes de redigir o documento. Toda evidência precisa citar `path:linha` (local) ou URL (remoto).</critical>
<critical>Anti-falso-positivo: marcar `confirmado` exige match em `path:linha` E inspeção do contexto. Match em teste/mock/fixture/exemplo cai em `suspeito` por padrão. Em caso de dúvida, sempre `suspeito` + nova rodada — re-trabalho de scoping custa mais que rodada extra.</critical>
<critical>Conduzir rodadas de clarificação em múltipla escolha até cobrir os oito eixos. Encerrar somente quando os oito estiverem `respondido` E nenhum candidato da localização ficar em `conflicting` aberto.</critical>
<critical>Declarar a natureza primária do débito assim que a Rodada 1 (eixos 1-4) for respondida.</critical>
<critical>NÃO auto-invocar outras skills. Materializar o documento e sugerir o próximo passo em texto.</critical>
<critical>Preservar termos técnicos, nomes próprios, identificadores e siglas como aparecem na descrição do usuário.</critical>
<critical>Não materializar `debt.md` enquanto algum dos oito eixos estiver pendente.</critical>

## Entrada Obrigatória
- Descrição livre do débito em PT-BR (ex.: "preciso criar autenticação na minha API").

## Entrada Opcional
- Path local ou módulo suspeito (ex.: `internal/auth/` ou `.`).
- Repositório remoto no formato `owner/repo` (GitHub) para confronto via `gh`.
- Autor/time responsável (default: usuário corrente).

## Saída
- Diretório `.specs/tech-debt-<slug>/` contendo:
  - `debt.md` — documento estruturado com problema + plano de ação.
  - `clarifications.md` — append-only com cada rodada de perguntas e respostas.

## Procedimentos

**Step 0: Detectar agente e aplicar fallbacks**
1. Se o agente em uso não for Claude Code, ler `references/multi-agent-usage.md` antes de qualquer pergunta.
2. Quando `AskUserQuestion` não estiver disponível, usar blocos de texto livre estruturados conforme `references/multi-agent-usage.md` (Fallback 1).
3. Garantias que se mantêm em qualquer agente: cap de 15 buscas/rodada, cap honesto de 3 rodadas sem progresso, anti-falso-positivo no confronto, escrita do bundle em `.specs/tech-debt-<slug>/`.

**Step 1: Validar entrada**
1. Exigir descrição não vazia. Encerrar com `needs_input` se ausente, solicitando a descrição em uma frase curta.
2. Derivar título curto (até 80 chars) e gerar slug com `python3 scripts/slugify.py "<título>"`.
3. Anunciar o slug e a saída prevista (`.specs/tech-debt-<slug>/debt.md`) ao usuário.

**Step 2: Coletar escopo de codebase**
1. Perguntar via `AskUserQuestion` (multiSelect=true) o escopo de confronto:
   - "Caminho local" — pedir o path; default `.` se não informado.
   - "Repo remoto via gh" — pedir `owner/repo`; validar com `gh repo view <owner>/<repo> --json name -q .name`.
   - "Pular confronto" — exigir justificativa textual; registrar em `Lacunas Observadas`.
2. Encerrar com `blocked` se `gh` não estiver autenticado ao consultar repo remoto (orientar `gh auth status`).

**Step 3: Localizar débito no codebase**
1. Ler `references/codebase-confrontation.md`.
2. Identificar a natureza provável a partir da descrição e ler `references/debt-taxonomy.md` para puxar termos buscáveis da categoria.
3. Derivar 2 a 4 termos buscáveis priorizando identificadores explícitos do domínio do usuário.
4. Executar buscas:
   - Local: `Grep` com `output_mode=files_with_matches` ou `content`.
   - Remoto: `gh search code "<termo> repo:<owner>/<repo>" --limit 10` ou `gh api repos/<owner>/<repo>/contents/<path>`.
5. Respeitar o limite de 15 chamadas por rodada de localização.
6. Para cada candidato, registrar `status` (`confirmado | suspeito | ausente | refutado`), até 2 evidências e nota curta.
7. Persistir a tabela em memória; será serializada no Step 5.

**Step 4: Rodadas de clarificação**
1. Ler `references/clarification-axes.md`.
2. Marcar cada eixo como `respondido` quando a descrição original ou os comentários já contiverem evidência objetiva. Citar a evidência.
3. Para cada item ainda pendente, gerar pergunta de múltipla escolha (máx 4 por chamada `AskUserQuestion`).
4. Cada candidato em `conflicting` (vários `confirmado` divergentes) vira pergunta na rodada seguinte com opções: "Refinar escopo do débito", "Tratar em débito separado", "Aceitar com nota explícita".
5. Após coletar respostas, atualizar a tabela de eixos e a tabela de localização. Anexar bloco `## Rodada <n>` em `.specs/tech-debt-<slug>/clarifications.md` (criar se não existir).
6. **Critério de parada**: encerrar quando todos os 8 eixos estiverem `respondido` E nenhum candidato permanecer em `conflicting` sem decisão.
7. Cap honesto: se a mesma categoria/eixo ficar pendente após 3 rodadas consecutivas sem progresso, encerrar com `needs_input` listando os pontos travados.

**Step 5: Materializar `debt.md`**
1. Criar `.specs/tech-debt-<slug>/` se não existir.
2. Ler `assets/debt-template.md`.
3. Aplicar fast-track de tamanho:
   - **XS/S (horas a dias)**: preencher seções 1-8, 11 e 12 integralmente. Para 9 e 10, usar a forma curta (1 linha) sugerida nos comentários do template.
   - **M/L/XL (semana ou mais) OU severidade alta OU prioridade ≤ P1**: preencher todas as 12 seções integralmente.
4. Calcular prioridade (P0-P3/backlog) usando a matriz severidade × urgência do template.
5. Não inventar conteúdo ausente; deixar em `Lacunas Observadas`.
6. Escrever em `.specs/tech-debt-<slug>/debt.md`.
7. Garantir que `clarifications.md` contém todas as rodadas (append-only).

**Step 6: Encerrar com sugestões**
1. Exibir ao usuário:
   - Caminho do `debt.md`.
   - Resumo em 3 a 5 linhas: natureza primária, prioridade resultante, estratégia escolhida, esforço, próximo passo.
2. Sugerir próximos passos sem auto-invocar:
   - "Publique este débito como work item em Jira ou Azure DevOps manualmente ou via skill dedicada."
   - "Se o débito virar feature de produto, use a skill `tracker-to-prd` a partir da issue criada."
   - "Se for um pacote de refactor com sub-tarefas, decomponha localmente antes de publicar no tracker."
3. Encerrar com `done`.

## Decisões Operacionais
1. A descrição do usuário é fonte de verdade. Confronto e clarificação refinam, não substituem.
2. Confronto é determinístico (busca textual). Sem heurística fuzzy.
3. Greenfield (status `ausente` predominante) é resultado válido e desbloqueia o eixo 3 com "ausência completa".
4. Documento é fiel e curto. Sem dump de logs ou de árvores de diretório.
5. Preferir ausência explícita em `Lacunas Observadas` a inferência fraca.
6. Status do débito sempre nasce `registrado`. Transições posteriores (`em-analise`, `aceito`, `pago`, `rejeitado`) ocorrem fora da skill.

## Estados Finais
- `done`: documento gerado em `.specs/tech-debt-<slug>/debt.md`, sugestões de próximo passo exibidas.
- `needs_input`: descrição ausente; pendência travada na mesma categoria após 3 rodadas sem progresso; `Outro` vazio repetido em pergunta de clarificação.
- `blocked`: `gh` não autenticado para repo remoto, ou repositório remoto inacessível, ou path local fornecido não existe.
- `failed`: erro repetido em escrita do documento após uma tentativa de recuperação.

## Tratamento de Erros
- Se a descrição inicial for vazia, encerrar com `needs_input` solicitando "Descreva o débito em uma frase curta".
- Se `python3 scripts/slugify.py` falhar (texto reduz a vazio após normalização), perguntar um título alternativo e tentar uma vez.
- Se o path local fornecido não existir, listar diretórios próximos ao cwd e encerrar com `needs_input`.
- Se `gh` não estiver autenticado, encerrar com `blocked` orientando `gh auth status` e `gh auth login`.
- Se o limite de 15 buscas por rodada for atingido com candidatos restantes, registrar os termos não cobertos como `ausente` com nota explícita e seguir para clarificação.
- Se o usuário responder `Outro` com texto vazio em qualquer rodada, repetir a pergunta uma vez antes de encerrar com `needs_input`.
- Se o diretório `.specs/tech-debt-<slug>/` já existir, perguntar via `AskUserQuestion`: "Reaproveitar diretório existente (anexa nova rodada)", "Renomear novo registro com sufixo `-v2`" ou "Cancelar".
- Se o agente não suportar `AskUserQuestion`, aplicar Fallback 1 de `references/multi-agent-usage.md` (texto livre estruturado com letras `a/b/c/d`) e validar a resposta antes de prosseguir.
