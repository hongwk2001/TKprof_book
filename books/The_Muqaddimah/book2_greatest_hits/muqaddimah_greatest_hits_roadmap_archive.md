# 🗺️ The Muqaddimah: Greatest Hits Edition — Production Roadmap

**What this book is:** 14 key passages from the Author's Introduction, Book Two, and Book Three of *The Muqaddimah*, rendered in plain modern English. Ibn Khaldun speaks; the editor stays out of the way.

**Target:** ~15,000–20,000 words / ~60–80 pages / ~90 min read / $5.99 ebook
**Current:** 11,755 words / ~47 pages / ~59 min read — **3,245w short of minimum target**

---

## ⚙️ The 7-Stage eBook Production Pipeline

```mermaid
flowchart LR
    Map[1. Source Mapping] --> Render[2. Render Passages]
    Render --> Frame[3. Opening & Closing]
    Frame --> Review[4. Voice Review]
    Review --> Compile[5. EPUB Build]
    Compile --> Cover[6. Cover Design]
    Cover --> Publish[7. KDP Upload]
```

---

### Stage 1: Source Mapping
- **Action:** Match each of the 14 passage slots to source sections in the extracted `.txt` files built from the original Arabic OCR dump.
- **Output:** Passage-to-source table (see below).
- **Status:** `[x]` Complete.

---

### Stage 2: Render All 14 Passages
- **Action:** Render each passage in plain modern English — clear sentences, no academic hedging. Keep Ibn Khaldun's own examples (Arab tribes, Berber dynasties, early caliphs). Introduce Arabic terms once, then use them consistently. Target 1,000–1,500 words per passage.
- **Output:** 14 `.md` files in `book2_greatest_hits/` (passages 1–14).
- **Status:** `[x]` Complete.

#### Passage Word Counts

| # | Passage Title | Source | Target | Current | Gap |
|---|---|---|---|---|---|
| 1 | Why I Wrote This Book | Author's Introduction | ~1,000w | 809w | +191w |
| 2 | What Is Asabiyyah? | Book Two | ~1,500w | 873w | +627w |
| 3 | Why Desert People Are Braver | Book Two | ~1,200w | 734w | +466w |
| 4 | How Asabiyyah Creates Leadership | Book Two | ~1,200w | 669w | +531w |
| 5 | The Desert Man Conquers the City | Book Two | ~1,500w | 811w | +689w |
| 6 | Why Religion Supercharges Asabiyyah | Book Two | ~1,200w | 800w | +400w |
| 7 | How Dynasties Are Born | Book Three | ~1,500w | 846w | +654w |
| 8 | The Ruler Who Hoards All the Glory | Book Three | ~1,200w | 742w | +458w |
| 9 | Why City Life Destroys Fighting Spirit | Book Three | ~1,200w | 772w | +428w |
| 10 | The Three Generations | Book Three | ~1,500w | 880w | +620w |
| 11 | How Taxation Kills the Dynasty | Book Three | ~1,200w | 812w | +388w |
| 12 | The Hired Soldiers Problem | Book Three | ~1,000w | 748w | +252w |
| 13 | The Senility of Dynasties | Book Three | ~1,200w | 888w | +312w |
| 14 | The Cycle Begins Again | Book Three | ~1,000w | 873w | +127w |
| **Total** | | | **~17,000w** | **11,755w** | **5,245w** |

---

### Stage 3: Opening and Closing Pages
- **Action:** Write the Editor's Note (framing the book and Ibn Khaldun), an "About the Source" page (full Muqaddimah structure with word counts), and a Copyright page (with cross-promotion to Book 1: *The Collapse Code*).
- **Output:**
  - `book2_greatest_hits/00_editors_note.md` — ~500w introduction
  - `book2_greatest_hits/15_about_the_source.md` — full source structure table
  - `book2_greatest_hits/16_copyright.md` — copyright + Book 1 cross-promo
- **Status:** `[x]` Complete.

---

