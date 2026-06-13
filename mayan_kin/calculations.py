"""Calendar and Kin calculations (extracted from core.py)."""

from datetime import date

from .constants import *  # noqa: F401,F403


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


