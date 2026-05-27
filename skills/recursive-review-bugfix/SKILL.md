---
name: recursive-review-bugfix
description: Executa ciclo recursivo de revisão crítica e correção (bugfix) sobre o diff atual, guiado integralmente pelo conteúdo da pasta de PRD/TechSpec/tasks informada pelo usuário. Repete revisão e correção até atingir veredito aprovado, sem assumir stack, linguagem, áreas de risco, comandos de validação ou padrões específicos: tudo é extraído dos artefatos presentes na pasta indicada. Aciona quando o usuário pedir revisão recursiva, fluxo review/bugfix iterativo, ou validação final antes de aprovar mudanças. Solicita obrigatoriamente o caminho da pasta a ser analisada antes de iniciar. Não usar para revisões superficiais pontuais, geração de PR, ou tarefas que não exijam ciclo iterativo até a aprovação.
---

# Fluxo de Revisão e Correção Recursiva (Review & Bugfix)

Orquestrar um ciclo contínuo de revisão crítica seguida de correção até que a entrega atinja o veredito **aprovado**, com ZERO achados Críticos ou Importantes. A skill é totalmente agnóstica: **nada** sobre stack, linguagem, áreas de risco, RFs, invariantes, comandos de validação ou padrões é assumido. Todo contexto é derivado exclusivamente do que existe na pasta indicada pelo usuário (PRD, TechSpec, tasks e demais artefatos).

## Passo 1: Coletar Caminho da Pasta a Analisar (OBRIGATÓRIO — needs_input)

1. **Sempre** solicitar ao usuário o caminho da pasta que contém PRD, TechSpec e/ou tasks antes de iniciar qualquer outra etapa. Não inferir, não usar valor padrão, não assumir convenções de nome.
2. Pergunta obrigatória (formato fixo):

---

**Para iniciar o ciclo de revisão recursiva, informe:**

- **Caminho da pasta a ser analisada recursivamente** (PRD, TechSpec, tasks e demais artefatos): ___

---

3. Validar que o caminho informado existe no repositório. Se não existir, reapresentar a pergunta indicando que o caminho não foi encontrado.
4. Registrar o caminho como `${ANALYSIS_PATH}` e usá-lo como única fonte canônica de contexto durante todo o ciclo.

## Passo 2: Extrair Contexto Recursivamente do Caminho

1. Percorrer recursivamente `${ANALYSIS_PATH}` lendo todos os artefatos relevantes (PRD, TechSpec, tasks, ADRs, anexos, esquemas, plano de teste, qualquer outro documento).
2. A partir do que estiver escrito nesses artefatos, extrair:
   - Lista de RFs e critérios de aceite.
   - Áreas de risco declaradas pelo próprio PRD/TechSpec.
   - Invariantes, contratos públicos e comportamentos que não podem mudar.
   - Restrições não negociáveis e regras específicas do domínio.
   - Skill ou processo usado na implementação, quando declarado.
   - Comandos de validação (testes, lint, build) referenciados nos artefatos.
3. **Não introduzir foco, regra, área de risco ou comando que não esteja respaldado pelo conteúdo dos artefatos lidos.** Se uma informação estiver ausente, registrar a lacuna e tratá-la como item a resolver com o usuário.
4. Inicializar contador `AI_INVOCATION_DEPTH = 0`.

## Passo 3: Etapa de Revisão Crítica (Skill: review)

Acionar a skill `review` usando o template abaixo, preenchendo todos os campos exclusivamente com dados extraídos no Passo 2. Manter os colchetes vazios ou pedir esclarecimento ao usuário caso algum campo não tenha respaldo nos artefatos lidos.

### Template de Prompt para `review`

```text
Use a skill review para revisar o diff atual.

Contexto da implementacao:
- Tasks executadas: ${ANALYSIS_PATH}
- Skill usada na implementacao: [extraido dos artefatos]
- Areas de risco: [extraidas dos artefatos]

Focos obrigatorios da revisao:
- corretude: a implementacao atende todos os RFs e criterios de aceite descritos nos artefatos?
- regressao: alguma mudanca quebra contrato publico ou comportamento existente declarado nos artefatos?
- seguranca: ha injecao de dependencia insegura, dado sensivel exposto ou validacao faltando conforme regras dos artefatos?
- testes: todos os cenarios do criterio de pronto descritos nos artefatos estao cobertos?
- dívida tecnica introduzida: o que precisara de refactor futuro?

Saidas esperadas:
- Mandatório NÃO TER FALSOS POSITIVOS, REALMENTE TENHA CERTEZA
- lista de achados por categoria (critico, importante, sugestao)
- para cada achado critico: arquivo, linha, descricao e correcao sugerida
- veredicto final: aprovado / aprovado com ressalvas / reprovado
```

### Regras de Decisão sobre o Veredito

