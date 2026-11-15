"""
Dracula - English audiobook via Zonos-v0.1 (local, free, 44.1 kHz).

Runs inside WSL Ubuntu, where Zonos lives. Imports the existing pipeline from
the Windows checkout so normalization, the proper-noun lexicon, ALL-CAPS
folding, epistolary casting, silence trimming, the variable pause policy and
the AR-compliant master chain are all shared: this differs from the Kokoro and
Azure builds ONLY by engine.

Why Zonos, after Kokoro was rejected 2026-09-14 for "monotonous or robotic
voice": Kokoro renders 24 kHz and exposes `speed` as its only prosody control.
Zonos generates natively at 44.1 kHz and exposes pitch_std (intonation
variation), speaking_rate, fmax and emotion as direct conditioning.

Measured on this machine: clone from a Kokoro-derived reference gives -12.5 dB
bandwidth headroom vs -24.4 for the rejected build (threshold -18).

All I/O stays on ext4. /mnt/c measured 93x slower on small files.

Usage (from /root/Zonos):
  uv run python make_english_audiobook_zonos.py 1
"""
import os
import re
import sys
import json
import time
import zlib
import shutil
import traceback
import subprocess

import numpy as np
import soundfile as sf
import torch
import torchaudio

WIN = "/mnt/c/git_repo/TKprof_book/books/dracula"
if WIN not in sys.path:
    sys.path.insert(0, WIN)

import make_english_audiobook as mk
from make_english_audiobook_azure import pause_ms   # shared pause policy

from zonos.model import Zonos
from zonos.conditioning import make_cond_dict


# --- upstream batching fix -------------------------------------------------
# Zonos.generate() takes a batch_size, but _prefill replicates the audio codes
# for classifier-free guidance with .expand(2N, -1, -1). expand only works on
# singleton dims, so it succeeds at N=1 and raises for every larger batch --
# the parameter is effectively untested upstream. Every other CFG site in
# model.py already uses .repeat(2,1,1), which is batch-correct and matches the
# logits.chunk(2) ordering; this makes _prefill consistent with them.
#
# Patched here rather than in /root/Zonos: that clone is not part of this
# repository, so an edit there would be untracked and lost on any refresh.
def _prefill_batched(self, prefix_hidden_states, input_ids, inference_params,
                     cfg_scale):
    if cfg_scale != 1.0:
        reps = prefix_hidden_states.shape[0] // input_ids.shape[0]
        input_ids = input_ids.repeat(reps, 1, 1)
    hidden_states = torch.cat(
        [prefix_hidden_states, self.embed_codes(input_ids)], dim=1)
    return self._compute_logits(hidden_states, inference_params, cfg_scale)


Zonos._prefill = _prefill_batched

# Measured on an RTX 3080 (10 GB), 16 real units, against sequential:
#   unsorted      batch 4 -> 1.35x, 45.8% of output wasted on padding
#   LENGTH-SORTED batch 4 -> 1.91x, 13.2% waste, 8.8 GB peak
#   LENGTH-SORTED batch 2 -> 1.56x,  4.4% waste, 6.4 GB peak
# A batch runs until its LONGEST member emits EOS, so mixing a 42-char unit
# with a 224-char one pays for the long one twice. Sorting by length first is
# what makes batching worth doing at all.
# WARNING, learned the hard way: batch 4 benchmarked at 1.91x on a 16-unit
# slice and then ran 1.5-2.9x SLOWER than sequential on real chapters, getting
# worse as it went (ch02 65min, ch03 129min, ch04 120min, vs 44min unbatched).
# Cause: the KV cache is allocated for batch_size*2 sequences at the FULL
# max_new_tokens, which saturated the 10 GB card. CUDA never raised OOM -- WSL
# silently spilled into system RAM over PCIe, so the OOM fallback below never
# fired and throughput collapsed instead. A short benchmark slice fit in VRAM;
# a 200-unit chapter does not.
#
# Batch 2 measured 6.4 GB peak (1.56x) against batch 4's 8.8 GB on a 10 GB
# card. Anything that pushes past ~8 GB here is not worth the speedup.
#
# FINAL ANSWER: 1. Batching does not pay on a 10 GB card here. Batch 2 with the
# KV cache already sized down still climbed to 9.3 GB on a real chapter and the
# watchdog dropped it to 1 partway through -- chapter 1 then took 40.8 min for
# 35.6 min of audio, i.e. exactly the sequential baseline. Generation is also
# bounded by the longest unit in each batch, so even when it fits, the win is
# far smaller than a benchmark on a uniform slice suggests.
BATCH_SIZE = 1

