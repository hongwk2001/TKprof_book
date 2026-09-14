# TKprof_book — Project Instructions

Public-domain classics reworked into bilingual (English/Korean) EPUBs and
audiobooks, distributed through Authors Republic, KDP, and Google Play.

> Rewritten 2026-09-14. The previous version of this file was copied verbatim
> from the `thefirstaicompany` project at the initial commit and described a
> `.swarm/` agent daemon, a triage-cockpit approval gate, `reels/`, and a `dev`
> branch convention — none of which have ever existed in this repository.

---

## Environment

**Always use the repo-root venv.** The system Python 3.11 on this machine has
none of the project dependencies:

```
venv/Scripts/python.exe        # Python 3.11.9 — numpy, soundfile, kokoro,
                               # azure-cognitiveservices-speech
```

`ffmpeg` and `ffprobe` must be on PATH; the whole audio chain shells out to them.

---

## Layout

* `books/<title>/` — one directory per book, self-contained. Typical contents:
  * `chapters/`, `scripts/` — source text and per-chapter synthesis scripts (JSON)
  * `make_epub_*.py`, `make_*_audiobook*.py` — per-book builders
  * `final_audio*/` — deliverables (`_en`, `_ko`, `_ar_ready` variants)
  * `temp_audio*/` — WAV masters and scratch; not deliverables
  * `*_roadmap.md`, `metadata.md` — production status and store metadata
* `authors_republic_requirements.md` — distributor technical + content spec
* `check_audio_quality.py` — the QC gate (see below)
* Repository root also holds a large amount of accumulated scratch (`b1.json`,
  `all_lines.txt`, one-off `patch_*.py` / `fix_*.py`). Root is **not** curated —
  do not infer conventions from it, and do not add more to it. Use the
  session scratchpad for temporary files.

---

## Audiobook QC gate

Every track must pass before any Authors Republic submission:

```bash
venv/Scripts/python.exe check_audio_quality.py books/<title>/final_audio_en
```

It checks container specs (192 kbps CBR, 44.1 kHz, peak, RMS, lead/trail
silence, duration) **and** three narration-content measures added after the
rejections below:

| Check | Fails when | Why |
| :--- | :--- | :--- |
| Source bandwidth | no energy above 13 kHz | a 24 kHz source upsampled to 44.1 kHz; reads as muffled |
| Silence ratio | above 12% of the narration body | dead air; the rejected build ran 17% |
| Pause distribution | *warning* above 30% in one 100 ms bucket | fixed pause constants sound mechanical |

The silence and pause measures cover the narration body only, excluding the
AR-mandated lead/trail padding, and are skipped for tracks with under 30 s of
body — otherwise a compliant 10 s credits track scores 60% silence and fails.
The pause threshold is an uncalibrated heuristic — it is a warning, not an
error. See the caveat comment in the source.

---

## Narration engines — read before building audio

**Kokoro and edge-tts must not be used for Authors Republic audio.** Both render
at 24 kHz with no SSML and no prosody control. Audiobooks built on them were
rejected twice:

* **2026-08-17** — Dracula bilingual: muffled, monotone, excessive pausing
* **2026-09-14** — Dracula English: "monotonous or robotic voice"

The second build had already fixed every *pipeline* defect (dead air, double
encoding, text normalization, multi-voice casting) and was still refused,
because the engine itself cannot produce intonation or bandwidth.

Full diagnosis, measurements, and reproduction commands:
`books/dracula/NARRATION_REJECTION_ANALYSIS.md`

Current replacement path — Azure Neural TTS at 48 kHz with per-sentence SSML
prosody, reusing the existing pipeline unchanged:

```bash
cd books/dracula
AZURE_SPEECH_KEY=<key> AZURE_SPEECH_REGION=<region> \
  ../../venv/Scripts/python.exe make_english_audiobook_azure.py voices   # casting demo
```

Then `... 1` for a chapter, `... verify` for the A/B against the Kokoro build.
Credentials come from the environment and are never committed.

**Render one chapter and listen to it before committing to a full book.** A
34-hour re-narration is the expensive way to discover the voice is wrong.

---

## Branching

One branch per book: `dracula`, `the_heroes`, `tono_bungay`, `art_of_war`,
`secret_garden`, `beowulf_kr`. Work on the branch for the book being changed;
`main` is the integration branch. Cross-cutting tooling changes (for example
`check_audio_quality.py`) may land on the current book branch and be merged.

---

## Editing rules

1. **Surgical diffs only.** Never rewrite a working file from scratch unless
   asked. Change the lines that are wrong.
2. **Trace-driven debugging.** Fix what the failing test, exception, or
   measurement actually points at — not what looks suspicious nearby.
3. **Measure before concluding.** This project has a long history of audio
   problems that are invisible in the container metadata and obvious in a
   spectral or silence measurement. Numbers in commit messages and analysis
   documents should be reproducible; include the command.
4. **Deliverables are large binaries.** `final_audio*/` runs to gigabytes per
   title. Do not regenerate a full book to test a change — build one chapter.
