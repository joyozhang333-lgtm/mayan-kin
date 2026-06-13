"""Precision and public-expression profiles (extracted from core.py)."""

from .constants import *  # noqa: F401,F403
from .calculations import *  # noqa: F401,F403


def precision_profile_for(detail):
    seal_profile = SEAL_PRECISION.get(detail["seal_name"], {
        "high": f"成熟表达 {detail['keywords']}",
        "low": f"把 {detail['keywords']} 活成失衡或代偿",
        "trigger": "相关主题被现实反复触发时",
        "need": "先确认现实条件、边界和承接方式",
        "question": "这个表达是在增加生命力，还是在重复旧模式？",
    })
    tone_profile = TONE_PRECISION.get(detail["tone_name"], {
        "task": f"以 {detail['tone_name']} 的方式推进主题",
        "shadow": "行动节奏和内在主题没有对齐",
        "check": "这个动作是否让主题更清楚、更可承接？",
    })
    return {
        "seal": seal_profile,
        "tone": tone_profile,
    }


def public_expression_for(detail):
    seal_profile = SEAL_PUBLIC_EXPRESSION.get(detail["seal_name"], {
        "tags": ["self_expression"],
        "fields": ["个人表达"],
        "expression": f"适合把 {detail['keywords']} 转化成可被看见的现实表达。",
        "risk": "容易停留在抽象感受，没有形成可验证的作品或行动。",
    })
    tone_tags = TONE_PUBLIC_EXPRESSION.get(detail["tone_name"], [])
    tags = sorted(set(seal_profile["tags"] + tone_tags))
    return {
        "tags": tags,
        "fields": seal_profile["fields"],
        "expression": seal_profile["expression"],
        "risk": seal_profile["risk"],
    }


def build_main_discernment_line(main, main_profile):
    if main["seal_name"] == "黄种子":
        return (
            f"{main['seal_name']} 的判断重点是“什么值得长期培育”。"
            "所以他/她不适合什么都试一点，而是要先分辨种子、土壤、节奏和目标是否匹配。"
        )
    if main["seal_name"] == "蓝手":
        return (
            f"{main['seal_name']} 的判断重点是“哪些事该由我的手完成，哪些要归还给对方”。"
            "所以他/她不适合把所有问题都接过来修，而是要先分辨责任、边界、节奏和可完成度。"
        )
    return (
        f"{main['seal_name']} 的判断重点是“{main_profile['seal']['need']}”。"
        "所以他/她不适合只凭惯性投入，而是要先分辨对象、边界、节奏和现实条件是否匹配。"
    )


def build_main_current_block_line(main, main_profile):
    if main["seal_name"] == "黄种子":
        return (
            f"最可能卡住的点，是“{main_profile['seal']['trigger']}”："
            "已经看见潜能或问题，却还没有决定这颗种子到底要不要继续培育。"
        )
    if main["seal_name"] == "蓝手":
        return (
            f"最可能卡住的点，是“{main_profile['seal']['trigger']}”："
            "已经看见哪里需要被处理，却还没有确认这是不是自己的责任、该完成到什么程度。"
        )
    return (
        f"最可能卡住的点，是“{main_profile['seal']['trigger']}”："
        "已经感到主题被触发，却还没有把它翻译成清楚的判断、边界和下一步动作。"
    )


def build_main_resonance_line(main, main_profile):
    if main["seal_name"] == "黄种子":
        return f"如果他/她最近觉得方向很多但都不够笃定，通常是 {main['seal_name']} 在提醒：先选种子，不要什么都培育。"
    if main["seal_name"] == "蓝手":
        return f"如果他/她最近总被问题、求助或收尾任务拉住，通常是 {main['seal_name']} 在提醒：先分清哪一件事真的该由自己完成。"
    return f"如果他/她最近反复遇到“{main_profile['seal']['trigger']}”，通常是 {main['seal_name']} 在提醒：{main_profile['seal']['need']}。"


def build_content_angle_for_main(main, main_profile):
    if main["seal_name"] == "黄种子":
        return f"《如何判断一颗种子值不值得长期培育：{main['seal_name']}使用手册》"
    if main["seal_name"] == "蓝手":
        return f"《如何判断一件事该不该由我完成：{main['seal_name']}使用手册》"
    return f"《如何把{main['seal_name']}天赋从感受变成行动：个人使用手册》"


