"""Metrics for the Claude embedding POC: cost, ROI, retrieval quality and resource use.

Every function is pure except measure_operation (which samples process memory) and evidence_record
(which hashes files). Prices are always passed in; never hardcode them. Use the current rates from
https://platform.claude.com/docs/en/about-claude/pricing and record the date you read them.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import threading
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable, Iterable, Sequence


# --------------------------------------------------------------------- cost
def calculate_api_cost(
    input_tokens: int,
    output_tokens: int,
    input_price: float,
    output_price: float,
    cache_read_tokens: int = 0,
    cache_write_tokens: int = 0,
    cache_read_price: float = 0.0,
    cache_write_price: float = 0.0,
) -> float:
    """Cost in dollars for one request. Prices are per million tokens.

    Pass uncached input tokens as input_tokens so cached tokens are not counted twice.
    """
    for v in (input_tokens, output_tokens, cache_read_tokens, cache_write_tokens,
              input_price, output_price, cache_read_price, cache_write_price):
        if v < 0:
            raise ValueError("Token counts and prices must be nonnegative")
    return (
        input_tokens * input_price
        + output_tokens * output_price
        + cache_read_tokens * cache_read_price
        + cache_write_tokens * cache_write_price
    ) / 1_000_000


def percentage_reduction(baseline: float, optimized: float) -> float | None:
    """Percent reduction from baseline; None when the baseline is zero or negative."""
    if baseline <= 0:
        return None
    return (1 - optimized / baseline) * 100


def cost_per_correct_answer(total_cost: float, correct_answers: int) -> float | None:
    return None if correct_answers <= 0 else total_cost / correct_answers


@dataclass
class RoiResult:
    annual_queries: float
    baseline_annual_api_cost: float
    optimized_annual_api_cost: float
    annual_api_savings: float
    cumulative_query_hours_saved: float
    realizable_hours: float
    productivity_value: float
    first_year_costs: float
    net_benefit_excluding_productivity: float
    roi_pct_excluding_productivity: float | None
    net_benefit: float
    roi_pct: float | None
    payback_months: float | None


def calculate_roi(
    baseline_cost_per_query: float,
    optimized_cost_per_query: float,
    baseline_seconds: float,
    optimized_seconds: float,
    agents: int,
    queries_per_agent_per_day: float,
    operating_days: int,
    hourly_rate: float,
    realization: float,
    initial_cost: float,
    monthly_operating_cost: float,
) -> RoiResult:
    """First-year ROI. realization is the share (0 to 1) of time saved that becomes usable employee time;
    use 0 for unattended automation. Productivity value is capacity, not necessarily cash."""
    if not 0 <= realization <= 1:
        raise ValueError("realization must be between 0 and 1")
    if min(baseline_cost_per_query, optimized_cost_per_query, baseline_seconds, optimized_seconds,
           agents, queries_per_agent_per_day, operating_days, hourly_rate, initial_cost,
           monthly_operating_cost) < 0:
        raise ValueError("Inputs must be nonnegative")
    q = agents * queries_per_agent_per_day * operating_days
    base_api, opt_api = baseline_cost_per_query * q, optimized_cost_per_query * q
    api_savings = base_api - opt_api
    hours = max(baseline_seconds - optimized_seconds, 0) * q / 3600
    realizable = hours * realization
    productivity = realizable * hourly_rate
    costs = initial_cost + 12 * monthly_operating_cost
    net_ex = api_savings - costs
    net = api_savings + productivity - costs
    monthly_net = (api_savings + productivity) / 12 - monthly_operating_cost
    return RoiResult(
        annual_queries=q,
        baseline_annual_api_cost=base_api,
        optimized_annual_api_cost=opt_api,
        annual_api_savings=api_savings,
        cumulative_query_hours_saved=hours,
        realizable_hours=realizable,
        productivity_value=productivity,
        first_year_costs=costs,
        net_benefit_excluding_productivity=net_ex,
        roi_pct_excluding_productivity=net_ex / costs * 100 if costs else None,
        net_benefit=net,
        roi_pct=net / costs * 100 if costs else None,
        payback_months=initial_cost / monthly_net if monthly_net > 0 else None,
    )


# ------------------------------------------------------------------ quality
def accuracy(correct: int, total: int) -> float | None:
    return None if total <= 0 else correct / total * 100


def precision_at_k(retrieved: Sequence[str], relevant: Iterable[str], k: int) -> float | None:
    top = list(retrieved)[:k]
    if not top:
        return None
    rel = set(relevant)
    return sum(1 for r in top if r in rel) / len(top)


def recall_at_k(retrieved: Sequence[str], relevant: Iterable[str], k: int) -> float | None:
    rel = set(relevant)
    if not rel:
        return None
    return len(rel.intersection(list(retrieved)[:k])) / len(rel)


def mean_reciprocal_rank(runs: Sequence[tuple[Sequence[str], Iterable[str]]]) -> float | None:
    """runs: (retrieved ids in rank order, relevant ids) per question."""
    if not runs:
        return None
    total = 0.0
    for retrieved, relevant in runs:
        rel = set(relevant)
        total += next((1 / (i + 1) for i, r in enumerate(retrieved) if r in rel), 0.0)
    return total / len(runs)


def citation_accuracy(valid_citations: int, total_citations: int) -> float | None:
    return None if total_citations <= 0 else valid_citations / total_citations * 100


def to_trec_run(question_id: str, retrieved: Sequence[str], run_name: str = "embed") -> str:
    """Lines in TREC run format for scoring with NIST trec_eval (https://github.com/usnistgov/trec_eval)."""
    return "".join(f"{question_id} Q0 {doc} {rank + 1} {len(retrieved) - rank} {run_name}\n" for rank, doc in enumerate(retrieved))


def to_trec_qrels(question_id: str, relevant: Iterable[str]) -> str:
    return "".join(f"{question_id} 0 {doc} 1\n" for doc in sorted(set(relevant)))


# ---------------------------------------------------------------- resources
def measure_operation(operation: Callable, *args, sample_interval: float = 0.01, **kwargs):
    """Run operation and return (result, metrics) with wall time, CPU seconds and PEAK resident memory,
    sampled on a background thread. Requires psutil (pip install psutil)."""
    import psutil

    proc = psutil.Process(os.getpid())
    peak = proc.memory_info().rss
    stop = threading.Event()

    def sample():
        nonlocal peak
        while not stop.is_set():
            peak = max(peak, proc.memory_info().rss)
            stop.wait(sample_interval)

    before_rss, before_cpu = proc.memory_info().rss, proc.cpu_times()
    t = threading.Thread(target=sample, daemon=True)
    t.start()
    start = time.perf_counter()
    try:
        result = operation(*args, **kwargs)
    finally:
        elapsed = time.perf_counter() - start
        stop.set()
        t.join()
    after_cpu = proc.cpu_times()
    peak = max(peak, proc.memory_info().rss)
    return result, {
        "execution_seconds": elapsed,
        "cpu_seconds": (after_cpu.user - before_cpu.user) + (after_cpu.system - before_cpu.system),
        "memory_before_mb": before_rss / 1e6,
        "memory_after_mb": proc.memory_info().rss / 1e6,
        "peak_memory_mb": peak / 1e6,
    }


# ----------------------------------------------------------------- evidence
def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


@dataclass
class EvidenceRecord:
    configuration: str
    claude_model: str
    embedding_model: str
    pricing_source_date: str
    documents: dict = field(default_factory=dict)
    usage: dict = field(default_factory=dict)
    retrieved_passages: list = field(default_factory=list)
    human_verified_correct: bool | None = None
    hardware: dict = field(default_factory=dict)
    controls: list = field(default_factory=list)
    passed: bool | None = None
    experiment_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)
    software: dict = field(default_factory=lambda: {"python": platform.python_version(), "platform": platform.platform()})

    def to_json(self) -> str:
        return json.dumps(asdict(self), sort_keys=True)


def evidence_record(configuration: str, claude_model: str, embedding_model: str, pricing_source_date: str,
                    document_paths: Iterable[str | Path], **kw) -> EvidenceRecord:
    docs = {Path(p).name: sha256_file(p) for p in document_paths}
    return EvidenceRecord(configuration, claude_model, embedding_model, pricing_source_date, documents=docs, **kw)
