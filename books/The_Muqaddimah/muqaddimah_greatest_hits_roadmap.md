# The Muqaddimah: Greatest Hits Edition — Production Roadmap

**What this book is:** 14 key passages from Books Two and Three, rendered in plain modern English. Ibn Khaldun speaks; the editor stays out of the way.

**Target:** ~15,000–20,000 words / ~60–80 pages / ~90 min read / $5.99 ebook

---

## Passage Structure

| # | Passage Title | Source Book | Target Words | Status |
|---|---|---|---|---|
| 0 | Editor's Note | Original | ~500w | **DONE** |
| 1 | Why I Wrote This Book | Author's Introduction | ~1,000w | **DONE** |
| 2 | What Is Asabiyyah? | Book Two | ~1,500w | **DONE** |
| 3 | Why Desert People Are Braver | Book Two | ~1,200w | **DONE** |
| 4 | How Asabiyyah Creates Leadership | Book Two | ~1,200w | **DONE** |
| 5 | The Desert Man Conquers the City | Book Two | ~1,500w | **DONE** |
| 6 | Why Religion Supercharges Asabiyyah | Book Two | ~1,200w | **DONE** |
| 7 | How Dynasties Are Born | Book Three | ~1,500w | **DONE** |
| 8 | The Ruler Who Hoards All the Glory | Book Three | ~1,200w | **DONE** |
| 9 | Why City Life Destroys Fighting Spirit | Book Three | ~1,200w | **DONE** |
| 10 | The Three Generations | Book Three | ~1,500w | **DONE** |
| 11 | How Taxation Kills the Dynasty | Book Three | ~1,200w | **DONE** |
| 12 | The Hired Soldiers Problem | Book Three | ~1,000w | **DONE** |
| 13 | The Senility of Dynasties | Book Three | ~1,200w | **DONE** |
| 14 | The Cycle Begins Again | Book Three | ~1,000w | **DONE** |
| **Total** | | | **~17,000w** | |

---

## Stage Progress

- [x] **Stage 1:** Match each passage slot to source text in `extracted_*.txt` files
- [x] **Stage 2:** Render all 14 passages in plain English
- [x] **Stage 3:** Write Editor's Note + 14 one-line headers
- [x] **Stage 4:** Full read-through — voice consistency, accuracy check
- [ ] **Stage 5:** EPUB build (`make_epub_native.py`)
- [ ] **Stage 6:** Cover design
- [ ] **Stage 7:** KDP upload — ebook + paperback

---

## Stage 1: Source Mapping

Match each passage to the extraction files already built. Most slots are pre-fed.

| Passage | Source File | Notes |
|---|---|---|
| 0 — Editor's Note | Original writing | ~500w, written fresh |
| 1 — Why I Wrote This Book | `The_Muqaddimah_Original.txt` | Author's intro section |
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
6. One-line header before the passage (italicized): *e.g., "Here Ibn Khaldun gives the first and clearest definition of Asabiyyah."*

---

## Stage 2: Passage Checklist

### Passage 0 — Editor's Note
- [x] Draft (~500w) → `00_editors_note.md`
- [ ] Review

### Passage 1 — Why I Wrote This Book
- [x] Locate source in Original.txt
- [x] Render → `01_why_i_wrote_this.md`
- [ ] Review

### Passage 2 — What Is Asabiyyah?
- [x] Locate in extracted_asabiyyah.txt
- [x] Render → `02_what_is_asabiyyah.md`
- [ ] Review

### Passage 3 — Why Desert People Are Braver
- [x] Locate in extracted_asabiyyah.txt
- [x] Render → `03_desert_people_braver.md`
- [ ] Review

### Passage 4 — How Asabiyyah Creates Leadership
- [x] Locate in extracted_asabiyyah.txt
- [x] Render → `04_asabiyyah_creates_leadership.md`
- [ ] Review

### Passage 5 — The Desert Man Conquers the City
- [x] Locate in extracted_asabiyyah.txt
- [x] Render → `05_desert_conquers_city.md`
- [ ] Review

### Passage 6 — Why Religion Supercharges Asabiyyah
- [x] Locate in extracted_asabiyyah.txt
- [x] Render → `06_religion_supercharges.md`
- [ ] Review

### Passage 7 — How Dynasties Are Born
- [x] Locate in extracted_generations.txt
- [x] Render → `07_dynasties_born.md`
- [ ] Review

### Passage 8 — The Ruler Who Hoards All the Glory
- [x] Locate in extracted_elite.txt
- [x] Render → `08_ruler_hoards_glory.md`
- [ ] Review

### Passage 9 — Why City Life Destroys Fighting Spirit
- [x] Locate in extracted_luxury.txt
- [x] Render → `09_city_life_destroys.md`
- [ ] Review

### Passage 10 — The Three Generations
- [x] Locate in extracted_generations.txt
- [x] Render → `10_three_generations.md`
- [ ] Review

### Passage 11 — How Taxation Kills the Dynasty
- [x] Locate in extracted_elite.txt
- [x] Render → `11_taxation_kills.md`
- [ ] Review

### Passage 12 — The Hired Soldiers Problem
- [x] Locate in extracted_asabiyyah.txt
- [x] Render → `12_hired_soldiers.md`
- [ ] Review

### Passage 13 — The Senility of Dynasties
- [x] Locate in extracted_generations.txt
- [x] Render → `13_senility_of_dynasties.md`
- [ ] Review

### Passage 14 — The Cycle Begins Again
- [x] Locate in extracted_asabiyyah.txt
- [x] Render → `14_cycle_begins_again.md`
- [ ] Review

---

## File Structure (when drafting begins)

```
books/The_Muqaddimah/
├── greatest_hits/
│   ├── 00_editors_note.md
│   ├── 01_why_i_wrote_this.md
│   ├── 02_what_is_asabiyyah.md
│   ├── 03_desert_people_braver.md
│   ├── 04_asabiyyah_creates_leadership.md
│   ├── 05_desert_conquers_city.md
│   ├── 06_religion_supercharges.md
│   ├── 07_dynasties_born.md
│   ├── 08_ruler_hoards_glory.md
│   ├── 09_city_life_destroys.md
│   ├── 10_three_generations.md
│   ├── 11_taxation_kills.md
│   ├── 12_hired_soldiers.md
│   ├── 13_senility_dynasties.md
│   └── 14_cycle_begins_again.md
```