def build_ai_instruction_for_main(main, main_profile):
    if main["seal_name"] == "黄种子":
        return f"先判断这是不是{main['seal_name']}的选择问题：种子、土壤、节奏和目标是否匹配。"
    if main["seal_name"] == "蓝手":
        return f"先判断这是不是{main['seal_name']}的介入问题：哪些是我的手该完成的，哪些需要归还给对方。"
    return f"先判断这是不是{main['seal_name']}的主轴问题：{main_profile['seal']['need']}。"


def build_content_angle_for_challenge(challenge, challenge_profile):
    if challenge["seal_name"] == "红地球":
        return f"《{challenge['seal_name']}的误区：同步性、现实反馈和节奏校准》"
    if challenge["seal_name"] == "白巫师":
        return f"《{challenge['seal_name']}的误区：感受、投射和现实校准》"
    return f"《{challenge['seal_name']}的误区：{challenge_profile['seal']['low']}》"


def weighted_expression_signature(roles):
    tag_scores = {}
    field_scores = {}
    for item in roles:
        weight = EXPRESSION_ROLE_WEIGHTS.get(item["role"], 0.5)
        for tag in item["tags"]:
            tag_scores[tag] = round(tag_scores.get(tag, 0.0) + weight, 4)
        for field in item["fields"]:
            field_scores[field] = round(field_scores.get(field, 0.0) + weight, 4)

    weighted_tags = [
        {"tag": tag, "weight": score}
        for tag, score in sorted(tag_scores.items(), key=lambda pair: (-pair[1], pair[0]))
    ]
    weighted_fields = [
        {"field": field, "weight": score}
        for field, score in sorted(field_scores.items(), key=lambda pair: (-pair[1], pair[0]))
    ]
    return {
        "protocol": "expression_signature_v1",
        "role_weights": EXPRESSION_ROLE_WEIGHTS,
        "primary_tags": [item["tag"] for item in weighted_tags[:18]],
        "primary_fields": [item["field"] for item in weighted_fields[:8]],
        "weighted_tags": weighted_tags,
        "weighted_fields": weighted_fields,
        "scoring_note": "Use weighted top tags for reproducible public-expression evaluation; do not treat this as proof of fate.",
    }


def build_expression_profile(destiny):
    role_labels = {
        "main": "主印记",
        "support": "支持位",
        "guide": "引导位",
        "challenge": "挑战位",
        "occult": "隐藏推动",
    }
    roles = []
    all_tags = set()
    field_rank = []
    for role in ("main", "support", "guide", "challenge", "occult"):
        detail = destiny[role]
        marker = public_expression_for(detail)
        all_tags.update(marker["tags"])
        field_rank.extend(marker["fields"])
        roles.append({
            "role": role,
            "label": role_labels[role],
            "sign": f"{detail['tone_name']}{detail['seal_name']}",
            "tags": marker["tags"],
            "fields": marker["fields"],
            "expression": marker["expression"],
            "risk": marker["risk"],
        })

    unique_fields = []
    for field in field_rank:
        if field not in unique_fields:
            unique_fields.append(field)

    main = destiny["main"]
    support = destiny["support"]
    challenge = destiny["challenge"]
    occult = destiny["occult"]
    main_marker = public_expression_for(main)
    support_marker = public_expression_for(support)
    challenge_marker = public_expression_for(challenge)
    occult_marker = public_expression_for(occult)

    return {
        "tags": sorted(all_tags),
        "fields": unique_fields[:8],
        "roles": roles,
        "evaluation_signature": weighted_expression_signature(roles),
        "summary": [
            f"公开表达主轴更靠近 {main['tone_name']}{main['seal_name']}：{main_marker['expression']}",
            f"可被放大的支持条件来自 {support['seal_name']}：优先建设 {', '.join(support_marker['fields'][:2])}。",
            f"最容易被公众误读或卡住的地方在 {challenge['seal_name']}：{challenge_marker['risk']}",
            f"长期影响力的暗线来自 {occult['seal_name']}：它会把个人经验推向更深层的选择和公共表达。",
        ],
        "public_questions": [
            f"我现在的作品、事业或公开表达，是否真的承载了 {main_marker['fields'][0]}？",
            f"我有没有先建设 {support_marker['fields'][0]}，再去放大影响力？",
            f"当 {challenge['seal_name']} 的低频出现时，我是在升级表达，还是在重复 {challenge_marker['risk']}？",
            f"我的长期影响力，是不是正在把 {occult_marker['fields'][0]} 这条暗线活出来？",
        ],
    }


