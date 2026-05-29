# Regras de Qualidade do Dossiê

Estas regras existem para impedir dossiê genérico, placeholder esquecido e falsa sensação de prontidão.

## Princípios
- Preferir premissa explícita a texto vago.
- Preferir faixa estimada a campo vazio, desde que a incerteza seja registrada.
- Preservar nomes dos sistemas, domínios e restrições reais do contexto do usuário.
- Não transformar ausência de material em invenção.

## Placeholders Proibidos

Uma linha deve ser tratada como inválida quando, após remover whitespace e marcador de bullet, for exatamente um destes valores:
- `TBD`
- `A DEFINIR`
- `A CONFIRMAR`
- `PENDENTE`
- `N/A`
- `?`
- `-`
- `...`

Também é inválida qualquer linha inteira no formato bracket-only, por exemplo:
- `[valor]`
- `[nome]`
- `[texto]`

## Seções Críticas

Não deixar placeholders ou seção vazia em:
- `## Título`
- `## Necessidade e Objetivos`
- `## Escopo`
- `## Viabilidade Técnica`
- `## Arquitetura Proposta`
- `## Volumetria e Capacidade`
- `## Segurança e Compliance`
- `## Confiabilidade e Resiliência`
- `## Observabilidade e Operação`
- `## Custos e Orçamento`
- `## Riscos e Mitigações`
- `## Decomposição em Épicos e Features`

## Requisitos Mínimos de Conteúdo
- `## Volumetria e Capacidade` precisa responder volume atual, pico, crescimento e meta operacional.
- `## Segurança e Compliance` precisa cobrir dados, AuthN/AuthZ, segredos, criptografia e auditoria.
- `## Confiabilidade e Resiliência` precisa cobrir SLA/SLO, RTO/RPO, retry/idempotência, degradação e rollback.
- `## Observabilidade e Operação` precisa cobrir métricas, logs, traces, alertas e runbooks.
- `## Custos e Orçamento` precisa cobrir valor ou faixa, drivers, guardrails e plano de otimização.
- `## Decomposição em Épicos e Features` precisa conter ao menos um `Epic` e uma `Feature`.

## Postura de Escrita
- Escrever de forma específica ao contexto.
- Evitar adjetivos vazios como "escalável", "seguro" ou "robusto" sem explicar mecanismo, limite ou trade-off.
- Declarar risco residual quando a solução depender de hipótese não validada.
