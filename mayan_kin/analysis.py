"""Personal and professional analysis blocks (extracted from core.py)."""

from .constants import *  # noqa: F401,F403
from .calculations import *  # noqa: F401,F403
from .profiles import *  # noqa: F401,F403


def build_personal_structural_analysis(destiny):
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
    support_marker = public_expression_for(support)
    guide_marker = public_expression_for(guide)
    return [
        f"这张盘的核心，是用 {main['tone_name']} 的方式把 {main['seal_name']} 活出来：不是泛泛追求“{main['keywords']}”，而是把“{main_profile['seal']['high']}”推进成可以服务现实的行动。",
        build_main_discernment_line(main, main_profile),
        f"{support['seal_name']} 是稳定资源，适配场域更靠近 {', '.join(support_marker['fields'][:3])}。当他/她能做到“{support_profile['seal']['need']}”，主轴会明显更容易落地。",
        f"{challenge['seal_name']} 是最容易失真的功课，常在“{challenge_profile['seal']['trigger']}”被触发。低频不是没能力，而是容易滑向“{challenge_profile['seal']['low']}”。",
        f"成熟方向由 {guide['seal_name']} 引导，适合把成果做成 {', '.join(guide_marker['fields'][:2])} 这类更有品质、更可见的表达；隐藏推动 {occult['seal_name']} 则不断要求他/她回应现实反馈：{occult_profile['seal']['question']}",
    ]


def build_personal_risk_matrix(destiny):
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
    return [
        {
            "label": "高频优势",
            "detail": f"他/她最容易在需要“{main_profile['seal']['high']}”的场景中发挥价值，并通过“{main_profile['tone']['task']}”把觉察转成具体贡献。",
        },
        {
            "label": "主要风险",
            "detail": f"当 {main['seal_name']} 低频时，会从天赋滑向“{main_profile['seal']['low']}”；当 {challenge['seal_name']} 被触发时，又容易叠加“{challenge_profile['seal']['low']}”。",
        },
        {
            "label": "资源条件",
            "detail": f"{support['seal_name']} 提醒他/她：资源不是抽象支持，而是要具体做到“{support_profile['seal']['need']}”。否则支持位会变成“{support_profile['seal']['low']}”。",
        },
        {
            "label": "升级方向",
            "detail": f"{guide['seal_name']} 要求成果更有品质和形式感：{guide_profile['seal']['high']}。{occult['seal_name']} 则要求他/她根据现实同步不断释放旧节奏：{occult_profile['tone']['task']}。",
        },
    ]


def build_personal_application_matrix(destiny):
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
    support_marker = public_expression_for(support)
    guide_marker = public_expression_for(guide)
    return {
        "career": [
            f"职业定位上，优先选择 {', '.join(main_marker['fields'][:3])} 这类能把主轴转成稳定成果的场景，而不是只要求短期反应和机械执行的环境。",
            f"工作方法上，要把 {support['seal_name']} 的视角落成流程：{support_profile['seal']['need']}，避免只停在“我看见了问题”。",
            f"交付标准上，{guide['seal_name']} 要求他/她把结果做得更清楚、更有品质：{guide_profile['seal']['high']}。",
        ],
        "relationship": [
            f"关系里要看对方是否支持他/她“{main_profile['seal']['high']}”，而不是只看感觉强不强或吸引力大不大。",
            f"当 {challenge['seal_name']} 被触发时，先做现实校准：{challenge_profile['seal']['need']}。不要只靠沉浸感、理想化或直觉维持关系。",
            f"{occult['seal_name']} 的课题要求他/她尊重节奏和现实反馈；不顺的关系或合作，需要及时导航，而不是一直解释成缘分或考验。",
        ],
        "development": [
            f"个人发展上，要把 {main['seal_name']} 训练成判断系统：先确认什么真实属于自己，再决定投入多少、做到哪里。",
            f"他/她的成长不是更用力，而是更会分辨：{main_profile['seal']['question']}",
            f"当能稳定调用 {support['seal_name']} 的资源、校准 {challenge['seal_name']} 的失真，并兑现 {guide['seal_name']} 的成熟表达时，这张盘会进入高水平发挥。",
        ],
    }


