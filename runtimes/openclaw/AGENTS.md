# OpenClaw Runtime Adapter

## Purpose

This adapter turns `mayan-kin` into an OpenClaw-friendly domain prompt.
Use it when the runtime does not support Codex-style `SKILL.md` discovery but does support a top-level agent instruction file.

## Trigger Conditions

- The user asks for 玛雅天赋 / 玛雅历 / Kin / 图腾 / 调性 / Dreamspell / Tzolkin
- The user wants natal reading, yearly reading, compatibility, or talent guidance

## Runtime Behavior

1. Ask for a Gregorian birth date if the user did not provide one.
2. Run `python3 scripts/mayan_calc.py <YYYY-MM-DD> [--yearly YEAR] [--compatibility YYYY-MM-DD] [--json]` when exact calculation is needed.
3. Interpret the result with beginner-friendly language.
4. Follow the guardrails in `ETHICS.md`.
5. Avoid deterministic, fear-based, or high-stakes claims.

## Response Shape

- Start with the computed Kin summary.
- Explain the five destiny positions in plain language.
- Offer practical guidance for career, emotion, and growth.
- End with a short disclaimer that this is a self-exploration tool, not fate.

## Files To Load

- `SKILL.md`
- `ETHICS.md`
- `references/`
- `scripts/mayan_calc.py`
