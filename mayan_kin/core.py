#!/usr/bin/env python3
"""Core Mayan Kin calculation logic."""

from datetime import date

from .knowledge import (
    build_auto_plan,
    load_knowledge_index,
    recommend_knowledge_cards,
    recommend_report_mode,
    recommend_report_style,
    route_query,
)


SEALS = [
    "",
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
    "",
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

REFERENCE_DATE = date(2013, 7, 26)
REFERENCE_KIN = 164

ROLE_GUIDANCE = {
    "main": "主印记代表你的核心天赋，是别人最容易感受到的你，也是你这一生最自然的表达方式。",
    "support": "支持位代表你的辅助力量，是你最容易调用、也最能给你安全感的资源。",
    "guide": "引导位代表更高版本的自己，提醒你在重大阶段往哪个方向成长和对齐。",
    "challenge": "挑战位不是缺点，而是你的成长功课。你一开始会不习惯，但整合之后会明显升级。",
    "occult": "隐藏推动代表你潜意识深处的力量，平时不一定显眼，但会在关键时刻推动你转变。",
}

SEAL_GUIDANCE = {
    "红月": "你更容易通过感受、净化、恢复流动来工作。卡住时，先清理情绪与环境，再做决定。",
    "白狗": "你的关系品质、忠诚感和真心投入，是很重要的资源。环境对不对，会直接影响发挥。",
    "蓝风暴": "变化和重组是你的成长入口。真正的功课不是逃开变化，而是学会不被变化吞没。",
    "黄人": "你的深层成长在于长出自由意志、判断力与影响力，不再只是感受，而是开始选择。",
    "黄种子": "你的重点会落在觉察、聚焦和培育真正值得生长的方向上。",
    "蓝鹰": "你的支持力量之一是视野。把自己从局部情绪里拉出来，常常能看清真正的问题。",
    "白巫师": "你容易被沉浸感和理想化吸引，修炼重点是把感受带回现实判断。",
    "红地球": "当你跟对节奏、对齐自身导航时，很多事会比硬推更顺。",
}

TONE_GUIDANCE = {
    "磁性": "这一调性的主题是聚焦。你的人生常常在问：我真正要把力气聚到哪里？",
    "韵律": "这一调性的主题是平衡、组织与结构。你越会整理节奏，越容易稳定发光。",
    "银河": "这一调性的主题是整合。你需要把理想、现实、关系与表达慢慢活成一致。",
    "宇宙": "这一调性的主题是超越与持久。你的成长不是一时爆发，而是长期活出更高版本的自己。",
}

DEEP_ROLE_GUIDANCE = {
    "main": "这股力量是你最像自己的地方。很多时候别人还没完全说清楚，你已经先用这种方式在感受、判断和反应。",
    "support": "这不是锦上添花的辅助项，而是你一稳下来就会自然调用的资源。它对了，你整个人会顺很多；它失真了，你会明显变累。",
    "guide": "这更像你正在被推过去的方向。不是要你立刻变成另一个人，而是提醒你，成熟以后会更像这样活。",
    "challenge": "这里往往不是你最不会，而是你最容易在低频里卡住的地方。它会先让你不舒服，但真正整合以后反而会变成力量。",
    "occult": "这股力量平时不一定挂在脸上，但总会在关键阶段把你往更深的选择上推。很多反复出现的课题，背后都和它有关。",
}

DEEP_TONE_GUIDANCE = {
    "磁性": "它会把问题不断拉回一个核心追问：你到底要把生命力放在哪里，而不是继续分散。",
    "韵律": "它会逼你面对节奏、结构和承接能力。很多卡点不是方向错，而是系统还没被整理好。",
    "银河": "它要求你把感受、现实、关系和表达慢慢活成一致，不能只停在其中一层。",
    "宇宙": "它会把你推向更长期的版本，不只是短期灵感或阶段性爆发，而是能不能持续活出来。",
}

SEAL_PRECISION = {
    "红龙": {
        "high": "把新的生命、项目或关系先稳稳滋养起来",
        "low": "过度照顾、替别人承担诞生前的混乱",
        "trigger": "事情刚开始、责任还没分清、别人需要被托住时",
        "need": "清楚区分滋养与代养，先确认自己是否有余力",
        "question": "我是在滋养一个真实会成长的东西，还是在替别人承担还没成形的混乱？",
    },
    "白风": {
        "high": "把精神、信息和真实感受清楚表达出来",
        "low": "话很多但没有落点，或为了维持气氛而失真表达",
        "trigger": "信息不透明、误会增多、真实话语被压住时",
        "need": "把感受翻译成清楚的话、边界和请求",
        "question": "我现在说的话，是在传递真实，还是在替关系维持表面顺畅？",
    },
    "蓝夜": {
        "high": "从内在愿景和直觉里看见丰盛方向",
        "low": "沉进想象、匮乏感或封闭的内在剧场",
        "trigger": "安全感不足、未来不清、外界催促你马上证明时",
        "need": "把愿景落成资源地图和下一步现实动作",
        "question": "这个愿景让我更有生命力，还是让我躲进一个不用行动的梦里？",
    },
    "黄种子": {
        "high": "聚焦真正值得培育的方向，让潜能持续开花",
        "low": "把成长变成过度控制、比较或迟迟不允许自己开始",
        "trigger": "选择太多、方向发散、需要长期培育时",
        "need": "确认种子、土壤、节奏和阶段目标是否匹配",
        "question": "我现在是在培育生命力，还是在用完美标准压住它？",
    },
    "红蛇": {
        "high": "顺着身体、本能和生命力做出快速而真实的反应",
        "low": "被生存焦虑、欲望冲动或身体紧绷牵着走",
        "trigger": "安全感受威胁、竞争加剧、身体已经明显反应时",
        "need": "先回到身体调节，再做重大决定",
        "question": "我的反应来自清醒的生命力，还是来自被威胁后的防御？",
    },
    "白世界桥": {
        "high": "完成旧阶段、放下不再适合的身份，打开新机会",
        "low": "用断开逃避投入，或迟迟不肯结束已经死亡的结构",
        "trigger": "旧关系、旧工作、旧身份已经不能承载你时",
        "need": "为结束设计仪式、边界和交接，而不是忽然消失",
        "question": "我是在清醒完成一个阶段，还是在用切断逃开未处理的责任？",
    },
    "蓝手": {
        "high": "通过亲自实践、疗愈和完成，让事情真正落地",
        "low": "不停修补、过度介入，或把价值感绑在解决问题上",
        "trigger": "别人求助、系统有漏洞、事情需要被收尾时",
        "need": "判断哪些是你的手该完成的，哪些需要归还给对方",
        "question": "我是在完成真正属于我的事，还是在用修补感证明自己有价值？",
    },
    "黄星星": {
        "high": "把秩序、美感和品质带进表达与作品",
        "low": "陷入挑剔、形象焦虑或只追求好看不追求真实",
        "trigger": "作品要公开、关系要被看见、品质标准被拉高时",
        "need": "让美服务真实表达，而不是替真实表达上妆",
        "question": "这个表达更真实优雅了，还是只是更安全、更好看了？",
    },
    "红月": {
        "high": "感知失真与堵塞，清理情绪并恢复生命流动",
        "low": "把敏感活成长期吸收、代谢别人情绪和自我消耗",
        "trigger": "环境失真、边界不清、情绪堆积或关系浑浊时",
        "need": "先清理边界、节奏和情绪归属，再决定投入",
        "question": "我是在恢复流动，还是在替别人排毒、替环境承担失真？",
    },
    "白狗": {
        "high": "以真心、忠诚和关系质量建立深层连接",
        "low": "把爱变成过度忠诚、关系代偿或害怕离开",
        "trigger": "关系需要承诺、信任被测试、归属感被撼动时",
        "need": "确认忠诚是否双向，真心是否被现实承接",
        "question": "我守护的是有生命力的连接，还是在守护自己害怕失去的执着？",
    },
    "蓝猴": {
        "high": "用游戏感、创意和灵活性打破僵局",
        "low": "用玩笑逃避深度，或把不确定包装成聪明",
        "trigger": "规则僵硬、气氛沉重、必须跳出原有框架时",
        "need": "让轻盈服务真实，而不是用轻盈躲开真实",
        "question": "我的轻松是在打开可能性，还是在回避需要认真面对的东西？",
    },
    "黄人": {
        "high": "长出自由意志、判断力和对他人的成熟影响力",
        "low": "被外界标准牵引，或用影响别人证明自己的选择正确",
        "trigger": "需要独立判断、价值观冲突、他人期待很强时",
        "need": "先确认这是自己的选择，再设计现实承载",
        "question": "这个选择是我清醒的自由意志，还是我在赢过别人的标准？",
    },
    "红天行者": {
        "high": "探索新空间、新经验和更大的生命边界",
        "low": "把探索变成逃离、不断换环境却不沉淀经验",
        "trigger": "空间受限、旧地图失效、需要走出舒适圈时",
        "need": "为探索设置目标、回收和落地方式",
        "question": "我是在扩展生命空间，还是在离开一个我不想面对的课题？",
    },
    "白巫师": {
        "high": "以临在、感受力和内在吸引力进入真实经验",
        "low": "沉浸在理想化、投射或不愿落地的感受里",
        "trigger": "被某种人事物强烈吸引、现实判断被感受覆盖时",
        "need": "让感受接受时间、事实和边界的校准",
        "question": "我感受到的是当下真实，还是我把渴望投射成了真实？",
    },
    "蓝鹰": {
        "high": "从高处看见系统、趋势和创造路线",
        "low": "停留在脑内蓝图，或用远景绕开眼前执行",
        "trigger": "局部混乱、路径不清、需要重新看整体时",
        "need": "把视野拆成阶段策略、角色分工和下一步动作",
        "question": "我的视野正在帮助落地，还是让我远离当下该做的选择？",
    },
    "黄战士": {
        "high": "用勇气、提问和智慧穿透虚假的权威",
        "low": "把质疑变成防御、对抗或永远不服输",
        "trigger": "权威压迫、规则不合理、内在真相被挑战时",
        "need": "把质疑导向求真，而不是导向证明自己赢",
        "question": "我是在追问真相，还是在用对抗维护自我？",
    },
    "红地球": {
        "high": "顺着同步性、节奏和现实反馈做导航",
        "low": "过度看征兆却不行动，或被环境节奏带跑",
        "trigger": "现实反馈密集、方向需要校准、节奏明显不顺时",
        "need": "把直觉导航和现实反馈同时记录、复盘、修正",
        "question": "我是在跟随真实同步，还是把外界变化都解释成命运安排？",
    },
    "白镜": {
        "high": "照见真相、秩序和关系里的真实边界",
        "low": "把看见变成审判、冷硬或不断挑错",
        "trigger": "关系失序、真相被遮盖、规则边界需要重建时",
        "need": "用清明服务修正，而不是用清明制造隔离",
        "question": "我照见真相后，是为了让事情更清楚，还是为了证明别人不对？",
    },
    "蓝风暴": {
        "high": "催化旧结构重组，让能量进入新版本",
        "low": "被变化吞没，或把混乱误认为升级",
        "trigger": "旧系统撑不住、压力突然放大、变化连续发生时",
        "need": "先稳定中心，再判断哪些变化值得承接",
        "question": "这场变化是在升级结构，还是只是把我卷进更大的消耗？",
    },
    "黄太阳": {
        "high": "把清明、温暖和生命智慧照亮给更多人",
        "low": "用正确感、光明感或救世感压过真实复杂性",
        "trigger": "需要定方向、给信心、承担照亮角色时",
        "need": "让光明保持谦卑，允许真实比理念更复杂",
        "question": "我是在照亮生命，还是在用正确感回避更细腻的真实？",
    },
}

TONE_PRECISION = {
    "磁性": {
        "task": "收束目的，把分散的生命力吸回一个核心",
        "shadow": "什么都想要，或用强烈吸引替代清楚选择",
        "check": "这件事是不是正在让我更聚焦，而不是更分散？",
    },
    "月亮": {
        "task": "识别两极、挑战和真正需要稳定的矛盾点",
        "shadow": "被对立拉扯，迟迟无法承认核心冲突",
        "check": "我是否已经说清楚当前最大的矛盾是什么？",
    },
    "电力": {
        "task": "激活连接，把觉察转化为服务和行动",
        "shadow": "到处连接却没有稳定服务对象",
        "check": "这个行动具体服务了谁，解决了什么现实问题？",
    },
    "自存": {
        "task": "定义形式、边界和可衡量的结构",
        "shadow": "概念很多，但边界、范围和标准不清",
        "check": "我能否把这件事说成一个清楚的形式和边界？",
    },
    "超频": {
        "task": "赋权、指挥和聚合资源，让能量放大",
        "shadow": "急着掌控，或把资源当成自我证明",
        "check": "我是在授权系统运转，还是在用控制维持安全感？",
    },
    "韵律": {
        "task": "组织节奏、恢复平衡，让系统可持续",
        "shadow": "为了平衡而压抑真实，或只整理不推进",
        "check": "这个节奏是否同时照顾真实、效率和承接能力？",
    },
    "共振": {
        "task": "调频、倾听和成为更清晰的通道",
        "shadow": "过度受环境影响，把共振误当成自己的方向",
        "check": "这是我的内在校准，还是我吸收了外界频率？",
    },
    "银河": {
        "task": "整合价值、关系、现实和表达，活成一致",
        "shadow": "只在理念上追求一致，却不愿处理现实冲突",
        "check": "我的选择是否让内在价值和外在行为更一致？",
    },
    "太阳": {
        "task": "把意图推向实现，让生命力持续脉动",
        "shadow": "只靠意志硬推，忽略承载系统",
        "check": "我是在健康推进，还是在用意志透支自己？",
    },
    "行星": {
        "task": "显化成果、优化品质，让价值进入现实",
        "shadow": "被结果绑架，或把不完美视为失败",
        "check": "这个成果是否真实进入了使用、交换或反馈？",
    },
    "光谱": {
        "task": "释放旧绑定，让能量重新流动",
        "shadow": "把释放变成逃避承诺，或越放越散",
        "check": "释放之后，我是否更自由也更清楚？",
    },
    "水晶": {
        "task": "合作、共享和把个人经验普遍化",
        "shadow": "为了团队而稀释自己，或把奉献变成委屈",
        "check": "这次合作是否让个人边界和共同目标同时更清楚？",
    },
    "宇宙": {
        "task": "完成一个周期，并把经验带入更高层次",
        "shadow": "停在超越感里，不再处理具体落地",
        "check": "这个完成是否让我更成熟，而不是只让我感觉已经看破？",
    },
}

SEAL_PUBLIC_EXPRESSION = {
    "红龙": {
        "tags": ["founding", "nurturing", "institution_building", "life_creation", "public_support", "nation_building"],
        "fields": ["开创型项目", "照护与教育", "组织与共同体建设"],
        "expression": "适合把一个新生命、新组织、新事业从无到有托起来。",
        "risk": "容易把滋养变成替别人承担，或把开创期混乱全部背在自己身上。",
    },
    "白风": {
        "tags": ["communication", "voice", "teaching", "media", "message", "product_storytelling"],
        "fields": ["表达传播", "教育演讲", "产品叙事", "精神与思想传递"],
        "expression": "适合把看不见的精神、理念、信息翻译成能被听见的话。",
        "risk": "容易说很多却不够落地，或为了维持沟通而牺牲真实。",
    },
    "蓝夜": {
        "tags": ["imagination", "inner_world", "visionary_dream", "hidden_resources", "abundance", "invention"],
        "fields": ["想象力产业", "愿景设计", "资源整合", "长期财富与梦想工程"],
        "expression": "适合从内在愿景、想象力和隐藏资源中创造现实可能。",
        "risk": "容易停在想象、匮乏或封闭的内在世界里。",
    },
    "黄种子": {
        "tags": ["growth", "focus", "talent_development", "cultivation", "long_term_development", "brand_building"],
        "fields": ["长期项目培育", "教育成长", "品牌与能力建设"],
        "expression": "适合把潜能长期培育成可见成果，让一个方向持续开花。",
        "risk": "容易把成长变成控制，或因标准过高而推迟开始。",
    },
    "红蛇": {
        "tags": ["embodiment", "vitality", "survival", "instinct", "body", "sensuality"],
        "fields": ["身体经验", "生命力表达", "危机生存", "强烈个人风格"],
        "expression": "适合把身体、本能和生命力转化成直接而有冲击力的表达。",
        "risk": "容易被生存焦虑、欲望或强烈身体反应牵引。",
    },
    "白世界桥": {
        "tags": ["transition", "bridge", "cross_boundary", "negotiation", "death_rebirth", "system_change"],
        "fields": ["跨界连接", "转型改革", "国际化与桥梁角色", "旧系统更新"],
        "expression": "适合连接不同世界，完成旧阶段，并把关系或系统带向新机会。",
        "risk": "容易把结束当逃避，或在关键转型中没有完成交接。",
    },
    "蓝手": {
        "tags": ["healing", "craft", "service", "completion", "practical_skill", "applied_work"],
        "fields": ["疗愈与服务", "工艺实践", "专业技能", "问题解决"],
        "expression": "适合通过亲手实践、完成、疗愈和服务让价值落地。",
        "risk": "容易过度修补，或把价值感绑在解决别人的问题上。",
    },
    "黄星星": {
        "tags": ["art", "aesthetics", "performance", "public_style", "harmony", "symbolic_design"],
        "fields": ["艺术创作", "审美表达", "舞台与视觉", "品牌风格"],
        "expression": "适合把美感、秩序和品质变成作品、风格或公众形象。",
        "risk": "容易被完美、形象或审美标准困住。",
    },
    "红月": {
        "tags": ["purification", "emotion", "flow", "reform", "public_healing", "moral_clarity"],
        "fields": ["情绪与疗愈", "改革净化", "公众议题清理", "水一样的流动表达"],
        "expression": "适合感知失真、清理堵塞，并让系统重新恢复流动。",
        "risk": "容易替人或环境吸收过多情绪，最后变成自我消耗。",
    },
    "白狗": {
        "tags": ["loyalty", "love", "community", "relationship", "empathy", "devotion"],
        "fields": ["关系经营", "社群凝聚", "情感连接", "忠诚与承诺"],
        "expression": "适合用真心、忠诚和关系品质建立深层连接。",
        "risk": "容易把爱变成代偿，或为了关系忽略自己的边界。",
    },
    "蓝猴": {
        "tags": ["creativity", "play", "experimental_intelligence", "entertainment", "imagination", "computing"],
        "fields": ["创意实验", "娱乐内容", "儿童与游戏", "聪明的跨界发明"],
        "expression": "适合用游戏感、创造力和实验精神打破僵局。",
        "risk": "容易用轻松逃避深度，或把不确定包装成聪明。",
    },
    "黄人": {
        "tags": ["influence", "free_will", "leadership", "social_change", "public_choice", "human_rights"],
        "fields": ["领导力", "公共影响", "社会运动", "价值观倡导"],
        "expression": "适合以自由意志、判断力和人本影响力推动公共选择。",
        "risk": "容易被外界标准牵引，或用影响别人证明自己正确。",
    },
    "红天行者": {
        "tags": ["exploration", "frontier", "space", "expansion", "travel", "boundary_testing"],
        "fields": ["空间探索", "跨地域拓展", "前沿技术", "新领域开路"],
        "expression": "适合探索新空间、新地图和更大的生命边界。",
        "risk": "容易把探索变成逃离，换环境却没有沉淀经验。",
    },
    "白巫师": {
        "tags": ["presence", "psychology", "symbolism", "spiritual_depth", "identity", "archetype"],
        "fields": ["心理与象征", "灵性与临在", "身份探索", "沉浸式艺术"],
        "expression": "适合以临在、感受力和象征语言触碰人的深层经验。",
        "risk": "容易把投射当真实，或沉浸在不落地的感受里。",
    },
    "蓝鹰": {
        "tags": ["vision", "strategy", "systems_thinking", "future", "mind", "big_picture"],
        "fields": ["战略规划", "系统设计", "未来想象", "宏观视野"],
        "expression": "适合从高处看见系统、趋势和未来路线。",
        "risk": "容易停在远景和脑内蓝图里，绕开眼前执行。",
    },
    "黄战士": {
        "tags": ["inquiry", "courage", "truth_seeking", "challenge_authority", "strategy", "critical_thinking"],
        "fields": ["质疑权威", "战略斗争", "科学追问", "公共辩论"],
        "expression": "适合用勇气、提问和战略意识穿透虚假权威。",
        "risk": "容易把质疑变成对抗，或为了赢而失去求真。",
    },
    "红地球": {
        "tags": ["navigation", "timing", "synchronization", "movement", "ecology", "cultural_timing"],
        "fields": ["节奏导航", "组织调度", "文化时机", "生态与土地议题"],
        "expression": "适合顺着现实反馈、同步性和时机做导航。",
        "risk": "容易过度看征兆，却没有把反馈变成行动。",
    },
    "白镜": {
        "tags": ["truth", "precision", "order", "analysis", "reflection", "justice", "scientific_research"],
        "fields": ["研究分析", "科学验证", "规则秩序", "真相与公正"],
        "expression": "适合照见真相、建立秩序，并把模糊问题分析清楚。",
        "risk": "容易把看见变成审判，或用正确感制造隔离。",
    },
    "蓝风暴": {
        "tags": ["transformation", "disruption", "energy", "innovation", "crisis_catalyst", "reinvention"],
        "fields": ["技术革新", "危机重组", "组织转型", "高能量突破"],
        "expression": "适合催化旧结构重组，让系统进入新版本。",
        "risk": "容易被变化吞没，或把混乱误认为升级。",
    },
    "黄太阳": {
        "tags": ["illumination", "wisdom", "public_light", "humanitarian", "leadership", "clarity"],
        "fields": ["公共启蒙", "智慧传播", "人道主义", "照亮型领导"],
        "expression": "适合把清明、智慧和生命力照亮给更多人。",
        "risk": "容易用正确感或救世感压过真实复杂性。",
    },
}

TONE_PUBLIC_EXPRESSION = {
    "磁性": ["purpose", "focus", "initiative", "attraction"],
    "月亮": ["polarity", "stabilization", "challenge_awareness", "tension_mapping"],
    "电力": ["activation", "service", "connection", "public_action"],
    "自存": ["definition", "form", "measurement", "structure"],
    "超频": ["empowerment", "command", "resource_gathering", "radiance"],
    "韵律": ["organization", "balance", "sustainable_system", "rhythm"],
    "共振": ["attunement", "channel", "inspiration", "frequency"],
    "银河": ["integration", "integrity", "modeling", "alignment"],
    "太阳": ["realization", "intention", "momentum", "manifesting_drive"],
    "行星": ["manifestation", "result", "quality", "public_output"],
    "光谱": ["release", "liberation", "deconstruction", "freedom"],
    "水晶": ["cooperation", "community", "sharing", "collective_work"],
    "宇宙": ["transcendence", "legacy", "endurance", "cycle_completion"],
}

STYLE_CONFIG = {
    "basic": {
        "label": "基础版",
        "description": "优先快速看懂盘面结构，适合先了解基本情况和核心主题。",
    },
    "deep": {
        "label": "深度版",
        "description": "优先做有穿透力的深度解读，结合结构、卡点、现实处境和下一步动作。",
    },
}


def normalize_report_style(style):
    if not style:
        return "basic"
    normalized = str(style).strip().lower().replace(" ", "_")
    alias_map = {
        "basic": "basic",
        "simple": "basic",
        "beginner": "basic",
        "novice": "basic",
        "xiaobai": "basic",
        "deep": "deep",
        "deep_dialogue": "deep",
        "consulting": "deep",
        "consultation": "deep",
        "advisor": "deep",
        "professional": "deep",
        "pro": "deep",
        "expert": "deep",
    }
    if normalized not in alias_map:
        valid = ", ".join(sorted(STYLE_CONFIG))
        raise ValueError(f"未知报告风格 '{style}'，可选值: {valid}")
    return alias_map[normalized]


def style_meta(style):
    normalized = normalize_report_style(style)
    return {
        "key": normalized,
        "label": STYLE_CONFIG[normalized]["label"],
        "description": STYLE_CONFIG[normalized]["description"],
    }


def stylize_text(text, style, field="general"):
    if not text:
        return text
    normalized = normalize_report_style(style)
    if normalized == "basic":
        basic_prefix = {
            "questions": "可以先问自己：",
            "decision_checks": "先检查：",
            "instructions": "使用时记住：",
            "prompts": "可直接这样问：",
        }
        prefix = basic_prefix.get(field)
        return f"{prefix}{text}" if prefix else text
    if normalized == "deep":
        return text
    return text


def stylize_sequence(items, style, field):
    return [stylize_text(item, style, field) for item in items]


def stylize_summary(summary, style):
    return {key: stylize_text(value, style, "summary") for key, value in summary.items()}


def stylize_growth_path(path, style):
    stylized = []
    for item in path:
        stylized.append(
            {
                **item,
                "focus": stylize_text(item["focus"], style, "focus"),
                "action": stylize_text(item["action"], style, "action"),
            }
        )
    return stylized


def stylize_action_guide(action_guide, style):
    return {
        section: stylize_sequence(items, style, "action")
        for section, items in action_guide.items()
    }


def stylize_delivery_layers(layers, style):
    stylized = {}
    for section_name, section in layers.items():
        stylized_section = {}
        for field, value in section.items():
            if isinstance(value, list):
                stylized_section[field] = stylize_sequence(value, style, field)
            elif isinstance(value, str):
                stylized_section[field] = stylize_text(value, style, field)
            else:
                stylized_section[field] = value
        stylized[section_name] = stylized_section
    return stylized


def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def count_leap_days_skipped(d1, d2):
    if d1 > d2:
        d1, d2 = d2, d1
        sign = -1
    else:
        sign = 1

    count = 0
    for year in range(d1.year, d2.year + 1):
        if is_leap_year(year):
            leap_day = date(year, 2, 29)
            if d1 < leap_day <= d2:
                count += 1

    return count * sign


def parse_iso_date(value, field_name="日期"):
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"无法解析{field_name} '{value}'，请使用 YYYY-MM-DD 格式") from exc