def build_personal_situational_insight(destiny):
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
    return {
        "current_block": [
            build_main_current_block_line(main, main_profile),
            f"{support['seal_name']} 会提供稳定资源，但低频时容易变成“{support_profile['seal']['low']}”，于是资源没有落成具体承接。",
            f"{challenge['seal_name']} 会在“{challenge_profile['seal']['trigger']}”放大张力，真正要分辨的是：{challenge_profile['seal']['question']}",
        ],
        "low_frequency": [
            f"低频时，{main['seal_name']} 会表现成：{main_profile['seal']['low']}。",
            f"{support['seal_name']} 低频时会表现成：{support_profile['seal']['low']}。",
            f"{challenge['seal_name']} 低频时会表现成：{challenge_profile['seal']['low']}。",
        ],
        "minimum_move": [
            f"最小动作不是继续分析所有可能性，而是先完成一步：{main_profile['seal']['need']}。",
            f"把 {support['seal_name']} 的资源拆成一个现实动作：{support_profile['seal']['need']}。",
            f"遇到 {challenge['seal_name']} 型压力时，先暂停判断，把事实、感受、边界分开写清楚，再决定是否投入。",
        ],
        "reflection_dialogue": {
            "resonance_points": [
                build_main_resonance_line(main, main_profile),
                f"如果他/她明明有资源却迟迟没有推进，通常是 {support['seal_name']} 还没有被拆成现实承载动作。",
                f"如果“{challenge_profile['seal']['trigger']}”反复出现，{challenge['seal_name']} 会提醒：{challenge_profile['seal']['need']}。",
            ],
            "conversation_questions": [
                f"{main_profile['seal']['question']}",
                f"{support_profile['seal']['question']}",
                f"{challenge_profile['seal']['question']}",
            ],
            "next_opening": [
                "可以从一个具体场景开始：他/她最近最想处理、完成或推进的是什么？",
                "然后看现实配置：这件事有没有资源、边界、节奏和反馈？",
                f"最后用 {guide['seal_name']} 校准品质：如果它真的要进入成熟表达，最小但更优雅的下一步是什么？",
            ],
        },
    }


def build_professional_personal_analysis(destiny):
    situational = build_personal_situational_insight(destiny)
    return {
        "structural_analysis": build_personal_structural_analysis(destiny),
        "precision_profile": build_precision_profile(destiny),
        "expression_profile": build_expression_profile(destiny),
        "risk_matrix": build_personal_risk_matrix(destiny),
        "application_matrix": build_personal_application_matrix(destiny),
        "situational_insight": {
            "current_block": situational["current_block"],
            "low_frequency": situational["low_frequency"],
            "minimum_move": situational["minimum_move"],
        },
        "reflection_dialogue": situational["reflection_dialogue"],
    }


