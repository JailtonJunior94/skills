# Gates de Prontidão

O dossiê só está pronto para handoff quando todos os gates abaixo estiverem atendidos ou explicitamente aceitos como risco residual pelo usuário.

## Gate 1 - Problema e Escopo
- Problema atual descrito com impacto claro.
- Objetivos de negócio e técnicos separados.
- Inclui e exclui definidos.

## Gate 2 - Viabilidade e Arquitetura
- Viabilidade classificada como `viável`, `viável com restrições` ou `inviável`.
- Arquitetura proposta explicada em termos de componentes, fluxo e decisão principal.
- Integrações e consistência de dados identificadas.

## Gate 3 - Volumetria e Escala
- Existe hipótese minimamente defensável para volume atual, pico e crescimento.
- Há SLO ou meta operacional compatível com o contexto.
- Há noção clara de gargalos e estratégia de escala.

## Gate 4 - Segurança e Compliance
- Classificação de dados identificada.
- AuthN/AuthZ, segredos, criptografia e auditoria definidos em nível compatível com o contexto.
- Impactos de LGPD, compliance ou regulação foram avaliados, mesmo que para concluir que não se aplicam.

## Gate 5 - Confiabilidade e Operação
- Existe estratégia de retry/idempotência ou justificativa para sua ausência.
- Existe estratégia de degradação, contingência e rollback.
- Observabilidade contém métricas, logs, traces e alertas suficientes para operar a solução.

## Gate 6 - Custo e Orçamento
- Existe orçamento estimado ou faixa de custo.
- Drivers de custo foram identificados.
- Há guardrails ou hipótese explícita de otimização.

## Gate 7 - Decomposição
- Existe ao menos um épico nomeado.
- Cada épico tem objetivo claro.
- Cada épico tem pelo menos uma feature identificada.
- A decomposição respeita o recorte escolhido nas rodadas de clarificação.

## Gate 8 - Riscos
- Riscos principais estão listados com mitigação e dono.
- Lacunas remanescentes estão em `## Itens em Aberto`.
- Nenhum risco material foi tratado como detalhe de implementação futura sem registro explícito.
