# Traces — Tempo (TraceQL) ↔ Coralogix Tracing

Traces **não** são portáveis. Gerar as duas abordagens.

## Traces lentos (> 1s)

### Tempo (TraceQL)
```
{ resource.service.name = "$service" && resource.deployment.environment = "$env" && duration > 1s }
```

### Coralogix Tracing
Filtro nativo (UI / API):
```
service.name: "$service"
deployment.environment: "$env"
duration: ">1000ms"
```

DataPrime equivalente sobre o índice de spans:
```
source spans
| filter $d.service_name == '$service' && $d.deployment_environment == '$env'
| filter $m.duration > 1000
| orderby $m.duration desc
| limit 50
```

## Traces com erro

### Tempo
```
{ resource.service.name = "$service" && status = error }
```

### Coralogix
```
service.name: "$service"
status: "error"
```

DataPrime:
```
source spans
| filter $d.service_name == '$service' && $m.status == 'error'
| groupby $d.http_route aggregate count() as error_spans
| orderby error_spans desc
```

## Contagem de erros em traces (timeseries)

### Tempo
```
{ resource.service.name = "$service" && status = error } | count_over_time() by (resource.service.name)
```

### Coralogix
Usar painel de série temporal sobre o índice de spans agregando por `service.name` com filtro `status = error`.

## Regras

- Em TraceQL, atributos de resource têm prefixo `resource.`; atributos de span vêm sem prefixo.
- No Coralogix Tracing, a query nativa é Lucene-like; DataPrime sobre spans cobre análises avançadas.
- Não assumir que TraceQL é executável no Coralogix.
