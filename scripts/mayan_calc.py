#!/usr/bin/env python3
"""玛雅天赋 CLI 入口。"""

import argparse
import json
import pathlib
import sys
from textwrap import dedent


ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mayan_kin.core import (  # noqa: E402
    build_compatibility_report,
    build_personal_report,
    build_yearly_report,
    calc_five_destiny,
    calc_relationship,
    calc_yearly_report,
    date_to_kin,
    format_compatibility,
    format_compatibility_report,
    format_destiny,
    format_personal_report,
    format_yearly_report,
    parse_iso_date,
    serialize_destiny,
)


CLI_NAME = "mayan_calc.py"
CLI_VERSION = "v1.0"
CLI_USAGE = "python3 scripts/mayan_calc.py [birthday] [options]"
CLI_OUTPUT_PRECEDENCE = ["--contract", "--report", "--json", "text"]


def build_cli_contract():
    return {
        "cli": CLI_NAME,
        "version": CLI_VERSION,
        "description": "Mayan Destiny / Dreamspell / Tzolkin Kin calculator CLI",
        "usage": CLI_USAGE,
        "input": {
            "birthday": {
                "required_for_normal_modes": True,
                "format": "YYYY-MM-DD",
                "calendar": "Gregorian",
            },
            "compatibility": {
                "optional": True,
                "format": "YYYY-MM-DD",
                "purpose": "第二个生日，用于合盘分析",
            },
            "yearly": {
                "optional": True,
                "type": "integer",
                "purpose": "计算指定年份的流年结果",
            },
        },
        "output_modes": {
            "text": "默认人类可读输出",
            "json": "机器可读输出，包含 birth_date / destiny / yearly / compatibility",
            "report": "指导型个人说明书输出，适合小白、咨询和内容复用",
            "contract": "CLI 与 JSON 契约说明，不需要 birthday",
        },
        "json_contract": {
            "top_level_fields": [
                "birth_date",
                "destiny",
                "yearly? (optional)",
                "compatibility? (optional)",
            ],
            "destiny_shape": "serialize_destiny(destiny) 的结果，包含五大天赋盘与 wavespell",
            "yearly_shape": "yearly.year + yearly.destiny，结构与 destiny 一致",
            "compatibility_shape": (
                "other_date, other_kin, b_in_a, a_in_b, combined_kin, "
                "color_relation, tone_relation"
            ),
        },
        "precedence": CLI_OUTPUT_PRECEDENCE,
        "exit_codes": {
            0: "success",
            1: "invalid input or parse failure",
        },
    }

def main():
    parser = argparse.ArgumentParser(
        prog=CLI_NAME,
        description=dedent(
            """
            玛雅天赋计算工具 (Mayan Destiny / Dreamspell / Tzolkin)

            默认模式输出可读文本；`--json` 输出机器可读结果；
            `--report` 输出个人说明书；`--contract` 输出接口契约。
            """
        ).strip(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=dedent(
            """
            Examples:
              python3 scripts/mayan_calc.py 1995-03-03
              python3 scripts/mayan_calc.py 1995-03-03 --json
              python3 scripts/mayan_calc.py 1995-03-03 --report
              python3 scripts/mayan_calc.py 1995-03-03 --yearly 2026
              python3 scripts/mayan_calc.py 1995-03-03 --compatibility 1992-07-20
              python3 scripts/mayan_calc.py --contract

            Output precedence:
              --contract > --report > --json > default text

            Notes:
              - `birthday` is required for normal modes.
              - `--contract` does not require `birthday`.
              - `--report` is intended for human reading; use `--json` for downstream systems.
            """
        ).strip(),
    )
    parser.add_argument(
        "birthday",
        nargs="?",
        help="阳历出生日期，格式: YYYY-MM-DD；普通模式必填，`--contract` 模式可省略"
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
    parser.add_argument(
        "--report", "-r",
        action="store_true",
        help="输出个人说明书报告"
    )
    parser.add_argument(
        "--contract",
        action="store_true",
        help="输出 CLI / JSON 契约说明，不需要 birthday"
    )

    args = parser.parse_args()

    if args.contract:
        print(json.dumps(build_cli_contract(), ensure_ascii=False, indent=2))
        return

    if not args.birthday:
        parser.error("birthday 为必填参数；如需查看接口契约，请使用 --contract")

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

    if args.report:
        report = build_personal_report(destiny, birth_date=birth_date)
        sys.stdout.write(format_personal_report(report))
        if args.yearly:
            yearly_report = build_yearly_report(birth_date, args.yearly)
            sys.stdout.write(format_yearly_report(yearly_report))
        if other_date:
            other_kin = date_to_kin(other_date)
            compatibility_report = build_compatibility_report(kin, other_kin)
            sys.stdout.write(format_compatibility_report(compatibility_report))
        return

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

    sys.stdout.write(format_destiny(destiny, f"出生日期: {birth_date}"))

    if args.yearly:
        yearly = calc_yearly_report(birth_date, args.yearly)
        sys.stdout.write(format_destiny(yearly, f"{args.yearly}年 流年运势"))

    if other_date:
        other_kin = date_to_kin(other_date)
        compat = calc_relationship(kin, other_kin)
        sys.stdout.write(format_destiny(compat["person_b"], f"合盘对象: {other_date}"))
        sys.stdout.write(format_compatibility(compat))


if __name__ == "__main__":
    main()
