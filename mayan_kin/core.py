#!/usr/bin/env python3
"""Core Mayan Kin calculation logic."""

from datetime import date

from .knowledge import (
    build_auto_plan,
    load_knowledge_index,
    recommend_knowledge_cards,
    recommend_report_style,
    route_query,
)


SEALS = [
    "",
    "红龙", "白风", "蓝夜", "黄种子", "红蛇",
    "白世界桥", "蓝手", "黄星星", "红月", "白狗",
    "蓝猴", "黄人", "红天行者", "白巫师", "蓝鹰",
    "黄战士", "红地球", "白镜", "蓝风暴", "黄太阳",
]

SEALS_EN = [
    "",
    "Red Dragon", "White Wind", "Blue Night", "Yellow Seed", "Red Serpent",
    "White Worldbridger", "Blue Hand", "Yellow Star", "Red Moon", "White Dog",
    "Blue Monkey", "Yellow Human", "Red Skywalker", "White Wizard", "Blue Eagle",
    "Yellow Warrior", "Red Earth", "White Mirror", "Blue Storm", "Yellow Sun",
]

SEAL_KEYWORDS = [
    "",
    "诞生·滋养·存在", "精神·呼吸·沟通", "梦想·丰盛·直觉", "觉察·目标·开花",
    "生命力·本能·生存", "死亡·平等·机会", "知道·疗愈·完成", "优雅·艺术·美",
    "净化·流动·水", "爱·忠诚·心", "魔法·幻象·游戏", "自由意志·智慧·影响",
    "空间·探索·觉醒", "永恒·魅力·感受力", "视野·创造·心智", "智慧·勇气·质疑",
    "导航·进化·同步", "无限·秩序·反射", "蜕变·催化·能量", "开悟·生命·智慧火",
]

TONES = [
    "",
    "磁性", "月亮", "电力", "自存", "超频",
    "韵律", "共振", "银河", "太阳", "行星",
    "光谱", "水晶", "宇宙",
]

TONES_EN = [
    "",
    "Magnetic", "Lunar", "Electric", "Self-Existing", "Overtone",
    "Rhythmic", "Resonant", "Galactic", "Solar", "Planetary",
    "Spectral", "Crystal", "Cosmic",
]

TONE_KEYWORDS = [
    "",
    "统一·吸引·目的", "极化·挑战·稳定", "激活·连接·服务",
    "定义·形式·测量", "赋权·指挥·辐射", "平衡·组织·等同",
    "通道·启发·调谐", "和谐·整合·模范", "意图·脉动·实现",
    "显化·完美·产出", "溶解·释放·解放", "合作·奉献·普遍化",
    "持久·超越·存在",
]

COLORS = ["", "红", "白", "蓝", "黄", "红", "白", "蓝", "黄",
          "红", "白", "蓝", "黄", "红", "白", "蓝", "黄",
          "红", "白", "蓝", "黄"]

REFERENCE_DATE = date(2013, 7, 26)
REFERENCE_KIN = 164

ROLE_GUIDANCE = {
    "main": "主印记代表你的核心天赋，是别人最容易感受到的你，也是你这一生最自然的表达方式。",
    "support": "支持位代表你的辅助力量，是你最容易调用、也最能给你安全感的资源。",
    "guide": "引导位代表更高版本的自己，提醒你在重大阶段往哪个方向成长和对齐。",
    "challenge": "挑战位不是缺点，而是你的成长功课。你一开始会不习惯，但整合之后会明显升级。",
    "occult": "隐藏推动代表你潜意识深处的力量，平时不一定显眼，但会在关键时刻推动你转变。",
}

SEAL_GUIDANCE = {
    "红月": "你更容易通过感受、净化、恢复流动来工作。卡住时，先清理情绪与环境，再做决定。",
    "白狗": "你的关系品质、忠诚感和真心投入，是很重要的资源。环境对不对，会直接影响发挥。",
    "蓝风暴": "变化和重组是你的成长入口。真正的功课不是逃开变化，而是学会不被变化吞没。",
    "黄人": "你的深层成长在于长出自由意志、判断力与影响力，不再只是感受，而是开始选择。",
    "黄种子": "你的重点会落在觉察、聚焦和培育真正值得生长的方向上。",
    "蓝鹰": "你的支持力量之一是视野。把自己从局部情绪里拉出来，常常能看清真正的问题。",
    "白巫师": "你容易被沉浸感和理想化吸引，修炼重点是把感受带回现实判断。",
    "红地球": "当你跟对节奏、对齐自身导航时，很多事会比硬推更顺。",
}

TONE_GUIDANCE = {
    "磁性": "这一调性的主题是聚焦。你的人生常常在问：我真正要把力气聚到哪里？",
    "韵律": "这一调性的主题是平衡、组织与结构。你越会整理节奏，越容易稳定发光。",
    "银河": "这一调性的主题是整合。你需要把理想、现实、关系与表达慢慢活成一致。",
    "宇宙": "这一调性的主题是超越与持久。你的成长不是一时爆发，而是长期活出更高版本的自己。",
}

STYLE_CONFIG = {
    "beginner": {
        "label": "小白版",
        "description": "优先用生活化语言解释概念，降低术语密度，先让普通用户看懂再追问。",
    },
    "consulting": {
        "label": "咨询版",
        "description": "优先突出卡点、判断点与下一步行动，适合咨询、陪伴和深度对话。",
    },
    "professional": {
        "label": "专业版",
        "description": "优先保留结构关系、解释层术语和可复用表述，适合专业使用者和内容生产。",
    },
}


