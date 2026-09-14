"""
Dracula - English audiobook, Azure Neural TTS trial (chapter 1 + retail sample).

Why this exists: the Kokoro build (make_english_audiobook.py) fixed every pipeline
defect from NARRATION_REJECTION_ANALYSIS.md 5.3 and was still rejected on
2026-09-14 for "monotonous or robotic voice". Kokoro cannot fix that -- it renders
at 24 kHz and exposes `speed` as its only prosody control. This swaps the engine
and nothing else:

  * 48 kHz native source     -> real bandwidth, not upsampled 24 kHz
  * SSML <prosody> per sentence, varied by sentence content -> intonation
  * retail sample cut from the WAV master, not from the finished mp3 (one encode)

Everything else -- text normalization, the proper-noun lexicon, ALL-CAPS folding,
epistolary voice casting, silence trimming, the AR-compliant master chain -- is
imported from make_english_audiobook.py so the two builds differ ONLY by engine.

Output goes to final_audio_en_azure/ so the Kokoro build stays intact for A/B.

Credentials (never hardcode):
  export AZURE_SPEECH_KEY=...
  export AZURE_SPEECH_REGION=eastus

Usage:
  python make_english_audiobook_azure.py voices    # 40s casting demo, ~1k chars
  python make_english_audiobook_azure.py 1         # chapter 1 + retail sample
  python make_english_audiobook_azure.py verify    # measure vs the Kokoro build
"""
import io
import os
import re
import sys
import json
import time
import zlib
import shutil
import subprocess

import numpy as np
import soundfile as sf

# imported first: it installs the win32 utf-8 stdout wrapper. Wrapping here too
# would re-wrap an already-wrapped buffer and close it on exit.
import make_english_audiobook as mk

# 48 kHz end to end. mk.trim/mk.silence/mk.master all read this module global,
# so overriding it here keeps the whole imported chain consistent.
SR = 48000
mk.SR = SR

DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(DIR, "scripts")
OUT = os.path.join(DIR, "final_audio_en_azure")
TMP = os.path.join(DIR, "temp_audio_en_azure")
os.makedirs(OUT, exist_ok=True)
os.makedirs(TMP, exist_ok=True)
mk.TMP = TMP

KEY = os.environ.get("AZURE_SPEECH_KEY", "").strip()
REGION = os.environ.get("AZURE_SPEECH_REGION", "eastus").strip()

# Kokoro voice id -> Azure voice. Keeps mk.voice_for() usable unchanged.
# en-GB throughout: Dracula is a British epistolary novel.
VOICE_MAP = {
    "bm_fable":  "en-GB-RyanNeural",     # narrator / newspaper cuttings
    "bm_george": "en-GB-ThomasNeural",   # Jonathan Harker
    "bf_emma":   "en-GB-SoniaNeural",    # Mina
    "bf_alice":  "en-GB-MaisieNeural",   # Lucy (younger)
    "bm_lewis":  "en-GB-OliverNeural",   # Dr Seward
    "am_fenrir": "en-GB-NoahNeural",     # Van Helsing
    "bm_daniel": "en-GB-ElliotNeural",   # Holmwood / Morris
}

BASE_RATE = -8      # percent; Azure neural default runs ~180 wpm, this lands ~160
BITRATE = "192k"    # must match the rest of the title exactly


# ---- prosody ---------------------------------------------------------------
def prosody_for(sent):
    """Per-sentence rate/pitch from sentence content.

    A fixed rate for 34 hours is exactly what 'monotonous' describes, so every
    sentence gets its own setting. The jitter is hash-derived, not random, so
    reruns are byte-identical -- it exists to stop consecutive sentences landing
    on the same numbers, which is what makes a read sound machine-regular.
    """
    rate, pitch = BASE_RATE, 0
    s = sent.strip()

    if s.endswith("?"):
        pitch += 5
        rate -= 3
    elif s.endswith("!"):
        pitch += 7
        rate += 2

    if len(s) > 160:            # long descriptive sentence: give it room
        rate -= 3
    elif len(s) < 40:           # short and punchy
        rate += 2

    if '"' in s or "“" in s:   # quoted speech lifts out of narration
        pitch += 2

    h = zlib.crc32(s.encode("utf-8"))
    rate += (h % 5) - 2             # +/-2%
    pitch += ((h >> 8) % 5) - 2     # +/-2%
    return rate, pitch