def build_professional_compatibility_analysis(result):
    person_a = result["person_a"]["main"]
    person_b = result["person_b"]["main"]
    combined = result["combined_destiny"]["main"]
    combined_challenge = result["combined_destiny"]["challenge"]

    return {
        "relationship_structure": [
            f"A 以 {person_a['tone_name']}{person_a['seal_name']} 运作，B 以 {person_b['tone_name']}{person_b['seal_name']} 运作，说明双方天然带入关系的不是同一种驱动力，合作前提不是相同，而是是否能被正确翻译。",
            f"合盘主轴落在 {combined['tone_name']}{combined['seal_name']}，所以这段关系真正要服务的主题是 {combined['keywords']}，不能只停留在感觉投射，还要看这条主轴能否落地。",
            f"颜色关系显示为 {result['color_relation']}，这决定了你们更像互补型、同频型还是彼此拉扯型搭档；颜色关系往往比单点感觉更能解释长期稳定度。",
            f"调性关系是 {result['tone_relation']}，这通常不只是沟通快慢问题，而是双方在推进、承接、反馈和修正上的节奏模型是否匹配。",
        ],
        "tension_matrix": [
            {
                "label": "主要张力源",
                "detail": "合盘里最常见的冲突，不是因为谁更坏，而是双方默认的表达方式、承压方式和决策顺序不同。",
            },
            {
                "label": "结构风险",
                "detail": f"如果 {result['tone_relation']} 长期没有被翻译成明确节奏，关系会从互相照见滑向互相放大卡点。",
            },
            {
                "label": "优势条件",
                "detail": f"当 {result['color_relation']} 被高质量使用时，双方其实可以形成天然分工：一方负责推动，一方负责校准，或者一方负责扩张，一方负责稳定。",
            },
            {
                "label": "关系边界",
                "detail": f"合盘 {combined['seal_name']} 的成长要求不是无限包容，而是先对齐目标、责任、边界和节奏，再谈情感浓度。",
            },
        ],
        "precision_profile": build_compatibility_precision_profile(result),
        "collaboration_model": {
            "division": [
                "先明确谁更适合发起、谁更适合承接、谁更适合校准，而不是默认两个人必须用同一种方式做事。",
                f"如果 A 的强项更靠近 {person_a['keywords']}，B 的强项更靠近 {person_b['keywords']}，分工就应该顺着差异设计，而不是压成一致。",
                f"合盘 {combined['seal_name']} 更像在提醒：真正可持续的关系，一定有明确角色，不靠长期猜测维持。",
            ],
            "communication": [
                "沟通上要优先处理节奏错位，而不是先争对错；很多冲突本质上是推进顺序不同。",
                "把情绪化表达翻译成任务、期待、边界和可执行动作，关系才会从消耗型进入协作型。",
                "每次卡住时先问：我们现在卡的是目标不一致，还是表达方式不兼容，还是责任没有落地。",
            ],
            "decision": [
                "是否继续投入，不只看感觉深不深，还要看这段关系能不能提升双方的稳定度、清晰度和执行质量。",
                "如果一段关系长期只剩下拉扯感、猜测感和代偿感，就算有合盘吸引，也不代表它适合长期配置。",
                "专业判断的关键不是这段关系有没有缘分，而是它有没有结构条件支撑长期成长。",
            ],
        },
        "situational_insight": {
            "current_knot": [
                "你们现在最可能卡住的，不是爱不爱或值不值得，而是关系里有些东西已经不顺了，却还没有被说清楚。",
                f"{result['tone_relation']} 说明这段关系很容易卡在节奏错位：一方觉得已经在推进，另一方却觉得自己还没准备好或还没被听见。",
                f"如果 {combined_challenge['seal_name']} 的课题已经开始反复出现，那当前要处理的通常不是感觉本身，而是边界、分工和现实承接能力。",
            ],
            "relationship_drift": [
                "低频时，这段关系容易从连接滑向猜测，从合作滑向代偿，从互相看见滑向互相消耗。",
                "最常见的表现不是一次大冲突，而是很多没说开的不舒服慢慢堆起来，最后谁都觉得累。",
                "如果你们总在讨论感受，却迟迟不处理目标、责任、节奏和决定方式，关系就会一直原地打转。",
            ],
            "minimum_alignment": [
                "先不要急着证明谁更懂这段关系，先把一件最现实的事讲清楚：你们现在到底卡在目标、边界、节奏，还是责任。",
                "先做一个最小对齐动作，比如重新确认分工、设一个明确的沟通节点，或把含糊的期待翻译成一句可执行的话。",
                "如果连最小对齐都做不到，那你们要面对的就不是如何继续升温，而是这段关系有没有长期配置条件。",
            ],
        },
    }