def normalize_report_style(style):
    if not style:
        return "beginner"
    normalized = str(style).strip().lower().replace(" ", "_")
    alias_map = {
        "xiaobai": "beginner",
        "beginner": "beginner",
        "simple": "beginner",
        "novice": "beginner",
        "consulting": "consulting",
        "consultation": "consulting",
        "advisor": "consulting",
        "professional": "professional",
        "pro": "professional",
        "expert": "professional",
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
    if normalized == "beginner":
        beginner_prefix = {
            "questions": "可以先问自己：",
            "decision_checks": "先检查：",
            "instructions": "使用时记住：",
            "prompts": "可直接这样问：",
        }
        prefix = beginner_prefix.get(field)
        return f"{prefix}{text}" if prefix else text
    if normalized == "consulting":
        consulting_prefix = {
            "summary": "咨询提示：",
            "focus": "本轮重点：",
            "questions": "追问：",
            "decision_checks": "判断点：",
            "instructions": "咨询用法：",
            "prompts": "对话提示：",
            "action": "行动建议：",
        }
        prefix = consulting_prefix.get(field, "咨询视角：")
        return f"{prefix}{text}"
    professional_prefix = {
        "summary": "结构判断：",
        "focus": "解释层重点：",
        "questions": "分析问题：",
        "decision_checks": "校验点：",
        "angles": "选题入口：",
        "formats": "输出形式：",
        "instructions": "调用说明：",
        "prompts": "提示词模板：",
        "action": "方法建议：",
    }
    prefix = professional_prefix.get(field, "专业表述：")
    return f"{prefix}{text}"


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


def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def count_leap_days_skipped(d1, d2):
    if d1 > d2:
        d1, d2 = d2, d1
        sign = -1
    else:
        sign = 1

    count = 0
    for year in range(d1.year, d2.year + 1):
        if is_leap_year(year):
            leap_day = date(year, 2, 29)
            if d1 < leap_day <= d2:
                count += 1

    return count * sign


def parse_iso_date(value, field_name="日期"):
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"无法解析{field_name} '{value}'，请使用 YYYY-MM-DD 格式") from exc


def date_to_kin(target_date):
    if isinstance(target_date, str):
        target_date = date.fromisoformat(target_date)

    delta_days = (target_date - REFERENCE_DATE).days
    if delta_days >= 0:
        leap_skips = count_leap_days_skipped(REFERENCE_DATE, target_date)
    else:
        leap_skips = -count_leap_days_skipped(target_date, REFERENCE_DATE)

    adjusted_days = delta_days - leap_skips
    return ((REFERENCE_KIN - 1 + adjusted_days) % 260) + 1


def kin_to_seal(kin):
    return ((kin - 1) % 20) + 1


def kin_to_tone(kin):
    return ((kin - 1) % 13) + 1


def seal_color(seal_num):
    return COLORS[seal_num]


def calc_support_seal(main_seal):
    support = 19 - main_seal
    if support <= 0:
        support += 20
    return support


def calc_challenge_seal(main_seal):
    challenge = main_seal + 10
    if challenge > 20:
        challenge -= 20
    return challenge


def calc_occult_seal(main_seal):
    occult = 21 - main_seal
    if occult <= 0:
        occult += 20
    return occult


def calc_guide_seal(main_seal, main_tone):
    if main_tone in (1, 6, 11):
        offset = 0
    elif main_tone in (2, 7, 12):
        offset = 12
    elif main_tone in (3, 8, 13):
        offset = 4
    elif main_tone in (4, 9):
        offset = 16
    elif main_tone in (5, 10):
        offset = 8
    else:
        offset = 0

    return ((main_seal - 1 + offset) % 20) + 1


def calc_occult_tone(main_tone):
    return 14 - main_tone


def calc_five_destiny(kin):
    main_seal = kin_to_seal(kin)
    main_tone = kin_to_tone(kin)
    support_seal = calc_support_seal(main_seal)
    challenge_seal = calc_challenge_seal(main_seal)
    occult_seal = calc_occult_seal(main_seal)
    guide_seal = calc_guide_seal(main_seal, main_tone)
    occult_tone = calc_occult_tone(main_tone)

    return {
        "kin": kin,
        "main": {
            "seal": main_seal,
            "tone": main_tone,
            "seal_name": SEALS[main_seal],
            "seal_en": SEALS_EN[main_seal],
            "tone_name": TONES[main_tone],
            "tone_en": TONES_EN[main_tone],
            "color": seal_color(main_seal),
            "keywords": SEAL_KEYWORDS[main_seal],
            "tone_keywords": TONE_KEYWORDS[main_tone],
        },
        "support": {
            "seal": support_seal,
            "tone": main_tone,
            "seal_name": SEALS[support_seal],
            "seal_en": SEALS_EN[support_seal],
            "tone_name": TONES[main_tone],
            "color": seal_color(support_seal),
            "keywords": SEAL_KEYWORDS[support_seal],
        },
        "guide": {
            "seal": guide_seal,
            "tone": main_tone,
            "seal_name": SEALS[guide_seal],
            "seal_en": SEALS_EN[guide_seal],
            "tone_name": TONES[main_tone],
            "color": seal_color(guide_seal),
            "keywords": SEAL_KEYWORDS[guide_seal],
        },
        "challenge": {
            "seal": challenge_seal,
            "tone": main_tone,
            "seal_name": SEALS[challenge_seal],
            "seal_en": SEALS_EN[challenge_seal],
            "tone_name": TONES[main_tone],
            "color": seal_color(challenge_seal),
            "keywords": SEAL_KEYWORDS[challenge_seal],
        },
        "occult": {
            "seal": occult_seal,
            "tone": occult_tone,
            "seal_name": SEALS[occult_seal],
            "seal_en": SEALS_EN[occult_seal],
            "tone_name": TONES[occult_tone],
            "color": seal_color(occult_seal),
            "keywords": SEAL_KEYWORDS[occult_seal],
            "tone_keywords": TONE_KEYWORDS[occult_tone],
        },
    }