def date_to_kin(target_date):
    if isinstance(target_date, str):
        target_date = date.fromisoformat(target_date)

    delta_days = (target_date - REFERENCE_DATE).days
    if delta_days >= 0:
        leap_skips = count_leap_days_skipped(REFERENCE_DATE, target_date)
    else:
        leap_skips = -count_leap_days_skipped(target_date, REFERENCE_DATE)

    adjusted_days = delta_days - leap_skips
    return ((REFERENCE_KIN - 1 + adjusted_days) % 260) + 1


def kin_to_seal(kin):
    return ((kin - 1) % 20) + 1


def kin_to_tone(kin):
    return ((kin - 1) % 13) + 1


def seal_color(seal_num):
    return COLORS[seal_num]


def calc_support_seal(main_seal):
    support = 19 - main_seal
    if support <= 0:
        support += 20
    return support


def calc_challenge_seal(main_seal):
    challenge = main_seal + 10
    if challenge > 20:
        challenge -= 20
    return challenge


def calc_occult_seal(main_seal):
    occult = 21 - main_seal
    if occult <= 0:
        occult += 20
    return occult


def calc_guide_seal(main_seal, main_tone):
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

    return ((main_seal - 1 + offset) % 20) + 1


def calc_occult_tone(main_tone):
    return 14 - main_tone


