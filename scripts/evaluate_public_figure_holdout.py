#!/usr/bin/env python3
"""Evaluate public figure forced-choice matching on a frozen holdout split."""

import argparse
import hashlib
import json
import math
import pathlib
import statistics
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mayan_kin.core import build_personal_report, calc_five_destiny, date_to_kin


DEFAULT_DATASET = ROOT / "references" / "public-figures-wikidata-1000.json"
DEFAULT_PROTOCOL = ROOT / "references" / "frozen-scoring-protocol-v1.json"


def binomial_survival(successes, trials, probability):
    if trials <= 0:
        return 1.0
    total = 0.0
    for k in range(successes, trials + 1):
        total += math.comb(trials, k) * (probability ** k) * ((1 - probability) ** (trials - k))
    return min(1.0, total)


def public_figure_score(observed_rate, chance_rate, p_value, sample_size, min_sample_size, alpha, target_rate):
    if sample_size < min_sample_size:
        return {
            "score": None,
            "status": "insufficient_sample",
            "reason": f"sample size {sample_size} is below required minimum {min_sample_size}",
        }
    if p_value > alpha:
        return {
            "score": round(min(59.0, observed_rate * 100), 2),
            "status": "not_significant",
            "reason": f"p-value {p_value:.6g} is above alpha {alpha}",
        }
    denominator = max(0.000001, target_rate - chance_rate)
    score = 60 + 40 * min(1.0, max(0.0, (observed_rate - chance_rate) / denominator))
    return {
        "score": round(score, 2),
        "status": "passed" if score >= 90 else "significant_but_below_target",
        "reason": "score combines forced-choice accuracy, chance baseline, sample size, and significance",
    }


def load_records(dataset_path, split):
    payload = json.loads(pathlib.Path(dataset_path).read_text(encoding="utf-8"))
    records = payload["records"]
    if split != "all":
        records = [item for item in records if item.get("split") == split]
    return payload, records


def expression_weights_for_birth_date(birth_date, top_n):
    destiny = calc_five_destiny(date_to_kin(birth_date))
    report = build_personal_report(destiny, birth_date=birth_date, style="deep")
    signature = report["deep_analysis"]["expression_profile"]["evaluation_signature"]
    weighted = signature["weighted_tags"][:top_n]
    return {item["tag"]: item["weight"] for item in weighted}


def score_overlap(tag_weights, observed_tags):
    observed = set(observed_tags)
    if not tag_weights:
        return 0.0
    return round(sum(weight for tag, weight in tag_weights.items() if tag in observed), 6)


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


def evaluate(dataset_path, protocol_path=DEFAULT_PROTOCOL, split="holdout", candidate_count=5, top_n=18,
             min_sample_size=100, alpha=0.001, target_rate=0.50):
    dataset, records = load_records(dataset_path, split)
    if len(records) < candidate_count:
        raise ValueError(f"split {split!r} has only {len(records)} records; candidate_count={candidate_count}")

    protocol = {}
    if protocol_path and pathlib.Path(protocol_path).exists():
        protocol = json.loads(pathlib.Path(protocol_path).read_text(encoding="utf-8"))
        metric = protocol.get("metrics", {}).get("public_figure_forced_choice", {})
        candidate_count = int(metric.get("candidate_count", candidate_count))
        top_n = int(metric.get("top_weighted_tags", top_n))
        target_rate = float(metric.get("target_top1_accuracy", target_rate))
        alpha = float(metric.get("alpha", alpha))

    seed = protocol.get("candidate_seed", "mayan-kin-public-figure-candidates-v1")
    trials = []
    for index, record in enumerate(records):
        tag_weights = expression_weights_for_birth_date(record["birth_date"], top_n=top_n)
        candidates = deterministic_candidates(records, index, candidate_count, seed)
        candidate_scores = [
            {
                "id": candidate["id"],
                "name": candidate["name"],
                "score": score_overlap(tag_weights, candidate.get("observed_tags", [])),
                "observed_tags": candidate.get("observed_tags", []),
            }
            for candidate in candidates
        ]
        best_score = max(item["score"] for item in candidate_scores)
        winners = [item for item in candidate_scores if item["score"] == best_score]
        predicted_id = winners[0]["id"] if len(winners) == 1 else None
        hits = sorted(set(tag_weights) & set(record.get("observed_tags", [])))
        precision = len(hits) / len(tag_weights) if tag_weights else 0.0
        recall = len(hits) / len(record.get("observed_tags", [])) if record.get("observed_tags") else 0.0
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
        "public_figure_accuracy_score": score["score"],
        "status": score["status"],
        "reason": score["reason"],
        "mean_tag_f1": round(statistics.mean(item["tag_f1"] for item in trials), 4) if trials else 0.0,
        "trials": trials,
    }


def main():
    parser = argparse.ArgumentParser(description="Evaluate public figure holdout matching accuracy.")
    parser.add_argument("--dataset", default=str(DEFAULT_DATASET))
    parser.add_argument("--protocol", default=str(DEFAULT_PROTOCOL))
    parser.add_argument("--split", choices=["train", "dev", "holdout", "all"], default="holdout")
    parser.add_argument("--candidate-count", type=int, default=5)
    parser.add_argument("--top-weighted-tags", type=int, default=18)
    parser.add_argument("--min-sample-size", type=int, default=100)
    parser.add_argument("--alpha", type=float, default=0.001)
    parser.add_argument("--target-rate", type=float, default=0.50)
    parser.add_argument("--min-score", type=float, default=90.0)
    parser.add_argument("--write", help="Write JSON result")
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
    print(f"Public figure accuracy score: {result['public_figure_accuracy_score']}")
    print(f"Mean tag F1: {result['mean_tag_f1']}")
    print(f"Status: {result['status']}")
    print(f"Reason: {result['reason']}")

    if args.write:
        pathlib.Path(args.write).write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    if result["public_figure_accuracy_score"] is None or result["public_figure_accuracy_score"] < args.min_score:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
