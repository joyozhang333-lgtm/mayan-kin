#!/usr/bin/env python3
"""Create no-Kin detailed history labels for public figure validation.

This script intentionally does not import `mayan_kin`. It labels public evidence
from Wikidata/Wikipedia only, so the answer labels are not generated from Kin,
seal, tone, or report output.
"""

import argparse
import datetime as dt
import json
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request


USER_AGENT = "mayan-kin-validation/2.0 (https://github.com/joyozhang333-lgtm/mayan-kin)"
WIKIDATA_API = "https://www.wikidata.org/w/api.php"
WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"
DATASET_VERSION = "public_figure_history_labels_v2"
DEFAULT_CUTOFF_YEAR = 2020


DIMENSION_RULES = {
    "core_achievements": [
        (["award", "prize", "nobel", "oscar", "grammy", "champion", "won", "winner"], ["public_output", "recognition", "achievement"]),
        (["founded", "co-founded", "founded", "established", "launched"], ["founding", "institution_building", "initiative"]),
        (["invented", "discovered", "developed", "pioneer", "breakthrough"], ["innovation", "invention", "scientific_research"]),
        (["president", "prime minister", "leader", "governor", "minister"], ["leadership", "public_choice", "strategy"]),
        (["bestselling", "published", "novel", "book", "wrote"], ["communication", "message", "creativity"]),
    ],
    "recurring_themes": [
        (["civil rights", "human rights", "freedom", "justice", "equality"], ["human_rights", "justice", "social_change"]),
        (["religion", "spiritual", "faith", "theology", "monk", "priest"], ["spiritual_depth", "wisdom", "truth"]),
        (["science", "physics", "chemistry", "mathematics", "research"], ["scientific_research", "analysis", "precision"]),
        (["business", "entrepreneur", "company", "industry", "market"], ["resource_gathering", "manifestation", "strategy"]),
        (["art", "painting", "music", "film", "performance", "design"], ["art", "aesthetics", "performance"]),
        (["environment", "ecology", "climate", "land"], ["ecology", "public_support", "social_change"]),
    ],
    "turning_points": [
        (["exile", "imprisoned", "arrested", "revolution", "war", "coup"], ["crisis_catalyst", "transformation", "justice"]),
        (["resigned", "retired", "dismissed", "fired", "bankrupt"], ["transition", "death_rebirth", "system_change"]),
        (["converted", "moved", "emigrated", "immigrated", "returned"], ["cross_boundary", "transition", "navigation"]),
        (["controversy", "scandal", "criticized", "lawsuit"], ["challenge_authority", "truth", "reflection"]),
    ],
    "relationship_patterns": [
        (["married", "spouse", "partner", "wife", "husband"], ["relationship", "devotion", "community"]),
        (["collaborated", "collaboration", "co-founder", "cofounder", "with"], ["cooperation", "connection", "collective_work"]),
        (["family", "father", "mother", "children", "daughter", "son"], ["nurturing", "community", "relationship"]),
        (["mentor", "student", "teacher", "professor"], ["teaching", "wisdom", "public_support"]),
    ],
    "public_expression": [
        (["speech", "orator", "talk show", "interview", "broadcast", "podcast"], ["voice", "communication", "media"]),
        (["film", "television", "stage", "concert", "performance"], ["performance", "public_style", "entertainment"]),
        (["wrote", "writer", "journalist", "essay", "book"], ["message", "voice", "communication"]),
        (["visual", "style", "fashion", "aesthetic", "design"], ["public_style", "aesthetics", "symbolic_design"]),
    ],
    "spiritual_or_value_themes": [
        (["peace", "nonviolence", "compassion", "humanitarian"], ["humanitarian", "moral_clarity", "public_light"]),
        (["truth", "ethics", "moral", "justice", "rights"], ["truth", "moral_clarity", "justice"]),
        (["enlightenment", "wisdom", "philosophy", "psychology"], ["wisdom", "psychology", "spiritual_depth"]),
    ],
    "crisis_and_rebirth": [
        (["illness", "injury", "disabled", "disease", "pain"], ["healing", "embodiment", "transformation"]),
        (["death", "assassinated", "killed", "suicide"], ["death_rebirth", "crisis_catalyst", "public_healing"]),
        (["survived", "recovered", "comeback", "revival"], ["reinvention", "transformation", "endurance"]),
        (["exile", "prison", "imprisoned", "persecuted"], ["liberation", "endurance", "social_change"]),
    ],
}