def calc_five_destiny(kin):
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


def calc_wavespell(kin):
    wavespell_index = (kin - 1) // 13
    wavespell_start_kin = wavespell_index * 13 + 1
    wavespell_seal = kin_to_seal(wavespell_start_kin)
    position = ((kin - 1) % 13) + 1
    return {
        "wavespell_number": wavespell_index + 1,
        "wavespell_seal": wavespell_seal,
        "wavespell_name": SEALS[wavespell_seal],
        "wavespell_en": SEALS_EN[wavespell_seal],
        "position": position,
        "start_kin": wavespell_start_kin,
    }


def calc_yearly_kin(birth_date, year):
    if isinstance(birth_date, str):
        birth_date = date.fromisoformat(birth_date)

    month, day = birth_date.month, birth_date.day
    if month == 2 and day == 29 and not is_leap_year(year):
        month, day = 2, 28

    return date_to_kin(date(year, month, day))


def calc_yearly_report(birth_date, year):
    return calc_five_destiny(calc_yearly_kin(birth_date, year))


def calc_relationship(kin_a, kin_b):
    seal_a = kin_to_seal(kin_a)
    seal_b = kin_to_seal(kin_b)
    tone_a = kin_to_tone(kin_a)
    tone_b = kin_to_tone(kin_b)

    a_support = calc_support_seal(seal_a)
    a_challenge = calc_challenge_seal(seal_a)
    a_occult = calc_occult_seal(seal_a)
    a_guide = calc_guide_seal(seal_a, tone_a)

    b_support = calc_support_seal(seal_b)
    b_challenge = calc_challenge_seal(seal_b)
    b_occult = calc_occult_seal(seal_b)
    b_guide = calc_guide_seal(seal_b, tone_b)

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

    combined_kin = ((kin_a + kin_b - 1) % 260) + 1
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

    summary = {
        "core_theme": f"{main['tone_name']}{main['seal_name']}的主轴是{main['keywords']}，人生会不断回到“我真正要如何使用自己的天赋”这个问题。",
        "strength": f"你的天然资源更接近{support['seal_name']}：{support['keywords']}。环境、关系与支持系统是否合适，会直接影响发挥。",
        "challenge": f"你的成长功课在{challenge['seal_name']}：{challenge['keywords']}。这不是缺点，而是你需要整合的力量。",
        "hidden_driver": f"更深层推动力来自{occult['seal_name']}：{occult['keywords']}。这常常决定你后续真正会长成什么样的人。",
        "guidance": f"引导位落在{guide['seal_name']}，说明你最终要活出的不是别人的版本，而是更成熟的自己。",
    }
    return summary


