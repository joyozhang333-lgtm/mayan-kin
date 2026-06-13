"""Destiny presentation, growth/action guides and delivery layers (extracted from core.py)."""

from .constants import *  # noqa: F401,F403
from .styling import *  # noqa: F401,F403
from .calculations import *  # noqa: F401,F403
from .profiles import *  # noqa: F401,F403


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
    main_profile = precision_profile_for(main)
    support_profile = precision_profile_for(support)
    challenge_profile = precision_profile_for(challenge)
    occult_profile = precision_profile_for(occult)
    guide_profile = precision_profile_for(guide)
    support_marker = public_expression_for(support)

    summary = {
        "core_theme": f"{main['tone_name']}{main['seal_name']}的主轴不是泛泛的“{main['keywords']}”，而是用“{main_profile['tone']['task']}”把“{main_profile['seal']['high']}”活出来。",
        "strength": f"天然资源更接近{support['seal_name']}：适合借助{', '.join(support_marker['fields'][:2])}来放大主轴，关键是{support_profile['seal']['need']}。",
        "challenge": f"成长功课在{challenge['seal_name']}：常被“{challenge_profile['seal']['trigger']}”触发，需要避免滑向“{challenge_profile['seal']['low']}”。",
        "hidden_driver": f"更深层推动力来自{occult['seal_name']}：{occult_profile['seal']['high']}，并通过“{occult_profile['tone']['task']}”释放旧节奏。",
        "guidance": f"引导位落在{guide['seal_name']}，成熟方向是更稳定地做到：{guide_profile['seal']['high']}。",
    }
    return summary


def build_growth_path(destiny):
    support = destiny["support"]
    main = destiny["main"]
    challenge = destiny["challenge"]
    occult = destiny["occult"]
    guide = destiny["guide"]
    main_profile = precision_profile_for(main)
    support_profile = precision_profile_for(support)
    challenge_profile = precision_profile_for(challenge)
    occult_profile = precision_profile_for(occult)
    guide_profile = precision_profile_for(guide)

    return [
        {
            "stage": "隐藏推动",
            "sign": f"{occult['tone_name']}{occult['seal_name']}",
            "focus": f"先认识深层推动：{occult_profile['seal']['high']}。",
            "action": occult_profile["seal"]["question"],
        },
        {
            "stage": "支持位",
            "sign": f"{support['tone_name']}{support['seal_name']}",
            "focus": f"建立支持资源：{support_profile['seal']['need']}。",
            "action": support_profile["seal"]["question"],
        },
        {
            "stage": "主印记",
            "sign": f"{main['tone_name']}{main['seal_name']}",
            "focus": f"扎根核心天赋：{main_profile['seal']['high']}。",
            "action": main_profile["seal"]["question"],
        },
        {
            "stage": "挑战位",
            "sign": f"{challenge['tone_name']}{challenge['seal_name']}",
            "focus": f"整合成长功课：{challenge_profile['seal']['need']}。",
            "action": challenge_profile["seal"]["question"],
        },
        {
            "stage": "引导位",
            "sign": f"{guide['tone_name']}{guide['seal_name']}",
            "focus": f"活出成熟方向：{guide_profile['seal']['high']}。",
            "action": guide_profile["seal"]["question"],
        },
    ]


def build_action_guide(destiny):
    main = destiny["main"]
    support = destiny["support"]
    challenge = destiny["challenge"]
    occult = destiny["occult"]
    guide = destiny["guide"]
    main_profile = precision_profile_for(main)
    support_profile = precision_profile_for(support)
    challenge_profile = precision_profile_for(challenge)
    occult_profile = precision_profile_for(occult)
    guide_profile = precision_profile_for(guide)
    main_marker = public_expression_for(main)
    return {
        "career": [
            f"优先考虑{', '.join(main_marker['fields'][:3])}这类能发挥{main['seal_name']}主轴的场景。",
            f"把{support['seal_name']}对应的资源具体化：{support_profile['seal']['need']}。",
            f"交付时用{guide['seal_name']}校准品质：{guide_profile['seal']['high']}。",
        ],
        "relationship": [
            f"不要只因为有感觉就长期投入，也要看这段关系是否支持“{main_profile['seal']['high']}”。",
            f"当{challenge['seal_name']}式张力出现时，先做现实校准：{challenge_profile['seal']['need']}。",
            f"更深层的成熟，来自把{occult['seal_name']}的导航能力活出来：{occult_profile['seal']['question']}",
        ],
        "growth": [
            f"先承认核心频率是{main['seal_name']}：{main_profile['seal']['high']}，不要把它活成{main_profile['seal']['low']}。",
            f"每次卡住时，先回到这句判断：{main_profile['seal']['question']}",
            f"把{main['seal_name']}的觉察推进成{main_profile['tone']['task']}，而不是长期停在想法里。",
        ],
    }




