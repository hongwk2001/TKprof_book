import os
import shutil

DRACULA_DIR = os.path.dirname(os.path.abspath(__file__))
FINAL_AUDIO_DIR = os.path.join(DRACULA_DIR, "final_audio")
TEMP_AUDIO_DIR = os.path.join(DRACULA_DIR, "temp_audio")

# Core final products to keep in final_audio
KEEP_FILES = set([
    f"dracula_ch_{ch:02d}_bilingual_sunhi.mp3" for ch in range(1, 28)
] + [
    "dracula_00_intro_bilingual_sunhi.mp3",
    "dracula_99_closing_bilingual_sunhi.mp3",
    "dracula_sample_bilingual_sunhi.mp3",
    "opening_credits.mp3",
    "closing_credits.mp3",
    "note_by_billy.txt"
])

def main():
    bytes_freed = 0
    deleted_files_count = 0

    print("--- Cleaning final_audio directory ---")
    if os.path.exists(FINAL_AUDIO_DIR):
        for fname in os.listdir(FINAL_AUDIO_DIR):
            fpath = os.path.join(FINAL_AUDIO_DIR, fname)
            if os.path.isfile(fpath):
                if fname not in KEEP_FILES:
                    size = os.path.getsize(fpath)
                    bytes_freed += size
                    deleted_files_count += 1
                    os.remove(fpath)
                    print(f"Deleted old trial file: {fname} ({size / 1024 / 1024:.2f} MB)")
                else:
                    print(f"Keeping final product: {fname}")

    print("\n--- Cleaning temp_audio directory ---")
    if os.path.exists(TEMP_AUDIO_DIR):
        for root, dirs, files in os.walk(TEMP_AUDIO_DIR, topdown=False):
            for file in files:
                fpath = os.path.join(root, file)
                size = os.path.getsize(fpath)
                bytes_freed += size
                deleted_files_count += 1
                os.remove(fpath)
            for d in dirs:
                dpath = os.path.join(root, d)
                os.rmdir(dpath)
        print(f"Emptied temp_audio directory.")

    print("\n==========================================")
    print(f"Cleanup Complete!")
    print(f"Total files removed: {deleted_files_count}")
    print(f"Total disk space reclaimed: {bytes_freed / 1024 / 1024 / 1024:.2f} GB ({bytes_freed / 1024 / 1024:.2f} MB)")
    print("==========================================")

if __name__ == "__main__":
    main()