def pause_ms(sent, is_para_end=False, next_text=""):
    """Variable pause length.

    Fixed constants are why the Kokoro build's pause histogram has two sharp
    spikes (422 gaps at 0.3-0.4s, 100 at 0.6-0.7s) instead of the smooth tail a
    human read produces. Same hash-jitter trick as prosody_for: deterministic,
    so a rerun is byte-identical.
    """
    s = sent.rstrip()
    if is_para_end:
        base = 750
        head = next_text.strip()[:90]
        # a new journal/letter heading is a scene change, not a paragraph break
        if head and len(head) < 90 and mk.ATTRIB.search(head):
            base = 1250
    else:
        # bases are spread by syntactic weight. Jitter alone cannot do this:
        # +/-15% of one 260ms constant stays inside a single 100ms bucket, which
        # concentrates the histogram instead of spreading it.
        if s.endswith("?") or s.endswith("!"):
            base = 430          # let the beat land
        elif s.endswith(","):
            base = 190          # mid-clause, keep it moving
        elif s.endswith(";") or s.endswith(":"):
            base = 240
        else:
            base = 300
        if len(s) < 40:
            base -= 50          # short lines in quick succession
        elif len(s) > 160:
            base += 70          # breath after a long one

    h = (zlib.crc32(s.encode("utf-8")) >> 16) % 51
    return int(base * (1.0 + (h - 25) / 100.0))     # +/-25%


def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def ssml_for(sent, azure_voice):
    rate, pitch = prosody_for(sent)
    return (
        '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" '
        'xml:lang="en-GB">'
        f'<voice name="{azure_voice}">'
        f'<prosody rate="{rate:+d}%" pitch="{pitch:+d}%">{esc(sent)}</prosody>'
        "</voice></speak>"
    )


# ---- engine ----------------------------------------------------------------
_synth = None


def synthesizer():
    global _synth
    if _synth is None:
        import azure.cognitiveservices.speech as speechsdk
        if not KEY:
            sys.exit(
                "\nAZURE_SPEECH_KEY is not set.\n"
                "  1. portal.azure.com -> Create resource -> Speech\n"
                "  2. Pricing tier F0 (free, 500K chars/month)\n"
                "  3. Keys and Endpoint -> copy KEY 1 and Location\n\n"
                "  export AZURE_SPEECH_KEY=<key>\n"
                "  export AZURE_SPEECH_REGION=<location, e.g. eastus>\n"
            )
        cfg = speechsdk.SpeechConfig(subscription=KEY, region=REGION)
        cfg.set_speech_synthesis_output_format(
            speechsdk.SpeechSynthesisOutputFormat.Riff48Khz16BitMonoPcm
        )
        _synth = speechsdk.SpeechSynthesizer(speech_config=cfg, audio_config=None)
        print(f"[init] Azure Speech, region={REGION}, 48 kHz PCM")
    return _synth


def synth(sent, kokoro_voice, retries=3):
    """One sentence -> float32 @ 48 kHz. Mirrors mk.synth()'s contract."""
    import azure.cognitiveservices.speech as speechsdk

    voice = VOICE_MAP.get(kokoro_voice, VOICE_MAP["bm_fable"])
    ssml = ssml_for(sent, voice)

    for attempt in range(retries):
        r = synthesizer().speak_ssml_async(ssml).get()
        if r.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            y, sr = sf.read(io.BytesIO(r.audio_data), dtype="float32")
            if y.ndim > 1:
                y = y.mean(axis=1)
            if sr != SR:
                print(f"[warn] engine returned {sr} Hz, expected {SR}")
            return y
        d = r.cancellation_details
        msg = getattr(d, "error_details", "") or str(getattr(d, "reason", ""))
        if attempt == retries - 1:
            print(f"[fail] {msg[:160]}\n       text: {sent[:70]!r}")
            return None
        time.sleep(1.5 * (attempt + 1))     # throttling / transient network
    return None


# ---- build -----------------------------------------------------------------
def build_chapter(n):
    src = os.path.join(SCRIPTS, f"bilingual_ch_{n:02d}.json")
    if not os.path.exists(src):
        print(f"[skip] no script for chapter {n}")
        return False

    items = [i for i in json.load(open(src, encoding="utf-8"))
             if i.get("lang") == "en"]
    out_mp3 = os.path.join(OUT, f"dracula_ch_{n:02d}_en.mp3")

    parts = []
    voice = mk.NARRATOR_VOICE
    done = failed = 0
    t0 = time.time()

    for idx, item in enumerate(items):
        raw = item["text"].strip()
        if not raw:
            continue
        voice = mk.voice_for(raw, voice)
        text = mk.normalize(raw)
        if not re.search(r"[A-Za-z0-9]", text):
            continue

        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
        for j, sent in enumerate(sentences):
            y = synth(sent, voice)
            if y is None:
                failed += 1
                continue
            clip = mk.trim(y)
            if clip.size == 0:
                continue
            parts.append(clip)
            done += 1
            if j < len(sentences) - 1:
                parts.append(mk.silence(pause_ms(sent)))
        nxt = items[idx + 1]["text"] if idx + 1 < len(items) else ""
        parts.append(mk.silence(pause_ms(text, is_para_end=True, next_text=nxt)))

        if idx % 10 == 0:
            print(f"  ch{n:02d} [{idx}/{len(items)}] voice={voice} "
                  f"sent={done} fail={failed} {time.time()-t0:.0f}s", flush=True)

    if not parts:
        print("[abort] nothing synthesized")
        return False

    secs = mk.master(parts, out_mp3)
    shutil.copyfile(os.path.join(TMP, "_master.wav"),
                    os.path.join(TMP, f"_ch{n:02d}_master.wav"))
    print(f"[done] ch{n:02d} -> {out_mp3}  ({secs/60.0:.1f} min, "
          f"{done} sentences, {failed} failed)", flush=True)
    return True


