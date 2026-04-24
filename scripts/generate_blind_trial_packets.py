#!/usr/bin/env python3
"""Generate blinded forced-choice trial packets for scientific validation."""

import argparse
import json
import pathlib
import random
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mayan_kin.core import (
    SEALS,
    TONES,
    build_personal_report,
    calc_five_destiny,
    date_to_kin,
)


LABELS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def load_participants(path):
    payload = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    participants = payload.get("participants", payload if isinstance(payload, list) else [])
    if not participants:
        raise ValueError("participants input must contain a non-empty participants list")
    for item in participants:
        if "participant_id" not in item or "birth_date" not in item:
            raise ValueError("each participant must include participant_id and birth_date")
    return payload.get("study_id", "mayan-kin-blind-study"), participants


def sanitize_symbols(text):
    sanitized = text
    for token in sorted([item for item in SEALS + TONES if item], key=len, reverse=True):
        sanitized = sanitized.replace(token, "某类能量")
    return sanitized


def build_blind_report_text(birth_date):
    destiny = calc_five_destiny(date_to_kin(birth_date))
    report = build_personal_report(destiny, birth_date=birth_date, style="deep")
    summary = report["summary"]
    analysis = report["deep_analysis"]
    precision = analysis["precision_profile"]
    expression = analysis["expression_profile"]
    lines = [
        "【核心摘要】",
        f"- 主轴: {summary['core_theme']}",
        f"- 资源: {summary['strength']}",
        f"- 功课: {summary['challenge']}",
        "【现实表达】",
    ]
    lines.extend(f"- {item}" for item in expression["summary"])
    lines.append("【可能适配场域】")
    lines.append("- " + "、".join(expression["fields"][:6]))
    lines.append("【验证问题】")
    for item in (expression["public_questions"] + precision["validation_checks"])[:8]:
        lines.append(f"- {item}")
    return sanitize_symbols("\n".join(lines))


def generate_packets(participants, candidate_count, seed):
    if candidate_count < 2:
        raise ValueError("candidate_count must be at least 2")
    if len(participants) < candidate_count:
        raise ValueError("participant count must be >= candidate_count")

    rng = random.Random(seed)
    reports = {
        item["participant_id"]: {
            "report_id": f"R_{item['participant_id']}",
            "report_text": build_blind_report_text(item["birth_date"]),
        }
        for item in participants
    }

    packets = []
    keys = []
    for index, participant in enumerate(participants, start=1):
        participant_id = participant["participant_id"]
        decoy_ids = [item["participant_id"] for item in participants if item["participant_id"] != participant_id]
        selected_ids = [participant_id] + rng.sample(decoy_ids, candidate_count - 1)
        rng.shuffle(selected_ids)
        candidates = []
        correct_label = None
        for label, report_id_key in zip(LABELS, selected_ids):
            report = reports[report_id_key]
            candidates.append({
                "label": label,
                "report_id": report["report_id"],
                "report_text": report["report_text"],
            })
            if report_id_key == participant_id:
                correct_label = label
        trial_id = f"T{index:04d}"
        packets.append({
            "trial_id": trial_id,
            "participant_id": participant_id,
            "candidate_count": candidate_count,
            "candidates": candidates,
        })
        keys.append({
            "trial_id": trial_id,
            "participant_id": participant_id,
            "correct_label": correct_label,
            "correct_report_id": reports[participant_id]["report_id"],
        })
    return packets, keys


def main():
    parser = argparse.ArgumentParser(description="Generate blinded Mayan Kin forced-choice trial packets.")
    parser.add_argument("--participants", required=True, help="JSON file with participant_id and birth_date")
    parser.add_argument("--candidate-count", type=int, default=5, help="Number of candidate reports per trial")
    parser.add_argument("--seed", type=int, default=20260424, help="Deterministic shuffle seed")
    parser.add_argument("--packets-out", required=True, help="Output JSON file for blinded packets")
    parser.add_argument("--key-out", required=True, help="Output JSON file for answer key")
    args = parser.parse_args()

    study_id, participants = load_participants(args.participants)
    packets, keys = generate_packets(participants, args.candidate_count, args.seed)
    packet_payload = {
        "study_id": study_id,
        "candidate_count": args.candidate_count,
        "blinding": "No birth date, Kin number, participant name, or explicit seal/tone symbol is included in report text.",
        "packets": packets,
    }
    key_payload = {
        "study_id": study_id,
        "candidate_count": args.candidate_count,
        "keys": keys,
    }
    pathlib.Path(args.packets_out).write_text(
        json.dumps(packet_payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    pathlib.Path(args.key_out).write_text(
        json.dumps(key_payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Generated {len(packets)} blinded trial packets")
    print(f"Packets: {args.packets_out}")
    print(f"Key: {args.key_out}")


if __name__ == "__main__":
    raise SystemExit(main())
