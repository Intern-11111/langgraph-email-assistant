# Milestone 2: Evaluation & Result Analysis

| Project | Internship Program | Task |
|---|---|---|
| LangGraph-based Email Assistant | Infosys Springboard | Intern 4 – Evaluation, Analysis & Result Interpretation |

## Table of Contents
- [Objective](#objective)
- [Evaluation Setup](#evaluation-setup)
  - [Tooling Used](#tooling-used)
  - [Evaluation Flow](#evaluation-flow)
- [Evaluation Metrics](#evaluation-metrics)
- [Sample Results](#sample-results)
- [Result Interpretation](#result-interpretation)
- [LangSmith Trace Analysis](#langsmith-trace-analysis)
- [Rate Limit Behavior](#rate-limit-behavior)
- [Attach Results (Images)](#attach-results-images)
- [System Health](#system-health)
- [Conclusion](#conclusion)

## Objective
Evaluate the Email Assistant agent against ideal responses using LangSmith; analyze quantitative metrics, diagnose errors/rate limits, and interpret system health. No model training or feature work is included in this milestone.

## Evaluation Setup

### Tooling Used
- LangSmith for tracing and evaluation
- LLM-based evaluator: `gpt-4o-mini`
- Custom evaluator prompt comparing Agent Response vs. Ideal Response

### Evaluation Flow
1. Input email is processed by the Email Assistant agent.
2. Agent generates a response.
3. Evaluator compares Agent Response vs. Ideal Response.
4. Evaluator outputs structured JSON metrics.
5. Results are visualized in LangSmith.

## Evaluation Metrics
Evaluator returns scores in the range 0.0–1.0:

| Metric | Description |
|---|---|
| Accuracy | How closely the agent matches the ideal response |
| Helpfulness | Usefulness and relevance of the response |
| Tone | Politeness and appropriateness |
| Overall | Aggregated score for general response quality |

## Sample Results
Example – Case 1:

```json
{
  "accuracy": 0.5,
  "helpfulness": 0.7,
  "tone": 0.6,
  "overall": 0.6
}
```

Example – Case 2:

```json
{
  "accuracy": 0.8,
  "helpfulness": 0.7,
  "tone": 0.6,
  "overall": 0.7
}
```

## Result Interpretation
- **Accuracy:** Varies with alignment to the ideal; lower scores suggest intent/wording mismatch.
- **Helpfulness:** Generally moderate to high; responses include relevant steps/clarifications.
- **Tone:** Stable and professional across runs.
- **Overall:** 0.6–0.7 indicates reliable performance with room to improve.

## LangSmith Trace Analysis
- **Latency:** ~1.3s–22s depending on retries
- **Tokens:** ~160 tokens per evaluation
- **Cost:** < $0.0001 per run (very low)

These indicate efficient usage, low cost, and a stable pipeline.

## Rate Limit Behavior
Observed during batch evaluation (automatic backoff):

```
[RateLimitError] Retry 1/5 in 10s...
[RateLimitError] Retry 2/5 in 20s...
```

- Expected when many evaluator requests are concurrent
- LangSmith retries automatically; final results unaffected
- Considered healthy/normal for this workload

## Attach Results (Images)

```text
src/
  reports/
    Milestone2/
      images/
        result1.png   # LangSmith trace or evaluation run
        result2.png   # Aggregated metrics (dashboard) view
```

Embed them below once added:

![LangSmith Trace – Case 1](images/Result(1).png)
*Figure 1. LangSmith trace of a single evaluation run.*

![Aggregate Metrics Dashboard](images/Result(2).png)
*Figure 2. Aggregated evaluation metrics across runs.*

> Note: Avoid attaching sensitive content (API keys, private emails, environment details).

## System Health

| Aspect | Status |
|---|---|
| Evaluation Execution | ✅ Successful |
| Metrics Generation | ✅ Accurate |
| Token Usage | ✅ Low |
| Cost | ✅ Minimal |
| Error Handling | ✅ Robust |

Overall system health is stable and reliable.

## Conclusion
The evaluation demonstrates correct evaluator integration, meaningful metrics, and proper interpretation of rate-limit behavior. The Email Assistant is reliable with moderate-to-good quality responses, and is a strong candidate for iterative improvements in future phases.