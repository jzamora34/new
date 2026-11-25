import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import metrics as m  # noqa: E402
import pytest  # noqa: E402


def test_cost_matches_poc_example():
    # Illustrative rates from the POC write-up ($3 input / $15 output per million tokens)
    assert m.calculate_api_cost(85_420, 410, 3, 15) == pytest.approx(0.26241)
    assert m.calculate_api_cost(2_650, 398, 3, 15) == pytest.approx(0.01392)


def test_cost_with_cache_and_validation():
    assert m.calculate_api_cost(0, 0, 3, 15, cache_read_tokens=1_000_000, cache_read_price=0.3) == pytest.approx(0.3)
    with pytest.raises(ValueError):
        m.calculate_api_cost(-1, 0, 3, 15)


def test_percentage_reduction():
    assert m.percentage_reduction(85_420, 2_650) == pytest.approx(96.8977, rel=1e-4)
    assert m.percentage_reduction(0, 5) is None


def test_roi_and_payback():
    r = m.calculate_roi(0.26241, 0.01392, 18.4, 4.2, agents=10, queries_per_agent_per_day=100,
                        operating_days=250, hourly_rate=75, realization=0.25,
                        initial_cost=5_000, monthly_operating_cost=200)
    assert r.annual_queries == 250_000
    assert r.annual_api_savings == pytest.approx(62_122.5)
    assert r.cumulative_query_hours_saved == pytest.approx(986.111, rel=1e-4)
    assert r.realizable_hours == pytest.approx(246.528, rel=1e-4)
    assert r.first_year_costs == 7_400
    assert r.payback_months is not None and r.payback_months < 1


def test_roi_rejects_bad_realization():
    with pytest.raises(ValueError):
        m.calculate_roi(1, 1, 1, 1, 1, 1, 1, 1, realization=1.5, initial_cost=0, monthly_operating_cost=0)


def test_retrieval_metrics():
    retrieved, relevant = ["a", "b", "c", "d"], {"b", "e"}
    assert m.precision_at_k(retrieved, relevant, 2) == 0.5
    assert m.recall_at_k(retrieved, relevant, 4) == 0.5
    assert m.mean_reciprocal_rank([(retrieved, relevant), (["x"], {"y"})]) == pytest.approx(0.25)
    assert m.accuracy(19, 20) == 95
    assert m.citation_accuracy(3, 3) == 100
    assert m.cost_per_correct_answer(1.0, 0) is None


def test_trec_formats():
    assert m.to_trec_run("q1", ["d1", "d2"]).splitlines() == ["q1 Q0 d1 1 2 embed", "q1 Q0 d2 2 1 embed"]
    assert m.to_trec_qrels("q1", {"d2"}) == "q1 0 d2 1\n"


def test_measure_operation():
    pytest.importorskip("psutil")
    result, stats = m.measure_operation(lambda: sum(range(100_000)))
    assert result == sum(range(100_000))
    assert stats["peak_memory_mb"] >= stats["memory_before_mb"] > 0


def test_evidence_record(tmp_path):
    doc = tmp_path / "policy.pdf"
    doc.write_bytes(b"synthetic")
    rec = m.evidence_record("D-embeddings", "model-id", "embed-id", "2026-11-25", [doc], controls=["AU-3"])
    data = json.loads(rec.to_json())
    assert data["documents"]["policy.pdf"] == m.sha256_file(doc)
    assert data["controls"] == ["AU-3"]
