# 🎙️ The Art of War — Audiobook Production Roadmap

**Author**: Sun Tzu  
**Target Edition**: English Multi-Voice Audiobook (`final_audio/`)  
**Directory**: `d:\git_repo\TKprof_book\books\art_of_war\`

---

## ⚙️ Audiobook Production Pipeline

```mermaid
flowchart TD
    VoiceMap[1. Voice Mapping] --> Tagging[2. Script JSON Generation]
    Tagging --> TTSGen[3. Multi-Voice Synthesis]
    TTSGen --> Normalization[4. FFmpeg Normalization]
    Normalization --> Audit[5. Authors Republic Quality Check]
```

---

## 🎭 Voice Mapping (Dual Male Cast)

| Role | Voice ID | Style & Direction |
| :--- | :--- | :--- |
| **Narrator / Commentary** | `en-US-AndrewNeural` | Authoritative, calm, military historian tone (`+0%`) |
| **Sun Tzu Direct Quotes** | `en-US-BrianNeural` | Resonant, strategic, tactical voice (`+2%`) |

---

## ⚙️ Technical Quality Standards (Authors Republic / ACX)

- **RMS Volume**: `-23.0 dB` to `-18.0 dB` (Target `-19.0 dB`)
- **Peak Level**: Max `-3.0 dB` (Target `-3.1 dB`)
- **Silence Padding**: Exactly `2.0s` clean room tone at both start and end
- **Bitrate**: `256 kbps CBR MP3`, `44.1 kHz`, 2-Channel

---

## 🏃 Progress Tracker

| Stage | Task | Status |
| :--- | :--- | :--- |
| **Stage 1** | Voice Mapping & Strategy Alignment | ✅ Complete |
| **Stage 2** | Dialogue Tagging & Script Generation | ⬜ Pending |
| **Stage 3** | Audio Track Synthesis (`generate_audio.py`) | ⬜ Pending |
| **Stage 4** | Normalization (`fix_audio_quality.py`) | ⬜ Pending |
| **Stage 5** | Compliance Quality Audit (`check_audio_quality.py`) | ⬜ Pending |