### Stage 4: Full Read-Through — Voice & Accuracy Review
- **Action:** Read all passages end-to-end. Check voice consistency across passages, verify accuracy against source intent, ensure one-line italic headers are present for each passage.
- **Output:** All 14 passage headers confirmed; voice consistent throughout.
- **Status:** `[x]` Complete.

---

### Stage 5: EPUB Build
- **Action:** Run `make_epub_greatest_hits.py` to compile all passage files into a spec-compliant EPUB 3.0. Validate structure (mimetype, container.xml, OPF, NCX, nav, CSS, all XHTML chapters).
- **Scripts:**
  - `make_epub_greatest_hits.py` — native Python zip packager, no external dependencies.
- **Output:** `The_Muqaddimah_Greatest_Hits.epub` — 40 KB, 17 chapters (cover + p00–p16), EPUB 3.0.
- **Status:** `[ ]` Pending rebuild after Stage 3 additions.

---

### Stage 6: Cover Design
- **Action:** Design a cover image at KDP spec (2,560 × 1,600px, min 300 DPI). Reflect the tone: austere, historical, Arabic manuscript aesthetic. Embed in EPUB and prepare standalone JPG for KDP upload.
- **Output:** `cover.jpg` added to EPUB; standalone cover file ready for KDP.
- **Status:** `[ ]` Pending.

---

### Stage 7: KDP Upload — eBook
- **Action:** Upload EPUB and cover to KDP. Set metadata, pricing, and categories. Submit for review.
- **Metadata:**
  - Title: *The Muqaddimah: Essential Passages in Plain English*
  - Subtitle: *The Ideas That Made It the Most Important Book You've Never Read*
  - Author: Ibn Khaldun (rendered by TKPROF)
  - Categories: History / Islamic Civilization / Political Philosophy
  - Price: $2.99 ebook (adjusted from $5.99 given current word count)
- **Output:** Live KDP listing.
- **Status:** `[ ]` Pending.

---

## Stage 1: Source Mapping Detail

| Passage | Source File | Notes |
|---|---|---|
| 1 — Why I Wrote This Book | `The_Muqaddimah_Original.txt` | Author's Introduction section |
| 2 — What Is Asabiyyah? | `extracted_asabiyyah.txt` | Opening definition passages |
| 3 — Why Desert People Are Braver | `extracted_asabiyyah.txt` | Bedouin hardship vs. city comfort |
| 4 — How Asabiyyah Creates Leadership | `extracted_asabiyyah.txt` | Leadership and dominance passages |
| 5 — The Desert Man Conquers the City | `extracted_asabiyyah.txt` | Collision passages |
| 6 — Why Religion Supercharges Asabiyyah | `extracted_asabiyyah.txt` | Prophethood and Asabiyyah sections |
| 7 — How Dynasties Are Born | `extracted_generations.txt` | First generation founding passages |
| 8 — The Ruler Who Hoards All the Glory | `extracted_elite.txt` | Centralization passages |
| 9 — Why City Life Destroys Fighting Spirit | `extracted_luxury.txt` | Luxury and sedentary life passages |
| 10 — The Three Generations | `extracted_generations.txt` | Full 3-gen arc passages |
| 11 — How Taxation Kills the Dynasty | `extracted_elite.txt` | Taxation and fiscal collapse passages |
| 12 — The Hired Soldiers Problem | `extracted_asabiyyah.txt` | Mercenary passages |
| 13 — The Senility of Dynasties | `extracted_generations.txt` | End-state passages |
| 14 — The Cycle Begins Again | `extracted_asabiyyah.txt` | New outsiders at the gates |

---

## Stage 2: Rendering Rules

For each passage:
1. Find the source text in the extraction file
2. Render in plain modern English — clear sentences, no academic hedging
3. Keep his examples (Arab tribes, Berber dynasties, early caliphs) — do not swap for modern ones
4. Introduce Arabic terms once in plain English, then use the term consistently
5. Target 1,000–1,500 words per passage
6. One-line italic header before the passage: *e.g., "Here Ibn Khaldun gives the first and clearest definition of Asabiyyah."*
