# Alert Rules and Runbooks

Service scope: OpenAI-powered AI Career Assistant for HUST students

## 1. High latency P95
- Severity: P2
- Trigger: `latency_p95_ms > 5000 for 30m`
- Impact: tail latency breaches SLO
- First checks:
  1. Open top slow traces in the last 1h
  2. Compare RAG span vs OpenAI completion span
  3. Check if incident toggle `rag_slow` is enabled
  4. Compare prompt size for `feature=qa` vs `feature=summary`
- Mitigation:
  - truncate long user queries before prompt assembly
  - fallback retrieval source or skip low-value retrieval
  - lower prompt size and output token cap
  - route to faster model during incident

## 2. High error rate
- Severity: P1
- Trigger: `error_rate_pct > 5 for 5m`
- Impact: users receive failed responses
- First checks:
  1. Group logs by `error_type`
  2. Inspect failed traces
  3. Determine whether failures are OpenAI, tool, schema, or timeout related
  4. Check API key quota and network egress from app host
- Mitigation:
  - rollback latest change
  - disable failing tool
  - retry with fallback model or fallback mock response
  - temporarily disable affected feature flag

## 3. Cost budget spike
- Severity: P2
- Trigger: `hourly_cost_usd > 2x_baseline for 15m`
- Impact: burn rate exceeds budget
- First checks:
  1. Split traces by feature and model
  2. Compare tokens_in/tokens_out
  3. Check if `cost_spike` incident was enabled
  4. Identify sessions with repeated regenerate behavior
- Mitigation:
  - shorten prompts
  - route easy requests to cheaper model
  - apply prompt cache and deduplicate repeated requests
  - lower max output tokens for non-critical features