def build_precision_profile(destiny):
    main = destiny["main"]
    support = destiny["support"]
    guide = destiny["guide"]
    challenge = destiny["challenge"]
    occult = destiny["occult"]

    main_profile = precision_profile_for(main)
    support_profile = precision_profile_for(support)
    guide_profile = precision_profile_for(guide)
    challenge_profile = precision_profile_for(challenge)
    occult_profile = precision_profile_for(occult)

    return {
        "axis_reading": [
            f"主轴精度: {main['tone_name']}{main['seal_name']} 不是泛泛的“{main['keywords']}”，更准确地说，是用“{main_profile['tone']['task']}”的方式，把“{main_profile['seal']['high']}”活出来。",
            f"资源精度: {support['tone_name']}{support['seal_name']} 不是辅助装饰，而是你的稳定条件。它要求你先做到：{support_profile['seal']['need']}。",
            f"挑战精度: {challenge['tone_name']}{challenge['seal_name']} 通常在“{challenge_profile['seal']['trigger']}”被触发；真正要分辨的是它在训练升级，还是正在放大“{challenge_profile['seal']['low']}”。",
            f"隐藏推动精度: {occult['tone_name']}{occult['seal_name']} 会在关键处把你从感受推向选择。它问的不是你懂不懂，而是：{occult_profile['seal']['question']}",
            f"引导精度: {guide['tone_name']}{guide['seal_name']} 指向成熟版本的你：能更稳定地“{guide_profile['seal']['high']}”，并通过“{guide_profile['tone']['task']}”把它落地。",
        ],
        "trigger_map": [
            {
                "label": "主轴触发",
                "detail": f"当{main_profile['seal']['trigger']}，你的第一反应通常不是马上行动，而是先感到哪里不对。精准用法是先命名堵点，再决定是否投入。",
            },
            {
                "label": "资源触发",
                "detail": f"当{support_profile['seal']['trigger']}，你需要主动建设支持系统。否则资源位会从支持滑向低频：{support_profile['seal']['low']}。",
            },
            {
                "label": "挑战触发",
                "detail": f"当{challenge_profile['seal']['trigger']}，不要只问能不能扛住，要问这次压力是在训练“{challenge_profile['tone']['task']}”，还是在重复旧消耗。",
            },
            {
                "label": "隐藏推动触发",
                "detail": f"当{occult_profile['seal']['trigger']}，潜意识会推你做选择。精准用法是把内在推动写成一句判断，而不是继续让它停在感受里。",
            },
        ],
        "misread_risks": [
            {
                "label": "把天赋误读成性格",
                "detail": f"{main['seal_name']} 的重点不是“我就是这样的人”，而是识别你何时处在“{main_profile['seal']['high']}”，何时掉进“{main_profile['seal']['low']}”。",
            },
            {
                "label": "把挑战误读成失败",
                "detail": f"{challenge['seal_name']} 出现时不一定说明你走错了，也可能说明系统正在要求升级。关键是看你是否能从“{challenge_profile['tone']['shadow']}”回到“{challenge_profile['tone']['task']}”。",
            },
            {
                "label": "把支持误读成依赖",
                "detail": f"{support['seal_name']} 不是让你依附外部环境，而是提醒你：你的发挥需要合适配置。配置不对时，先调整资源、边界和承接方式，不要直接否定能力。",
            },
            {
                "label": "把引导误读成标准答案",
                "detail": f"{guide['seal_name']} 不是逼你变成某种模板，而是作为校准方向：当你越来越能“{guide_profile['seal']['high']}”，说明天赋正在进入成熟表达。",
            },
        ],
        "validation_checks": [
            main_profile["seal"]["question"],
            support_profile["seal"]["question"],
            challenge_profile["seal"]["question"],
            occult_profile["seal"]["question"],
            guide_profile["tone"]["check"],
        ],
        "minimum_experiments": [
            f"连续 7 天记录一次“{main['seal_name']} 信号”：今天哪里出现了 {main_profile['seal']['trigger']}？我命名了哪个真实堵点？",
            f"遇到 {challenge['seal_name']} 型压力时，不急着下结论，先写三列：事实是什么、我感受到什么、我准备做的最小边界是什么。",
            f"为 {support['seal_name']} 建一个现实承载动作：明确一个能支持你稳定发挥的人、环境、流程或固定练习。",
            f"每周用 {occult['seal_name']} 做一次选择复盘：这周哪件事我其实已经知道答案，但还没有把感受推进成决定？",
            f"把 {guide['seal_name']} 当成校准方向，选择一个小场景练习“{guide_profile['tone']['task']}”，并观察现实反馈。",
        ],
    }


