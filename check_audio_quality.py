import os
import sys
import json
import re
import subprocess
import argparse

# Authors Republic / ACX Quality Standards:
# 1. 192 kbps or higher Constant Bit Rate (CBR)
# 2. 44.1 kHz sample rate (44100 Hz)
# 3. Channels must be consistent across all files (either all mono or all stereo)
# 4. Max Peak level must be under -3.0 dB (-3 dB or lower, e.g. -3.1 dB)
# 5. RMS level must be between -23 dB and -18 dB RMS
# 6. Beginning silence (heading): 0.5 to 1.0 seconds
# 7. Ending silence (trailing): 1.0 to 5.0 seconds
# 8. File duration: Less than 120 minutes

def probe_audio_format(filepath):
    """
    Runs ffprobe on the file to extract audio properties.
    """
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "a:0",
        "-show_entries", "stream=sample_rate,channels,bit_rate,codec_name",
        "-show_entries", "format=duration,bit_rate",
        "-of", "json",
        filepath
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(res.stdout)
        
        stream = data.get("streams", [{}])[0]
        fmt = data.get("format", {})
        
        sample_rate = int(stream.get("sample_rate", 0))
        channels = int(stream.get("channels", 0))
        duration = float(fmt.get("duration", 0.0))
        
        # Stream bitrate is more accurate, fallback to format bitrate
        bitrate_str = stream.get("bit_rate") or fmt.get("bit_rate")
        bitrate = int(bitrate_str) // 1000 if bitrate_str else 0
        
        return {
            "sample_rate": sample_rate,
            "channels": channels,
            "duration": duration,
            "bitrate_kbps": bitrate,
            "codec": stream.get("codec_name", "unknown")
        }
    except Exception as e:
        print(f"Error probing format for {filepath}: {e}", file=sys.stderr)
        return None

def analyze_audio_levels_and_silence(filepath, duration):
    """
    Runs ffmpeg with volumedetect and silencedetect filters.
    """
    # We detect silence with noise threshold of -50dB, which is standard.
    # If the environment has very low noise floor, -55dB or -60dB can be used.
    cmd = [
        "ffmpeg", "-y", "-i", filepath,
        "-filter_complex", "volumedetect;[0:a]silencedetect=noise=-50dB:d=0.1",
        "-f", "null", "-"
    ]
    try:
        # ffmpeg outputs stats to stderr
        res = subprocess.run(cmd, capture_output=True, text=True)
        stderr = res.stderr
        
        # 1. Parse Volume Stats
        max_vol_match = re.search(r"max_volume:\s+([-\d.]+)\s+dB", stderr)
        mean_vol_match = re.search(r"mean_volume:\s+([-\d.]+)\s+dB", stderr)
        
        max_vol = float(max_vol_match.group(1)) if max_vol_match else None
        mean_vol = float(mean_vol_match.group(1)) if mean_vol_match else None
        
        # 2. Parse Silence
        silences = []
        # Look for: [silencedetect @ 0x...] silence_start: 0
        # and [silencedetect @ 0x...] silence_end: 1.25 | silence_duration: 1.25
        # Also parse lines where silence starts but might not end before EOF (ending silence)
        
        start_pattern = re.compile(r"silence_start:\s+([\d.]+)")
        end_pattern = re.compile(r"silence_end:\s+([\d.]+)\s+\|\s+silence_duration:\s+([\d.]+)")
        
        current_start = None
        for line in stderr.splitlines():
            s_match = start_pattern.search(line)
            e_match = end_pattern.search(line)
            if s_match:
                current_start = float(s_match.group(1))
            if e_match:
                end_time = float(e_match.group(1))
                dur = float(e_match.group(2))
                if current_start is not None:
                    silences.append({"start": current_start, "end": end_time, "duration": dur})
                    current_start = None
        
        # Handle case where the file ends in silence but no end event is printed
        if current_start is not None:
            silences.append({"start": current_start, "end": duration, "duration": duration - current_start})
            
        # Determine leading/trailing silence
        leading_silence = 0.0
        trailing_silence = 0.0
        
        if silences:
            # Leading silence: check if the first silence starts near the beginning (<= 0.1s)
            first = silences[0]
            if first["start"] <= 0.1:
                leading_silence = first["duration"]
            
            # Trailing silence: check if the last silence ends near the duration (within 0.2s)
            last = silences[-1]
            if abs(last["end"] - duration) <= 0.2:
                trailing_silence = last["duration"]
                
        return {
            "max_volume_db": max_vol,
            "mean_volume_db": mean_vol,
            "leading_silence": leading_silence,
            "trailing_silence": trailing_silence,
            "raw_silences": silences
        }
    except Exception as e:
        print(f"Error analyzing levels/silence for {filepath}: {e}", file=sys.stderr)
        return None

