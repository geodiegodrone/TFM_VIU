"""Baseline evaluation for susceptibility inventory modeling."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import ks_2samp
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    confusion_matrix,
    f1_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def load_dataset(path: str | Path) -> pd.DataFrame:
    """Load and validate the thesis modeling dataset."""
    df = pd.read_parquet(path)
    required = {"susceptibilidad", "inventario"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    df = df[list(required)].dropna().copy()
    df["inventario"] = df["inventario"].astype(int)
    return df


def ks_inventory_statistic(df: pd.DataFrame) -> float:
    """Compute KS statistic between inventory-positive and inventory-negative scores."""
    positive = df.loc[df["inventario"] == 1, "susceptibilidad"]
    negative = df.loc[df["inventario"] == 0, "susceptibilidad"]
    return float(ks_2samp(positive, negative).statistic)


def evaluate_susceptibility(
    df: pd.DataFrame,
    threshold: float = 0.5,
    random_state: int = 42,
) -> dict[str, object]:
    """Evaluate susceptibility score and simple ML baselines."""
    x = df[["susceptibilidad"]].astype(float)
    y = df["inventario"].astype(int)
    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.25,
        random_state=random_state,
        stratify=y,
    )
    models = {
        "score_direct": None,
        "logistic_regression": Pipeline(
            [("scale", StandardScaler()), ("model", LogisticRegression(max_iter=1000))]
        ),
        "random_forest": RandomForestClassifier(
            n_estimators=200,
            min_samples_leaf=5,
            random_state=random_state,
            class_weight="balanced",
        ),
        "hist_gradient_boosting": HistGradientBoostingClassifier(random_state=random_state),
    }
    metrics: dict[str, object] = {"ks_statistic": ks_inventory_statistic(df)}
    direct_scores = (x_test["susceptibilidad"] - x_train["susceptibilidad"].min()) / (
        x_train["susceptibilidad"].max() - x_train["susceptibilidad"].min()
    )
    for name, model in models.items():
        if model is None:
            score = direct_scores.clip(0, 1).to_numpy()
        else:
            model.fit(x_train, y_train)
            score = model.predict_proba(x_test)[:, 1]
        pred = (score >= threshold).astype(int)
        metrics[name] = {
            "roc_auc": float(roc_auc_score(y_test, score)),
            "average_precision": float(average_precision_score(y_test, score)),
            "f1": float(f1_score(y_test, pred)),
            "confusion_matrix": confusion_matrix(y_test, pred).tolist(),
        }
    return metrics


def main() -> None:
    """Run baseline evaluation from the command line."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=Path("data.parquet"))
    parser.add_argument("--output", type=Path, default=Path("reports/baseline_metrics.json"))
    args = parser.parse_args()
    df = load_dataset(args.data)
    metrics = evaluate_susceptibility(df)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
