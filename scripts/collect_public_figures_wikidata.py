#!/usr/bin/env python3
"""Collect public figure samples from Wikidata for reproducible validation."""

import argparse
import datetime as dt
import hashlib
import json
import pathlib
import re
import sys
import urllib.parse
import urllib.request


WIKIDATA_SPARQL_URL = "https://query.wikidata.org/sparql"
DATASET_VERSION = "wikidata_public_figures_v1"
DEFAULT_SPLIT_SEED = "mayan-kin-public-figure-holdout-v1"
USER_AGENT = "mayan-kin-validation/1.0 (https://github.com/joyozhang333-lgtm/mayan-kin)"

DEFAULT_OCCUPATIONS = {
    "Q82955": "politician",
    "Q33999": "actor",
    "Q36180": "writer",
    "Q177220": "singer",
    "Q937857": "association football player",
    "Q1930187": "journalist",
    "Q43845": "businessperson",
    "Q2526255": "film director",
    "Q36834": "composer",
    "Q10800557": "film producer",
    "Q1028181": "painter",
    "Q4964182": "philosopher",
    "Q482980": "author",
    "Q169470": "physicist",
    "Q28389": "screenwriter",
    "Q49757": "poet",
    "Q901": "scientist",
    "Q1622272": "university teacher",
    "Q250867": "Catholic priest",
    "Q639669": "musician",
    "Q81096": "engineer",
    "Q205375": "inventor",
    "Q82594": "computer scientist",
    "Q18844224": "science communicator",
    "Q2066131": "athlete",
}

KEYWORD_TAG_RULES = [
    (
        ["politician", "president", "minister", "governor", "mayor", "diplomat", "activist", "statesman"],
        ["leadership", "public_choice", "social_change", "human_rights", "strategy"],
    ),
    (
        ["actor", "actress", "film", "television", "performer", "comedian"],
        ["performance", "art", "public_style", "entertainment"],
    ),
    (
        ["singer", "musician", "composer", "rapper", "songwriter", "vocalist"],
        ["performance", "art", "voice", "harmony", "public_output"],
    ),
    (
        ["writer", "novelist", "poet", "journalist", "screenwriter", "author", "playwright"],
        ["communication", "voice", "media", "creativity", "message"],
    ),
    (
        ["scientist", "physicist", "chemist", "mathematician", "engineer", "inventor", "computer scientist"],
        ["scientific_research", "precision", "analysis", "invention", "innovation", "truth"],
    ),
    (
        ["businessperson", "entrepreneur", "executive", "investor", "founder"],
        ["leadership", "resource_gathering", "manifestation", "strategy", "public_output"],
    ),
    (
        ["athlete", "football", "basketball", "tennis", "sport", "player"],
        ["vitality", "body", "performance", "endurance", "rhythm"],
    ),
    (
        ["artist", "painter", "sculptor", "designer", "architect", "photographer"],
        ["art", "aesthetics", "symbolic_design", "public_style", "creativity"],
    ),
    (
        ["philosopher", "psychologist", "psychiatrist", "theologian", "spiritual", "monk", "religious", "priest"],
        ["psychology", "symbolism", "spiritual_depth", "wisdom", "truth"],
    ),
    (
        ["lawyer", "judge", "jurist", "justice"],
        ["justice", "truth", "order", "analysis"],
    ),
    (
        ["humanitarian", "philanthropist", "civil rights", "peace"],
        ["humanitarian", "public_support", "social_change"],
    ),
    (
        ["director", "producer"],
        ["vision", "media", "product_storytelling", "strategy", "art"],
    ),
    (
        ["teacher", "professor", "educator", "academic"],
        ["teaching", "wisdom", "scientific_research", "communication"],
    ),
]


def build_query(limit):
    values = " ".join(f"wd:{qid}" for qid in DEFAULT_OCCUPATIONS)
    return f"""
SELECT ?person ?personLabel ?personDescription ?birth ?occupation ?occupationLabel WHERE {{
  VALUES ?occupation {{ {values} }}
  ?person wdt:P31 wd:Q5 ;
          wdt:P106 ?occupation .
  ?person p:P569/psv:P569 ?birth_node .
  ?birth_node wikibase:timePrecision "11"^^xsd:integer .
  ?birth_node wikibase:timeValue ?birth .
  ?person rdfs:label ?personLabel FILTER(LANG(?personLabel) = "en") .
  ?occupation rdfs:label ?occupationLabel FILTER(LANG(?occupationLabel) = "en") .
  OPTIONAL {{ ?person schema:description ?personDescription FILTER(LANG(?personDescription) = "en") . }}
}}
LIMIT {int(limit)}
""".strip()


