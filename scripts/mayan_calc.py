#!/usr/bin/env python3
"""
玛雅天赋计算工具 (Mayan Destiny Calculator)
基于 Dreamspell / 卓尔金历 体系

用法:
    python3 mayan_calc.py 1990-03-15
    python3 mayan_calc.py 1990-03-15 --compatibility 1992-07-20
    python3 mayan_calc.py 1990-03-15 --yearly 2026
"""

import sys
import argparse
from datetime import date, timedelta

# ============================================================
# 基础数据
# ============================================================

SEALS = [
    "",  # 占位，让编号从1开始
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
    "",  # 占位
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

# 参考日期: 2013年7月26日 = Kin 164
REFERENCE_DATE = date(2013, 7, 26)
REFERENCE_KIN = 164


# ============================================================
# 核心计算函数
# ============================================================

def is_leap_year(year):
    """判断是否为闰年"""
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def count_leap_days_skipped(d1, d2):
    """
    计算两个日期之间的2月29日数量（Dreamspell体系跳过闰日）
    d1 < d2
    """
    if d1 > d2:
        d1, d2 = d2, d1
        sign = -1
    else:
        sign = 1

    count = 0
    start_year = d1.year
    end_year = d2.year

    for y in range(start_year, end_year + 1):
        if is_leap_year(y):
            leap_day = date(y, 2, 29)
            if d1 < leap_day <= d2:
                count += 1

    return count * sign


def date_to_kin(target_date):
    """
    将阳历日期转换为Dreamspell Kin号 (1-260)
    """
    if isinstance(target_date, str):
        target_date = date.fromisoformat(target_date)

    # 计算天数差
    delta_days = (target_date - REFERENCE_DATE).days

    # 计算需要跳过的闰日数
    if delta_days >= 0:
        leap_skips = count_leap_days_skipped(REFERENCE_DATE, target_date)
    else:
        leap_skips = -count_leap_days_skipped(target_date, REFERENCE_DATE)

    # 计算Kin
    adjusted_days = delta_days - leap_skips
    kin = ((REFERENCE_KIN - 1 + adjusted_days) % 260) + 1

    return kin


def kin_to_seal(kin):
    """从Kin号获取图腾编号 (1-20)"""
    return ((kin - 1) % 20) + 1


def kin_to_tone(kin):
    """从Kin号获取调性编号 (1-13)"""
    return ((kin - 1) % 13) + 1


def seal_color(seal_num):
    """获取图腾颜色"""
    return COLORS[seal_num]


# ============================================================
# 五大天赋盘计算
# ============================================================

def calc_support_seal(main_seal):
    """计算支持图腾: 主 + 支持 = 19 (mod 20)"""
    s = 19 - main_seal
    if s <= 0:
        s += 20
    return s


def calc_challenge_seal(main_seal):
    """计算挑战图腾: 主 + 10 (mod 20)"""
    s = main_seal + 10
    if s > 20:
        s -= 20
    return s


def calc_occult_seal(main_seal):
    """计算隐藏推动图腾: 主 + 隐藏 = 21 (mod 20)"""
    s = 21 - main_seal
    if s <= 0:
        s += 20
    return s


def calc_guide_seal(main_seal, main_tone):
    """
    计算引导图腾: 与主印记同色，具体由调性决定
    """
    # 引导位移表（按调性分组）
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

    s = ((main_seal - 1 + offset) % 20) + 1
    return s


def calc_occult_tone(main_tone):
    """计算隐藏推动调性: 14 - 主调性"""
    return 14 - main_tone


def calc_five_destiny(kin):
    """计算完整五大天赋盘"""
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


# ============================================================
# 波符计算
# ============================================================

def calc_wavespell(kin):
    """计算所属波符（每13个Kin为一个波符）"""
    ws_index = ((kin - 1) // 13)  # 0-19
    ws_start_kin = ws_index * 13 + 1
    ws_seal = kin_to_seal(ws_start_kin)
    position_in_ws = ((kin - 1) % 13) + 1  # 1-13

    return {
        "wavespell_number": ws_index + 1,
        "wavespell_seal": ws_seal,
        "wavespell_name": SEALS[ws_seal],
        "wavespell_en": SEALS_EN[ws_seal],
        "position": position_in_ws,
        "start_kin": ws_start_kin,
    }


# ============================================================
# 流年计算
# ============================================================

def calc_yearly_kin(birth_date, year):
    """计算某一年的流年Kin（该年生日当天的Kin）"""
    if isinstance(birth_date, str):
        birth_date = date.fromisoformat(birth_date)

    # 处理2月29日出生的情况
    month, day = birth_date.month, birth_date.day
    if month == 2 and day == 29:
        if not is_leap_year(year):
            month, day = 2, 28

    birthday_this_year = date(year, month, day)
    return date_to_kin(birthday_this_year)


def calc_yearly_report(birth_date, year):
    """生成流年报告"""
    yearly_kin = calc_yearly_kin(birth_date, year)
    return calc_five_destiny(yearly_kin)


# ============================================================
# 合盘计算
# ============================================================

def calc_relationship(kin_a, kin_b):
    """计算两人的关系类型"""
    seal_a = kin_to_seal(kin_a)
    seal_b = kin_to_seal(kin_b)
    tone_a = kin_to_tone(kin_a)
    tone_b = kin_to_tone(kin_b)

    # 计算A的五大位
    a_support = calc_support_seal(seal_a)
    a_challenge = calc_challenge_seal(seal_a)
    a_occult = calc_occult_seal(seal_a)
    a_guide = calc_guide_seal(seal_a, tone_a)

    # 计算B的五大位
    b_support = calc_support_seal(seal_b)
    b_challenge = calc_challenge_seal(seal_b)
    b_occult = calc_occult_seal(seal_b)
    b_guide = calc_guide_seal(seal_b, tone_b)

    # B的图腾出现在A的哪个位置
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

    # A的图腾出现在B的哪个位置
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

    # 合盘Kin
    combined_kin = ((kin_a + kin_b - 1) % 260) + 1

    # 颜色关系
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

    # 调性关系
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


# ============================================================
# 格式化输出
# ============================================================

def format_destiny(destiny, label=""):
    """格式化五大天赋盘输出"""
    m = destiny["main"]
    s = destiny["support"]
    g = destiny["guide"]
    c = destiny["challenge"]
    o = destiny["occult"]

    title = f"{'=' * 50}\n"
    if label:
        title += f"  {label}\n{'=' * 50}\n"
    else:
        title += f"  星系印记解读\n{'=' * 50}\n"

    output = title
    output += f"\n✦ Kin {destiny['kin']}: {m['tone_name']}{m['tone']} · {m['seal_name']}\n"
    output += f"  {m['tone_en']} {m['tone']} · {m['seal_en']}\n"
    output += f"  颜色: {m['color']}色 | 图腾关键词: {m['keywords']}\n"
    output += f"  调性关键词: {m['tone_keywords']}\n"

    output += f"\n{'─' * 50}\n"
    output += f"  五大天赋盘\n"
    output += f"{'─' * 50}\n"

    output += f"\n              【引导】\n"
    output += f"           {g['tone_name']}{destiny['main']['tone']} · {g['seal_name']}\n"
    output += f"           ({g['seal_en']})\n"
    output += f"           关键词: {g['keywords']}\n"

    output += f"\n  【支持】  ←  【主印记】  →  【挑战】\n"
    output += f"  {s['tone_name']}{destiny['main']['tone']}·{s['seal_name']}   {m['tone_name']}{m['tone']}·{m['seal_name']}   {c['tone_name']}{destiny['main']['tone']}·{c['seal_name']}\n"

    output += f"\n              【隐藏推动】\n"
    output += f"           {o['tone_name']}{o['tone']} · {o['seal_name']}\n"
    output += f"           ({o['seal_en']})\n"
    output += f"           关键词: {o['keywords']}\n"

    # 波符信息
    ws = calc_wavespell(destiny['kin'])
    output += f"\n{'─' * 50}\n"
    output += f"  波符信息\n"
    output += f"{'─' * 50}\n"
    output += f"  所属波符: 第{ws['wavespell_number']}波符 · {ws['wavespell_name']}波符\n"
    output += f"  波符内位置: 第{ws['position']}天 (调性{ws['position']}: {TONES[ws['position']]})\n"

    return output


def format_compatibility(result):
    """格式化合盘输出"""
    a = result["person_a"]["main"]
    b = result["person_b"]["main"]

    output = f"\n{'=' * 50}\n"
    output += f"  双人合盘分析\n"
    output += f"{'=' * 50}\n\n"

    output += f"  A: Kin {result['person_a']['kin']} {a['tone_name']}{a['tone']}·{a['seal_name']}\n"
    output += f"  B: Kin {result['person_b']['kin']} {b['tone_name']}{b['tone']}·{b['seal_name']}\n\n"

    output += f"  颜色关系: {result['color_relation']}\n"
    output += f"  调性关系: {result['tone_relation']}\n\n"

    output += f"  B在A天赋盘中的位置: {', '.join(result['b_in_a_positions'])}\n"
    output += f"  A在B天赋盘中的位置: {', '.join(result['a_in_b_positions'])}\n\n"

    cm = result["combined_destiny"]["main"]
    output += f"  合盘Kin: Kin {result['combined_kin']} {cm['tone_name']}{cm['tone']}·{cm['seal_name']}\n"
    output += f"  合盘关键词: {cm['keywords']}\n"

    return output


# ============================================================
# 主程序
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="玛雅天赋计算工具 (Mayan Destiny Calculator)"
    )
    parser.add_argument(
        "birthday",
        help="阳历出生日期，格式: YYYY-MM-DD"
    )
    parser.add_argument(
        "--compatibility", "-c",
        help="合盘对象的阳历出生日期，格式: YYYY-MM-DD"
    )
    parser.add_argument(
        "--yearly", "-y",
        type=int,
        help="计算指定年份的流年运势"
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="以JSON格式输出"
    )

    args = parser.parse_args()

    try:
        birth_date = date.fromisoformat(args.birthday)
    except ValueError:
        print(f"错误: 无法解析日期 '{args.birthday}'，请使用 YYYY-MM-DD 格式")
        sys.exit(1)

    # 计算主印记
    kin = date_to_kin(birth_date)
    destiny = calc_five_destiny(kin)

    if args.json:
        import json
        result = {"birth_date": str(birth_date), "destiny": destiny}

        if args.yearly:
            yearly = calc_yearly_report(birth_date, args.yearly)
            result["yearly"] = {"year": args.yearly, "destiny": yearly}

        if args.compatibility:
            other_date = date.fromisoformat(args.compatibility)
            other_kin = date_to_kin(other_date)
            compat = calc_relationship(kin, other_kin)
            # 简化JSON输出（去掉重复的person_a）
            result["compatibility"] = {
                "other_date": str(other_date),
                "other_kin": other_kin,
                "b_in_a": compat["b_in_a_positions"],
                "a_in_b": compat["a_in_b_positions"],
                "combined_kin": compat["combined_kin"],
                "color_relation": compat["color_relation"],
                "tone_relation": compat["tone_relation"],
            }

        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 文本输出
        print(format_destiny(destiny, f"出生日期: {birth_date}"))

        if args.yearly:
            yearly = calc_yearly_report(birth_date, args.yearly)
            print(format_destiny(yearly, f"{args.yearly}年 流年运势"))

        if args.compatibility:
            try:
                other_date = date.fromisoformat(args.compatibility)
            except ValueError:
                print(f"错误: 无法解析合盘日期 '{args.compatibility}'")
                sys.exit(1)
            other_kin = date_to_kin(other_date)
            compat = calc_relationship(kin, other_kin)
            print(format_destiny(compat["person_b"], f"合盘对象: {other_date}"))
            print(format_compatibility(compat))


if __name__ == "__main__":
    main()