1. Se houver QUALQUER achado `[Crítico]` ou `[Importante]`, o veredito deve ser `reprovado`.
2. `aprovado` só é permitido com ZERO achados Críticos ou Importantes.
3. `aprovado com ressalvas` é tratado como reprovação para fins deste ciclo: aplicar correção.
4. Cada achado deve trazer evidência no código (`arquivo:linha`) e referência ao artefato do `${ANALYSIS_PATH}` que sustenta a regra violada.
5. Ler `references/checklist-review.md` para o roteiro genérico de revisão.

## Passo 4: Decidir Próximo Passo

1. Se o veredito for `aprovado`, ir para o Passo 6 (encerramento).
2. Caso contrário, incrementar `AI_INVOCATION_DEPTH += 1` e seguir para o Passo 5.
3. Se `AI_INVOCATION_DEPTH >= 2` sem convergência, parar e seguir o Passo 7 (intervenção manual).

## Passo 5: Etapa de Correção (Skill: bugfix)

Acionar a skill `bugfix` usando o template abaixo, preenchendo todos os campos com dados extraídos dos artefatos do Passo 2 e dos achados do Passo 3.

### Template de Prompt para `bugfix`

```text
Use a skill bugfix para corrigir TODOS os achados da revisao.

Achados a corrigir (da saida da skill review):
- [arquivo:linha] Achado 1: [descricao do problema]
- [arquivo:linha] Achado 2: [descricao do problema]

Comportamento esperado apos a correcao:
- [descricao do comportamento correto para cada achado, extraida dos artefatos]

Invariantes que nao podem mudar:
- contratos publicos: [assinaturas, endpoints ou tipos declarados nos artefatos como invariantes]
- tipos de erro: [erros declarados nos artefatos como contrato]
- comportamento de outros fluxos nao afetados por estes achados

Regras de execucao nao negociaveis:
- identifique a causa raiz de cada achado antes de escrever qualquer linha de codigo
- adicione ou corrija testes de regressao que provem que o bug nao pode regredir
- nao altere comportamento fora do escopo dos achados listados
- ao finalizar: rode os testes, rode o lint e registre o output como evidencia (use os comandos declarados nos artefatos ou detectados no repositorio)
- nao declare o bugfix concluido sem evidencia de que a causa raiz foi eliminada

Saidas esperadas:
- diff com a correcao minima necessaria
- testes de regressao adicionados ou corrigidos
- evidencia de validacao (output dos comandos de teste e lint do projeto)
- descricao da causa raiz de cada achado corrigido
```

### Pós-processamento

1. Validar que a saída do `bugfix` traz diff, testes de regressão, evidência de execução e descrição da causa raiz para cada achado.
2. Se algum item estiver ausente, recusar a entrega parcial e re-acionar `bugfix` apenas para os achados sem evidência.
3. Retornar ao Passo 3 para nova rodada de revisão.

## Passo 6: Encerramento por Aprovação

1. Confirmar que o veredito final é `aprovado` com ZERO achados Críticos ou Importantes.
2. Apresentar resumo executivo:
   - Quantidade de rodadas executadas.
   - Achados resolvidos por categoria.
   - Comandos de teste e lint executados (os detectados ou declarados nos artefatos) e seus resultados finais.
3. Não prosseguir para entrega/PR. Esta skill encerra apenas o ciclo review/bugfix.

## Passo 7: Encerramento por Não Convergência

1. Quando `AI_INVOCATION_DEPTH >= 2` sem alcançar `aprovado`, interromper o ciclo.
2. Solicitar intervenção manual detalhando:
   - Achados que não convergiram.
   - Tentativas de correção aplicadas.
   - Hipóteses sobre o impedimento (lacuna nos artefatos, ambiguidade de RF, restrição técnica, falta de contexto).

## Restrições Não Negociáveis

- **Falsos positivos:** Avaliar cada achado com base em evidência no código e em regra explícita nos artefatos do `${ANALYSIS_PATH}`. Sem essa dupla evidência, o achado não existe.
- **Preguiça:** Revisões superficiais são consideradas falha na tarefa.
- **Escopo:** Não alterar contratos públicos ou comportamentos fora do bug em correção.
- **Agnosticismo total:** Não impor stack, linguagem, comandos, áreas de risco, padrões de qualidade ou checklists que não estejam declarados nos artefatos lidos. Quando faltar informação, perguntar ao usuário em vez de assumir.

## Tratamento de Erros

* **Caminho da pasta não informado:** Não iniciar o ciclo. Reapresentar a pergunta do Passo 1.
* **Caminho não encontrado:** Indicar o caminho ausente e reapresentar a pergunta do Passo 1.
* **Artefatos insuficientes para extrair contexto:** Listar as lacunas e perguntar ao usuário antes de prosseguir. Nunca preencher com defaults.
* **Skill `review` ou `bugfix` indisponível no ambiente:** Parar e informar a dependência ausente.
* **Loop sem convergência (`AI_INVOCATION_DEPTH >= 2`):** Seguir o Passo 7.
* **Falha nos comandos de validação detectados:** Tratar como achado `[Crítico]` e retornar ao Passo 5.
* **Achado sem `arquivo:linha` ou sem referência a artefato:** Recusar o achado e exigir que `review` reapresente com evidência.
