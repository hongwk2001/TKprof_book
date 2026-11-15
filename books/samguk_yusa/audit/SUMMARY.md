# Overnight run — 2026-09-14 10:18

model: `gemma4:12b`

## Stages

| stage | exit | minutes |
|---|---:|---:|
| 2-audit | 0 | 0.0 |
| 3-llm-audit | 0 | 26.2 |
| 4-migrate | 0 | 0.0 |

## Alignment

- 271/271 items aligned

## Cards (vs werther: ko mean 101 / max 186, en mean 197 / max 300, 0 over 300)

- rows **1103**
- ko mean 90, max 147
- en mean 214, max 375
- en over 300: **58**

## Findings

- deterministic (`audit/logs/2-audit.log`): **10 high**, 44 med
- semantic (`audit/problems.md`): **93** — {'SHIFTED': 13, 'OMITTED': 28, 'EXTRA': 16, 'MISSING': 36}

## Read in this order

1. `audit/problems.md` — SHIFTED first, that is the defect you heard
2. `audit/logs/2-audit.log` — every `[high]` line
3. `audit/logs/4-migrate.log` — any chapter it REFUSED to write
