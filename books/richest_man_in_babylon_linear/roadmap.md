# The Richest Man in Babylon: Recreated as a Novel - Project Roadmap

This project aims to rewrite George S. Clason’s classic *The Richest Man in Babylon* into a single, cohesive, chronological novel following the journey of Tarkad under the mentorship of Arkad and Mathon.

---

## 🗺️ Execution Phases

### Stage 1: Outline & Structure
- [x] Create linear story map (saved at `notes/linear_story_map.md`).
- [x] Initialize new project directory `books/richest_man_in_babylon_linear/`.
- [x] Create this `roadmap.md` file.
- [x] Draft the introduction and copyright texts (`introduction_en.txt`, `copyright_en.txt`).

### Stage 2: Drafting Chapters (Target: ~44,000 words total)
- [x] Draft **Chapter 1: The Golden City of Barefoot Men** (~3,000 words)
- [x] Draft **Chapter 2: The Scribe's Legacy** (~4,000 words)
- [x] Draft **Chapter 3: The Temple of Learning (The Seven Cures)** (~6,000 words)
- [x] Draft **Chapter 4: The Gold Lender's Scales** (~4,000 words)
- [x] Draft **Chapter 5: The Five Laws of Gold** (~4,000 words)
- [x] Draft **Chapter 6: The Syrian Trail (Dabasir's Escape)** (~6,500 words)
- [x] Draft **Chapter 7: The Debt Cleansing (The 70-20-10 Plan)** (~4,000 words)
- [x] Draft **Chapter 8: The Luckiest Man in Babylon** (~5,500 words)
- [x] Draft **Chapter 9: The Legacy of Babylon** (~2,000 words)
- [x] Draft **Epilogue: The Nottingham Letters** (~1,500 words)

### Stage 3: Language Polish & Quality Audit
- [ ] Review all chapters to ensure conversational flow, simple vocabulary (ideal for ESL/casual listeners), and consistent tone.
- [ ] Ensure all key financial principles are clearly highlighted.

### Stage 4: Audiobook Production (TTS Generation)
- [ ] Tag characters in drafted chapters (e.g., `<narrator>`, `<tarkad>`, `<arkad>`, `<mathon>`, `<dabasir>`).
- [ ] Convert tagged chapters to structured scripts (`scripts/script_ch_*.json`).
- [ ] Generate high-quality voice clips using `edge-tts`.
- [ ] Mix final tracks per chapter with the cinematic intro music.
- [ ] Verify timing, pronunciation, and audio clarity.

### Stage 5: E-book Compilation (EPUB)
- [ ] Copy and configure the native EPUB compiler `make_epub_native.py` for this directory.
- [ ] Build the final `the_richest_man_in_babylon_linear.epub` using the custom cover image.
- [ ] Verify EPUB metadata and styling.

### Stage 6: Metadata & Publishing Setup
- [ ] Finalize metadata (suggested price: $2.99).
- [ ] Calculate total audiobook runtime to determine Audible pricing brackets.
- [ ] Package final `.epub` and `.mp3` assets for release.
