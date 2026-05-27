# Detecção Determinística de Épico Duplicado via WIQL

Substitui heurísticas subjetivas de "X% similar" por comparação programática.

## Estratégia

1. Normalizar o título do bundle com `scripts/normalize-title.py --json`.
2. Extrair `distinctive_token` (token mais longo, sem stopword).
3. Construir WIQL filtrando candidatos no projeto.
4. Para cada candidato retornado, normalizar o título usando o mesmo script.
5. Comparar `normalized` do bundle com `normalized` do candidato.
6. Match exato (igualdade de string) marca duplicata. Sem match → seguir para criação.

## WIQL Padrão

```
SELECT [System.Id], [System.Title], [System.State]
FROM WorkItems
WHERE
    [System.TeamProject] = @project
    AND [System.WorkItemType] = '<epicType>'
    AND [System.State] <> 'Closed'
    AND [System.State] <> 'Removed'
    AND [System.Title] CONTAINS '<distinctive_token>'
ORDER BY [System.ChangedDate] DESC
```

Substituir `<epicType>` pelo tipo detectado em `references/ado-process-types.md` e `<distinctive_token>` pela saída do script de normalização.

## Critério de Match

```
bundle_normalized == candidate_normalized
```

Por que igualdade após normalização (e não similaridade fuzzy):
- **Determinístico**: mesma entrada → mesmo resultado em qualquer execução, qualquer agente, qualquer máquina.
- **Sem falso positivo**: títulos diferentes mas com palavras parecidas não casam (ex.: "Autenticação self-service" vs "Autenticação corporativa" → tokens distintivos diferem).
- **Sem falso negativo trivial**: stopwords e acentos não atrapalham. "Autenticação Self-Service" e "autenticacao self service" produzem o mesmo `normalized`.

## Quando o Token Distintivo Retorna Muitos Candidatos

Se a query retornar mais de 50 itens (limiar prático), o token distintivo é pouco discriminante. Estratégia:
1. Pegar o segundo token mais longo dos `raw_tokens` e rodar nova WIQL filtrando por ambos via `CONTAINS WORDS`.
2. Comparar `normalized` apenas dos candidatos refinados.

## Quando Não Há Candidatos

WIQL vazio significa nenhum épico aberto com o token. Seguir para criação direta — não há duplicata.

## Item Reutilizado vs Novo

Quando o usuário escolhe "Reutilizar épico existente":
- Usar `epicId` do candidato matched para vincular as US.
- Não modificar o épico existente (sem editar título, descrição ou área).
- Audit log registra `reused: true` e `matched_normalized_title`.

Quando o usuário escolhe "Criar novo mesmo assim":
- Audit log registra `force_create: true` e o `epicId` do candidato que foi ignorado.
- Útil para épicos que coincidem no título mas pertencem a contextos distintos (ex.: refatoração em domínios diferentes).
