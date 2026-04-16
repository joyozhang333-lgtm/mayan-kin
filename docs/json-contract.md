# JSON Contract

这个页面说明 `mayan-kin` 的机器可读契约。目标是让前端、脚本、数据库、自动化系统和 AI agent 都能稳定消费输出。

## Contract Modes

### `--json`

`--json` 输出当前计算结果的结构化 JSON。顶层键如下：

- `birth_date`
- `destiny`
- `yearly`（可选）
- `compatibility`（可选）

### `--contract`

`--contract` 不计算生日结果，只输出 CLI 与 JSON 契约说明，方便对接前先看边界。

## `--json` Top-Level Shape

```json
{
  "birth_date": "1995-03-03",
  "destiny": {},
  "yearly": {
    "year": 2026,
    "destiny": {}
  },
  "compatibility": {}
}
```

## `destiny` Shape

`destiny` 来自 `serialize_destiny(destiny)`，实际包含：

- `kin`
- `main`
- `support`
- `guide`
- `challenge`
- `occult`
- `wavespell`

其中：

- `main` 包含 `seal`, `tone`, `seal_name`, `seal_en`, `tone_name`, `tone_en`, `color`, `keywords`, `tone_keywords`
- `support`, `guide`, `challenge` 包含 `seal`, `tone`, `seal_name`, `seal_en`, `tone_name`, `color`, `keywords`
- `occult` 与 `main` 一样，另外包含 `tone_keywords`
- `wavespell` 包含 `wavespell_number`, `wavespell_seal`, `wavespell_name`, `wavespell_en`, `position`, `start_kin`

## `yearly` Shape

`yearly` 只在传入 `--yearly` 时出现，结构为：

- `year`
- `destiny`

其中 `destiny` 的结构与普通 `destiny` 完全一致。

## `compatibility` Shape

`compatibility` 只在传入 `--compatibility` 时出现，结构为：

- `other_date`
- `other_kin`
- `b_in_a`
- `a_in_b`
- `combined_kin`
- `color_relation`
- `tone_relation`

## Stability Notes

- 顶层键是该版本最重要的稳定边界。
- 如果未来要破坏性改动 JSON 结构，应在新版本里显式说明。
- `--contract` 会优先于其他输出模式，因此适合作为接口验收入口。