def fetch_wikidata(limit, timeout):
    query = build_query(limit)
    url = WIKIDATA_SPARQL_URL + "?" + urllib.parse.urlencode({"query": query, "format": "json"})
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.load(response), query


def qid_from_uri(uri):
    return uri.rstrip("/").rsplit("/", 1)[-1]


def parse_birth_date(value):
    clean = value.replace("Z", "").split("T", 1)[0].lstrip("+")
    if clean.startswith("-"):
        return None
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", clean):
        return None
    return clean


def infer_observed_tags(occupations, description):
    haystack = " ".join(occupations + [description or ""]).lower()
    tags = set()
    for keywords, rule_tags in KEYWORD_TAG_RULES:
        if any(keyword in haystack for keyword in keywords):
            tags.update(rule_tags)
    return sorted(tags)


def split_for_qid(qid, seed=DEFAULT_SPLIT_SEED):
    digest = hashlib.sha256(f"{seed}:{qid}".encode("utf-8")).hexdigest()
    bucket = int(digest[:8], 16) % 100
    if bucket < 70:
        return "train"
    if bucket < 85:
        return "dev"
    return "holdout"


def normalize_bindings(bindings, split_seed=DEFAULT_SPLIT_SEED, min_tags=2):
    people = {}
    for row in bindings:
        qid = qid_from_uri(row["person"]["value"])
        birth_date = parse_birth_date(row["birth"]["value"])
        if not birth_date:
            continue
        person = people.setdefault(
            qid,
            {
                "id": qid,
                "name": row["personLabel"]["value"],
                "birth_date": birth_date,
                "description": row.get("personDescription", {}).get("value", ""),
                "occupations": [],
                "source_url": row["person"]["value"],
            },
        )
        occupation = row.get("occupationLabel", {}).get("value")
        if occupation and occupation not in person["occupations"]:
            person["occupations"].append(occupation)

    records = []
    for qid, person in people.items():
        person["occupations"] = sorted(person["occupations"])
        person["observed_tags"] = infer_observed_tags(person["occupations"], person["description"])
        if len(person["observed_tags"]) < min_tags:
            continue
        person["split"] = split_for_qid(qid, split_seed)
        person["blind_note"] = "; ".join(filter(None, [person["description"], ", ".join(person["occupations"])]))
        records.append(person)

    def sort_key(item):
        numeric = int(item["id"][1:]) if item["id"][1:].isdigit() else 0
        return (numeric, item["id"])

    return sorted(records, key=sort_key)


def split_counts(records):
    counts = {"train": 0, "dev": 0, "holdout": 0}
    for item in records:
        counts[item["split"]] = counts.get(item["split"], 0) + 1
    return counts


def build_dataset(bindings, query, split_seed, min_tags):
    records = normalize_bindings(bindings, split_seed=split_seed, min_tags=min_tags)
    return {
        "version": DATASET_VERSION,
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "source": {
            "name": "Wikidata Query Service",
            "url": WIKIDATA_SPARQL_URL,
            "query": query,
            "license_note": "Wikidata content is available under CC0; verify downstream attribution needs for derived datasets.",
        },
        "split_seed": split_seed,
        "split_policy": {
            "train": "hash bucket 0-69",
            "dev": "hash bucket 70-84",
            "holdout": "hash bucket 85-99",
        },
        "record_count": len(records),
        "split_counts": split_counts(records),
        "records": records,
    }


def main():
    parser = argparse.ArgumentParser(description="Collect 1000+ public figure validation samples from Wikidata.")
    parser.add_argument("--limit", type=int, default=1600, help="Maximum Wikidata rows to request")
    parser.add_argument("--timeout", type=int, default=90, help="HTTP timeout in seconds")
    parser.add_argument("--min-records", type=int, default=1000, help="Minimum normalized records required")
    parser.add_argument("--min-tags", type=int, default=2, help="Minimum observed tags per record")
    parser.add_argument("--split-seed", default=DEFAULT_SPLIT_SEED)
    parser.add_argument("--output", required=True, help="Output JSON dataset path")
    args = parser.parse_args()

    payload, query = fetch_wikidata(args.limit, args.timeout)
    bindings = payload["results"]["bindings"]
    dataset = build_dataset(bindings, query, split_seed=args.split_seed, min_tags=args.min_tags)

    output_path = pathlib.Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(dataset, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Wikidata rows: {len(bindings)}")
    print(f"Normalized records: {dataset['record_count']}")
    print(f"Split counts: {dataset['split_counts']}")
    print(f"Output: {output_path}")

    if dataset["record_count"] < args.min_records:
        print(
            f"Only {dataset['record_count']} records collected; required {args.min_records}.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
