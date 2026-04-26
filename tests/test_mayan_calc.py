import json
import pathlib
import subprocess
import sys
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "mayan_calc.py"
KNOWLEDGE_INDEX = ROOT / "references" / "knowledge-index.json"
sys.path.insert(0, str(ROOT))

from mayan_kin import core as mayan_calc
from scripts.collect_public_figures_wikidata import normalize_bindings
from scripts.enrich_public_figure_history_labels import build_history_label
from scripts.evaluate_history_label_holdout import evaluate as evaluate_history_label_holdout
from scripts.evaluate_public_figure_holdout import evaluate as evaluate_public_figure_holdout
from scripts.evaluate_public_figure_holdout import expression_weights_for_birth_date
from scripts.evaluate_time_split_predictions import evaluate as evaluate_time_split_predictions
from scripts.evaluate_prospective_predictions import evaluate as evaluate_prospective_predictions
from scripts.generate_prospective_predictions import build_registry


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
        self.assertEqual(report["style"], "basic")
        self.assertEqual(len(report["growth_path"]), 5)
        self.assertIn("career", report["action_guide"])
        self.assertIn("consultation", report["delivery_layers"])

    def test_report_style_changes_metadata_and_language(self):
        destiny = mayan_calc.calc_five_destiny(mayan_calc.date_to_kin("1995-03-03"))
        basic = mayan_calc.build_personal_report(destiny, birth_date="1995-03-03", style="basic")
        deep = mayan_calc.build_personal_report(destiny, birth_date="1995-03-03", style="deep")
        legacy = mayan_calc.build_personal_report(destiny, birth_date="1995-03-03", style="professional")
        self.assertEqual(basic["style_label"], "基础版")
        self.assertEqual(deep["style_label"], "深度版")
        self.assertEqual(legacy["style"], "deep")
        self.assertIn("磁性红月的主轴", deep["summary"]["core_theme"])
        self.assertIn("deep_analysis", deep)
        self.assertEqual(len(deep["deep_analysis"]["structural_analysis"]), 5)
        self.assertIn("precision_profile", deep["deep_analysis"])
        self.assertEqual(len(deep["deep_analysis"]["precision_profile"]["axis_reading"]), 5)
        self.assertEqual(len(deep["deep_analysis"]["precision_profile"]["trigger_map"]), 4)
        self.assertEqual(len(deep["deep_analysis"]["precision_profile"]["validation_checks"]), 5)
        self.assertIn("红月", deep["deep_analysis"]["precision_profile"]["axis_reading"][0])
        self.assertIn("expression_profile", deep["deep_analysis"])
        self.assertIn("public_healing", deep["deep_analysis"]["expression_profile"]["tags"])
        self.assertIn("evaluation_signature", deep["deep_analysis"]["expression_profile"])
        signature = deep["deep_analysis"]["expression_profile"]["evaluation_signature"]
        self.assertEqual(signature["protocol"], "expression_signature_v1")
        self.assertGreaterEqual(len(signature["primary_tags"]), 10)
        self.assertGreaterEqual(signature["weighted_tags"][0]["weight"], 1.0)
        self.assertGreaterEqual(signature["weighted_tags"][0]["weight"], signature["weighted_tags"][1]["weight"])
        self.assertEqual(len(deep["deep_analysis"]["expression_profile"]["roles"]), 5)
        self.assertEqual(len(deep["deep_analysis"]["risk_matrix"]), 4)
        self.assertEqual(len(deep["deep_analysis"]["situational_insight"]["current_block"]), 3)
        self.assertEqual(len(deep["deep_analysis"]["reflection_dialogue"]["resonance_points"]), 3)
        self.assertIn("这股力量是你最像自己的地方", deep["positions"]["main"]["explanation"])
        self.assertIn("放在你身上，它通常会表现成这样", deep["positions"]["main"]["explanation"])
        self.assertIn("它会把问题不断拉回一个核心追问", deep["positions"]["main"]["explanation"])

    def test_xiaowu_deep_report_is_not_red_moon_template(self):
        destiny = mayan_calc.calc_five_destiny(mayan_calc.date_to_kin("1991-08-25"))
        report = mayan_calc.build_personal_report(destiny, birth_date="1991-08-25", style="deep")
        rendered = mayan_calc.format_personal_report(report)
        self.assertEqual(report["kin"], 224)
        self.assertIn("电力黄种子", rendered)
        self.assertIn("什么值得长期培育", rendered)
        self.assertIn("把视野拆成阶段策略", rendered)
        self.assertIn("感受、投射和现实校准", rendered)
        self.assertNotIn("敏感活成长期承受", rendered)
        self.assertNotIn("维持关系质量", rendered)
        self.assertNotIn("理解别人", rendered)

    def test_wenyi_deep_report_uses_blue_hand_not_seed_template(self):
        destiny = mayan_calc.calc_five_destiny(mayan_calc.date_to_kin("1999-11-16"))
        report = mayan_calc.build_personal_report(destiny, birth_date="1999-11-16", style="deep")
        rendered = mayan_calc.format_personal_report(report)
        self.assertEqual(report["kin"], 107)
        self.assertIn("电力蓝手", rendered)
        self.assertIn("哪些事该由我的手完成，哪些要归还给对方", rendered)
        self.assertIn("问题、求助或收尾任务", rendered)
        self.assertNotIn("这颗种子到底要不要继续培育", rendered)
        self.assertNotIn("先选种子", rendered)
        self.assertNotIn("种子、土壤、节奏和目标", rendered)

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

    def test_cli_deep_style_report_output_is_rendered(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "1995-03-03", "--report", "--style", "deep"],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("输出风格: 深度版", result.stdout)
        self.assertIn("解读校准", result.stdout)
        self.assertIn("验证问题", result.stdout)
        self.assertIn("最小实验", result.stdout)
        self.assertIn("现实表达校准", result.stdout)
        self.assertIn("情境直读", result.stdout)
        self.assertIn("个人感悟对话入口", result.stdout)
        self.assertNotIn("行动建议：", result.stdout)

    def test_cli_deep_style_report_contains_deeper_sections(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "1995-03-03", "--report", "--style", "deep"],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("输出风格: 深度版", result.stdout)
        self.assertIn("结构分析", result.stdout)
        self.assertIn("风险矩阵", result.stdout)
        self.assertIn("解读校准", result.stdout)
        self.assertIn("深度应用", result.stdout)
        self.assertIn("情境直读", result.stdout)

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

    def test_auto_plan_recommends_deep_for_yearly_direction_query(self):
        plan = mayan_calc.build_auto_plan("我想看2026流年和事业方向")
        self.assertEqual(plan["recommended_style"], "deep")
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
        self.assertEqual(payload["recommended_style"], "basic")
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
        self.assertIn("\"recommended_style\": \"deep\"", result.stdout)
        self.assertIn("\"recommended_report_mode\": \"yearly\"", result.stdout)
        self.assertNotIn("玛雅天赋个人说明书", result.stdout)
        self.assertIn("2026 年流年说明书", result.stdout)
        self.assertIn("输出风格: 深度版", result.stdout)

    def test_build_yearly_report_contains_multi_scene_layers(self):
        report = mayan_calc.build_yearly_report("1995-03-03", 2026, style="deep")
        self.assertEqual(report["scene"], "yearly")
        self.assertEqual(report["style"], "deep")
        self.assertEqual(report["year"], 2026)
        self.assertEqual(report["natal_kin"], 209)
        self.assertEqual(report["kin"], mayan_calc.calc_yearly_kin("1995-03-03", 2026))
        self.assertEqual(len(report["delivery_layers"]["consultation"]["questions"]), 3)
        self.assertEqual(len(report["delivery_layers"]["content"]["angles"]), 4)
        self.assertIn("deep_analysis", report)
        self.assertEqual(len(report["deep_analysis"]["annual_structure"]), 5)
        self.assertEqual(len(report["deep_analysis"]["risk_windows"]), 4)
        self.assertIn("precision_profile", report["deep_analysis"])
        self.assertEqual(len(report["deep_analysis"]["precision_profile"]["axis_reading"]), 5)
        rendered = mayan_calc.format_yearly_report(report)
        self.assertIn("输出风格: 深度版", rendered)
        self.assertIn("年度结构", rendered)
        self.assertIn("风险窗口", rendered)
        self.assertIn("年度解读校准", rendered)
        self.assertIn("年度情境直读", rendered)
        self.assertIn("策略配置", rendered)
        self.assertIn("咨询视角", rendered)
        self.assertIn("内容产品视角", rendered)
        self.assertIn("AI 对话视角", rendered)

    def test_build_compatibility_report_contains_multi_scene_layers(self):
        report = mayan_calc.build_compatibility_report(216, 67, style="deep")
        self.assertEqual(report["scene"], "compatibility")
        self.assertEqual(report["style"], "deep")
        self.assertEqual(report["combined_kin"], 23)
        self.assertEqual(report["interaction"]["tone_relation"], "调性差值 6（需要主动调频共振）")
        self.assertEqual(len(report["delivery_layers"]["consultation"]["questions"]), 3)
        self.assertEqual(len(report["delivery_layers"]["ai"]["prompts"]), 3)
        rendered = mayan_calc.format_compatibility_report(report)
        self.assertIn("输出风格: 深度版", rendered)
        self.assertIn("关系建议", rendered)
        self.assertIn("咨询视角", rendered)
        self.assertIn("内容产品视角", rendered)
        self.assertIn("AI 对话视角", rendered)

    def test_deep_compatibility_report_contains_deeper_sections(self):
        report = mayan_calc.build_compatibility_report(216, 67, style="deep")
        self.assertEqual(report["style"], "deep")
        self.assertIn("deep_analysis", report)
        self.assertEqual(len(report["deep_analysis"]["relationship_structure"]), 4)
        self.assertEqual(len(report["deep_analysis"]["tension_matrix"]), 4)
        self.assertIn("precision_profile", report["deep_analysis"])
        self.assertEqual(len(report["deep_analysis"]["precision_profile"]["trigger_map"]), 4)
        self.assertIn("situational_insight", report["deep_analysis"])
        rendered = mayan_calc.format_compatibility_report(report)
        self.assertIn("关系结构", rendered)
        self.assertIn("张力来源", rendered)
        self.assertIn("关系解读校准", rendered)
        self.assertIn("关系情境直读", rendered)
        self.assertIn("协作模型", rendered)

    def test_deep_yearly_report_contains_situational_insight(self):
        report = mayan_calc.build_yearly_report("1995-03-03", 2026, style="deep")
        self.assertIn("deep_analysis", report)
        self.assertIn("situational_insight", report["deep_analysis"])
        insight = report["deep_analysis"]["situational_insight"]
        self.assertEqual(len(insight["current_pressure"]), 3)
        self.assertEqual(len(insight["common_misread"]), 3)
        self.assertEqual(len(insight["minimum_move"]), 3)

    def test_deep_compatibility_report_contains_situational_insight(self):
        report = mayan_calc.build_compatibility_report(216, 67, style="deep")
        self.assertIn("deep_analysis", report)
        insight = report["deep_analysis"]["situational_insight"]
        self.assertEqual(len(insight["current_knot"]), 3)
        self.assertEqual(len(insight["relationship_drift"]), 3)
        self.assertEqual(len(insight["minimum_alignment"]), 3)

    def test_public_figure_benchmark_exceeds_threshold(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "evaluate_public_figures.py"), "--min-score", "90"],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("Public figure benchmark cases: 12", result.stdout)
        self.assertIn("Average score:", result.stdout)

    def test_blind_trial_pipeline_scores_control_data(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = pathlib.Path(tmpdir)
            packets = tmp / "packets.json"
            key = tmp / "key.json"
            responses = tmp / "responses.json"
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "generate_blind_trial_packets.py"),
                    "--participants",
                    str(ROOT / "references" / "blind-participants-template.json"),
                    "--candidate-count",
                    "3",
                    "--packets-out",
                    str(packets),
                    "--key-out",
                    str(key),
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            key_payload = json.loads(key.read_text(encoding="utf-8"))
            responses.write_text(
                json.dumps(
                    {
                        "responses": [
                            {"trial_id": item["trial_id"], "selected_label": item["correct_label"]}
                            for item in key_payload["keys"]
                        ]
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "evaluate_blind_trials.py"),
                    "--responses",
                    str(responses),
                    "--key",
                    str(key),
                    "--packets",
                    str(packets),
                    "--min-sample-size",
                    "5",
                    "--alpha",
                    "0.01",
                    "--target-rate",
                    "0.8",
                    "--min-score",
                    "90",
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertIn("Scientific accuracy score: 100.0", result.stdout)

    def test_wikidata_public_figure_normalizer_aggregates_and_splits(self):
        bindings = [
            {
                "person": {"value": "http://www.wikidata.org/entity/Q100"},
                "personLabel": {"value": "Sample Writer"},
                "personDescription": {"value": "public novelist and journalist"},
                "birth": {"value": "1970-01-02T00:00:00Z"},
                "occupationLabel": {"value": "writer"},
            },
            {
                "person": {"value": "http://www.wikidata.org/entity/Q100"},
                "personLabel": {"value": "Sample Writer"},
                "personDescription": {"value": "public novelist and journalist"},
                "birth": {"value": "1970-01-02T00:00:00Z"},
                "occupationLabel": {"value": "journalist"},
            },
        ]
        records = normalize_bindings(bindings)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["id"], "Q100")
        self.assertEqual(records[0]["birth_date"], "1970-01-02")
        self.assertIn("communication", records[0]["observed_tags"])
        self.assertIn(records[0]["split"], {"train", "dev", "holdout"})

    def test_public_figure_holdout_evaluator_runs_on_control_dataset(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = pathlib.Path(tmpdir)
            records = []
            for index, birth_date in enumerate([
                "1995-03-03",
                "1990-03-15",
                "1981-09-04",
                "1955-02-24",
                "1879-03-14",
                "1918-07-18",
            ]):
                tag_weights = expression_weights_for_birth_date(birth_date, top_n=18)
                records.append({
                    "id": f"Q{index + 1}",
                    "name": f"Control {index + 1}",
                    "birth_date": birth_date,
                    "split": "holdout",
                    "observed_tags": list(tag_weights)[:5],
                })
            dataset = {
                "version": "test",
                "record_count": len(records),
                "records": records,
            }
            dataset_path = tmp / "dataset.json"
            dataset_path.write_text(json.dumps(dataset, ensure_ascii=False), encoding="utf-8")
            result = evaluate_public_figure_holdout(
                dataset_path,
                protocol_path=tmp / "missing-protocol.json",
                split="holdout",
                candidate_count=3,
                top_n=18,
                min_sample_size=1,
            )
            self.assertEqual(result["sample_size"], 6)
            self.assertIn("public_figure_accuracy_score", result)
            self.assertIn(result["status"], {"passed", "significant_but_below_target", "not_significant"})

    def test_history_label_builder_uses_public_biography_without_kin(self):
        record = {
            "id": "Q-test",
            "name": "Public Sample",
            "birth_date": "1970-01-02",
            "split": "holdout",
            "description": "civil rights leader and writer",
            "occupations": ["writer", "activist"],
        }
        extract = (
            "Public Sample founded a civil rights organization in 2005. "
            "In 2018, she won an award for humanitarian leadership after surviving exile."
        )
        label = build_history_label(record, "Public Sample", extract, "https://example.com", 2010)
        self.assertFalse(label["history_labels"]["leakage_guard"]["uses_kin"])
        self.assertIn("core_achievements", label["history_labels"]["dimensions"])
        self.assertIn("human_rights", label["history_labels"]["detailed_tags"])
        self.assertIn("humanitarian", label["time_split"]["post_cutoff_tags"])

    def test_history_label_and_time_split_evaluators_run_on_control_data(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = pathlib.Path(tmpdir)
            records = []
            for index, birth_date in enumerate([
                "1995-03-03",
                "1990-03-15",
                "1981-09-04",
                "1955-02-24",
                "1879-03-14",
                "1918-07-18",
            ]):
                tags = list(expression_weights_for_birth_date(birth_date, top_n=18))[:6]
                records.append({
                    "id": f"Q{index + 1}",
                    "name": f"History Control {index + 1}",
                    "birth_date": birth_date,
                    "split": "holdout",
                    "history_labels": {
                        "detailed_tags": tags,
                        "dimensions": {
                            "core_achievements": {"tags": tags[:3]},
                            "public_expression": {"tags": tags[3:]},
                        },
                    },
                    "time_split": {
                        "cutoff_year": 2010,
                        "post_cutoff_tags": tags[:4],
                        "post_cutoff_sentences": ["In 2018, public evidence matched the control tags."],
                    },
                })
            dataset_path = tmp / "history.json"
            dataset_path.write_text(
                json.dumps({"version": "test", "record_count": len(records), "records": records}, ensure_ascii=False),
                encoding="utf-8",
            )
            history_result = evaluate_history_label_holdout(
                dataset_path,
                protocol_path=tmp / "missing-protocol.json",
                split="holdout",
                candidate_count=3,
                top_n=18,
                min_sample_size=1,
            )
            time_result = evaluate_time_split_predictions(
                dataset_path,
                protocol_path=tmp / "missing-protocol.json",
                split="holdout",
                top_n=18,
                min_sample_size=1,
                min_score=0,
            )
            self.assertEqual(history_result["sample_size"], 6)
            self.assertIn("history_label_accuracy_score", history_result)
            self.assertEqual(time_result["eligible_sample_size"], 6)
            self.assertIsNotNone(time_result["time_split_prediction_score"])

    def test_prospective_prediction_registry_and_evaluator(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = pathlib.Path(tmpdir)
            registry = build_registry(
                [{"id": "subject_1", "name": "Subject", "birth_date": "1995-03-03"}],
                target_year=2027,
            )
            prediction = registry["predictions"][0]
            registry_path = tmp / "registry.json"
            outcomes_path = tmp / "outcomes.json"
            registry_path.write_text(json.dumps(registry, ensure_ascii=False), encoding="utf-8")
            outcomes_path.write_text(
                json.dumps(
                    {
                        "outcomes": [
                            {
                                "prediction_id": prediction["prediction_id"],
                                "evidence_tags": prediction["prediction"]["top_expression_tags"],
                            }
                        ]
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            result = evaluate_prospective_predictions(registry_path, outcomes_path, min_score=90)
            self.assertEqual(result["average_prospective_score"], 100.0)
            self.assertEqual(result["status"], "passed")


if __name__ == "__main__":
    unittest.main()
