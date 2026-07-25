import os
import sys
import json
import re
import subprocess
import argparse
from check_audio_quality import probe_audio_format, check_file

from pydub import AudioSegment

def fix_audio_file(input_path, output_path, bitrate=256):
    """
    Applies Pydub to strip silence, FFmpeg loudnorm for target volume,
    and Pydub to pad exact 2.0s leading/trailing silences.
    """
    # 1. Probe original properties to detect channel count
    fmt = probe_audio_format(input_path)
    if not fmt:
        print(f"Error: Could not probe format for {input_path}")
        return False
        
    channels = fmt.get("channels", 2)
    out_bitrate = max(192, fmt.get("bitrate_kbps", bitrate))
    
    # Create temporary files in the same directory as output
    temp_dir = os.path.dirname(output_path)
    temp_stripped = os.path.join(temp_dir, "temp_stripped.mp3")
    temp_norm = os.path.join(temp_dir, "temp_norm.mp3")
    
    try:
        # 2. Load with pydub and strip leading/trailing silence
        sound = AudioSegment.from_mp3(input_path)
        
        # Strip leading silence (below -50 dBFS)
        start_trim = 0
        chunk_size = 10  # ms
        for i in range(0, len(sound), chunk_size):
            if sound[i:i+chunk_size].dBFS > -50:
                start_trim = i
                break
                
        # Strip trailing silence
        end_trim = len(sound)
        for i in range(len(sound), 0, -chunk_size):
            if sound[i-chunk_size:i].dBFS > -50:
                end_trim = i
                break
                
        sound_trimmed = sound[start_trim:end_trim]
        sound_trimmed.export(temp_stripped, format="mp3", bitrate=f"{out_bitrate}k")
        
        # 3. Apply loudnorm normalization via FFmpeg (on stripped audio)
        volume_norm = "loudnorm=I=-19:TP=-3.1:LRA=11"
        cmd = [
            "ffmpeg", "-y", "-i", temp_stripped,
            "-af", volume_norm,
            "-ar", "44100",
            "-b:a", f"{out_bitrate}k",
            temp_norm
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"FFmpeg normalization failed:\n{result.stderr}", file=sys.stderr)
            return False
            
        # 4. Load normalized audio and add exactly 2.0s of clean silence at start and end
        norm_sound = AudioSegment.from_mp3(temp_norm)
        silence_padding = AudioSegment.silent(duration=2000, frame_rate=44100)
        
        # Combine
        final_sound = silence_padding + norm_sound + silence_padding
        
        # Export final file (ensuring constant bitrate & 44.1 kHz)
        final_sound.export(output_path, format="mp3", bitrate=f"{out_bitrate}k")
        return True
        
    except Exception as e:
        print(f"Exception during processing of {os.path.basename(input_path)}: {e}", file=sys.stderr)
        return False
    finally:
        # Clean up temporary files
        for temp_file in [temp_stripped, temp_norm]:
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except OSError:
                    pass

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
