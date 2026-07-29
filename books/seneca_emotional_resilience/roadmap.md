# 📚 Stoic Treatises on Emotional Resilience — eBook & Audio Roadmap

**Author**: Lucius Annaeus Seneca  
**Edition**: Modernized English Edition (`seneca_emotional_resilience_en.epub`)  
**Directory**: `d:\git_repo\TKprof_book\books\seneca_emotional_resilience\`

---

## ⚙️ Production Pipeline

```mermaid
flowchart LR
    Source[1. Source Acquisition] --> Segment[2. Chapter Segmentation]
    Segment --> Modernize[3. Text Modernization Pass]
    Modernize --> IntroClose[4. Intro & Copyright Prep]
    IntroClose --> EPUBGen[5. Native EPUB Generation]
    EPUBGen --> AudioPrep[6. TTS Audio Generation]
```

---

## 📋 Chapter Plan Structure

To preserve the original structure of Seneca's treatises, the files will be organized under separate subdirectories for each work:

### 1. On Anger (*De Ira*)
Located in `chapters/1.on_anger/`:
*   **Book I** (Chapters 1–21): Named as `on_anger_book1_ch01_en.txt` to `on_anger_book1_ch21_en.txt`
*   **Book II** (Chapters 1–36): Named as `on_anger_book2_ch01_en.txt` to `on_anger_book2_ch36_en.txt`
*   **Book III** (Chapters 1–43): Named as `on_anger_book3_ch01_en.txt` to `on_anger_book3_ch43_en.txt`

### 2. On Tranquillity of Mind (*De Tranquillitate Animi*)
Located in `chapters/2.tranquillity_of_mind/`:
*   Chapters 1–17: Named as `tranquillity_ch01_en.txt` to `tranquillity_ch17_en.txt`

### 3. On Constancy (*De Constantia Sapientis*)
Located in `chapters/3.constancy/`:
*   Chapters 1–19: Named as `constancy_ch01_en.txt` to `constancy_ch19_en.txt`

### 4. On Providence (*De Providentia*)
Located in `chapters/4.providence/`:
*   Chapters 1–6: Named as `providence_ch01_en.txt` to `providence_ch06_en.txt`

---

## 🏃 Progress Tracker

| Stage | Task | Status | Details |
| :--- | :--- | :--- | :--- |
| **Stage 1** | Directory Setup & Document Framing | ✅ Complete | Directory created, metadata, prompt, and roadmap initialized. |
| **Stage 2** | Raw Source Text Acquisition | ✅ Complete | Downloaded Gutenberg eBook #64576 (Aubrey Stewart's 1889 translation). |
| **Stage 3** | Chapter Segmentation & Setup | ✅ Complete | Split raw texts into book/chapter structure inside the `chapters/` directory. |
| **Stage 4** | Text Modernization & Verification | ✅ Complete | Applied modernization prompt across all 142 chapters using parallel pro subagents. |
| **Stage 5** | EPUB Formatting & Packaging | ⬜ Pending | Generate standard ePUB using Python builder. |
| **Stage 6** | Audio Script & TTS Generation | ⬜ Pending | Prepare TTS json scripts and run quality checks. |