def build_professional_yearly_analysis(natal_destiny, annual_destiny, interaction, year):
    natal = natal_destiny["main"]
    annual = annual_destiny["main"]
    support = annual_destiny["support"]
    challenge = annual_destiny["challenge"]
    guide = annual_destiny["guide"]

    return {
        "annual_structure": [
            f"{year} 年主轴由 {annual['tone_name']}{annual['seal_name']} 构成，意味着年度议题首先落在 {annual['keywords']}，这一年更看重结构化成长，而不是情绪式冲刺。",
            f"年度资源位是 {annual_destiny['support']['tone_name']}{support['seal_name']}，说明真正能帮你跑稳这一年的，不只是能力，而是视野、系统感和支撑结构能否跟上。",
            f"年度挑战位落在 {annual_destiny['challenge']['tone_name']}{challenge['seal_name']}，所以风险不是单点失误，而是理想化、沉浸感或节奏失真会不会让你偏离主轴。",
            f"本命 {natal['tone_name']}{natal['seal_name']} 与流年 {annual['tone_name']}{annual['seal_name']} 的互动表现为 {interaction['color_relation']} / {interaction['tone_relation']}，这决定了你今年该顺势放大，还是先做调频和整理。",
            f"引导位走向 {annual_destiny['guide']['tone_name']}{guide['seal_name']}，说明这一年的正确打开方式不是盲目加码，而是让年度主题进入可持续配置。",
        ],
        "risk_windows": [
            {
                "label": "年度主风险",
                "detail": f"如果 {challenge['seal_name']} 被低水平触发，容易把年度课题活成理想化判断、拖延确认、或在感觉里绕圈却迟迟不落地。",
            },
            {
                "label": "节奏风险",
                "detail": f"{interaction['tone_relation']} 提示今年很怕节奏失配。方向不一定错，但推进顺序和承接方式如果错了，摩擦会显著放大。",
            },
            {
                "label": "资源风险",
                "detail": f"如果没有先调用 {support['seal_name']} 的支持系统，你会更容易把年度压力误判为自己能力不足，而不是系统没搭好。",
            },
            {
                "label": "年度机会",
                "detail": f"当 {annual['seal_name']} 的主题被高质量落地时，这一年很适合做聚焦、筛选、搭结构、养长期项目，而不是到处分散试错。",
            },
        ],
        "precision_profile": build_yearly_precision_profile(natal_destiny, annual_destiny, interaction, year),
        "strategy_matrix": {
            "focus": [
                f"年度配置上优先服务 {annual['keywords']}，先决定今年真正值得种下的 1 到 3 个主题，再分配资源。",
                f"涉及扩张、转型或重大投入时，先用 {support['seal_name']} 的方式做全局视角检查，而不是只看短期情绪反馈。",
                f"如果本命 {natal['seal_name']} 的惯性还在主导你，今年要特别注意：不能只凭熟悉的做法推进，要按年度主轴重新校准。",
            ],
            "watch": [
                f"不要把 {challenge['seal_name']} 式的不确定感当成灵感本身；先验证，再投入。",
                "不要同时维护过多目标。对你来说，年度质量通常来自聚焦，而不是并行项目数量。",
                "不要在系统还没搭稳前就急着追结果，不然很容易出现前期看起来有感觉，后期却全靠补救的情况。",
            ],
            "timing": [
                "更适合先做盘点、筛选、结构搭建，再进入放量或公开表达阶段。",
                "季度复盘要围绕：我现在是在播种、培育、修剪，还是收割，而不是只看忙不忙。",
                "每次卡顿时先判断：这是方向需要调整，还是节奏需要调整，还是支持系统没有跟上。",
            ],
        },
        "situational_insight": {
            "current_pressure": [
                f"你今年最可能的真实压力，不是事情太多，而是 {annual['seal_name']} 要你聚焦，可现实里你还在被旧节奏、旧责任或旧惯性拉着走。",
                f"{interaction['tone_relation']} 说明你一旦节奏乱了，就很容易开始怀疑方向；但今年真正要调的，往往先是推进顺序，不是全部推翻。",
                f"如果 {challenge['seal_name']} 的低频已经在冒头，你现在最需要警惕的，不是没机会，而是把感觉、犹豫和理想化误当成判断本身。",
            ],
            "common_misread": [
                "你很容易把今年的摩擦感理解成自己状态不好，其实很多时候是因为年度主题要求你做减法和重排，而不是继续硬撑。",
                "低频时会表现成：明明知道该聚焦，却还是同时抓很多目标；明明知道该搭结构，却总想等更有感觉再开始。",
                "如果一直停留在分析和盘点，却没有进入真正的配置动作，这一年会显得很忙，但推进感很弱。",
            ],
            "minimum_move": [
                "先不要急着回答‘我今年到底要不要大改’，先选出一个最值得种的主题，把资源集中回去。",
                "先做一个最小结构动作，比如删掉一个分散目标、固定一个复盘节奏，或补上一个一直缺位的支持系统。",
                "今年最有效的推进不是更拼，而是先让系统稳下来，再决定哪些事情值得放大。",
            ],
        },
    }