def calc_wavespell(kin):
    wavespell_index = (kin - 1) // 13
    wavespell_start_kin = wavespell_index * 13 + 1
    wavespell_seal = kin_to_seal(wavespell_start_kin)
    position = ((kin - 1) % 13) + 1
    return {
        "wavespell_number": wavespell_index + 1,
        "wavespell_seal": wavespell_seal,
        "wavespell_name": SEALS[wavespell_seal],
        "wavespell_en": SEALS_EN[wavespell_seal],
        "position": position,
        "start_kin": wavespell_start_kin,
    }


def calc_yearly_kin(birth_date, year):
    if isinstance(birth_date, str):
        birth_date = date.fromisoformat(birth_date)

    month, day = birth_date.month, birth_date.day
    if month == 2 and day == 29 and not is_leap_year(year):
        month, day = 2, 28

    return date_to_kin(date(year, month, day))


def calc_yearly_report(birth_date, year):
    return calc_five_destiny(calc_yearly_kin(birth_date, year))


def calc_relationship(kin_a, kin_b):
    seal_a = kin_to_seal(kin_a)
    seal_b = kin_to_seal(kin_b)
    tone_a = kin_to_tone(kin_a)
    tone_b = kin_to_tone(kin_b)

    a_support = calc_support_seal(seal_a)
    a_challenge = calc_challenge_seal(seal_a)
    a_occult = calc_occult_seal(seal_a)
    a_guide = calc_guide_seal(seal_a, tone_a)

    b_support = calc_support_seal(seal_b)
    b_challenge = calc_challenge_seal(seal_b)
    b_occult = calc_occult_seal(seal_b)
    b_guide = calc_guide_seal(seal_b, tone_b)

    b_in_a = []
    if seal_b == seal_a:
        b_in_a.append("主印记（相同图腾）")
    if seal_b == a_support:
        b_in_a.append("支持位")
    if seal_b == a_challenge:
        b_in_a.append("挑战位")
    if seal_b == a_occult:
        b_in_a.append("隐藏推动位")
    if seal_b == a_guide:
        b_in_a.append("引导位")

    a_in_b = []
    if seal_a == seal_b:
        a_in_b.append("主印记（相同图腾）")
    if seal_a == b_support:
        a_in_b.append("支持位")
    if seal_a == b_challenge:
        a_in_b.append("挑战位")
    if seal_a == b_occult:
        a_in_b.append("隐藏推动位")
    if seal_a == b_guide:
        a_in_b.append("引导位")

    combined_kin = ((kin_a + kin_b - 1) % 260) + 1
    color_a = seal_color(seal_a)
    color_b = seal_color(seal_b)

    if color_a == color_b:
        color_relation = "同色族群（深度共鸣，理解彼此的核心能量）"
    elif (color_a in ("红", "白") and color_b in ("红", "白")):
        color_relation = "红白互补（启动与净化的互补，天然支持关系）"
    elif (color_a in ("蓝", "黄") and color_b in ("蓝", "黄")):
        color_relation = "蓝黄互补（转化与成熟的互补，天然支持关系）"
    elif (color_a in ("红", "蓝") and color_b in ("红", "蓝")):
        color_relation = "红蓝对冲（启动与转化的张力，互为挑战与成长）"
    elif (color_a in ("白", "黄") and color_b in ("白", "黄")):
        color_relation = "白黄对冲（净化与成熟的张力，互为挑战与成长）"
    else:
        color_relation = "其他颜色关系"

    tone_sum = tone_a + tone_b
    if tone_sum == 14:
        tone_relation = "调性互补（如同隐藏推动关系，深层灵魂连接）"
    elif tone_a == tone_b:
        tone_relation = "调性相同（共振频率一致，容易同步）"
    elif abs(tone_a - tone_b) == 1:
        tone_relation = "调性相邻（自然流动的递进关系）"
    else:
        tone_relation = f"调性差值 {abs(tone_a - tone_b)}（需要主动调频共振）"

    return {
        "person_a": calc_five_destiny(kin_a),
        "person_b": calc_five_destiny(kin_b),
        "b_in_a_positions": b_in_a if b_in_a else ["无直接天赋位连接"],
        "a_in_b_positions": a_in_b if a_in_b else ["无直接天赋位连接"],
        "combined_kin": combined_kin,
        "combined_destiny": calc_five_destiny(combined_kin),
        "color_relation": color_relation,
        "tone_relation": tone_relation,
    }


