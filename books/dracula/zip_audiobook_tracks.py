import os
import zipfile
import time

AUDIO_DIR = r'C:\git_repo\TKprof_book\books\dracula\final_audio'
ZIP_PATH = r'C:\git_repo\TKprof_book\books\dracula\dracula_bilingual_audiobook_34tracks.zip'

TRACK_NAMES = [
    "opening_credits.mp3",
    "dracula_00_intro_bilingual_sunhi.mp3",
    "dracula_ch_01_bilingual_sunhi.mp3",
    "dracula_ch_02_bilingual_sunhi.mp3",
    "dracula_ch_03_bilingual_sunhi.mp3",
    "dracula_ch_04_bilingual_sunhi.mp3",
    "dracula_ch_05_bilingual_sunhi.mp3",
    "dracula_ch_06_bilingual_sunhi.mp3",
    "dracula_ch_07_bilingual_sunhi.mp3",
    "dracula_ch_08_bilingual_sunhi.mp3",
    "dracula_ch_09_bilingual_sunhi.mp3",
    "dracula_ch_10_bilingual_sunhi.mp3",
    "dracula_ch_11_bilingual_sunhi.mp3",
    "dracula_ch_12_bilingual_sunhi.mp3",
    "dracula_ch_13a_bilingual_sunhi.mp3",
    "dracula_ch_13b_bilingual_sunhi.mp3",
    "dracula_ch_14_bilingual_sunhi.mp3",
    "dracula_ch_15_bilingual_sunhi.mp3",
    "dracula_ch_16_bilingual_sunhi.mp3",
    "dracula_ch_17_bilingual_sunhi.mp3",
    "dracula_ch_18_bilingual_sunhi.mp3",
    "dracula_ch_19_bilingual_sunhi.mp3",
    "dracula_ch_20_bilingual_sunhi.mp3",
    "dracula_ch_21_bilingual_sunhi.mp3",
    "dracula_ch_22_bilingual_sunhi.mp3",
    "dracula_ch_23_bilingual_sunhi.mp3",
    "dracula_ch_24_bilingual_sunhi.mp3",
    "dracula_ch_25_bilingual_sunhi.mp3",
    "dracula_ch_26a_bilingual_sunhi.mp3",
    "dracula_ch_26b_bilingual_sunhi.mp3",
    "dracula_ch_27a_bilingual_sunhi.mp3",
    "dracula_ch_27b_bilingual_sunhi.mp3",
    "dracula_99_closing_bilingual_sunhi.mp3",
    "closing_credits.mp3"
]

def main():
    print(f"Creating audiobook tracks ZIP archive: {ZIP_PATH}...")
    start = time.time()
    
    with zipfile.ZipFile(ZIP_PATH, 'w', compression=zipfile.ZIP_STORED) as zf:
        for idx, track_name in enumerate(TRACK_NAMES, 1):
            file_path = os.path.join(AUDIO_DIR, track_name)
            if not os.path.exists(file_path):
                print(f"[ERROR] Missing track file: {file_path}")
                return False
                
            # Prefix filename with sequence index (01_, 02_, ...) so Google Play orders them 100% perfectly!
            arc_name = f"{idx:02d}_{track_name}"
            size_mb = os.path.getsize(file_path) / (1024 * 1024)
            print(f" [{idx:02d}/{len(TRACK_NAMES)}] Adding {track_name} -> {arc_name} ({size_mb:.2f} MB)")
            zf.write(file_path, arcname=arc_name)
            
    zip_size_gb = os.path.getsize(ZIP_PATH) / (1024 * 1024 * 1024)
    elapsed = time.time() - start
    print(f"\n[SUCCESS] Created {ZIP_PATH} ({zip_size_gb:.2f} GB) in {elapsed:.1f}s")
    return True

if __name__ == '__main__':
    main()
