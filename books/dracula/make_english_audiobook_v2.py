"""
Dracula - English audiobook, Kokoro v2.

Same engine as make_english_audiobook.py (which this imports for synthesis,
casting, normalization and trimming), plus every pipeline fix worked out during
the Zonos evaluation. Engine choice, measured on this machine:

    Kokoro     29.6x realtime   0.6 h for the book   <- this
    Zonos       0.8x realtime    20 h                shelved: too slow
    Qwen 0.6B   0.28x realtime   66 h                shelved: too slow
    Qwen 1.7B   0.28x realtime   67 h                shelved: too slow

Kokoro is 33x faster than its nearest rival because it is an 82M
non-autoregressive model rather than a 0.6-1.6B autoregressive one. That gap
is architectural and will not close.

What this adds over the rejected build:

  * MERGED UNITS -- sentences are combined into ~120-220 char units. Short
    fragments read slowly and awkwardly on their own, which is what made
    'Chapter 1' and the journal headings sound wrong.
  * CARRIER SYNTHESIS -- a unit too short to merge (the chapter heading, whose
    voice differs from the line after it) is rendered with a throwaway trailing
    sentence for context, then cut at the sentence gap.
  * VARIABLE PAUSES -- pause length varies by syntactic weight instead of two
    constants, which put 39% of all pauses in a single 100 ms bucket.
  * SQUEEZE -- caps over-long internal pauses with a soft knee. A hard cap
    manufactures the same quantization it was meant to remove.
  * TRIM AT -40 dB -- matches what the QC gate measures, so residual room tone
    cannot stack onto inserted pauses.
  * CLARITY EQ -- cuts low-mid mud and lifts presence, improving the
    presence-to-mud ratio by 2.6 dB. There is no high-shelf 'air' lift: the
    source is 24 kHz, so above ~12 kHz there is only hiss to amplify.

Usage:
  venv/Scripts/python.exe books/dracula/make_english_audiobook_v2.py 1
  venv/Scripts/python.exe books/dracula/make_english_audiobook_v2.py all
"""
import os
import re
import sys
import json
import time
import zlib
import shutil
import subprocess
import traceback

import numpy as np
import soundfile as sf

import make_english_audiobook as mk

DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(DIR, "scripts")
OUT = os.path.join(DIR, "final_audio_en_v2")
TMP = os.path.join(DIR, "temp_audio_en_v2")
os.makedirs(OUT, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

SR = mk.SR                 # Kokoro renders 24 kHz; delivery is 44.1 kHz
BITRATE = "192k"

# ---- cast: two voices for the whole book -----------------------------------
# Chosen by ear on a real Seward diary passage, 2026-09-15.
#
# The seven-voice cast was replaced because four of its voices were weak and
# one of them carried the book. Measured share of the 919,806 characters:
#
#     Dr Seward        41.1%   was bm_lewis  <- judged the blurry one
#     Jonathan Harker  26.6%   was bm_george
#     Mina             23.4%   was bf_emma
#     Lucy              4.1%   was bf_alice
#     Van Helsing       3.6%   was am_fenrir
#     Narrator          1.0%   was bm_fable
#     Holmwood/Morris   0.2%   was bm_daniel
#
# Note the narrator is 1% -- the voice a listener actually hears is Seward's.
# Two voices split the book 73/27 along gender, every speaker change is
# announced by its heading, and both were picked by listening rather than by
# the upstream grades (see CLAUDE.md on why those are not trustworthy).
NARRATOR_VOICE = "bm_fable"        # all male roles + narration + cuttings
FEMALE_VOICE = "af_bella"          # Mina and Lucy

# The male roles need EXPLICIT entries even though they all use the narrator
# voice: voice_for() returns the CURRENT voice when no pattern matches, so with
# female entries alone a "Dr Seward's Diary" heading after a Mina letter kept
# her voice. That produced a 52/48 split instead of the expected 73/27.
# Female patterns come first so "Mina Harker" cannot be caught by "harker".
CAST = [
    (r"mina (murray|harker)", FEMALE_VOICE),
    (r"lucy westenra", FEMALE_VOICE),
    (r"jonathan harker", NARRATOR_VOICE),
    (r"seward", NARRATOR_VOICE),
    (r"van helsing", NARRATOR_VOICE),
    (r"(arthur holmwood|quincey morris|godalming)", NARRATOR_VOICE),
]

# voice_for() reads these from the engine module, so install them there.
mk.NARRATOR_VOICE = NARRATOR_VOICE
mk.CAST = CAST

# Kokoro's only prosody control, and it is global -- mk.synth() reads mk.SPEED.
#
# 0.82 was tuned for the old seven-voice cast. bm_fable reads intrinsically
# faster than the voices it replaced (40.1s vs bm_lewis's 48.5s on the same
# passage), so at 73% of the book it pulled chapter 1 from 40.5 min down to
# 32.0 min and the read came across rushed. Slowed to land near the 158 wpm
# audiobook standard; "speaking too quickly" is on the Authors Republic list.
SPEED = 0.79
mk.SPEED = SPEED

TRIM_DB = -40.0            # match the QC gate's silence threshold
TRIM_KEEP_MS = 30

MERGE_MIN = 120            # keep absorbing sentences until a unit reaches this
MERGE_MAX = 220            # never build a unit longer than this
MERGE_UNDER = 32           # a unit still shorter than this gets a carrier
CARRIER = "And so the record begins."

# Cuts low-mid mud that masks consonants, lifts the 2-5 kHz presence band where
# intelligibility lives. Measured +2.6 dB presence-to-mud on a test passage.
CLARITY_EQ = ("highpass=f=75,"
              "equalizer=f=250:width_type=q:w=1.2:g=-2.5,"
              "equalizer=f=3000:width_type=q:w=1.0:g=+2.5")


# ---- pause policy ----------------------------------------------------------
def pause_ms(sent, is_para_end=False, next_text=""):
    """Pause length by syntactic weight, with deterministic jitter.

    Two fixed constants put 422 of 1088 pauses into one 100 ms bucket, which a
    QA listener hears as mechanical. Jitter alone cannot fix that: +/-15% of a
    single 260 ms constant never leaves its bucket. The bases have to differ.
    """
    s = sent.rstrip()
    if is_para_end:
        base = 750
        head = next_text.strip()[:90]
        if head and len(head) < 90 and mk.ATTRIB.search(head):
            base = 1250                      # scene change, not a paragraph break
    else:
        if s.endswith("?") or s.endswith("!"):
            base = 430
        elif s.endswith(","):
            base = 190
        elif s.endswith(";") or s.endswith(":"):
            base = 240
        else:
            base = 300
        if len(s) < 40:
            base -= 50
        elif len(s) > 160:
            base += 70

    h = (zlib.crc32(s.encode("utf-8")) >> 16) % 51
    return int(base * (1.0 + (h - 25) / 100.0))     # +/-25%


def squeeze(y, max_ms=450, thresh_db=TRIM_DB, knee=0.45):
    """Cap silences inside a clip, with a soft knee.

    trim() only strips head and tail, so it cannot reach a mid-sentence pause.
    A HARD cap is wrong: it put 45% of pauses into one bucket, manufacturing
    the mechanical regularity the pause policy exists to avoid. The knee pulls
    long pauses in while keeping their spread.

    The CAP ITSELF is also jittered. With one fixed cap value, every pause that
    exceeded it landed just above the same number -- 382 of 999 pauses piled
    into the 0.4-0.5s bucket with a cliff immediately after. Varying the cap
    per pause spreads that pile across neighbouring buckets. Jitter is derived
    from the run's position so a rerun is byte-identical.
    """
    if y is None or y.size == 0:
        return y
    win = int(SR * 0.010)
    n = y.size // win
    if n == 0:
        return y
    frames = y[:n * win].reshape(n, win).astype(np.float32)
    db = 20.0 * np.log10(np.sqrt((frames ** 2).mean(axis=1)) + 1e-12)
    silent = db <= thresh_db

    keep = np.ones(n, dtype=bool)
    i = 0
    while i < n:
        if not silent[i]:
            i += 1
            continue
        j = i
        while j < n and silent[j]:
            j += 1
        run = j - i
        # cap jittered +/-25% per pause, so compressed pauses do not all land
        # on the same value
        jit = 1.0 + (((i * 2654435761) >> 8) % 51 - 25) / 100.0
        maxw = max(1, int(max_ms * jit / 10))
        if run > maxw:
            keep[i + int(maxw + (run - maxw) * knee):j] = False
        i = j
    return np.concatenate([frames[keep].reshape(-1), y[n * win:]])


# ---- unit building ---------------------------------------------------------
def build_units(items):
    """Flatten a chapter into synthesis units.

    Short fragments read slowly and awkwardly alone -- the reason 'Chapter 1'
    and the journal headings sounded wrong. Sentences merge within a paragraph;
    merging ACROSS a paragraph happens only when a unit is still too short and
    the cast voice is unchanged, because the journal heading switches voice and
    that boundary must survive.
    """
    units = []
    voice = mk.NARRATOR_VOICE

    for idx, item in enumerate(items):
        raw = item["text"].strip()
        if not raw:
            continue
        voice = mk.voice_for(raw, voice)
        text = mk.normalize(raw)
        if not re.search(r"[A-Za-z0-9]", text):
            continue

        nxt = items[idx + 1]["text"] if idx + 1 < len(items) else ""
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]

        cur = None
        for j, sent in enumerate(sentences):
            last = (j == len(sentences) - 1)
            gap = (pause_ms(text, is_para_end=True, next_text=nxt) if last
                   else pause_ms(sent))
            if cur is None:
                cur = {"voice": voice, "text": sent, "pause": gap}
            elif (len(cur["text"]) < MERGE_MIN
                  and len(cur["text"]) + 1 + len(sent) <= MERGE_MAX):
                cur["text"] += " " + sent
                cur["pause"] = gap
            else:
                units.append(cur)
                cur = {"voice": voice, "text": sent, "pause": gap}
        if cur is not None:
            units.append(cur)

    merged = []
    for u in units:
        if (merged and len(merged[-1]["text"]) < MERGE_UNDER
                and merged[-1]["voice"] == u["voice"]
                and len(merged[-1]["text"]) + 1 + len(u["text"]) <= MERGE_MAX):
            merged[-1]["text"] += " " + u["text"]
            merged[-1]["pause"] = u["pause"]
        else:
            merged.append(u)
    return merged


