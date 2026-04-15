#!/usr/bin/env python3
"""玛雅天赋 CLI 入口。"""

import argparse
import json
import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mayan_kin.core import (  # noqa: E402
    calc_five_destiny,
    calc_relationship,
    calc_yearly_report,
    date_to_kin,
    format_compatibility,
    format_destiny,
    parse_iso_date,
    serialize_destiny,
)


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
        birth_date = parse_iso_date(args.birthday, "日期")
        other_date = (
            parse_iso_date(args.compatibility, "合盘日期")
            if args.compatibility else None
        )
    except ValueError as exc:
        print(f"错误: {exc}", file=sys.stderr)
        sys.exit(1)

    kin = date_to_kin(birth_date)
    destiny = calc_five_destiny(kin)

    if args.json:
        result = {"birth_date": str(birth_date), "destiny": serialize_destiny(destiny)}

        if args.yearly:
            yearly = calc_yearly_report(birth_date, args.yearly)
            result["yearly"] = {
                "year": args.yearly,
                "destiny": serialize_destiny(yearly),
            }

        if other_date:
            other_kin = date_to_kin(other_date)
            compat = calc_relationship(kin, other_kin)
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
        return

    print(format_destiny(destiny, f"出生日期: {birth_date}"))

    if args.yearly:
        yearly = calc_yearly_report(birth_date, args.yearly)
        print(format_destiny(yearly, f"{args.yearly}年 流年运势"))

    if other_date:
        other_kin = date_to_kin(other_date)
        compat = calc_relationship(kin, other_kin)
        print(format_destiny(compat["person_b"], f"合盘对象: {other_date}"))
        print(format_compatibility(compat))


if __name__ == "__main__":
    main()
