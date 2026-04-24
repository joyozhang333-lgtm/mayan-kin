# 🌀 mayan-kin · Mayan Destiny / Dreamspell / Tzolkin Kin Calculator

> Open-source **Mayan Destiny / Dreamspell / Tzolkin Kin calculator** and AI-ready interpretation toolkit. 输入一个阳历生日，即可计算 `Kin number / Kin 号`、`solar seal / 图腾`、`galactic tone / 调性`、五大天赋盘、波符、流年、合盘，并生成面向小白和专业人士的非宿命论解读报告。

**Repository URL:** [github.com/joyozhang333-lgtm/mayan-kin](https://github.com/joyozhang333-lgtm/mayan-kin)

**Core search keywords:** `mayan destiny calculator`, `dreamspell calculator`, `tzolkin calculator`, `kin calculator`, `kin number calculator`, `maya calendar calculator`, `galactic signature`, `solar seal`, `galactic tone`, `mayan compatibility reading`, `yearly kin reading`, `玛雅天赋`, `星系印记`, `Kin 计算器`, `玛雅合盘`, `玛雅流年`

## 中文简介：这是什么项目？

`mayan-kin` 是一个开源的 **玛雅天赋 / Mayan Destiny / Dreamspell / Tzolkin / Kin Calculator** 项目。它不是一个只告诉你编号的玩具脚本，而是一套可以被普通用户阅读、也可以被开发者和 AI agent 集成的玛雅天赋计算与解读基础设施。

你只需要输入一个阳历生日，例如 `1995-03-03`，系统就可以计算并输出：

- `Kin number / Kin 号`
- `Solar Seal / 图腾`
- `Galactic Tone / 调性`
- 五大天赋盘：主印记、支持位、引导位、挑战位、隐藏推动
- 波符与波符内位置
- 任意年份的流年 Kin 与年度主题
- 双人合盘、颜色关系、调性关系与互相照见位置
- 适合人阅读的基础版 / 深度版报告
- 适合程序、前端、数据库和 AI agent 复用的 JSON 输出

这个项目的核心定位是：**用可计算、可验证、可集成的方式，把玛雅天赋从“神秘标签”变成“可解释的自我理解工具”。**

它强调非宿命论。玛雅天赋在这里不是用来定义你、限制你、替你决定人生，而是帮助你观察：

- 你的核心天赋是什么，它在现实里通常怎么表现
- 你的卡点在哪里，哪些压力其实是在提醒你成长
- 你的支持力量来自哪里，什么样的关系、环境和节奏更能让你发挥
- 你的挑战位不是缺点，而是需要被整合的成长入口
- 你的隐藏推动如何把你从“感受到很多”推向“做出清楚选择”
- 你如何把自己的天赋落到事业、关系、内容、咨询和个人成长中

## English Introduction

`mayan-kin` is an open-source **Mayan Destiny, Dreamspell, Tzolkin, Maya Calendar, and Kin calculator** for self-exploration, AI assistants, consultants, creators, and developers.

It converts a Gregorian birth date into structured Mayan Destiny data, including `Kin number`, `solar seal`, `galactic tone`, five destiny positions, wavespell placement, yearly Kin cycles, and compatibility readings. On top of the calculation layer, it also generates beginner-friendly and deep interpretation reports that can be used in personal reflection, coaching, content creation, or AI agent workflows.

If you are searching GitHub or Google for a **Mayan Destiny calculator**, **Dreamspell calculator**, **Tzolkin calculator**, **Kin number calculator**, **Maya calendar calculator**, **galactic signature lookup**, **solar seal reading**, **galactic tone reading**, **Mayan compatibility reading**, or **yearly Kin reading**, this repository is designed to be a practical open-source foundation.

The project is built around three principles:

- **Accessible:** beginners can start with one birth date and understand what their Kin, solar seal, galactic tone, and five destiny positions mean.
- **Structured:** developers can import the Python core, call the CLI, consume JSON output, or connect the logic to AI agents and runtime toolkits.
- **Verifiable:** the calculation core is covered by tests and validation samples, so the project can improve without silently breaking core Kin calculations.

## What Can You Build With It?

`mayan-kin` can be used as:

- a `Kin calculator` for personal Mayan Destiny lookup
- a `Dreamspell / Tzolkin chart` generator
- a `Mayan Destiny reading` engine for beginner-friendly reports
- a `Mayan compatibility reading` tool for relationship or collaboration analysis
- a `yearly Kin reading` tool for annual themes and timing reflection
- a Python CLI for structured `Maya calendar` calculations
- an AI skill for Codex, Claude-style runtimes, OpenClaw, Hermes, and other agent systems
- a reusable interpretation layer for coaching, consulting, courses, content products, or self-reflection apps

## 核心功能

### 计算层

- 阳历生日转 `Kin number / Kin 号`
- 20 个图腾与 13 个调性的组合计算
- 五大天赋盘排盘
- 波符与波符内位置计算
- 流年 Kin 计算
- 双人合盘与关系互动计算

### 解读层

- 基础版报告：快速看懂盘面结构，适合第一次接触玛雅天赋的人
- 深度版报告：输出结构分析、风险矩阵、情境直读、成长路径和行动建议
- 解读校准：把盘面翻译成触发条件、误读风险、验证问题和最小实验
- 小白友好表达：减少术语堆叠，让用户知道“这和我的生活有什么关系”
- 专业输出结构：适合咨询师、内容创作者、课程设计者和 AI 产品开发者二次使用

### 工程层

- CLI 命令行工具
- JSON 机器可读输出
- `--contract` 接口契约
- `--route-query` 知识卡路由
- `--auto-answer` 自动判断知识卡、报告风格和报告模式
- 公开人物 benchmark：用 12 位公开人物的生日与公开生平主题评测深度解读覆盖度
- Codex / Claude 风格 skill
- OpenClaw runtime 版本
- Hermes runtime 版本
- 测试基线与公开样本校验

## Who Is This For?

### For Beginners

Use this repository if you want to understand your Mayan Destiny without learning the whole system first. You can enter one birth date and get a readable explanation of your Kin, solar seal, galactic tone, five destiny positions, yearly cycle, or compatibility pattern.

This project is intentionally written in a non-fatalistic way. It does not tell you that your life is fixed. It helps you notice your talents, recurring blocks, support conditions, and possible growth directions.

### For Developers

Use this project if you want an open-source `Mayan Destiny calculator`, `Dreamspell calculator`, or `Tzolkin calculator` that can be integrated into another tool. You can call the CLI, import the Python module, use JSON output, or adapt the skill files for AI runtime environments.

### For AI Builders

Use `mayan-kin` if you want to build an AI assistant that can answer questions about Kin, solar seals, galactic tones, five destiny positions, yearly readings, and compatibility readings. The repository includes a knowledge index, report styles, route-query support, and runtime prompts for agent systems.

### For Consultants, Coaches, and Creators

Use it as a structured reference layer for self-exploration reports, coaching conversations, relationship reflection, career direction content, personal growth courses, or long-form article generation. The output is designed to support conversation and reflection, not to replace human judgment.

## SEO Search Phrases

This repository is relevant to searches such as:

- `Mayan Destiny calculator`
- `Dreamspell calculator`
- `Tzolkin calculator`
- `Kin calculator`
- `Kin number calculator`
- `Maya calendar calculator`
- `Galactic signature calculator`
- `Solar seal calculator`
- `Galactic tone calculator`
- `Mayan astrology calculator`
- `Mayan compatibility reading`
- `Mayan relationship compatibility`
- `Yearly Kin reading`
- `Dreamspell birth chart`
- `Tzolkin birth chart`
- `玛雅天赋 计算`
- `玛雅天赋 计算器`
- `星系印记 查询`
- `星系印记 计算器`
- `Kin 号 查询`
- `Kin 计算器`
- `玛雅合盘`
- `玛雅流年`
- `玛雅图腾`
- `玛雅调性`

## 适用人群

### 对小白用户

- 想第一次看懂自己的玛雅天赋，不想被术语劝退
- 希望知道“这个系统到底在讲什么”，而不只是拿到一个编号
- 想从事业、关系、自我成长角度理解自己的天赋倾向
- 希望获得有启发但不过度宿命化的解释

### 对专业人士

- 咨询师、内容创作者、课程设计者，希望把玛雅天赋做成标准化输出
- AI 产品开发者，希望把该体系接进 agent、skill、bot 或内容工作流
- 研究者或重度爱好者，希望有一个可读、可测、可扩展的基础实现
- 需要多运行时版本，而不是只绑定单一平台

## 为什么做这个项目

这个项目的出发点，不是为了把人定义死，更不是为了制造“你命中注定就是这样”的宿命论。
相反，它想做的是一件更有生命力的事情：
帮助一个人以非宿命论的方式，去理解自己的天赋、卡点、成长方向，以及自己在这一生里更自然、更有力量的表达方式。

很多人接触类似体系时，最容易掉进两个误区：
- 一种是把它当成绝对命运，最后越看越被框住
- 一种是只拿到一些漂亮词汇，却不知道这些词汇和现实生活到底有什么关系

`mayan-kin` 想解决的，就是这两个问题。

它希望帮助用户回答几类更真实的问题：
- 我的核心天赋到底是什么？它在现实中会怎么表现？
- 我为什么总是在某些地方卡住？这些卡点和我的成长课题有什么关系？
- 我的支持力量在哪里？我真正可以依靠的内在资源是什么？
- 我不是要“变成别人”，而是要如何更好地活出我原本就带着的生命光芒？

从这个角度看，玛雅天赋不是一个“给你下定义”的系统，而更像一面镜子：
- 帮你看见你已经带着的频率
- 帮你识别你当下反复碰到的卡点
- 帮你理解这些卡点不一定是缺陷，也可能正是你通往绽放的入口
- 帮你把“知道自己是谁”进一步推进到“知道如何使用自己的天赋”

这个项目相信，一个人的绽放并不是靠强行成为另一个人，而是更清楚地认识自己、整合自己、使用自己。
当你知道自己的核心天赋是什么、支持位在哪里、挑战位想教你什么、隐藏推动如何在关键时刻出现时，
你就更有机会从“总觉得自己哪里不对”转向“我开始知道如何活出我本来的精彩”。

所以，这个项目不是为了替你决定人生，
而是为了给你一个更清晰、更温和、也更可落地的自我理解工具。

## 适用场景

### 个人探索

- 想知道自己的核心天赋是什么，以及为什么自己会被某类事情自然吸引
- 想理解自己长期重复出现的卡点、关系模式、表达障碍或成长瓶颈
- 想把“灵性系统”转译成能落到现实生活中的自我认知工具

### 咨询与陪伴

- 咨询师、教练、疗愈工作者把它作为辅助性的自我探索镜子
- 在不做宿命化判断的前提下，帮助来访者理解自己的天赋结构与成长课题
- 作为关系、事业、自我价值感等议题的补充观察维度

### 内容创作与课程产品

- 用于撰写公众号文章、课程内容、解读模板、用户报告
- 把玛雅天赋从“术语堆叠”整理成面向普通用户可理解的结构化表达
- 为内容产品提供统一的计算底座和解释框架

### AI Agent / 工具集成

- 接入 Codex、Claude 风格 skills、OpenClaw、Hermes 等运行时
- 作为 AI 解读助手、聊天机器人、咨询辅助工具的底层能力
- 输出结构化 JSON，方便接到自己的前端、数据库、工作流或自动化系统

### 研究与验证

- 对 Dreamspell / Tzolkin 相关计算逻辑做可复核实现
- 用测试样本和公开锚点验证核心算法稳定性
- 为后续扩展更多盘面、规则和解释体系提供基础工程结构

## 路线图

### 近期方向

- 持续补充权威样本校验，降低核心计算回归风险
- 打磨 README、运行时适配和示例，让不同用户更快上手
- 继续优化小白友好的解释语言，减少“术语懂了但不会用”的问题

### 中期方向

- 补充更完整的流年、合盘、波符与颜色关系解释模板
- 增加更适合咨询、内容产品和 AI 对话的输出格式
- 扩展更多运行时接入方式，让同一套核心可以服务不同平台

### 长期方向

- 建立更系统的玛雅天赋知识库与解释层
- 形成既适合普通用户，也适合专业使用者的多层输出体系
- 让这个项目从“一个会算 Kin 的 skill”，升级成“一个可解释、可验证、可集成的玛雅天赋开源基础设施”

## Quick Start

### 1. 克隆仓库

```bash
git clone https://github.com/joyozhang333-lgtm/mayan-kin.git
cd mayan-kin
```

### 2. 直接运行命令行工具

```bash
python3 scripts/mayan_calc.py 1990-03-15
```

### 3. 输出 JSON 结果

```bash
python3 scripts/mayan_calc.py 1990-03-15 --json
python3 scripts/mayan_calc.py 1990-03-15 --report
```

### 4. 查看 CLI 契约

```bash
python3 scripts/mayan_calc.py --contract
```

### 5. 路由用户问题到知识卡

```bash
python3 scripts/mayan_calc.py --route-query "我想看2026流年和事业方向"
```

### 6. 自动路由并决定报告风格

```bash
python3 scripts/mayan_calc.py --auto-answer "我想看2026流年和事业方向"
python3 scripts/mayan_calc.py 1995-03-03 --auto-answer "我想看2026流年和事业方向" --yearly 2026
```

### 7. 切换报告风格

```bash
python3 scripts/mayan_calc.py 1995-03-03 --report --style basic
python3 scripts/mayan_calc.py 1995-03-03 --report --style deep
```

### 8. 查看流年或合盘

```bash
python3 scripts/mayan_calc.py 1990-03-15 --yearly 2026
python3 scripts/mayan_calc.py 1990-03-15 --compatibility 1992-07-20
```

### 9. 跑测试

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

### 10. 跑公开人物 benchmark

```bash
python3 scripts/evaluate_public_figures.py --min-score 90
```

这个 benchmark 使用 `references/public-figure-benchmark.json` 中的公开人物生日、资料来源和公开生平主题，评测深度报告的现实表达标签是否覆盖这些主题。它是产品质量评测，不是科学宿命论证明。

如果你是要接进 AI 助手，而不是只在命令行里用：
- Codex / Claude 风格：看 `SKILL.md`
- OpenClaw：看 `runtimes/openclaw/AGENTS.md` 和 `runtimes/openclaw/DEMO.md`
- Hermes：看 `runtimes/hermes/SYSTEM_PROMPT.md` 和 `runtimes/hermes/DEMO.md`

## Interface & Docs

### CLI Usage

```bash
python3 scripts/mayan_calc.py [birthday] [options]
```

- `birthday` 是普通模式的必填输入，格式为 `YYYY-MM-DD`
- `--json` 输出机器可读结果，适合前端、数据库和二次处理
- `--report` 输出指导型个人说明书，适合人阅读
- `--style` 控制报告风格，推荐只用 `basic / deep`
- `--auto-answer` 根据自然语言问题自动选知识卡和风格；提供生日时直接出报告
- `--auto-answer` 还会自动决定更适合出 `personal / yearly / compatibility / combined` 哪种报告
- `--route-query` 根据自然语言问题推荐知识卡，适合 agent / runtime 做最小加载
- `--contract` 输出 CLI / JSON 契约说明，不需要 `birthday`
- 输出优先级固定为 `--contract > --auto-answer > --route-query > --report > --json > 默认文本`

### Documentation Entry Points

- [docs/README.md](docs/README.md) - 文档导航页
- [docs/cli.md](docs/cli.md) - CLI 参考、usage 和参数说明
- [docs/report.md](docs/report.md) - `--report` 命令说明
- [docs/json-contract.md](docs/json-contract.md) - JSON 契约说明
- [docs/kin-calculator.md](docs/kin-calculator.md) - 英文落地页
- [docs/v2-roadmap.md](docs/v2-roadmap.md) - v2 / v1.0 路线图
- [references/README.md](references/README.md) - 知识卡导航页
- [references/knowledge-index.json](references/knowledge-index.json) - 机读知识索引
- [references/public-figure-benchmark.json](references/public-figure-benchmark.json) - 公开人物解读贴合度 benchmark
- [references/public-figure-benchmark-results.json](references/public-figure-benchmark-results.json) - 最近一次 benchmark 结果

## Examples

### 示例一：基础排盘

输入：

```bash
python3 scripts/mayan_calc.py 1990-03-15
```

你会得到：
- Kin、图腾、调性
- 五大天赋盘
- 波符位置

适合第一次认识自己的核心天赋结构。

### 示例二：流年运势

输入：

```bash
python3 scripts/mayan_calc.py 1988-06-20 --yearly 2026
```

适合回答：
- 这一年被点亮的主题是什么？
- 这一年更适合处理哪些课题？
- 流年和本命之间是支持、挑战还是放大？

### 示例三：双人合盘

输入：

```bash
python3 scripts/mayan_calc.py 1990-03-15 --compatibility 1992-07-20
```

适合观察：
- 两人的颜色关系
- 调性关系
- 对方的图腾落在自己五大盘的什么位置

### 示例四：结构化输出给程序使用

输入：

```bash
python3 scripts/mayan_calc.py 1990-03-15 --json
```

适合：
- 接前端页面
- 存数据库
- 做 AI agent 二次解释
- 做批量报告生成

### 示例五：个人说明书报告

输入：

```bash
python3 scripts/mayan_calc.py 1995-03-03 --report
```

适合：
- 生成更有指导性的个人说明书
- 输出成长路径、位置解释和行动建议
- 作为咨询、内容产品或 AI 对话的中间层材料

### 示例六：知识卡自动路由

输入：

```bash
python3 scripts/mayan_calc.py --route-query "我想看合盘和关系边界"
```

适合：
- agent 在加载解释知识前先做问题路由
- 调试 `knowledge-index.json` 的匹配效果
- 判断当前问题最应该读哪几张卡

### 示例七：自动选卡 + 自动选风格

输入：

```bash
python3 scripts/mayan_calc.py 1995-03-03 --auto-answer "我想看2026流年和事业方向" --yearly 2026
```

适合：
- 让系统先判断这是哪类问题
- 自动决定更适合 `basic / deep` 哪种风格
- 先打印决策结果，再直接输出对应的报告模式

### 示例八：深度版报告

输入：

```bash
python3 scripts/mayan_calc.py 1995-03-03 --report --style deep
```

适合：
- 咨询师、陪伴者、教练直接拿来追问和判断
- 更快看见卡点、判断点和下一步动作
- 用“解读校准”区分高频表达、低频代偿、触发条件和现实验证点
- 把同一份盘切换成更偏对话与行动的输出

### 示例九：接口契约

输入：

```bash
python3 scripts/mayan_calc.py --contract
```

适合：
- 快速确认 CLI 的参数、优先级和 JSON 结构
- 给前端、自动化脚本和 AI agent 对接前先看契约
- 让外部用户明确这不是“猜输出”，而是有稳定边界的接口

## FAQ

### 1. 这是算命吗？

不是传统意义上的“宿命论算命”。
这个项目的定位是自我认知与天赋探索工具，强调的是看见自己的倾向、资源、卡点和成长方向，而不是替你决定命运。

### 2. 需要出生时辰吗？

当前不需要。
`mayan-kin` 目前使用的是阳历生日作为计算输入。

### 3. 需要用农历吗？

不需要。
请直接输入阳历（公历）日期，例如 `1990-03-15`。

### 4. 适合完全不懂玛雅天赋的人吗？

适合。
这个项目就是按“小白也能读懂”的方向在写解释层的，同时也保留了专业用户可复用的结构化输出。

### 5. 可以拿来做咨询或内容产品吗？

可以，但建议明确把它定位为辅助性的自我探索工具，而不是绝对判断系统。
如果用于咨询、课程、内容产品，也建议同时保留 `ETHICS.md` 中的非宿命化边界。

### 6. 这个项目的算法可验证吗？

可以。
仓库里已经有测试基线和公开样本校验文件：
- `tests/test_mayan_calc.py`
- `references/validation-samples.md`

### 7. 现在最适合哪些运行时？

当前已经整理好的版本包括：
- Codex / Claude 风格 skill
- OpenClaw
- Hermes

后续还可以继续扩展到更多 agent 或自动化工作流环境。

## 功能特性

### 核心功能
- **星系印记计算** — 阳历生日 → Kin号 + 图腾 + 调性
- **五大天赋盘** — 主印记·支持·引导·挑战·隐藏推动完整排盘
- **深度解读报告** — 每个位置的含义、成因、运用方法

### 解读功能
- **小白友好** — 用比喻和生活化语言解释所有概念
- **事业天赋指导** — 根据五大盘建议职业方向与工作方式
- **情感天赋指导** — 关系中的天赋表达和爱的语言
- **成长路径指引** — 从隐藏推动到引导的完整修炼路线图

### 进阶功能
- **流年运势** — 计算任意年份流年Kin，与本命盘对比解读
- **双人合盘** — 图腾互位分析 + 颜色/调性关系 + 合盘Kin
- **波符解读** — 所属波符与波符内位置分析
- **对话式问答** — 针对具体人生问题提供天赋视角的回答

## 安装方法

### 方法一：符号链接（推荐）

```bash
# 克隆仓库
git clone https://github.com/joyozhang333-lgtm/mayan-kin.git

# Codex
mkdir -p ~/.codex/skills
ln -s "$(pwd)/mayan-kin" ~/.codex/skills/mayan-kin

# Claude Code
mkdir -p ~/.claude/skills
ln -s "$(pwd)/mayan-kin" ~/.claude/skills/mayan-kin
```

### 方法二：直接复制

```bash
git clone https://github.com/joyozhang333-lgtm/mayan-kin.git
cp -r mayan-kin ~/.codex/skills/mayan-kin
cp -r mayan-kin ~/.claude/skills/mayan-kin
```

## 使用方法

安装后，在 Codex / Claude Code 中直接输入触发词即可：

```
> 帮我看看玛雅天赋，我是1990年3月15日出生的

> 我想看看我的流年运势，1988-06-20，看看2026年

> 帮我合盘，我1990-03-15，他1992-07-20

> 我是Kin 164，帮我解读一下五大天赋盘

> 蓝猴图腾的人适合什么工作？
```

### 命令行计算工具

也可以直接运行 Python 脚本：

```bash
# 基础排盘
python3 scripts/mayan_calc.py 1990-03-15

# 流年运势
python3 scripts/mayan_calc.py 1990-03-15 --yearly 2026

# 双人合盘
python3 scripts/mayan_calc.py 1990-03-15 --compatibility 1992-07-20

# JSON 格式输出
python3 scripts/mayan_calc.py 1990-03-15 --json
```

## 目录结构

```text
mayan-kin/
├── mayan_kin/
│   ├── __init__.py               ← 可复用 Python API
│   └── core.py                   ← 计算核心与格式化逻辑
├── SKILL.md                      ← 核心技能定义
├── ETHICS.md                     ← 伦理准则
├── README.md                     ← 本文件
├── LICENSE                       ← MIT 开源协议
├── docs/
│   ├── README.md                 ← 文档导航页
│   ├── cli.md                    ← CLI 参考与 usage
│   ├── report.md                 ← report 命令说明
│   ├── json-contract.md          ← JSON 契约说明
│   ├── kin-calculator.md         ← 英文落地页
│   └── v2-roadmap.md             ← v2 / v1.0 路线图
├── runtimes/
│   ├── README.md                 ← 多运行时适配说明
│   ├── openclaw/AGENTS.md        ← OpenClaw 版本
│   ├── openclaw/DEMO.md          ← OpenClaw 示例对话
│   ├── hermes/SYSTEM_PROMPT.md   ← Hermes 版本
│   └── hermes/DEMO.md            ← Hermes 示例对话
├── references/
│   ├── README.md                 ← 知识卡导航页
│   ├── knowledge-index.json      ← 机读知识索引
│   ├── 20-seals.md               ← 20图腾详解
│   ├── 13-tones.md               ← 13调性详解
│   ├── five-destiny.md           ← 五大天赋位详解
│   ├── yearly-fortune.md         ← 流年运势分析方法
│   ├── compatibility.md          ← 双人合盘方法
│   ├── guidance.md               ← 天赋运用指导
│   ├── validation-samples.md     ← 权威样本校验基线
│   ├── colors-wavespell.md       ← 颜色与波符
│   └── career-emotion.md         ← 事业与情感应用
└── scripts/
    └── mayan_calc.py             ← CLI 入口
```

## 开发验证

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

## 多运行时版本

- `SKILL.md`：Codex / Claude 风格的 skill 定义
- `SKILL.md` + `references/knowledge-index.json`：推荐的技能路由入口，先索引再最小加载知识卡
- `docs/README.md`：文档导航页
- `docs/cli.md`：CLI usage 与参数说明
- `docs/report.md`：report 命令说明
- `docs/json-contract.md`：JSON 契约说明
- `references/README.md`：知识卡导航页
- `references/knowledge-index.json`：机读知识索引
- `runtimes/openclaw/AGENTS.md`：OpenClaw 对应版本
- `runtimes/openclaw/DEMO.md`：OpenClaw 示例对话
- `runtimes/hermes/SYSTEM_PROMPT.md`：Hermes 对应版本
- `runtimes/hermes/DEMO.md`：Hermes 示例对话

三者共用同一套 `mayan_kin/core.py` 计算逻辑与 `references/` 知识库，后续升级时只需要维护一套核心。

## 知识体系

本 skill 基于以下体系构建：

- **卓尔金历 (Tzolkin)**: 玛雅神圣历法，260天为一个周期
- **Dreamspell**: José Argüelles 基于玛雅历法创建的现代解读体系
- **13月亮历 (13 Moon Calendar)**: Law of Time 组织推广的和谐时间系统

## 参考资源

- [Law of Time](https://lawoftime.org/) — 13月亮历官方
- [MayanKin](https://mayankin.com/) — 卓尔金历基础教学
- [Foundation for the Law of Time](https://lawoftime.org/lawoftime/fifth-force-oracle.html) — 第五力神谕

## 开源协议

MIT License — 自由使用、修改、分发。

## 贡献

欢迎提 Issue 和 PR。

特别欢迎以下方向的贡献：
- 图腾、调性、五大天赋盘的解释深化
- 流年、合盘、波符等进阶维度的扩展
- 更多语言版本的 README、提示词和解释模板
- 计算算法的验证、测试样本补充与稳定性优化
- 新的运行时适配，例如更多 agent / bot / workflow 环境
- 更适合咨询、内容产品、课程产品的输出格式

建议贡献流程：

1. 先提 Issue，说明你想解决的问题或补充的方向
2. 如果涉及算法调整，请同时补测试或样本依据
3. 如果涉及解释层修改，请尽量保持非宿命论、非恐吓式表达
4. 提 PR 时简要说明：
   - 改了什么
   - 为什么改
   - 如何验证

在贡献前，建议先阅读：
- `SKILL.md`
- `ETHICS.md`
- `references/validation-samples.md`
- `tests/test_mayan_calc.py`

---

> In Lak'ech — 我是另一个你 🌀