def build_yearly_precision_profile(natal_destiny, annual_destiny, interaction, year):
    natal = natal_destiny["main"]
    annual = annual_destiny["main"]
    support = annual_destiny["support"]
    challenge = annual_destiny["challenge"]
    guide = annual_destiny["guide"]

    natal_profile = precision_profile_for(natal)
    annual_profile = precision_profile_for(annual)
    support_profile = precision_profile_for(support)
    challenge_profile = precision_profile_for(challenge)
    guide_profile = precision_profile_for(guide)

    return {
        "axis_reading": [
            f"{year} 年主轴精度: {annual['tone_name']}{annual['seal_name']} 不是简单的年度标签，而是用“{annual_profile['tone']['task']}”去承接“{annual_profile['seal']['high']}”。",
            f"本命互动精度: 本命 {natal['tone_name']}{natal['seal_name']} 的惯性是“{natal_profile['seal']['high']}”；今年要看它与流年主轴是互相支持，还是需要先调频。",
            f"资源精度: 年度支持位 {support['tone_name']}{support['seal_name']} 要求你先做到：{support_profile['seal']['need']}。资源没搭好时，不要把压力直接归因成自己不行。",
            f"挑战精度: 年度挑战位 {challenge['tone_name']}{challenge['seal_name']} 会在“{challenge_profile['seal']['trigger']}”时放大；它最容易被误读成“{challenge_profile['seal']['low']}”。",
            f"引导精度: 年度引导位 {guide['tone_name']}{guide['seal_name']} 指向“{guide_profile['seal']['high']}”，但必须通过“{guide_profile['tone']['task']}”进入现实节奏。",
        ],
        "trigger_map": [
            {
                "label": "年度主轴触发",
                "detail": f"当{annual_profile['seal']['trigger']}，这一年会要求你回到年度主轴，而不是继续沿用旧惯性。",
            },
            {
                "label": "本命惯性触发",
                "detail": f"当压力变大时，本命 {natal['seal_name']} 可能会先按熟悉方式反应。精准用法是先问：{natal_profile['tone']['check']}",
            },
            {
                "label": "资源条件触发",
                "detail": f"当{support_profile['seal']['trigger']}，要优先补资源配置。否则年度推进会滑向：{support_profile['seal']['low']}。",
            },
            {
                "label": "年度挑战触发",
                "detail": f"当{challenge_profile['seal']['trigger']}，先做事实校验和节奏校验，再决定是否投入更多资源。",
            },
        ],
        "misread_risks": [
            {
                "label": "把年度气候误读成命运定论",
                "detail": f"{year} 年的 {annual['seal_name']} 是阶段气候，不是终身定义。它提醒你今年优先练“{annual_profile['seal']['high']}”。",
            },
            {
                "label": "把摩擦误读成方向错误",
                "detail": f"{interaction['tone_relation']} 带来的摩擦，很多时候先说明节奏需要调，不一定说明年度方向要推翻。",
            },
            {
                "label": "把机会误读成必须抓住",
                "detail": f"{annual['seal_name']} 年的机会要看是否能被“{support_profile['seal']['need']}”承载；不能承载的机会也会变成消耗。",
            },
            {
                "label": "把挑战误读成个人失败",
                "detail": f"{challenge['seal_name']} 的出现更像年度训练题。关键不是有没有压力，而是能否从“{challenge_profile['tone']['shadow']}”回到“{challenge_profile['tone']['task']}”。",
            },
        ],
        "validation_checks": [
            annual_profile["seal"]["question"],
            annual_profile["tone"]["check"],
            support_profile["seal"]["question"],
            challenge_profile["seal"]["question"],
            guide_profile["tone"]["check"],
        ],
        "minimum_experiments": [
            f"为 {year} 年只选 1 到 3 个年度主轴目标，每个目标都写清它如何服务 {annual['seal_name']} 的高频表达。",
            f"每月做一次本命与流年复盘：我是按本命 {natal['seal_name']} 的惯性在动，还是按年度 {annual['seal_name']} 的主轴在配置资源？",
            f"遇到 {challenge['seal_name']} 型阻力时，先暂停加码，做一次事实、节奏、资源三项校验。",
            f"给 {support['seal_name']} 建一个年度支持动作：固定复盘、固定合作人、固定环境，或固定资源池。",
            f"用 {guide['seal_name']} 做季度校准：这三个月的选择，是否正在靠近“{guide_profile['seal']['high']}”？",
        ],
    }


