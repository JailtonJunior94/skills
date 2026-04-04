# Agent Skills

Coleção de skills reutilizáveis para agentes de IA — Claude Code, Gemini CLI, GitHub Copilot e Cursor.

## Sobre

Skills são instruções estruturadas que ensinam agentes de IA a executar tarefas específicas com qualidade consistente. Cada skill define um fluxo de trabalho completo: desde a validação da entrada até a entrega do resultado.

Este repositório reúne skills voltadas para o dia a dia de desenvolvimento de software: correção de bugs, code review, criação de PRs, refatoração e mais.

## Skills Disponíveis

| Skill | Descrição |
|-------|-----------|
| **bugfix** | Correção de bugs pela causa raiz com testes de regressão obrigatórios |
| **jira-tasks** | Integração e automação de tarefas do Jira |
| **pull-request** | Criação de Pull Requests com descrição estruturada |
| **refactor** | Refatoração de código com foco em legibilidade e manutenção |
| **reviewer** | Revisão técnica de código com foco em boas práticas |
| **semantic-commit** | Geração de mensagens no padrão Conventional Commits |
| **us-to-prd** | Conversão de User Stories para PRDs técnicos |
| **postman-collection-generator** | Geração de collections do Postman a partir de APIs |
| **skill-best-practices** | Boas práticas para criação de skills reutilizáveis |

## Instalação

```bash
npx skills add https://github.com/JailtonJunior94/skills
```

Ou instale manualmente:

```bash
# Copia uma skill específica
cp -r skills/bugfix ~/.claude/skills/bugfix

# Ou cria um link simbólico para toda a coleção
ln -s $(pwd)/skills ~/.claude/skills
```

## Uso

Após a instalação, as skills ficam disponíveis para o agente de IA automaticamente. Basta referenciá-las em seu prompt:

```
Use a skill bugfix para corrigir o erro no arquivo main.go
```

```
Use a skill semantic-commit para gerar a mensagem de commit
```

```
Use a skill reviewer para revisar o código deste PR
```

## Estrutura do Repositório

```
skills/
├── bugfix/SKILL.md
├── jira-tasks/SKILL.md
├── pull-request/SKILL.md
├── refactor/SKILL.md
├── reviewer/SKILL.md
├── semantic-commit/SKILL.md
├── us-to-prd/SKILL.md
├── postman-collection-generator/SKILL.md
└── skill-best-practices/SKILL.md
```

Cada skill é definida em um arquivo `SKILL.md` com frontmatter YAML (`name`, `description`) seguido das instruções de comportamento.

## Criando uma Nova Skill

1. Crie um diretório em `skills/<nome-da-skill>/`
2. Adicione um arquivo `SKILL.md` com o frontmatter:

```yaml
---
name: minha-skill
description: |
  Descrição do que a skill faz.
  Quando usar e quando não usar.
---
```

3. Defina os procedimentos, regras e formato de saída no corpo do arquivo.

## Contribuição

Contribuições são bem-vindas! Para adicionar uma nova skill ou melhorar uma existente:

1. Faça um fork do repositório
2. Crie uma branch para sua alteração
3. Siga a estrutura existente das skills como referência
4. Abra um Pull Request com a descrição da mudança

## Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo [`LICENSE`](LICENSE) para mais informações.
