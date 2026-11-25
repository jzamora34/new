# Claude embedding POC: ROI and performance measurement

Goal: prove that embedding-based retrieval answers the same questions, over the same three PDFs, with the same Claude model, at equal or better verified quality and lower total cost. Token savings alone prove nothing if accuracy drops. Code: `../tools/embedding-roi/metrics.py` (tested; `pytest tools/embedding-roi`).

> All figures in this document are simulated illustrations using assumed rates of $3 per million input tokens and $15 per million output tokens. They are not benchmark results or current prices. Replace them with measured values and prices from the [Claude pricing page](https://platform.claude.com/docs/en/about-claude/pricing), with the date read, before presenting.

## 1. Metrics

| Category | Metric | Unit |
| --- | --- | --- |
| Financial | API cost savings; annual cost avoidance; ROI; break-even; cost per correct answer | $, $/yr, %, months, $ |
| Productivity | Response time reduction; employee time recovered; agent throughput | s, h/yr, queries/h |
| Computational | Input and output token reduction; context window use; local RAM and CPU; vector storage; embedding time | %, MB, %, MB, s |
| Quality | Answer accuracy; retrieval precision and recall; citation accuracy | % |
| Governance | Source traceability; audit completeness | % |
| Security | Unauthorized retrieval | incidents |

## 2. Illustrative benchmark (simulated)

| Metric | Agent A, full PDFs | Agent B, embeddings |
| --- | --- | --- |
| Input tokens | 85,420 | 2,650 |
| Output tokens | 410 | 398 |
| API cost per query | $0.26241 | $0.01392 |
| Response time | 18.4 s | 4.2 s |
| Accuracy | assumed equal | assumed equal |

Input tokens fall 96.9%, cost 94.7%, latency 77.2%. The metrics tests reproduce these numbers.

## 3. First-year ROI (simulated)

Inputs: 10 agents, 100 queries per agent per day, 250 days (250,000 queries), $75/hour, 25% of saved query time realized as usable employee time, $5,000 build, $200/month to run. Results: annual API savings $62,123; 986.1 cumulative query hours saved; 246.5 realizable hours; first-year costs $7,400; ROI excluding productivity about 740%. Payback is under one month. Projections assume constant workload and uncached pricing; include caching, infrastructure, index refreshes, retries and maintenance in real calculations. Productivity value is capacity, not necessarily cash.

## 4. Formulas

```latex
C = \frac{T_i P_i + T_o P_o}{10^6}
```

```latex
H_{saved} = \frac{(t_A - t_B) \times Q}{3600}, \qquad V_{labor} = H_{saved} \times R \times U
```

Accuracy = correct / total x 100. Precision@k = relevant retrieved / retrieved. Recall@k = relevant retrieved / all labeled relevant. Citation accuracy = valid supporting citations / total citations x 100. Payback = initial investment / monthly net benefit. With prompt caching, add cache-read and cache-write tokens at their own rates and pass only uncached input as T_i ([prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching), [token counting](https://platform.claude.com/docs/en/build-with-claude/token-counting)). For multi-part technical questions, score individual factual claims as well as whole answers.

## 5. Benchmark design

| Run | Configuration | Purpose |
| --- | --- | --- |
| A | Native PDFs | Standard Claude PDF analysis |
| B | Full extracted text | Text-only baseline |
| C | Keyword retrieval (BM25) | Traditional search comparison |
| D | Embedding retrieval | Semantic search |

Run D against C, not only A: it shows whether embeddings beat ordinary keyword search, rather than that sending less text costs less. Initial size: 3 PDFs, 20 questions, 4 configurations, 3 repetitions = 240 Claude requests (excluding retries and judge calls). Record cold and warm starts separately, and include embedding, retrieval, API latency, retries and validation time. Score retrieval with [trec_eval](https://github.com/usnistgov/trec_eval) using `to_trec_run` and `to_trec_qrels`.

## 6. Proposed acceptance criteria

These are proposed targets, not external standards; 20 questions supports a preliminary demonstration, not production accuracy claims.

| KPI | Target |
| --- | --- |
| Input token reduction vs full text | at least 80% |
| API cost reduction | at least 70% |
| End-to-end latency reduction | at least 50% |
| Answer accuracy | at least 95%, and no more than 2 points below baseline |
| Citation accuracy; source traceability; audit completeness | 100% |
| Retrieval Recall@10 | at least 90% |
| Unauthorized data retrieval | 0 |
| First-year financial ROI; payback | positive; within 12 months |

## 7. Evidence per experiment

`evidence_record()` in metrics.py captures: experiment ID, document SHA-256, Claude and embedding model versions, pricing source date, API usage response, retrieved passages, human verification, hardware measurements (`measure_operation` samples peak memory), configuration, software versions, control IDs and pass/fail. Reconcile spend with the [Usage and Cost API](https://platform.claude.com/docs/en/manage-claude/usage-cost-api). Claude server-side RAM or VRAM is not exposed by the API.

## 8. Dashboard tabs

Executive ROI (savings, net benefit, payback) · Financial (API spend, cost per correct answer) · Computational (tokens, CPU, RAM, storage) · Productivity (latency, throughput, recovered hours) · Testing (accuracy, recall, precision, citations) · Audit and governance (evidence, controls, risks).

References: [psutil](https://psutil.readthedocs.io/) · [Python time](https://docs.python.org/3/library/time.html) · [Sentence Transformers evaluation](https://sbert.net/docs/package_reference/sentence_transformer/evaluation.html) · [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) · [OSCAL](https://pages.nist.gov/OSCAL/) · [Apache ECharts](https://echarts.apache.org/)
