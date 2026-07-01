# The Richest Man in Babylon - Project Roadmap

**Author:** George S. Clason
**Status:** Planning

## Stage 1: Source Material Acquisition
- [x] Locate and download the raw public domain text (originally published in 1926).
- [x] Clean up the raw text (remove Gutenberg headers, extra formatting, etc.).
- [x] Save as `raw_source.txt`.

## Stage 2: Chapter Segmentation
- [x] Split the full text into separate raw chapters stored under `chapters/` directory (e.g., `raw_ch_00.txt`, `raw_ch_01.txt`, referencing the Blue Castle project segmentation style).

## Stage 3: Language Modernization
- [/] Modernize the language (if desired) to make it more accessible ,
     prioritize readability over historical authenticity
     - **Create a custom `prompt.txt`** for the book outlining specific modernization rules (e.g., target audience, sentence breakdown for TTS, vocabulary preservation).
     - Process each segmented chapter using `modernize_book.py` (which will automatically read `prompt.txt`).
       - [x] Chapter 00: Frontmatter
       - [x] Chapter 01: About the Author
       - [x] Chapter 02: Foreword
       - [x] Chapter 03: An Historical Sketch of Babylon
       - [x] Chapter 04: The Man Who Desired Gold
       - [x] Chapter 05: The Richest Man in Babylon
       - [x] Chapter 06: Seven Cures For a Lean Purse
       - [x] Chapter 07: Meet the Goddess of Good Luck
       - [x] Chapter 08: The Five Laws of Gold
       - [x] Chapter 09: The Gold Lender of Babylon
       - [x] Chapter 10: The Walls of Babylon
       - [x] Chapter 11: The Luckiest Man in Babylon
     - Review modernized outputs for flow, tone, and ESL suitability

## Stage 4: Intro and Copyright
- [x] Draft the introduction and copyright texts (`introduction_en.txt`, `copyright_en.txt`).
     - Incorporate notes from `note.txt` into the introduction.
     - Frame the context of the 1926 publication and its timeless financial wisdom.

## Stage 5: Audio Production (TTS Generation)
- [x] Set up `edge_tts` (Steffan/Arkad, Christopher/Narrator, Ryan/Rest characters).
- [x] Dialogue tagging with `<arkad>` and `<rest>` XML tags via subagent swarm.
- [x] Convert tagged chapters to structured JSON scripts (`scripts/script_ch_*.json`).
- [x] Generate TTS clips and mix final audio per chapter (`final_audio/final_ch_*.mp3`).
- [x] Verify audio quality and pacing.

### 🎵 Audio Structure (per chapter)
Each chapter audio is assembled in this order:
1. **Cinematic Intro** — `freesound_community-cinematic-intro-6097.mp3` (dramatic opening)
2. **Bach Bumper (Intro)** — `background.mp3` first 7s, fade-in → fade-out
3. **Bell Chime** — `chime.mp3` (user-selected soft bell from freesound.org)
4. **Narration** — Multi-voice TTS (Christopher/Narrator, Steffan/Arkad, Ryan/Rest)
5. **Bell Chime** — `chime.mp3` (closing)
6. **Bach Bumper (Outro)** — `background.mp3` 7–14s, fade-in → fade-out

### 🛠 Scripts
- `generate_audio.py` — Full generation (TTS + mix), use for new chapters
- `remix_audio.py` — Fast remix only (reuses cached clips), use to change music/chime

## Stage 6: E-book Compilation (Reference: Blue Castle Project)
- [ ] Compile the segmented chapters and assets into standard e-reader formats (EPUB/HTML).
- [ ] Use the `make_epub_native.py` script to compile clean, spec-compliant EPUB3 books without dependencies.

## Stage 7: Metadata & Publishing Prep
- [ ] Calculate the total runtime of all audio files to determine Audible/ACX pricing tiers.
- [ ] Draft a catchy, sales-optimized Title, Subtitle, and Description.
- [ ] Draft an "About the Author" section for George S. Clason.
- [ ] Determine the best target genres (e.g., Personal Finance, Classics, Wealth Management).
- [ ] Digital Marketing & SEO: Ensure listing metadata leverages appropriate keywords.
- [ ] XHTML & Metadata Validation: `dc:date`, Book ID (UUID), `dcterms:modified`, `dc:description`.

## Stage 8: Final Packaging & Audit
- [ ] Ensure all `.mp3` files are properly named and backed up in an `audio_archive` directory.
- [ ] Audit eBook for publisher-specific issues and device compatibility (following Blue Castle audit standards).
- [ ] Upload to the chosen publishing platforms (ACX, Google Play Books, etc.).
