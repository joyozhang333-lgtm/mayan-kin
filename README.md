# 🌀 mayan-kin · 玛雅天赋解读

> 输入一个生日，解锁一套专属于你的宇宙天赋蓝图。

`mayan-kin` 是一个开源的玛雅天赋 / Dreamspell / Tzolkin 解读项目，面向 AI 助手、创作者、咨询场景和个人探索者。
它把阳历生日转换为可计算、可验证的星系印记信息，包括 `Kin`、图腾、调性、五大天赋盘、波符、流年与合盘结果，
同时把这些结果翻译成普通人也能理解的解释语言，以及专业使用者可继续复用的结构化输出。

如果你是小白，这个项目能帮你从零理解“玛雅天赋到底在看什么”：什么是 Kin、什么是图腾、什么是调性、五大位置为什么这样排、这些能量在事业、情感和成长里通常如何体现。
你不需要先懂术语，也不需要会算历法，只要输入一个阳历生日，就能得到一份完整、相对友好、不宿命化的解读入口。

如果你是专业使用者，这个项目也适合作为一个可扩展的基础设施层：
- 可以作为 AI agent / skill / prompt runtime 的底层计算模块
- 可以输出适合二次处理的 JSON 结果
- 可以接入 Codex、Claude、OpenClaw、Hermes 等不同运行时
- 可以作为咨询、内容创作、课程产品或研究型项目的计算与解释底座

项目当前同时强调三件事：
- **可用性**：让第一次接触玛雅天赋的人也能看懂、继续问下去、真的用起来
- **可复用性**：让开发者、研究者、咨询师可以把计算核心和解释框架接进自己的系统
- **可验证性**：核心计算支持脚本调用、测试基线和公开样本校验，而不是只停留在“神秘描述”

## Overview (English)

`mayan-kin` is an open-source Mayan Destiny / Dreamspell / Tzolkin interpretation project for AI assistants, creators, consultants, and self-exploration use cases.
It turns a Gregorian birth date into structured and reusable outputs such as `Kin`, solar seal, galactic tone, the five destiny positions, wavespell placement, yearly cycles, and compatibility data,
then translates those symbolic results into readable explanations for beginners and machine-friendly outputs for advanced workflows.

For beginners, the goal is simple: make Mayan Destiny understandable without assuming prior knowledge.
You do not need to know the terminology, calendar system, or oracle structure in advance.
You can start with one birth date and immediately get an explanation of what each position means, why it appears in the chart, and how it may show up in work, relationships, and personal growth.

For advanced users, this project is designed as a reusable foundation:
- a calculation core that can be imported into other tools
- JSON output for downstream processing
- runtime adapters for Codex, Claude-style skills, OpenClaw, and Hermes
- a practical base for consulting workflows, educational products, content generation, or research-oriented experimentation

In short, `mayan-kin` is built to be both accessible and rigorous:
- accessible enough for first-time users
- structured enough for builders
- explicit enough to test, validate, and improve over time

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
```

### 4. 查看流年或合盘

```bash
python3 scripts/mayan_calc.py 1990-03-15 --yearly 2026
python3 scripts/mayan_calc.py 1990-03-15 --compatibility 1992-07-20
```

### 5. 跑测试

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

如果你是要接进 AI 助手，而不是只在命令行里用：
- Codex / Claude 风格：看 `SKILL.md`
- OpenClaw：看 `runtimes/openclaw/AGENTS.md` 和 `runtimes/openclaw/DEMO.md`
- Hermes：看 `runtimes/hermes/SYSTEM_PROMPT.md` 和 `runtimes/hermes/DEMO.md`

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
├── runtimes/
│   ├── README.md                 ← 多运行时适配说明
│   ├── openclaw/AGENTS.md        ← OpenClaw 版本
│   ├── openclaw/DEMO.md          ← OpenClaw 示例对话
│   ├── hermes/SYSTEM_PROMPT.md   ← Hermes 版本
│   └── hermes/DEMO.md            ← Hermes 示例对话
├── references/
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
