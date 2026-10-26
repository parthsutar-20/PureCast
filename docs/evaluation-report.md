# PureCast Evaluation Framework & Targets Report

## 1. Evaluation Objectives (atomQUEST 2026, Track 2)

This report outlines the quantitative targets, testing rig methodology, and validation metrics used to prove the accuracy, safety, and economic value of the PureCast platform.

---

## 2. Quantitative Target Benchmarks

| Metric | Target Specification | Validation Method |
| :--- | :--- | :--- |
| **Remaining Life Error** | $\le \pm 15\%$ error at 30 days prior to true EOL | Golden testbench rig datasets |
| **Advance Warning Lead Time** | $\ge 30$ days advance notice for $\ge 90\%$ of cartridge failures | Accelerated degradation stress runs |
| **Fault Diagnosis Accuracy** | $\ge 90\%$ across 4 primary fault classes | Confusion matrix on labeled fault rig runs |
| **Wasted Cartridge Life** | $\le 10\%$ remaining life upon replacement | Compared against calendar-based (12 mo) baselines |
| **Temperature Flow Invariance** | $< 5\%$ residual flow drift across $20^\circ\text{C} - 32^\circ\text{C}$ | Chilled/heated reservoir flow loops |

---

## 3. Evaluation Scripts & Artifact Generation

The automated evaluation suite is triggered via:
```bash
python scripts/run_evaluation.py --output-dir=docs/evaluation_results/
```

This generates:
1. `confusion_matrix.json` and confusion matrix plot.
2. `kalman_forecast_accuracy.json` with Mean Absolute Percentage Error (MAPE) curves over time.
3. `temperature_compensation_residuals.csv` confirming $<5\%$ drift across temperature sweeps.
