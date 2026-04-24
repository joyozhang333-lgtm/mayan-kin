# Validation Findings v2 - Detailed Public Biography Labels

## Why v2 Exists

v1 used occupation and short description tags. That was too coarse: a public figure's life cannot be reduced to "politician", "actor", or "writer".

v2 labels public biographies across seven dimensions:

- Core achievements
- Recurring themes
- Turning points
- Relationship patterns
- Public expression
- Spiritual or value themes
- Crisis and rebirth

The labeling script does **not** import `mayan_kin`, does not calculate Kin, and does not read seal/tone/report output. It only uses public Wikidata/Wikipedia biography data.

## Dataset

- Source pool: `references/public-figures-wikidata-expanded.json`
- Source records: `3710`
- Enriched history-label records: `1080`
- Split counts: `745` train / `167` dev / `168` holdout
- Cutoff year for time split: `2010`

## Holdout Result

Command:

```bash
python3 scripts/evaluate_history_label_holdout.py \
  --dataset references/public-figures-history-labels-v2.json \
  --protocol references/frozen-scoring-protocol-v2.json \
  --split holdout \
  --write references/history-label-holdout-results-v2.json
```

Result:

- Sample size: `168`
- Correct: `20`
- Observed accuracy: `11.9%`
- Chance baseline: `20.0%`
- p-value: `0.9979966613196325`
- History label accuracy score: `11.9`
- Status: `not_significant`

## Train / Dev Diagnostic

- Train: `745` samples, `15.17%` accuracy
- Dev: `167` samples, `12.57%` accuracy

Because train/dev are also below random baseline, the failure is not a holdout-only accident. The current expression-tag layer is not yet a reliable predictor of public biography themes.

## Time-Split Result

Command:

```bash
python3 scripts/evaluate_time_split_predictions.py \
  --dataset references/public-figures-history-labels-v2.json \
  --protocol references/frozen-scoring-protocol-v2.json \
  --split holdout \
  --write references/time-split-prediction-results-v2.json
```

Result:

- Eligible holdout sample size: `26`
- Average F1: `0.0602`
- Time-split prediction score: `6.02`
- Status: `not_passed`

## Interpretation

This v2 benchmark is stronger and more meaningful than v1 because it looks at biography themes rather than occupation names.

It still does not validate the current Mayan expression signature. The correct conclusion is:

> The project now has a better public biography benchmark, but the current prediction layer does not pass it.

## Next Product Iteration

Use train/dev only to redesign the interpretation layer:

- Reduce overly generic tags.
- Make seal/tone outputs distinguish similar public paths.
- Add negative signatures: "this pattern is less likely to express as..."
- Weight recurring themes and turning points separately from occupation-like achievements.
- Keep holdout frozen until a new version is ready.
