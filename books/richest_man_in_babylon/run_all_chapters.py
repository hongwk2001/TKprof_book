"""
Run audio generation for all chapters serially.
If interrupted, simply re-run this script — already completed chapters are skipped.
"""
import os
import subprocess
import sys

CHAPTERS = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11"]
DONE_LOG = "batch_progress.log"
OUTPUT_DIR = "final_audio"

def load_done():
    if not os.path.exists(DONE_LOG):
        return set()
    with open(DONE_LOG, 'r') as f:
        return set(line.strip() for line in f if line.strip())

def mark_done(ch):
    with open(DONE_LOG, 'a') as f:
        f.write(ch + "\n")
    print(f"  ✅ Chapter {ch} marked complete in {DONE_LOG}")

def main():
    done = load_done()
    remaining = [ch for ch in CHAPTERS if ch not in done]
    
    if not remaining:
        print("All chapters already complete!")
        return

    print(f"Chapters already done: {sorted(done) or 'none'}")
    print(f"Chapters to process:   {remaining}")
    print("=" * 50)

    for ch in remaining:
        out_file = os.path.join(OUTPUT_DIR, f"final_ch_{ch}.mp3")
        
        # If final output already exists, skip
        if os.path.exists(out_file):
            print(f"[CH {ch}] Output already exists, skipping TTS. Marking done.")
            mark_done(ch)
            continue

        print(f"\n[CH {ch}] Starting generation...")
        result = subprocess.run(
            ["python", "generate_audio.py", ch],
            capture_output=False
        )

        if result.returncode == 0:
            mark_done(ch)
            print(f"[CH {ch}] Done!")
        else:
            print(f"[CH {ch}] ❌ FAILED (exit code {result.returncode}). Stopping.")
            print("Re-run this script to resume from this chapter.")
            sys.exit(1)

    print("\n" + "=" * 50)
    print("🎉 All chapters complete!")

if __name__ == "__main__":
    main()
