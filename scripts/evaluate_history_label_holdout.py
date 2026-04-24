#!/usr/bin/env python3
"""Evaluate Mayan expression signatures against detailed public history labels."""

import argparse
import hashlib
import json
import math
import pathlib
import statistics
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.evaluate_public_figure_holdout import (
    binomial_survival,
    expression_weights_for_birth_date,
    public_figure_score,
    score_overlap,
)


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


def detailed_tags(record):
    labels = record.get("history_labels", {})
    return labels.get("detailed_tags", record.get("observed_tags", []))


def dimension_scores(tag_weights, record):
    scores = {}
    for dimension, payload in record.get("history_labels", {}).get("dimensions", {}).items():
        tags = payload.get("tags", [])
        hits = sorted(set(tag_weights) & set(tags))
        recall = len(hits) / len(tags) if tags else None
        precision = len(hits) / len(tag_weights) if tag_weights else None
        if recall is None:
            continue
        f1 = (2 * precision * recall / (precision + recall)) if precision and recall else 0.0
        scores[dimension] = {
            "hits": hits,
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4),
        }
    return scores


def deterministic_candidates(records, target_index, candidate_count, seed):
    target = records[target_index]
    others = [item for index, item in enumerate(records) if index != target_index]
    ranked = sorted(
        others,
        key=lambda item: hashlib.sha256(
            f"{seed}:{target['id']}:{item['id']}".encode("utf-8")
        ).hexdigest(),
    )
    return [target] + ranked[: max(0, candidate_count - 1)]


def evaluate(dataset_path, protocol_path=DEFAULT_PROTOCOL, split="holdout", candidate_count=5,
             top_n=18, min_sample_size=100, alpha=0.001, target_rate=0.50):
    dataset, records = load_records(dataset_path, split)
    if len(records) < candidate_count:
        raise ValueError(f"split {split!r} has only {len(records)} records; candidate_count={candidate_count}")

    protocol = load_protocol(protocol_path)
    metric = protocol.get("metrics", {}).get("history_label_forced_choice", {})
    candidate_count = int(metric.get("candidate_count", candidate_count))
    top_n = int(metric.get("top_weighted_tags", top_n))
    target_rate = float(metric.get("target_top1_accuracy", target_rate))
    alpha = float(metric.get("alpha", alpha))
    min_sample_size = int(metric.get("minimum_holdout_sample_size", min_sample_size))
    seed = protocol.get("candidate_seed", "mayan-kin-history-label-candidates-v2")

    trials = []
    for index, record in enumerate(records):
        tag_weights = expression_weights_for_birth_date(record["birth_date"], top_n=top_n)
        candidates = deterministic_candidates(records, index, candidate_count, seed)
        candidate_scores = [
            {
                "id": candidate["id"],
                "name": candidate["name"],
                "score": score_overlap(tag_weights, detailed_tags(candidate)),
                "detailed_tags": detailed_tags(candidate),
            }
            for candidate in candidates
        ]
        best_score = max(item["score"] for item in candidate_scores)
        winners = [item for item in candidate_scores if item["score"] == best_score]
        predicted_id = winners[0]["id"] if len(winners) == 1 else None
        tags = detailed_tags(record)
        hits = sorted(set(tag_weights) & set(tags))
        precision = len(hits) / len(tag_weights) if tag_weights else 0.0
        recall = len(hits) / len(tags) if tags else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if precision + recall else 0.0
        trials.append({
            "id": record["id"],
            "name": record["name"],
            "birth_date": record["birth_date"],
            "split": record["split"],
            "correct": predicted_id == record["id"],
            "predicted_id": predicted_id,
            "best_score": best_score,
            "correct_candidate_score": next(item["score"] for item in candidate_scores if item["id"] == record["id"]),
            "candidate_scores": candidate_scores,
            "tag_hits": hits,
            "tag_precision": round(precision, 4),
            "tag_recall": round(recall, 4),
            "tag_f1": round(f1, 4),
            "dimension_scores": dimension_scores(tag_weights, record),
        })

    sample_size = len(trials)
    correct_count = sum(1 for item in trials if item["correct"])
    observed_rate = correct_count / sample_size if sample_size else 0.0
    chance_rate = 1 / candidate_count
    p_value = binomial_survival(correct_count, sample_size, chance_rate)
    score = public_figure_score(
        observed_rate,
        chance_rate,
        p_value,
        sample_size,
        min_sample_size,
        alpha,
        target_rate,
    )
    return {
        "dataset_version": dataset.get("version"),
        "dataset_record_count": dataset.get("record_count"),
        "protocol_version": protocol.get("version", "ad_hoc"),
        "split": split,
        "sample_size": sample_size,
        "candidate_count": candidate_count,
        "top_weighted_tags": top_n,
        "correct_count": correct_count,
        "observed_accuracy": round(observed_rate, 4),
        "observed_accuracy_percent": round(observed_rate * 100, 2),
        "chance_accuracy": round(chance_rate, 4),
        "chance_accuracy_percent": round(chance_rate * 100, 2),
        "p_value": p_value,
        "alpha": alpha,
        "target_accuracy_percent": round(target_rate * 100, 2),
        "history_label_accuracy_score": score["score"],
        "status": score["status"],
        "reason": score["reason"],
        "mean_tag_f1": round(statistics.mean(item["tag_f1"] for item in trials), 4) if trials else 0.0,
        "trials": trials,
    }


def main():
    parser = argparse.ArgumentParser(description="Evaluate detailed history-label holdout matching.")
    parser.add_argument("--dataset", default=str(DEFAULT_DATASET))
    parser.add_argument("--protocol", default=str(DEFAULT_PROTOCOL))
    parser.add_argument("--split", choices=["train", "dev", "holdout", "all"], default="holdout")
    parser.add_argument("--candidate-count", type=int, default=5)
    parser.add_argument("--top-weighted-tags", type=int, default=18)
    parser.add_argument("--min-sample-size", type=int, default=100)
    parser.add_argument("--alpha", type=float, default=0.001)
    parser.add_argument("--target-rate", type=float, default=0.50)
    parser.add_argument("--min-score", type=float, default=90.0)
    parser.add_argument("--write")
    args = parser.parse_args()

    result = evaluate(
        args.dataset,
        protocol_path=args.protocol,
        split=args.split,
        candidate_count=args.candidate_count,
        top_n=args.top_weighted_tags,
        min_sample_size=args.min_sample_size,
        alpha=args.alpha,
        target_rate=args.target_rate,
    )
    print(f"Dataset records: {result['dataset_record_count']}")
    print(f"Evaluated split: {result['split']}")
    print(f"Sample size: {result['sample_size']}")
    print(f"Correct: {result['correct_count']}")
    print(f"Observed accuracy: {result['observed_accuracy_percent']}%")
    print(f"Chance accuracy: {result['chance_accuracy_percent']}%")
    print(f"p-value: {result['p_value']}")
    print(f"History label accuracy score: {result['history_label_accuracy_score']}")
    print(f"Mean tag F1: {result['mean_tag_f1']}")
    print(f"Status: {result['status']}")
    print(f"Reason: {result['reason']}")
    if args.write:
        pathlib.Path(args.write).write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    if result["history_label_accuracy_score"] is None or result["history_label_accuracy_score"] < args.min_score:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
