"""Tests for reproducible thesis baselines."""

from __future__ import annotations

import pandas as pd

from tfm_viu.baseline import evaluate_susceptibility, ks_inventory_statistic, load_dataset


def test_load_dataset() -> None:
    """Dataset loads with expected columns."""
    df = load_dataset("data.parquet")
    assert {"susceptibilidad", "inventario"}.issubset(df.columns)
    assert len(df) > 1000


def test_ks_inventory_statistic() -> None:
    """KS statistic is bounded."""
    df = pd.DataFrame({"susceptibilidad": [0, 1, 2, 3], "inventario": [0, 0, 1, 1]})
    value = ks_inventory_statistic(df)
    assert 0 <= value <= 1


def test_evaluate_susceptibility() -> None:
    """Baseline metrics are produced."""
    df = load_dataset("data.parquet").sample(1000, random_state=42)
    metrics = evaluate_susceptibility(df)
    assert "score_direct" in metrics
    assert metrics["ks_statistic"] >= 0