def chunked(items, size):
    for index in range(0, len(items), size):
        yield items[index:index + size]


def http_get_json(url, timeout):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.load(response)


def fetch_enwiki_titles(qids, timeout=45, sleep_seconds=0.05):
    titles = {}
    for batch in chunked(qids, 50):
        params = {
            "action": "wbgetentities",
            "format": "json",
            "ids": "|".join(batch),
            "props": "sitelinks",
            "sitefilter": "enwiki",
        }
        url = WIKIDATA_API + "?" + urllib.parse.urlencode(params)
        payload = http_get_json(url, timeout)
        for qid, entity in payload.get("entities", {}).items():
            sitelink = entity.get("sitelinks", {}).get("enwiki")
            if sitelink and sitelink.get("title"):
                titles[qid] = sitelink["title"]
        time.sleep(sleep_seconds)
    return titles


def fetch_extracts(titles, timeout=45, sleep_seconds=0.05):
    extracts = {}
    page_urls = {}
    for batch in chunked(titles, 50):
        params = {
            "action": "query",
            "format": "json",
            "prop": "extracts|info",
            "inprop": "url",
            "exintro": "1",
            "explaintext": "1",
            "redirects": "1",
            "titles": "|".join(batch),
        }
        url = WIKIPEDIA_API + "?" + urllib.parse.urlencode(params)
        payload = http_get_json(url, timeout)
        for page in payload.get("query", {}).get("pages", {}).values():
            title = page.get("title")
            if not title:
                continue
            extracts[title] = clean_text(page.get("extract", ""))
            if page.get("fullurl"):
                page_urls[title] = page["fullurl"]
        time.sleep(sleep_seconds)
    return extracts, page_urls


def clean_text(text):
    return re.sub(r"\s+", " ", (text or "").strip())


def split_sentences(text):
    if not text:
        return []
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [part.strip() for part in parts if len(part.strip()) >= 20]


def years_in_text(text):
    return [int(value) for value in re.findall(r"\b(1[5-9]\d{2}|20\d{2})\b", text)]


def apply_dimension_rules(text):
    haystack = text.lower()
    dimensions = {}
    all_tags = set()
    for dimension, rules in DIMENSION_RULES.items():
        tags = set()
        evidence = []
        for keywords, rule_tags in rules:
            hits = [keyword for keyword in keywords if keyword in haystack]
            if hits:
                tags.update(rule_tags)
                evidence.append({"keywords": hits[:5], "tags": rule_tags})
        dimensions[dimension] = {
            "tags": sorted(tags),
            "evidence_rules": evidence[:8],
        }
        all_tags.update(tags)
    return dimensions, sorted(all_tags)


def time_split_sentences(sentences, cutoff_year):
    before = []
    after = []
    undated = []
    for sentence in sentences:
        years = years_in_text(sentence)
        if not years:
            undated.append(sentence)
        elif min(years) <= cutoff_year:
            before.append(sentence)
        elif min(years) > cutoff_year:
            after.append(sentence)
    return {
        "cutoff_year": cutoff_year,
        "pre_cutoff_sentences": before[:8],
        "post_cutoff_sentences": after[:8],
        "undated_context_sentences": undated[:8],
    }


def build_history_label(record, title, extract, page_url, cutoff_year):
    source_text = " ".join(
        filter(
            None,
            [
                record.get("description", ""),
                ", ".join(record.get("occupations", [])),
                extract,
            ],
        )
    )
    dimensions, detailed_tags = apply_dimension_rules(source_text)
    sentences = split_sentences(extract)
    split = time_split_sentences(sentences, cutoff_year)
    pre_dimensions, pre_tags = apply_dimension_rules(" ".join(split["pre_cutoff_sentences"]))
    post_dimensions, post_tags = apply_dimension_rules(" ".join(split["post_cutoff_sentences"]))
    return {
        **record,
        "wikipedia_title": title,
        "wikipedia_url": page_url,
        "wikipedia_extract": extract[:1800],
        "history_labels": {
            "label_protocol": "public_history_labels_v2",
            "leakage_guard": {
                "uses_kin": False,
                "uses_birth_chart": False,
                "uses_public_biography_only": True,
                "script": "scripts/enrich_public_figure_history_labels.py",
            },
            "dimensions": dimensions,
            "detailed_tags": detailed_tags,
            "tag_count": len(detailed_tags),
        },
        "time_split": {
            **split,
            "pre_cutoff_tags": pre_tags,
            "post_cutoff_tags": post_tags,
            "pre_cutoff_dimensions": pre_dimensions,
            "post_cutoff_dimensions": post_dimensions,
            "time_split_note": "Only sentences with explicit years are placed into pre/post cutoff buckets; undated context is not used as future evidence.",
        },
    }


