---
name: technical-discovery-production
description: Conduz discovery técnico e refinamento de solução em PT-BR com rodadas obrigatórias de múltipla escolha sobre problema, materiais de apoio, viabilidade, arquitetura, volumetria, segurança, confiabilidade, observabilidade, escalabilidade e orçamento. Confronta o pedido do usuário com riscos, trade-offs e boas práticas de produção, e materializa um dossiê técnico validado pronto para decomposição em épicos e features. Use quando o usuário pedir discovery técnico, system design, estudo de viabilidade, arquitetura de solução, estimativa inicial de custos ou refinamento production-ready. Não use para implementar código, apenas registrar brainstorming sem decisão, ou decompor backlog diretamente em tarefas finais.
---

# Discovery Técnico Production-Ready

<critical>Todos os artefatos DEVEM ser escritos em PT-BR.</critical>
<critical>Toda clarificação DEVE ocorrer em formato de múltipla escolha. Se a ferramenta nativa de pergunta estruturada não estiver disponível, enviar perguntas textuais com 2 a 4 opções mutuamente exclusivas e aguardar a escolha do usuário antes de avançar.</critical>
<critical>Cada pergunta DEVE confrontar o pedido atual do usuário com pelo menos um eixo de decisão real: risco, segurança, viabilidade técnica, custo, escalabilidade, confiabilidade ou observabilidade.</critical>
<critical>Segurança, robustez, observabilidade, confiabilidade, volumetria e custo NÃO são opcionais. Se qualquer um desses eixos estiver indefinido, abrir nova rodada em vez de materializar o dossiê.</critical>
<critical>O dossiê só é considerado pronto quando `scripts/validate-bundle.py` retornar `SUCCESS`.</critical>
<critical>O comportamento da skill DEVE ser agnóstico de agente: Claude Code e Codex CLI DEVEM seguir a mesma ordem de passos, os mesmos gates de prontidão, o mesmo formato de saída em arquivos e a mesma política de perguntas em múltipla escolha.</critical>

## Entrada Obrigatória
- Tema da descoberta, problema ou iniciativa a ser analisada.
- Contexto inicial do usuário: objetivo, restrições conhecidas, prazo, sistema impactado ou hipótese de solução.

## Entrada Recomendável
- Materiais de apoio: PRD, RFC, diagramas, contratos de API, logs, métricas, dashboards, requisitos regulatórios, orçamento alvo, SLAs/SLOs, incidentes anteriores.

## Saída
Bundle local em `./discoveries/technical-<slug>/`:
- `bundle.json` - índice da descoberta com metadados e prontidão.
- `discovery.md` - dossiê técnico consolidado.
- `transcript.md` - histórico das rodadas, decisões e materiais usados.

## Contrato de Compatibilidade
- Não depender de componentes visuais, widgets, formulários ou APIs específicas do agente.
- Quando houver suporte a pergunta estruturada, usar esse mecanismo sem alterar o conteúdo lógico das opções.
- Quando não houver suporte a pergunta estruturada, renderizar a pergunta em texto puro com opções `A`, `B`, `C`, `D` e aguardar uma resposta inequívoca antes de prosseguir.
- Não assumir nomes de ferramentas, estados internos ou integrações exclusivas de Claude Code ou Codex CLI.
- Preservar o mesmo bundle local, os mesmos nomes de arquivos e o mesmo critério de validação em qualquer agente.

## Procedimentos

**Step 1: Validar tema e inicializar bundle**
1. Identificar um título curto para a iniciativa a partir do pedido do usuário.
2. Executar `python3 scripts/slugify.py "<titulo>"` para normalizar o slug.
3. Verificar se `./discoveries/technical-<slug>/` já existe. Se existir, perguntar em múltipla escolha se deve reaproveitar, criar novo com sufixo ou cancelar.
4. Executar `python3 scripts/init-bundle.py <slug>` para criar `bundle.json`, `discovery.md` e `transcript.md`.
5. Encerrar com `blocked` se o script falhar por conflito de diretório, permissão ou slug inválido.

**Step 2: Coletar necessidade e materiais de apoio**
1. Pedir ao usuário, em múltipla escolha, qual é a natureza principal da demanda: nova capacidade, modernização, redução de custo, correção estrutural, compliance/segurança ou outra categoria equivalente ao contexto.
2. Pedir ao usuário, em múltipla escolha, qual é o estado atual de materiais de apoio: documentação robusta, documentação parcial, apenas contexto verbal, ou sistema legado pouco conhecido.
3. Solicitar os artefatos concretos que sustentam a descoberta: links, arquivos locais, caminhos de repositório ou descrições curtas. Se o usuário não tiver materiais, registrar explicitamente a ausência.
4. Resumir o entendimento inicial em até 6 bullets e registrar em `transcript.md` no bloco `## Contexto Inicial`.

**Step 3: Rodada 1 obrigatória - objetivo, escopo e criticidade**
1. Ler `references/clarification-rounds.md` e aplicar os eixos da Rodada 1.
2. Formular de 3 a 4 perguntas em múltipla escolha cobrindo, no mínimo: objetivo principal, criticidade do domínio, recorte de escopo inicial e restrição dominante.
3. Em cada pergunta, explicitar a tensão entre o pedido do usuário e o impacto técnico. Exemplo: maior velocidade de entrega versus maior risco operacional.
4. Registrar perguntas, opções e respostas em `transcript.md` no bloco `## Rodada 1`.
5. Atualizar o rascunho interno do dossiê com hipóteses e restrições confirmadas.

