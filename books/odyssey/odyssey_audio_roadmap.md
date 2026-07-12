# 🎙️ Odyssey Audiobook — Production Reference & Audiobook Roadmap

**Project**: The Odyssey (오디세이아) Audiobook  
**Version**: v1.0  
**Working Directory**: `D:\git_repo\TKprof_book\books\odyssey\`

---

## 📅 Full Pipeline Workflow

```
chapters/
  ch_01.txt ~ ch_24.txt
  introduction.txt
  copyright.txt
        │
        ▼
[ Stage 1 ] tag_dialogue.py / tag_dialogue_ko.py
  Tag dialogues using LLM (Gemini)
  → chapters/tagged/tagged_ch_NN.txt
        │
        ▼
[ Stage 2 ] prepare_scripts.py / prepare_scripts_ko.py
  Parse tagged text and assign voices
  → scripts/script_ch_NN.json
        │
        ▼
[ Stage 3 ] generate_audio.py / generate_audio_ko.py
  Synthesize segments using edge-tts (CBR/VBR MP3)
  → final_audio/final_track_NN.mp3 (26 files including intro/outro)
        │
        ▼
[ Stage 4 ] QA Auditing & Quality Check
  Verify against authors_republic_requirements.md
  using check_audio_quality.py
        │
        ▼
[ Stage 5 ] Part Concatenation (optional merging)
  → final_audio/merged/
        │
        ▼
[ Stage 6 ] Final Publishing
```

---

## 🎭 Character Cast & Microsoft Neural Voices (English Reference)

Below is the recommended character voice mapping for the English edition:

| Role (Tag) | Speaker | edge-tts Voice ID | Gender | Persona & Speed Setting |
| :--- | :--- | :--- | :--- | :--- |
| **narrator** | General Narrator | `en-US-AndrewNeural` | Male | Deep, engaging, epic storyteller pace (`-2%`) |
| **odysseus** | Odysseus | `en-US-BrianNeural` | Male | Courageous, rich, strong, and noble tone (`+0%`) |
| **telemachus**| Telemachus | `en-US-ChristopherNeural`| Male | Young, clear, earnest, and direct (`+2%`) |
| **penelope** | Penelope | `en-US-EmmaNeural` | Female | Soft, warm, melancholic, yet strong (`-2%`) |
| **athena** | Athena / Mentor | `en-US-JennyNeural` | Female | Wise, commanding, crisp, and clear (`+0%`) |
| **suitors** | Antinous & Suitors | `en-US-GuyNeural` | Male | Arrogant, loud, and demanding (`+3%`) |
| **others** | Eumaeus, Nestors, etc. | `en-US-EricNeural` | Male | Gritty, slow, and aged tone (`-5%`) |

---

## 📂 File Structure Map (Expected File Tree)

```
books/odyssey/
│
├── chapters/                        ← Segmented raw text chapters
│   ├── ch_01.txt ~ ch_24.txt
│   ├── introduction.txt
│   └── copyright.txt
│
├── scripts/                         ← JSON scripts for speech synthesis
│   ├── script_intro.json
│   ├── script_ch_01.json ~ script_ch_24.json
│   └── script_closing.json
│
├── final_audio/                     ← Output audio tracks (CBR MP3)
│   ├── final_track_00_intro.mp3
│   ├── final_track_01.mp3 ~ final_track_24.mp3
│   └── closing.mp3
│
├── prompt.txt                       ← Modernization guidelines
├── odyssey_roadmap.md               ← eBook tracking
└── odyssey_audio_roadmap.md         ← This document
```

---

## 🏃 Progress Tracker

| Stage | Task Description | Status |
| :--- | :--- | :--- |
| **Prep** | Get Gutenberg Source Text (`raw_source.txt`) | ✅ Complete |
| **Stage 1** | Segment into 24 Chapters | ✅ Complete |
| **Stage 2** | Tag Dialogues with LLM | ⬜ Pending |
| **Stage 3** | Convert to JSON Script | ⬜ Pending |
| **Stage 4** | Generate Audio with edge-tts | ⬜ Pending |
| **Stage 5** | Verify Quality with `check_audio_quality.py` | ⬜ Pending |
| **Stage 6** | Export & Publish | ⬜ Pending |
