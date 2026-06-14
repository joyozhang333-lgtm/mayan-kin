"""Top-level report builders and formatters (extracted from core.py)."""

from .constants import *  # noqa: F401,F403
from .styling import *  # noqa: F401,F403
from .calculations import *  # noqa: F401,F403
from .profiles import *  # noqa: F401,F403
from .analysis import *  # noqa: F401,F403
from .presentation import *  # noqa: F401,F403


def build_yearly_report(birth_date, year, style="basic"):
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
            "explanation": explain_position(role, annual_destiny[role], normalized_style),
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
    if normalized_style == "deep":
        report["deep_analysis"] = build_professional_yearly_analysis(
            natal_destiny,
            annual_destiny,
            interaction,
            year,
        )
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
    lines.append(f"  输出风格: {report.get('style_label', '基础版')}")
    lines.append(f"  本命参考: Kin {report['natal_kin']} {natal['main']['tone_name']}{natal['main']['seal_name']}")
    lines.append(f"  年度与本命关系: {interaction['color_relation']} | {interaction['tone_relation']}")
    lines.append(f"  风格说明: {report.get('style_description', STYLE_CONFIG['basic']['description'])}")

    lines.append(f"\n{'─' * 50}")
    lines.append("  年度摘要")
    lines.append(f"{'─' * 50}")
    lines.append(f"- 主轴: {report['summary']['core_theme']}")
    lines.append(f"- 资源: {report['summary']['resource']}")
    lines.append(f"- 课题: {report['summary']['challenge']}")
    lines.append(f"- 指引: {report['summary']['guidance']}")

    if report.get("deep_analysis"):
        analysis = report["deep_analysis"]
        lines.append(f"\n{'─' * 50}")
        lines.append("  年度结构")
        lines.append(f"{'─' * 50}")
        for item in analysis["annual_structure"]:
            lines.append(f"- {item}")

        lines.append(f"\n{'─' * 50}")
        lines.append("  风险窗口")
        lines.append(f"{'─' * 50}")
        for item in analysis["risk_windows"]:
            lines.append(f"- {item['label']}: {item['detail']}")
        format_precision_section(lines, "年度解读校准", analysis["precision_profile"])
        insight = analysis["situational_insight"]
        lines.append(f"\n{'─' * 50}")
        lines.append("  年度情境直读")
        lines.append(f"{'─' * 50}")
        lines.append("- 你现在最可能承受的压力")
        for item in insight["current_pressure"]:
            lines.append(f"  {item}")
        lines.append("- 常见误读")
        for item in insight["common_misread"]:
            lines.append(f"  {item}")
        lines.append("- 最小动作")
        for item in insight["minimum_move"]:
            lines.append(f"  {item}")

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

    if report.get("deep_analysis"):
        strategy = report["deep_analysis"]["strategy_matrix"]
        lines.append(f"\n{'─' * 50}")
        lines.append("  策略配置")
        lines.append(f"{'─' * 50}")
        lines.append("- 聚焦")
        for item in strategy["focus"]:
            lines.append(f"  {item}")
        lines.append("- 盯防")
        for item in strategy["watch"]:
            lines.append(f"  {item}")
        lines.append("- 节奏")
        for item in strategy["timing"]:
            lines.append(f"  {item}")

    format_delivery_layers(lines, report["delivery_layers"])
    return "\n".join(lines) + "\n"


