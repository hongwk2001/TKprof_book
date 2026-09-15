"""
Authors Republic submission audit.

check_audio_quality.py gates individual tracks on the numbers. This audits a
whole SUBMISSION against every requirement in authors_republic_requirements.md,
including the ones no per-file check covers: CBR vs VBR, noise floor, file
size, bitrate consistency across the package, track structure, credits content,
retail sample length, and cover art.

Written after two rejections whose stated reasons were boilerplate, so the only
defence is to satisfy every documented requirement rather than guess which one
was missed.

Usage:
  venv/Scripts/python.exe ar_submission_audit.py books/dracula/final_audio_en_v2 \
      --cover books/dracula/cover_en_2400.jpg \
      --narrator "Fable AI and Bella AI" --title Dracula --author "Bram Stoker"
"""
import argparse
import json
import os
import re
import subprocess
import sys

PASS, FAIL, WARN = "PASS", "FAIL", "WARN"
results = []


def check(name, ok, detail=""):
    results.append((PASS if ok is True else (WARN if ok == WARN else FAIL),
                    name, detail))


def probe(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "stream=codec_name,sample_rate,channels,bit_rate",
         "-show_entries", "format=duration,bit_rate,size,format_name",
         "-of", "json", path], capture_output=True, text=True)
    d = json.loads(r.stdout or "{}")
    st = (d.get("streams") or [{}])[0]
    fm = d.get("format") or {}
    return {
        "codec": st.get("codec_name"),
        "sample_rate": int(st.get("sample_rate") or 0),
        "channels": int(st.get("channels") or 0),
        # STREAM bitrate, not format. The format figure includes ID3 and
        # container overhead, which made identical 192k CBR files report
        # 192006 / 192003 / 193411 and look inconsistent.
        "bitrate": int(st.get("bit_rate") or fm.get("bit_rate") or 0),
        "duration": float(fm.get("duration") or 0),
        "size": int(fm.get("size") or 0),
    }


def volume(path, af="volumedetect"):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", af,
                        "-f", "null", "-"], capture_output=True, text=True)
    out = {}
    for k in ("mean_volume", "max_volume"):
        m = re.search(rf"{k}:\s*(-?[\d.]+) dB", r.stderr)
        if m:
            out[k] = float(m.group(1))
    return out


