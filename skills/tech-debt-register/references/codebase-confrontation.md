# Localização de Débito no Codebase

## Objetivo
Localizar onde o débito mora hoje (ou onde a ausência se manifesta) confrontando a descrição do usuário com o codebase informado. O resultado popula a tabela `Localização no Codebase` do `debt.md` e alimenta as rodadas de clarificação.

## Escopo do Codebase
- **Caminho local**: caminho de diretório informado pelo usuário (default `cwd`). Usar `Grep` e `Read`.
- **Repo remoto**: `owner/repo` no GitHub. Usar `gh search code "<termo> repo:<owner>/<repo>" --limit 10` ou `gh api repos/<owner>/<repo>/contents/<path>` quando o path é conhecido.
- **Misto**: aceitar local + remoto quando o débito atravessa dois sistemas.

## Mapeamento Descrição → Termos Buscáveis
Para a descrição do débito, derivar 2 a 4 termos em ordem de especificidade:
1. **Identificadores explícitos do domínio do usuário**: nomes de serviços, endpoints, módulos, classes, eventos citados na descrição.
2. **Termos da taxonomia**: ler `references/debt-taxonomy.md` e usar a lista da natureza correspondente.
3. **Verbos de ação + objeto**: ex.: "validar entrada", "publicar evento", "renovar token".

Evitar termos genéricos (`user`, `service`, `manager`, `handler`) — geram ruído sem sinal.

## Status por Candidato

| Status | Significado | Critério mínimo |
|---|---|---|
| `confirmado` | O débito mora aqui. | Match textual em `path:linha` citável **E** inspeção breve (até 30 linhas em volta) confirmando o anti-padrão. Sem as duas condições, rebaixar para `suspeito`. |
| `suspeito` | Match parcial; precisa de leitura humana. | Match textual em `path:linha`, mas contexto ambíguo ou termo encontrado em comentário/teste/log. |
| `ausente` | Termos não encontrados. | Buscas executadas com 0 hits relevantes. Reforça hipótese de greenfield. |
| `refutado` | Match existe mas o débito **não** se aplica. | Evidência clara de que o comportamento problemático já foi corrigido (PR/commit recente) ou nunca existiu nessa área. |

## Regra Anti-Falso-Positivo (production-ready)
- **Nunca** marcar `confirmado` apenas com base em nome de variável, comentário ou import. Exige inspeção do corpo da função/módulo.
- Match em arquivo de teste, mock, exemplo ou documentação **não** promove a `confirmado` — fica em `suspeito` até confirmação humana.
- Se 80% dos hits caem em `_test.`, `mock`, `fixture` ou `example`, considerar a evidência `suspeito` por padrão.
- Quando houver dúvida, preferir `suspeito` e disparar pergunta de clarificação no Step 4 a marcar `confirmado` precocemente. O custo de um falso positivo (re-trabalho de scoping) é maior que o de uma rodada extra.

## Limites de Custo
- Máximo de **15 chamadas** de Grep/Read/gh por rodada de localização.
- Preferir busca textual a leitura completa de arquivos.
- Ler arquivo inteiro apenas quando o match estiver concentrado em um único local crítico e for necessário para classificar.
- Não navegar a árvore de dependências em profundidade.

## Quando "Pular Confronto" é Aceitável
- Débito puramente externo (ex.: política de retenção de logs em provedor SaaS).
- Débito de documentação ou processo sem expressão no código.
- Skill rodando sem acesso a repositório (situação de exceção; documentar em `Lacunas Observadas`).

Em todos os outros casos, alertar o usuário antes de pular.

## Registro Interno
Manter durante a execução estrutura `{candidato → {status, evidencias[], notas}}`. Cada evidência cita `path:linha` (local) ou URL do GitHub (remoto). Será serializada na seção `Localização no Codebase` do `debt.md`.

## Disparo de Nova Rodada
- Pelo menos um `suspeito` ainda pendente → pergunta de clarificação para promover a `confirmado` ou `refutado`.
- Vários `confirmado` espalhados (ex.: 4 implementações divergentes da mesma lógica) → pergunta sobre referência canônica e escopo do débito.
- `ausente` com hipótese greenfield → confirmar com o usuário se a entrega é "criar do zero" antes de prosseguir aos eixos 4-8.