SR = 44100
BITRATE = "192k"      # CBR; must be identical across every track in the title
# NOTE: importing make_english_audiobook_azure above sets mk.SR = 48000 as a
# side effect, so this assignment must come AFTER that import. Getting it wrong
# renders an entire chapter at the wrong rate, which sounds like a pitch shift
# and is easy to miss until the whole book is built. The assert makes the
# dependency explicit rather than leaving it to import order.
mk.SR = SR
assert mk.SR == SR == 44100, f"mk.SR is {mk.SR}, expected {SR}"

SCRIPTS = os.path.join(WIN, "scripts")
REFS = "/root/voice_refs"
OUT = "/root/zonos_build"
TMP = "/root/zonos_tmp"
CACHE = "/root/zonos_cache"
for d in (OUT, TMP, CACHE):
    os.makedirs(d, exist_ok=True)
mk.TMP = TMP

# Zonos' own defaults are pitch_std=20 (a flat read) and speaking_rate=15.
# 45 is the expressive setting; it is the direct answer to "monotonous".
BASE_PITCH_STD = 45.0
# 14.0 rendered ch01 in 35.7min vs the Kokoro build's 40.5min on identical
# text -- about 180 wpm against the 158 wpm Kokoro was deliberately tuned to.
# "Speaking too quickly" is on the Authors Republic list, so slow it down.
# ZONOS_RATE overrides it: rate feeds the sentence cache key, so re-running at
# a previous rate replays cached clips and re-masters in seconds instead of
# re-synthesizing the chapter. Useful for isolating pipeline changes from
# engine changes.
BASE_RATE = float(os.environ.get("ZONOS_RATE", "12.5"))
CHARS_PER_SEC = 15.0        # measured at BASE_RATE; used only for sanity checks

# mk.trim() defaults to -45 dB, but silencedetect (and therefore the QC gate)
# calls anything below -40 dB silence. Residue in that 5 dB band survived
# trimming and stacked onto the inserted pause: ch01 had 165 gaps averaging
# 1.09s, longer than the 750ms paragraph pause that is the longest thing the
# pause policy inserts. Trim at the same threshold the gate measures at.
TRIM_DB = -40.0
TRIM_KEEP_MS = 30

# Zonos is autoregressive and needs runway to settle into pitch and pace.
# 'Chapter 1' alone renders in 0.74s and sounds unstable; the same words inside
# a 5.4s utterance do not. 33 of chapter 1's 347 sentences are under 30 chars,
# and the first four utterances of EVERY chapter are short, so this lands on
# the opening seconds of every track a reviewer samples.
# Sentence-level synthesis was inherited from the Kokoro build, where it existed
# to control pauses. squeeze() now caps internal pauses instead, so units can be
# built up to a length that actually sounds good: longer utterances were judged
# better by ear on both headings AND body text.
MERGE_MIN = 120       # keep absorbing sentences until a unit reaches this
MERGE_MAX = 220       # but never build a unit longer than this (~15s)
# Only genuine fragments need the carrier. At 45 this also caught ordinary
# 41-char sentences that render fine on their own, and running them through
# the carrier cut risks truncating real speech for no benefit.
MERGE_UNDER = 32      # a unit still shorter than this gets a carrier
CARRIER = "And so the record begins."