def synth_carrier(text, voice):
    """Render a too-short unit with a throwaway tail, then cut the tail.

    'Chapter 1' is narrator-voiced and the line after it switches to Harker, so
    it has nowhere to merge. The carrier gives it context; only the heading
    ships.
    """
    body = text.rstrip()
    if not body.endswith((".", "!", "?")):
        body += "."
    y = mk.synth(body + " " + CARRIER, voice)
    if y is None or y.size == 0:
        return y

    win = int(SR * 0.010)
    n = y.size // win
    if n == 0:
        return y
    frames = y[:n * win].reshape(n, win).astype(np.float32)
    db = 20.0 * np.log10(np.sqrt((frames ** 2).mean(axis=1)) + 1e-12)
    silent = db <= TRIM_DB

    cuts, i = [], 0
    while i < n:
        if silent[i]:
            j = i
            while j < n and silent[j]:
                j += 1
            if (j - i) * win >= int(SR * 0.18):
                cuts.append(((i + j) // 2) * win)
            i = j
        else:
            i += 1

    est = int(y.size * len(body) / float(len(body) + 1 + len(CARRIER)))
    if not cuts:
        return y
    cut = min(cuts, key=lambda p: abs(p - est))
    if not (0.4 * est <= cut <= 2.0 * est):
        return y
    return y[:cut]


# ---- mastering -------------------------------------------------------------
def master(parts, out_mp3, target_i="-20", pad="2000|2000", tail="2"):
    """Concatenate -> lossless WAV master -> exactly one mp3 encode."""
    y = np.concatenate(parts) if parts else np.zeros(1, dtype=np.float32)
    peak = float(np.max(np.abs(y))) if y.size else 0.0
    if peak > 0.999:
        y = y * (0.999 / peak)
    wav = os.path.join(TMP, "_master.wav")
    sf.write(wav, y, SR, subtype="PCM_16")
    subprocess.run([
        "ffmpeg", "-y", "-v", "error", "-i", wav,
        "-af", f"{CLARITY_EQ},"
               f"loudnorm=I={target_i}:TP=-3.5:LRA=7,"
               f"adelay={pad},apad=pad_dur={tail}",
        "-ar", "44100", "-ac", "1", "-b:a", BITRATE, out_mp3,
    ], check=True)
    return y.size / float(SR)


# ---- build -----------------------------------------------------------------
def build_chapter(n):
    src = os.path.join(SCRIPTS, f"bilingual_ch_{n:02d}.json")
    if not os.path.exists(src):
        print(f"[skip] no script for chapter {n}")
        return False

    items = [i for i in json.load(open(src, encoding="utf-8"))
             if i.get("lang") == "en"]
    out_mp3 = os.path.join(OUT, f"dracula_ch_{n:02d}_en.mp3")

    units = build_units(items)
    lens = [len(u["text"]) for u in units]
    short = sum(1 for l in lens if l < MERGE_UNDER)
    print(f"  ch{n:02d}: {len(units)} units from {len(items)} paragraphs "
          f"(median {sorted(lens)[len(lens)//2]} chars, {short} carrier)",
          flush=True)

    parts = []
    t0 = time.time()
    for k, u in enumerate(units):
        raw = (synth_carrier(u["text"], u["voice"])
               if len(u["text"]) < MERGE_UNDER
               else mk.synth(u["text"], u["voice"]))
        clip = squeeze(mk.trim(raw, thresh_db=TRIM_DB, keep_ms=TRIM_KEEP_MS))
        if clip is not None and clip.size:
            parts.append(clip)
        parts.append(mk.silence(u["pause"]))
        if k and k % 50 == 0:
            print(f"    [{k}/{len(units)}] {time.time()-t0:.0f}s", flush=True)

    if not parts:
        print("[abort] nothing synthesized")
        return False

    secs = master(parts, out_mp3)
    shutil.copyfile(os.path.join(TMP, "_master.wav"),
                    os.path.join(TMP, f"_ch{n:02d}_master.wav"))
    print(f"[done] ch{n:02d} -> {secs/60.0:.1f} min audio in "
          f"{(time.time()-t0)/60:.1f} min", flush=True)
    return True


def build_credits():
    """Opening credits must name ONLY title, author and narrator -- anything
    more is an Authors Republic rejection. Short tracks need a higher loudness
    target and minimal padding or silence drags their RMS below the -23 floor.
    """
    opening = f"{mk.TITLE}. Written by {mk.AUTHOR}. Narrated by {mk.NARRATOR}."
    closing = f"This has been {mk.TITLE}, by {mk.AUTHOR}. The end."

    for name, text in (("opening_credits", opening), ("closing_credits", closing)):
        clip = squeeze(mk.trim(mk.synth(mk.normalize(text), mk.NARRATOR_VOICE),
                               thresh_db=TRIM_DB, keep_ms=TRIM_KEEP_MS))
        if clip is None or clip.size == 0:
            print(f"[warn] could not synthesize {name}")
            continue
        # -13, not -16: AR requires RMS in [-23, -18] and a short track's
        # mandated lead/trail padding drags the average down. At -16 the
        # opening credits landed on exactly -23.0 -- inside the window with
        # zero margin, which AR's own spec warns against for short tracks.
        master([clip], os.path.join(OUT, f"{name}.mp3"),
               target_i="-13", pad="1200|1200", tail="1.2")
        print(f"[done] {name}", flush=True)

    # Retail sample from the WAV master: one encode, not two.
    wav = os.path.join(TMP, "_ch01_master.wav")
    if os.path.exists(wav):
        subprocess.run([
            "ffmpeg", "-y", "-v", "error", "-ss", "30", "-t", "180", "-i", wav,
            "-af", f"{CLARITY_EQ},"
                   "loudnorm=I=-20:TP=-3.5:LRA=7,adelay=1500|1500,apad=pad_dur=1.5",
            "-ar", "44100", "-ac", "1", "-b:a", BITRATE,
            os.path.join(OUT, "dracula_retail_sample.mp3"),
        ], check=True)
        print("[done] retail sample", flush=True)
    else:
        print("[warn] no chapter 1 master; skipping retail sample")


def build_all(first=1, last=27):
    t0 = time.time()
    built, failed = 0, []
    for n in range(first, last + 1):
        try:
            if build_chapter(n):
                built += 1
        except Exception:
            failed.append(n)
            traceback.print_exc()
    build_credits()
    print(f"[ALL DONE] {built} chapters in {(time.time()-t0)/60:.1f} min",
          flush=True)
    if failed:
        print(f"[ALL DONE] FAILED: {failed}", flush=True)
    return not failed


if __name__ == "__main__":
    arg = (sys.argv[1] if len(sys.argv) > 1 else "").lower()
    if arg == "all":
        build_all()
    elif arg == "credits":
        build_credits()
    elif arg.isdigit():
        build_chapter(int(arg))
    else:
        print(__doc__)
