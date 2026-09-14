"""
Dracula - English-only audiobook generator (Kokoro, local, free).

Addresses the defects behind the Authors Republic narration rejection:
  * speed 0.82  -> ~158 wpm (was 193 wpm: "speaking too quickly")
  * multi-voice casting by epistolary narrator (was one flat voice: "monotonous")
  * sentence-level synthesis + trimmed padding (was 21% dead air)
  * WAV master -> exactly ONE mp3 encode (was double-encoded)
  * text normalization for abbreviations, dates, stray hyphens
  * pronunciation lexicon for proper nouns Kokoro mishandles

Usage:
  python make_english_audiobook.py 1         # one chapter (start here)
  python make_english_audiobook.py all       # every chapter, then credits
  python make_english_audiobook.py credits   # opening + closing + retail sample
"""
import os
import re
import sys
import json
import subprocess

import numpy as np
import soundfile as sf

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(DIR, "scripts")
OUT = os.path.join(DIR, "final_audio_en")
TMP = os.path.join(DIR, "temp_audio_en")
os.makedirs(OUT, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

SR = 24000
SPEED = 0.82          # ~158 wpm, audiobook standard
BITRATE = "192k"      # CBR; must be identical across every track
TITLE = "Dracula"
AUTHOR = "Bram Stoker"
NARRATOR = "Aiden AI"   # must match cover art + metadata EXACTLY

# ---- casting: Dracula is epistolary, each narrator gets their own voice -----
NARRATOR_VOICE = "bm_fable"     # neutral narrator / newspaper cuttings
CAST = [
    (r"jonathan harker", "bm_george"),
    (r"mina (murray|harker)", "bf_emma"),
    (r"lucy westenra", "bf_alice"),
    (r"seward", "bm_lewis"),
    (r"van helsing", "am_fenrir"),
    (r"(arthur holmwood|quincey morris|godalming)", "bm_daniel"),
]
ATTRIB = re.compile(
    r"(journal|diary|letter|telegram|note|memorandum|log|phonograph)", re.I
)

# ---- text normalization ----------------------------------------------------
NORM = [
    (r"\s+-\s+", ", "),            # stray hyphen -> real pause
    (r"[—–]", ", "),     # em/en dash -> pause
    (r"\bMr\.", "Mister"),
    (r"\bMrs\.", "Missus"),
    (r"\bDr\.", "Doctor"),
    (r"\bSt\.", "Saint"),
    (r"\bNo\.\s*(\d)", r"Number \1"),
    (r"\b(\d{1,2}):(\d{2})\s*PM\b", r"\1 \2 in the evening"),
    (r"\b(\d{1,2}):(\d{2})\s*AM\b", r"\1 \2 in the morning"),
    (r"\b(\d{1,2})\s*PM\b", r"\1 in the evening"),   # bare hour: "5 PM"
    (r"\b(\d{1,2})\s*AM\b", r"\1 in the morning"),
    (r"\bP\.?M\.?\b", "P M"),
    (r"\bA\.?M\.?\b", "A M"),
    (r"\.{3,}", ", "),
    (r"\s{2,}", " "),
]

# proper nouns Kokoro's g2p mishandles
LEX = [
    (r"\bBistritz\b", "Bistritsa"),
    (r"\bSzgany\b", "Zgany"),
    (r"\bSzekely(s)?\b", r"Sekely\1"),
    (r"\bVámbéry\b", "Vambery"),
    (r"\bGalatz\b", "Galats"),
    (r"\bNosferatu\b", "Nos fer ah too"),
]


# misaki's g2p spells unknown ALL-CAPS tokens out letter by letter, so
# "DR. SEWARD'S DIARY" is read as "Doctor S-E-W-A-R-D-S Diary". Genuine
# initialisms must survive; everything else gets folded to title case.
KEEP_CAPS = {"PM", "AM", "MP", "US", "UK", "BC", "AD", "OK", "AI"}
CAPS_TOKEN = re.compile(r"\b[A-Z]{2,}(?:['’][A-Z]+)?\b")
CHAPTER_ROMAN = re.compile(r"\b(CHAPTER|Chapter)\s+([MDCLXVI]{1,8})\b")
_ROMAN = {"M": 1000, "D": 500, "C": 100, "L": 50, "X": 10, "V": 5, "I": 1}


def roman_to_int(s):
    total, prev = 0, 0
    for ch in reversed(s.upper()):
        v = _ROMAN.get(ch, 0)
        total = total - v if v < prev else total + v
        prev = max(prev, v)
    return total


def decaps(text):
    # roman chapter numbers read as letters ("CHAPTER XVI" -> "ex-vee-eye")
    text = CHAPTER_ROMAN.sub(
        lambda m: f"Chapter {roman_to_int(m.group(2))}", text
    )

    def fold(m):
        w = m.group(0)
        core = re.split(r"['’]", w)[0]
        if core in KEEP_CAPS:
            return w
        return w[0] + w[1:].lower()      # HARKER'S -> Harker's

    return CAPS_TOKEN.sub(fold, text)


def normalize(text):
    text = decaps(text)                  # must precede NORM so "DR." -> "Dr."
    for pat, rep in NORM + LEX:
        text = re.sub(pat, rep, text)
    return text.strip()


_pipe = None


def pipe():
    global _pipe
    if _pipe is None:
        print("[init] loading Kokoro...")
        from kokoro import KPipeline   # lazy: lets other engines reuse this module
        _pipe = KPipeline(lang_code="a")
    return _pipe


def synth(text, voice):
    """Return raw float32 audio. Stays in numpy: no wav round-trip, no ffmpeg."""
    segs = []
    for _, _, a in pipe()(text, voice=voice, speed=SPEED):
        if a is None:
            continue
        a = a.detach().cpu().numpy() if hasattr(a, "detach") else np.asarray(a)
        if a.size:
            segs.append(a.astype(np.float32, copy=False))
    if not segs:
        return None
    return np.concatenate(segs)


def trim(y, thresh_db=-45.0, keep_ms=40):
    """Strip the engine's own head/tail silence so pauses cannot stack."""
    if y is None or y.size == 0:
        return np.zeros(0, dtype=np.float32)
    win = int(SR * 0.010)
    n = y.size // win
    if n == 0:
        return y
    frames = y[:n * win].reshape(n, win).astype(np.float32)
    db = 20.0 * np.log10(np.sqrt((frames ** 2).mean(axis=1)) + 1e-12)
    voiced = np.flatnonzero(db > thresh_db)
    if voiced.size == 0:
        return np.zeros(0, dtype=np.float32)
    keep = int(SR * keep_ms / 1000.0)
    a = max(0, voiced[0] * win - keep)
    b = min(y.size, (voiced[-1] + 1) * win + keep)
    return y[a:b]


def silence(ms):
    return np.zeros(int(SR * ms / 1000.0), dtype=np.float32)


def voice_for(text, current):
    """Switch voice when an epistolary attribution header appears."""
    if len(text) < 90 and ATTRIB.search(text):
        low = text.lower()
        m = re.search(r"letter from ([^,.]+?) to ", low)
        probe = m.group(1) if m else low
        for pat, v in CAST:
            if re.search(pat, probe):
                return v
        for pat, v in CAST:
            if re.search(pat, low):
                return v
    return current


def master(parts, out_mp3, target_i="-20", pad="2000|2000", tail="2"):
    """One concatenate -> lossless WAV master -> exactly one mp3 encode."""
    y = np.concatenate(parts) if parts else np.zeros(1, dtype=np.float32)
    peak = float(np.max(np.abs(y))) if y.size else 0.0
    if peak > 0.999:                       # guard the encoder against clipping
        y = y * (0.999 / peak)
    wav = os.path.join(TMP, "_master.wav")
    sf.write(wav, y, SR, subtype="PCM_16")
    subprocess.run([
        "ffmpeg", "-y", "-v", "error", "-i", wav,
        "-af", f"loudnorm=I={target_i}:TP=-3.5:LRA=7,"
               f"adelay={pad},apad=pad_dur={tail}",
        "-ar", "44100", "-ac", "1", "-b:a", BITRATE, out_mp3,
    ], check=True)
    return y.size / float(SR)


def build_chapter(n):
    src = os.path.join(SCRIPTS, f"bilingual_ch_{n:02d}.json")
    if not os.path.exists(src):
        print(f"[skip] no script for chapter {n}")
        return False

    items = [i for i in json.load(open(src, encoding="utf-8"))
             if i.get("lang") == "en"]
    out_mp3 = os.path.join(OUT, f"dracula_ch_{n:02d}_en.mp3")

    parts = []
    voice = NARRATOR_VOICE
    sent_pause, para_pause = silence(260), silence(600)

    for idx, item in enumerate(items):
        raw = item["text"].strip()
        if not raw:
            continue
        voice = voice_for(raw, voice)
        text = normalize(raw)
        if not re.search(r"[A-Za-z0-9]", text):
            continue

        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
        for j, sent in enumerate(sentences):
            clip = trim(synth(sent, voice))
            if clip.size == 0:
                continue
            parts.append(clip)
            if j < len(sentences) - 1:
                parts.append(sent_pause)
        parts.append(para_pause)

        if idx % 25 == 0:
            print(f"  ch{n:02d} [{idx}/{len(items)}] voice={voice}", flush=True)

    secs = master(parts, out_mp3)
    print(f"[done] ch{n:02d} -> {out_mp3}  ({secs / 60.0:.1f} min)", flush=True)
    return True


def build_credits():
    opening = f"{TITLE}. Written by {AUTHOR}. Narrated by {NARRATOR}."
    closing = f"This has been {TITLE}, by {AUTHOR}. The end."

    for name, text in (("opening_credits", opening), ("closing_credits", closing)):
        clip = trim(synth(text, NARRATOR_VOICE))
        if clip.size == 0:
            print(f"[warn] could not synthesize {name}")
            continue
        # short tracks: boost target and pad minimally or RMS fails the -23 dB floor
        master([clip], os.path.join(OUT, f"{name}.mp3"),
               target_i="-16", pad="1200|1200", tail="1.2")
        print(f"[done] {name}.mp3", flush=True)

    # retail sample: 3 minutes of real narration, per Authors Republic
    ch1 = os.path.join(OUT, "dracula_ch_01_en.mp3")
    if os.path.exists(ch1):
        subprocess.run([
            "ffmpeg", "-y", "-v", "error", "-ss", "5", "-t", "180", "-i", ch1,
            "-af", "loudnorm=I=-20:TP=-3.5:LRA=7,adelay=1500|1500,apad=pad_dur=1.5",
            "-ar", "44100", "-ac", "1", "-b:a", BITRATE,
            os.path.join(OUT, "dracula_retail_sample.mp3"),
        ], check=True)
        print("[done] dracula_retail_sample.mp3")
    else:
        print("[warn] chapter 1 not built yet; skipping retail sample")


if __name__ == "__main__":
    arg = (sys.argv[1] if len(sys.argv) > 1 else "").lower()
    if arg == "all":
        for n in range(1, 28):
            build_chapter(n)
        build_credits()
    elif arg == "credits":
        build_credits()
    elif arg.isdigit():
        build_chapter(int(arg))
    else:
        print(__doc__)