def build_compatibility_precision_profile(result):
    person_a = result["person_a"]["main"]
    person_b = result["person_b"]["main"]
    combined = result["combined_destiny"]["main"]
    combined_support = result["combined_destiny"]["support"]
    combined_challenge = result["combined_destiny"]["challenge"]

    a_profile = precision_profile_for(person_a)
    b_profile = precision_profile_for(person_b)
    combined_profile = precision_profile_for(combined)
    support_profile = precision_profile_for(combined_support)
    challenge_profile = precision_profile_for(combined_challenge)

    return {
        "axis_reading": [
            f"A 的默认表达更接近 {person_a['tone_name']}{person_a['seal_name']}：用“{a_profile['tone']['task']}”去表达“{a_profile['seal']['high']}”。",
            f"B 的默认表达更接近 {person_b['tone_name']}{person_b['seal_name']}：用“{b_profile['tone']['task']}”去表达“{b_profile['seal']['high']}”。",
            f"合盘主轴 {combined['tone_name']}{combined['seal_name']} 不是两个人的平均值，而是这段关系真正要服务的共同主题：{combined_profile['seal']['high']}。",
            f"合盘支持位 {combined_support['seal_name']} 决定这段关系能不能稳定承载，它要求：{support_profile['seal']['need']}。",
            f"合盘挑战位 {combined_challenge['seal_name']} 会在“{challenge_profile['seal']['trigger']}”时暴露问题，不能只用感情浓度或合作热情盖过去。",
        ],
        "trigger_map": [
            {
                "label": "A 的触发点",
                "detail": f"当{a_profile['seal']['trigger']}，A 容易先按自己的默认节奏反应。关系里需要把它翻译成明确请求，而不是让 B 猜。",
            },
            {
                "label": "B 的触发点",
                "detail": f"当{b_profile['seal']['trigger']}，B 容易先按自己的默认节奏反应。关系里需要说清这是需要支持、边界，还是需要空间。",
            },
            {
                "label": "合盘主轴触发",
                "detail": f"当关系要共同处理 {combined['keywords']} 时，真正要对齐的是目标、角色和节奏，不只是情绪感受。",
            },
            {
                "label": "合盘挑战触发",
                "detail": f"当{challenge_profile['seal']['trigger']}，这段关系要先重建边界和分工，再谈继续升温或继续投入。",
            },
        ],
        "misread_risks": [
            {
                "label": "把差异误读成不合",
                "detail": f"A 的 {person_a['seal_name']} 与 B 的 {person_b['seal_name']} 不同，不等于不合；关键是能否把差异翻译成分工。",
            },
            {
                "label": "把合盘吸引误读成长期条件",
                "detail": f"合盘 {combined['seal_name']} 有共同主题，但长期条件还要看 {combined_support['seal_name']} 的支持系统是否真实存在。",
            },
            {
                "label": "把冲突误读成谁错了",
                "detail": f"{result['tone_relation']} 的错位更像节奏模型不同。先翻译节奏，再讨论对错。",
            },
            {
                "label": "把包容误读成无边界",
                "detail": f"合盘挑战 {combined_challenge['seal_name']} 出现时，越想长期走下去，越要清楚边界、责任和最小对齐动作。",
            },
        ],
        "validation_checks": [
            a_profile["seal"]["question"],
            b_profile["seal"]["question"],
            combined_profile["seal"]["question"],
            support_profile["seal"]["question"],
            challenge_profile["seal"]["question"],
        ],
        "minimum_experiments": [
            "做一次 30 分钟关系对齐：每个人只说事实、需要和下一步，不评价对方人格。",
            f"把合盘 {combined['seal_name']} 写成一个共同目标：这段关系如果高频运作，现实中会产出什么？",
            f"为合盘支持位 {combined_support['seal_name']} 设计一个固定支持动作，例如分工表、沟通节点或复盘机制。",
            f"当 {combined_challenge['seal_name']} 型张力出现时，只处理一个最小边界，不一次性清算所有旧账。",
            "连续两周记录一次冲突前兆：到底是目标没对齐、节奏没对齐、边界没对齐，还是责任没对齐？",
        ],
    }