def format_destiny(destiny, label=""):
    main = destiny["main"]
    support = destiny["support"]
    guide = destiny["guide"]
    challenge = destiny["challenge"]
    occult = destiny["occult"]

    title = f"{'=' * 50}\n"
    if label:
        title += f"  {label}\n{'=' * 50}\n"
    else:
        title += f"  星系印记解读\n{'=' * 50}\n"

    output = title
    output += f"\n✦ Kin {destiny['kin']}: {main['tone_name']}{main['tone']} · {main['seal_name']}\n"
    output += f"  {main['tone_en']} {main['tone']} · {main['seal_en']}\n"
    output += f"  颜色: {main['color']}色 | 图腾关键词: {main['keywords']}\n"
    output += f"  调性关键词: {main['tone_keywords']}\n"
    output += f"\n{'─' * 50}\n  五大天赋盘\n{'─' * 50}\n"
    output += f"\n              【引导】\n"
    output += f"           {guide['tone_name']}{main['tone']} · {guide['seal_name']}\n"
    output += f"           ({guide['seal_en']})\n"
    output += f"           关键词: {guide['keywords']}\n"
    output += "\n  【支持】  ←  【主印记】  →  【挑战】\n"
    output += (
        f"  {support['tone_name']}{main['tone']}·{support['seal_name']}   "
        f"{main['tone_name']}{main['tone']}·{main['seal_name']}   "
        f"{challenge['tone_name']}{main['tone']}·{challenge['seal_name']}\n"
    )
    output += f"\n              【隐藏推动】\n"
    output += f"           {occult['tone_name']}{occult['tone']} · {occult['seal_name']}\n"
    output += f"           ({occult['seal_en']})\n"
    output += f"           关键词: {occult['keywords']}\n"

    wavespell = calc_wavespell(destiny["kin"])
    output += f"\n{'─' * 50}\n  波符信息\n{'─' * 50}\n"
    output += f"  所属波符: 第{wavespell['wavespell_number']}波符 · {wavespell['wavespell_name']}波符\n"
    output += f"  波符内位置: 第{wavespell['position']}天 (调性{wavespell['position']}: {TONES[wavespell['position']]})\n"
    return output


def serialize_destiny(destiny):
    payload = dict(destiny)
    payload["wavespell"] = calc_wavespell(destiny["kin"])
    return payload


def summarize_destiny(destiny):
    main = destiny["main"]
    support = destiny["support"]
    challenge = destiny["challenge"]
    occult = destiny["occult"]
    guide = destiny["guide"]

    summary = {
        "core_theme": f"{main['tone_name']}{main['seal_name']}的主轴是{main['keywords']}，人生会不断回到“我真正要如何使用自己的天赋”这个问题。",
        "strength": f"你的天然资源更接近{support['seal_name']}：{support['keywords']}。环境、关系与支持系统是否合适，会直接影响发挥。",
        "challenge": f"你的成长功课在{challenge['seal_name']}：{challenge['keywords']}。这不是缺点，而是你需要整合的力量。",
        "hidden_driver": f"更深层推动力来自{occult['seal_name']}：{occult['keywords']}。这常常决定你后续真正会长成什么样的人。",
        "guidance": f"引导位落在{guide['seal_name']}，说明你最终要活出的不是别人的版本，而是更成熟的自己。",
    }
    return summary


def build_growth_path(destiny):
    support = destiny["support"]
    main = destiny["main"]
    challenge = destiny["challenge"]
    occult = destiny["occult"]
    guide = destiny["guide"]

    return [
        {
            "stage": "隐藏推动",
            "sign": f"{occult['tone_name']}{occult['seal_name']}",
            "focus": f"先认识你潜意识深处的力量：{occult['keywords']}。",
            "action": "先问自己真正想要什么，不要总是让环境先替你做决定。",
        },
        {
            "stage": "支持位",
            "sign": f"{support['tone_name']}{support['seal_name']}",
            "focus": f"建立能支持你的资源系统：{support['keywords']}。",
            "action": "筛选关系、环境与合作，把真心给对地方。",
        },
        {
            "stage": "主印记",
            "sign": f"{main['tone_name']}{main['seal_name']}",
            "focus": f"扎根你的核心天赋：{main['keywords']}。",
            "action": "让自己的生活和表达重新回到真实、流动和一致。",
        },
        {
            "stage": "挑战位",
            "sign": f"{challenge['tone_name']}{challenge['seal_name']}",
            "focus": f"整合你的成长功课：{challenge['keywords']}。",
            "action": "变化来了不要先自我否定，而是判断这次升级在教你什么。",
        },
        {
            "stage": "引导位",
            "sign": f"{guide['tone_name']}{guide['seal_name']}",
            "focus": "活出更成熟、更有力量的自己。",
            "action": "不是变成别人，而是让自己的天赋越来越清楚、稳定、可持续。",
        },
    ]


def build_action_guide(destiny):
    main = destiny["main"]
    support = destiny["support"]
    challenge = destiny["challenge"]
    occult = destiny["occult"]
    return {
        "career": [
            f"优先考虑能发挥{main['keywords']}的工作，而不是长期要求你压住天赋的环境。",
            f"把{support['seal_name']}对应的资源系统建起来：关系、合作和支持氛围会直接影响你的表现。",
            f"遇到{challenge['seal_name']}式压力时，先分辨它是在训练你升级，还是在单纯消耗你。",
        ],
        "relationship": [
            "不要只因为有感觉就长期留下来，也要看这段关系是否真的滋养你。",
            f"当你开始反复感受到{challenge['seal_name']}式张力时，记得补边界，而不是只补耐心。",
            f"更深层的成熟，来自把{occult['seal_name']}对应的判断力、选择权和方向感长出来。",
        ],
        "growth": [
            f"先承认自己的核心频率是{main['seal_name']}，不要总逼自己活成别人的节奏。",
            "每次卡住时，先问这是信息堵、情绪堵、边界堵、责任堵还是节奏堵。",
            "把感受推进成选择，把觉察推进成行动，而不是长期停留在“我知道不对”。",
        ],
    }


