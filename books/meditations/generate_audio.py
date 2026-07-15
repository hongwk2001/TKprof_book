import os
import subprocess
import glob
import sys

# Add project root to path so we can import check_audio_quality
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# The bumper file is shared, so we point to the prince folder for the mp3
BUMPER_FILE = os.path.join(os.path.dirname(BASE_DIR), "the_prince", "lordsonny-cinematic-hit-159487.mp3")
TEMP_DIR = os.path.join(BASE_DIR, "temp_audio")
FINAL_DIR = os.path.join(BASE_DIR, "final_audio")
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(FINAL_DIR, exist_ok=True)

VOICE = "en-GB-RyanNeural"

def check_track(filepath):
    """
    Runs Authors Republic QC check on a generated file.
    Prints PASS or FAIL with details. Returns True if passed.
    Per authors_republic_requirements.md:
      - RMS: -23 dB to -18 dB
      - Peak: max -3.0 dB
      - Leading silence: 1-5 seconds
      - Trailing silence: 1-5 seconds
      - Sample rate: 44100 Hz, CBR 192+ kbps
    """
    try:
        from check_audio_quality import check_file
        result = check_file(filepath)
        name = os.path.basename(filepath)
        if result and result['status'] == 'PASS':
            print(f"  [QC PASS] {name} — Peak={result['peak_db']:.2f}dB, RMS={result['rms_db']:.2f}dB")
            return True
        else:
            print(f"  [QC FAIL] {name} — DOES NOT MEET AUTHORS REPUBLIC REQUIREMENTS:")
            for err in (result or {}).get('errors', ['Unknown error']):
                print(f"    ✗ {err}")
            return False
    except Exception as e:
        print(f"  [QC ERROR] Could not verify {os.path.basename(filepath)}: {e}")
        return False

def run_cmd(cmd):
    # cmd is a list of strings
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error executing command:\n{result.stderr}")
        raise Exception(f"Command failed: {cmd}")

def generate_tts(text_file, out_file):
    if not os.path.exists(text_file):
        print(f"Skipping {text_file}, not found.")
        return False
    
    cmd = ["edge-tts", "--file", text_file, "--voice", VOICE, "--write-media", out_file]
    run_cmd(cmd)
    return True

def mix_audio(bumper, raw_audio, out_file, bumper_duration, add_full_outro=False):
    # Trim the bumper to bumper_duration
    trimmed_bumper = os.path.join(TEMP_DIR, "trimmed_bumper.mp3")
    run_cmd([
        "ffmpeg", "-y",
        "-t", str(bumper_duration),
        "-i", bumper,
        "-ar", "44100",
        "-b:a", "256k",
        trimmed_bumper,
        "-loglevel", "error"
    ])
    
    # Use filter_complex to concatenate, which automatically handles mismatched sample rates/channels
    filter_str = "[0:a]volume=0.2[b0];[b0][1:a]concat=n=2:v=0:a=1[outa]"
    cmd = [
        "ffmpeg", "-y",
        "-i", trimmed_bumper,
        "-i", raw_audio
    ]
    if add_full_outro:
        cmd.extend(["-i", bumper])
        filter_str = "[0:a]volume=0.2[b0];[2:a]volume=0.2[b2];[b0][1:a][b2]concat=n=3:v=0:a=1[outa]"
    
    cmd.extend([
        "-filter_complex", filter_str,
        "-map", "[outa]",
        "-ar", "44100",
        "-b:a", "256k",
        out_file,
        "-loglevel", "error"
    ])
    run_cmd(cmd)

def generate_closing(bumper, raw_audio, out_file):
    """
    Generate the closing track with:
    - 2s of clean silence at the START (required by Authors Republic QC)
    - bumper music intro (2s)
    - narration
    - bumper music outro
    - loudnorm applied to bring RMS into -23 to -18 dB target range
    - 2s of clean trailing silence at the END
    """
    # Step 1: Mix bumper + narration + outro bumper (same as add_full_outro)
    mixed_raw = os.path.join(TEMP_DIR, "closing_mixed_raw.mp3")
    trimmed_bumper = os.path.join(TEMP_DIR, "trimmed_bumper_closing.mp3")
    run_cmd([
        "ffmpeg", "-y",
        "-t", "2.0",
        "-i", bumper,
        "-ar", "44100",
        "-b:a", "256k",
        trimmed_bumper,
        "-loglevel", "error"
    ])
    run_cmd([
        "ffmpeg", "-y",
        "-i", trimmed_bumper,
        "-i", raw_audio,
        "-i", bumper,
        "-filter_complex",
        "[0:a]volume=0.2[b0];[2:a]volume=0.2[b2];[b0][1:a][b2]concat=n=3:v=0:a=1[outa]",
        "-map", "[outa]",
        "-ar", "44100",
        "-b:a", "256k",
        mixed_raw,
        "-loglevel", "error"
    ])

    # Step 2: Apply loudnorm to bring RMS to -19 dB (within -23 to -18 dB range),
    #         prepend 2s of clean silence, append 2s trailing silence
    #         adelay adds leading silence; apad adds trailing silence
    run_cmd([
        "ffmpeg", "-y",
        "-i", mixed_raw,
        "-af",
        "loudnorm=I=-19:TP=-3.1:LRA=11,adelay=2000|2000,apad=pad_dur=2",
        "-ar", "44100",
        "-b:a", "256k",
        out_file,
        "-loglevel", "error"
    ])
    print(f"  -> Closing track generated with silence padding and loudnorm normalization.")

