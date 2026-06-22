# 🗺️ The Scarlet Letter eBook Production Roadmap & Tracker

This roadmap guides the processing of *The Scarlet Letter* by Nathaniel Hawthorne for modernization and automated eBook compilation.

---

## ⚙️ The eBook Production Pipeline

```mermaid
flowchart LR
    Ingest[1. Ingest Raw Text] --> Segment[2. Segment Chapters]
    Segment --> Modernize[3. Casual Modernize]
    Modernize --> OpenClose[4. Open & Close Pages]
    OpenClose --> Colorize[5. Colorize Illustrations]
    Colorize --> Compile[6. Compile EPUB]
    Compile --> Review[7. Review & Fix]
    Review --> Publish[8. Publish]
```

---

### Stage 1: Ingestion (Source Text)
- **Action**: Locate clean, public domain English source texts and illustrations.
- **Output**: Save raw text file to `books/scarlet_letter/raw_source.txt` and raw HTML to `books/scarlet_letter/raw_source.html`.
- **Status**: `[x]` Complete (raw source text, HTML, and all illustrations/plates downloaded).

---

### Stage 2: Chapter Segmentation
- **Action**: Split the full text into separate chapters (Introductory "The Custom-House" and Chapters 1 to 24) stored under `books/scarlet_letter/chapters/`.
- **Status**: `[x]` Complete (`raw_ch_00.txt` to `raw_ch_24.txt` created).

---

### Stage 3: Modernization
- **Action**: Simplify 19th-century Puritan prose to clear, engaging modern English (middle-school level, ESL-friendly, audiobook-optimized).
- **Status**: `[x]` Complete. All 25 chapters modernized and quality-checked (`ch_00_en.txt` to `ch_24_en.txt`). No em-dashes, no double hyphens, no inverted word order.

### Stage 3b: Custom-House Deep Cleanup
- **Action**: Repair corrupted/archaic paragraphs in `ch_00_en.txt` from earlier subagent run.
  * Line 139: Removed fused double-paragraph (raw + modernized text merged with artifacts).
  * Line 141: Modernized archaic newspaper/Headless Horseman language.
  * Line 143: Replaced Victorian academic prose ("lucubrations", "requisite", "quitted").
- **Status**: `[x]` Complete (`ch_00_en.txt` fully clean, 150 lines, audiobook-ready).

---

### Stage 4: Add Opening and Closing Pages
- **Action**: Write introduction for readers and finalize copyright/feedback closing.
  * `introduction_en.txt`: Plot summary, historical context, note on Custom-House placement at back.
  * `copyright_en.txt`: Reordered — Thank You first, then editorial notes, then legal copyright.
- **Status**: `[x]` Complete.

---

### Stage 5: Illustration Colorization
- **Action**: Run original 1878 B&W engravings through AI image colorizer (watercolor/period-accurate style).
- **Total assets**: 18 large scene illustrations + 12 initial drop caps + 9 ornamental dividers = 39 assets.
- **Progress**:
  * `[x]` All 18 large scene illustrations (illu_001 through illu_320) completed.
  * `[x]` All 12 initial drop caps (initial_a through initial_w) completed.
  * `[x]` ornament_i completed.
  * `[x]` Remaining 8 ornamental dividers (ornament_ii through ornament_ix) completed.
- **Status**: `[x]` Complete (39 of 39 assets colorized and embedded).

---

### Stage 6: EPUB Compilation
- **Action**: Assemble all chapters, images, and CSS into a valid EPUB file natively.
  * Script: `make_epub_native.py` (Replaced buggy `ebooklib` with a strict EPUB3 native zip builder)
  * Layout: Introduction → Chapters 1–24 → Custom-House → Copyright
  * Accessibility: Fully optimized for Text-to-Speech (TTS) audiobook engines. Chapters spell out numbers in the code (e.g. `<h1>Chapter Three</h1>`) while visually rendering as separate centered lines to maintain historic 19th-century typesetting.
  * Styling: Georgia serif, warm cream background (#fdfaf5), 1.7 line spacing
  * Illustrations: colorized versions embedded; B&W fallback where colorization pending
- **Metadata & Tags added**:
  * Title: "The Scarlet Letter: Modern English Edition"
  * Author: Nathaniel Hawthorne | Publisher: TKPROF LLC | Date: 2026
  * Rights: Modernized edition Copyright 2026 TKPROF LLC. Original text public domain.
  * Description: Full audiobook/ESL-focused pitch description
  * Subject tags: Fiction, Classic Literature, Historical Fiction, American Literature, 19th Century, ESL EFL Learning, Audiobook Friendly, Puritan New England, Nathaniel Hawthorne
- **Output**: `scarlet_letter.epub`
- **Status**: `[x]` Complete. EPUB built successfully using native ZIP packaging and TTS-optimized headers.

---

### Stage 7: Review & Fix
- **Action**: Open the EPUB in a reader and verify layout, chapter flow, illustration placement, and styling.
- **Sub-tasks**:
  * `[x]` Calibre link error fixed (abandoned ebooklib, built EPUB native zip structure).
  * `[x]` Google Play Books "processing" error fixed (escaped XML ampersand `&amp;` in copyright title).
  * `[x]` Duplicate chapter titles fixed (script parses out raw text file uppercase headers).
  * `[x]` Audiobook TTS compatibility fixed (numbers spelled out, separated visually onto two lines).
  * `[x]` Final EPUB compile with the last 8 ornament images colorized.
- **Status**: `[x]` Complete. Structural code is perfect and all image assets are included.

---

### Stage 8: Publish
- **Action**: Upload finalized EPUB to distribution platforms.
  * **Google Play Books**: Primary target
  * **Amazon KDP**: Secondary target
  * **Metadata**: Title = "The Scarlet Letter: Modern English Edition" / Author = Nathaniel Hawthorne / Publisher = TKPROF LLC
- **Status**: `[ ]` Pending Stage 7 sign-off.
