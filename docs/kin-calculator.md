# Kin Calculator for Mayan Destiny, Dreamspell, and Tzolkin

`mayan-kin` is an open-source **Kin calculator** for **Mayan Destiny**, **Dreamspell**, **Tzolkin**, and **Maya calendar** workflows.

It helps you calculate a `Kin number` from a Gregorian birth date, read the related `solar seal`, `galactic tone`, and five destiny positions, and generate structured reports for yearly readings, compatibility readings, and AI-assisted interpretation.

Use this page if you are looking for:

- `Kin calculator`
- `Kin number calculator`
- `Mayan Destiny calculator`
- `Dreamspell calculator`
- `Tzolkin calculator`
- `Maya calendar calculator`
- `Galactic signature calculator`
- `Solar seal calculator`
- `Galactic tone calculator`
- `Mayan compatibility reading`
- `Yearly Kin reading`
- `Dreamspell birth chart`
- `Tzolkin birth chart`

## Documentation Navigation

If you want the full navigation for the repository docs, start here:

- [Documentation Index](README.md)
- [CLI Reference](cli.md)
- [Report Command](report.md)
- [JSON Contract](json-contract.md)

## What It Does

Given a Gregorian birth date, `mayan-kin` can calculate and explain:

- `Kin number`
- `solar seal`
- `galactic tone`
- `five destiny positions`
- `wavespell position`
- `yearly Kin reading`
- `compatibility reading`
- `color relationship`
- `tone relationship`
- beginner-friendly and deep interpretation reports
- JSON output for apps, databases, and AI agents

## Why Use This Kin Calculator?

Most users do not only want a Kin number. They want to understand what the Kin number means, how the solar seal and galactic tone interact, and how the result may show up in work, relationships, self-development, yearly cycles, and collaboration patterns.

`mayan-kin` combines calculation and interpretation:

- The calculation layer keeps the Kin, seal, tone, wavespell, yearly, and compatibility logic reusable.
- The report layer turns symbolic output into readable guidance.
- The deep interpretation layer adds trigger conditions, misread risks, validation questions, and minimum experiments.
- The runtime layer makes the same core usable in Codex, Claude-style skills, OpenClaw, Hermes, and other AI agent environments.

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

For a human-readable report:

```bash
python3 scripts/mayan_calc.py 1995-03-03 --report
python3 scripts/mayan_calc.py 1995-03-03 --report --style deep
```

For an AI or app integration:

```bash
python3 scripts/mayan_calc.py 1995-03-03 --json
python3 scripts/mayan_calc.py --contract
python3 scripts/mayan_calc.py --route-query "I want a yearly Kin reading and career direction"
```

## Why This Exists

Many repositories mention Dreamspell or Tzolkin as abstract ideas, but fewer provide:

- a reusable Kin calculator
- structured output
- yearly and compatibility features
- AI runtime adapters
- a beginner-friendly interpretation layer
- deep interpretation calibration for real-world reflection

`mayan-kin` is designed to cover all of those.

## Related Pages

- [README](../README.md)
- [Documentation Index](README.md)
- [validation samples](../references/validation-samples.md)
- [OpenClaw runtime](../runtimes/openclaw/AGENTS.md)
- [Hermes runtime](../runtimes/hermes/SYSTEM_PROMPT.md)
