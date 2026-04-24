#!/usr/bin/env python3
"""Generate a locked prospective prediction registry."""

import argparse
import datetime as dt
import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mayan_kin.core import build_personal_report, build_yearly_report, calc_five_destiny, date_to_kin


PROTOCOL_VERSION = "prospective_prediction_v1"


def load_subjects(path):
    payload = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    return payload.get("subjects", payload.get("records", []))


def prediction_id_for(subject, target_year):
    source_id = subject.get("id") or subject.get("participant_id") or subject.get("name", "anonymous")
    digest = hashlib.sha256(
        f"{PROTOCOL_VERSION}:{source_id}:{subject['birth_date']}:{target_year}".encode("utf-8")
    ).hexdigest()
    return digest[:16]


def build_prediction(subject, target_year, locked_at):
    birth_date = subject["birth_date"]
    destiny = calc_five_destiny(date_to_kin(birth_date))
    personal = build_personal_report(destiny, birth_date=birth_date, style="deep")
    signature = personal["deep_analysis"]["expression_profile"]["evaluation_signature"]
    yearly = build_yearly_report(birth_date, target_year, style="deep")
    top_tags = signature["primary_tags"][:12]
    top_fields = signature["primary_fields"][:5]
    return {
        "prediction_id": prediction_id_for(subject, target_year),
        "protocol_version": PROTOCOL_VERSION,
        "locked_at": locked_at,
        "not_evaluable_before": f"{target_year}-12-31",
        "subject": {
            "id": subject.get("id") or subject.get("participant_id"),
            "name": subject.get("name"),
            "birth_date": birth_date,
            "source_url": subject.get("source_url"),
        },
        "target_year": target_year,
        "prediction": {
            "top_expression_tags": top_tags,
            "top_expression_fields": top_fields,
            "yearly_core_theme": yearly["summary"]["core_theme"],
            "yearly_action_bias": yearly["action_guide"]["focus"][:3],
            "falsifiable_claims": [
                f"Independent evidence coded after {target_year}-12-31 should contain at least 3 of the top expression tags: {', '.join(top_tags[:8])}.",
                f"Public work or life events should be more consistent with these fields than with randomly sampled candidate fields: {', '.join(top_fields)}.",
                "If no independent evidence can be coded, this prediction must be marked unevaluable rather than counted as a success.",
            ],
        },
    }


def build_registry(subjects, target_year):
    locked_at = dt.datetime.now(dt.timezone.utc).isoformat()
    predictions = [build_prediction(subject, target_year, locked_at) for subject in subjects]
    return {
        "version": PROTOCOL_VERSION,
        "created_at": locked_at,
        "target_year": target_year,
        "claim_boundary": "Prospective predictions are only evaluable against future independent evidence collected after the lock date.",
        "prediction_count": len(predictions),
        "predictions": predictions,
    }


def main():
    parser = argparse.ArgumentParser(description="Generate locked prospective Mayan Kin predictions.")
    parser.add_argument("--subjects", required=True, help="JSON file with subjects or records")
    parser.add_argument("--target-year", type=int, required=True)
    parser.add_argument("--limit", type=int, help="Optional maximum number of subjects")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    subjects = load_subjects(args.subjects)
    if args.limit:
        subjects = subjects[: args.limit]
    registry = build_registry(subjects, args.target_year)
    output_path = pathlib.Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Predictions: {registry['prediction_count']}")
    print(f"Output: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
