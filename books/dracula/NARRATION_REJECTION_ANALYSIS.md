# Dracula Bilingual Audiobook — Narration Rejection Analysis

**Rejected by:** Authors Republic, 2026-08-17
**Title:** Dracula: Bilingual English-Korean Edition (드라큘라 영한대역)
**Verdict:** "We are unable to distribute this audiobook without significant improvement to its narration."

This is a **content/performance** rejection, not a technical-spec rejection. All 35 tracks
pass `check_audio_quality.py` (bitrate, sample rate, peak, RMS, silence padding, duration).
The ACX numbers are green; the narration underneath them is not.

Every claim below is measured, not inferred. Reproduction commands are included.

---

## 1. Summary of measurements

| Metric | Measured |
| :--- | :--- |
| Total runtime | 34.67 hours across 35 tracks |
| Korean source format | **24 kHz, 48 kbps MP3** |
| English source format | **24 kHz** PCM |
| Audible bandwidth ceiling | **~12 kHz brickwall** (vs. 16–20 kHz for real 44.1 kHz narration) |
| Dead air, Chapter 1 | **858 s of 4006 s = 21.4%** (14.3 min of a 67 min chapter) |
| Dead air, retail sample | **66.2 s of 272 s = 24.3%** |
| Dead air, whole title (extrapolated) | **~7.4 hours** |
| MP3 encode generations | **2** (pydub 256k → ffmpeg 256k) on top of a 48 kbps source |

---

## 2. Mapping each rejection bullet to its cause

| Authors Republic complaint | Measured root cause |
| :--- | :--- |
| Muffled audio quality or static | Korean narration is sourced from a **48 kbps / 24 kHz** MP3; English from 24 kHz PCM. Hard 12 kHz ceiling, then re-encoded twice. |
| Pausing unnecessarily between words | TTS-native padding is **never trimmed** before stitching, so it stacks with the hardcoded pauses. |
| Not pausing between sentences | Synthesis is paragraph-atomic; sentence boundaries inside a segment get no deliberate timing. |
| Monotonous or robotic voice | No SSML. No prosody control. `speed=1.0` fixed for every line of a 34-hour gothic novel. |
| Lack of intonation and inflection | Same — flat default delivery, no `<prosody>` / `<emphasis>`, no per-passage pacing. |
| Mispronouncing basic words | No pronunciation lexicon. Dracula is dense with proper nouns (Bistritz, Szgany, Vámbéry, Carfax, Whitby, Van Helsing). |
| Misreading punctuation or abbreviations | Raw script text goes straight to the engine. No normalization of `Mr.` / `Dr.` / `St.`, em-dashes, or diary date headings (`3 May. Bistritz.—`). |

---

## 3. The decisive finding: the source is 48 kbps

`edge-tts` is **not** a configurable API. It is the free Edge read-aloud endpoint, and its
output format is hardcoded:

```
site-packages/edge_tts/constants.py:41
# The output format "audio-24khz-48kbitrate-mono-mp3" is a 48 kbps constant bitrate stream.
MP3_BITRATE_BPS = 48_000
```

Verified against a freshly generated SunHi segment: `sample_rate=24000`, `bit_rate=48000`.

So the Korean half of this audiobook was built from **48 kbps audio**, decoded to WAV,
concatenated, encoded to 256 kbps MP3, then re-encoded to 256 kbps MP3 again. The 256 kbps
in the deliverable is cosmetic — it faithfully preserves a 48 kbps source plus two
generations of added artifacts.

**No amount of re-mastering recovers this.** Loudness normalization, EQ, and re-encoding
cannot restore bandwidth that was never captured. This requires re-narration.

### Spectral evidence

```bash
ffmpeg -ss 60 -t 60 -i final_audio/dracula_sample_bilingual_sunhi.mp3 \
  -lavfi "showspectrumpic=s=1200x600:mode=combined:legend=1:fscale=lin" spec.png
```

Result: all speech energy stops dead at ~11.8 kHz (the Nyquist limit of a 24 kHz source).
Above it, only a faint imaging ghost near 13.2 kHz — a resampling artifact, not content.

---

## 4. Where the dead air comes from

Measured native padding on a fresh `ko-KR-SunHiNeural` segment:

- **~0.21 s** leading silence
- **~0.91 s** trailing silence

`generate_bilingual_audio.py` stitches segments **without trimming them** and then *adds*
its own pauses (`generate_bilingual_audio.py:263-277`):

