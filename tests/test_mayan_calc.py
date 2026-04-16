import json
import pathlib
import subprocess
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "mayan_calc.py"
KNOWLEDGE_INDEX = ROOT / "references" / "knowledge-index.json"
sys.path.insert(0, str(ROOT))

from mayan_kin import core as mayan_calc


class MayanCalcTests(unittest.TestCase):
    REFERENCE_SAMPLES = [
        ("1997-07-26", 44, "黄种子", "超频"),
        ("2012-07-26", 59, "蓝风暴", "共振"),
        ("2013-07-26", 164, "黄种子", "银河"),
        ("2014-07-26", 9, "红月", "太阳"),
    ]

    def test_reference_date_maps_to_reference_kin(self):
        self.assertEqual(mayan_calc.date_to_kin("2013-07-26"), 164)

    def test_leap_day_is_skipped_in_kin_progression(self):
        kin_feb_28 = mayan_calc.date_to_kin("2024-02-28")
        kin_feb_29 = mayan_calc.date_to_kin("2024-02-29")
        kin_mar_01 = mayan_calc.date_to_kin("2024-03-01")
        self.assertEqual(kin_feb_28, kin_feb_29)
        self.assertEqual(kin_mar_01, ((kin_feb_28 % 260) + 1))

    def test_yearly_kin_handles_feb_29_birthdays(self):
        self.assertEqual(
            mayan_calc.calc_yearly_kin("2000-02-29", 2025),
            mayan_calc.date_to_kin("2025-02-28"),
        )

    def test_json_output_includes_wavespell(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "1990-03-15", "--json"],
            capture_output=True,
            text=True,
            check=True,
        )
        payload = json.loads(result.stdout)
        self.assertEqual(payload["destiny"]["wavespell"]["wavespell_number"], 17)
        self.assertEqual(payload["destiny"]["wavespell"]["position"], 8)

    def test_invalid_compatibility_date_exits_cleanly(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "1990-03-15", "--json", "--compatibility", "bad-date"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("无法解析合盘日期", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_core_relationship_result_is_stable(self):
        result = mayan_calc.calc_relationship(216, 67)
        self.assertEqual(result["combined_kin"], 23)
        self.assertEqual(result["color_relation"], "蓝黄互补（转化与成熟的互补，天然支持关系）")
        self.assertEqual(result["tone_relation"], "调性差值 6（需要主动调频共振）")

    def test_cli_yearly_json_is_parseable(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "1990-03-15", "--json", "--yearly", "2026"],
            capture_output=True,
            text=True,
            check=True,
        )
        payload = json.loads(result.stdout)
        self.assertEqual(payload["yearly"]["year"], 2026)
        self.assertIn("wavespell", payload["yearly"]["destiny"])

    def test_law_of_time_reference_samples(self):
        for birth_date, kin, seal_name, tone_name in self.REFERENCE_SAMPLES:
            with self.subTest(birth_date=birth_date):
                destiny = mayan_calc.calc_five_destiny(mayan_calc.date_to_kin(birth_date))
                self.assertEqual(destiny["kin"], kin)
                self.assertEqual(destiny["main"]["seal_name"], seal_name)
                self.assertEqual(destiny["main"]["tone_name"], tone_name)

    def test_build_personal_report_contains_growth_path(self):
        destiny = mayan_calc.calc_five_destiny(mayan_calc.date_to_kin("1995-03-03"))
        report = mayan_calc.build_personal_report(destiny, birth_date="1995-03-03")
        self.assertEqual(report["kin"], 209)
        self.assertEqual(report["scene"], "personal")
        self.assertEqual(report["style"], "beginner")
        self.assertEqual(len(report["growth_path"]), 5)
        self.assertIn("career", report["action_guide"])
        self.assertIn("consultation", report["delivery_layers"])

    def test_report_style_changes_metadata_and_language(self):
        destiny = mayan_calc.calc_five_destiny(mayan_calc.date_to_kin("1995-03-03"))
        beginner = mayan_calc.build_personal_report(destiny, birth_date="1995-03-03", style="beginner")
        consulting = mayan_calc.build_personal_report(destiny, birth_date="1995-03-03", style="consulting")
        professional = mayan_calc.build_personal_report(destiny, birth_date="1995-03-03", style="professional")
        self.assertEqual(consulting["style_label"], "咨询版")
        self.assertEqual(professional["style_label"], "专业版")
        self.assertNotEqual(beginner["summary"]["core_theme"], consulting["summary"]["core_theme"])
        self.assertTrue(consulting["summary"]["core_theme"].startswith("咨询提示："))
        self.assertIn("磁性红月的主轴", professional["summary"]["core_theme"])
        self.assertIn("professional_analysis", professional)
        self.assertEqual(len(professional["professional_analysis"]["structural_analysis"]), 5)
        self.assertEqual(len(professional["professional_analysis"]["risk_matrix"]), 4)

    def test_cli_report_output_is_rendered(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "1995-03-03", "--report"],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("玛雅天赋个人说明书", result.stdout)
        self.assertIn("成长路径", result.stdout)
        self.assertIn("行动建议", result.stdout)
        self.assertIn("咨询视角", result.stdout)
        self.assertIn("AI 对话视角", result.stdout)

    def test_cli_consulting_style_report_output_is_rendered(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "1995-03-03", "--report", "--style", "consulting"],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("输出风格: 咨询版", result.stdout)
        self.assertIn("咨询提示：", result.stdout)

    def test_cli_professional_style_report_contains_deeper_sections(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "1995-03-03", "--report", "--style", "professional"],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("输出风格: 专业版", result.stdout)
        self.assertIn("结构分析", result.stdout)
        self.assertIn("风险矩阵", result.stdout)
        self.assertIn("专业应用", result.stdout)

    def test_cli_yearly_report_output_is_rendered(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "1995-03-03", "--report", "--yearly", "2026"],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("2026 年流年说明书", result.stdout)
        self.assertIn("年度摘要", result.stdout)
        self.assertIn("年度建议", result.stdout)

    def test_cli_compatibility_report_output_is_rendered(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "1995-03-03", "--report", "--compatibility", "1992-07-20"],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("双人合盘说明书", result.stdout)
        self.assertIn("关系摘要", result.stdout)
        self.assertIn("关系建议", result.stdout)

    def test_cli_contract_output_is_parseable(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--contract"],
            capture_output=True,
            text=True,
            check=True,
        )
        payload = json.loads(result.stdout)
        self.assertEqual(payload["cli"], "mayan_calc.py")
        self.assertEqual(payload["precedence"][0], "--contract")
        self.assertIn("report", payload["output_modes"])
        self.assertIn("style", payload["input"])

    def test_knowledge_index_is_parseable(self):
        payload = json.loads(KNOWLEDGE_INDEX.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], "v1")
        self.assertGreaterEqual(len(payload["cards"]), 10)
        self.assertTrue(any(card["id"] == "yearly" for card in payload["cards"]))

    def test_knowledge_router_matches_yearly_query(self):
        routed = mayan_calc.route_query("我想看2026流年和事业方向", limit=3)
        ids = [card["id"] for card in routed["recommended_cards"]]
        self.assertIn("yearly", ids)
        self.assertIn("guidance", ids)

    def test_cli_route_query_output_is_parseable(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--route-query", "我想看合盘和关系边界"],
            capture_output=True,
            text=True,
            check=True,
        )
        payload = json.loads(result.stdout)
        self.assertEqual(payload["index_version"], "v1")
        ids = [card["id"] for card in payload["recommended_cards"]]
        self.assertIn("compatibility", ids)

    def test_auto_plan_recommends_consulting_for_yearly_direction_query(self):
        plan = mayan_calc.build_auto_plan("我想看2026流年和事业方向")
        self.assertEqual(plan["recommended_style"], "consulting")
        self.assertEqual(plan["recommended_report_mode"], "yearly")
        self.assertIn("yearly", plan["card_ids"])

    def test_auto_plan_recommends_compatibility_mode_for_relationship_query(self):
        plan = mayan_calc.build_auto_plan("我想看合盘和关系边界")
        self.assertEqual(plan["recommended_report_mode"], "compatibility")

    def test_auto_plan_recommends_combined_mode_for_yearly_and_relationship_query(self):
        plan = mayan_calc.build_auto_plan("我想看2026流年、关系和边界")
        self.assertEqual(plan["recommended_report_mode"], "combined")

    def test_cli_auto_answer_without_birthday_is_parseable(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--auto-answer", "我完全不懂玛雅天赋，先给我讲清楚"],
            capture_output=True,
            text=True,
            check=True,
        )
        payload = json.loads(result.stdout)
        self.assertEqual(payload["recommended_style"], "beginner")
        self.assertEqual(payload["recommended_report_mode"], "personal")
        self.assertIn("five_destiny", payload["card_ids"])

    def test_cli_auto_answer_with_birthday_renders_plan_and_report(self):
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "1995-03-03",
                "--auto-answer",
                "我想看2026流年和事业方向",
                "--yearly",
                "2026",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("\"recommended_style\": \"consulting\"", result.stdout)
        self.assertIn("\"recommended_report_mode\": \"yearly\"", result.stdout)
        self.assertNotIn("玛雅天赋个人说明书", result.stdout)
        self.assertIn("2026 年流年说明书", result.stdout)
        self.assertIn("输出风格: 咨询版", result.stdout)

    def test_build_yearly_report_contains_multi_scene_layers(self):
        report = mayan_calc.build_yearly_report("1995-03-03", 2026, style="professional")
        self.assertEqual(report["scene"], "yearly")
        self.assertEqual(report["style"], "professional")
        self.assertEqual(report["year"], 2026)
        self.assertEqual(report["natal_kin"], 209)
        self.assertEqual(report["kin"], mayan_calc.calc_yearly_kin("1995-03-03", 2026))
        self.assertEqual(len(report["delivery_layers"]["consultation"]["questions"]), 3)
        self.assertEqual(len(report["delivery_layers"]["content"]["angles"]), 4)
        rendered = mayan_calc.format_yearly_report(report)
        self.assertIn("输出风格: 专业版", rendered)
        self.assertIn("咨询视角", rendered)
        self.assertIn("内容产品视角", rendered)
        self.assertIn("AI 对话视角", rendered)

    def test_build_compatibility_report_contains_multi_scene_layers(self):
        report = mayan_calc.build_compatibility_report(216, 67, style="consulting")
        self.assertEqual(report["scene"], "compatibility")
        self.assertEqual(report["style"], "consulting")
        self.assertEqual(report["combined_kin"], 23)
        self.assertEqual(report["interaction"]["tone_relation"], "调性差值 6（需要主动调频共振）")
        self.assertEqual(len(report["delivery_layers"]["consultation"]["questions"]), 3)
        self.assertEqual(len(report["delivery_layers"]["ai"]["prompts"]), 3)
        rendered = mayan_calc.format_compatibility_report(report)
        self.assertIn("输出风格: 咨询版", rendered)
        self.assertIn("关系建议", rendered)
        self.assertIn("咨询视角", rendered)
        self.assertIn("内容产品视角", rendered)
        self.assertIn("AI 对话视角", rendered)

    def test_professional_compatibility_report_contains_deeper_sections(self):
        report = mayan_calc.build_compatibility_report(216, 67, style="professional")
        self.assertEqual(report["style"], "professional")
        self.assertIn("professional_analysis", report)
        self.assertEqual(len(report["professional_analysis"]["relationship_structure"]), 4)
        self.assertEqual(len(report["professional_analysis"]["tension_matrix"]), 4)
        rendered = mayan_calc.format_compatibility_report(report)
        self.assertIn("关系结构", rendered)
        self.assertIn("张力来源", rendered)
        self.assertIn("协作模型", rendered)


if __name__ == "__main__":
    unittest.main()
