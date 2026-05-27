# Roteiro Genérico de Revisão Crítica

Aplicar este roteiro durante o Passo 3 (Etapa de Revisão Crítica) do `SKILL.md`. **Este roteiro é apenas um guia de perguntas genéricas.** Cada pergunta só vira achado se houver evidência no código (`arquivo:linha`) **e** respaldo em algum artefato dentro de `${ANALYSIS_PATH}`. Sem essa dupla evidência, o item é falso positivo e deve ser descartado.

## Como Usar
1. Ler todos os artefatos de `${ANALYSIS_PATH}` antes de aplicar qualquer pergunta.
2. Para cada eixo abaixo, traduzir as perguntas em verificações concretas usando apenas o que os artefatos declararem.
3. Se um eixo não for endereçado pelos artefatos, ignorá-lo. **Não introduzir regras que não estejam nos artefatos.**

## Eixos de Verificação (perguntas genéricas)

### 1. Corretude Funcional
- Os RFs e critérios de aceite descritos nos artefatos foram atendidos?
- O comportamento implementado coincide com o descrito?
- Os casos de borda explícitos nos artefatos foram tratados?

### 2. Regressão e Contratos
- Houve mudança em alguma assinatura, endpoint, contrato de mensagem, schema, tipo de erro ou comportamento declarado como invariante nos artefatos?
- Existem migrações ou flags novas? O comportamento padrão é seguro segundo o que os artefatos exigem?

### 3. Segurança
- O código viola alguma regra de segurança declarada nos artefatos (validação obrigatória, tratamento de dado sensível, autorização, etc.)?
- Inputs externos referenciados pelos artefatos estão validados antes do uso?

### 4. Concorrência e Arquitetura
- O código respeita as decisões arquiteturais descritas nos artefatos?
- Recursos com ciclo de vida têm critério de término coerente com o que os artefatos definem?

### 5. Cobertura de Testes
- Os cenários listados no critério de pronto dos artefatos têm teste correspondente?
- Há cenários de erro e edge cases relevantes (segundo os artefatos) sem cobertura?

### 6. Dívida Técnica
- Foi introduzida complexidade não justificada pelos artefatos?
- Existe código morto, duplicação ou abstração prematura sem respaldo nos artefatos?

### 7. Observabilidade
- Os requisitos de observabilidade descritos nos artefatos (logs, métricas, traces) foram cumpridos?

## Classificação dos Achados
- **`[Crítico]`**: Viola regra obrigatória explícita nos artefatos, quebra contrato declarado invariante, ou falha em RF marcado como obrigatório.
- **`[Importante]`**: Viola regra ou expectativa declarada nos artefatos sem caráter bloqueante imediato, ou deixa cenário relevante do critério de pronto sem cobertura.
- **`[Sugestão]`**: Melhoria opcional alinhada ao espírito dos artefatos, sem regra explícita violada.

## Formato Obrigatório do Achado
```
[Crítico|Importante|Sugestão] caminho/arquivo.ext:linha
  Descrição: <o que está errado>
  Artefato de referência: <arquivo dentro de ${ANALYSIS_PATH} e trecho que sustenta a regra>
  Correção sugerida: <ação mínima recomendada>
```

## Regra Anti-Falso-Positivo
Se um achado não puder citar um trecho específico de um artefato de `${ANALYSIS_PATH}` que sustente a regra violada, ele **não é um achado**. Descartar.