def build_personal_delivery_layers(destiny, style="beginner"):
    main = destiny["main"]
    support = destiny["support"]
    challenge = destiny["challenge"]
    occult = destiny["occult"]
    guide = destiny["guide"]
    layers = {
        "consultation": {
            "focus": "围绕天赋、卡点和边界来提问，先看清哪里堵，再决定怎么动。",
            "questions": [
                f"我现在最反复卡住的地方，和{challenge['seal_name']}的成长功课有什么关系？",
                f"我看到的堵点，是信息、情绪、边界、责任还是节奏的问题？",
                f"这段关系或这个环境，真的值得我继续用{occult['seal_name']}式能量去推动吗？",
            ],
            "decision_checks": [
                f"我有没有先调用{support['seal_name']}对应的支持资源，而不是一上来就硬扛？",
                f"我是不是已经看见{guide['seal_name']}式的成长方向，但还没真正站过去？",
                "如果我要保护自己的流动感，现在最小的动作应该是什么？",
            ],
        },
        "content": {
            "focus": "适合做成个人说明书、成长路线图、卡点清单和边界练习稿。",
            "angles": [
                f"《为什么我会卡住，以及怎么把{main['seal_name']}的天赋用起来》",
                f"《我的{support['seal_name']}资源怎么影响我的发挥》",
                f"《我和{challenge['seal_name']}的关系：变化来了，我怎么不被卷走》",
                f"《如何把{occult['seal_name']}的深层推动，变成更成熟的选择》",
            ],
            "formats": [
                "咨询记录",
                "公众号长文",
                "短视频脚本",
                "个人复盘模板",
            ],
        },
        "ai": {
            "focus": "给 AI 的问题要先交代场景、卡点和目标，然后要求它先结论、再解释、再行动。",
            "instructions": [
                "先判断这是个人天赋、关系消耗还是环境不适配。",
                f"输出时优先围绕{main['seal_name']}的主轴、{challenge['seal_name']}的功课和{guide['seal_name']}的成长方向。",
                "如果信息不足，先提出 1 到 3 个关键追问，不要直接泛泛而谈。",
            ],
            "prompts": [
                "请先判断我现在的卡点属于哪一类，再给我可执行的下一步。",
                "请把这张盘翻译成适合普通用户理解的行动建议。",
                "请用咨询顾问的方式，先指出问题，再给出边界和选择。",
            ],
        },
    }
    return stylize_delivery_layers(layers, style)


def build_yearly_delivery_layers(natal_destiny, annual_destiny, interaction, style="beginner"):
    natal = natal_destiny["main"]
    annual = annual_destiny["main"]
    support = annual_destiny["support"]
    challenge = annual_destiny["challenge"]
    guide = annual_destiny["guide"]
    layers = {
        "consultation": {
            "focus": "围绕年度主轴、年度与本命的关系，以及这一年该怎么种种子来提问。",
            "questions": [
                f"今年最值得持续投入的一个方向是什么？",
                f"年度主轴{annual['seal_name']}和本命{natal['seal_name']}的关系，说明我该加法还是减法？",
                f"这一年的压力，是节奏问题、关系问题，还是方向问题？",
            ],
            "decision_checks": [
                f"这一年我是不是更适合先用{support['seal_name']}的方式稳住系统，而不是急着扩张？",
                f"{interaction['color_relation']}和{interaction['tone_relation']}在提醒我什么样的调整顺序？",
                f"我现在是不是已经感受到{challenge['seal_name']}的课题，但还没把它翻译成行动？",
            ],
        },
        "content": {
            "focus": "适合做成年度说明书、年度复盘、季度规划和年度主题内容。",
            "angles": [
                f"《{annual['seal_name']}年：今年最该种下的种子是什么》",
                f"《流年怎么和本命互动：今年我该怎么调节节奏》",
                f"《年度复盘模板：这一年我到底在练什么》",
                f"《把{guide['seal_name']}式成长方向翻译成年度行动》",
            ],
            "formats": [
                "年度咨询报告",
                "年度复盘长文",
                "季度行动清单",
                "内容栏目选题",
            ],
        },
        "ai": {
            "focus": "给 AI 的问题要先告诉它出生日期、目标年份和当前最关心的现实问题。",
            "instructions": [
                "先输出年度主轴，再输出与本命的互动关系，最后给出行动建议。",
                "要区分年度气候和个人惯性，避免把流年压力误判为个人能力不足。",
                "优先给出今年适合做、应该少做、不能拖的三类建议。",
            ],
            "prompts": [
                "请把这份流年翻译成年度主题、风险和行动建议。",
                "请按咨询师口吻给我一个今年的节奏建议。",
                "请告诉我今年最值得种的种子和最需要避免的消耗。",
            ],
        },
    }
    return stylize_delivery_layers(layers, style)


def build_compatibility_delivery_layers(result, style="beginner"):
    person_a = result["person_a"]["main"]
    person_b = result["person_b"]["main"]
    combined = result["combined_destiny"]["main"]
    layers = {
        "consultation": {
            "focus": "围绕合作类型、冲突来源、分工边界和长期可持续性来提问。",
            "questions": [
                "这段关系是合作型、成长型，还是消耗型？",
                "你们的卡点主要来自节奏、边界还是价值观？",
                "如果要继续合作，最需要先对齐的是什么？",
            ],
            "decision_checks": [
                f"A 与 B 的颜色关系是{result['color_relation']}，这提示你们是互补、同频还是互相拉扯？",
                f"调性关系是{result['tone_relation']}，说明彼此需要怎样的沟通节奏？",
                f"合盘 {combined['seal_name']} 的主题，是否真的支持这段关系长期发展？",
            ],
        },
        "content": {
            "focus": "适合做成合盘分析、关系说明书、合作建议和冲突化解内容。",
            "angles": [
                f"《A: {person_a['seal_name']}，B: {person_b['seal_name']}，你们怎么合作更顺》",
                "《这段关系里的优势、张力和边界怎么写成说明书》",
                "《合盘不只看感觉，还要看怎么分工、怎么沟通》",
                f"《{combined['seal_name']}合盘：这段关系最适合往哪里长》",
            ],
            "formats": [
                "合盘咨询报告",
                "关系复盘稿",
                "短视频解读",
                "AI 对话模板",
            ],
        },
        "ai": {
            "focus": "给 AI 的问题要先交代双方关系、现实场景和你想得到的结果。",
            "instructions": [
                "先判断关系类型，再给出合作建议、沟通建议和风险提示。",
                "如果是长期合作，要优先看分工、边界和节奏，不要只看感觉。",
                "尽量把结论翻译成可执行的沟通句式和协作建议。",
            ],
            "prompts": [
                "请把这段关系翻译成合作优势、冲突点和相处建议。",
                "请按咨询师视角告诉我这段关系值不值得继续投入。",
                "请给我一个适合双方的沟通和分工模板。",
            ],
        },
    }
    return stylize_delivery_layers(layers, style)


