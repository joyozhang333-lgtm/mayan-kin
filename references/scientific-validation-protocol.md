# Scientific Validation Protocol

本文件定义 `mayan-kin` 用来评估“玛雅天赋系统是否具有高于随机的客观识别能力”的实验协议。

核心原则：**可以验证，也可以失败。** 如果盲测结果没有显著高于随机，系统不能宣称科学证明有效。

## 当前结论状态

- 当前产品具备实验框架：是。
- 当前是否已经科学证明命运系统客观准确：否。
- 当前可给出的真实科学准确率：需要真实盲测数据后才能计算。
- 当前目标：让实验框架、数据结构、盲测流程和评分脚本达到可复核的 90 分以上成熟度。

## 实验问题

主问题：

> 在不知道生日、姓名、Kin 号、图腾和调性的情况下，参与者能否从多份候选报告中，显著高于随机概率地选出自己的报告？

如果 5 选 1，随机命中率是 20%。

## 预注册假设

### H0 零假设

参与者选择正确报告的概率不高于随机概率。

### H1 备择假设

参与者选择正确报告的概率显著高于随机概率。

## 最小实验设计

- 样本量：至少 30 人，推荐 100 人以上。
- 候选数：每位参与者至少 5 份报告，1 份真实报告 + 4 份随机他人报告。
- 盲法：参与者不能看到生日、姓名、Kin 号、图腾、调性或任何可直接识别身份的信息。
- 随机化：候选报告顺序由脚本随机打乱，随机种子记录在实验日志中。
- 评分方式：参与者只选择“最像自己的一份”，也可以额外给每份报告打 1 到 5 分。
- 主要指标：Top-1 correct accuracy。
- 统计检验：单侧二项检验，检验正确率是否高于随机命中率。
- 显著性阈值：`p < 0.001`。
- 产品目标：`scientific_accuracy_score >= 90`。

## 90 分定义

`scripts/evaluate_blind_trials.py` 会输出 `scientific_accuracy_score`。

该分数不是主观评分，而是由以下因素共同决定：

- 样本量是否达到最低要求。
- 正确匹配率是否高于随机概率。
- 结果是否达到统计显著。
- 正确率是否接近预设目标正确率。

默认参数：

- `min_sample_size = 30`
- `alpha = 0.001`
- `target_rate = 0.60`
- `min_score = 90`

在 5 选 1 的实验中，随机是 20%。如果真实正确率显著高于随机，并接近或超过 60%，系统才可能接近满分。

## 数据流程

### 1. 准备参与者文件

使用 `references/blind-participants-template.json` 作为模板。

只需要收集：

- `participant_id`
- `birth_date`

不要在盲测包里放真实姓名。

### 2. 生成盲测包和答案 key

```bash
python3 scripts/generate_blind_trial_packets.py \
  --participants references/blind-participants-template.json \
  --candidate-count 5 \
  --packets-out /tmp/mayan-blind-packets.json \
  --key-out /tmp/mayan-blind-key.json
```

给参与者的只能是 `mayan-blind-packets.json`。

`mayan-blind-key.json` 必须由实验组织者保管，不能给参与者或评分者提前看到。

### 3. 收集参与者回答

使用 `references/blind-responses-template.json` 作为模板。

每条回答至少包含：

- `trial_id`
- `selected_label`

### 4. 计算科学准确率分数

```bash
python3 scripts/evaluate_blind_trials.py \
  --responses /tmp/mayan-blind-responses.json \
  --key /tmp/mayan-blind-key.json \
  --packets /tmp/mayan-blind-packets.json \
  --min-sample-size 30 \
  --min-score 90
```

## 防止自证循环

为了避免“先看答案再调解释”的循环，正式实验必须遵守：

- 在生成盲测包后冻结当前代码版本。
- 在收集完所有回答前，不允许改解释规则。
- 不允许把参与者姓名、职业、公开身份、社交媒体内容输入生成器。
- 不允许人工修改某个参与者的报告。
- 不允许删除低分样本，除非预注册排除标准已经写清。

## 迭代规则

如果没有达到 90 分：

1. 固定实验结果，不重写历史数据。
2. 分析失败项：报告太泛、候选太相似、问题太暗示、解释层不够具体。
3. 在新版本中改解释层或报告结构。
4. 用新的参与者样本重新跑盲测。
5. 不允许用同一批已经看过答案的数据反复调到 90。

## 可以声称什么

如果通过：

> 在预注册的 N 人、K 选 1 盲测中，`mayan-kin` 报告的正确匹配率显著高于随机，达到 `scientific_accuracy_score >= 90`。

不应该声称：

> 科学证明命运绝对存在。

更严谨的说法是：

> 该版本报告在特定盲测任务中表现出高于随机的自我识别能力。

## 当前产品成熟度

当前已经具备：

- 盲测包生成器
- 答案 key 分离
- 符号隐藏，避免参与者靠 Kin/图腾识别
- 客观评分脚本
- 二项检验
- 样本量阈值
- 90 分门槛
- 测试覆盖

因此当前是“可开始科学验证”的状态，而不是“已经科学证明”的状态。

## 公开人物 1000+ 样本 Holdout

公开人物样本用于测试“出生日期生成的现实表达标签，是否能匹配公开职业 / 生平证据”。它是产品质量与可证伪能力测试，不等同于人格或命运的科学证明。

数据集：

- `references/public-figures-wikidata-1000.json`
- 来源：Wikidata Query Service
- 当前规模：`1425` 条公开人物记录
- 划分：`1012` train / `201` dev / `212` holdout
- 划分方式：`frozen-scoring-protocol-v1.json` 中的 hash seed

冻结协议：

- `references/frozen-scoring-protocol-v1.json`

评估命令：

```bash
python3 scripts/evaluate_public_figure_holdout.py \
  --dataset references/public-figures-wikidata-1000.json \
  --protocol references/frozen-scoring-protocol-v1.json \
  --split holdout \
  --write references/public-figure-holdout-results.json
```

当前结果：

- Holdout 样本量：`212`
- 命中：`15`
- 准确率：`7.08%`
- 5 选 1 随机基线：`20.0%`
- 结论：未通过，不显著，不能声称 90 分。

## 前瞻预测

前瞻预测必须先锁定预测，再等待未来证据出现后评分。

生成预测登记表：

```bash
python3 scripts/generate_prospective_predictions.py \
  --subjects references/prospective-subjects-template.json \
  --target-year 2027 \
  --output /tmp/mayan-prospective-registry.json
```

未来证据出现后评分：

```bash
python3 scripts/evaluate_prospective_predictions.py \
  --registry /tmp/mayan-prospective-registry.json \
  --outcomes references/prospective-outcomes-template.json \
  --min-score 90
```

前瞻预测在目标年份结束前不能算成功。