def build_growth_path(destiny):
    support = destiny["support"]
    main = destiny["main"]
    challenge = destiny["challenge"]
    occult = destiny["occult"]
    guide = destiny["guide"]

    return [
        {
            "stage": "隐藏推动",
            "sign": f"{occult['tone_name']}{occult['seal_name']}",
            "focus": f"先认识你潜意识深处的力量：{occult['keywords']}。",
            "action": "先问自己真正想要什么，不要总是让环境先替你做决定。",
        },
        {
            "stage": "支持位",
            "sign": f"{support['tone_name']}{support['seal_name']}",
            "focus": f"建立能支持你的资源系统：{support['keywords']}。",
            "action": "筛选关系、环境与合作，把真心给对地方。",
        },
        {
            "stage": "主印记",
            "sign": f"{main['tone_name']}{main['seal_name']}",
            "focus": f"扎根你的核心天赋：{main['keywords']}。",
            "action": "让自己的生活和表达重新回到真实、流动和一致。",
        },
        {
            "stage": "挑战位",
            "sign": f"{challenge['tone_name']}{challenge['seal_name']}",
            "focus": f"整合你的成长功课：{challenge['keywords']}。",
            "action": "变化来了不要先自我否定，而是判断这次升级在教你什么。",
        },
        {
            "stage": "引导位",
            "sign": f"{guide['tone_name']}{guide['seal_name']}",
            "focus": "活出更成熟、更有力量的自己。",
            "action": "不是变成别人，而是让自己的天赋越来越清楚、稳定、可持续。",
        },
    ]