def format_delivery_layers(lines, layers):
    section_titles = {
        "consultation": "咨询视角",
        "content": "内容产品视角",
        "ai": "AI 对话视角",
    }
    for key in ("consultation", "content", "ai"):
        section = layers[key]
        lines.append(f"\n{'─' * 50}")
        lines.append(f"  {section_titles[key]}")
        lines.append(f"{'─' * 50}")
        lines.append(f"- 重点: {section['focus']}")
        for field in ("questions", "decision_checks", "angles", "formats", "instructions", "prompts"):
            if field in section:
                label = {
                    "questions": "提问",
                    "decision_checks": "判断",
                    "angles": "选题角度",
                    "formats": "推荐形式",
                    "instructions": "使用说明",
                    "prompts": "可直接复制的提示词",
                }[field]
                lines.append(f"- {label}")
                for item in section[field]:
                    lines.append(f"  {item}")


def build_yearly_report(birth_date, year, style="beginner"):
    normalized_style = normalize_report_style(style)
    style_info = style_meta(normalized_style)
    natal_kin = date_to_kin(birth_date)
    natal_destiny = calc_five_destiny(natal_kin)
    annual_kin = calc_yearly_kin(birth_date, year)
    annual_destiny = calc_five_destiny(annual_kin)
    interaction = calc_relationship(natal_kin, annual_kin)
    positions = {
        role: {
            "name": f"{annual_destiny[role]['tone_name']}{annual_destiny[role]['seal_name']}",
            "keywords": annual_destiny[role]["keywords"],
            "explanation": explain_position(role, annual_destiny[role]),
        }
        for role in ("main", "support", "guide", "challenge", "occult")
    }
    summary = stylize_summary({
        "core_theme": f"{year} 年的主轴是 {annual_destiny['main']['tone_name']}{annual_destiny['main']['seal_name']}：{annual_destiny['main']['keywords']}。",
        "resource": f"这一年的资源来自 {annual_destiny['support']['seal_name']}：{annual_destiny['support']['keywords']}；本命 {natal_destiny['support']['seal_name']} 也会影响你能不能稳住节奏。",
        "challenge": f"年度课题落在 {annual_destiny['challenge']['seal_name']}：{annual_destiny['challenge']['keywords']}，与本命互动呈现 {interaction['color_relation']} / {interaction['tone_relation']}。",
        "guidance": f"这不是一味冲刺的一年，而是先种对种子、再让结构长稳的一年。",
    }, normalized_style)
    action_guide = stylize_action_guide({
        "focus": [
            f"优先把 {annual_destiny['main']['seal_name']} 对应的主题落地，而不是继续分散能量。",
            f"把 {interaction['color_relation']} 当成年度风格参考，决定你是更适合外扩还是内收整理。",
            f"遇到 {interaction['tone_relation']} 带来的摩擦时，先调节节奏，再调结果。",
        ],
        "watchouts": [
            "不要把年度压力直接解释成自己不行。",
            "不要等状态完美才开始行动。",
            "不要一遇到卡顿就想彻底推翻现有结构。",
        ],
        "practice": [
            "每个季度回看一次：我现在是在播种、培育，还是收割。",
            "把每次犹豫翻译成一个最小可执行动作。",
            "让年度目标和本命天赋对齐，而不是彼此拉扯。",
        ],
    }, normalized_style)
    report = {
        "scene": "yearly",
        "scene_label": f"{year} 年流年说明书",
        "style": normalized_style,
        "style_label": style_info["label"],
        "style_description": style_info["description"],
        "birth_date": str(birth_date) if birth_date else None,
        "year": year,
        "kin": annual_kin,
        "natal_kin": natal_kin,
        "title": f"Kin {annual_kin} {annual_destiny['main']['tone_name']}{annual_destiny['main']['seal_name']}",
        "natal": natal_destiny,
        "annual": annual_destiny,
        "interaction": interaction,
        "summary": summary,
        "positions": positions,
        "growth_path": stylize_growth_path(build_growth_path(annual_destiny), normalized_style),
        "action_guide": action_guide,
        "delivery_layers": build_yearly_delivery_layers(natal_destiny, annual_destiny, interaction, normalized_style),
    }
    return report


