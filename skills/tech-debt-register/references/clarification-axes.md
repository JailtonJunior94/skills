# Eixos de Clarificação para Débito Técnico

A skill `tech-debt-register` exige os oito eixos abaixo preenchidos antes de materializar o documento. Cada rodada de `AskUserQuestion` cobre eixos pendentes, com no máximo 4 perguntas por chamada. Cada opção deve trazer `description` explicando trade-off.

## Critério de Parada
A skill encerra e materializa o `debt.md` **somente quando**:
1. Todos os 8 eixos abaixo estiverem com status `respondido`.
2. Nenhum item da localização no codebase permanecer em status `conflicting` sem decisão.

Enquanto qualquer condição falhar, abrir nova rodada focada nos pontos pendentes.

## Eixos Obrigatórios

### Eixo 1 — Natureza do Débito
Categoria primária do débito (consultar `references/debt-taxonomy.md`).

**Pergunta-modelo:**
> Qual é a natureza primária deste débito?
- (a) Segurança — risco de exposição ou violação
- (b) Performance — latência/throughput/recursos
- (c) Manutenibilidade — código difícil de evoluir
- (d) Confiabilidade — falhas intermitentes ou perda silenciosa
- (Outras categorias seguem em rodada complementar se necessário: observabilidade, complexidade, lock-in, testes, conformidade, documentação.)

### Eixo 2 — Sintoma Observável Hoje
Como o débito se manifesta no presente.

**Pergunta-modelo:**
> Qual é o sintoma observável hoje?
- (a) Incidentes recorrentes ou bug em produção
- (b) Lentidão medida (latência ou throughput)
- (c) Retrabalho frequente em PRs ou bugs intermitentes
- (d) Bloqueio para entregar nova feature
- (Opcionais: dificuldade de onboarding, achado de auditoria, ainda apenas previsão.)

### Eixo 3 — Localização no Codebase
Confirma/refina o resultado do confronto.

**Pergunta-modelo:**
> Onde o débito mora no codebase?
- (a) Em um módulo único e bem delimitado
- (b) Em módulos vizinhos (2-3 áreas próximas)
- (c) Espalhado em vários pontos do mesmo serviço
- (d) Transversal a múltiplos serviços
- (Greenfield: o débito é a ausência completa — não há código sobre o tema ainda.)

### Eixo 4 — Blast Radius
Quem é impactado.

**Pergunta-modelo:**
> Qual é o blast radius do débito?
- (a) 1 serviço/módulo isolado
- (b) 2-5 serviços internos
- (c) Todos os serviços (transversal)
- (d) Atinge clientes externos ou parceiros
- (Opcional: atinge compliance/regulatório.)

### Eixo 5 — Severidade
Magnitude do risco ou do impacto.

**Pergunta-modelo:**
> Qual é a severidade?
- (a) Alta — risco material em curto prazo (incidente, perda de receita, exposição)
- (b) Média — degrada qualidade contínua (retrabalho, lentidão crônica)
- (c) Baixa — irritação esporádica sem impacto material

### Eixo 6 — Urgência
Janela de tempo para tratar.

**Pergunta-modelo:**
> Qual é a urgência?
- (a) Agora — bloqueia entrega ativa ou exige resposta imediata
- (b) Próxima sprint — encaixa no ciclo atual
- (c) Próximo trimestre — entra em roadmap
- (d) Oportunística — quando alguém estiver na área

### Eixo 7 — Estratégia de Pagamento
Como pretende ser pago.

**Pergunta-modelo:**
> Qual a estratégia de pagamento preferida?
- (a) Refactor incremental — pequenas PRs ao longo de sprints
- (b) Big bang — uma entrega única, mais rápida e mais arriscada
- (c) Isolar e substituir (strangler) — caminho novo coexiste e migra gradual
- (d) Aceitar e documentar — registrar e conviver, sem pagar agora
- (Opcional: transferir para outro time que owna a área.)

### Eixo 8 — Esforço Estimado
T-shirt sizing.

**Pergunta-modelo:**
> Qual é o tamanho de esforço estimado?
- (a) XS — horas
- (b) S — dias
- (c) M — uma semana
- (d) L — uma sprint
- (Opcional: XL — trimestre ou mais.)

## Regras de Aplicação
- Marcar um eixo como `respondido` automaticamente quando a descrição inicial do usuário trouxer evidência objetiva. Citar a evidência ao apresentar o resultado.
- Itens em status `conflicting` no confronto (ex.: 4 implementações divergentes de retry) viram pergunta antes de continuar pelos eixos restantes. Opções: "Refinar escopo do débito", "Tratar em débito separado", "Aceitar com nota explícita".
- Quando o usuário responder `Outro` com texto vazio, repetir a pergunta uma vez antes de encerrar com `needs_input`.
- Se a mesma categoria/eixo ficar pendente após 3 rodadas consecutivas sem progresso, encerrar com `needs_input` listando os pontos travados.
