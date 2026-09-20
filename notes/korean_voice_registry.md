# Korean Voice Registry & Selection Guide

This note documents the evaluated and verified Korean neural voice options for bilingual audiobooks, covering offline local GPU voices (Qwen3-TTS) and cloud voices (Edge-TTS).

---

## 🟢 Qwen3-TTS Local GPU Korean Voices (Recommended for Offline High Quality)

All Qwen3-TTS Korean voices run offline on the local GPU (NVIDIA RTX 3080) at 44.1 kHz native sample rate with natural neural inflection:

| Voice Name | Gender | Pitch & Tone Style | Best Use Cases | ACX Quality Status |
| :--- | :--- | :--- | :--- | :--- |
| **`Vivian`** | Female | Bright, expressive, natural modern Korean cadence | Primary Korean female narrator, dialogues | **`[PASS]`** (-21.1 dB RMS, -3.5 dB Peak) |
| **`Sohee`** | Female | Calm, polite (`하십시오체`), elegant reading tone | Formal audiobooks, philosophical/historical texts | **`[PASS]`** (-21.0 dB RMS, -3.5 dB Peak) |
| **`Ono_Anna`** | Female | Gentle, clear diction, serene reading style | Warm storytelling, secondary female roles | **`[PASS]`** (-21.1 dB RMS, -3.5 dB Peak) |
| **`Uncle_Fu`** | Male | Deep, mature, authoritative male narrator tone | Primary Korean male narrator, elder characters | **`[PASS]`** (-22.0 dB RMS, -3.5 dB Peak) |

---

## 🔵 Edge-TTS Cloud Korean Voices

| Voice Name | Gender | Tone Style | Best Use Cases | ACX Quality Status |
| :--- | :--- | :--- | :--- | :--- |
| **`ko-KR-SunHiNeural`** | Female | Standard modern Korean female voice | Secondary cloud fallback | **`[PASS]`** (-20.8 dB RMS, -4.8 dB Peak) |
| **`ko-KR-InJoonNeural`** | Male | Standard modern Korean male voice | Secondary cloud fallback | **`[PASS]`** (-21.8 dB RMS, -3.5 dB Peak) |

---

## Sample Audio Clip References

Sample MP3 introduce tracks generated and verified in `books/dracula/final_audio/`:
- `sample_voice_ko_vivian.mp3`
- `sample_voice_ko_sohee.mp3`
- `sample_voice_ko_ono_anna.mp3`
- `sample_voice_ko_uncle_fu.mp3`
- `sample_voice_ko_sunhi_edge.mp3`
- `sample_voice_ko_injoon_edge.mp3`