def _build_compatibility_report_from_result(result, style="basic"):
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
    report = {
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
    if normalized_style == "deep":
        report["deep_analysis"] = build_professional_compatibility_analysis(result)
    return report


def build_compatibility_report(kin_a, kin_b, style="basic"):
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
    lines.append(f"\n  输出风格: {report.get('style_label', '基础版')}")
    lines.append(f"  风格说明: {report.get('style_description', STYLE_CONFIG['basic']['description'])}")
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

    if report.get("deep_analysis"):
        analysis = report["deep_analysis"]
        lines.append(f"\n{'─' * 50}")
        lines.append("  关系结构")
        lines.append(f"{'─' * 50}")
        for item in analysis["relationship_structure"]:
            lines.append(f"- {item}")

        lines.append(f"\n{'─' * 50}")
        lines.append("  张力来源")
        lines.append(f"{'─' * 50}")
        for item in analysis["tension_matrix"]:
            lines.append(f"- {item['label']}: {item['detail']}")
        format_precision_section(lines, "关系解读校准", analysis["precision_profile"])
        insight = analysis["situational_insight"]
        lines.append(f"\n{'─' * 50}")
        lines.append("  关系情境直读")
        lines.append(f"{'─' * 50}")
        lines.append("- 你们现在最可能卡住的地方")
        for item in insight["current_knot"]:
            lines.append(f"  {item}")
        lines.append("- 关系低频表现")
        for item in insight["relationship_drift"]:
            lines.append(f"  {item}")
        lines.append("- 最小对齐动作")
        for item in insight["minimum_alignment"]:
            lines.append(f"  {item}")

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

    if report.get("deep_analysis"):
        model = report["deep_analysis"]["collaboration_model"]
        lines.append(f"\n{'─' * 50}")
        lines.append("  协作模型")
        lines.append(f"{'─' * 50}")
        lines.append("- 分工")
        for item in model["division"]:
            lines.append(f"  {item}")
        lines.append("- 沟通")
        for item in model["communication"]:
            lines.append(f"  {item}")
        lines.append("- 决策")
        for item in model["decision"]:
            lines.append(f"  {item}")

    format_delivery_layers(lines, report["delivery_layers"])
    return "\n".join(lines) + "\n"


def explain_position(role, detail, style="basic"):
    normalized_style = normalize_report_style(style)
    if normalized_style == "deep":
        parts = [DEEP_ROLE_GUIDANCE[role]]
        seal_hint = SEAL_GUIDANCE.get(detail["seal_name"])
        if seal_hint:
            parts.append(f"放在你身上，它通常会表现成这样：{seal_hint}")
        tone_hint = DEEP_TONE_GUIDANCE.get(detail["tone_name"])
        if tone_hint:
            parts.append(tone_hint)
        return " ".join(parts)

    parts = [ROLE_GUIDANCE[role]]
    seal_hint = SEAL_GUIDANCE.get(detail["seal_name"])
    if seal_hint:
        parts.append(seal_hint)
    tone_hint = TONE_GUIDANCE.get(detail["tone_name"])
    if tone_hint:
        parts.append(tone_hint)
    return " ".join(parts)


def build_personal_report(destiny, birth_date=None, style="basic"):
    normalized_style = normalize_report_style(style)
    style_info = style_meta(normalized_style)
    summary = stylize_summary(summarize_destiny(destiny), normalized_style)
    path = stylize_growth_path(build_growth_path(destiny), normalized_style)
    actions = stylize_action_guide(build_action_guide(destiny), normalized_style)
    positions = {
        role: {
            "name": f"{destiny[role]['tone_name']}{destiny[role]['seal_name']}",
            "keywords": destiny[role]["keywords"],
            "explanation": explain_position(role, destiny[role], normalized_style),
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
        "narrative": build_personal_narrative(destiny),
        "positions": positions,
        "growth_path": path,
        "action_guide": actions,
        "delivery_layers": build_personal_delivery_layers(destiny, normalized_style),
    }
    if normalized_style == "deep":
        report["deep_analysis"] = build_professional_personal_analysis(destiny)
    return report


def format_personal_report(report):
    lines = []
    lines.append("=" * 50)
    lines.append(f"  {report.get('scene_label', '玛雅天赋个人说明书')}")
    lines.append("=" * 50)
    if report["birth_date"]:
        lines.append(f"\n  出生日期: {report['birth_date']}")
    lines.append(f"  核心印记: {report['title']}")
    lines.append(f"  输出风格: {report.get('style_label', '基础版')}")
    lines.append(f"  风格说明: {report.get('style_description', STYLE_CONFIG['basic']['description'])}")

    lines.append(f"\n{'─' * 50}")
    lines.append("  整合解读")
    lines.append(f"{'─' * 50}")
    for para in report.get("narrative", []):
        lines.append(para)
        lines.append("")
    if lines and lines[-1] == "":
        lines.pop()

    if report.get("deep_analysis"):
        analysis = report["deep_analysis"]
        lines.append(f"\n{'─' * 50}")
        lines.append("  风险矩阵")
        lines.append(f"{'─' * 50}")
        for item in analysis["risk_matrix"]:
            lines.append(f"- {item['label']}: {item['detail']}")
        _precision = analysis["precision_profile"]
        lines.append(f"\n{'─' * 50}")
        lines.append("  解读校准")
        lines.append(f"{'─' * 50}")
        lines.append("- 触发条件")
        for item in _precision["trigger_map"]:
            lines.append(f"  {item['label']}: {item['detail']}")
        lines.append("- 误读风险")
        for item in _precision["misread_risks"]:
            lines.append(f"  {item['label']}: {item['detail']}")
        lines.append("- 验证问题")
        for item in _precision["validation_checks"]:
            lines.append(f"  {item}")
        lines.append("- 最小实验")
        for item in _precision["minimum_experiments"]:
            lines.append(f"  {item}")
        expression = analysis["expression_profile"]
        lines.append(f"\n{'─' * 50}")
        lines.append("  现实表达校准")
        lines.append(f"{'─' * 50}")
        lines.append(f"- 表达标签: {', '.join(expression['tags'])}")
        lines.append(f"- 适配场域: {', '.join(expression['fields'])}")
        lines.append("- 公开表达主线")
        for item in expression["summary"]:
            lines.append(f"  {item}")
        lines.append("- 五大位置的现实表达")
        for item in expression["roles"]:
            lines.append(f"  {item['label']} · {item['sign']}: {item['expression']}")
            lines.append(f"  风险: {item['risk']}")
        lines.append("- 现实验证问题")
        for item in expression["public_questions"]:
            lines.append(f"  {item}")

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

    if not report.get("deep_analysis"):
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

    if report.get("deep_analysis"):
        matrix = report["deep_analysis"]["application_matrix"]
        lines.append(f"\n{'─' * 50}")
        lines.append("  深度应用")
        lines.append(f"{'─' * 50}")
        lines.append("- 事业")
        for item in matrix["career"]:
            lines.append(f"  {item}")
        lines.append("- 关系")
        for item in matrix["relationship"]:
            lines.append(f"  {item}")
        lines.append("- 发展")
        for item in matrix["development"]:
            lines.append(f"  {item}")
        insight = report["deep_analysis"]["situational_insight"]
        lines.append(f"\n{'─' * 50}")
        lines.append("  情境直读")
        lines.append(f"{'─' * 50}")
        lines.append("- 你现在最可能的卡点")
        for item in insight["current_block"]:
            lines.append(f"  {item}")
        lines.append("- 最小动作")
        for item in insight["minimum_move"]:
            lines.append(f"  {item}")
        dialogue = report["deep_analysis"]["reflection_dialogue"]
        lines.append(f"\n{'─' * 50}")
        lines.append("  个人感悟对话入口")
        lines.append(f"{'─' * 50}")
        lines.append("- 你最近可能会有共鸣的地方")
        for item in dialogue["resonance_points"]:
            lines.append(f"  {item}")
        lines.append("- 如果现在就想继续聊，可以这样开口")
        for item in dialogue["next_opening"]:
            lines.append(f"  {item}")
    format_delivery_layers(lines, report["delivery_layers"])
    return "\n".join(lines) + "\n"


def format_compatibility(result):
    if "scene" in result and result.get("scene") == "compatibility":
        return format_compatibility_report(result)
    return format_compatibility_report(_build_compatibility_report_from_result(result))