def build_action_guide(destiny):
    main = destiny["main"]
    support = destiny["support"]
    challenge = destiny["challenge"]
    occult = destiny["occult"]
    return {
        "career": [
            f"优先考虑能发挥{main['keywords']}的工作，而不是长期要求你压住天赋的环境。",
            f"把{support['seal_name']}对应的资源系统建起来：关系、合作和支持氛围会直接影响你的表现。",
            f"遇到{challenge['seal_name']}式压力时，先分辨它是在训练你升级，还是在单纯消耗你。",
        ],
        "relationship": [
            "不要只因为有感觉就长期留下来，也要看这段关系是否真的滋养你。",
            f"当你开始反复感受到{challenge['seal_name']}式张力时，记得补边界，而不是只补耐心。",
            f"更深层的成熟，来自把{occult['seal_name']}对应的判断力、选择权和方向感长出来。",
        ],
        "growth": [
            f"先承认自己的核心频率是{main['seal_name']}，不要总逼自己活成别人的节奏。",
            "每次卡住时，先问这是信息堵、情绪堵、边界堵、责任堵还是节奏堵。",
            "把感受推进成选择，把觉察推进成行动，而不是长期停留在“我知道不对”。",
        ],
    }


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
                "detail": f"{support['seal_name']} 不是让你依附外部环境，而是提醒你：你的发挥需要合适土壤。土壤不对时，先调整配置，不要直接否定能力。",
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


