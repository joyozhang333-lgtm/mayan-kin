# Validation Findings - 2026-04-24

## What Was Added

- Collected `1425` public figure samples from Wikidata.
- Split them deterministically into `1012` train, `201` dev, and `212` holdout records.
- Froze the scoring rules in `frozen-scoring-protocol-v1.json`.
- Added public figure forced-choice evaluation.
- Added prospective prediction registry and future outcome evaluator.

## Holdout Result

Command:

```bash
python3 scripts/evaluate_public_figure_holdout.py \
  --dataset references/public-figures-wikidata-1000.json \
  --protocol references/frozen-scoring-protocol-v1.json \
  --split holdout \
  --write references/public-figure-holdout-results.json
```

Result:

- Sample size: `212`
- Correct: `15`
- Observed accuracy: `7.08%`
- Chance baseline: `20.0%`
- p-value: `0.9999999599242533`
- Public figure accuracy score: `7.08`
- Status: `not_significant`

## Interpretation

This is a failed public-figure forced-choice validation.

It means the current birth-date-only expression signature does not predict public occupation / biography evidence above random baseline under this protocol.

This does not invalidate reflective use of the report as a self-understanding tool, but it does mean the project cannot honestly claim:

> scientifically proven 90-point objective destiny prediction

The accurate claim is:

> the project now has a reproducible protocol capable of testing this claim, and the first 1000+ public figure holdout run did not pass.

## Next Iteration Rules

- Do not tune on holdout and reuse it as proof.
- Use train/dev only for model or interpretation improvements.
- Freeze a new `v2` protocol before a new holdout claim.
- For personality and talent accuracy, collect self-report or expert-coded blind data; public occupation metadata is not a sufficient proxy for inner personality.
