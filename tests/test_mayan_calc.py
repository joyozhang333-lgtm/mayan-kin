import json
import pathlib
import subprocess
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "mayan_calc.py"
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
        self.assertEqual(len(report["growth_path"]), 5)
        self.assertIn("career", report["action_guide"])
        self.assertIn("consultation", report["delivery_layers"])

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

    def test_build_yearly_report_contains_multi_scene_layers(self):
        report = mayan_calc.build_yearly_report("1995-03-03", 2026)
        self.assertEqual(report["scene"], "yearly")
        self.assertEqual(report["year"], 2026)
        self.assertEqual(report["natal_kin"], 209)
        self.assertEqual(report["kin"], mayan_calc.calc_yearly_kin("1995-03-03", 2026))
        self.assertEqual(len(report["delivery_layers"]["consultation"]["questions"]), 3)
        self.assertEqual(len(report["delivery_layers"]["content"]["angles"]), 4)
        self.assertIn("咨询视角", mayan_calc.format_yearly_report(report))
        self.assertIn("内容产品视角", mayan_calc.format_yearly_report(report))
        self.assertIn("AI 对话视角", mayan_calc.format_yearly_report(report))

    def test_build_compatibility_report_contains_multi_scene_layers(self):
        report = mayan_calc.build_compatibility_report(216, 67)
        self.assertEqual(report["scene"], "compatibility")
        self.assertEqual(report["combined_kin"], 23)
        self.assertEqual(report["interaction"]["tone_relation"], "调性差值 6（需要主动调频共振）")
        self.assertEqual(len(report["delivery_layers"]["consultation"]["questions"]), 3)
        self.assertEqual(len(report["delivery_layers"]["ai"]["prompts"]), 3)
        rendered = mayan_calc.format_compatibility_report(report)
        self.assertIn("关系建议", rendered)
        self.assertIn("咨询视角", rendered)
        self.assertIn("内容产品视角", rendered)
        self.assertIn("AI 对话视角", rendered)


if __name__ == "__main__":
    unittest.main()
