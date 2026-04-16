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


def recommend_report_style(query, cards=None):
    query_text = (query or "").strip().casefold()
    card_ids = {card["id"] for card in (cards or [])}

    professional_terms = (
        "专业", "课程", "内容产品", "prompt", "模板", "结构", "术语", "研究", "系统", "framework"
    )
    consulting_terms = (
        "卡点", "边界", "怎么做", "怎么办", "咨询", "关系", "合盘", "流年", "方向", "事业", "成长"
    )
    beginner_terms = (
        "小白", "不懂", "入门", "先讲清楚", "什么意思", "怎么看", "第一次"
    )

    if any(term in query_text for term in professional_terms):
        return "professional"
    if any(term in query_text for term in beginner_terms):
        return "beginner"
    if any(term in query_text for term in consulting_terms):
        return "consulting"
    if {"compatibility", "yearly", "guidance", "career_emotion"} & card_ids:
        return "consulting"
    if {"oracle", "earth_families"} & card_ids:
        return "professional"
    return "beginner"


def recommend_report_mode(query, cards=None):
    query_text = (query or "").strip().casefold()
    card_ids = {card["id"] for card in (cards or [])}

    has_yearly_signal = (
        "流年" in query_text
        or "年度" in query_text
        or "yearly" in query_text
        or "今年" in query_text
        or "明年" in query_text
        or "202" in query_text
        or "yearly" in card_ids
    )
    has_compatibility_signal = (
        "合盘" in query_text
        or "关系" in query_text
        or "compatibility" in query_text
        or "另一人" in query_text
        or "边界" in query_text
        or "compatibility" in card_ids
    )

    if has_yearly_signal and has_compatibility_signal:
        return "combined"
    if has_yearly_signal:
        return "yearly"
    if has_compatibility_signal:
        return "compatibility"
    return "personal"


def build_auto_plan(query, limit=4):
    routed = route_query(query, limit=limit)
    recommended_cards = routed["recommended_cards"]
    style = recommend_report_style(query, recommended_cards)
    report_mode = recommend_report_mode(query, recommended_cards)
    card_ids = [card["id"] for card in recommended_cards]

    if style == "professional":
        reason = "问题更偏专业结构、内容复用或方法论表达，适合保留更多术语和结构。"
    elif style == "consulting":
        reason = "问题更偏现实卡点、关系判断或行动建议，适合用咨询版突出判断点和下一步。"
    else:
        reason = "问题更偏入门理解或概念澄清，适合先用小白版降低术语门槛。"

    return {
        "query": query,
        "index_version": routed["index_version"],
        "recommended_style": style,
        "recommended_report_mode": report_mode,
        "recommended_cards": recommended_cards,
        "card_ids": card_ids,
        "reason": reason,
    }
