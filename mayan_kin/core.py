#!/usr/bin/env python3
"""Core Mayan Kin calculation logic."""

from datetime import date


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


def format_compatibility(result):
    person_a = result["person_a"]["main"]
    person_b = result["person_b"]["main"]
    combined_main = result["combined_destiny"]["main"]

    output = f"\n{'=' * 50}\n  双人合盘分析\n{'=' * 50}\n\n"
    output += f"  A: Kin {result['person_a']['kin']} {person_a['tone_name']}{person_a['tone']}·{person_a['seal_name']}\n"
    output += f"  B: Kin {result['person_b']['kin']} {person_b['tone_name']}{person_b['tone']}·{person_b['seal_name']}\n\n"
    output += f"  颜色关系: {result['color_relation']}\n"
    output += f"  调性关系: {result['tone_relation']}\n\n"
    output += f"  B在A天赋盘中的位置: {', '.join(result['b_in_a_positions'])}\n"
    output += f"  A在B天赋盘中的位置: {', '.join(result['a_in_b_positions'])}\n\n"
    output += f"  合盘Kin: Kin {result['combined_kin']} {combined_main['tone_name']}{combined_main['tone']}·{combined_main['seal_name']}\n"
    output += f"  合盘关键词: {combined_main['keywords']}\n"
    return output


def serialize_destiny(destiny):
    payload = dict(destiny)
    payload["wavespell"] = calc_wavespell(destiny["kin"])
    return payload
