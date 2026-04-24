#!/usr/bin/env python3
"""Evaluate deep report expression tags against public figure benchmark cases."""

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mayan_kin.core import build_personal_report, calc_five_destiny, date_to_kin


BENCHMARK_PATH = ROOT / "references" / "public-figure-benchmark.json"


def score_case(case):
    destiny = calc_five_destiny(date_to_kin(case["birth_date"]))
    report = build_personal_report(destiny, birth_date=case["birth_date"], style="deep")
    analysis = report["deep_analysis"]
    expression = analysis["expression_profile"]
    generated_tags = set(expression["tags"])
    expected_tags = set(case["expected_tags"])
    primary_tags = set(case["primary_tags"])

    expected_hits = sorted(expected_tags & generated_tags)
    primary_hits = sorted(primary_tags & generated_tags)
    coverage_score = (len(expected_hits) / len(expected_tags)) * 60 if expected_tags else 0
    primary_score = (len(primary_hits) / len(primary_tags)) * 25 if primary_tags else 0
    structure_score = 10 if analysis.get("precision_profile") and expression.get("roles") else 0
    specificity_score = 5 if len(generated_tags) <= 45 else max(0, 5 - ((len(generated_tags) - 45) * 0.25))
    total_score = round(coverage_score + primary_score + structure_score + specificity_score, 2)

    return {
        "name": case["name"],
        "birth_date": case["birth_date"],
        "kin": destiny["kin"],
        "signature": f"{destiny['main']['tone_name']}{destiny['main']['seal_name']}",
        "score": total_score,
        "expected_hits": expected_hits,
        "missing_expected_tags": sorted(expected_tags - generated_tags),
        "primary_hits": primary_hits,
        "generated_tag_count": len(generated_tags),
        "source_url": case["source_url"],
    }


def evaluate(benchmark_path=BENCHMARK_PATH):
    payload = json.loads(pathlib.Path(benchmark_path).read_text(encoding="utf-8"))
    results = [score_case(case) for case in payload["cases"]]
    average_score = round(sum(item["score"] for item in results) / len(results), 2) if results else 0
    return {
        "benchmark_version": payload["version"],
        "case_count": len(results),
        "average_score": average_score,
        "results": results,
    }


def main():
    parser = argparse.ArgumentParser(description="Evaluate public figure benchmark accuracy.")
    parser.add_argument("--benchmark", default=str(BENCHMARK_PATH), help="Path to benchmark JSON")
    parser.add_argument("--min-score", type=float, default=90.0, help="Minimum average score")
    parser.add_argument("--write", help="Write JSON result to this path")
    args = parser.parse_args()

    result = evaluate(args.benchmark)
    print(f"Public figure benchmark cases: {result['case_count']}")
    print(f"Average score: {result['average_score']}")
    for item in result["results"]:
        missing = ", ".join(item["missing_expected_tags"]) or "none"
        print(f"- {item['name']}: {item['score']} | {item['signature']} | missing: {missing}")

    if args.write:
        output_path = pathlib.Path(args.write)
        output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if result["average_score"] < args.min_score:
        print(
            f"Average score {result['average_score']} is below required minimum {args.min_score}",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