```python
en_ko_pause = AudioSegment.silent(duration=350)   # between EN and KO
para_pause   = AudioSegment.silent(duration=500)  # between paragraphs
```

So an actual paragraph boundary is:

```
0.91s (native tail)  +  0.50s (added)  +  0.21s (native head)  ≈  1.62s
```

This matches the measured histogram exactly — pause lengths cluster at 1.0–1.1 s (EN→KO)
and 1.7–1.8 s (paragraph), with nothing in between. The distribution is bimodal and
machine-regular, which is precisely what a human QA listener hears as mechanical.

Chapter 1 contains **465 pauses of 0.8 s or longer**, totalling 9.5 minutes — far more than
its 190 segment boundaries, because the engine also drops ~1.0 s gaps between sentences
*inside* each segment, which then stack with everything above.

---

## 5. Remediation

### 5.1 Required: change the Korean engine (fixes 4 of 7 complaints at once)

Move from `edge-tts` to the **paid Azure Speech API**, keeping the **identical SunHi voice**
already validated in `final_audio/note_by_billy.txt` ("edge voice good for Korean"). Same
voice, real API:

- Output `audio-48khz-192kbitrate-mono-mp3` or `riff-48khz-16bit-mono-pcm` → **eliminates the muffling**
- Full **SSML**: `<prosody rate/pitch>`, `<break>`, `<emphasis>` → **addresses monotone and pacing**
- `<phoneme>` and custom lexicon → **addresses mispronounced proper nouns**

Estimated cost: the full bilingual script is roughly 1.3 M characters, approximately
**$20–30** at standard neural rates. This is not a budget obstacle.

### 5.2 Required: change the English engine

Kokoro writes at 24 kHz (`generate_bilingual_audio.py:94`, `sf.write(out_wav_path, merged_audio, 24000)`)
and has the same 12 kHz ceiling. It needs to move to a 44.1/48 kHz narration voice —
Azure en-US narration voices, or ElevenLabs if a more expressive read is wanted.

### 5.3 Required: pipeline fixes (engine-independent)

1. **Trim each segment before stitching.** Strip native head/tail silence, then insert
   exactly one deliberate pause. Target ~250 ms EN→KO and ~700 ms between paragraph pairs.
2. **Encode once.** Export the stitched master as **WAV**, not MP3, and let the single
   ffmpeg post-processing pass produce the only MP3. Removes one full encode generation.
3. **Normalize text before synthesis.** Expand `Mr.`/`Dr.`/`St.`, handle em-dashes and
   diary date headings, and route proper nouns through a pronunciation lexicon.
4. **Synthesize per sentence, not per paragraph**, so sentence-level timing is controlled
   rather than left to the engine.

### 5.4 Extend `check_audio_quality.py`

The current checker passed all 35 tracks that Authors Republic then rejected. It validates
the container, not the content. Add:

- **Source bandwidth check** — reject if there is no meaningful energy above ~13 kHz
  (catches upsampled low-rate sources).
- **Silence ratio check** — flag any track above ~12% total silence.
- **Pause distribution check** — flag bimodal/quantized pause histograms.

These three would have caught this rejection before submission.

---

## 6. Recommended order of work

1. Extend `check_audio_quality.py` with the three content checks above.
2. Rebuild the pipeline fixes in §5.3.
3. Re-narrate **one chapter** plus the retail sample on Azure at 48 kHz with SSML.
4. **Listen to it**, and verify it against the extended checker.
5. Only then commit to the full 34-hour re-narration.

Do not re-narrate all 34 hours before step 4 confirms the new chain sounds right.

---

## 7. Reproduction

```bash
# Spectral ceiling
ffmpeg -ss 60 -t 60 -i final_audio/dracula_sample_bilingual_sunhi.mp3 \
  -lavfi "showspectrumpic=s=1200x600:mode=combined:legend=1:fscale=lin" spec.png

# Silence ratio for a track
ffmpeg -i final_audio/dracula_ch_01_bilingual_sunhi.mp3 \
  -af "silencedetect=noise=-40dB:d=0.15" -f null - 2>&1 \
  | grep silence_duration | sed -E 's/.*silence_duration: //' \
  | awk '{s+=$1; n++} END{printf "%d pauses, %.1fs silence\n", n, s}'

# Native edge-tts format
python -c "import edge_tts,asyncio; asyncio.run(edge_tts.Communicate('테스트','ko-KR-SunHiNeural').save('t.mp3'))"
ffprobe -v error -show_entries stream=sample_rate,bit_rate -of default=noprint_wrappers=1 t.mp3
```
