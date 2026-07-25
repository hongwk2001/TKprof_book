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
        
    status = "FAIL" if errors else "PASS"
    
    return {
        "filename": filename,
        "filepath": filepath,
        "status": status,
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
                if file.lower().endswith(".mp3"):
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
        print(f"  Levels: Peak = {r['peak_db']:.2f} dB, RMS = {r['rms_db']:.2f} dB")
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
