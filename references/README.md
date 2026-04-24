# References Index

`references/` 现在不再只是“很多解释文档放在一起”，而是 `mayan-kin` 的知识卡入口。

你可以把这里理解成两层：

- 人读入口：按主题快速找到要看的解释文档
- 机读入口：通过 `knowledge-index.json` 让 agent、脚本或生成流程按主题检索知识卡

## Start Here

- [knowledge-index.json](knowledge-index.json) - 机器可检索索引，包含主题、标签、适用场景和调用建议
- [20-seals.md](20-seals.md) - 20 图腾基础卡
- [13-tones.md](13-tones.md) - 13 调性基础卡
- [five-destiny.md](five-destiny.md) - 五大天赋位阅读框架
- [guidance.md](guidance.md) - 从盘走到行动建议的运用卡

## Advanced Cards

- [oracle.md](oracle.md) - 神谕十字 / 五位关系结构卡
- [earth-families.md](earth-families.md) - 地球家族 / 共振分组卡
- [yearly-fortune.md](yearly-fortune.md) - 年度趋势 / 流年说明卡
- [compatibility.md](compatibility.md) - 关系动力学 / 合盘卡
- [colors-wavespell.md](colors-wavespell.md) - 颜色与波符卡
- [career-emotion.md](career-emotion.md) - 事业与情感应用卡

## Validation

- [validation-samples.md](validation-samples.md) - 权威样本与公开锚点校验
- [scientific-validation-protocol.md](scientific-validation-protocol.md) - 科学盲测实验协议与 90 分定义
- [scientific-validation-readiness.json](scientific-validation-readiness.json) - 当前实验框架成熟度与待收集数据说明
- [blind-participants-template.json](blind-participants-template.json) - 盲测参与者输入模板
- [blind-responses-template.json](blind-responses-template.json) - 盲测回答模板
- [public-figure-benchmark.json](public-figure-benchmark.json) - 公开人物生日、生平主题与解读贴合度 benchmark
- [public-figure-benchmark-results.json](public-figure-benchmark-results.json) - 最近一次公开人物 benchmark 结果

## How To Use This Layer

如果你是人类读者：

1. 先看基础卡：图腾、调性、五大位
2. 再看主题卡：流年、关系、波符、地球家族
3. 最后回到 `guidance.md`，把概念翻译成行动建议

如果你是开发者或 agent：

1. 先读取 `knowledge-index.json`
2. 根据 `keywords`、`use_cases` 和 `when_to_load` 选最小知识集合
3. 或者直接调用 `python3 scripts/mayan_calc.py --route-query "<用户问题>"`
4. 避免一次性加载全部文档，优先按问题场景组合卡片

## Card Design Rules

- 每张卡优先回答“它能解释什么”，而不是先堆术语
- 每张卡都尽量包含概念、读法、适用场景和输出模板
- 机器索引只做导航，不重复正文内容
