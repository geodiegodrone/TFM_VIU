# TFM_VIU

**Machine-learning evaluation of susceptibility scores against geohazard inventory labels**

[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](requirements.txt)
[![Data](https://img.shields.io/badge/data-parquet-green)](data.parquet)
[![CI](https://img.shields.io/badge/CI-tests%20%2B%20reproducibility-brightgreen)](.github/workflows/ci.yml)

This repository contains the research notebooks and reproducible baseline code for a Master's thesis workflow focused on evaluating susceptibility values against an inventory target. The dataset contains 19,676 observations with:

- `susceptibilidad`: continuous susceptibility score.
- `inventario`: binary inventory label.

The project is being upgraded from notebook-only experimentation to an academic repository with reproducible evaluation, documentation, tests, and CI.

## Research Objective

Evaluate how well susceptibility scores discriminate inventory-positive cells and establish a reproducible benchmark for classical machine-learning models.

## Repository Contents

```text
TFM_VIU/
├── data.parquet                         # Modeling dataset
├── *.ipynb                              # Original experiments
├── filtro_celdas.py                     # QGIS processing helper
├── src/tfm_viu/                         # Reproducible analysis package
├── tests/                               # Pytest checks
├── docs/                                # Academic methodology and roadmap
├── requirements.txt                     # Runtime dependencies
└── .github/workflows/ci.yml             # Automated validation
```

## Quickstart

```bash
python -m pip install -r requirements.txt
python -m tfm_viu.baseline --data data.parquet --output reports/baseline_metrics.json
pytest
```

## Baseline Metrics

The baseline script evaluates:

- ROC AUC,
- average precision,
- F1 score,
- Kolmogorov-Smirnov statistic,
- confusion matrix at a configurable threshold.

## Scientific Standards Added

- deterministic train/test split,
- metrics exported as JSON,
- unit tests for data loading and metrics,
- CI workflow,
- academic methodology report,
- reproducibility checklist.

## Limitations

The current dataset has only one predictor column. It is valuable for benchmarking susceptibility discrimination but should be extended with terrain, lithology, land-cover, rainfall, distance-to-fault, drainage, and anthropogenic variables for a full geohazard susceptibility model.

## Author

Diego F. Pulido Sastoque