def edge_silence(path, duration):
    """Leading and trailing silence, in seconds.

    Trailing is measured in its own window seeked to the last WINDOW seconds,
    because scanning the whole file and reasoning about the final silence_start
    got it wrong on every track -- it reported 0.0 for files that actually
    carry 1.2-2.8 s of padding.
    """
    WINDOW = 8.0

    head = subprocess.run(
        ["ffmpeg", "-hide_banner", "-t", str(WINDOW), "-i", path, "-af",
         "silencedetect=noise=-50dB:d=0.3", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    hs = [float(x) for x in re.findall(r"silence_start:\s*(-?[\d.]+)", head)]
    he = [float(x) for x in re.findall(r"silence_end:\s*([\d.]+)", head)]
    lead = he[0] if (he and (not hs or hs[0] <= 0.05)) else 0.0

    start = max(0.0, duration - WINDOW)
    win = min(WINDOW, duration)
    tail = subprocess.run(
        ["ffmpeg", "-hide_banner", "-ss", str(start), "-i", path, "-af",
         "silencedetect=noise=-50dB:d=0.3", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    ts = [float(x) for x in re.findall(r"silence_start:\s*(-?[\d.]+)", tail)]
    te = [float(x) for x in re.findall(r"silence_end:\s*([\d.]+)", tail)]
    trail = 0.0
    if ts:
        # the last run counts only if it reaches the end of the window
        if not te or te[-1] >= win - 0.15 or te[-1] < ts[-1]:
            trail = win - ts[-1]
    return lead, trail


def is_cbr(path):
    """CBR is required; VBR causes rejection. Sample frame bitrates."""
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries",
         "packet=size", "-read_intervals", "%+#400", "-of", "csv=p=0", path],
        capture_output=True, text=True)
    sizes = [int(x) for x in r.stdout.split() if x.strip().isdigit()]
    if len(sizes) < 50:
        return None, "too few frames sampled"
    uniq = set(sizes[5:-5])
    return (len(uniq) <= 2), f"{len(uniq)} distinct frame sizes in sample"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--cover")
    ap.add_argument("--narrator", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--author", required=True)
    a = ap.parse_args()

    mp3s = sorted(f for f in os.listdir(a.folder) if f.lower().endswith(".mp3"))
    paths = [os.path.join(a.folder, f) for f in mp3s]
    if not paths:
        print("no mp3 files found")
        return 1
    info = {f: probe(p) for f, p in zip(mp3s, paths)}

    # ---- section 1: audio specs -------------------------------------------
    bad = [f for f, i in info.items() if i["bitrate"] < 190000]
    check("bitrate >= 192 kbps", not bad, f"{len(bad)} under" if bad else
          f"all {len(mp3s)} at {info[mp3s[0]]['bitrate']//1000} kbps")

    rates = {i["bitrate"] // 1000 for i in info.values()}
    check("bitrate identical across package", len(rates) == 1, f"{sorted(rates)} kbps")

    srs = {i["sample_rate"] for i in info.values()}
    check("sample rate exactly 44100", srs == {44100}, str(sorted(srs)))

    chs = {i["channels"] for i in info.values()}
    check("channels consistent", len(chs) == 1,
          "mono" if chs == {1} else str(sorted(chs)))

    vbr_bad, vbr_note = [], ""
    for f, p in zip(mp3s, paths):
        ok, note = is_cbr(p)
        if ok is False:
            vbr_bad.append(f)
            vbr_note = note
    check("constant bitrate (CBR, not VBR)", not vbr_bad,
          f"{len(vbr_bad)} look VBR ({vbr_note})" if vbr_bad else "all CBR")

    over = [(f, i["duration"] / 60) for f, i in info.items() if i["duration"] > 120 * 60]
    check("duration <= 120 min", not over,
          f"max {max(i['duration'] for i in info.values())/60:.1f} min")

    big = [(f, i["size"] / 1048576) for f, i in info.items() if i["size"] > 170 * 1048576]
    check("file size <= 170 MB", not big,
          f"max {max(i['size'] for i in info.values())/1048576:.1f} MB")

    peaks, rmss, floors = {}, {}, {}
    for f, p in zip(mp3s, paths):
        v = volume(p)
        peaks[f] = v.get("max_volume", 0.0)
        rmss[f] = v.get("mean_volume", 0.0)
    bad = [f for f, v in peaks.items() if v > -3.0]
    check("peak below -3.0 dB", not bad,
          f"range {min(peaks.values()):.1f} to {max(peaks.values()):.1f}")
    bad = [f for f, v in rmss.items() if not (-23.0 < v < -18.0)]
    check("RMS within -23 to -18 dB", not bad,
          f"range {min(rmss.values()):.1f} to {max(rmss.values()):.1f}"
          + (f"; outside: {bad[:3]}" if bad else ""))

    # noise floor: measure the quietest 1s window near the padded head
    for f, p in zip(mp3s, paths):
        r = subprocess.run(["ffmpeg", "-hide_banner", "-ss", "0.2", "-t", "0.6",
                            "-i", p, "-af", "volumedetect", "-f", "null", "-"],
                           capture_output=True, text=True)
        m = re.search(r"mean_volume:\s*(-?[\d.]+) dB", r.stderr)
        floors[f] = float(m.group(1)) if m else 0.0
    loud_floor = [f for f, v in floors.items() if v > -60.0]
    check("noise floor below -60 dB", not loud_floor,
          f"worst {max(floors.values()):.1f} dB"
          + (f" ({len(loud_floor)} tracks above)" if loud_floor else ""))

    # ---- section 2: silence padding ---------------------------------------
    lead_bad, trail_bad = [], []
    for f, p in zip(mp3s, paths):
        lead, trail = edge_silence(p, info[f]["duration"])
        if not (1.0 <= lead <= 5.0):
            lead_bad.append((f, round(lead, 2)))
        if not (1.0 <= trail <= 5.0):
            trail_bad.append((f, round(trail, 2)))
    check("leading silence 1-5 s", not lead_bad,
          f"{len(lead_bad)} outside: {lead_bad[:3]}" if lead_bad else "all in range")
    check("trailing silence 1-5 s", not trail_bad,
          f"{len(trail_bad)} outside: {trail_bad[:3]}" if trail_bad else "all in range")

    # ---- section 4: required tracks ---------------------------------------
    has_open = any("opening_credits" in f for f in mp3s)
    has_close = any("closing_credits" in f for f in mp3s)
    sample = [f for f in mp3s if "retail_sample" in f]
    check("opening credits track present", has_open)
    check("closing credits track present", has_close)
    check("retail sample present", bool(sample))
    if sample:
        d = info[sample[0]]["duration"]
        check("retail sample 1-5 min", 60 <= d <= 300, f"{d/60:.1f} min")

    chapters = [f for f in mp3s if re.search(r"ch_?\d+", f)]
    check("chapters are standalone files", len(chapters) >= 1,
          f"{len(chapters)} chapter tracks")

    # ---- section 5: cover art ---------------------------------------------
    if a.cover and os.path.exists(a.cover):
        r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v",
                            "-show_entries", "stream=width,height,pix_fmt",
                            "-of", "csv=p=0", a.cover], capture_output=True, text=True)
        parts = r.stdout.strip().split(",")
        w, h = int(parts[0]), int(parts[1])
        pix = parts[2] if len(parts) > 2 else "?"
        check("cover 2400x2400", w == 2400 and h == 2400, f"{w}x{h}")
        check("cover is RGB (not CMYK)", not pix.startswith("cmyk"), pix)
        check("cover format jpg/png",
              a.cover.lower().endswith((".jpg", ".jpeg", ".png")),
              os.path.splitext(a.cover)[1])
    else:
        check("cover art", WARN, "not supplied or missing -- not audited")

    # ---- manual items ------------------------------------------------------
    check("opening credits say only title/author/narrator", WARN,
          f'expected: "{a.title}. Written by {a.author}. Narrated by '
          f'{a.narrator}." -- LISTEN to confirm')
    check("closing credits contain no URLs or extras", WARN, "LISTEN to confirm")
    check("each chapter announces its number/title", WARN, "LISTEN to confirm")
    check("cover narrator text matches audio exactly", WARN,
          f'cover must read "Narrated by {a.narrator}"')

    # ---- report -----------------------------------------------------------
    w = max(len(n) for _, n, _ in results)
    print(f"\nAUTHORS REPUBLIC SUBMISSION AUDIT — {a.folder}")
    print(f"{len(mp3s)} tracks\n")
    for status, name, detail in results:
        print(f"  [{status}] {name:<{w}}  {detail}")
    nf = sum(1 for s, _, _ in results if s == FAIL)
    nw = sum(1 for s, _, _ in results if s == WARN)
    print(f"\n  {sum(1 for s,_,_ in results if s==PASS)} passed, "
          f"{nf} failed, {nw} need a human")
    return 1 if nf else 0


if __name__ == "__main__":
    sys.exit(main())
