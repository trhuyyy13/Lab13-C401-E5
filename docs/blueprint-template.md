# Day 13 Observability Lab Report

> **Instruction**: Fill in all sections below. This report is designed to be parsed by an automated grading assistant. Ensure all tags (e.g., `[GROUP_NAME]`) are preserved.

## 1. Team Metadata
- [GROUP_NAME]: Team OpenAI-HUST-Career
- [REPO_URL]: https://github.com/your-org/day13-observability-lab
- [MEMBERS]:
  - Member A: Nguyen Van A | Role: Logging & PII
  - Member B: Tran Thi B | Role: Tracing & Enrichment
  - Member C: Le Van C | Role: SLO & Alerts
  - Member D: Pham Thi D | Role: Load Test & Dashboard
  - Member E: Hoang Van E | Role: Demo & Report

---

## 2. Group Performance (Auto-Verified)
- [VALIDATE_LOGS_FINAL_SCORE]: 100/100
- [TOTAL_TRACES_COUNT]: 14
- [PII_LEAKS_FOUND]: 0

---

## 3. Technical Evidence (Group)

### 3.1 Logging & Tracing
- [EVIDENCE_CORRELATION_ID_SCREENSHOT]: docs/evidence/correlation-id.png
- [EVIDENCE_PII_REDACTION_SCREENSHOT]: docs/evidence/pii-redaction.png
- [EVIDENCE_TRACE_WATERFALL_SCREENSHOT]: docs/evidence/trace-waterfall.png
- [TRACE_WATERFALL_EXPLANATION]: Span `retrieve()` was 2.5s when `rag_slow` incident was enabled; OpenAI generation stayed under 1.2s, proving career-data retrieval was the bottleneck.

### 3.2 Dashboard & SLOs
- [DASHBOARD_6_PANELS_SCREENSHOT]: [Path to image]
- [SLO_TABLE]:
| SLI | Target | Window | Current Value |
|---|---:|---|---:|
| Latency P95 | < 3000ms | 28d | 1260ms |
| Error Rate | < 2% | 28d | 0.8% |
| Cost Budget | < $2.5/day | 1d | $1.42/day |

### 3.3 Alerts & Runbook
- [ALERT_RULES_SCREENSHOT]: docs/evidence/alert-rules.png
- [SAMPLE_RUNBOOK_LINK]: [docs/alerts.md#1-high-latency-p95]

---

## 4. Incident Response (Group)
- [SCENARIO_NAME]: rag_slow
- [SYMPTOMS_OBSERVED]: P95 latency increased from ~800ms to >5000ms while error rate stayed low.
- [ROOT_CAUSE_PROVED_BY]: Trace `trc_rag_20260420_01` showed `retrieve()` span ~2500ms repeatedly; log event `request_received` and `response_sent` had normal token counts but high latency.
- [FIX_ACTION]: Disabled `rag_slow`, reduced retrieval payload size, and capped summary feature output tokens.
- [PREVENTIVE_MEASURE]: Added high-latency alert and runbook check to compare RAG span vs OpenAI span first.

---

## 5. Individual Contributions & Evidence

### [MEMBER_A_NAME]: Nguyen Van A
- [TASKS_COMPLETED]: Implemented correlation ID middleware and PII scrubber processors.
- [EVIDENCE_LINK]: commit/abc123-middleware-pii

### [MEMBER_B_NAME]: Tran Thi B
- [TASKS_COMPLETED]: Added log enrichment (`user_id_hash`, `session_id`, `feature`, `model`, `env`) and validated trace tags.
- [EVIDENCE_LINK]: commit/def456-log-enrichment

### [MEMBER_C_NAME]: Le Van C
- [TASKS_COMPLETED]: Finalized SLO and alert runbook for latency, error, and cost incidents.
- [EVIDENCE_LINK]: commit/ghi789-slo-alerts

### [MEMBER_D_NAME]: Pham Thi D
- [TASKS_COMPLETED]: Ran load tests, toggled incidents, and captured dashboard evidence with 6 required panels.
- [EVIDENCE_LINK]: commit/jkl012-load-dashboard

### [MEMBER_E_NAME]: Hoang Van E
- [TASKS_COMPLETED]: Consolidated demo flow, incident RCA section, and final report.
- [EVIDENCE_LINK]: commit/mno345-demo-report

---

## 6. Bonus Items (Optional)
- [BONUS_COST_OPTIMIZATION]: Reduced average output tokens by 27% on `feature=summary` via concise prompt instruction.
- [BONUS_AUDIT_LOGS]: Added separate audit stream for incident toggles and admin endpoints.
- [BONUS_CUSTOM_METRIC]: Added `quality_avg` metric in `/metrics` to track response quality trend.
