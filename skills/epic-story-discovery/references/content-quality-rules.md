# Regras de Qualidade de Conteúdo (sem falso positivo)

Estas regras são aplicadas pelo `scripts/validate-bundle.py`. Foram desenhadas para detectar conteúdo claramente não preenchido SEM bloquear prosa legítima que apenas contenha palavras semelhantes.

## Princípio de Não-Falso-Positivo

Toda regra abaixo:
1. Opera sobre **linhas inteiras** após strip de whitespace e marcador de bullet (`-`, `*`, `+`, `1.`).
2. Compara com **igualdade exata** (case-insensitive) contra um conjunto fechado de placeholders proibidos.
3. Para placeholders entre colchetes, exige que a **linha inteira** seja apenas o colchete — não flagga colchetes dentro de prosa.
4. **Não usa substring match** sobre frases comuns. Texto como "É necessário definir o critério mínimo" NÃO é flaggado.

## Placeholders Proibidos por Linha Inteira

Após strip de bullet e whitespace, a linha (em uppercase) é flaggada apenas se for **igual** a um destes valores:

- `TBD`
- `A DEFINIR`
- `A CONFIRMAR`
- `PENDENTE`
- `N/A`
- `?`
- `-`
- `...`

Casos NÃO flaggados (intencionalmente, para evitar falso positivo):
- `É necessário a definir-se um padrão` — substring, não linha inteira.
- `Status: pendente de aprovação` — substring.
- `Resposta esperada: N/A para usuários sem conta` — substring em prosa.

## Linhas Bracket-Only

Uma linha é flaggada como placeholder bracket-only quando, após strip de bullet/whitespace, ela:
1. Inicia com `[`.
2. Termina com `]`.
3. **Não** é um checkbox markdown válido (`[ ]`, `[x]`, `[X]`).

Regex de referência usada pelo validador:
```
^\s*(?:[-*+]|\d+\.)?\s*\[(?![ xX]?\s*\]).+\]\s*$
```

Casos flaggados (corretamente):
- `[persona]`
- `[Domínio/Produto] + [objetivo estratégico]` — linha inicia com `[` e termina com `]`, falsamente parece prosa porque tem `+` no meio mas é o padrão do template não preenchido.
- `- [regra de negócio 1]`
- `[valor]`

Casos NÃO flaggados (intencionalmente):
- `- [ ] Critério atendido` — checkbox vazio com conteúdo, válido markdown.
- `- [x] Critério atendido` — checkbox marcado.
- `Ver documentação em [Confluence/Acesso] para detalhes` — colchete em meio à prosa, linha não termina em `]` sozinha.
- `Use [Wiki] como referência` — idem.

## Seções Críticas (placeholders bloqueiam materialização)

Para o **épico**:
- `## Título`
- `## Objetivo do Negócio`
- `## Hipótese de Valor`
- `## Escopo`
- `## Critérios de Aceite do Épico`
- `## KPIs / Métricas de Sucesso`

Para cada **User Story**:
- `## Título`
- `## Descrição`
- `## Contexto / Regras de Negócio`
- `## Critérios de Aceite`

Seções não críticas (Stakeholders, Observações Técnicas, Releases/Marcos) podem ficar com placeholder sem bloquear, mas o validador emite warning informativo.

## Verificações Estruturais Adicionais

**Épico**:
- Todas as 13 seções obrigatórias do template presentes.
- Seções críticas não vazias.

**User Story**:
- Todas as 7 seções obrigatórias do template presentes.
- Bloco Como/Quero/Para presente na descrição (verificado por keywords exatas).
- Cenários de aceite contêm `Dado que`, `Quando`, `Então` (mínimo um cenário válido).
- Pelo menos um cenário de exceção/erro (heurística: presença de palavras como `Exceção`, `Erro`, `Inválid`).

## Por que essas regras

Regras anteriores em validadores genéricos costumam falhar em dois extremos:
1. **Muito permissivas** — passam rascunhos com `TBD` em campos críticos.
2. **Muito agressivas** — flaggam prosa legítima que contém substring "pendente" ou colchete em link.

Este conjunto evita ambos: igualdade exata por linha + bracket-only ancorado no início/fim da linha. Cobre o caso real (template não preenchido) sem bloquear escrita natural em PT-BR.
