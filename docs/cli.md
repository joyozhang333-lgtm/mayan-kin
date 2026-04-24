# CLI Reference

`mayan_calc.py` 是 `mayan-kin` 的命令行入口。它负责把阳历生日转换成 Kin、五大天赋盘、流年、合盘和个人说明书。

## Usage

```bash
python3 scripts/mayan_calc.py [birthday] [options]
```

- `birthday` 是普通模式的必填参数，格式为 `YYYY-MM-DD`
- `--contract` 模式不需要 `birthday`

## Options

- `--compatibility / -c` - 合盘对象的生日
- `--yearly / -y` - 计算指定年份的流年结果
- `--json / -j` - 输出机器可读 JSON
- `--report / -r` - 输出个人说明书
- `--style` - 选择报告风格：`basic / deep`
- `--auto-answer` - 自动推荐知识卡和报告风格；提供生日时直接出报告
- `--auto-answer` 也会自动推荐 `personal / yearly / compatibility / combined` 报告模式
- `--route-query` - 根据自然语言问题推荐知识卡
- `--contract` - 输出 CLI / JSON 契约说明

## Output Precedence

输出模式优先级固定为：

1. `--contract`
2. `--auto-answer`
3. `--route-query`
4. `--report`
5. `--json`
6. 默认文本输出

这意味着如果你同时传了多个输出模式，`mayan_calc.py` 会先执行优先级更高的那个。

## Examples

```bash
python3 scripts/mayan_calc.py 1995-03-03
python3 scripts/mayan_calc.py 1995-03-03 --json
python3 scripts/mayan_calc.py --auto-answer "我想看流年和事业方向"
python3 scripts/mayan_calc.py 1995-03-03 --auto-answer "我想看流年和事业方向" --yearly 2026
python3 scripts/mayan_calc.py --route-query "我想看流年和事业方向"
python3 scripts/mayan_calc.py 1995-03-03 --report
python3 scripts/mayan_calc.py 1995-03-03 --report --style deep
python3 scripts/mayan_calc.py 1995-03-03 --yearly 2026
python3 scripts/mayan_calc.py 1995-03-03 --compatibility 1992-07-20
python3 scripts/mayan_calc.py --contract
```

## Scientific Validation Helpers

这些脚本不属于 `mayan_calc.py` 主入口，但属于仓库的科学验证工具链：

```bash
python3 scripts/generate_blind_trial_packets.py \
  --participants references/blind-participants-template.json \
  --candidate-count 5 \
  --packets-out /tmp/mayan-blind-packets.json \
  --key-out /tmp/mayan-blind-key.json

python3 scripts/evaluate_blind_trials.py \
  --responses references/blind-responses-template.json \
  --key /tmp/mayan-blind-key.json \
  --packets /tmp/mayan-blind-packets.json \
  --min-sample-size 30 \
  --min-score 90
```

盲测评分会同时输出正确率、随机基线、p 值和 `scientific_accuracy_score`。

### Public Figure Holdout

```bash
python3 scripts/collect_public_figures_wikidata.py \
  --limit 1600 \
  --min-records 1000 \
  --output references/public-figures-wikidata-1000.json

python3 scripts/evaluate_public_figure_holdout.py \
  --dataset references/public-figures-wikidata-1000.json \
  --protocol references/frozen-scoring-protocol-v1.json \
  --split holdout \
  --write references/public-figure-holdout-results.json
```

该评估是公开人物职业 / 生平证据的 forced-choice benchmark，不等于命运系统科学证明。当前 holdout 结果低于随机基线，必须如实报告。

### Detailed Biography Labels v2

```bash
python3 scripts/enrich_public_figure_history_labels.py \
  --input references/public-figures-wikidata-expanded.json \
  --output references/public-figures-history-labels-v2.json \
  --cutoff-year 2010

python3 scripts/evaluate_history_label_holdout.py \
  --dataset references/public-figures-history-labels-v2.json \
  --protocol references/frozen-scoring-protocol-v2.json \
  --split holdout \
  --write references/history-label-holdout-results-v2.json

python3 scripts/evaluate_time_split_predictions.py \
  --dataset references/public-figures-history-labels-v2.json \
  --protocol references/frozen-scoring-protocol-v2.json \
  --split holdout \
  --write references/time-split-prediction-results-v2.json
```

v2 会标注核心成就、反复主题、重大转折、关系模式、公众表达、精神/价值主题、危机与重生。标注脚本不导入 `mayan_kin`，避免在答案标签阶段看到 Kin。

### Prospective Predictions

```bash
python3 scripts/generate_prospective_predictions.py \
  --subjects references/prospective-subjects-template.json \
  --target-year 2027 \
  --output /tmp/mayan-prospective-registry.json

python3 scripts/evaluate_prospective_predictions.py \
  --registry /tmp/mayan-prospective-registry.json \
  --outcomes references/prospective-outcomes-template.json \
  --min-score 90
```

前瞻预测必须先锁定，再等待未来证据出现后评估。

## Exit Codes

- `0` - 成功
- `1` - 输入不合法、日期解析失败、或缺少必填参数

## Notes

- 默认文本输出适合人工阅读。
- `--json` 适合前端、数据库、自动化脚本和 AI 二次处理。
- `--auto-answer` 会先输出自动规划结果，再按推荐的风格和报告模式渲染报告。
- `--route-query` 适合 runtime 先决定要加载哪几张知识卡。
- `--report` 适合直接给用户看的说明书。
- `--style` 只影响报告模式，不影响默认文本和 JSON 结构。
- `--contract` 适合对接前先确认接口边界。
