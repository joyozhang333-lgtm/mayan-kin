# 🌀 Mayan Destiny — 玛雅天赋 Claude Code Skill

基于卓尔金历 (Tzolkin) / Dreamspell 体系的专业玛雅天赋解读技能，为 [Claude Code](https://claude.ai/claude-code) 打造。

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
git clone https://github.com/joyozhang333-lgtm/mayan-destiny.git

# 创建符号链接到 Claude Code skills 目录
mkdir -p ~/.claude/skills
ln -s $(pwd)/mayan-destiny ~/.claude/skills/mayan-destiny
```

### 方法二：直接复制

```bash
git clone https://github.com/joyozhang333-lgtm/mayan-destiny.git
cp -r mayan-destiny ~/.claude/skills/mayan-destiny
```

## 使用方法

安装后，在 Claude Code 中直接输入触发词即可：

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

```
mayan-destiny/
├── SKILL.md                  ← 核心技能定义
├── ETHICS.md                 ← 伦理准则
├── README.md                 ← 本文件
├── LICENSE                   ← MIT 开源协议
├── references/
│   ├── 20-seals.md               ← 20图腾详解
│   ├── 13-tones.md               ← 13调性详解
│   ├── five-destiny.md           ← 五大天赋位详解
│   ├── yearly-fortune.md         ← 流年运势分析方法
│   ├── compatibility.md          ← 双人合盘方法
│   ├── guidance.md               ← 天赋运用指导
│   ├── colors-wavespell.md       ← 颜色与波符
│   └── career-emotion.md         ← 事业与情感应用
└── scripts/
    └── mayan_calc.py             ← 玛雅历计算工具
```

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
