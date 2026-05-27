# Rodadas de Clarificação Obrigatórias

Toda execução da skill DEVE incluir as Rodadas 1 e 2. Sem exceções. Rodadas adicionais (3, 4, ...) são abertas enquanto persistir ambiguidade material.

## Princípios Gerais
- Cada pergunta usa `AskUserQuestion` com 2 a 4 opções mutuamente exclusivas.
- Header com no máximo 12 caracteres (`Escopo`, `Persona`, `KPI`, `Trade-off`, `Rollout`).
- Cada chamada `AskUserQuestion` carrega no máximo 4 perguntas (limite da ferramenta).
- Nunca apresentar opção "Outro" manualmente — o componente já adiciona.
- Cada `option.label` é curto (1-5 palavras); cada `option.description` explicita implicação ou trade-off.

## Rodada 1 — Refinar Produto/Feature

Cobertura obrigatória (uma pergunta por eixo):

1. **Objetivo macro**
   - Pergunta sugerida: "Qual é o objetivo estratégico principal deste épico?"
   - Opções típicas:
     - Reduzir custo operacional
     - Aumentar conversão/receita
     - Atender compliance/segurança
     - Habilitar nova capacidade

2. **Persona-alvo prioritária**
   - Pergunta sugerida: "Qual persona é o alvo prioritário desta entrega?"
   - Opções derivadas do contexto. Exemplos: cliente final, operador interno, suporte, antifraude.

3. **Recorte de escopo**
   - Pergunta sugerida: "Qual recorte de escopo entra na primeira entrega?"
   - Opções com diferentes amplitudes: mínimo viável, escopo médio, escopo completo.

4. **KPI principal**
   - Pergunta sugerida: "Qual métrica será o KPI principal de sucesso?"
   - Opções típicas: conversão, tempo médio de execução, volume de tickets, NPS, adoção, SLA.

## Rodada 2 — Trade-offs e Edge Cases (mandatória)

Cobertura obrigatória:

1. **Trade-off arquitetural ou de produto**
   - Apresentar 2 a 4 opções comparáveis. Cada `description` explicita custo/benefício.
   - Exemplo: "MFA obrigatório para todos" (mais segurança, mais fricção) vs. "MFA opcional por elegibilidade" (menos fricção, cobertura parcial).

2. **Edge cases a cobrir**
   - Listar 2 a 4 cenários concretos derivados do contexto.
   - Cada opção representa um edge case e o usuário decide: cobrir agora, descartar ou tratar em iteração futura.
   - Exemplos genéricos:
     - Usuário sem dado obrigatório tenta fluxo principal
     - Operação concorrente sobre o mesmo recurso
     - Falha de integração com sistema externo
     - Retentativa após timeout

3. **Dependências externas**
   - Pergunta sugerida: "Qual dependência externa é bloqueante?"
   - Opções: nenhuma, API interna, vendor externo, aprovação regulatória.

4. **Estratégia de rollout**
   - Pergunta sugerida: "Como deve ser feito o rollout?"
   - Opções típicas:
     - Dark launch com feature flag
     - Canary por percentual de usuários
     - Big-bang após homologação
     - Piloto fechado por segmento

## Critério de Parada
- Encerrar as rodadas apenas quando todas as seções críticas do épico (Título, Objetivo, Hipótese de Valor, Escopo, Critérios de Aceite, KPIs) e de cada US (Título, Descrição, Critérios de Aceite Gherkin) puderem ser preenchidas sem placeholder proibido.
- Abrir Rodada 3+ se restar ambiguidade. Cada rodada extra é focada exclusivamente nos pontos pendentes.

## Exemplo de Rodada Bem Conduzida (referência)
- Pergunta: "Qual recorte de escopo entra na primeira entrega?"
  - Opção A: "Apenas recuperação de senha" — entrega mais rápida, menor cobertura.
  - Opção B: "Recuperação + desbloqueio de conta" — escopo médio, cobre dois fluxos críticos.
  - Opção C: "Recuperação + desbloqueio + MFA opcional" — escopo amplo, exige integração com provedor de MFA.
