# The Muqaddimah: Greatest Hits Edition — Project Master Document

## 1. What This Book Is

**The 30 best pages of the Muqaddimah, in Ibn Khaldun's own voice, in plain English.**

Not a summary. Not a synthesis with modern examples. Not a full translation. The Muqaddimah is 700,000 words — nobody reads all of it, not even Zuckerberg. This edition finds the passages where Ibn Khaldun states his big ideas most clearly and vividly, renders them in comfortable modern English, and gets out of the way.

A curious lay reader finishes this in 90 minutes and understands exactly why the Muqaddimah has survived 650 years.

---

## 2. The Gap

| What exists | Problem |
|---|---|
| Rosenthal 3-volume translation (1958) | 1,600 pages. Academic footnotes. Nobody finishes it. |
| Dawood abridgment (1969) | Still scholarly in tone. Still 400+ pages. |
| Summary articles / YouTube videos | Secondhand. Reader never hears Ibn Khaldun's actual voice. |
| *The Collapse Code* (our archived Book 1) | Applies his framework — doesn't render his text. Makes claims that need fact-checking. |

**The gap:** A short, readable book where Ibn Khaldun speaks for himself. ~15,000–20,000 words. No fact-checking risk — every claim in the book is his claim.

---

## 3. Legal Basis

- Ibn Khaldun's Arabic original (1377 CE) is in the public domain worldwide.
- Rosenthal's translation (Princeton, 1958) is under copyright — we do not copy his wording.
- This is an **original plain-English rendering** worked from the source text. Not derived from any existing translation.
- Zero exposure to fact-checking challenges: the only claims in the book are Ibn Khaldun's own.

---

## 4. Book Concept

**Working title:** *The Muqaddimah: Essential Passages in Plain English*

**Subtitle options:**
- *The Ideas That Made It the Most Important Book You've Never Read*
- *Ibn Khaldun's Greatest Hits — In His Own Words*
- *650 Years Old. Never More Relevant.*

**Format:** ~15,000–20,000 words / ~60–80 pages / ~90 min read

**Price:** $4.99–$6.99 ebook (short read = lower price point, lower barrier to buy)

**What it is NOT:**
- Not a complete translation
- Not a retelling with modern examples added (that's The Collapse Code)
- Not a summary that strips out his reasoning

**What it IS:**
- The 20–25 passages where Ibn Khaldun is at his most clear, most vivid, most alive
- Each passage rendered in fluent modern English that preserves his voice
- A one-sentence editorial header before each passage saying what it is — then he speaks
- Drawn almost entirely from Books Two and Three, where the famous ideas live

---

## 5. Structure

Books Two and Three are the heart of the Muqaddimah. Everything Zuckerberg was reading, everything Dalio's framework echoes, everything that gets cited — it's there.

### Source Focus

| Book | Topic | Include? |
|---|---|---|
| Author's Introduction | Why he wrote it, his method | 1–2 passages only |
| Book One | Human civilization — methodological | 1 passage (the opening argument) |
| **Book Two** | **Bedouin civilization, Asabiyyah** | **~50% of the edition** |
| **Book Three** | **Dynasties, luxury, collapse** | **~45% of the edition** |
| Book Four | Countries and cities | Skip |
| Book Five | Making a living, crafts | Skip |
| Book Six | Sciences and education (339,864 words) | Skip |

### Proposed Passage List

| # | Passage | Source | Core Idea |
|---|---|---|---|
| 0 | Editor's note (original) | — | What this book is, how to read it |
| 1 | Why I wrote this book | Author's Introduction | His method — laws, not divine will |
| 2 | What is Asabiyyah? | Book Two | The definition — group feeling as force of nature |
| 3 | Why desert people are braver | Book Two | Hardship vs. comfort |
| 4 | How Asabiyyah creates leadership | Book Two | Power flows from group cohesion |
| 5 | The desert man conquers the city | Book Two | The fundamental collision |
| 6 | Why religion supercharges Asabiyyah | Book Two | The early Islamic conquests explained |
| 7 | How dynasties are born | Book Three | The first generation — founding energy |
| 8 | The ruler who hoards all the glory | Book Three | Centralization and the crack in cohesion |
| 9 | Why city life destroys fighting spirit | Book Three | The luxury trap begins |
| 10 | The three generations | Book Three | The complete arc — founder, son, grandson |
| 11 | How taxation kills the dynasty | Book Three | The debt spiral |
| 12 | The hired soldiers problem | Book Three | Mercenaries replace loyal troops |
| 13 | The senility of dynasties | Book Three | The end state — waiting for the next hungry group |
| 14 | The cycle begins again | Book Three | Closing — the new desert men at the gates |

**Target: ~1,000–1,500 words per passage = ~15,000–20,000 words total**

---

## 6. Voice and Editorial Rules

**Ibn Khaldun's voice:** Systematic. Confident. Concrete. He states conclusions directly, builds arguments step by step, and always grounds abstractions in historical examples (usually Arabic or Berber). Keep all of this.

**What the editor does:**
- One sentence before each passage: *"Here Ibn Khaldun defines Asabiyyah for the first time."* Then stop.
- Modernize the language — but not the examples. His examples are his evidence. Don't swap them for Apple or Samsung.
- Where he uses an untranslatable Arabic term (Asabiyyah, 'umran, mulk), introduce it once in plain English then use it consistently.

**What the editor does NOT do:**
- Add modern parallels or applications
- Editorialize about whether he is right or wrong
- Hedge his claims
- Add footnotes by editor, only footnotes by IK.

---

## 7. Commercial Strategy

**Pricing:** $4.99–$6.99 ebook — short read, impulse buy price point

**KDP Royalty at $4.99 (35% tier):** ~$1.75/sale
**KDP Royalty at $5.99 (70% tier):** ~$4.19/sale — target this

**Amazon positioning:**
- Ibn Khaldun
- Muqaddimah English translation
- History of civilizations
- Political philosophy classics
- Islamic golden age
- Rise and fall of empires

**The bundle:** Pair with *The Collapse Code* (if/when published) at $14.99 — source text + modern application.

---

## 8. Stage Plan

| Stage | Task | Status |
|---|---|---|
| 1 | Identify exact passages from `extracted_*.txt` files for each of the 14 slots | Not started |
| 2 | Render each passage in plain English (~1,000–1,500w each) | Not started |
| 3 | Write editor's note and 14 one-line headers | Not started |
| 4 | Full read-through — voice consistency check | Not started |
| 5 | EPUB build with `make_epub_native.py` | Not started |
| 6 | Cover design | Not started |
| 7 | KDP upload | Not started |

---

## 9. Source Material Available

- `The_Muqaddimah_Original.txt` — full source text (OCR'd from Arabic)
- `extracted_asabiyyah.txt` — Asabiyyah passages (feeds passages 2–6)
- `extracted_generations.txt` — 3-generation passages (feeds passage 10)
- `extracted_luxury.txt` — luxury trap passages (feeds passages 9, 12)
- `extracted_elite.txt` — elite overproduction passages (feeds passage 11)

Stage 1 is mostly pre-done: the extraction scripts have already pulled the relevant passages. Stage 2 is the writing work.