def main():
    # 1. Generate Intro (Short Credits)
    intro_txt = os.path.join(BASE_DIR, "introduction_en.txt")
    intro_raw = os.path.join(TEMP_DIR, "raw_intro.mp3")
    intro_final = os.path.join(FINAL_DIR, "final_track_00_intro.mp3")
    
    print("Generating Intro...")
    if generate_tts(intro_txt, intro_raw):
        mix_audio(BUMPER_FILE, intro_raw, intro_final, bumper_duration=4.5)
        check_track(intro_final)
        print(f"Finished {intro_final}")

    # 1b. Generate Overview (Introduction Content)
    overview_txt = os.path.join(BASE_DIR, "overview_en.txt")
    overview_raw = os.path.join(TEMP_DIR, "raw_overview.mp3")
    overview_final = os.path.join(FINAL_DIR, "final_track_01.mp3")
    
    print("Generating Overview...")
    if generate_tts(overview_txt, overview_raw):
        mix_audio(BUMPER_FILE, overview_raw, overview_final, bumper_duration=2.0, add_full_outro=False)
        check_track(overview_final)
        print(f"Finished {overview_final}")

    # 2. Generate Chapters 1 to 12
    for i in range(1, 13):
        ch_txt = os.path.join(CHAPTERS_DIR, f"ch_{i:02d}_en.txt")
        ch_raw = os.path.join(TEMP_DIR, f"raw_ch_{i:02d}.mp3")
        # Shift output chapter files down by 1 (e.g. ch 1 -> track 02)
        ch_final = os.path.join(FINAL_DIR, f"final_track_{i+1:02d}.mp3")
        
        print(f"Generating Chapter {i} (saved as track {i+1})...")
        if generate_tts(ch_txt, ch_raw):
            mix_audio(BUMPER_FILE, ch_raw, ch_final, bumper_duration=2.0, add_full_outro=False)
            check_track(ch_final)
            print(f"Finished {ch_final}")

    # 3. Generate Closing Track
    # Uses generate_closing() instead of mix_audio() to satisfy Authors Republic QC:
    #   - Prepends 2s clean silence (start-of-track silence requirement)
    #   - Applies loudnorm normalization (RMS must be between -23 dB and -18 dB)
    closing_txt = os.path.join(BASE_DIR, "closing_en.txt")
    closing_raw = os.path.join(TEMP_DIR, "raw_closing.mp3")
    closing_final = os.path.join(FINAL_DIR, "closing.mp3")
    
    print("Generating Closing Track...")
    if generate_tts(closing_txt, closing_raw):
        generate_closing(BUMPER_FILE, closing_raw, closing_final)
        check_track(closing_final)
        print(f"Finished {closing_final}")

    # 4. Generate Sample Track (Intro + Chapter 1, cut to < 5 mins)
    sample_final = os.path.join(FINAL_DIR, "sample.mp3")
    print("Generating Sample Track...")
    sample_cmd = [
        "ffmpeg", "-y",
        "-i", intro_final,
        "-i", os.path.join(FINAL_DIR, "final_track_01.mp3"),
        "-filter_complex", "[0:a][1:a]concat=n=2:v=0:a=1[outa]",
        "-map", "[outa]",
        "-t", "290", # Limit duration to 4m 50s (under 5 minutes)
        "-ar", "44100",
        "-b:a", "256k",
        sample_final,
        "-loglevel", "error"
    ]
    run_cmd(sample_cmd)
    check_track(sample_final)
    print(f"Finished {sample_final}")

    print("\nAudio generation complete. Review any [QC FAIL] items above before uploading.")

if __name__ == "__main__":
    main()
