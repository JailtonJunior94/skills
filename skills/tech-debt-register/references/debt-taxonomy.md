# Taxonomia de Débito Técnico

Lista canônica de naturezas de débito. Cada item declara: definição em uma linha, sinais típicos no codebase, e termos buscáveis sugeridos para o confronto.

## 1. Segurança
- **Definição**: Risco de exposição, escalonamento de privilégio, ou violação de confidencialidade/integridade.
- **Sinais típicos**: ausência de autenticação/autorização, segredos em código, criptografia fraca, dependências com CVE, inputs sem sanitização.
- **Termos buscáveis**: `auth`, `login`, `token`, `secret`, `password`, `crypto`, `hash`, `jwt`, `bearer`, `cors`, `csrf`, `xss`, `sanitize`.

## 2. Performance
- **Definição**: Latência, throughput ou consumo de recursos abaixo do esperado.
- **Sinais típicos**: queries N+1, full table scan, loops aninhados sobre IO, ausência de cache, deserialização redundante.
- **Termos buscáveis**: `for `, `range`, `select *`, `findAll`, `eager`, `cache`, `O(n`, `sleep`, `time.Sleep`, `await ` (em loop).

## 3. Manutenibilidade
- **Definição**: Código difícil de ler, alterar com segurança, ou estender sem retrabalho.
- **Sinais típicos**: funções grandes, código duplicado, naming inconsistente, ausência de tipos, comentários desatualizados.
- **Termos buscáveis**: `TODO`, `FIXME`, `HACK`, `XXX`, `deprecated`, `legacy`, `old_`, `_v1`, `_v2`, `_new`.

## 4. Confiabilidade
- **Definição**: Falhas intermitentes, ausência de retries/timeouts, perda silenciosa de dados.
- **Sinais típicos**: chamadas externas sem timeout, retry exponencial ausente, swallowing de exceptions, ausência de circuit breaker.
- **Termos buscáveis**: `retry`, `timeout`, `circuit`, `breaker`, `catch`, `recover`, `panic`, `error nil`, `_ = err`.

## 5. Observabilidade
- **Definição**: Falta de visibilidade sobre comportamento em produção (logs, métricas, traces).
- **Sinais típicos**: ausência de logs estruturados, sem trace IDs, métricas faltando, alertas inexistentes.
- **Termos buscáveis**: `log`, `metric`, `trace`, `span`, `otel`, `prometheus`, `Println`, `fmt.Print`, `console.log`.

## 6. Complexidade
- **Definição**: Acoplamento alto, ciclos de dependência, abstração prematura ou faltando.
- **Sinais típicos**: import cycles, classes-deus, herança profunda, switch gigante por tipo, ausência de fronteiras claras.
- **Termos buscáveis**: `interface{`, `any`, `switch`, `instanceof`, `isinstance`, `cast`, nomes terminados em `Manager`, `Handler`, `Service` genéricos.

## 7. Lock-in Tecnológico
- **Definição**: Acoplamento a vendor, framework ou versão específica que dificulta substituição.
- **Sinais típicos**: chamadas diretas a SDK proprietário sem camada de abstração, queries específicas de banco em domínio.
- **Termos buscáveis**: nome do vendor (`aws.`, `azure.`, `gcp.`), nome do ORM/driver, versões hard-coded.

## 8. Cobertura de Testes
- **Definição**: Ausência de testes em caminhos críticos, cobertura desbalanceada, testes frágeis.
- **Sinais típicos**: arquivos sem `_test.go`/`.test.ts`/`_spec.rb`, mocks excessivos, testes que dependem de ordem.
- **Termos buscáveis**: `_test.`, `.test.`, `_spec.`, `mock`, `stub`, `fake`, `skip`, `xit`, `xdescribe`.

## 9. Conformidade
- **Definição**: Gaps regulatórios ou de política interna (LGPD, GDPR, PCI, SOX, ISO).
- **Sinais típicos**: dados pessoais sem mascaramento, logs com PII, retenção indefinida, ausência de consentimento.
- **Termos buscáveis**: `cpf`, `email`, `phone`, `address`, `pii`, `gdpr`, `lgpd`, `consent`, `retention`.

## 10. Documentação
- **Definição**: Ausência ou desatualização de documentação que bloqueia onboarding ou decisões.
- **Sinais típicos**: README desatualizado, ADRs faltando, contratos de API sem schema, runbooks ausentes.
- **Termos buscáveis**: `README`, `ADR`, `runbook`, `openapi`, `swagger`, `docs/`, comentários `// TODO doc`.

## Regras de Uso
- Cada débito tem uma natureza **primária** obrigatória. Naturezas secundárias são permitidas (até 2).
- Os termos buscáveis são ponto de partida; refinar com identificadores do domínio do usuário (nomes de serviços, módulos, classes citadas na descrição).
- Quando a descrição cita explicitamente uma natureza, marcar o eixo 1 como `respondido` sem pergunta.
