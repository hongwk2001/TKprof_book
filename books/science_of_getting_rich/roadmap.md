# The Science of Getting Rich - Project Roadmap

**Author:** Wallace D. Wattles
**Status:** Planning

## Stage 1: Source Material Acquisition
- [x] Locate and download the raw public domain text (originally published in 1910).
- [x] Clean up the raw text (remove Gutenberg headers, extra formatting, etc.).
- [x] Save as `science_of_getting_rich_raw.txt`.

## Stage 2: Chapter Segmentation
- [x] Split the full text into separate raw chapters stored under `chapters/` directory:
  - `raw_ch_00.txt` (Frontmatter / Preface)
  - `raw_ch_01.txt` (Chapter I: The Right to Be Rich)
  - `raw_ch_02.txt` (Chapter II: There Is a Science of Getting Rich)
  - `raw_ch_03.txt` (Chapter III: Is Opportunity Monopolized?)
  - `raw_ch_04.txt` (Chapter IV: The First Principle in the Science of Getting Rich)
  - `raw_ch_05.txt` (Chapter V: Increasing Life)
  - `raw_ch_06.txt` (Chapter VI: How Riches Come to You)
  - `raw_ch_07.txt` (Chapter VII: Gratitude)
  - `raw_ch_08.txt` (Chapter VIII: Thinking in the Certain Way)
  - `raw_ch_09.txt` (Chapter IX: How to Use the Will)
  - `raw_ch_10.txt` (Chapter X: Further Use of the Will)
  - `raw_ch_11.txt` (Chapter XI: Acting in the Certain Way)
  - `raw_ch_12.txt` (Chapter XII: Efficient Action)
  - `raw_ch_13.txt` (Chapter XIII: Getting into the Right Business)
  - `raw_ch_14.txt` (Chapter XIV: The Impression of Increase)
  - `raw_ch_15.txt` (Chapter XV: The Advancing Man)
  - `raw_ch_16.txt` (Chapter XVI: Some Cautions, and Concluding Observations)
  - `raw_ch_17.txt` (Chapter XVII: Summary of the Science of Getting Rich)

## Stage 3: Language Modernization
- [ ] Modernize the language (if desired) to make it more accessible, prioritizing readability over historical authenticity:
  - **Create a custom `prompt.txt`** for the book outlining specific modernization rules (e.g., target audience, sentence breakdown for TTS, vocabulary preservation).
  - Process each segmented chapter using a `modernize_book.py` script.
  - Review modernized outputs for flow, tone, and ESL suitability.

## Stage 4: Intro and Copyright
- [ ] Draft the introduction and copyright texts (`introduction_en.txt`, `copyright_en.txt`).
  - Frame the context of the 1910 publication and its impact on the New Thought movement.

## Stage 5: Audio Production (TTS Generation)
- [ ] Set up `edge_tts` voices (e.g., Steffan, Christopher).
- [ ] Dialogue / paragraph tagging using XML voice tags.
- [ ] Convert chapters to structured JSON scripts.
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
- [ ] Draft an "About the Author" section for Wallace D. Wattles.
- [ ] Determine the best target genres (e.g., Personal Finance, Self-Help, New Thought).
- [ ] Digital Marketing & SEO: Ensure listing metadata leverages appropriate keywords.
- [ ] XHTML & Metadata Validation: `dc:date`, Book ID (UUID), `dcterms:modified`, `dc:description`.

## Stage 8: Final Packaging & Audit
- [ ] Ensure all `.mp3` files are properly named and backed up in an `audio_archive` directory.
- [ ] Audit eBook for publisher-specific issues and device compatibility.
- [ ] Upload to the chosen publishing platforms (ACX, Google Play Books, etc.).
