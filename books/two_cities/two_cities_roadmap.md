# 🗺️ Parallel Multi-Book eBook Production Roadmap & Tracker

This roadmap guides the parallel processing of our selected classic books for modernization and automated eBook compilation.

---

## ⚙️ The eBook Production Pipeline

For this book, we execute the following standardized steps:

```mermaid
flowchart LR
    Ingest[1. Ingest Raw Text] --> Segment[2. Segment Chapters]
    Segment --> Modernize[3. Casual Modernize]
    Modernize --> OpenClose[4. Open & Close Pages]
    OpenClose --> Colorize[5. Illustrations & Colorize]
    Colorize --> Compile[6. Compile EPUB/HTML]
    Compile --> Review[7. Review & Optimize]
    Review --> Publish[8. Publish]
```

### Stage 1: Ingestion (Source Text)
- **Action**: Locate clean, public domain English source texts (e.g., from Project Gutenberg or Standard Ebooks).
- **Output**: Save raw text file to `books/two_cities/raw_source.txt`.

### Stage 2: Chapter Segmentation
- segmentation before modernization, so review can start by chapter. 
- **Action**: Split full text into separate chapters (`ch_01_en.txt`, etc.) stored under `books/two_cities/chapters/`.

### Stage 3: Modernization chapter by chapter
- tried automated script , just remove right away, wasted token. 
- will just use chat, and if used up will take break. 
- **Action**: Simplify the original challenging English narrative (Victorian, ancient, or formal prose) to a clear, engaging, middle-school level modern English style (ideal for ESL/EFL learners and casual readers).  will keep _i_ _me_ ( italic ) for now.
- **Output**: Save modernized chapters to `books/two_cities/chapters/ch_01_en.txt` (or `book2_ch_XX_en.txt`, etc.).
- **Status**: `[x]` Complete. All 3 Books (45 Chapters) fully modernized.
- **Review**: `[x]` The surgical fixes (Subject-first, no dashes) have been verified and applied to all flagged sentences via `surgical_fix_list.md`.

### Stage 4: Add Opening and Closing Pages
- **Action**: Create clean, engaging introduction and closing pages to frame the modernized work.
- **Opening Page (`introduction_en.txt`)**:
  - **Title**: `A Note to the Reader` (Header `<h1>`).
  - **Contents**: Includes historical context, plot themes of revolutionary France/London, and notes regarding casual modernization rules.
  - **Constraint**: Main title is not repeated in the text body to avoid double-reading in audiobooks.
- **Closing Page (`copyright_en.txt`)**:
  - **TOC Title**: `Copyright & About This Edition`.
  - **Structure**:
    1. **Thank You for Reading**: Placed at the top.
    2. **Feedback & Review Request**: Call-to-action asking for reviews/ratings.
    3. **About This Modernized Edition**: Editorial criteria details (e.g. modernization guidelines, drop caps, and watercolor illustrations).
    4. **Word Count Comparison**:
       * **Original Text**: ~138,900 words
       * **Modernized Text**: ~107,000 words
    5. **Copyright Notice**: Licensing details under `TKPROF LLC`.
  - **Constraint**: Section titles formatted using semantic `<h2>` headings.
- **Status**: `[x]` Complete. `copyright_en.txt` and `introduction_en.txt` have been successfully synchronized to match this layout.

### Stage 5: Illustrations & Colorization
- **Action**: Extract original illustrations from Gutenberg source, colorize them, and insert them into the EPUB.
- **Status**: `[x]` Complete. All 16 original illustrations have been successfully downloaded, beautifully colorized in a watercolor style, and successfully injected into the EPUB chapter texts.

### Stage 6: E-book Compilation
- **Action**: Run compile script to compile the segmented chapters into standard formats:
  - **EPUB**: The primary digital reading format for Google Play Books, Amazon KDP, and general e-readers.
  - **HTML**: A web-friendly version for landing pages or direct previews.
- **Status**: `[x]` Complete. EPUB and HTML successfully built for the modernized text.

### Stage 7: Review, Validation, & Optimization (Publisher Readiness Audit)
- **Action**: Audit the compiled EPUB for validation, metadata, size limits, and TTS optimization.
- **Tasks**:
  - `[ ]` Validate metadata fields (`dc:date` ISO-8601 formatting, dynamic build timestamp for `dcterms:modified`, generate proper UUID).
  - `[ ]` Ensure descriptive `dc:description` is in the package document.
  - `[ ]` Convert any visual page pseudo-headers to semantic `<h2>` headers in introduction and closing files.
  - `[ ]` Optimize image payloads: Back up original colorized illustrations and compress them to JPEG format (max-dimension 800px, 80% quality) to keep the total book payload **under 5 MB**.
  - `[ ]` Prevent TTS stuttering: Shorten `<title>` tags inside `<head>` of the chapter pages to only the chapter name (e.g. `<title>Chapter 1</title>`) to stop screen-readers and read-aloud systems from repeating subtitles twice.
- **Status**: `[ ]` Pending audit review.

### Stage 8: Publish
- **Action**: Upload finalized EPUB to distribution platforms.
  - **Google Play Books**: Primary target
  - **Amazon KDP**: Secondary target
- **Status**: `[ ]` Pending Stage 7 completion.
