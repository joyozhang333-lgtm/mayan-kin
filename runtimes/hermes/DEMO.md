# Hermes Demo

## Example System Usage

System Prompt:

`runtimes/hermes/SYSTEM_PROMPT.md`

User:

```text
我想看流年运势，生日是 1988-06-20，帮我看看 2026。
```

Hermes 执行建议：

1. 调用 `python3 scripts/mayan_calc.py 1988-06-20 --yearly 2026 --json`
2. 先输出本命，再补充 2026 流年
3. 用“倾向 / 可能 / 适合探索”的语言，而不是宿命式判断

## Example Response Shape

```text
先看本命，你的核心频率决定了你长期稳定的表达方式；再看 2026 流年，它更像是这一年被点亮的主题。

如果 2026 的流年印记和你的本命支持位或挑战位形成呼应，通常意味着这一年会更明显地推动你去处理某类课题，例如关系、表达、边界、创造或执行。

我可以继续往下展开两种版本：
1. 偏灵性/象征解释版
2. 偏现实/事业关系落地版
```
