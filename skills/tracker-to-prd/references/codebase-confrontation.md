# Confronto de Requisitos com o Codebase

## Objetivo
Para cada requisito extraído da US ou do Épico, decidir se o codebase do usuário **já cobre**, **cobre parcialmente**, **não cobre** ou **conflita** com o requisito. O resultado alimenta as rodadas de clarificação e a tabela final do bundle.

## Escopo do Codebase
- **Caminho local**: caminho de diretório informado pelo usuário (default `cwd`). Usar `Grep` e `Read` para inspeção.
- **Repo remoto**: `owner/repo` no GitHub. Usar `gh api repos/<owner>/<repo>/contents/<path>` para listar ou `gh search code "<termo> repo:<owner>/<repo>"` para buscar. Restringir a `--limit 10` em buscas.
- **Misto**: aceitar local + remoto simultaneamente quando o requisito atravessa dois sistemas (ex.: front-end local + back-end remoto).

## Mapeamento Requisito → Termos Buscáveis
Para cada requisito, derivar 1 a 3 termos buscáveis em ordem de especificidade:
1. **Identificadores explícitos**: nomes de serviços, endpoints, tabelas, eventos, feature flags citados no requisito.
2. **Substantivos próprios**: termos de negócio (ex.: "Onboarding", "Cancelamento Antecipado", "Cashback").
3. **Verbos de ação + objeto**: ex.: "validar CPF", "publicar evento", "enviar e-mail de confirmação".

Evitar termos genéricos (`user`, `service`, `manager`, `handler`) — geram ruído sem sinal.

## Sinais de Cobertura

| Sinal | Veredito |
|---|---|
| Função/rota/módulo com nome alinhado ao requisito + teste cobrindo o caminho feliz | `covered` |
| Função existente mas faltando branch, validação, evento ou persistência citados no requisito | `partial` |
| Nenhum match para os termos de especificidade alta | `absent` |
| Match existente, porém regra atual contradiz o requisito (ex.: bloqueia onde a US permite, ou vice-versa) | `conflicting` |

## Limites de Custo
- Máximo de **15 chamadas de Grep/Read/gh** por rodada de confronto. Cada chamada deve testar um termo distinto.
- Preferir busca textual (`Grep` ou `gh search code`) a leitura completa de arquivos. Ler arquivo inteiro apenas quando o match estiver concentrado em um único local crítico.
- Não navegar a árvore de dependências em profundidade. Se o ponto de entrada existe, marcar `covered` ou `partial` sem seguir os imports.

## Quando "Pular Confronto" é Aceitável
- Bug fix em arquivo único já identificado pelo usuário.
- Mudança puramente cosmética (texto, label, cor) sem regra de negócio nova.
- Skill rodando sem acesso a repositório (situação de exceção; documentar em `Lacunas Observadas`).

Em todos os outros casos, alertar o usuário antes de pular e seguir apenas após resposta explícita.

## Registro Interno
Manter durante a execução uma estrutura `{requisito → {status, evidencias[], conflito_detalhe}}` que será serializada para `assets/context-template.md` na seção `## Confronto com Codebase`. Cada evidência deve citar `path:linha` ou URL do GitHub.

## Disparo de Nova Rodada
- Cada item em `conflicting` exige pelo menos uma pergunta de clarificação na rodada seguinte para decidir entre: ajustar requisito, ajustar codebase em escopo de outra US, ou aceitar incompatibilidade explícita.
- Itens em `partial` viram pergunta de clarificação somente se a US não declarar claramente o gap.
- Itens em `absent` viram pergunta quando o requisito implica entrega completamente nova e o usuário não definiu critérios de aceite suficientes.
