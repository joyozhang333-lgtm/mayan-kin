"""Knowledge card routing for mayan-kin."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE_INDEX_PATH = ROOT / "references" / "knowledge-index.json"

DEFAULT_FOUNDATION_IDS = ["five_destiny", "seals", "tones"]
DEFAULT_APPLICATION_IDS = ["guidance"]


def load_knowledge_index():
    return json.loads(KNOWLEDGE_INDEX_PATH.read_text(encoding="utf-8"))


def _normalized_terms(card):
    fields = []
    for key in ("id", "title", "category", "when_to_load"):
        fields.append(str(card.get(key, "")))
    for key in ("keywords", "use_cases"):
        fields.extend(card.get(key, []))
    return [item.casefold() for item in fields if item]


def recommend_knowledge_cards(query, limit=4):
    query_text = (query or "").strip().casefold()
    payload = load_knowledge_index()
    cards = payload["cards"]

    if not query_text:
        defaults = DEFAULT_FOUNDATION_IDS + DEFAULT_APPLICATION_IDS
        return [card for card in cards if card["id"] in defaults][:limit]

    scored = []
    for order, card in enumerate(cards):
        score = 0
        for term in _normalized_terms(card):
            if term and term in query_text:
                score += 3
            elif term:
                overlaps = [token for token in term.replace("/", " ").split() if token and token in query_text]
                score += len(overlaps)
        if card["category"] == "foundation" and any(token in query_text for token in ("图腾", "调性", "kin", "玛雅", "印记")):
            score += 1
        if score > 0:
            scored.append((score, order, card))

    if not scored:
        defaults = DEFAULT_FOUNDATION_IDS + DEFAULT_APPLICATION_IDS
        return [card for card in cards if card["id"] in defaults][:limit]

    scored.sort(key=lambda item: (-item[0], item[1]))
    chosen = [card for _, _, card in scored[:limit]]

    if not any(card["id"] == "guidance" for card in chosen):
        guidance = next((card for card in cards if card["id"] == "guidance"), None)
        if guidance:
            if len(chosen) < limit:
                chosen.append(guidance)
            elif chosen:
                chosen[-1] = guidance

    return chosen


def route_query(query, limit=4):
    payload = load_knowledge_index()
    cards = recommend_knowledge_cards(query, limit=limit)
    return {
        "query": query,
        "index_version": payload["version"],
        "recommended_cards": cards,
    }
