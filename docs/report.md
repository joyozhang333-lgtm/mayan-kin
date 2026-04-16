# `--report` Command

`--report` 是 `mayan-kin` 的指导型输出模式。它不是单纯打印 Kin 编号，而是把计算结果整理成更适合阅读和咨询场景的个人说明书。

## What It Includes

报告会围绕以下部分展开：

- 核心摘要
- 五大位置解释
- 成长路径
- 行动建议

这些内容来自同一套计算核心，但会被包装成更容易读懂、也更容易继续追问的结构。

## When To Use It

适合这些场景：

- 小白用户第一次看自己的玛雅天赋
- 咨询、陪伴、课程或内容产品
- 想把“计算结果”转成“可以行动的建议”

## Examples

```bash
python3 scripts/mayan_calc.py 1995-03-03 --report
python3 scripts/mayan_calc.py 1995-03-03 --report --yearly 2026
```

## Behavior

- `--report` 的优先级高于 `--json`
- `--report` 可以和 `--yearly` 一起使用
- 当同时请求多个输出模式时，报告模式会优先执行

## Reading Tip

如果你要把输出接到程序里，请用 `--json`。
如果你要给真人阅读，请用 `--report`。
如果你要先看接口边界，请用 `--contract`。