def prosody_for(sent):
    """Per-sentence pitch variation and pace, from sentence content.

    Same policy as the Azure build's SSML prosody, expressed in Zonos'
    conditioning instead: a single fixed setting across 34 hours is what
    'monotonous' describes. Jitter is hash-derived so reruns are identical.
    """
    s = sent.strip()
    pitch = BASE_PITCH_STD

    if s.endswith("?"):
        pitch += 10.0
    elif s.endswith("!"):
        pitch += 15.0
    if '"' in s or "“" in s:
        pitch += 5.0

    h = zlib.crc32(s.encode("utf-8"))
    pitch *= 1.0 + ((h % 21) - 10) / 100.0          # +/-10%

    # PACE IS HELD CONSTANT, deliberately.
    #
    # This used to vary per unit the same way pitch does, which was right when
    # a unit was one sentence -- small pace shifts read as phrasing. After
    # units were merged it applied to whole 10-15s paragraphs instead, giving a
    # 16% spread across the chapter and adjacent-paragraph jumps up to 14.6%.
    # That is heard as the narrator randomly speeding up and slowing down, not
    # as expression. A human narrator holds a steady pace and varies pitch and
    # emphasis, so that is what this does now.
    return round(pitch, 1), BASE_RATE


def squeeze(y, max_ms=450, thresh_db=TRIM_DB, knee=0.25):
    """Cap silences INSIDE a clip.

    mk.trim() only strips head and tail, so it cannot reach a pause in the
    middle of a sentence. Zonos emits plenty: ch01 measured ~100 internal gaps
    over 0.7s, which is what "pausing unnecessarily between words" describes.
    Runs longer than max_ms are compressed toward it with a soft knee, not
    truncated to it. A hard cap put 45% of chapter 1's pauses in a single
    100ms bucket -- it manufactured exactly the mechanical quantization the
    variable pause policy exists to prevent. The knee keeps the ordering and
    spread of long pauses while pulling them in:

        0.7s -> 0.51s    1.2s -> 0.64s    2.0s -> 0.84s

    Shorter runs are left alone so natural comma-level phrasing survives.
    Cuts land inside sub-threshold audio, so they do not click.
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
    maxw = max(1, int(max_ms / 10))

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
        if run > maxw:
            target = int(maxw + (run - maxw) * knee)
            keep[i + target:j] = False
        i = j

    return np.concatenate([frames[keep].reshape(-1), y[n * win:]])


_model = None
_speakers = {}


def model():
    global _model
    if _model is None:
        print("[init] loading Zonos-v0.1-transformer...", flush=True)
        _model = Zonos.from_pretrained("Zyphra/Zonos-v0.1-transformer",
                                       device="cuda")
        print(f"[init] sampling_rate={_model.autoencoder.sampling_rate}",
              flush=True)
    return _model


def speaker(kokoro_voice):
    """Speaker embedding per cast voice, so the voice is stable across calls."""
    if kokoro_voice not in _speakers:
        path = os.path.join(REFS, f"{kokoro_voice}.wav")
        if not os.path.exists(path):
            path = os.path.join(REFS, f"{mk.NARRATOR_VOICE}.wav")
        wav, sr = torchaudio.load(path)
        _speakers[kokoro_voice] = model().make_speaker_embedding(wav, sr)
    return _speakers[kokoro_voice]


def cache_path(sent, voice):
    """Cache key covers text, voice and prosody, so batched and sequential
    generation share the same entries."""
    pitch, rate = prosody_for(sent)
    key = zlib.crc32(f"{voice}|{pitch}|{rate}|{sent}".encode("utf-8"))
    return os.path.join(CACHE, f"{key:08x}.wav")


def cond_for(sent, voice):
    pitch, rate = prosody_for(sent)
    return make_cond_dict(text=sent, speaker=speaker(voice), language="en-us",
                          fmax=22050.0, pitch_std=pitch, speaking_rate=rate)


def has_long_tone(y, min_ms=500, tol_hz=6.0, floor=3e-3):
    """True if the clip holds one pitch unnaturally long -- a hallucinated tone.

    Distinct from the EOS padding that trim_pad_codes() removes: Zonos also
    emits sustained tones in the MIDDLE of an utterance. Chapter 2 carried a
    3.6-second held pitch at 108 Hz that every other check passed.

    These take the pitch of the cloned voice, so at a male 108 Hz they hide
    inside the narration, while at a female 258 Hz they are an obvious beep --
    which is why the Mina and Lucy chapters are where a listener hears them.

    Real speech does not hold a pitch within 6 Hz for half a second.
    """
    win, hop = 2048, 1024
    n = (y.size - win) // hop
    if n < 3:
        return False
    w = np.hanning(win).astype(np.float32)
    need = int(min_ms / 1000.0 * SR / hop)

    run, prev = 0, None
    for i in range(n):
        seg = y[i * hop:i * hop + win] * w
        if np.sqrt(np.dot(seg, seg) / win) <= floor:      # too quiet to matter
            run, prev = 0, None
            continue
        f = int(np.argmax(np.abs(np.fft.rfft(seg)))) * SR / win
        if prev is not None and abs(f - prev) < tol_hz:
            run += 1
            if run >= need:
                return True
        else:
            run = 0
        prev = f
    return False


def trim_pad_codes(c):
    """Cut one sequence's codes at its last non-padding frame.

    generate() zero-fills after EOS -- for a batch, out to the longest member's
    length; even for a single sequence, the final masked frames. Decoding that
    constant run yields a steady TONE, which is above the -40 dB floor and so
    survives trim() and squeeze(). Measured: a short unit batched with a long
    one carried 232 ms of tone before this, 0 ms after.

    Token 0 across ALL nine codebooks simultaneously is the padding signature;
    one codebook hitting 0 during real audio is normal.
    """
    nz = (c != 0).any(dim=0).nonzero()
    last = int(nz[-1]) + 1 if nz.numel() else c.shape[1]
    return c[:, :last]


def _decode(codes):
    w = model().autoencoder.decode(codes).cpu()
    out = []
    for i in range(w.shape[0]):
        a = w[i]
        out.append(a.mean(dim=0).numpy().astype(np.float32) if a.ndim > 1
                   else a.numpy().astype(np.float32))
    return out


def gen_batch(units):
    """Generate several units in one forward pass, writing each to the cache.

    Conditioner.forward does apply_cond(*inputs), so a batched (N,1,X) tensor
    would unpack into N arguments; wrapping it in a 1-tuple makes the unpack
    yield the whole tensor. Only 'espeak' is already list-shaped upstream.
    """
    ds = [cond_for(u["text"], u["voice"]) for u in units]
    cond = {"espeak": ([d["espeak"][0][0] for d in ds],
                       [d["espeak"][1][0] for d in ds])}
    for k in ds[0]:
        if k != "espeak":
            cond[k] = (torch.cat([d[k] for d in ds], dim=0),)

    # Size the KV cache to the actual work. Upstream defaults to 86*30 tokens
    # (30s of audio) regardless of text length, and setup_cache allocates that
    # for batch_size*2 sequences up front -- the single biggest contributor to
    # the VRAM saturation that made batch 4 slower than sequential. Our units
    # run to ~250 chars, well under 20s. The 1.5x margin keeps a slow-spoken
    # unit from being cut off; if one is, the duration check below catches it
    # and it gets regenerated individually.
    # QUANTIZED TO 256-TOKEN BUCKETS, deliberately. Sizing this from the exact
    # text length gave a different allocation on nearly every call, which
    # defeated PyTorch's caching allocator: reserved memory climbed to 20.7 GB
    # on a 10 GB card, throughput halved within each chapter (13.9 -> 5.3
    # units/min), and the Linux OOM killer eventually took the process (exit 4,
    # no traceback). A handful of distinct sizes lets blocks be reused.
    longest = max(len(u["text"]) for u in units)
    want = int(86 * (longest / CHARS_PER_SEC) * 1.5) + 128
    max_tok = min(86 * 30, ((want + 255) // 256) * 256)

    codes = model().generate(model().prepare_conditioning(cond),
                             batch_size=len(units), max_new_tokens=max_tok,
                             progress_bar=False)

    # CRITICAL: generate() truncates the batch to its LONGEST member and
    # zero-fills every sequence that finished earlier. Decoding that constant
    # token run produces a steady TONE, not silence -- so it sits well above
    # the -40 dB floor and survives both trim() and squeeze(). Chapter 4 was
    # rendered without this and came out 14.3% steady tones (vs 7.6% for a
    # sequential chapter), audible as beeps and lurching pace.
    #
    # Cut each sequence at its own last non-padding frame. Token 0 across ALL
    # nine codebooks at once is the padding signature; a single codebook
    # hitting 0 during real audio is normal.
    audio = []
    for i in range(codes.shape[0]):
        audio.extend(_decode(trim_pad_codes(codes[i]).unsqueeze(0)))

    bad = []
    for u, y in zip(units, audio):
        expect = max(0.6, len(u["text"]) / CHARS_PER_SEC)
        dur = y.size / SR
        if not (0.4 * expect <= dur <= 2.5 * expect):
            bad.append(u)
        elif has_long_tone(y):
            print(f"    [tone] held pitch in: {u['text'][:50]!r}", flush=True)
            bad.append(u)
        else:
            sf.write(cache_path(u["text"], u["voice"]), y, SR, subtype="PCM_16")
    return bad


def prefill_cache(units):
    """Fill the cache for a chapter, batching length-sorted misses.

    Units are grouped by length because a batch costs as long as its longest
    member. Anything that fails the duration check, and anything short enough
    to need the carrier, falls back to one-at-a-time generation.
    """
    todo = [u for u in units
            if len(u["text"]) >= MERGE_UNDER
            and not os.path.exists(cache_path(u["text"], u["voice"]))]
    if not todo:
        return
    todo.sort(key=lambda u: len(u["text"]))

    bs, i, redo = BATCH_SIZE, 0, []
    t0, n0 = time.time(), 0
    while i < len(todo):
        chunk = todo[i:i + bs]
        try:
            redo.extend(gen_batch(chunk))
            i += len(chunk)
        except torch.cuda.OutOfMemoryError:
            torch.cuda.empty_cache()
            if bs == 1:
                raise
            bs = max(1, bs // 2)
            print(f"    [oom] batch size -> {bs}", flush=True)
            continue

        # CUDA never raises OOM here -- WSL spills to system RAM instead and
        # just gets slow. So watch the number directly: sustained use near the
        # card's capacity means we are already spilling, and a smaller batch is
        # strictly faster than paging over PCIe.
        if i - n0 >= 20:
            # Release fragmented blocks back to the driver. Without this,
            # reserved memory only ever grows: it reached 20.7 GB on a 10 GB
            # card, spilled into system RAM, and the run was OOM-killed.
            torch.cuda.empty_cache()
            used = torch.cuda.memory_reserved() / 1e9
            rate = (i / max(time.time() - t0, 1e-6)) * 60
            print(f"    [{i}/{len(todo)}] bs={bs} {used:.1f} GB reserved, "
                  f"{rate:.1f} units/min", flush=True)
            if used > 8.0 and bs > 1:
                bs = max(1, bs // 2)
                print(f"    [vram {used:.1f} GB] batch size -> {bs}", flush=True)
            n0 = i

    for u in redo:
        print(f"    [resynth] {u['text'][:50]!r}", flush=True)
        synth(u["text"], u["voice"])


def synth(sent, voice, retries=2):
    """One sentence -> float32 @ 44.1 kHz. Mirrors mk.synth()'s contract."""
    cached = cache_path(sent, voice)
    if os.path.exists(cached):
        y, _ = sf.read(cached, dtype="float32")
        return y
    pitch, rate = prosody_for(sent)

    expect = max(0.6, len(sent) / CHARS_PER_SEC)
    for attempt in range(retries + 1):
        cond = make_cond_dict(text=sent, speaker=speaker(voice),
                              language="en-us", fmax=22050.0,
                              pitch_std=pitch, speaking_rate=rate)
        codes = model().generate(model().prepare_conditioning(cond),
                                 progress_bar=False)
        # same padding-tone truncation as the batched path
        y = model().autoencoder.decode(
            trim_pad_codes(codes[0]).unsqueeze(0)).cpu()[0]
        y = y.mean(dim=0).numpy().astype(np.float32) if y.ndim > 1 \
            else y.numpy().astype(np.float32)
        dur = y.size / SR

        # Zonos is stochastic and can run away on a sentence, emitting a long
        # garbled tail or clipping it short. Catch the obvious failures and
        # resample rather than baking them into a 40-minute chapter.
        if 0.4 * expect <= dur <= 2.5 * expect and not has_long_tone(y):
            sf.write(cached, y, SR, subtype="PCM_16")
            return y
        why = ("held tone" if 0.4 * expect <= dur <= 2.5 * expect
               else f"{dur:.1f}s vs ~{expect:.1f}s")
        print(f"    [retry {attempt+1}] {why}: {sent[:50]!r}", flush=True)

    print(f"    [give up] using last take for: {sent[:55]!r}", flush=True)
    sf.write(cached, y, SR, subtype="PCM_16")
    return y


