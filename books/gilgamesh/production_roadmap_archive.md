# Production Roadmap & Tracker: The Epic of Gilgamesh (2-Part Podcast)

This document tracks the end-to-end production pipeline specifically for **The Epic of Gilgamesh** formatted as a 2-part podcast series (~40 minutes total running time) optimized for middle-school level ESL students.

---

## ⚙️ The 6-Stage Production Pipeline Status

```mermaid
flowchart LR
    Ingest[1. Ingest Raw Text\nComplete] --> Modernize[2. Simplify & Translate\nComplete]
    Modernize --> Segment[3. Chapter Split\nComplete]
    Segment --> Voice[4. Voice Map\nComplete]
    Voice --> Render[5. Batch TTS\nComplete]
    Render --> Publish[6. Publish\nIn Progress]
    
    style Ingest fill:#4CAF50,stroke:#388E3C,color:#fff
    style Modernize fill:#4CAF50,stroke:#388E3C,color:#fff
    style Segment fill:#4CAF50,stroke:#388E3C,color:#fff
    style Voice fill:#4CAF50,stroke:#388E3C,color:#fff
    style Render fill:#4CAF50,stroke:#388E3C,color:#fff
    style Publish fill:#FF9800,stroke:#F57C00,color:#fff
```

| Stage | Action Description | Target Outputs / Locations | Status |
| :---: | :--- | :--- | :---: |
| **1** | **Ingest Raw Text** | [books/gilgamesh/raw_source.txt](file:///d:/git_repo/thefirstaicompany/books/gilgamesh/raw_source.txt) | **`[x]` Complete** |
| **2** | **Modernize & Translate (Dual-Lang)** | [modern_draft_prt_1_en.txt](file:///d:/git_repo/thefirstaicompany/books/gilgamesh/modern_draft_prt_1_en.txt), [modern_draft_prt_1_ko.txt](file:///d:/git_repo/thefirstaicompany/books/gilgamesh/modern_draft_prt_1_ko.txt), [modern_draft_prt_2_en.txt](file:///d:/git_repo/thefirstaicompany/books/gilgamesh/modern_draft_prt_2_en.txt), [modern_draft_prt_2_ko.txt](file:///d:/git_repo/thefirstaicompany/books/gilgamesh/modern_draft_prt_2_ko.txt) | **`[x]` Complete** |
| **3** | **Chapter Segmentation** | [chapters/ch_01_en.txt to ch_06_ko.txt](file:///d:/git_repo/thefirstaicompany/books/gilgamesh/chapters/) | **`[x]` Complete** |
| **4** | **Voice Scheme & Phonetics** | [tts_config.json](file:///d:/git_repo/thefirstaicompany/books/gilgamesh/tts_config.json) & [prepare_scripts.py](file:///d:/git_repo/thefirstaicompany/books/prepare_scripts.py) casting | **`[x]` Complete** |
| **5** | **Batch Audio Rendering & Stitching** | [audio/podcast_prt_1_en.mp3 to podcast_prt_2_ko.mp3](file:///d:/git_repo/thefirstaicompany/books/gilgamesh/audio/) | **`[x]` Complete** |
| **6** | **Multi-Channel Publishing Assets** | Static-image MP4 videos, SRT subtitles, distribution links | **`[/]` In Progress** |

---

## 🎙️ Podcast Packaging Structure

The audio files are stitched and compiled into a 2-part structure to prevent long-listening fatigue for ESL learners.

### Part 1: The Coming of Enkidu and The Great Forest Campaign
*   **Chapters Included**: 
    *   **Chapter 1**: The Wild Man of the Forest
    *   **Chapter 2**: The Great Battle and Friendship
    *   **Chapter 3**: The Battle in the Cedar Forest
*   **Outputs**:
    *   🇺🇸 English Track: [podcast_prt_1_en.mp3](file:///d:/git_repo/thefirstaicompany/books/gilgamesh/audio/podcast_prt_1_en.mp3) *(~17.9 MB)*
    *   🇰🇷 Korean Track: [podcast_prt_1_ko.mp3](file:///d:/git_repo/thefirstaicompany/books/gilgamesh/audio/podcast_prt_1_ko.mp3) *(~22.8 MB)*

### Part 2: The Quest for Immortality and The Return
*   **Chapters Included**:
    *   **Chapter 4**: The Bull of Heaven and Enkidu's Fate
    *   **Chapter 5**: The Search for Immortality
    *   **Chapter 6**: The Great Flood and the Return
*   **Outputs**:
    *   🇺🇸 English Track: [podcast_prt_2_en.mp3](file:///d:/git_repo/thefirstaicompany/books/gilgamesh/audio/podcast_prt_2_en.mp3) *(~16.2 MB)*
    *   🇰🇷 Korean Track: [podcast_prt_2_ko.mp3](file:///d:/git_repo/thefirstaicompany/books/gilgamesh/audio/podcast_prt_2_ko.mp3) *(~20.4 MB)*

---

## 👥 Voice Cast Configuration

Voices are configured using the local **Kokoro-82M** engine for primary voices (English) and **Edge-TTS** (online fallback) for secondary/Korean roles.

| Role | Character Description | English Voice Engine/Voice | Korean Voice Engine/Voice |
| :--- | :--- | :--- | :--- |
| **Narrator** | Overall Storyteller | Kokoro (`am_michael`) | Edge-TTS (`ko-KR-InJoonNeural`) |
| **Gilgamesh** | King of Uruk (Protagonist) | Kokoro (`bm_george`) | Edge-TTS (`en-US-BrianMultilingualNeural`) |
| **Enkidu** | Wild Man of the Grasslands | Edge-TTS (`en-GB-RyanNeural`) | Edge-TTS (`ko-KR-InJoonNeural`) |
| **Shamhat** | Temple Priestess of Uruk | Kokoro (`af_bella`) | Edge-TTS (`ko-KR-SunHiNeural`) |
| **Ishtar** | Goddess of Love and War | Edge-TTS (`en-GB-SoniaNeural`) | Edge-TTS (`ko-KR-SunHiNeural`) |
| **Siduri** | Wise Tavern Keeper at Sea | Kokoro (`af_bella`) | Edge-TTS (`ko-KR-SunHiNeural`) |
| **Utnapishtim** | Ancient Sage / Flood Survivor | Edge-TTS (`en-US-BrianNeural`) | Edge-TTS (`ko-KR-InJoonNeural`) |
| **Utnapishtim's Wife** | Utnapishtim's Companion | Edge-TTS (`en-US-JennyNeural`) | Edge-TTS (`ko-KR-SunHiNeural`) |
| **Huwawa** | Guardian of the Cedar Forest | Edge-TTS (`en-GB-RyanNeural`) | Edge-TTS (`ko-KR-HyunsuMultilingualNeural`) |
| **ScorpionMan** | Guardian of Mount Mashu | Edge-TTS (`en-GB-RyanNeural`) | Edge-TTS (`ko-KR-InJoonNeural`) |
| **Hunter** | Discoverer of Enkidu | Edge-TTS (`en-US-BrianNeural`) | Edge-TTS (`ko-KR-InJoonNeural`) |
| **Father** | Hunter's Father | Edge-TTS (`en-US-BrianNeural`) | Edge-TTS (`ko-KR-HyunsuMultilingualNeural`) |

---