def analyze_narration_content(filepath, duration, lead=0.0, trail=0.0):
    """
    Content checks that the container-level checks above cannot see.

    Both Authors Republic rejections (2026-08-17 bilingual, 2026-09-14 English)
    passed every check in check_file() and were still refused on narration
    quality. These are the three measurements that would have caught them, per
    NARRATION_REJECTION_ANALYSIS.md section 5.4.

    Samples a 120s excerpt from the middle of the file: three extra ffmpeg
    passes over a full 40-minute chapter is too slow to run on every build.
    """
    start = max(0.0, duration / 2.0 - 60.0)
    excerpt = ["-ss", str(start), "-t", "120"]

    def mean_db(af):
        r = subprocess.run(
            ["ffmpeg", "-hide_banner"] + excerpt + ["-i", filepath,
             "-af", af, "-f", "null", "-"],
            capture_output=True, text=True)
        m = re.search(r"mean_volume:\s*(-?[\d.]+) dB", r.stderr)
        return float(m.group(1)) if m else None

    # 1. source bandwidth: a 24 kHz source upsampled to 44.1 kHz has a hard
    #    ~12 kHz ceiling, which a listener hears as muffled.
    low = mean_db("highpass=f=8000,lowpass=f=11000,volumedetect")
    high = mean_db("highpass=f=13000,highpass=f=13000,volumedetect")
    headroom = (high - low) if (low is not None and high is not None) else None

    # 2 & 3. silence ratio and pause distribution. This is a single cheap pass,
    # so it gets a wider window than the bandwidth passes above -- 120s yields
    # too few pauses for the bucket statistic to be stable.
    #
    # Measure the BODY only. AR mandates 1-5s of silence at each end, so
    # including it makes short credits tracks look pathological: a 10s intro
    # with 4s of required padding scores 60% silence and fails for complying
    # with the spec. Below 30s of body there is not enough left to measure.
    body = max(0.0, duration - lead - trail)
    pause_span = min(300.0, body)
    pause_start = lead + max(0.0, (body - pause_span) / 2.0)
    if pause_span < 30.0:
        return {
            "band_8_11k_db": low,
            "band_13k_db": high,
            "bandwidth_headroom_db": headroom,
            "silence_ratio_pct": None,
            "pause_count": None,
            "top_pause_bucket_pct": None,
        }
    r = subprocess.run(
        ["ffmpeg", "-hide_banner", "-ss", str(pause_start), "-t",
         str(pause_span), "-i", filepath, "-af",
         "silencedetect=noise=-40dB:d=0.15", "-f", "null", "-"],
        capture_output=True, text=True)
    pauses = [float(x) for x in
              re.findall(r"silence_duration:\s*([\d.]+)", r.stderr)]

    span = pause_span
    silence_ratio = 100.0 * sum(pauses) / span if span else 0.0

    # quantization: fixed pause constants pile every gap into one 100 ms
    # bucket. A human read spreads out with a long tail.
    #
    # CAVEAT: the 30% threshold below is a heuristic, not a calibrated figure --
    # it flags the known-rejected build but has never been checked against a
    # human-narrated reference, and it is sensitive to bucket width (the same
    # file scores 39% at 100ms, 27% at 50ms, 18% at 20ms). It is a WARNING, not
    # an error, for that reason. Recalibrate once a passing build exists.
    top_bucket_pct = None
    if len(pauses) >= 20:
        buckets = {}
        for p in pauses:
            b = round(p // 0.1 * 0.1, 1)
            buckets[b] = buckets.get(b, 0) + 1
        top_bucket_pct = 100.0 * max(buckets.values()) / len(pauses)

    return {
        "band_8_11k_db": low,
        "band_13k_db": high,
        "bandwidth_headroom_db": headroom,
        "silence_ratio_pct": silence_ratio,
        "pause_count": len(pauses),
        "top_pause_bucket_pct": top_bucket_pct,
    }


def check_file(filepath):
    """
    Checks a single audio file against ACX/Authors Republic standards.
    """
    filename = os.path.basename(filepath)
    fmt = probe_audio_format(filepath)
    if not fmt:
        return {"filename": filename, "status": "FAIL", "errors": ["Failed to probe file format."]}
        
    analysis = analyze_audio_levels_and_silence(filepath, fmt["duration"])
    if not analysis:
        return {"filename": filename, "status": "FAIL", "errors": ["Failed to analyze audio levels/silence."]}
        
    errors = []
    warnings = []
    
    # 1. Bitrate check
    if fmt["bitrate_kbps"] < 192:
        errors.append(f"Bitrate is {fmt['bitrate_kbps']}kbps (min required: 192kbps).")
        
    # 2. Sample rate check
    if fmt["sample_rate"] != 44100:
        errors.append(f"Sample rate is {fmt['sample_rate']}Hz (must be exactly 44100Hz).")
        
    # 3. Peak check
    peak = analysis["max_volume_db"]
    if peak is not None:
        if peak > -3.0:
            errors.append(f"Peak level is {peak:.1f} dB (must be under -3.0 dB).")
    else:
        errors.append("Could not detect peak level.")
        
    # 4. RMS check
    rms = analysis["mean_volume_db"]
    if rms is not None:
        if rms > -18.0 or rms < -23.0:
            errors.append(f"RMS is {rms:.1f} dB (must be between -23.0 dB and -18.0 dB).")
    else:
        errors.append("Could not detect RMS volume.")
        
    # 5. Silence checks
    leading = analysis["leading_silence"]
    trailing = analysis["trailing_silence"]
    
    if leading < 1.0 or leading > 5.0:
        errors.append(f"Leading silence is {leading:.2f}s (must be between 1.0s and 5.0s).")
        
    if trailing < 1.0 or trailing > 5.0:
        errors.append(f"Trailing silence is {trailing:.2f}s (must be between 1.0s and 5.0s).")
        
    # 6. Duration check (120 minutes)
    dur_mins = fmt["duration"] / 60.0
    if dur_mins > 120.0:
        errors.append(f"Duration is {dur_mins:.1f} minutes (max limit is 120 minutes).")
        
    # 7-9. Narration content checks (see analyze_narration_content).
    content = analyze_narration_content(filepath, fmt["duration"], leading, trailing)

    headroom = content["bandwidth_headroom_db"]
    if headroom is not None and headroom <= -15.0:
        errors.append(
            f"No energy above 13kHz (headroom {headroom:.1f} dB): the source is "
            f"upsampled, not {fmt['sample_rate']}Hz narration. Reads as muffled."
        )

    sil_pct = content["silence_ratio_pct"]
    if sil_pct is not None and sil_pct > 12.0:
        errors.append(f"Silence is {sil_pct:.1f}% of narration body (max 12%).")

    top = content["top_pause_bucket_pct"]
    if top is not None and top > 30.0:
        warnings.append(
            f"{top:.0f}% of pauses fall in one 100ms bucket: pause lengths are "
            f"quantized, which sounds mechanical. Vary them."
        )

    status = "FAIL" if errors else "PASS"

    return {
        "filename": filename,
        "filepath": filepath,
        "status": status,
        **content,
        "sample_rate": fmt["sample_rate"],
        "channels": fmt["channels"],
        "duration": fmt["duration"],
        "bitrate_kbps": fmt["bitrate_kbps"],
        "peak_db": peak,
        "rms_db": rms,
        "leading_silence": leading,
        "trailing_silence": trailing,
        "errors": errors,
        "warnings": warnings
    }

def main():
    parser = argparse.ArgumentParser(description="Check audio files against Authors Republic / ACX quality standards.")
    parser.add_argument("path", nargs="?", default=".", help="Path to file or directory of audio files (default: current directory)")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    args = parser.parse_args()
    
    target_path = os.path.abspath(args.path)
    
    if not os.path.exists(target_path):
        print(f"Error: Path '{target_path}' does not exist.")
        sys.exit(1)
        
    audio_files = []
    if os.path.isdir(target_path):
        # Scan for mp3 files
        for root, _, files in os.walk(target_path):
            # Skip hidden folders or venv
            if any(part.startswith(".") or part == "venv" for part in root.split(os.sep)):
                continue
            for file in files:
                if file.lower().endswith(".mp3") and not file.startswith("temp_") and not file.endswith(".tmp.mp3"):
                    audio_files.append(os.path.join(root, file))
    else:
        if target_path.lower().endswith(".mp3"):
            audio_files.append(target_path)
            
    if not audio_files:
        if args.json:
            print(json.dumps({"error": "No MP3 files found."}))
        else:
            print("No MP3 files found in the specified path.")
        sys.exit(0)
        
    results = []
    channel_counts = set()
    
    print(f"Scanning {len(audio_files)} files...", file=sys.stderr if not args.json else sys.stdout)
    
    for filepath in sorted(audio_files):
        res = check_file(filepath)
        results.append(res)
        if "channels" in res:
            channel_counts.add(res["channels"])
            
    # Check channel consistency
    channel_error = None
    if len(channel_counts) > 1:
        channel_error = f"Inconsistent channel counts detected across files: {list(channel_counts)}. Files must all be mono or all be stereo."
        for res in results:
            if res["status"] == "PASS":
                res["status"] = "FAIL"
            res["errors"].append(channel_error)
            
    if args.json:
        print(json.dumps(results, indent=2))
        sys.exit(0)
        
    # Print human-readable report
    passed_count = sum(1 for r in results if r["status"] == "PASS")
    failed_count = len(results) - passed_count
    
    print("\n" + "="*80)
    print(f" AUDIO QUALITY CHECK REPORT: {passed_count} PASSED, {failed_count} FAILED")
    print("="*80 + "\n")
    
    for r in results:
        print(f"File: {r['filename']}")
        status_str = f"[{r['status']}]"
        
        print(f"  Status: {status_str}")
        print(f"  Format: {r['bitrate_kbps']}kbps CBR, {r['sample_rate']}Hz, {r['channels']}ch, {r['duration']/60.0:.2f} mins")
        peak_str = f"{r['peak_db']:.2f} dB" if r['peak_db'] is not None else "N/A"
        rms_str = f"{r['rms_db']:.2f} dB" if r['rms_db'] is not None else "N/A"
        print(f"  Levels: Peak = {peak_str}, RMS = {rms_str}")
        print(f"  Silence: Leading = {r['leading_silence']:.2f}s (target: 0.5-1.0s), Trailing = {r['trailing_silence']:.2f}s (target: 1.0-5.0s)")
        
        if r["errors"]:
            print("  Errors:")
            for err in r["errors"]:
                print(f"    - {err}")
        print("-" * 50)
        
    if channel_error:
        print(f"\n[CRITICAL WARNING] {channel_error}")
        
    print(f"\nSummary: {passed_count} files passed, {failed_count} files failed.")

if __name__ == "__main__":
    main()
