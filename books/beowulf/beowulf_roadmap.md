# Beowulf (Modern English Edition) - Audiobook Project Roadmap

**Author:** Anonymous (circa 8th–11th Century AD)
**Status:** Audio Production

---

## ⚙️ The Audiobook Production Pipeline

```mermaid
flowchart LR
    Ingest[1. Ingest Raw Text] --> Segment[2. Segment Chapters]
    Segment --> Modernize[3. Audiobook Modernization]
    Modernize --> OpenClose[4. Open & Close Pages]
    OpenClose --> AudioGen[5. Audio Production (TTS)]
    AudioGen --> MetaPrep[6. Metadata & Publishing Prep]
    MetaPrep --> Packaging[7. Final Packaging & Audit]
```

---

## Stage 1: Source Material Acquisition
- [x] Locate and download the raw public domain text.
- [x] Clean up the raw text, keeping both Old English and translation references.
- [x] Save as `Beowulf_original.txt`.

## Stage 2: Chapter Segmentation
- [x] Split the full text into separate fitts (chapters) based on Roman numeral headings.
- [x] Save chapter files under `chapters/` (and subsequently `chapters_en_v2/` for modernized versions).

## Stage 3: Language Modernization & Audiobook Flow Pass
- [x] Convert the Old English poem into modernized prose narrative (a novel-like story) optimized for listening.
- [x] Remove em-dashes, apply subject-first word order, simplify rhythm, and clarify archaic kennings (e.g., "curved prow" instead of "ring-necked").
- [x] Complete modernized pass for Prologue (`ch_00_en.txt`) and all chapters up to `ch_43_en.txt` stored in `chapters_en_v2/`.

## Stage 4: Intro and Copyright / Closing
- [x] Draft introduction (`introduction_en_v2.txt`) and copyright closing (`copyright_en_v2.txt`) inside `chapters_en_v2/`.
- [x] Frame the historical context of the manuscript's survival and its status as the first 'overpowered' fantasy hero in English history.

## Stage 5: Audio Production (Multi-Voice TTS Generation)
- [ ] Define the multi-voice character configuration using Kokoro voices:
  - **Narrator**: `am_michael` (Michael)
  - **Beowulf**: `bm_george` (George)
  - **Hrothgar**: `bm_george` (George) or custom voice
  - **Unferth / Wiglaf**: `am_adam` (Adam)
  - **Wealhtheow / Female**: `bf_emma` (Emma)
- [ ] Run a dialogue tagger script to insert character tags (e.g., `<beowulf>`, `<hrothgar>`, etc.) into the modernized text.
- [ ] Convert tagged text files to JSON dialogue scripts (`scripts/script_ch_*.json`).
- [ ] Create `generate_audio.py` that utilizes the python `kokoro` library and `soundfile` to render narration and character lines.
- [ ] Generate TTS clips and mix final audio:
  - **Intro Track**: `final_track_00_intro.mp3` (from `introduction_en_v2.txt`).
  - **Chapters**: `final_track_00.mp3` through `final_track_43.mp3` (mixed with cinematic bumper).
  - **Closing Track**: `closing.mp3` (from `copyright_en_v2.txt` mixed with full cinematic outro).
  - **Sample Track**: `sample.mp3` (Concatenation of intro and Prologue, limited to under 5 minutes).
- [ ] Verify audio quality, pacing, and 256kbps bitrate format.

### 🎵 Audio Structure (per track)
1. **Cinematic Intro** — `freesound_community-cinematic-intro-6097.mp3` (opening theme)
   - Play 4.5 seconds at the beginning of the Intro track.
   - Play 2.0 seconds at the beginning of each chapter track.
   - Play full length of the music at the end of the Closing track.
2. **Narration** — Multi-voice Kokoro TTS pipeline based on character dialogue script.

---

## Stage 6: Metadata & Publishing Prep
- [ ] Calculate the total runtime of all audio files to determine Audible/ACX pricing tiers.
- [ ] Draft a catchy, sales-optimized Title, Subtitle, and Description.
- [ ] Draft an "About the Author" section for the anonymous poet.
- [ ] Determine the best target genres (e.g., Epic Poetry, Action, Fantasy, Classics).
- [ ] Digital Marketing & SEO: Ensure listing metadata leverages appropriate keywords.

---

## Stage 7: Final Packaging & Audit
- [ ] Ensure all `.mp3` files are properly named and backed up in an `audio_archive` directory.
- [ ] Audit audio for quality, silence spacing, and ACX technical compliance.
- [ ] Upload to the chosen publishing platforms (ACX, Google Play Books, etc.).
