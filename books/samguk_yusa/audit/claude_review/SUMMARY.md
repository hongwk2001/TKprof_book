# Claude review of the local-LLM translation audit — 삼국유사 전체

Reviewed all 24 chapters' findings from `audit/problems.md` (93 semantic-equivalence
flags, from `llm_audit.py`) and `audit/quality.md` (489 term-accuracy/fluency flags, from
the new `quality_audit.py`), grounding every verdict in the actual hanmun rather than
trusting either pass's own notes. Per-chapter detail lives in `ch_01.md` … `ch_24.md` in
this folder.

## Tally (582 raw findings → ~530 distinct issues after merging equiv+quality flags on the same defect)

| Verdict | Count | Meaning |
|---|---:|---|
| ACCEPT | ~383 | Real issue, suggested fix (mine or the audit's) is correct — safe to apply |
| REVISE | ~90 | Real issue, but the audit's own fix was wrong or incomplete — my fix given instead |
| REJECT | ~41 | False positive — audit flagged something that wasn't actually wrong |
| NEEDS-HUMAN | ~16 | Real issue, genuinely uncertain reading — flagged with a candidate but not applied |

## What this confirms from your original ask

Found the exact 공자/Confucius-class error you described, more than once:
- **ch_15 P0003 n3**: 公 (純貞公, "the lord") mistranslated as **"Confucius"**.
- **ch_12 P0012 n3**: 三十三天 ("the Heaven of the Thirty-Three," a Buddhist term)
  misread as "thirty-three **thousand**" — confusing 天 (heaven) with its homophone 千
  (thousand).
- A whole family of the same failure mode recurs throughout: honorific pronouns or
  titles (公, 王師, 虜足下) mistaken for personal names, and vice versa — real names
  (Yeosin→Yusin, Norin→"the elder") flattened into common words.

## What surprised me: the audit tool's own fixes aren't safe to trust blind

This is the main finding for how you should treat this pipeline going forward:
- **~90 of the audit's own "fixes" were themselves wrong**, sometimes introducing new
  errors (turning a real historical detail — Wei Shan's execution — into a fabricated
  one; making a male king character become pregnant; inventing nonexistent people like
  "Wanggi" or "Jang-gong" from misread grammar).
- Several **fix_en values are partial clauses, not full paragraphs**, with nothing in
  the data to tell them apart — a script that blindly string-replaces on them will
  silently delete real content. Any future "apply" step must diff-check, not
  auto-replace.
- **~41 flags were false alarms** — the local model's own audit note misread its own
  Korean or hallucinated a problem that wasn't in the text.

## Systemic patterns worth a glossary entry, not a one-off fix

1. **虎-for-武 naming taboo** (already documented for 周虎王 in `glossary.json`, but the
   substitution recurs elsewhere): 光虎帝/建虎/興虎/文虎王/虎王 all appeared across
   chapters 1, 2, 5, 10, 11, 12 — confirmed exhaustive via corpus grep, all now fixed
   in the per-chapter reviews. Worth generalizing the glossary rule from "周虎王" to the
   whole 虎-substitution pattern so future retranslation passes catch it automatically.
2. **"Nth 王代/至Nth王" = the Nth king, not the Nth year of his reign** — caused real
   errors in ch_04 (Heongang) and ch_10 (Gyeongmyeong); likely worth a standing glossary
   note given how often this construction recurs across the corpus (see the sweep list
   in ch_10.md — ~37 occurrences total, only a few individually checked).
3. **公/王師/虜足下 as honorifics, not names** — this class of error (a polite/insulting
   2nd- or 3rd-person address mistaken for a proper name) recurred in at least 8
   chapters. Worth a standing glossary note: "check whether a single-character or
   two-character 'name' next to a title actually has a hanja antecedent nearby before
   trusting it as a person."

## NEEDS-HUMAN — the 16 flagged for your own read

- ch_02: P0002 n3 ("Waljok" — unresolved segmentation in a compressed classical
  citation), P0020 n1 (a likely mis-parsed citation title)
- ch_03: P0002 n=None (dropped author's-note parenthetical, no surrounding text to place it in)
- ch_04: P0010 n=None (dropped village-affiliation list), P0015 n3 ("Two Sages" epithet scope)
- ch_08: P0008 n1 (ambiguous agency in "who reported what to the king")
- ch_09: P0004 n=None (two dropped author's-note parentheticals), P0003 n5 ("Chajipsa" office title)
- ch_11: P0004 n2 (a name-list segmentation ambiguity)
- ch_13: P0012 n4 (a name+rank+variant-reading knot)
- ch_21: P0001 n3/n4 (a dense multi-generation genealogy)
- ch_22: P0005 n1 (a name-list segmentation ambiguity), P0007 n5 (a name I couldn't
  locate in the given Korean text to verify)
- ch_23: P0004 n=None (dropped "the country was called Great Garak," no placement
  context), P0014 n3 (title-reform mechanics)

## What I did not do

- Did not re-run the full-corpus audit (verified unnecessary — the shipped app content
  matches the existing 09-14 overnight run exactly, per file mtimes).
- Did not apply any fix to `batches/result_ch_*.json` or the Book_apps assets — every
  fix above is written but not yet committed to the actual translation.
- Did not touch anything in `manual.json` or the six pinned hyangga — none of the 582
  findings from either audit pass touched them (both passes already skip `manual`
  items), and I confirmed no pinned-poem text appeared incidentally in the surrounding
  prose I reviewed.
