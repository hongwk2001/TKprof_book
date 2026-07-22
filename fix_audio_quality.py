import os
import sys
import json
import re
import subprocess
import argparse
from check_audio_quality import probe_audio_format, check_file

def fix_audio_file(input_path, output_path, bitrate=256):
    """
    Applies FFmpeg filters to clean silence, normalize volume, and adjust leading/trailing silence.
    """
    # 1. Probe original properties to detect channel count
    fmt = probe_audio_format(input_path)
    if not fmt:
        print(f"Error: Could not probe format for {input_path}")
        return False
        
    channels = fmt.get("channels", 2)
    # Target bitrate matching the source, but at least 192k
    out_bitrate = max(192, fmt.get("bitrate_kbps", bitrate))
    
    # 2. Build the filter graph
    # Strip existing silence
    strip_silence = "silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0,areverse,silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0,areverse"
    
    # Volume normalization (RMS target -19 LUFS, true peak -3.1 dB)
    volume_norm = "loudnorm=I=-19:TP=-3.1:LRA=11"
    
    # Add leading silence (2.0 seconds = 2000ms)
    # Format of adelay is delay_channel1|delay_channel2|...
    delay_str = "|".join(["2000"] * channels)
    leading_silence = f"adelay={delay_str}"
    
    # Add trailing silence (2.0 seconds)
    trailing_silence = "apad=pad_dur=2"
    
    filter_chain = f"{volume_norm},{strip_silence},{leading_silence},{trailing_silence}"
    
    cmd = [
        "ffmpeg", "-y", "-i", input_path,
        "-af", filter_chain,
        "-ar", "44100",
        "-b:a", f"{out_bitrate}k",
        output_path
    ]
    
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg failed for {os.path.basename(input_path)}:\n{e.stderr}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description="Fix audio quality of MP3 files to match Authors Republic / ACX specifications.")
    parser.add_argument("input_dir", help="Directory containing MP3 files to fix")
    parser.add_argument("output_dir", nargs="?", help="Directory to save fixed files (default: <input_dir>_fixed)")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite original files in-place (caution!)")
    args = parser.parse_args()
    
    input_dir = os.path.abspath(args.input_dir)
    if not os.path.isdir(input_dir):
        print(f"Error: Input directory '{input_dir}' does not exist.")
        sys.exit(1)
        
    if args.overwrite:
        output_dir = input_dir
        print("[WARNING] Overwrite mode enabled. Files will be modified in-place.")
    else:
        if args.output_dir:
            output_dir = os.path.abspath(args.output_dir)
        else:
            output_dir = input_dir.rstrip(r"\/") + "_fixed"
            
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # Scan for MP3s
    mp3_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".mp3")]
    if not mp3_files:
        print(f"No MP3 files found in '{input_dir}'")
        sys.exit(0)
        
    print(f"Found {len(mp3_files)} MP3 files to process.")
    print(f"Output directory: {output_dir}")
    print("="*60)
    
    success_count = 0
    fail_count = 0
    
    for filename in sorted(mp3_files):
        in_path = os.path.join(input_dir, filename)
        
        # If writing to same directory without overwrite flag, append _fixed to name
        if input_dir == output_dir and not args.overwrite:
            out_name = filename.replace(".mp3", "_fixed.mp3")
        else:
            out_name = filename
            
        out_path = os.path.join(output_dir, out_name)
        
        print(f"Processing {filename}...")
        
        # We process to a temp file first if overwriting
        temp_mode = (in_path == out_path)
        if temp_mode:
            proc_path = out_path + ".tmp.mp3"
        else:
            proc_path = out_path
            
        if fix_audio_file(in_path, proc_path):
            # Check the fixed file quality
            check_res = check_file(proc_path)
            if temp_mode:
                if os.path.exists(in_path):
                    os.remove(in_path)
                os.rename(proc_path, out_path)
            if check_res and check_res["status"] == "PASS":
                print(f"  -> SUCCESS! Passed quality check. (Peak={check_res['peak_db']:.2f}dB, RMS={check_res['rms_db']:.2f}dB)")
                success_count += 1
            else:
                print(f"  -> WARNING: Fixed file output saved (Peak={check_res['peak_db']:.2f}dB, RMS={check_res['rms_db']:.2f}dB).")
                for err in check_res.get("errors", []):
                    print(f"     - {err}")
                fail_count += 1
        else:
            print(f"  -> FAILED processing.")
            fail_count += 1
            
    print("\n" + "="*60)
    print(f"Process complete: {success_count} files fixed successfully, {fail_count} files failed.")
    print("="*60)

if __name__ == "__main__":
    main()
