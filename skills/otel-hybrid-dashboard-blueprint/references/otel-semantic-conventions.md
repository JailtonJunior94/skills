# OpenTelemetry Semantic Conventions — Referência Canônica

Use apenas os nomes desta lista. Não inventar métricas ou atributos.

## Labels (Resource + Span/Metric Attributes)

### Identidade do Serviço
- `service.name` → `service_name`
- `service.namespace` → `service_namespace`
- `service.instance.id` → `service_instance_id`
- `service.version` → `service_version`
- `deployment.environment` → `deployment_environment`

### Plataforma / Cloud
- `cloud.region` → `cloud_region`
- `cloud.provider` → `cloud_provider`
- `k8s.namespace.name` → `k8s_namespace_name`
- `k8s.pod.name` → `k8s_pod_name`
- `k8s.container.name` → `k8s_container_name`

### HTTP
- `http.route` → `http_route`
- `http.method` (legacy) ou `http.request.method` → `http_method` / `http_request_method`
- `http.status_code` ou `http.response.status_code` → `http_status_code` / `http_response_status_code`
- `http.scheme` → `http_scheme`
- `url.path`, `url.full`

### RPC / gRPC
- `rpc.system`, `rpc.service`, `rpc.method`
- `rpc.grpc.status_code`

### Banco de Dados
- `db.system`, `db.name`, `db.operation`, `db.statement`

### Mensageria
- `messaging.system`, `messaging.destination.name`, `messaging.operation`

## Métricas Padrão

### HTTP Server
- `http.server.request.duration` (histogram, segundos)
  → exposto como `http_server_request_duration_seconds_bucket|sum|count`
- `http.server.active_requests` (updowncounter)
- `http.server.request.body.size` (histogram)
- `http.server.response.body.size` (histogram)

Métrica legada (instrumentações antigas):
- `http_server_requests_total` (counter, equivalente a `_count` do histogram)

### HTTP Client
- `http.client.request.duration`
- `http.client.request.body.size`
- `http.client.response.body.size`

### RPC
- `rpc.server.duration` / `rpc.client.duration`

### Runtime (process / runtime / system)
- `process.cpu.utilization`
- `process.memory.usage`
- `runtime.go.gc.duration` (Go)
- `runtime.jvm.memory.used` (Java)

## Conversão OTel → Prometheus

Regras de transformação aplicadas pelo OTLP receiver:

1. `.` → `_`
2. Sufixo de unidade adicionado quando ausente (`_seconds`, `_bytes`).
3. Histogram exporta três séries: `_bucket`, `_sum`, `_count`.
4. Counters em Prometheus recebem sufixo `_total`.

Exemplo:
- OTel: `http.server.request.duration` (s) →
- Prom: `http_server_request_duration_seconds_{bucket,sum,count}`
