import os
import sys
import subprocess
import time

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GEN_SCRIPT = os.path.join(SCRIPT_DIR, "generate_bilingual_audio.py")
PREP_SCRIPT = os.path.join(SCRIPT_DIR, "prepare_bilingual_script.py")

def main():
    print("=========================================================================")
    print("       DRACULA BILINGUAL AUDIOBOOK MASTER PRODUCTION RUNNER               ")
    print("=========================================================================\n")

    # Step 1: Ensure scripts exist
    print("[STEP 1] Verifying / Regenerating bilingual chapter scripts...")
    subprocess.run([sys.executable, PREP_SCRIPT], check=True)

    # Step 2: Determine target chapters and Korean voice engine
    target_arg = sys.argv[1] if len(sys.argv) > 1 else "rest"
    ko_engine = sys.argv[2] if len(sys.argv) > 2 else "edge"

    if target_arg == "all":
        chapters = list(range(1, 28))
    elif target_arg == "rest":
        chapters = list(range(2, 28))
    else:
        try:
            chapters = [int(target_arg)]
        except ValueError:
            print(f"[ERROR] Invalid target chapter argument: {target_arg}")
            sys.exit(1)

    print(f"\n[STEP 2] Processing {len(chapters)} chapter(s)... Target range: {chapters} | KO Engine: {ko_engine.upper()}\n")

    start_time = time.time()
    success_chapters = []
    failed_chapters = []

    for ch in chapters:
        ch_str = f"{ch:02d}"
        print(f"\n-------------------------------------------------------------------------")
        print(f" >>> RUNNING CHAPTER {ch_str} (KO Engine: {ko_engine.upper()}) <<<")
        print(f"-------------------------------------------------------------------------")

        cmd = [sys.executable, GEN_SCRIPT, str(ch), ko_engine]
        res = subprocess.run(cmd)

        if res.returncode == 0:
            success_chapters.append(ch)
            print(f"\n[COMPLETE] Chapter {ch_str} finished successfully.")
        else:
            failed_chapters.append(ch)
            print(f"\n[FAIL] Chapter {ch_str} encountered an error.")

    elapsed = time.time() - start_time
    mins = int(elapsed // 60)
    secs = int(elapsed % 60)

    print("\n=========================================================================")
    print(" PRODUCTION SUMMARY REPORT")
    print("=========================================================================")
    print(f" Total Time Elapsed : {mins}m {secs}s")
    print(f" Successful Chapters: {len(success_chapters)}/{len(chapters)} {success_chapters}")
    if failed_chapters:
        print(f" Failed Chapters    : {len(failed_chapters)} {failed_chapters}")
    print("=========================================================================\n")

if __name__ == "__main__":
    main()
