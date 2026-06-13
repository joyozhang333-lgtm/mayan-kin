"""Report styling helpers (extracted from core.py)."""

from .constants import *  # noqa: F401,F403


def normalize_report_style(style):
    if not style:
        return "basic"
    normalized = str(style).strip().lower().replace(" ", "_")
    alias_map = {
        "basic": "basic",
        "simple": "basic",
        "beginner": "basic",
        "novice": "basic",
        "xiaobai": "basic",
        "deep": "deep",
        "deep_dialogue": "deep",
        "consulting": "deep",
        "consultation": "deep",
        "advisor": "deep",
        "professional": "deep",
        "pro": "deep",
        "expert": "deep",
    }
    if normalized not in alias_map:
        valid = ", ".join(sorted(STYLE_CONFIG))
        raise ValueError(f"未知报告风格 '{style}'，可选值: {valid}")
    return alias_map[normalized]


def style_meta(style):
    normalized = normalize_report_style(style)
    return {
        "key": normalized,
        "label": STYLE_CONFIG[normalized]["label"],
        "description": STYLE_CONFIG[normalized]["description"],
    }


def stylize_text(text, style, field="general"):
    if not text:
        return text
    normalized = normalize_report_style(style)
    if normalized == "basic":
        basic_prefix = {
            "questions": "可以先问自己：",
            "decision_checks": "先检查：",
            "instructions": "使用时记住：",
            "prompts": "可直接这样问：",
        }
        prefix = basic_prefix.get(field)
        return f"{prefix}{text}" if prefix else text
    if normalized == "deep":
        return text
    return text


def stylize_sequence(items, style, field):
    return [stylize_text(item, style, field) for item in items]


def stylize_summary(summary, style):
    return {key: stylize_text(value, style, "summary") for key, value in summary.items()}


def stylize_growth_path(path, style):
    stylized = []
    for item in path:
        stylized.append(
            {
                **item,
                "focus": stylize_text(item["focus"], style, "focus"),
                "action": stylize_text(item["action"], style, "action"),
            }
        )
    return stylized


def stylize_action_guide(action_guide, style):
    return {
        section: stylize_sequence(items, style, "action")
        for section, items in action_guide.items()
    }


def stylize_delivery_layers(layers, style):
    stylized = {}
    for section_name, section in layers.items():
        stylized_section = {}
        for field, value in section.items():
            if isinstance(value, list):
                stylized_section[field] = stylize_sequence(value, style, field)
            elif isinstance(value, str):
                stylized_section[field] = stylize_text(value, style, field)
            else:
                stylized_section[field] = value
        stylized[section_name] = stylized_section
    return stylized


