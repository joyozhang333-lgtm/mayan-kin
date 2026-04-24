#!/usr/bin/env python3
"""Evaluate birth-date predictions against post-cutoff public evidence tags."""

import argparse
import json
import pathlib
import statistics
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.evaluate_public_figure_holdout import expression_weights_for_birth_date


DEFAULT_DATASET = ROOT / "references" / "public-figures-history-labels-v2.json"
DEFAULT_PROTOCOL = ROOT / "references" / "frozen-scoring-protocol-v2.json"


def load_protocol(protocol_path):
    if protocol_path and pathlib.Path(protocol_path).exists():
        return json.loads(pathlib.Path(protocol_path).read_text(encoding="utf-8"))
    return {}


def load_records(dataset_path, split):
    payload = json.loads(pathlib.Path(dataset_path).read_text(encoding="utf-8"))
    records = payload["records"]
    if split != "all":
        records = [item for item in records if item.get("split") == split]
    return payload, records


def score_tags(predicted_tags, evidence_tags):
    predicted = set(predicted_tags)
    evidence = set(evidence_tags)
    hits = sorted(predicted & evidence)
    precision = len(hits) / len(predicted) if predicted else 0.0
    recall = len(hits) / len(evidence) if evidence else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if precision + recall else 0.0
    return hits, precision, recall, f1


def evaluate(dataset_path, protocol_path=DEFAULT_PROTOCOL, split="holdout", top_n=18, min_evidence_tags=1,
             min_sample_size=20, min_score=90.0):
    dataset, records = load_records(dataset_path, split)
    protocol = load_protocol(protocol_path)
    metric = protocol.get("metrics", {}).get("time_split_prediction", {})
    top_n = int(metric.get("top_weighted_tags", top_n))
    min_evidence_tags = int(metric.get("minimum_post_cutoff_tags", min_evidence_tags))
    min_sample_size = int(metric.get("minimum_sample_size", min_sample_size))
    min_score = float(metric.get("target_score", min_score))

    trials = []
    for record in records:
        evidence_tags = record.get("time_split", {}).get("post_cutoff_tags", [])
        if len(evidence_tags) < min_evidence_tags:
            continue
        tag_weights = expression_weights_for_birth_date(record["birth_date"], top_n=top_n)
        predicted_tags = list(tag_weights)
        hits, precision, recall, f1 = score_tags(predicted_tags, evidence_tags)
        trials.append({
            "id": record["id"],
            "name": record["name"],
            "birth_date": record["birth_date"],
            "split": record["split"],
            "cutoff_year": record.get("time_split", {}).get("cutoff_year"),
            "predicted_tags": predicted_tags,
            "post_cutoff_tags": evidence_tags,
            "hits": hits,
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4),
            "post_cutoff_sentences": record.get("time_split", {}).get("post_cutoff_sentences", []),
        })

    f1_scores = [item["f1"] for item in trials]
    average_f1 = statistics.mean(f1_scores) if f1_scores else 0.0
    score = round(average_f1 * 100, 2) if len(trials) >= min_sample_size else None
    return {
        "dataset_version": dataset.get("version"),
        "protocol_version": protocol.get("version", "ad_hoc"),
        "split": split,
        "eligible_sample_size": len(trials),
        "minimum_sample_size": min_sample_size,
        "top_weighted_tags": top_n,
        "minimum_post_cutoff_tags": min_evidence_tags,
        "average_f1": round(average_f1, 4),
        "time_split_prediction_score": score,
        "status": "passed" if score is not None and score >= min_score else "not_passed",
        "reason": "score is average F1 against explicitly dated post-cutoff evidence tags; missing future evidence is not counted as success",
        "trials": trials,
    }


def main():
    parser = argparse.ArgumentParser(description="Evaluate time-split public figure predictions.")
    parser.add_argument("--dataset", default=str(DEFAULT_DATASET))
    parser.add_argument("--protocol", default=str(DEFAULT_PROTOCOL))
    parser.add_argument("--split", choices=["train", "dev", "holdout", "all"], default="holdout")
    parser.add_argument("--top-weighted-tags", type=int, default=18)
    parser.add_argument("--min-evidence-tags", type=int, default=1)
    parser.add_argument("--min-sample-size", type=int, default=20)
    parser.add_argument("--min-score", type=float, default=90.0)
    parser.add_argument("--write")
    args = parser.parse_args()

    result = evaluate(
        args.dataset,
        protocol_path=args.protocol,
        split=args.split,
        top_n=args.top_weighted_tags,
        min_evidence_tags=args.min_evidence_tags,
        min_sample_size=args.min_sample_size,
        min_score=args.min_score,
    )
    print(f"Evaluated split: {result['split']}")
    print(f"Eligible sample size: {result['eligible_sample_size']}")
    print(f"Average F1: {result['average_f1']}")
    print(f"Time-split prediction score: {result['time_split_prediction_score']}")
    print(f"Status: {result['status']}")
    print(f"Reason: {result['reason']}")
    if args.write:
        pathlib.Path(args.write).write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    if result["time_split_prediction_score"] is None or result["time_split_prediction_score"] < args.min_score:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
