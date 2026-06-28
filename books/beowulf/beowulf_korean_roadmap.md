# 🗺️ Beowulf Korean Translation eBook Production Roadmap & Tracker

This roadmap guides the production of a Korean translation of *Beowulf* using the existing segmented English chapters as the source, formatted and compiled as an eBook.

---

## ⚙️ The eBook Production Pipeline

```mermaid
flowchart LR
    Source[1. Source Chapters] --> Translate[2. Translate to Korean]
    Translate --> Localize[3. Localization Pass]
    Localize --> OpenClose[4. Open & Close Pages]
    OpenClose --> Compile[5. Compile EPUB]
    Compile --> Review[6. Review & Fix]
    Review --> Publish[7. Publish]
```

---

### Stage 1: Source Chapters (Input)
- **Action**: Use the existing segmented English chapter files as the translation source.
- **Input**: `books/beowulf/chapters/` — 44 files (`ch_00_en.txt` through `ch_43_en.txt`).
- **Status**: `[x]` Complete (chapter files already on disk).

---

### Stage 2: Translate to Korean
- **Action**: Translate each chapter into Korean prose. Target a general adult readership — clear, natural Korean prose, not overly literary or archaic.
- **Output**: Korean chapter files saved under `books/beowulf/chapters_kr/` (e.g., `ch_00_ko.txt`, `ch_01_ko.txt`, etc.).
- **Guidelines**:
  * Translate meaning and tone faithfully, not word-for-word.
  * Use natural Korean sentence structure (SOV).
  * Render proper nouns phonetically (e.g., 베오울프, 흐로스가르, 그렌델).
  * Preserve the epic tone without using archaic Korean (고어) vocabulary.
  * Keep chapters approximately proportional in length to the English originals.
  * Easy understanding and fun is more important than the literal translation.
  * Using the modern Korean style of translation, not the literary translation style.
- **Sub-tasks**:
  * `[x]` Prologue (ch_00)
  * `[x]` Chapters 01–10
  * `[x]` Chapters 11–20
  * `[x]` Chapters 21–30
  * `[x]` Chapters 31–43

---

### Stage 3: Localization Pass
- **Action**: Review all Korean chapters for naturalness, consistency, and audiobook-friendliness.
- **Checklist**:
  * `[ ]` Consistent proper noun spelling throughout (create a 고유명사 glossary).
  * `[ ]` Remove or adapt English idioms that don't translate cleanly.
  * `[ ]` Ensure sentences read smoothly aloud in Korean (TTS and human narration friendly).
  * `[ ]` Check honorific levels — maintain a consistent register appropriate for epic storytelling.
  * `[ ]` Verify punctuation follows Korean typographic conventions.

---

### Stage 4: Add Opening and Closing Pages (Korean)
- **Action**: Write or adapt front and back matter in Korean.
  * `introduction_ko.txt`: Korean introduction — plot summary, historical context, note on the poem's origins and preservation.
  * `copyright_ko.txt`: Korean editorial notes and copyright page.
- **Status**: `[x]` Complete
  * `introduction_ko.txt` — saved to `books/beowulf/`
  * `copyright_ko.txt` — saved to `books/beowulf/`

---

### Stage 5: EPUB Compilation
- **Action**: Assemble all Korean chapter files, introduction, and copyright page into a clean `.epub` file.
  * Use the same native Python EPUB script as the English edition.
  * Verify Korean character encoding (UTF-8) is enforced throughout.
  * Accessibility: Optimized for Korean TTS audiobook engines.
- **Metadata & Tags**:
  * Title: "베오울프: 현대 한국어판" (Beowulf: Modern Korean Edition)
  * Author: 작자 미상 (Anonymous)
  * Language: `ko`
  * Description: Korean-language audiobook/general reader pitch.
  * Subject tags: 서사시, 고전 문학, 앵글로색슨 문학, 신화, 한국어판, 오디오북.
- **Output**: `beowulf_ko.epub`
- **Script**: `make_epub_native_ko.py`
- **Status**: `[x]` Complete (7,259 KB, 46 XHTML files)

---

### Stage 6: Review & Fix
- **Action**: Open the EPUB in a reader and verify layout, chapter flow, and Korean text rendering.
- **Sub-tasks**:
  * `[ ]` Verify Korean fonts render correctly in EPUB readers.
  * `[ ]` Confirm chapter navigation and table of contents display in Korean.
  * `[ ]` Test TTS playback in Korean on at least one device/app.
  * `[ ]` Proofread final compiled output for encoding artifacts or formatting breaks.
- **Status**: `[ ]` Pending

---

### Stage 7: Publish
- **Action**: Upload finalized Korean EPUB to distribution platforms.
- **Status**: `[ ]` Pending
