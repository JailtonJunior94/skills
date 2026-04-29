---
name: otel-hybrid-dashboard-blueprint
description: Gera um modelo de dashboard de observabilidade para cenário híbrido Grafana (otel-lgtm) + Coralogix, baseado em OpenTelemetry Semantic Conventions, PromQL portável, queries Loki/DataPrime para logs e TraceQL/Coralogix Tracing para traces. Produz JSON Grafana importável e estrutura equivalente para Coralogix (widgets + queries), com Golden Signals, SLO, alertas e variáveis de serviço, ambiente e região. Aciona quando o usuário pedir blueprint de dashboard híbrido OTel, observabilidade SRE com Grafana e Coralogix, ou padronização de dashboards entre local e produção. Solicita o contexto do serviço antes de gerar o dashboard. Não usar para instrumentação não-OTel, monitoramento puramente de infraestrutura, conversão direta de JSON Grafana para Coralogix, nem para configurar ingestão ou collectors.
---

# Blueprint de Dashboard Híbrido OTel (Grafana + Coralogix)

Gerar um modelo de dashboard de observabilidade pronto para produção, estruturalmente consistente entre Grafana local (otel-lgtm: Prometheus + Loki + Tempo) e Coralogix (PromQL + DataPrime + Tracing + SLO), seguindo OpenTelemetry Semantic Conventions e práticas SRE (Golden Signals + SLO).

## Passo 1: Coletar Contexto do Serviço (OBRIGATÓRIO)

Antes de qualquer geração, **sempre** perguntar ao usuário e aguardar resposta. Não inferir, não usar valores padrão silenciosamente.

1. Solicitar explicitamente os seguintes campos em uma única pergunta:
   - **Nome do serviço** (`service_name`, ex.: `payments-api`)
   - **Tipo do serviço** (ex.: API REST, gRPC, worker, consumer Kafka)
   - **Plataforma de execução** (ex.: Kubernetes, ECS, VM)
   - **Ambientes existentes** (`deployment_environment`, ex.: `dev`, `staging`, `prod`)
   - **Regiões** (ex.: `sa-east-1`, `us-east-1`)
   - **Volume aproximado de requisições** (RPS médio e pico)
   - **SLO alvo** (ex.: 99,9% disponibilidade, P95 < 300ms)
   - **Endpoints críticos** (rotas que precisam de visibilidade dedicada)
   - **Dependências externas** (banco, cache, filas, APIs upstream)
2. Se o usuário não fornecer um campo, perguntar novamente. Não prosseguir sem o contexto mínimo: `service_name`, ambientes, regiões e SLO alvo.
3. Registrar o contexto coletado e usá-lo para preencher variáveis e thresholds nas etapas seguintes.

## Passo 2: Padronizar Labels e Métricas (OBRIGATÓRIO)

1. Usar exclusivamente OpenTelemetry Semantic Conventions. Ler `references/otel-semantic-conventions.md` para a lista canônica de labels e métricas suportadas.
2. Labels obrigatórias em todos os painéis de métricas:
   - `service_name`
   - `deployment_environment`
   - `http.route`
   - `http.method`
   - `http.status_code`
3. Métricas padrão (não inventar nomes nem atributos):
   - `http_server_request_duration_seconds` (histogram)
   - `http_server_requests_total` (counter)
4. Regras de query PromQL:
   - Usar `rate()` para counters
   - Usar `histogram_quantile()` para latência (P95, P99)
   - **NÃO** usar média simples para latência
   - Evitar combinações de labels que aumentem cardinalidade (ex.: `user_id`, `request_id`)
5. As mesmas queries PromQL devem funcionar tanto no Grafana quanto no Coralogix. Validar contra `references/promql-portable-queries.md`.

## Passo 3: Definir Variáveis de Template

Incluir obrigatoriamente:

- `$service` → label `service_name`
- `$env` → label `deployment_environment`
- `$region` → label `region` (ou `cloud_region` conforme semconv)

Variáveis de datasource:

- `${DS_PROMETHEUS}`, `${DS_LOKI}`, `${DS_TEMPO}` no Grafana
- No Coralogix, o datasource é implícito; documentar a equivalência por widget.

## Passo 4: Montar a Estrutura do Dashboard

