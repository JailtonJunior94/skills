# Estrutura Equivalente para Coralogix

> Não gerar JSON Grafana. Documentar a estrutura widget a widget.

## Variáveis (Coralogix Custom Dashboards)

- `$service` → label PromQL `service_name`
- `$env` → label PromQL `deployment_environment`
- `$region` → label PromQL `region`

## Seção A — Golden Signals

| Widget | Tipo | Datasource | Query |
|---|---|---|---|
| Request Rate | Single Stat | Prometheus (Coralogix) | (PromQL Request Rate) |
| Error Rate (%) | Single Stat | Prometheus | (PromQL Error Rate) |
| Latência P95 | Single Stat | Prometheus | (PromQL P95) |
| Latência P99 | Single Stat | Prometheus | (PromQL P99) |
| Saturação | Gauge | Prometheus | (PromQL Saturação) |

## Seção B — Service Health

| Widget | Tipo | Datasource | Query |
|---|---|---|---|
| Top 10 endpoints lentos | Bar Chart | Prometheus | (PromQL Top 10) |
| Erros por endpoint | Time Series | Prometheus | (PromQL Erros por endpoint) |
| Requests por status code | Stacked Time Series | Prometheus | (PromQL Status code) |

## Seção C — Logs Deep Dive

| Widget | Tipo | Datasource | Query |
|---|---|---|---|
| Erros recentes | Logs Table | Logs (DataPrime) | (DataPrime erros) |
| Erros por endpoint | Bar Chart | Logs (DataPrime) | (DataPrime top10) |

## Seção D — Traces

| Widget | Tipo | Datasource | Query |
|---|---|---|---|
| Traces lentos | Spans Table | Tracing (Coralogix) | duration > 1s + filtros |
| Erros em traces | Time Series | Tracing / DataPrime spans | status=error |

## Seção E — SLO

Usar **SLO nativo do Coralogix** quando possível:
- Definir SLI: bom = `http_status_code !~ "5.." AND duration < threshold`
- SLO target conforme contexto fornecido pelo usuário
- Burn rate alerts em janelas de 1h e 6h

Quando o SLO nativo não for usado, replicar as queries PromQL de SLO em widgets Time Series.
