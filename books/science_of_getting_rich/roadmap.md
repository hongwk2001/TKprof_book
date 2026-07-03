# The Science of Getting Rich: Recreated as a Novel - Project Roadmap

This project aims to rewrite Wallace D. Wattles’ 1910 classic *The Science of Getting Rich* into a single, cohesive, chronological novel following a clear protagonist's journey, similar to the novelization of *The Richest Man in Babylon*.

---

## 🗺️ Execution Phases

### Stage 1: Outline & Structure
- [ ] Research and outline the character journey and setting (saved at `notes/linear_story_map.md`).
- [ ] Create the project directory `books/science_of_getting_rich/`.
- [x] Download the raw public domain text (`science_of_getting_rich_raw.txt`).
- [x] Create this `roadmap.md` file.

### Stage 2: Drafting Chapters (Novelization)
- [ ] Draft **Chapter 1: The Right to Be Rich** (Introducing the protagonist and their struggle with poverty).
- [ ] Draft **Chapter 2: The Science of Getting Rich** (Introducing the mentor and the concept of a natural science of wealth).
- [ ] Draft **Chapter 3: The Source of Abundance** (First principles: Thinking in a "Certain Way").
- [ ] Draft **Chapter 4: The Creative Mind** (Moving from the competitive mind to the creative mind).
- [ ] Draft **Chapter 5: Increasing Life** (Sowing value and growth for everyone).
- [ ] Draft **Chapter 6: The Law of Gratitude** (Developing the mindset of absolute gratitude).
- [ ] Draft **Chapter 7: Efficient Action** (Combining mental vision with immediate, powerful physical action).
- [ ] Draft **Chapter 8: The Impression of Increase** (Communicating success and growth to others).
- [ ] Draft **Chapter 9: The Advancing Man** (The final steps to success and realizing the vision).

### Stage 3: Language Polish & Quality Audit (TTS & ESL Optimization)
- [ ] Audit all chapters against `prompt.txt` guidelines:
  - Clean, modern, accessible English.
  - Break down complex, meandering sentences to optimize for listening.
  - Eliminate all archaic/obsolete grammar.
  - Remove formatting symbols (`*`, `_`) that trip up TTS engines.

### Stage 4: Audiobook Production
- [ ] Generate high-quality voice files using `edge-tts`.
- [ ] Mix tracks with a cinematic music intro and chapter transition bumpers.
- [ ] Verify timing, pronunciation, and audio clarity.

### Stage 5: E-book Compilation (EPUB)
- [ ] Set up the native EPUB compiler `make_epub_native.py` for this directory.
- [ ] Design and bundle a custom cover image.
- [ ] Build the final `the_science_of_getting_rich_linear.epub`.
