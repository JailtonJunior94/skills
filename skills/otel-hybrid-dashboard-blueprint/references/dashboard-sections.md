# Estrutura de Seções do Dashboard

Cinco seções obrigatórias, na ordem.

## A. Golden Signals (linha 1)

| Painel | Tipo | Largura | Query |
|---|---|---|---|
| Request Rate | stat / timeseries | 6 | ver `promql-portable-queries.md` → Request Rate |
| Error Rate (%) | stat | 6 | Error Rate |
| Latência P95 | stat | 6 | P95 |
| Latência P99 | stat | 6 | P99 |
| Saturação | gauge | 6 | Saturação CPU |

## B. Service Health (linha 2)

| Painel | Tipo | Largura | Query |
|---|---|---|---|
| Top 10 endpoints mais lentos (P95) | table | 12 | Top 10 endpoints |
| Erros por endpoint | timeseries | 12 | Erros por endpoint |
| Requests por status code | timeseries | 24 | Requests por status |

## C. Logs Deep Dive (linha 3)

| Painel | Tipo | Largura | Local (Loki) | Prod (DataPrime) |
|---|---|---|---|---|
| Erros recentes | logs | 24 | LogQL erros | DataPrime erros |
| Erros por endpoint | bar chart | 12 | LogQL top10 | DataPrime top10 |

## D. Traces (linha 4)

| Painel | Tipo | Largura | Local (Tempo) | Prod (Coralogix) |
|---|---|---|---|---|
| Traces lentos | traces / table | 12 | TraceQL > 1s | Coralogix duration > 1s |
| Erros em traces | timeseries | 12 | TraceQL status=error | Coralogix status=error |

## E. SLO (linha 5)

| Painel | Tipo | Largura | Query |
|---|---|---|---|
| Status SLO atual | gauge | 8 | Good/Total |
| Good vs Total events | timeseries | 8 | Good vs Total |
| Burn rate 1h / 6h | stat | 8 | Burn rate |
