import os
import sys
import glob
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
FINAL_KO_DIR = os.path.join(SCRIPT_DIR, "final_audio_ko")

def apply_post_processing_mono(raw_path, clean_path, bitrate=256):
    """
    Applies standard FFmpeg post-processing to satisfy ACX / Authors Republic requirements:
    - Target RMS: -19 LUFS (RMS between -23 dB and -18 dB)
    - True Peak limit: <= -3.0 dB (-3.5 dB targeted)
    - Clean silence padding: 2.0s (2000ms) at start AND end
    - Sample rate: 44,100 Hz
    - Channels: Mono (-ac 1) across 100% of files
    - Bitrate: 256 kbps CBR MP3
    """
    volume_norm = "loudnorm=I=-19:TP=-3.5:LRA=7"
    peak_limiter = "alimiter=limit=-3.5dB:level=false"
    strip_silence = "silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0,areverse,silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0,areverse"
    leading_silence = "adelay=2000|2000"
    trailing_silence = "apad=pad_dur=2"

    filter_chain = f"{strip_silence},{volume_norm},{peak_limiter},{leading_silence},{trailing_silence}"

    cmd = [
        "ffmpeg", "-y", "-threads", "8", "-i", raw_path,
        "-af", filter_chain,
        "-ac", "1",
        "-ar", "44100",
        "-b:a", f"{bitrate}k",
        clean_path
    ]

    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] FFmpeg failed for {os.path.basename(raw_path)}: {e.stderr}", file=sys.stderr)
        return False

def main():
    print("=========================================================================")
    print("      ENFORCING MONO (-ac 1) & ACX SPECS FOR BEOWULF KOREAN AUDIO       ")
    print("=========================================================================\n")

    files = sorted(glob.glob(os.path.join(FINAL_KO_DIR, "**", "*.mp3"), recursive=True))
    print(f"Found {len(files)} MP3 files across {FINAL_KO_DIR} and subdirectories...\n")

    repaired_count = 0

    for fpath in files:
        fname = os.path.basename(fpath)
        temp_out = fpath + ".tmp.mp3"

        print(f" Processing (Mono -ac 1): {fname}...")
        if apply_post_processing_mono(fpath, temp_out, bitrate=256):
            os.replace(temp_out, fpath)
            repaired_count += 1
            print(f"   -> [MONO FIXED] {fname}")
        else:
            if os.path.exists(temp_out):
                os.remove(temp_out)
            print(f"   -> [FAIL] {fname}")

    print("\n=========================================================================")
    print(f" MONO ENFORCEMENT COMPLETE: {repaired_count}/{len(files)} files converted to Mono 256k CBR MP3.")
    print("=========================================================================\n")

if __name__ == "__main__":
    main()
