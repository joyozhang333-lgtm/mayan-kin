# Kin Calculator

`mayan-kin` is an open-source **Kin calculator** for **Mayan Destiny**, **Dreamspell**, and **Tzolkin** charting.

If you want the full navigation for the docs, start here:

- [Documentation Index](README.md)
- [CLI Reference](cli.md)
- [Report Command](report.md)
- [JSON Contract](json-contract.md)

If you are searching for:

- Kin calculator
- Kin number calculator
- Mayan Destiny calculator
- Dreamspell calculator
- Tzolkin calculator
- Maya calendar calculator
- yearly Kin reading
- Mayan compatibility reading

this repository is built for that exact use case.

## What It Calculates

Given a Gregorian birth date, `mayan-kin` can calculate:

- `Kin number`
- `solar seal`
- `galactic tone`
- `five destiny positions`
- `wavespell position`
- `yearly reading`
- `compatibility reading`

## Who It Is For

This repository is useful for:

- people exploring Mayan Destiny for the first time
- creators writing about Dreamspell or Tzolkin
- consultants or facilitators using symbolic systems for self-exploration
- developers who want to integrate a Kin calculator into AI agents, skills, bots, or workflow tools

## Quick Example

```bash
python3 scripts/mayan_calc.py 1995-03-03
python3 scripts/mayan_calc.py 1995-03-03 --yearly 2026
python3 scripts/mayan_calc.py 1995-03-03 --compatibility 1992-07-20
python3 scripts/mayan_calc.py 1995-03-03 --json
```

## Why This Exists

Many repositories mention Dreamspell or Tzolkin as abstract ideas, but fewer provide:

- a reusable Kin calculator
- structured output
- yearly and compatibility features
- AI runtime adapters
- a beginner-friendly interpretation layer

`mayan-kin` is designed to cover all of those.

## Related Pages

- [README](../README.md)
- [Documentation Index](README.md)
- [validation samples](../references/validation-samples.md)
- [OpenClaw runtime](../runtimes/openclaw/AGENTS.md)
- [Hermes runtime](../runtimes/hermes/SYSTEM_PROMPT.md)