def build_units(items):
    """Flatten the chapter into synthesis units.

    Sentences are merged within a paragraph up to MERGE_MIN/MERGE_MAX so each
    unit has enough runway. Merging across a paragraph boundary happens only
    when the unit is still too short to stand alone AND the cast voice is
    unchanged -- the opening of every chapter is four short one-line paragraphs
    ('Chapter 1', the journal heading, the shorthand note, the date), and the
    voice switches at the heading, so that boundary must be respected.
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

    # cross-paragraph pass: only for units too short to stand alone
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
    """Render a too-short utterance with a throwaway tail, then cut the tail.

    Used for units that cannot merge -- 'Chapter 1' is narrator-voiced and the
    line after it switches to Harker, so it has nowhere to merge to. The
    carrier gives the model runway; only the heading ships.
    """
    body = text.rstrip()
    if not body.endswith((".", "!", "?")):
        body += "."
    y = synth(body + " " + CARRIER, voice)
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
            if (j - i) * win >= int(SR * 0.18):      # a real sentence gap
                cuts.append(((i + j) // 2) * win)
            i = j
        else:
            i += 1

    est = int(y.size * len(body) / float(len(body) + 1 + len(CARRIER)))
    if not cuts:
        return y
    cut = min(cuts, key=lambda p: abs(p - est))
    if not (0.4 * est <= cut <= 2.0 * est):          # cut landed implausibly
        return y
    return y[:cut]


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
    print(f"  ch{n:02d}: {len(units)} units from {len(items)} paragraphs "
          f"(chars min={min(lens)} median={sorted(lens)[len(lens)//2]} "
          f"max={max(lens)}, {sum(1 for l in lens if l < MERGE_UNDER)} need carrier)",
          flush=True)

    t0 = time.time()
    # Generate first, in length-sorted batches; assembly below then reads
    # everything from the cache in document order.
    prefill_cache(units)
    print(f"  ch{n:02d}: synthesis done in {(time.time()-t0)/60:.1f} min, "
          f"assembling", flush=True)

    parts = []
    done = 0

    for k, u in enumerate(units):
        raw = (synth_carrier(u["text"], u["voice"])
               if len(u["text"]) < MERGE_UNDER else synth(u["text"], u["voice"]))
        clip = squeeze(mk.trim(raw, thresh_db=TRIM_DB, keep_ms=TRIM_KEEP_MS))
        if clip.size:
            parts.append(clip)
            done += 1
        parts.append(mk.silence(u["pause"]))

        if k % 20 == 0:
            el = time.time() - t0
            audio_s = sum(p.size for p in parts) / SR
            print(f"  ch{n:02d} [{k}/{len(units)}] voice={u['voice']} "
                  f"audio={audio_s/60:.1f}min elapsed={el/60:.1f}min", flush=True)

    if not parts:
        print("[abort] nothing synthesized")
        return False

    secs = mk.master(parts, out_mp3)
    shutil.copyfile(os.path.join(TMP, "_master.wav"),
                    os.path.join(TMP, f"_ch{n:02d}_master.wav"))
    print(f"[done] ch{n:02d} -> {out_mp3}  ({secs/60.0:.1f} min audio, "
          f"{done} units, {(time.time()-t0)/60:.1f} min wall)", flush=True)
    return True


def build_credits():
    """Opening credits, closing credits and the retail sample.

    Authors Republic requires the opening track to name ONLY title, author and
    narrator -- anything more (copyright, production credits) is a rejection.
    Short tracks also need a higher loudness target and minimal padding or the
    silence drags their RMS below the -23 dB floor. Both rules are in
    authors_republic_requirements.md.
    """
    opening = f"{mk.TITLE}. Written by {mk.AUTHOR}. Narrated by {mk.NARRATOR}."
    closing = f"This has been {mk.TITLE}, by {mk.AUTHOR}. The end."

    for name, text in (("opening_credits", opening), ("closing_credits", closing)):
        out = os.path.join(OUT, f"{name}.mp3")
        if os.path.exists(out) and os.path.getsize(out) > 20000:
            print(f"[skip] {name} already built", flush=True)
            continue
        clip = squeeze(mk.trim(synth(text, mk.NARRATOR_VOICE),
                               thresh_db=TRIM_DB, keep_ms=TRIM_KEEP_MS))
        if clip.size == 0:
            print(f"[warn] could not synthesize {name}", flush=True)
            continue
        mk.master([clip], out, target_i="-16", pad="1200|1200", tail="1.2")
        print(f"[done] {name}", flush=True)

    # Retail sample: 3 minutes cut from the chapter 1 WAV master, so it is
    # encoded once. The Kokoro build cut it from the finished mp3, making the
    # one track a reviewer is guaranteed to hear the only double-encoded file.
    master_wav = os.path.join(TMP, "_ch01_master.wav")
    out = os.path.join(OUT, "dracula_retail_sample.mp3")
    if os.path.exists(master_wav):
        subprocess.run([
            "ffmpeg", "-y", "-v", "error", "-ss", "30", "-t", "180",
            "-i", master_wav,
            "-af", "loudnorm=I=-20:TP=-3.5:LRA=7,adelay=1500|1500,apad=pad_dur=1.5",
            "-ar", "44100", "-ac", "1", "-b:a", BITRATE, out,
        ], check=True)
        print(f"[done] retail sample", flush=True)
    else:
        print("[warn] no chapter 1 master; skipping retail sample", flush=True)


def build_all(first=1, last=27):
    """Every chapter, then credits. Resumable: a chapter whose mp3 already
    exists is skipped, and the sentence cache replays anything already
    synthesized, so an interrupted run costs only the chapter it was inside."""
    t_all = time.time()
    built, skipped, failed = 0, 0, []

    for n in range(first, last + 1):
        out = os.path.join(OUT, f"dracula_ch_{n:02d}_en.mp3")
        if os.path.exists(out) and os.path.getsize(out) > 100000:
            print(f"[skip] ch{n:02d} already built", flush=True)
            skipped += 1
            continue
        try:
            if build_chapter(n):
                built += 1
        except Exception:
            failed.append(n)
            print(f"[ERROR] ch{n:02d} failed, continuing", flush=True)
            traceback.print_exc()
        el = (time.time() - t_all) / 3600.0
        print(f"[progress] {built} built, {skipped} skipped, "
              f"{len(failed)} failed, {el:.2f} h elapsed", flush=True)

    build_credits()
    print(f"[ALL DONE] {built} built, {skipped} skipped, "
          f"{(time.time()-t_all)/3600:.2f} h total", flush=True)
    if failed:
        print(f"[ALL DONE] FAILED CHAPTERS: {failed} -- rerun to retry",
              flush=True)
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
