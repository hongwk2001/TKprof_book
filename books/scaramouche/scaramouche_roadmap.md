# 🗺️ Scaramouche (스카라무슈) eBook Production & Translation Roadmap

This roadmap tracks the processing of *Scaramouche* by Rafael Sabatini (1921) for Korean translation and automated eBook compilation, following the standardized multi-book production pipeline adapted for the classic adventure and historical romance web novel market.

---

## ⚙️ The 6-Stage eBook Production Pipeline

```mermaid
flowchart LR
    Ingest[1. Ingestion] --> Segment[2. Segmentation]
    Segment --> Translate[3. Translation]
    Translate --> OpenClose[4. Intro/Copyright]
    OpenClose --> Compile[5. Compilation]
    Compile --> Audit[6. Audit & Review]
```

---

### Stage 1: Ingestion (Source Text)
- **Action**: Locate clean, public domain English source texts (Project Gutenberg, etc.) and cover assets.
- **Output**: Save raw text file to `books/scaramouche/raw_source.txt`.
- **Status**: `[x]` Complete (raw source text downloaded from Project Gutenberg eBook #1947).

---

### Stage 2: Chapter Segmentation
- **Action**: Split the full raw text into separate chapters stored under `books/scaramouche/chapters/`.
  - Book I: The Robe (Chapters 1–9)
  - Book II: The Buskin (Chapters 1–11)
  - Book III: The Sword (Chapters 1–16)
- **Status**: `[x]` Complete (36 chapters segmented under `books/scaramouche/chapters/`).

---

### Stage 3: Translation & Modernization (English & Korean)
- **Action**: Modernize the original English prose into engaging, fluent modern English optimized for TTS/general reading, and translate into Korean web-novel style.
- **Modernization Status**: `[/]` In Progress (Chapters 1–3 modernized successfully under `books/scaramouche/chapters/ch_NN_en.txt`).
- **Korean Translation Status**: `[/]` In Progress (Chapters 1–3 translated successfully under `books/scaramouche/chapters/ch_NN_ko.txt`).
- **Translation & Adaptation Guidelines**:
  - **Character Tone**: Emphasize André-Louis's sharp wit, cynicism, and rhetorical mastery. Ensure his transition from an indifferent observer to a passionate revolutionary leader feels compelling.
  - **Theatrical Backdrop**: Maintain authentic Commedia dell'arte vocabulary (Scaramouche, Pantaloon, Harlequin, Columbine, Climene, etc.).
  - **Swordplay & Action**: Translate dueling scenes with dynamic, active verbs to enhance pacing and readability.
  - **Historical Terminology**: Keep French Revolution terms clear (Tiers État, States-General, Marquis, Jacobins, etc.) while explaining key concepts naturally in context.
- **Status**: `[ ]` Pending.

---

### Stage 4: Add Opening and Closing Pages
- **Action**: Create clean, engaging introduction and closing pages to frame the translated work.
- **Opening Page (`introduction_ko.txt` / `introduction_en.txt`)**:
  - **TOC Title**: `작가 및 작품 소개` (About the Author & Book)
  - **Contents**: Context on Rafael Sabatini's legacy, the historical setting of the French Revolution, the significance of the opening line (*"He was born with a gift of laughter and a sense that the world was mad"*), and themes of identity and theatricality.
- **Closing Page (`copyright_ko.txt` / `copyright_en.txt`)**:
  - **TOC Title**: `저작권 및 편집자 노트` (Copyright & Editorial Notes)
  - **Structure**: (1) Thank You section, (2) Platform review request, (3) Editorial notes about the translation and modernization approach, (4) Public domain copyright status.
- **Status**: `[ ]` Pending.

---

### Stage 5: E-book Compilation
- **Action**: Compile the segmented chapters and metadata into standard e-reader formats (EPUB/HTML).
- **Scripts**:
  - Use/adapt `make_epub_native.py` to package clean, spec-compliant EPUB3 books directly.
- **Status**: `[ ]` Pending.

---

### Stage 6: Review, Validation, & Marketing Optimization
Before publishing, the book must be audited for device compatibility and SEO:
- **Digital Marketing & SEO**:
  - Optimize metadata for keywords like "Historical Adventure" (역사 모험 소액), "French Revolution" (프랑스 혁명), "Swashbuckler" (활극), and "Scaramouche" (스카라무슈).
- **EPUB & Metadata Validation**:
  - Validate package via EPUBCheck.
  - Ensure UUIDs, dates, and formatting are valid.
- **Image Optimization**:
  - Compress cover art (`cover.png`) to JPG/PNG, keeping size under 5 MB.
- **Audiobook & TTS Compatibility**:
  - Ensure clean HTML layout and short headers to prevent redundant reading by TTS engines.
- **Status**: `[ ]` Pending.
