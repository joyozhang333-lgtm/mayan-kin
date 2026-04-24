#!/usr/bin/env python3
"""Evaluate locked prospective predictions against later coded evidence."""

import argparse
import json
import pathlib
import statistics


def load_items(path, key):
    payload = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    return payload.get(key, [])


def evaluate(registry_path, outcomes_path, min_score=90.0):
    predictions = load_items(registry_path, "predictions")
    outcomes = load_items(outcomes_path, "outcomes")
    outcomes_by_id = {item["prediction_id"]: item for item in outcomes}
    scored = []
    for prediction in predictions:
        prediction_id = prediction["prediction_id"]
        outcome = outcomes_by_id.get(prediction_id)
        if not outcome:
            scored.append({
                "prediction_id": prediction_id,
                "status": "missing_outcome",
                "score": None,
                "hits": [],
            })
            continue
        predicted_tags = set(prediction["prediction"]["top_expression_tags"])
        evidence_tags = set(outcome.get("evidence_tags", []))
        hits = sorted(predicted_tags & evidence_tags)
        recall = len(hits) / len(evidence_tags) if evidence_tags else 0.0
        precision = len(hits) / len(predicted_tags) if predicted_tags else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if precision + recall else 0.0
        scored.append({
            "prediction_id": prediction_id,
            "status": "scored",
            "score": round(f1 * 100, 2),
            "hits": hits,
            "precision": round(precision, 4),
            "recall": round(recall, 4),
        })

    valid_scores = [item["score"] for item in scored if item["score"] is not None]
    average_score = round(statistics.mean(valid_scores), 2) if valid_scores else None
    return {
        "prediction_count": len(predictions),
        "outcome_count": len(outcomes),
        "scored_count": len(valid_scores),
        "average_prospective_score": average_score,
        "target_score": min_score,
        "status": "passed" if average_score is not None and average_score >= min_score else "not_passed",
        "results": scored,
    }


def main():
    parser = argparse.ArgumentParser(description="Evaluate prospective prediction outcomes.")
    parser.add_argument("--registry", required=True)
    parser.add_argument("--outcomes", required=True)
    parser.add_argument("--min-score", type=float, default=90.0)
    parser.add_argument("--write", help="Write JSON result")
    args = parser.parse_args()

    result = evaluate(args.registry, args.outcomes, min_score=args.min_score)
    print(f"Predictions: {result['prediction_count']}")
    print(f"Outcomes: {result['outcome_count']}")
    print(f"Scored: {result['scored_count']}")
    print(f"Average prospective score: {result['average_prospective_score']}")
    print(f"Status: {result['status']}")
    if args.write:
        pathlib.Path(args.write).write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
