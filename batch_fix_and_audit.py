import os
import sys
import glob
import subprocess
from fix_audio_quality import fix_audio_file
from check_audio_quality import check_file

FAILING_FOLDERS = [
    r"books/blue_castle/final_audio_ko_ready",
    r"books/beowulf/final_audio",
    r"books/gilgamesh/audio",
    r"books/richest_man_in_babylon/final_audio_ar_ready",
    r"books/richest_man_in_babylon_linear/final_audio",
    r"books/secret_garden/final_audio_ko",
    r"books/christmas_carol/audio",
    r"books/the_enchanted_april/final_audio_ko_ready",
    r"books/art_of_war/final_audio",
    r"books/dracula/final_audio"
]

def clean_temp_files(folder_abs):
    temp_patterns = ["temp_stripped.mp3", "temp_norm.mp3", "*.tmp.mp3"]
    for pat in temp_patterns:
        for fpath in glob.glob(os.path.join(folder_abs, pat)):
            try:
                os.remove(fpath)
                print(f"Cleaned temp file: {os.path.basename(fpath)}")
            except OSError:
                pass

def process_folder(folder_rel):
    folder_abs = os.path.abspath(folder_rel)
    if not os.path.exists(folder_abs):
        print(f"[SKIP] Directory non-existent: {folder_abs}")
        return
    
    clean_temp_files(folder_abs)
    
    all_files = os.listdir(folder_abs)
    mp3_files = [
        f for f in all_files 
        if f.lower().endswith(".mp3") 
        and not f.startswith("temp_") 
        and not f.endswith(".tmp.mp3")
    ]
    
    print(f"\n==================================================")
    print(f" Processing Folder ({len(mp3_files)} files): {folder_rel}")
    print(f"==================================================")
    
    success_count = 0
    fail_count = 0
    
    for filename in sorted(mp3_files):
        file_path = os.path.join(folder_abs, filename)
        tmp_path = file_path + ".tmp.mp3"
        
        print(f"  Fixing {filename}...")
        if fix_audio_file(file_path, tmp_path, bitrate=256):
            if os.path.exists(file_path):
                os.remove(file_path)
            os.rename(tmp_path, file_path)
            
            res = check_file(file_path)
            if res and res["status"] == "PASS":
                success_count += 1
                print(f"    [PASS] {filename} (Peak={res['peak_db']:.2f}dB, RMS={res['rms_db']:.2f}dB, Bitrate={res['bitrate_kbps']}k)")
            else:
                fail_count += 1
                print(f"    [FAIL] {filename}: {res.get('errors') if res else 'Unknown error'}")
        else:
            fail_count += 1
            print(f"    [ERROR] Failed to fix {filename}")
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except OSError:
                    pass
                    
    clean_temp_files(folder_abs)
    
    # Run full folder audit check
    print(f"\n-- Running Full Compliance Check on {folder_rel} --")
    audit_cmd = [sys.executable, "check_audio_quality.py", folder_abs]
    proc = subprocess.run(audit_cmd, capture_output=True, text=True)
    print(proc.stdout)
    if proc.stderr:
        print(proc.stderr, file=sys.stderr)
        
    print(f"--> Summary for {folder_rel}: {success_count} passed, {fail_count} failed.")

def main():
    for folder in FAILING_FOLDERS:
        process_folder(folder)

if __name__ == "__main__":
    main()
