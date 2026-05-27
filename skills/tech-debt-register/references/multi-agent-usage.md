# Uso Multi-Agente

A skill é nativa em Claude Code. Para Codex CLI, Gemini CLI e Copilot CLI, aplicar os fallbacks descritos aqui antes de executar.

## Capacidades por Agente

| Capacidade | Claude Code | Codex CLI | Gemini CLI | Copilot CLI |
|---|---|---|---|---|
| Loader nativo de `SKILL.md` | Sim | Não — carregar como prompt | Via slash command custom em `.gemini/commands/` | Não — carregar como prompt |
| `AskUserQuestion` (múltipla escolha estruturada) | Sim | Não — usar texto livre estruturado | Não — usar texto livre estruturado | Não — usar texto livre estruturado |
| `Grep` / `Read` locais | Sim | Sim (busca/leitura de arquivos) | Sim | Sim |
| `gh` CLI | Sim | Sim | Sim | Sim |
| MCP genérico | Sim | Sim (com config) | Sim (com config) | Limitado |

## Fallbacks Obrigatórios

### Fallback 1 — Sem `AskUserQuestion`
Quando o agente não suporta múltipla escolha estruturada, formatar a pergunta como bloco em texto livre. Manter número da rodada, cabeçalho do eixo, e opções `a`, `b`, `c`, `d` com a mesma `description` da versão estruturada.

Exemplo (Codex / Gemini / Copilot):

```
[Rodada 2 — Eixo 5: Severidade]
Qual é a severidade?
a) Alta — risco material em curto prazo (incidente, perda de receita, exposição)
b) Média — degrada qualidade contínua (retrabalho, lentidão crônica)
c) Baixa — irritação esporádica sem impacto material
Outro: descreva em texto.

Responda com a letra (ou "Outro: <texto>"). Pode responder múltiplas perguntas em um único bloco.
```

Validar a resposta antes de seguir. Se vier `Outro` vazio, repetir uma vez e encerrar com `needs_input` na falha.

### Fallback 2 — Loader não-nativo
Quando o agente não carrega `SKILL.md` automaticamente, o usuário deve invocar com prompt explícito:

```
Siga o procedimento em skills/tech-debt-register/SKILL.md.
Quando o passo pedir AskUserQuestion, use blocos em texto livre conforme references/multi-agent-usage.md.
Materialize os artefatos em .specs/tech-debt-<slug>/.
```

### Fallback 3 — MCP indisponível
A skill **não depende** de MCP externo para o fluxo principal. As únicas ferramentas externas usadas são `Grep`/`Read` (local) e `gh` (remoto). Se `gh` não estiver autenticado, encerrar com `blocked` orientando `gh auth status`.

## Restrições Conhecidas
- **Copilot CLI** não tem padrão estável para slash commands customizados em 2026. Tratar como executor manual.
- **Codex CLI** usa `AGENTS.md`/`.codex/config.toml`; verificar se o repositório do usuário já registra a skill nessa convenção antes de invocar.
- **Gemini CLI** suporta slash command via `.gemini/commands/<x>.toml`; o owner do repositório precisa criar o arquivo apontando para `SKILL.md`.

## Garantias de Determinismo
Independente do agente, manter:
- Cap de 15 buscas/rodada no Step 3.
- Cap honesto de 3 rodadas sem progresso no Step 4.
- Anti-falso-positivo: `confirmado` exige `path:linha` + inspeção contextual (ver `references/codebase-confrontation.md`).
- Bundle final escrito em `.specs/tech-debt-<slug>/` independentemente do agente.
