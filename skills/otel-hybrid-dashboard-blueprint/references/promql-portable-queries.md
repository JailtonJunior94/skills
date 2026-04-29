# Queries PromQL Portáveis (Grafana otel-lgtm + Coralogix)

Todas as queries devem funcionar nos dois ambientes sem modificação. Filtros sempre incluem `service_name`, `deployment_environment` e (quando aplicável) `region`.

## Filtro Base

```
{service_name="$service", deployment_environment="$env", region="$region"}
```

## Golden Signals

### Request Rate (RPS)
```
sum by (service_name) (
  rate(http_server_request_duration_seconds_count{service_name="$service", deployment_environment="$env"}[$__rate_interval])
)
```

### Error Rate (%)
```
100 *
sum(rate(http_server_request_duration_seconds_count{service_name="$service", deployment_environment="$env", http_status_code=~"5.."}[$__rate_interval]))
/
sum(rate(http_server_request_duration_seconds_count{service_name="$service", deployment_environment="$env"}[$__rate_interval]))
```

### Latência P95
```
histogram_quantile(0.95,
  sum by (le, http_route) (
    rate(http_server_request_duration_seconds_bucket{service_name="$service", deployment_environment="$env"}[$__rate_interval])
  )
)
```

### Latência P99
```
histogram_quantile(0.99,
  sum by (le) (
    rate(http_server_request_duration_seconds_bucket{service_name="$service", deployment_environment="$env"}[$__rate_interval])
  )
)
```

### Saturação (CPU)
```
avg by (service_name) (
  process_cpu_utilization{service_name="$service", deployment_environment="$env"}
)
```

## Service Health

### Top 10 endpoints mais lentos (P95)
```
topk(10,
  histogram_quantile(0.95,
    sum by (le, http_route) (
      rate(http_server_request_duration_seconds_bucket{service_name="$service", deployment_environment="$env"}[$__rate_interval])
    )
  )
)
```

### Erros por endpoint
```
sum by (http_route) (
  rate(http_server_request_duration_seconds_count{service_name="$service", deployment_environment="$env", http_status_code=~"5.."}[$__rate_interval])
)
```

### Requests por status code
```
sum by (http_status_code) (
  rate(http_server_request_duration_seconds_count{service_name="$service", deployment_environment="$env"}[$__rate_interval])
)
```

## SLO

### Good vs Total events (latência < 300ms)
```
sum(rate(http_server_request_duration_seconds_bucket{service_name="$service", deployment_environment="$env", le="0.3"}[$__rate_interval]))
/
sum(rate(http_server_request_duration_seconds_count{service_name="$service", deployment_environment="$env"}[$__rate_interval]))
```

### Burn rate 1h
```
(1 -
  sum(rate(http_server_request_duration_seconds_count{service_name="$service", deployment_environment="$env", http_status_code!~"5.."}[1h]))
  /
  sum(rate(http_server_request_duration_seconds_count{service_name="$service", deployment_environment="$env"}[1h]))
) / (1 - 0.999)
```

## Regras

- Sempre `rate()` em counters e `_count`/`_bucket` de histograms.
- Sempre `histogram_quantile()` para latência.
- Nunca dividir `_sum` por `_count` para reportar latência ao usuário (média mascara cauda).
- Usar `$__rate_interval` (Grafana) ou `[5m]` no Coralogix se a variável não existir.