def build_professional_personal_analysis(destiny):
    main = destiny["main"]
    support = destiny["support"]
    challenge = destiny["challenge"]
    occult = destiny["occult"]
    guide = destiny["guide"]

    return {
        "structural_analysis": [
            f"你这张盘的核心，不是靠外放征服世界，而是先用 {main['keywords']} 去感受到哪里失真、哪里堵住、哪里需要重新校准，然后再决定怎么动。",
            f"你真正稳的时候，通常不是因为一个人硬撑住了，而是因为 {support['seal_name']} 这层资源到位了：关系质量、信任密度、合作氛围都在帮你稳住自己。",
            f"你的人生压力点也不只是事情多，而是 {challenge['seal_name']} 一来，变化、重组和能量冲击会不会先把你的中心打散，让你一边感受到不对，一边又很难马上表态。",
            f"更深一层看，{occult['seal_name']} 一直在推着你长判断、长选择、长影响力，所以你的人生不会只停在“我感受很多”，最后一定会走向“那我到底怎么选”。",
            f"引导位又回到 {guide['seal_name']}，说明你真正成熟后的样子，不是换成另一个人格，而是把原本这套天赋活得更稳定、更清楚，也更不容易被外界拖走。",
        ],
        "precision_profile": build_precision_profile(destiny),
        "expression_profile": build_expression_profile(destiny),
        "risk_matrix": [
            {
                "label": "高频优势",
                "detail": f"你最容易在需要 {main['keywords']}、关系理解与系统调频的场景中发挥价值。别人觉得乱的地方，你反而比较容易先感觉到真正的堵点。",
            },
            {
                "label": "主要风险",
                "detail": f"当 {challenge['seal_name']} 被低水平触发时，你很容易先失去节奏，再谈判断。外面看像你在犹豫，里面其实常常是变化已经压到你了。",
            },
            {
                "label": "资源条件",
                "detail": f"{support['seal_name']} 提醒你：你的发挥从来不只看能力，还看环境是不是允许真诚沟通、角色清晰和相互信任。土壤不对，你会明显耗掉。",
            },
            {
                "label": "升级方向",
                "detail": f"{occult['seal_name']} 对应的成长，不是把自己练得更能忍，而是把感受转换成边界，把直觉转换成选择，把经验转换成影响力。",
            },
        ],
        "application_matrix": {
            "career": [
                f"职业定位上，优先选择需要 {main['keywords']}、洞察、梳理、咨询、陪伴、内容转译或复杂关系协同的工作。",
                f"管理与合作上，要先建 {support['seal_name']} 型支持系统，再谈高压推进；没有信任基础时，硬推只会放大 {challenge['seal_name']} 的成本。",
                f"决策上要避免把所有变化都当成机会。先判断这次变化是在升级结构，还是只是在重复消耗。",
            ],
            "relationship": [
                "关系层面不能只看感觉强不强，还要看这段关系是否真的提高了你的稳定度、清晰度和生命流动感。",
                f"当 {challenge['seal_name']} 型冲击出现时，第一动作应该是重建边界和节奏，而不是继续用理解去覆盖问题。",
                f"{occult['seal_name']} 的课题要求你在关系里长出选择权，不再让“我理解你”自动滑向“那我继续承担”。",
            ],
            "development": [
                f"个人发展上，要把 {main['seal_name']} 的敏感度训练成方法，而不是停留在体验层。",
                "建议长期保留一套自己的堵点诊断框架，用来区分信息堵、情绪堵、边界堵、责任堵和节奏堵。",
                f"当你能稳定调用 {support['seal_name']} 的资源、承接 {challenge['seal_name']} 的波动，并兑现 {occult['seal_name']} 的判断力时，这张盘会进入高水平发挥。",
            ],
        },
        "situational_insight": {
            "current_block": [
                f"你现在最可能反复卡住的，不是看不见问题，而是明明已经感受到 {main['seal_name']} 式失真，却还没有把它足够快地推进成决定。",
                f"当 {support['seal_name']} 想维持关系质量、而 {challenge['seal_name']} 又把变化推到你面前时，你很容易卡在“我再看一下”而不是“我现在就表态”。",
                f"{occult['seal_name']} 的课题说明，你真正难的不是理解别人，而是理解完之后，有没有及时站回自己的判断。",
            ],
            "low_frequency": [
                "低频时，你会把敏感活成长期承受，把觉察活成迟疑，把理解活成代偿。",
                "你可能会先处理气氛、照顾关系、维持流动，最后才轮到处理自己真正的边界和选择。",
                "表面上看像是在忍，实质上是在延迟那一个早该做出的判断。",
            ],
            "minimum_move": [
                "现在最小但最有效的动作，不是想清全部，而是把一个已经感受到的不对劲，翻译成一句明确的话或一个明确边界。",
                "你要先从“我知道哪里不对”走到“所以我现在准备怎么处理”，这一步比继续分析更关键。",
                "对你这张盘来说，真正的升级通常不是更努力，而是更早识别、更早表达、更早止损、更早投入对的地方。",
            ],
        },
        "reflection_dialogue": {
            "resonance_points": [
                f"如果你最近一直觉得哪里不太对，却又说不清，那通常不是你想太多，而是 {main['seal_name']} 已经先感觉到了流动出了问题。",
                f"如果你一边想维持关系，一边又越来越累，这往往是 {support['seal_name']} 想守住连接，而 {challenge['seal_name']} 又在不断把真实问题顶出来。",
                f"如果你最近反复在想“我到底要不要为自己做一个更清楚的决定”，那不是偶然，通常是 {occult['seal_name']} 已经开始往前推你了。",
            ],
            "conversation_questions": [
                "你最近最明显的一次委屈，背后其实在提醒你什么边界？",
                "你现在最不想承认、但其实已经感觉到不对的地方，是哪一件事？",
                "如果这次你不再只理解别人，而是站回自己，你最想先说出来的一句话会是什么？",
            ],
            "next_opening": [
                "如果你愿意继续聊，可以直接从最近最卡的一件事讲起，不用先讲大道理。",
                "你也可以直接说：我现在最难受的是哪段关系、哪个环境、还是哪个决定，我会顺着这张盘继续帮你往下拆。",
                "对你来说，真正有价值的不是把盘读完，而是把它放回你现在的生活里，看它到底在提醒你什么。",
            ],
        },
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


def build_personal_delivery_layers(destiny, style="basic"):
    main = destiny["main"]
    support = destiny["support"]
    challenge = destiny["challenge"]
    occult = destiny["occult"]
    guide = destiny["guide"]
    layers = {
        "consultation": {
            "focus": "围绕天赋、卡点和边界来提问，先看清哪里堵，再决定怎么动。",
            "questions": [
                f"我现在最反复卡住的地方，和{challenge['seal_name']}的成长功课有什么关系？",
                f"我看到的堵点，是信息、情绪、边界、责任还是节奏的问题？",
                f"这段关系或这个环境，真的值得我继续用{occult['seal_name']}式能量去推动吗？",
            ],
            "decision_checks": [
                f"我有没有先调用{support['seal_name']}对应的支持资源，而不是一上来就硬扛？",
                f"我是不是已经看见{guide['seal_name']}式的成长方向，但还没真正站过去？",
                "如果我要保护自己的流动感，现在最小的动作应该是什么？",
            ],
        },
        "content": {
            "focus": "适合做成个人说明书、成长路线图、卡点清单和边界练习稿。",
            "angles": [
                f"《为什么我会卡住，以及怎么把{main['seal_name']}的天赋用起来》",
                f"《我的{support['seal_name']}资源怎么影响我的发挥》",
                f"《我和{challenge['seal_name']}的关系：变化来了，我怎么不被卷走》",
                f"《如何把{occult['seal_name']}的深层推动，变成更成熟的选择》",
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
                "先判断这是个人天赋、关系消耗还是环境不适配。",
                f"输出时优先围绕{main['seal_name']}的主轴、{challenge['seal_name']}的功课和{guide['seal_name']}的成长方向。",
                "如果信息不足，先提出 1 到 3 个关键追问，不要直接泛泛而谈。",
            ],
            "prompts": [
                "请先判断我现在的卡点属于哪一类，再给我可执行的下一步。",
                "请把这张盘翻译成适合普通用户理解的行动建议。",
                "请用咨询顾问的方式，先指出问题，再给出边界和选择。",
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
    lines.append("  核心摘要")
    lines.append(f"{'─' * 50}")
    lines.append(f"- 主轴: {report['summary']['core_theme']}")
    lines.append(f"- 资源: {report['summary']['strength']}")
    lines.append(f"- 功课: {report['summary']['challenge']}")
    lines.append(f"- 深层推动: {report['summary']['hidden_driver']}")
    lines.append(f"- 引导方向: {report['summary']['guidance']}")

    if report.get("deep_analysis"):
        analysis = report["deep_analysis"]
        lines.append(f"\n{'─' * 50}")
        lines.append("  结构分析")
        lines.append(f"{'─' * 50}")
        for item in analysis["structural_analysis"]:
            lines.append(f"- {item}")

        lines.append(f"\n{'─' * 50}")
        lines.append("  风险矩阵")
        lines.append(f"{'─' * 50}")
        for item in analysis["risk_matrix"]:
            lines.append(f"- {item['label']}: {item['detail']}")
        format_precision_section(lines, "解读校准", analysis["precision_profile"])
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
        lines.append("- 低频表现")
        for item in insight["low_frequency"]:
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
        lines.append("- 可以继续往下聊的问题")
        for item in dialogue["conversation_questions"]:
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