def build_sample(n=1):
    """Retail sample from the WAV master -- one encode, not two.

    The Kokoro build cut this from the finished mp3, so the one track a reviewer
    is guaranteed to hear was the only double-encoded file in the package.
    """
    wav = os.path.join(TMP, f"_ch{n:02d}_master.wav")
    if not os.path.exists(wav):
        print(f"[warn] no master for chapter {n}; build the chapter first")
        return
    out = os.path.join(OUT, "dracula_retail_sample.mp3")
    subprocess.run([
        "ffmpeg", "-y", "-v", "error", "-ss", "5", "-t", "180", "-i", wav,
        "-af", "loudnorm=I=-20:TP=-3.5:LRA=7,adelay=1500|1500,apad=pad_dur=1.5",
        "-ar", "44100", "-ac", "1", "-b:a", BITRATE, out,
    ], check=True)
    print(f"[done] {out}")


def build_voices():
    """Short casting demo. ~1k characters -- run this first to hear the cast."""
    lines = [
        ("bm_fable",  "Dracula. Written by Bram Stoker. Narrated by Aiden AI."),
        ("bm_george", "3 May. Bistritsa. Left Munich at 8:35 in the evening, "
                      "on the first of May, arriving at Vienna early next morning."),
        ("bf_emma",   "I must keep writing at every chance, for I cannot tell "
                      "when I shall see him again. Is he well? Is he safe?"),
        ("bf_alice",  "Oh, I am so happy! Why are men so noble, and women so "
                      "little worthy of them?"),
        ("bm_lewis",  "Let me record this exactly as it happened. The patient "
                      "is more excitable than usual."),
        ("am_fenrir", "There are mysteries which men can only guess at, which "
                      "age by age they solve only in part!"),
    ]
    parts = []
    for v, text in lines:
        y = synth(mk.normalize(text), v)
        if y is None:
            continue
        parts.append(mk.trim(y))
        parts.append(mk.silence(700))
        print(f"  {VOICE_MAP[v]:<22} {text[:50]}...")
    if parts:
        mk.master(parts, os.path.join(OUT, "_voice_demo.mp3"),
                  target_i="-18", pad="800|800", tail="1")
        print(f"[done] {OUT}/_voice_demo.mp3  -- listen before the full chapter")


# ---- verification (analysis 5.4) -------------------------------------------
def _band_db(path, af):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", af,
                        "-f", "null", "-"], capture_output=True, text=True)
    m = re.search(r"mean_volume:\s*(-?[\d.]+) dB", r.stderr)
    return float(m.group(1)) if m else float("nan")


def _silence_ratio(path):
    dur = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", path], capture_output=True, text=True).stdout.strip())
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af",
                        "silencedetect=noise=-40dB:d=0.15", "-f", "null", "-"],
                       capture_output=True, text=True)
    tot = sum(float(x) for x in re.findall(r"silence_duration:\s*([\d.]+)", r.stderr))
    return dur, 100.0 * tot / dur if dur else 0.0


def verify():
    """The three checks check_audio_quality.py is missing, run as an A/B."""
    targets = [
        ("kokoro", os.path.join(DIR, "final_audio_en", "dracula_ch_01_en.mp3")),
        ("azure",  os.path.join(OUT, "dracula_ch_01_en.mp3")),
    ]
    print(f"{'build':<8}{'dur':>8}{'8-11kHz':>10}{'>13kHz':>9}"
          f"{'headroom':>10}{'silence':>9}   verdict")
    for name, path in targets:
        if not os.path.exists(path):
            print(f"{name:<8}  (not built)")
            continue
        low = _band_db(path, "highpass=f=8000,lowpass=f=11000,volumedetect")
        high = _band_db(path, "highpass=f=13000,highpass=f=13000,volumedetect")
        dur, sil = _silence_ratio(path)
        gap = high - low
        ok = "PASS" if gap > -15 and sil < 12 else "FAIL"
        why = []
        if gap <= -15:
            why.append("upsampled source")
        if sil >= 12:
            why.append("dead air")
        print(f"{name:<8}{dur/60:>7.1f}m{low:>10.1f}{high:>9.1f}"
              f"{gap:>10.1f}{sil:>8.1f}%   {ok} {' '.join(why)}")
    print("\n  headroom = >13kHz minus 8-11kHz. Below -15 dB means the top end is")
    print("  empty: a 24 kHz source upsampled to 44.1, which reads as muffled.")


if __name__ == "__main__":
    arg = (sys.argv[1] if len(sys.argv) > 1 else "").lower()
    if arg == "verify":
        verify()
    elif arg == "voices":
        build_voices()
    elif arg == "sample":
        build_sample(1)
    elif arg.isdigit():
        if build_chapter(int(arg)):
            build_sample(int(arg))
        verify()
    else:
        print(__doc__)
