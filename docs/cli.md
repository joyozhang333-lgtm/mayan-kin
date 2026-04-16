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
- `--style` - 选择报告风格：`beginner / consulting / professional`
- `--route-query` - 根据自然语言问题推荐知识卡
- `--contract` - 输出 CLI / JSON 契约说明

## Output Precedence

输出模式优先级固定为：

1. `--contract`
2. `--route-query`
3. `--report`
4. `--json`
5. 默认文本输出

这意味着如果你同时传了多个输出模式，`mayan_calc.py` 会先执行优先级更高的那个。

## Examples

```bash
python3 scripts/mayan_calc.py 1995-03-03
python3 scripts/mayan_calc.py 1995-03-03 --json
python3 scripts/mayan_calc.py --route-query "我想看流年和事业方向"
python3 scripts/mayan_calc.py 1995-03-03 --report
python3 scripts/mayan_calc.py 1995-03-03 --report --style consulting
python3 scripts/mayan_calc.py 1995-03-03 --yearly 2026
python3 scripts/mayan_calc.py 1995-03-03 --compatibility 1992-07-20
python3 scripts/mayan_calc.py --contract
```

## Exit Codes

- `0` - 成功
- `1` - 输入不合法、日期解析失败、或缺少必填参数

## Notes

- 默认文本输出适合人工阅读。
- `--json` 适合前端、数据库、自动化脚本和 AI 二次处理。
- `--route-query` 适合 runtime 先决定要加载哪几张知识卡。
- `--report` 适合直接给用户看的说明书。
- `--style` 只影响报告模式，不影响默认文本和 JSON 结构。
- `--contract` 适合对接前先确认接口边界。