def enrich_records(records, cutoff_year, limit=None, include_splits=None, timeout=45):
    selected = records
    if include_splits:
        allowed = set(include_splits)
        selected = [record for record in selected if record.get("split") in allowed]
    if limit:
        selected = selected[:limit]

    qids = [record["id"] for record in selected]
    titles_by_qid = fetch_enwiki_titles(qids, timeout=timeout)
    extracts_by_title, urls_by_title = fetch_extracts(list(titles_by_qid.values()), timeout=timeout)

    enriched = []
    skipped = []
    for record in selected:
        title = titles_by_qid.get(record["id"])
        extract = extracts_by_title.get(title or "", "")
        if not title or not extract:
            skipped.append({"id": record["id"], "name": record["name"], "reason": "missing_enwiki_extract"})
            continue
        enriched.append(
            build_history_label(
                record,
                title,
                extract,
                urls_by_title.get(title),
                cutoff_year,
            )
        )
    return enriched, skipped


def split_counts(records):
    counts = {"train": 0, "dev": 0, "holdout": 0}
    for item in records:
        counts[item.get("split")] = counts.get(item.get("split"), 0) + 1
    return counts


def build_dataset(source_payload, enriched, skipped, cutoff_year):
    return {
        "version": DATASET_VERSION,
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "source_dataset_version": source_payload.get("version"),
        "source_record_count": source_payload.get("record_count"),
        "record_count": len(enriched),
        "split_counts": split_counts(enriched),
        "cutoff_year": cutoff_year,
        "source_policy": {
            "wikidata": "QID, birth date, description, occupation, and enwiki sitelink.",
            "wikipedia": "English Wikipedia intro extract via MediaWiki Action API.",
            "license_note": "Wikipedia text is CC BY-SA; this dataset stores short extracts and derived labels for validation. Check license obligations before redistribution.",
        },
        "labeling_policy": {
            "no_kin_leakage": True,
            "no_mayan_import": True,
            "human_meaning": "Labels describe public biography themes, not private personality proof.",
            "dimensions": list(DIMENSION_RULES),
        },
        "skipped_count": len(skipped),
        "skipped": skipped,
        "records": enriched,
    }


def main():
    parser = argparse.ArgumentParser(description="Enrich public figures with detailed no-Kin history labels.")
    parser.add_argument("--input", required=True, help="Source public figure JSON dataset")
    parser.add_argument("--output", required=True, help="Output enriched JSON dataset")
    parser.add_argument("--cutoff-year", type=int, default=DEFAULT_CUTOFF_YEAR)
    parser.add_argument("--limit", type=int, help="Optional max records for smoke tests")
    parser.add_argument("--splits", nargs="*", choices=["train", "dev", "holdout"], help="Optional split filter")
    parser.add_argument("--timeout", type=int, default=45)
    args = parser.parse_args()

    payload = json.loads(pathlib.Path(args.input).read_text(encoding="utf-8"))
    enriched, skipped = enrich_records(
        payload["records"],
        cutoff_year=args.cutoff_year,
        limit=args.limit,
        include_splits=args.splits,
        timeout=args.timeout,
    )
    dataset = build_dataset(payload, enriched, skipped, args.cutoff_year)
    output_path = pathlib.Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(dataset, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Source records: {payload.get('record_count')}")
    print(f"Enriched records: {dataset['record_count']}")
    print(f"Split counts: {dataset['split_counts']}")
    print(f"Skipped: {dataset['skipped_count']}")
    print(f"Output: {output_path}")
    if not enriched:
        print("No records were enriched.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
