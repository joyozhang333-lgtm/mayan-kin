# 权威样本校验基线

这份样本表用于验证 `mayan-kin` 的核心计算是否与 Law of Time 体系公开锚点一致。

## 样本选择原则

- 优先选用 Law of Time 公开页面中明确写出的 `Kin + 图腾 + 调性`
- 以每年 7 月 26 日的新年锚点为主，因为该日期在公开资料中最常见、最稳定
- 这些样本用于程序回归校验，不代替更广泛的学术或历史争议判断

## 样本表

| 日期 | 期望 Kin | 期望印记 | 来源 |
|------|-----------|----------|------|
| 1997-07-26 | Kin 44 | Yellow Overtone Seed | [Star Travelers Almanac - 7Storm Moon09](https://lawoftime.org/pdfs/Star-Travelers-Almanac-7Storm-Moon09.pdf) |
| 2012-07-26 | Kin 59 | Blue Resonant Storm | [Noos-letter Issue #26](https://www.lawoftime.org/noos-letter/issue026-complete.html) |
| 2013-07-26 | Kin 164 | Yellow Galactic Seed | [Annual Ring Oracle - 8Seed](https://www.lawoftime.org/thirteenmoon/annualoracle-8seed.html) |
| 2014-07-26 | Kin 9 | Red Solar Moon | [Noos-letter Issue #60](https://lawoftime.org/noos-letter/issue060-complete.html) |

## 使用方式

程序测试中应至少验证：

1. 日期转 Kin 是否与上表一致
2. Kin 对应的图腾与调性名称是否一致
3. 后续如替换参考锚点或重写日期算法，这份表必须继续通过
