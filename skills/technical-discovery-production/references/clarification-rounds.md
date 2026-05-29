# Rodadas Obrigatórias de Clarificação

Toda execução DEVE usar múltipla escolha e DEVE confrontar o pedido do usuário com limites reais da solução. Rodadas 1, 2 e 3 são obrigatórias. Rodadas adicionais são abertas enquanto existir risco material sem decisão.

## Regras Gerais
- Formular de 2 a 4 opções mutuamente exclusivas por pergunta.
- Manter cada chamada com no máximo 4 perguntas.
- Explicitar em cada opção a consequência principal: mais custo, mais segurança, menor prazo, maior risco, menor cobertura, maior escalabilidade ou menor complexidade.
- Referenciar o pedido atual do usuário no enunciado. Exemplo: "Considerando que o pedido é liberar em 60 dias..."
- Se a ferramenta estruturada de perguntas não existir, renderizar a mesma pergunta no texto com opções `A`, `B`, `C`, `D`.
- Manter o mesmo conteúdo decisório entre agentes: trocar o meio de interação é permitido; trocar a lógica das opções, não.
- Solicitar arquivos, links ou caminhos logo após a classificação, mas não substituir a classificação por pergunta aberta.

## Rodada 1 - Objetivo, escopo e criticidade

Cobertura mínima:
1. Objetivo dominante da iniciativa.
2. Criticidade do domínio ou do fluxo.
3. Recorte de escopo da primeira entrega.
4. Restrição dominante: prazo, custo, compliance, legado, time ou dependência externa.

Exemplos de perguntas:
- Qual objetivo principal deve prevalecer: velocidade, robustez, redução de custo ou compliance?
- O fluxo impactado é operacionalmente crítico, sensível a dados ou tolerante a indisponibilidade parcial?
- A primeira entrega cobre somente o núcleo do fluxo, o fluxo completo ou inclui automações adjacentes?

## Rodada 2 - Arquitetura, dados, volumetria e custo

Cobertura mínima:
1. Estilo arquitetural ou estratégia de entrega.
2. Dependência mais crítica de dados ou integração.
3. Perfil de volumetria e expectativa de crescimento.
4. Postura de custo/orçamento.

Exemplos de perguntas:
- O pedido comporta centralização em serviço único, evolução incremental no monólito ou extração de capacidade dedicada?
- A solução exige consistência forte, consistência eventual ou modelo híbrido?
- O volume esperado é baixo, médio, pico sazonal forte ou crescimento contínuo relevante?
- O orçamento favorece time-to-market com custo maior, equilíbrio, ou otimização rígida de custo?

## Rodada 3 - Segurança, confiabilidade e operação

Cobertura mínima:
1. Baseline de segurança.
2. Estratégia de resiliência e degradação.
3. Profundidade de observabilidade.
4. Estratégia de rollout e rollback.

Exemplos de perguntas:
- O pedido exige baseline padrão, baseline reforçada com trilha de auditoria, ou baseline máxima com segregação e controles adicionais?
- Em falha, a solução deve bloquear, degradar parcialmente ou operar com contingência offline?
- A operação precisa de métricas básicas, telemetria completa com tracing ou nível auditável para incidentes/regulação?
- O rollout será por feature flag, canary, piloto fechado ou big-bang controlado?

## Rodadas Adicionais

Abrir nova rodada quando faltar decisão sobre qualquer um dos pontos abaixo:
- risco de segurança não tratado;
- volumetria sem hipótese minimamente defensável;
- custo sem guardrail;
- integração crítica sem estratégia de erro;
- observabilidade sem métricas/alertas mínimos;
- decomposição em épicos e features ainda ambígua.

## Critério de Encerramento
- Encerrar apenas quando o dossiê puder ser preenchido sem placeholder proibido nas seções críticas.
- Não encerrar se a solução ainda não responder claramente: o que será construído, por que é viável, como escala, como é observada, como é protegida, quanto tende a custar e como será quebrada em épicos/features.
