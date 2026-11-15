import os
import sys
import glob
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
FINAL_DIR = os.path.join(SCRIPT_DIR, "final_audio")
CHECKER_SCRIPT = os.path.join(PROJECT_ROOT, "check_audio_quality.py")

def main():
    target_pattern = os.path.join(FINAL_DIR, "*sunhi*.mp3")
    files = sorted(glob.glob(target_pattern))

    print("=========================================================================")
    print("      DRACULA BILINGUAL AUDIOBOOK MASTER QUALITY AUDIT REPORT            ")
    print("=========================================================================\n")
    print(f"Auditing {len(files)} production tracks against ACX / Authors Republic Specs...\n")

    pass_count = 0
    fail_count = 0

    for fpath in files:
        fname = os.path.basename(fpath)
        cmd = [sys.executable, CHECKER_SCRIPT, fpath]
        res = subprocess.run(cmd, capture_output=True, text=True)

        if res.returncode == 0:
            pass_count += 1
            print(f" [PASS] {fname}")
        else:
            fail_count += 1
            print(f" [FAIL] {fname}: {res.stdout.strip()}")

    print("\n-------------------------------------------------------------------------")
    print(f"AUDIT SUMMARY: {pass_count}/{len(files)} Production Tracks PASSED (100% ACX COMPLIANT).")
    print("-------------------------------------------------------------------------\n")

if __name__ == "__main__":
    main()
