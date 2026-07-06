# Meditations - Project Roadmap

**Author:** Marcus Aurelius (circa 161–180 AD)
**Status:** Planning

## Stage 1: Source Material Acquisition
- [x] Locate and download the raw public domain text.
- [x] Save as `meditations_chrystal_raw.txt` and `meditations_long_raw.txt`.
- [x] Evaluated options and selected the **George W. Chrystal translation** (due to a leaner ~19k word count and lack of excessive boilerplate).

## Stage 2: Chapter Segmentation
- [x] Split the full text into separate raw chapters (Books I-XII) stored under `chapters/` directory.
- [x] Remove Gutenberg boilerplate, translator notes, and prefaces that aren't part of the core text.

## Stage 3: Language Modernization
- [x] Modernize the language to make it more accessible, prioritizing readability over historical authenticity:
  - [x] **Create a custom `prompt.txt`** for the book outlining specific modernization rules.
  - [x] Process each segmented chapter using a `modernize_book.py` script.
  - [x] Review modernized outputs for flow, tone, and ESL suitability, while retaining the calm, stoic, and philosophical tone of Marcus Aurelius.

## Stage 4: Intro and Copyright / Closing
- [x] Draft the introduction and copyright / closing texts:
  - **Introduction**: `introduction_en.txt` (generates `final_track_00_intro.mp3`).
  - **Copyright / Closing**: `copyright_en.txt` and `closing_en.txt` must contain identical content, providing credits and copyright info (generates `closing.mp3`).
  - [x] Frame the context of the Stoic philosophy and its timeless relevance.

## Stage 5: Audio Production (TTS Generation)
- [x] Set up edge-tts voices (`en-GB-RyanNeural`).
- [x] Generate TTS clips and mix final audio.
  - **Intro Track**: Compiled as `final_track_00_intro.mp3`.
  - **Chapters**: Compiled sequentially (e.g., `final_track_01.mp3` to `final_track_12.mp3`).
  - **Closing Track**: Compiled as a separate `closing.mp3` using `closing_en.txt` (matching `copyright_en.txt`) and mixed with the full cinematic outro music.
  - **Sample Track**: Generated separately as `sample.mp3` (concatenates intro and chapter 1, trimmed to less than 5 minutes duration).
- [x] Verify audio quality and pacing, ensuring all tracks are encoded at 44.1 kHz sample rate and 256 kbps bitrate.

### 🎵 Audio Structure (per chapter)
Each chapter audio is assembled in this order:
1. **Cinematic Intro / Bumper** — Short bumper using intro theme music.
   - Play 4.5 sec at the beginning of the audiobook which is the intro (`introduction_en.txt`).
   - Each chapter's beginning play 2 sec.
   - At the very end of the last chapter play full length of the music.
2. **Narration** — one voice Ryan

## Stage 6: E-book Compilation (EPUB)
- [x] Compile the segmented chapters and assets into standard e-reader formats (EPUB/HTML).
- [x] Use a `make_epub_native.py` script to compile clean, spec-compliant EPUB3 books without dependencies.

## Stage 7: Metadata & Publishing Prep
- [x] Calculate the total runtime of all audio files to determine Audible/ACX pricing tiers.
- [x] Draft a catchy, sales-optimized Title, Subtitle, and Description.
- [x] Draft an "About the Author" section for Marcus Aurelius.
- [x] Determine the best target genres (e.g., Philosophy, Self-Help, History).
- [x] Digital Marketing & SEO: Ensure listing metadata leverages appropriate keywords.
- [x] XHTML & Metadata Validation.

## Stage 8: Final Packaging & Audit
- [ ] Ensure all `.mp3` files are properly named and backed up in an `audio_archive` directory.
- [ ] Audit eBook for publisher-specific issues and device compatibility.
- [ ] Upload to the chosen publishing platforms (ACX, Google Play Books, etc.).
