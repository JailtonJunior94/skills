# Queries de Logs — Loki (local) ↔ DataPrime (Coralogix)

Logs **não** são portáveis. Sempre gerar as duas versões.

## Erros recentes do serviço

### Loki (LogQL)
```
{service_name="$service", deployment_environment="$env"}
  | json
  | severity=~"ERROR|FATAL"
```

### DataPrime (Coralogix)
```
source logs
| filter $d.service_name == '$service' && $d.deployment_environment == '$env'
| filter $m.severity in ('ERROR', 'FATAL')
| orderby $m.timestamp desc
| limit 200
```

## Erros por endpoint (top 10)

### Loki
```
topk(10,
  sum by (http_route) (
    count_over_time({service_name="$service", deployment_environment="$env"} |= "ERROR" [$__interval])
  )
)
```

### DataPrime
```
source logs
| filter $d.service_name == '$service' && $d.deployment_environment == '$env'
| filter $m.severity == 'ERROR'
| groupby $d.http_route aggregate count() as errors
| orderby errors desc
| limit 10
```

## Mensagens contendo padrão

### Loki
```
{service_name="$service"} |= "timeout"
```

### DataPrime
```
source logs
| filter $d.service_name == '$service'
| filter $d.message ~ 'timeout'
```

## Regras

- Em DataPrime, `$d` referencia atributos do payload (resource + span attrs); `$m` referencia metadados (`severity`, `timestamp`).
- Em Loki, labels precisam ter sido promovidos a stream labels no pipeline. Se não estiverem, usar `| json | label=value`.
- Não tentar reusar a mesma string entre os dois backends.