**Step 4: Rodada 2 obrigatória - arquitetura, dados, volumetria e custo**
1. Ler `references/clarification-rounds.md` e aplicar os eixos da Rodada 2.
2. Formular de 3 a 4 perguntas em múltipla escolha cobrindo, no mínimo: estilo arquitetural ou estratégia de entrega, integrações/dados críticos, perfil de volumetria e orçamento/guardrail de custo.
3. Confrontar o pedido original com limites reais do sistema: throughput, latência, consistência, dependências externas e operação.
4. Registrar tudo em `transcript.md` no bloco `## Rodada 2`.

**Step 5: Rodada 3 obrigatória - segurança, confiabilidade e operação**
1. Ler `references/clarification-rounds.md` e aplicar os eixos da Rodada 3.
2. Formular de 3 a 4 perguntas em múltipla escolha cobrindo, no mínimo: baseline de segurança, estratégia de resiliência, profundidade de observabilidade e rollout/rollback.
3. Não aceitar resposta genérica do tipo "depois define". Se o usuário não souber, oferecer opções conservadoras e registrar a premissa escolhida.
4. Registrar tudo em `transcript.md` no bloco `## Rodada 3`.

**Step 6: Abrir rodadas adicionais enquanto houver risco material**
1. Ler `references/readiness-gates.md`.
2. Avaliar se ainda faltam definições para qualquer gate mandatório: viabilidade, segurança, volumetria, confiabilidade, observabilidade, custo ou decomposição.
3. Se faltar, abrir Rodada 4+ com perguntas focadas exclusivamente nos pontos pendentes.
4. Manter cada rodada com no máximo 4 perguntas e registrar no `transcript.md`.
5. Não materializar `discovery.md` enquanto existir bloqueio material não decidido.

**Step 7: Consolidar hipótese de solução e confirmar direção**
1. Apresentar ao usuário um resumo consolidado em até 10 bullets com: problema, escopo, arquitetura proposta, principais riscos, custo esperado, volumetria, baseline de segurança, estratégia operacional e implicações do trade-off adotado.
2. Perguntar em múltipla escolha se deve: materializar o dossiê agora, refinar mais um ponto específico, ou cancelar.
3. Se o usuário pedir refinamento, voltar ao Step 6.
4. Se o usuário cancelar, encerrar com `done` sem materializar novos artefatos além do transcript.

**Step 8: Materializar o dossiê técnico**
1. Ler `assets/discovery-template.md`.
2. Ler `references/document-quality-rules.md`.
3. Preencher `discovery.md` integralmente com base nas respostas e materiais coletados. Não inventar fatos ausentes; registrar lacunas explicitamente em `## Itens em Aberto`.
4. Garantir que as seções de segurança, confiabilidade, observabilidade, volumetria, custo e decomposição sejam específicas ao contexto do usuário, sem texto genérico reaproveitado.
5. Atualizar `bundle.json` com título, status de prontidão, blockers remanescentes e épicos planejados.

**Step 9: Validar e corrigir**
1. Executar `python3 scripts/validate-bundle.py ./discoveries/technical-<slug>`.
2. Se houver erro, ler o stderr, identificar a seção, corrigir o documento e reexecutar.
3. Encerrar com `blocked` se a validação continuar falhando após uma rodada de correção honesta.

**Step 10: Relatar a saída**
1. Informar o caminho do bundle gerado.
2. Resumir em até 6 bullets os pontos centrais da solução proposta, riscos residuais e prontidão para quebrar em épicos/features.
3. Sugerir como próximo passo a decomposição em backlog, mas não criar tarefas finais automaticamente neste skill.

## Decisões Operacionais
1. Tratar produção como restrição de primeira classe, não como seção cosmética.
2. Preferir premissa explícita e auditável a inferência fraca.
3. Exigir granularidade suficiente para responder: o que será construído, quanto suporta, quanto custa, como falha, como observa e como volta atrás.
4. Formular perguntas que desafiem o pedido do usuário quando ele implicar risco oculto. Não apenas coletar preferências.
5. Preservar a terminologia de negócio e os nomes dos sistemas informados pelo usuário.
6. Se não houver ferramenta de pergunta estruturada, manter o formato de múltipla escolha no texto e aguardar escolha antes de seguir.
7. Tratar materiais ausentes como risco explícito no dossiê, nunca como permissão para preencher lacunas por suposição forte.
8. Se o agente suportar recursos extras, não alterar o fluxo decisório obrigatório da skill por causa disso.

## Estados Finais
- `done`: transcript e, quando aprovado, dossiê materializados e validados.
- `needs_input`: falta resposta do usuário para risco material ou falta insumo indispensável após tentativa de clarificação.
- `blocked`: erro de I/O, conflito de diretório, falha persistente de validação ou impossibilidade de materializar o bundle.
- `failed`: erro inesperado de execução após tentativa de recuperação.

## Tratamento de Erros
- Se `scripts/slugify.py` retornar slug vazio, pedir um título curto ao usuário e repetir a normalização.
- Se `scripts/init-bundle.py` falhar por diretório existente, oferecer em múltipla escolha reaproveitar, versionar ou cancelar.
- Se o usuário insistir em seguir sem materiais de apoio, registrar isso em `## Materiais de Apoio`, marcar risco correspondente e abrir perguntas adicionais de redução de incerteza.
- Se a validação apontar placeholder não resolvido em seção crítica, completar a seção ou registrar a lacuna em `## Itens em Aberto` e voltar para nova rodada antes de revalidar.
- Se não for possível estimar volumetria, custo ou estratégia operacional com o material disponível, encerrar com `needs_input` em vez de declarar a solução pronta para backlog.
