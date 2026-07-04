# Think and Grow Rich - Project Roadmap

**Author:** Napoleon Hill (1937 Edition)
**Status:** Planning

## Stage 1: Source Material Acquisition
- [x] Locate and download the raw public domain text (originally published in 1937).
- [ ] Clean up the raw text (extract from EPUB, remove extra formatting, etc.).
- [ ] Save as `think_and_grow_rich_raw.txt`.

## Stage 2: Chapter Segmentation
- [ ] Split the full text into separate raw chapters stored under `chapters/` directory.

## Stage 3: Language Modernization
- [ ] Modernize the language to make it more accessible, prioritizing readability over historical authenticity:
  - **Create a custom `prompt.txt`** for the book outlining specific modernization rules (e.g., target audience, sentence breakdown for TTS, vocabulary preservation).
  - Process each segmented chapter using a `modernize_book.py` script.
  - Review modernized outputs for flow, tone, and ESL suitability.

## Stage 4: Intro and Copyright
- [ ] Draft the introduction and copyright texts (`introduction_en.txt`, `copyright_en.txt`).
  - Frame the context of the 1937 publication and its impact on the personal development genre.

## Stage 5: Audio Production (TTS Generation)
- [ ] Set up `edge_tts` voices.
- [ ] Generate TTS clips and mix final audio per chapter (`final_audio/final_ch_*.mp3`).
  - *Note: `final_ch_00.mp3` (Frontmatter) is excluded from the final audiobook.*
- [ ] Verify audio quality and pacing.

### 🎵 Audio Structure (per chapter)
Each chapter audio is assembled in this order:
1. **Cinematic Intro / Bumper** — Short bumper using intro theme music.
2. **Narration** — Multi-voice TTS.

## Stage 6: E-book Compilation (EPUB)
- [ ] Compile the segmented chapters and assets into standard e-reader formats (EPUB/HTML).
  - *Note: `ch_00` (Frontmatter/TOC) is excluded from the final text compilations.*
- [ ] Use a `make_epub_native.py` script to compile clean, spec-compliant EPUB3 books without dependencies.

## Stage 7: Metadata & Publishing Prep
- [ ] Calculate the total runtime of all audio files to determine Audible/ACX pricing tiers.
- [ ] Draft a catchy, sales-optimized Title, Subtitle, and Description.
- [ ] Draft an "About the Author" section for Napoleon Hill.
- [ ] Determine the best target genres.
- [ ] Digital Marketing & SEO: Ensure listing metadata leverages appropriate keywords.
- [ ] XHTML & Metadata Validation.

## Stage 8: Final Packaging & Audit
- [ ] Ensure all `.mp3` files are properly named and backed up in an `audio_archive` directory.
- [ ] Audit eBook for publisher-specific issues and device compatibility.
- [ ] Upload to the chosen publishing platforms (ACX, Google Play Books, etc.).
