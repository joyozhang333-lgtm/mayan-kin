#!/usr/bin/env python3
"""Evaluate blinded forced-choice trial responses against an answer key."""

import argparse
import json
import math
import pathlib


def load_json_or_jsonl(path):
    text = pathlib.Path(path).read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError(f"empty input file: {path}")
    if text.startswith("[") or text.startswith("{"):
        payload = json.loads(text)
        if isinstance(payload, dict):
            return payload.get("responses", payload.get("keys", payload.get("packets", [])))
        return payload
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def binomial_survival(successes, trials, probability):
    if trials <= 0:
        return 1.0
    total = 0.0
    for k in range(successes, trials + 1):
        total += math.comb(trials, k) * (probability ** k) * ((1 - probability) ** (trials - k))
    return min(1.0, total)


def scientific_score(observed_rate, chance_rate, p_value, sample_size, min_sample_size, alpha, target_rate):
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
    if observed_rate <= chance_rate:
        score = 50.0
    else:
        denominator = max(0.000001, target_rate - chance_rate)
        score = 60 + 40 * min(1.0, (observed_rate - chance_rate) / denominator)
    return {
        "score": round(score, 2),
        "status": "passed" if score >= 90 else "significant_but_below_target",
        "reason": "score combines forced-choice accuracy, chance baseline, sample size, and significance",
    }


def evaluate(responses_path, key_path, packets_path=None, min_sample_size=30, alpha=0.001, target_rate=0.60):
    responses = load_json_or_jsonl(responses_path)
    keys = load_json_or_jsonl(key_path)
    key_by_trial = {item["trial_id"]: item for item in keys}
    packet_by_trial = {}
    if packets_path:
        packet_payload = json.loads(pathlib.Path(packets_path).read_text(encoding="utf-8"))
        packet_by_trial = {item["trial_id"]: item for item in packet_payload.get("packets", [])}

    scored = []
    for response in responses:
        trial_id = response["trial_id"]
        key = key_by_trial[trial_id]
        selected_label = response.get("selected_label")
        if selected_label is None and "ratings" in response:
            selected_label = max(response["ratings"], key=response["ratings"].get)
        if selected_label is None:
            raise ValueError(f"response for {trial_id} must include selected_label or ratings")
        candidate_count = response.get("candidate_count")
        if candidate_count is None and trial_id in packet_by_trial:
            candidate_count = packet_by_trial[trial_id]["candidate_count"]
        if candidate_count is None:
            candidate_count = response.get("options", 5)
        correct = selected_label == key["correct_label"]
        scored.append({
            "trial_id": trial_id,
            "selected_label": selected_label,
            "correct_label": key["correct_label"],
            "candidate_count": candidate_count,
            "correct": correct,
        })

    sample_size = len(scored)
    correct_count = sum(1 for item in scored if item["correct"])
    observed_rate = correct_count / sample_size if sample_size else 0.0
    candidate_counts = {item["candidate_count"] for item in scored}
    if len(candidate_counts) == 1:
        chance_rate = 1 / next(iter(candidate_counts))
        p_value = binomial_survival(correct_count, sample_size, chance_rate)
    else:
        chance_rate = sum(1 / item["candidate_count"] for item in scored) / sample_size
        p_value = None

    score = scientific_score(
        observed_rate,
        chance_rate,
        p_value if p_value is not None else 1.0,
        sample_size,
        min_sample_size,
        alpha,
        target_rate,
    )
    return {
        "sample_size": sample_size,
        "correct_count": correct_count,
        "observed_accuracy": round(observed_rate, 4),
        "observed_accuracy_percent": round(observed_rate * 100, 2),
        "chance_accuracy": round(chance_rate, 4),
        "chance_accuracy_percent": round(chance_rate * 100, 2),
        "p_value": p_value,
        "alpha": alpha,
        "target_accuracy_percent": round(target_rate * 100, 2),
        "scientific_accuracy_score": score["score"],
        "status": score["status"],
        "reason": score["reason"],
        "trials": scored,
    }


def main():
    parser = argparse.ArgumentParser(description="Evaluate Mayan Kin blind trial responses.")
    parser.add_argument("--responses", required=True, help="JSON or JSONL response file")
    parser.add_argument("--key", required=True, help="Answer key generated by generate_blind_trial_packets.py")
    parser.add_argument("--packets", help="Optional blinded packets file")
    parser.add_argument("--min-sample-size", type=int, default=30)
    parser.add_argument("--alpha", type=float, default=0.001)
    parser.add_argument("--target-rate", type=float, default=0.60)
    parser.add_argument("--min-score", type=float, default=90.0)
    parser.add_argument("--write", help="Write JSON evaluation result")
    args = parser.parse_args()

    result = evaluate(
        args.responses,
        args.key,
        packets_path=args.packets,
        min_sample_size=args.min_sample_size,
        alpha=args.alpha,
        target_rate=args.target_rate,
    )
    print(f"Sample size: {result['sample_size']}")
    print(f"Correct: {result['correct_count']}")
    print(f"Observed accuracy: {result['observed_accuracy_percent']}%")
    print(f"Chance accuracy: {result['chance_accuracy_percent']}%")
    print(f"p-value: {result['p_value']}")
    print(f"Scientific accuracy score: {result['scientific_accuracy_score']}")
    print(f"Status: {result['status']}")
    print(f"Reason: {result['reason']}")

    if args.write:
        pathlib.Path(args.write).write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    if result["scientific_accuracy_score"] is None or result["scientific_accuracy_score"] < args.min_score:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
