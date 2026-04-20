# Run Summary - 2026-04-20

## Environment
- App started with `.env` via: `uvicorn app.main:app --reload --env-file .env`
- `tracing_enabled` at startup: `true`
- OpenAI and Langfuse keys are loaded from `.env`

## Traffic generation
Commands used:

```powershell
python scripts/load_test.py --concurrency 1
python scripts/load_test.py --concurrency 1
```

Additional request:

```powershell
python -c "import httpx; payload={'user_id':'u-extra','session_id':'s-extra','feature':'qa','message':'Give me one internship tip'}; print(httpx.post('http://127.0.0.1:8000/chat', json=payload, timeout=60).status_code)"
```

## Langfuse trace evidence
Queried endpoint:
- `GET https://cloud.langfuse.com/api/public/traces?limit=1`

Observed result:
- `totalItems = 21`

Sample trace IDs:
- `2cd6b4ae020ad70a5f9831c68156f101`
- `4826f2677531039a4207aba6ab97c90d`
- `1187250696fba6e488c1a5435e446981`

## Alert evaluation
Command:

```powershell
python scripts/check_alerts.py --json
```

Artifact:
- `docs/evidence/alert-eval-2026-04-20.json`

Observed highlights:
- `high_latency_p95`: firing `true`
- `high_error_rate`: firing `false`
- `cost_budget_spike`: firing `true`

## Log validation
Command:

```powershell
python scripts/validate_logs.py
```

Result:
- Estimated score: `100/100`
- Missing required fields: `0`
- Missing enrichment fields: `0`
- Potential PII leaks: `0`
- Unique correlation IDs: `147`

## Metrics snapshot
Source: `GET /metrics`

- `traffic`: `10`
- `latency_p50`: `5461.0`
- `latency_p95`: `8796.0`
- `latency_p99`: `8796.0`
- `avg_cost_usd`: `0.0036`
- `total_cost_usd`: `0.0357`
- `tokens_in_total`: `1369`
- `tokens_out_total`: `2109`
- `error_breakdown`: `{}`
- `quality_avg`: `0.87`

## Notes for submission
- Add screenshots into `docs/evidence/`:
  - `trace-list.png` (>=10 traces)
  - `trace-waterfall.png`
  - `dashboard-6-panels.png`
  - `alert-rules.png`
  - `correlation-id.png`
  - `pii-redaction.png`
