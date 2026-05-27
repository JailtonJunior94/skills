# Checklist de Clarificação para o PRD

A skill `create-prd` do orchestrator exige seis categorias preenchidas antes de redigir o PRD. Esta checklist espelha essas categorias com perguntas-modelo em múltipla escolha (PT-BR) prontas para `AskUserQuestion`. Cada rodada da `tracker-to-prd` deve cobrir lacunas pendentes ou conflitos abertos do confronto com o codebase.

## Critério de Parada
A skill encerra as rodadas e materializa o bundle **somente quando**:
1. Todas as 6 categorias abaixo tiverem status `respondido` na tabela `## Categorias do create-prd` do bundle.
2. Nenhum item da tabela `## Confronto com Codebase` permanecer em `conflicting` sem decisão registrada.

Enquanto qualquer das duas condições falhar, abrir nova rodada com perguntas focadas nos pontos pendentes.

## Categorias Obrigatórias

### 1. Problema e Objetivo
- O que esta funcionalidade resolve hoje que não está resolvido?
- Qual é a dor ou oportunidade primária?

**Pergunta-modelo:**
> Qual é o problema central que esta feature resolve?
- (a) Reduz fricção em fluxo existente (ex.: passos a menos)
- (b) Habilita capacidade ausente hoje
- (c) Corrige regra de negócio incorreta
- (d) Atende exigência regulatória/compliance

### 2. Usuário / Persona Principal
- Quem usa? Qual segmento? Interno vs. externo?

**Pergunta-modelo:**
> Qual é a persona primária impactada?
- (a) Cliente final (externo, autosserviço)
- (b) Operador interno (suporte/back-office)
- (c) Parceiro / integrador via API
- (d) Stakeholder de produto/compliance (relatório)

### 3. Escopo Incluído
- O que entra na primeira versão?

**Pergunta-modelo:**
> Qual recorte é o MVP?
- (a) Caminho feliz somente (1 cenário)
- (b) Caminho feliz + 1 cenário alternativo crítico
- (c) Cobertura plena de casos derivados da US
- (d) Cobertura plena + integrações novas (ampliar escopo)

### 4. Escopo Excluído
- O que explicitamente fica fora?

**Pergunta-modelo:**
> Quais itens ficam fora desta entrega?
- (a) Variações regionais/idiomas adicionais
- (b) Suporte a canais secundários (ex.: mobile, API pública)
- (c) Métricas avançadas / dashboards
- (d) Migração de dados históricos

### 5. Restrições e Conformidade
- Compliance, segurança, performance, integrações obrigatórias.

**Pergunta-modelo:**
> Existem restrições não negociáveis?
- (a) Compliance (LGPD/GDPR/PCI/SOX)
- (b) Performance (latência ≤ X ou throughput ≥ Y)
- (c) Integração obrigatória com sistema legado
- (d) Nenhuma restrição rígida conhecida

### 6. Critérios de Sucesso Mensuráveis
- Como saberemos que entregou valor?

**Pergunta-modelo:**
> Como mediremos o sucesso após o lançamento?
- (a) Métrica de adoção (% de usuários ativando)
- (b) Métrica de conversão / receita (Δ)
- (c) Redução de incidentes / chamados de suporte
- (d) Ainda não definido — precisa de baseline

## Regras de Pergunta
- No máximo 4 perguntas por chamada `AskUserQuestion`.
- Cada opção tem `description` explicando trade-off ou implicação.
- Quando a US ou o Épico já responde a categoria com evidência textual, marcar como `respondido` sem nova pergunta. Citar a evidência no bundle.
- Quando o confronto com o codebase gerar `conflicting`, perguntar primeiro sobre a resolução do conflito antes de prosseguir para próximas categorias.
- Quando o usuário responder `Outro` com texto vazio, repetir a pergunta uma vez antes de encerrar com `needs_input`.
