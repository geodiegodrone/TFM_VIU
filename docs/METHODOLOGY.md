# Methodology

## Dataset

The working dataset contains a susceptibility score and a binary inventory label. The first reproducible objective is to evaluate whether susceptibility values discriminate inventory-positive observations.

## Evaluation Metrics

- ROC AUC: ranking quality across thresholds.
- Average precision: performance under class imbalance.
- F1 score: thresholded classification balance.
- Kolmogorov-Smirnov statistic: separation between positive and negative susceptibility distributions.
- Confusion matrix: operational error interpretation.

## Modeling Baselines

The repository includes:

- direct susceptibility score evaluation,
- logistic regression,
- random forest,
- histogram gradient boosting.

These baselines establish a transparent performance floor before adding richer geospatial predictors.

## Academic Upgrade Path

For thesis-level rigor, future work should include spatial cross-validation, terrain covariates, lithological classes, rainfall triggers, distance-to-road and distance-to-drainage variables, calibration curves, uncertainty analysis, and reproducible map exports.