def build_personal_delivery_layers(destiny, style="basic"):
    main = destiny["main"]
    support = destiny["support"]
    challenge = destiny["challenge"]
    occult = destiny["occult"]
    guide = destiny["guide"]
    main_profile = precision_profile_for(main)
    support_profile = precision_profile_for(support)
    challenge_profile = precision_profile_for(challenge)
    occult_profile = precision_profile_for(occult)
    guide_profile = precision_profile_for(guide)
    main_marker = public_expression_for(main)
    layers = {
        "consultation": {
            "focus": f"围绕{main['seal_name']}的主轴、{support['seal_name']}的资源和{challenge['seal_name']}的误读风险来提问。",
            "questions": [
                main_profile["seal"]["question"],
                support_profile["seal"]["question"],
                challenge_profile["seal"]["question"],
            ],
            "decision_checks": [
                f"我有没有先做到：{main_profile['seal']['need']}？",
                f"我有没有把{support['seal_name']}的资源落成现实步骤：{support_profile['seal']['need']}？",
                f"我现在是否正在靠近{guide['seal_name']}的成熟表达：{guide_profile['seal']['high']}？",
            ],
        },
        "content": {
            "focus": f"适合做成{main_marker['fields'][0]}、成长路线图、选择清单和落地实验。",
            "angles": [
                build_content_angle_for_main(main, main_profile),
                f"《把{support['seal_name']}的资源落成现实承载：从看见到下一步》",
                build_content_angle_for_challenge(challenge, challenge_profile),
                f"《用{occult['seal_name']}做复盘：什么时候该跟随，什么时候该释放》",
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
                build_ai_instruction_for_main(main, main_profile),
                f"输出时优先围绕{main['seal_name']}的主轴、{challenge['seal_name']}的功课和{guide['seal_name']}的成长方向。",
                "如果信息不足，先提出 1 到 3 个关键追问，不要直接泛泛而谈。",
            ],
            "prompts": [
                f"请先判断我现在是在高频使用{main['seal_name']}，还是掉进了它的低频。",
                f"请把{support['seal_name']}的资源拆成我接下来一周能执行的三个动作。",
                f"请帮我区分：这是{challenge['seal_name']}带来的真实感受，还是投射和理想化。",
            ],
        },
    }
    return stylize_delivery_layers(layers, style)


def build_yearly_delivery_layers(natal_destiny, annual_destiny, interaction, style="basic"):
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


def build_compatibility_delivery_layers(result, style="basic"):
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
        lines.append(f"- {section['focus']}")
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


def format_precision_section(lines, title, precision):
    lines.append(f"\n{'─' * 50}")
    lines.append(f"  {title}")
    lines.append(f"{'─' * 50}")
    lines.append("- 结构判读")
    for item in precision["axis_reading"]:
        lines.append(f"  {item}")
    lines.append("- 触发条件")
    for item in precision["trigger_map"]:
        lines.append(f"  {item['label']}: {item['detail']}")
    lines.append("- 误读风险")
    for item in precision["misread_risks"]:
        lines.append(f"  {item['label']}: {item['detail']}")
    lines.append("- 验证问题")
    for item in precision["validation_checks"]:
        lines.append(f"  {item}")
    lines.append("- 最小实验")
    for item in precision["minimum_experiments"]:
        lines.append(f"  {item}")


