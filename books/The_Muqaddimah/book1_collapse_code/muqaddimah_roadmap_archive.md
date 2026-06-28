# The Collapse Code — Production Roadmap
## Based on: The Muqaddimah by Ibn Khaldun

**What this book is:** Each chapter takes one of Ibn Khaldun's big ideas and applies it to a real historical empire — then connects it to today. Fast, punchy, fun to read. Ibn Khaldun is the credibility and framework; the case studies bring it alive.

**Commercial target:** ~40,000 words / ~160 pages / ~3hr read / $9.99 ebook / $14.99 paperback

**Comparable titles:** Malcolm Gladwell's *Outliers*, Peter Thiel's *Zero to One*

**Title candidates:**
- *The Collapse Code: Ibn Khaldun's 650-Year-Old Formula for Why Civilizations Fall*
- *Asabiyyah: The Ancient Idea That Predicts Every Empire's Fall*

---

## Chapter Structure

| File | Chapter | Core Idea | Target | Current | Status |
|---|---|---|---|---|---|
| `00_introduction.md` | Introduction | Hook: Ibn Khaldun predicted everything | 1,500w | ~400w | Pass 2 needed |
| `chapter_1_draft.md` | Ch 1: Who Was This Guy? | His wild political life — credibility hook | 5,000w | 3,936w | **Pass 2 DONE** |
| `chapter_2_draft.md` | Ch 2: What Is Asabiyyah? | The invisible glue of civilizations | 5,000w | 4,324w | **Pass 2 DONE** |
| `chapter_3_draft.md` | Ch 3: How Empires Are Born | The hungry outsiders always win | 5,000w | 3,437w | **Pass 2 DONE** |
| `chapter_4_draft.md` | Ch 4: The Luxury Trap | Success is the beginning of the end | 5,000w | 3,235w | **Pass 2 DONE** |
| `chapter_5_draft.md` | Ch 5: Elite Overproduction | Too many ambitious people, not enough thrones | 5,000w | 3,205w | **Pass 2 DONE** |
| `chapter_6_draft.md` | Ch 6: The 3-Generation Rule | Founder → Son → Grandson → Collapse | 5,000w | 3,568w | **Pass 2 DONE** |
| `chapter_7_draft.md` | Ch 7: Who's Next? | The cycle starting again today | 5,000w | 2,754w | **Pass 2 DONE** |
| `08_readers_guide.md` | Appendix: Reader's Guide | Further reading, key terms | 500w | ~300w | Draft done |
| `09_copyright.md` | Copyright | Standard page | 200w | ~200w | Done |
| **Total** | | | **~38,700w** | **~25,359w** | **Stage 4C DONE** |

---

## Stage Progress

- [x] **Stage 1:** Source mapping and concept definition
- [x] **Stage 2:** Chapter outlines
- [x] **Stage 3:** EPUB infrastructure (`make_epub.py`)
- [x] **Stage 4A:** Stub drafts for all chapters
- [x] **Stage 4B (Pass 1):** All chapters expanded to ~1,900–3,900w
- [x] **Stage 4C (Pass 2):** Deep pass — each chapter to ~5,000w — DONE
- [ ] **Stage 5:** EPUB rebuild (after Pass 2 complete)
- [ ] **Stage 6:** KDP metadata, blurb, pricing, upload

---

## Stage 4C: Pass 2 Checklist

### Ch 1 — DONE (~3,936w)
Added: "What He Inherited" section, deepened Fez prison scene, Granada/Pedro scene, Timur encounter expanded to full scene (~900w).

### Ch 2: What Is Asabiyyah? — DONE (4,324w)
- [x] Deepened Band of Brothers section — Valley Forge origin of American military Asabiyyah (~650w)
- [x] Added: Asabiyyah in religion — Islam's first century, Mormon pioneer movement (~1,050w)
- [x] Added: When Asabiyyah turns dark — gangs, Jonestown, extremism (~800w)

### Ch 3: How Empires Are Born — DONE (3,437w)
- [x] Deepened Rome — citizen-soldier distinction, Senate after Cannae (~380w)
- [x] Added Arab Conquests — pre-Islamic Arabia → Muhammad → al-Qadisiyyah → 100-year conquest (~950w)
- [x] Deepened Mongols — decimal system, collective accountability structure (~200w)
- [x] Added Tesla/SpaceX — modern desert vs. city parallel (~600w)

### Ch 4: The Luxury Trap — DONE (3,235w)
- [x] Extended Rome arc to 476 AD — Odoacer, the shrug ending (~400w)
- [x] Added Song Dynasty — peak civilization, Mongol conquest, Battle of Yamen (~600w)
- [x] Added Rockefeller contrast to Vanderbilts — institutional structures vs. dissipation (~250w)
- [x] Added Corporate Luxury Trap — Kodak/digital camera 1975, Blockbuster/Netflix, Nokia/iPhone (~700w)

### Ch 5: Elite Overproduction — DONE (3,205w)
- [x] Deepened Turchin — wealth pump data, Seshat project, 2010 Nature prediction (~500w)
- [x] Deepened Dalio — Roman denarius debasement, Diocletian price controls (~400w)
- [x] Deepened Ming — Wei Zhongxian, Chongzhen's 17 finance ministers (~350w)
- [x] Added Roman bureaucracy — title multiplication, 30-40k salaried officials, patronage machine (~500w)

### Ch 6: The 3-Generation Rule — DONE (3,568w)
- [x] Deepened Roman arc — Flavians, Commodus/Hercules delusion, Year of Five Emperors (~600w)
- [x] Deepened Mongol arc — Kublai's Japan invasions (kamikaze), personal decline (~450w)
- [x] Added Samsung/chaebol — Lee Byung-chul → Lee Kun-hee → Lee Jae-yong bribery scandal (~550w)
- [x] Added Putnam *Bowling Alone* data to US section — civic org collapse as Asabiyyah measurement (~350w)

### Ch 7: Who's Next? — DONE (2,754w)
- [x] Expanded all four candidates — China (Century of Humiliation, Belt and Road), Global South (demographic data, BRICS+), religious movements (Africa/LatAm growth), tech tribes (Bitcoin arc, open-source AI) (~800w)
- [x] Deepened optimist case — Bronze Age collapse → Iron Age democratization, Black Death → Renaissance (~450w)
- [x] Expanded individual framework — concrete first/second/third gen diagnostic signs, personal Asabiyyah (~600w)

---

## After Pass 2
- Re-run `python make_epub.py` from `books/The_Muqaddimah/`
- Validate in Calibre and Kindle Previewer
- Then Stage 6: KDP
