# Débito Técnico: <título-curto>

<!-- debt-version: 1 -->
<!-- fast-track: XS/S podem omitir seções 9 e 10 ou preencher em uma linha. M/L/XL preenchem todas as 12. -->

## 1. Identificação
- Slug: `<slug-kebab-case>`
- Título curto: <título legível em uma linha>
- Autor: <nome ou time>
- Data de registro: <YYYY-MM-DD>
- Status: `registrado` <!-- registrado | em-analise | aceito | pago | rejeitado -->

## 2. Problema
**Descrição expandida:** <expansão da descrição original, preservando termos técnicos do usuário>

**Contexto que gerou o débito:** <histórico, decisão anterior, restrição que levou ao estado atual; "não informado" se ausente>

**Sintomas hoje:** <o que se observa no presente, evidências citáveis>

## 3. Natureza
- Primária: <uma de: segurança | performance | manutenibilidade | confiabilidade | observabilidade | complexidade | lock-in tecnológico | cobertura de testes | conformidade | documentação>
- Secundárias (até 2): <lista ou "nenhuma">

Referência: `references/debt-taxonomy.md`.

## 4. Localização no Codebase

Escopo confrontado: <caminho local | repo `owner/repo` | misto | pulado-com-justificativa>

| Arquivo / Módulo | Status | Evidência | Notas |
|---|---|---|---|
| <ex.: `internal/auth/handler.go`> | confirmado | `internal/auth/handler.go:42` | sem validação de token expirado |
| <ex.: `internal/middleware/`> | suspeito | `internal/middleware/log.go:15` | menciona `auth` mas é só log |
| <ex.: `cmd/api/main.go`> | ausente | — | nenhum handler de login registrado |

Status legend: `confirmado | suspeito | ausente | refutado`.

## 5. Impacto e Blast Radius
- **Quem é afetado:** <clientes externos | times internos | um serviço único | múltiplos serviços | compliance>
- **O que quebra ou atrasa hoje:** <descrição concreta>
- **Blast radius:** <1 serviço | 2-5 serviços | todos os serviços | clientes externos | compliance>

## 6. Severidade e Urgência
- **Severidade:** <alta | média | baixa> — <justificativa em 1 linha>
- **Urgência:** <agora | próxima sprint | próximo trimestre | oportunística> — <justificativa em 1 linha>

Matriz de prioridade (use para guiar a decisão):

| | Urgência: agora | próxima sprint | próximo trimestre | oportunística |
|---|---|---|---|---|
| **Severidade alta** | P0 | P1 | P2 | P2 |
| **Severidade média** | P1 | P2 | P3 | P3 |
| **Severidade baixa** | P2 | P3 | P3 | backlog |

**Prioridade resultante:** <P0/P1/P2/P3/backlog>

## 7. Estratégia de Pagamento
- **Estratégia escolhida:** <refactor incremental | big bang | isolar e substituir | aceitar e documentar | transferir>
- **Justificativa:** <por que esta estratégia, considerando blast radius, severidade e esforço>
- **Alternativas consideradas:** <lista curta com motivo do descarte>

## 8. Esforço Estimado
- Tamanho: <XS (horas) | S (dias) | M (semana) | L (sprint) | XL (trimestre+)>
- Suposições de cálculo: <o que precisa ser verdade para o tamanho se manter; ex.: "assume 1 pessoa full-time", "exige migração de 200 registros">
- Confiança da estimativa: <alta | média | baixa>

## 9. Riscos de Não Pagar
<!-- Obrigatório para M/L/XL ou severidade alta ou prioridade <= P1. Opcional para XS/S. -->

- Em 3 meses: <o que piora>
- Em 6 meses: <o que piora>
- Em 12 meses: <o que piora>
- Riscos compostos (se outro débito relacionado também não for pago): <descrição ou "não aplicável">

<!-- XS/S fast-track: substituir tudo acima por 1 linha. Ex.: "Risco baixo a curto prazo; apenas custo de manutenção crescente." -->

## 10. Plano de Ação Proposto
<!-- Obrigatório para M/L/XL ou severidade alta ou prioridade <= P1. Opcional para XS/S. -->

1. <passo 1 concreto — verbo + objeto + critério de saída>
2. <passo 2>
3. <passo 3>

**Testes de saída por passo:** <como saber que cada passo terminou>

**Critérios de aceite globais:**
- [ ] <critério mensurável 1>
- [ ] <critério mensurável 2>
- [ ] <critério mensurável 3>

<!-- XS/S fast-track: substituir tudo acima por 1 linha. Ex.: "Renomear handler X para Y e atualizar 3 call sites; aceite = lint passa e teste unitário verde." -->

## 11. Lacunas Observadas
- <perguntas que ficaram sem resposta>
- <dados ausentes que precisam ser coletados antes de iniciar>
- <validações pendentes com stakeholder>

## 12. Próximo Passo
> <instrução literal sugerida pela skill — ex.: "Publique este débito como work item no Azure DevOps na board <X>" ou "Quando virar feature, use a skill tracker-to-prd a partir da issue criada">