def format_yearly_report(report):
    natal = report["natal"]
    interaction = report["interaction"]
    positions = report["positions"]
    lines = []
    lines.append("=" * 50)
    lines.append(f"  {report['scene_label']}")
    lines.append("=" * 50)
    if report["birth_date"]:
        lines.append(f"\n  出生日期: {report['birth_date']}")
    lines.append(f"  年度主轴: {report['title']}")
    lines.append(f"  输出风格: {report.get('style_label', '小白版')}")
    lines.append(f"  本命参考: Kin {report['natal_kin']} {natal['main']['tone_name']}{natal['main']['seal_name']}")
    lines.append(f"  年度与本命关系: {interaction['color_relation']} | {interaction['tone_relation']}")
    lines.append(f"  风格说明: {report.get('style_description', STYLE_CONFIG['beginner']['description'])}")

    lines.append(f"\n{'─' * 50}")
    lines.append("  年度摘要")
    lines.append(f"{'─' * 50}")
    lines.append(f"- 主轴: {report['summary']['core_theme']}")
    lines.append(f"- 资源: {report['summary']['resource']}")
    lines.append(f"- 课题: {report['summary']['challenge']}")
    lines.append(f"- 指引: {report['summary']['guidance']}")

    lines.append(f"\n{'─' * 50}")
    lines.append("  年度五大位置")
    lines.append(f"{'─' * 50}")
    for role, label in (("main", "主印记"), ("support", "支持位"), ("guide", "引导位"), ("challenge", "挑战位"), ("occult", "隐藏推动")):
        pos = positions[role]
        lines.append(f"- {label}: {pos['name']} | {pos['keywords']}")
        lines.append(f"  {pos['explanation']}")

    lines.append(f"\n{'─' * 50}")
    lines.append("  年度建议")
    lines.append(f"{'─' * 50}")
    lines.append("- 聚焦")
    for item in report["action_guide"]["focus"]:
        lines.append(f"  {item}")
    lines.append("- 需要避免")
    for item in report["action_guide"]["watchouts"]:
        lines.append(f"  {item}")
    lines.append("- 练习")
    for item in report["action_guide"]["practice"]:
        lines.append(f"  {item}")

    format_delivery_layers(lines, report["delivery_layers"])
    return "\n".join(lines) + "\n"


def _build_compatibility_report_from_result(result, style="beginner"):
    normalized_style = normalize_report_style(style)
    style_info = style_meta(normalized_style)
    person_a = result["person_a"]
    person_b = result["person_b"]
    combined = result["combined_destiny"]
    summary = stylize_summary({
        "core_theme": f"这段关系的合盘主轴是 Kin {result['combined_kin']} {combined['main']['tone_name']}{combined['main']['seal_name']}：{combined['main']['keywords']}。",
        "strength": f"你们的优势来自 {result['color_relation']}，而 {result['tone_relation']} 决定了协作时的同步方式。",
        "challenge": f"A 与 B 的天赋位互照，说明你们既容易互相看见，也容易互相放大卡点。",
        "guidance": f"要让关系顺起来，关键不是谁更对，而是先对齐目标、边界和节奏。",
    }, normalized_style)
    action_guide = stylize_action_guide({
        "cooperation": [
            f"先把 {combined['support']['seal_name']} 式支持系统建立起来，把分工和责任说清楚。",
            "如果一方总在推进、另一方总在承接，要尽早重画协作方式。",
            "关系能不能长期合作，先看执行方式，再看感觉是否顺。",
        ],
        "communication": [
            f"当 {result['tone_relation']} 提示存在节奏差异时，优先调整沟通频率。",
            "把‘我感觉不对’翻译成‘我希望怎么改’。",
            "不要让沉默替代真正的对话。",
        ],
        "growth": [
            f"把 {combined['challenge']['seal_name']} 的课题当作共同成长点，而不是彼此指责点。",
            "每次冲突都回到：我们是在共同解决问题，还是在互相消耗。",
            "这段关系最好的版本，是双方都更清楚自己，也更能尊重对方。",
        ],
    }, normalized_style)
    return {
        "scene": "compatibility",
        "scene_label": "双人合盘说明书",
        "style": normalized_style,
        "style_label": style_info["label"],
        "style_description": style_info["description"],
        "kin_a": result["person_a"]["kin"],
        "kin_b": result["person_b"]["kin"],
        "title": f"Kin {result['combined_kin']} {combined['main']['tone_name']}{combined['main']['seal_name']}",
        "person_a": person_a,
        "person_b": person_b,
        "combined_kin": result["combined_kin"],
        "combined_destiny": combined,
        "interaction": result,
        "summary": summary,
        "growth_path": stylize_growth_path(build_growth_path(combined), normalized_style),
        "action_guide": action_guide,
        "delivery_layers": build_compatibility_delivery_layers(result, normalized_style),
    }


def build_compatibility_report(kin_a, kin_b, style="beginner"):
    return _build_compatibility_report_from_result(calc_relationship(kin_a, kin_b), style=style)


def format_compatibility_report(report):
    person_a = report["person_a"]["main"]
    person_b = report["person_b"]["main"]
    combined = report["combined_destiny"]["main"]
    interaction = report["interaction"]
    lines = []
    lines.append("=" * 50)
    lines.append(f"  {report['scene_label']}")
    lines.append("=" * 50)
    lines.append(f"\n  输出风格: {report.get('style_label', '小白版')}")
    lines.append(f"  风格说明: {report.get('style_description', STYLE_CONFIG['beginner']['description'])}")
    lines.append(f"\n  A: Kin {report['kin_a']} {person_a['tone_name']}{person_a['tone']}·{person_a['seal_name']}")
    lines.append(f"  B: Kin {report['kin_b']} {person_b['tone_name']}{person_b['tone']}·{person_b['seal_name']}")
    lines.append(f"  合盘: {report['title']}")
    lines.append(f"  颜色关系: {interaction['color_relation']}")
    lines.append(f"  调性关系: {interaction['tone_relation']}")
    lines.append(f"  互相照见: B在A中的位置 {', '.join(interaction['b_in_a_positions'])}")
    lines.append(f"  互相照见: A在B中的位置 {', '.join(interaction['a_in_b_positions'])}")

    lines.append(f"\n{'─' * 50}")
    lines.append("  关系摘要")
    lines.append(f"{'─' * 50}")
    lines.append(f"- 主轴: {report['summary']['core_theme']}")
    lines.append(f"- 优势: {report['summary']['strength']}")
    lines.append(f"- 课题: {report['summary']['challenge']}")
    lines.append(f"- 指引: {report['summary']['guidance']}")

    lines.append(f"\n{'─' * 50}")
    lines.append("  合盘与成长")
    lines.append(f"{'─' * 50}")
    lines.append(f"- 合盘Kin: Kin {report['combined_kin']} {combined['tone_name']}{combined['tone']}·{combined['seal_name']}")
    lines.append(f"- 合盘关键词: {combined['keywords']}")
    for item in report["growth_path"]:
        lines.append(f"- {item['stage']} · {item['sign']}: {item['focus']}")
        lines.append(f"  练习: {item['action']}")

    lines.append(f"\n{'─' * 50}")
    lines.append("  关系建议")
    lines.append(f"{'─' * 50}")
    lines.append("- 协作")
    for item in report["action_guide"]["cooperation"]:
        lines.append(f"  {item}")
    lines.append("- 沟通")
    for item in report["action_guide"]["communication"]:
        lines.append(f"  {item}")
    lines.append("- 成长")
    for item in report["action_guide"]["growth"]:
        lines.append(f"  {item}")

    format_delivery_layers(lines, report["delivery_layers"])
    return "\n".join(lines) + "\n"