Gerar exatamente esta estrutura, em ambas as plataformas. Ler `references/dashboard-sections.md` para queries por seção.

### A. Golden Signals
- Request Rate (RPS)
- Error Rate (%)
- Latência P95
- Latência P99
- Saturação (se métricas de runtime/host disponíveis)

### B. Service Health
- Top 10 endpoints mais lentos (P95 por `http.route`)
- Erros por endpoint (`http.status_code` classe `5..` por `http.route`)
- Requests por status code

### C. Logs Deep Dive
- Lista de erros recentes filtrados por `service_name` e `deployment_environment`
- Gerar **duas versões** de query (ver Passo 5)

### D. Traces
- Traces lentos
- Contagem de erros em traces
- Gerar **duas versões** de query (ver Passo 6)

### E. SLO
- Status atual do SLO (good vs total)
- Burn rate (1h e 6h)

## Passo 5: Adaptar Queries de Logs

Logs **não são portáveis**. Gerar duas versões para cada painel da seção C:

1. **Loki (local)**: usar LogQL. Padrão: `{service_name="$service", deployment_environment="$env"} |= "error"`.
2. **DataPrime (Coralogix)**: usar sintaxe DataPrime equivalente. Ler `references/dataprime-queries.md` para mapeamento LogQL → DataPrime.

## Passo 6: Adaptar Queries de Traces

Traces **não são portáveis**. Gerar duas abordagens para cada painel da seção D:

1. **Grafana Tempo**: TraceQL. Ex.: `{ resource.service.name = "$service" && status = error }`.
2. **Coralogix Tracing**: filtro nativo equivalente. Ler `references/coralogix-tracing-filters.md` para o modelo da plataforma.

## Passo 7: Gerar Saídas

### A. Grafana Dashboard JSON
1. Ler `assets/grafana-dashboard-template.json` como esqueleto.
2. Preencher seções A–E com painéis (PromQL + LogQL + TraceQL).
3. Aplicar grid de 24 colunas (stat=6, timeseries=12, table=24).
4. IDs de painéis auto-incrementais a partir de 1.
5. Validar com `python3 scripts/validate-dashboard.py --file <caminho>`.

### B. Estrutura para Coralogix
**Não gerar JSON completo.** Ler `assets/coralogix-structure-template.md` e produzir, por seção:
- Lista de widgets
- Tipo de visualização recomendado
- Queries (PromQL, DataPrime, tracing nativo)
- Variáveis equivalentes

## Passo 8: Definir Alertas

Sugerir thresholds baseados no SLO informado pelo usuário no Passo 1. Defaults quando o usuário não especificar:

- Error rate > 5% por 5 min
- Latência P95 > 500ms por 10 min
- Saturação (CPU ou memória do runtime) > 80% por 10 min

Gerar alertas em ambas as plataformas usando PromQL portável.

## Passo 9: Regras Críticas (Checklist Final)

Antes de entregar, validar:

- [ ] Estrutura idêntica entre plataformas, **implementação adaptada** por backend
- [ ] **NÃO** tentou converter JSON Grafana para Coralogix
- [ ] **NÃO** assumiu portabilidade de logs ou traces
- [ ] Métricas usam apenas PromQL padrão (sem vendor lock-in)
- [ ] Recursos nativos do Coralogix (DataPrime, SLO nativo) usados quando agregam valor
- [ ] Todas as labels obrigatórias presentes
- [ ] Variáveis `$service`, `$env`, `$region` configuradas
- [ ] Alertas com thresholds explícitos

## Tratamento de Erros

* **Contexto do serviço não fornecido:** Não gerar dashboard. Repetir a pergunta do Passo 1 listando apenas os campos faltantes.
* **Métrica solicitada fora do semconv:** Recusar e sugerir o nome canônico equivalente em `references/otel-semantic-conventions.md`.
* **Validação JSON falha:** Ler stderr de `scripts/validate-dashboard.py`, corrigir IDs duplicados, posições de grid ou variáveis de datasource ausentes e revalidar.
* **Usuário pede conversão direta JSON Grafana → Coralogix:** Recusar. Explicar que apenas a estrutura é portável e oferecer regenerar a versão Coralogix a partir do contexto.
