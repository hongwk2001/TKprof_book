# The Prince - Project Roadmap

**Author:** Niccolò Machiavelli (1532)
**Status:** Planning

## Stage 1: Source Material Acquisition
- [x] Locate and download the raw public domain text.
- [x] Save as `the_prince_raw.txt`.

## Stage 2: Chapter Segmentation
- [x] Split the full text into separate raw chapters stored under `chapters/` directory.
- [x] Remove Gutenberg boilerplate, translator notes, and prefaces that aren't part of the core text.

## Stage 3: Language Modernization
- [x] Modernize the language to make it more accessible, prioritizing readability over historical authenticity:
  - **Create a custom `prompt.txt`** for the book outlining specific modernization rules (e.g., target audience, sentence breakdown for TTS, vocabulary preservation).
  - Process each segmented chapter using a `modernize_book.py` script.
  - Review modernized outputs for flow, tone, and ESL suitability, while retaining Machiavelli's calculated and pragmatic tone.

## Stage 4: Intro and Copyright / Closing
- [x] Draft the introduction and copyright / closing texts:
  - **Introduction**: `introduction_en.txt` (generates `intro.mp3` / `introduction.mp3`).
  - **Copyright / Closing**: `copyright_en.txt` and `closing_en.txt` must contain identical content, providing credits and copyright info (generates `closing.mp3`).
  - Frame the context of the 1532 publication and its impact on modern political philosophy.

## Stage 5: Audio Production (TTS Generation)
- [x] Set up edge-tts voices (`en-GB-RyanNeural`).
- [x] Generate TTS clips and mix final audio.
  - **Intro Track**: Compiled as a separate `intro.mp3` (or `introduction.mp3`).
  - **Chapters**: Compiled sequentially (e.g., `final_track_01.mp3` to `final_track_26.mp3`).
  - **Closing Track**: Compiled as a separate `closing.mp3` using `closing_en.txt` (matching `copyright_en.txt`) and mixed with the full cinematic outro music.
  - **Sample Track**: Generated separately as `sample.mp3` (1-5 minutes duration) from the introduction.
- [x] Verify audio quality and pacing, ensuring all tracks are encoded at 44.1 kHz sample rate and 256 kbps bitrate.

### 🎵 Audio Structure (per chapter)
Each chapter audio is assembled in this order:
1. **Cinematic Intro / Bumper** — Short bumper using intro theme music.
   D:\git_repo\TKprof_book\books\the_prince\lordsonny-cinematic-hit-159487.mp3
  play 4.5 sec at the beginning of the audiobook which is intro: D:\git_repo\TKprof_book\books\the_prince\introduction_en.txt, not chapter 1.
  each chapters beginning play  2 sec
  At the very end of last chapter 26 play full length of the music
2. **Narration** — one voice Ryan

## Stage 6: E-book Compilation (EPUB)
- [x] Compile the segmented chapters and assets into standard e-reader formats (EPUB/HTML).
  - *Note: `ch_00` (Frontmatter/TOC) is excluded from the final text compilations.*
- [x] Use a `make_epub_native.py` script to compile clean, spec-compliant EPUB3 books without dependencies.

## Stage 7: Metadata & Publishing Prep
- [ ] Calculate the total runtime of all audio files to determine Audible/ACX pricing tiers.
- [ ] Draft a catchy, sales-optimized Title, Subtitle, and Description.
- [ ] Draft an "About the Author" section for Niccolò Machiavelli.
- [ ] Determine the best target genres (e.g., Philosophy, Political Science, History).
- [ ] Digital Marketing & SEO: Ensure listing metadata leverages appropriate keywords.
- [ ] XHTML & Metadata Validation.

## Stage 8: Final Packaging & Audit
- [ ] Ensure all `.mp3` files are properly named and backed up in an `audio_archive` directory.
- [ ] Audit eBook for publisher-specific issues and device compatibility.
- [ ] Upload to the chosen publishing platforms (ACX, Google Play Books, etc.).
