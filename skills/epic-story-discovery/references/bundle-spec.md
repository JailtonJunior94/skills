# Especificação do Bundle de Discovery

Contrato consumido por skills downstream (ex.: `azure-devops-epic-stories`, integrações Jira/GitHub/Confluence). Manter compatibilidade. Mudanças incompatíveis exigem versionamento.

## Versão Atual
`1`

## Estrutura de Diretório
```
discoveries/
└── epic-<slug>/
    ├── bundle.json
    ├── epic.md
    ├── transcript.md
    └── us/
        ├── 01_<slug-us>.md
        ├── 02_<slug-us>.md
        └── ...
```

## `bundle.json`

```json
{
  "version": 1,
  "slug": "auth-self-service",
  "title": "Autenticação self-service para clientes finais",
  "created_at": "2026-05-27T14:32:11Z",
  "language": "pt-BR",
  "epic": {
    "file": "epic.md",
    "title": "Autenticação self-service para clientes finais"
  },
  "user_stories": [
    {
      "local_id": "01",
      "slug": "recuperar-senha-por-email",
      "title": "Cliente recupera senha por e-mail",
      "file": "us/01_recuperar-senha-por-email.md"
    },
    {
      "local_id": "02",
      "slug": "desbloquear-conta-bloqueada",
      "title": "Cliente desbloqueia conta após múltiplas tentativas",
      "file": "us/02_desbloquear-conta-bloqueada.md"
    }
  ]
}
```

### Campos obrigatórios
- `version` (int) — número da versão do contrato.
- `slug` (string kebab-case) — identificador único do bundle no projeto.
- `title` (string) — título humano do épico em PT-BR.
- `created_at` (string ISO 8601 UTC com `Z`) — timestamp de criação.
- `language` (string) — sempre `pt-BR` neste skill.
- `epic.file` (string) — caminho relativo dentro do bundle (`epic.md`).
- `epic.title` (string) — espelha o título da seção `## Título` do `epic.md`.
- `user_stories[]` (array) — lista ordenada por `local_id`.
  - `local_id` (string `NN` com dois dígitos) — ordem dentro do bundle.
  - `slug` (string kebab-case) — slug da US.
  - `title` (string) — título humano da US em PT-BR.
  - `file` (string) — caminho relativo dentro do bundle.

### Campos opcionais
- `target_hints` (objeto) — sugestões opcionais para skills consumidoras:
  - `azure_devops`: `{ "organization": "...", "project": "...", "board": "..." }`
  - `jira`: `{ "project_key": "..." }`
- `tags` (array de strings) — tags livres.

## `epic.md`
Markdown seguindo `assets/epic-template.md`. Todas as seções obrigatórias presentes e seções críticas preenchidas conforme `references/content-quality-rules.md`.

## `us/<num>_<slug>.md`
Markdown seguindo `assets/user-story-template.md`. Mesmas regras de qualidade do épico.

## `transcript.md`
Markdown livre com blocos numerados por rodada:
```
## Contexto Inicial
...

## Rodada 1
### Pergunta 1: ...
- Opção escolhida: ...
- Justificativa: ...

## Rodada 2
...
```

## Garantias Contratuais
- Encoding sempre UTF-8.
- Quebras de linha LF.
- Caminhos sempre relativos ao diretório do bundle, usando `/`.
- Nomes de arquivos US prefixados com `NN_` em dois dígitos para garantir ordem lexicográfica.