def explain_position(role, detail):
    parts = [ROLE_GUIDANCE[role]]
    seal_hint = SEAL_GUIDANCE.get(detail["seal_name"])
    if seal_hint:
        parts.append(seal_hint)
    tone_hint = TONE_GUIDANCE.get(detail["tone_name"])
    if tone_hint:
        parts.append(tone_hint)
    return " ".join(parts)


def build_personal_report(destiny, birth_date=None, style="beginner"):
    normalized_style = normalize_report_style(style)
    style_info = style_meta(normalized_style)
    summary = stylize_summary(summarize_destiny(destiny), normalized_style)
    path = stylize_growth_path(build_growth_path(destiny), normalized_style)
    actions = stylize_action_guide(build_action_guide(destiny), normalized_style)
    positions = {
        role: {
            "name": f"{destiny[role]['tone_name']}{destiny[role]['seal_name']}",
            "keywords": destiny[role]["keywords"],
            "explanation": explain_position(role, destiny[role]),
        }
        for role in ("main", "support", "guide", "challenge", "occult")
    }
    report = {
        "birth_date": str(birth_date) if birth_date else None,
        "kin": destiny["kin"],
        "scene": "personal",
        "scene_label": "玛雅天赋个人说明书",
        "style": normalized_style,
        "style_label": style_info["label"],
        "style_description": style_info["description"],
        "title": f"Kin {destiny['kin']} {destiny['main']['tone_name']}{destiny['main']['seal_name']}",
        "summary": summary,
        "positions": positions,
        "growth_path": path,
        "action_guide": actions,
        "delivery_layers": build_personal_delivery_layers(destiny, normalized_style),
    }
    return report


def format_personal_report(report):
    lines = []
    lines.append("=" * 50)
    lines.append(f"  {report.get('scene_label', '玛雅天赋个人说明书')}")
    lines.append("=" * 50)
    if report["birth_date"]:
        lines.append(f"\n  出生日期: {report['birth_date']}")
    lines.append(f"  核心印记: {report['title']}")
    lines.append(f"  输出风格: {report.get('style_label', '小白版')}")
    lines.append(f"  风格说明: {report.get('style_description', STYLE_CONFIG['beginner']['description'])}")

    lines.append(f"\n{'─' * 50}")
    lines.append("  核心摘要")
    lines.append(f"{'─' * 50}")
    lines.append(f"- 主轴: {report['summary']['core_theme']}")
    lines.append(f"- 资源: {report['summary']['strength']}")
    lines.append(f"- 功课: {report['summary']['challenge']}")
    lines.append(f"- 深层推动: {report['summary']['hidden_driver']}")
    lines.append(f"- 引导方向: {report['summary']['guidance']}")

    lines.append(f"\n{'─' * 50}")
    lines.append("  五大位置解释")
    lines.append(f"{'─' * 50}")
    role_labels = {
        "main": "主印记",
        "support": "支持位",
        "guide": "引导位",
        "challenge": "挑战位",
        "occult": "隐藏推动",
    }
    for role in ("main", "support", "guide", "challenge", "occult"):
        pos = report["positions"][role]
        lines.append(f"- {role_labels[role]}: {pos['name']} | {pos['keywords']}")
        lines.append(f"  {pos['explanation']}")

    lines.append(f"\n{'─' * 50}")
    lines.append("  成长路径")
    lines.append(f"{'─' * 50}")
    for item in report["growth_path"]:
        lines.append(f"- {item['stage']} · {item['sign']}: {item['focus']}")
        lines.append(f"  练习: {item['action']}")

    lines.append(f"\n{'─' * 50}")
    lines.append("  行动建议")
    lines.append(f"{'─' * 50}")
    lines.append("- 事业")
    for item in report["action_guide"]["career"]:
        lines.append(f"  {item}")
    lines.append("- 关系")
    for item in report["action_guide"]["relationship"]:
        lines.append(f"  {item}")
    lines.append("- 成长")
    for item in report["action_guide"]["growth"]:
        lines.append(f"  {item}")
    format_delivery_layers(lines, report["delivery_layers"])
    return "\n".join(lines) + "\n"


def format_compatibility(result):
    if "scene" in result and result.get("scene") == "compatibility":
        return format_compatibility_report(result)
    return format_compatibility_report(_build_compatibility_report_from_result(result))
