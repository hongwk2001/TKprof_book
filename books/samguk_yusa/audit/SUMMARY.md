# Overnight run — 2026-09-13 22:03

model: `gemma4:12b`

## Stages

| stage | exit | minutes |
|---|---:|---:|
| 1-translate | 0 | 77.8 |
| 2-audit | 0 | 0.0 |
| 3-llm-audit | 0 | 26.5 |
| 4-migrate | 0 | 0.0 |

## Alignment

- 271/271 items aligned

## Cards (vs werther: ko mean 101 / max 186, en mean 197 / max 300, 0 over 300)

- rows **1245**
- ko mean 84, max 160
- en mean 189, max 473
- en over 300: **41**

## Findings

- deterministic (`audit/logs/2-audit.log`): **2 high**, 23 med
- semantic (`audit/problems.md`): **59** — {'EXTRA': 11, 'SHIFTED': 15, 'MISSING': 31, 'OMITTED': 2}

## Read in this order

1. `audit/problems.md` — SHIFTED first, that is the defect you heard
2. `audit/logs/2-audit.log` — every `[high]` line
3. `audit/logs/4-migrate.log` — any chapter it REFUSED to write
