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

欢迎提 Issue 和 PR！特别欢迎：
- 图腾和调性的更深度解读
- 更多语言的翻译
- 计算算法的验证和优化
- 新的解读维度（如地球家族、色彩城堡等）

---

> In Lak'ech — 我是另一个你 🌀
