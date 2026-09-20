import os
import subprocess
import sys

FINAL_AUDIO_DIR = r'C:\git_repo\TKprof_book\books\dracula\final_audio'

def main():
    print("--- Re-encoding all Dracula audio tracks to 192 kbps CBR ---")
    files = sorted([f for f in os.listdir(FINAL_AUDIO_DIR) if f.endswith('.mp3')])
    
    for idx, fname in enumerate(files, 1):
        fpath = os.path.join(FINAL_AUDIO_DIR, fname)
        tmp_path = os.path.join(FINAL_AUDIO_DIR, f"tmp_{fname}")
        
        orig_size = os.path.getsize(fpath) / (1024 * 1024)
        
        # ffmpeg command for 192 kbps CBR encoding
        cmd = [
            "ffmpeg", "-y",
            "-i", fpath,
            "-b:a", "192k",
            "-minrate", "192k",
            "-maxrate", "192k",
            "-bufsize", "192k",
            "-c:a", "libmp3lame",
            tmp_path
        ]
        
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        
        new_size = os.path.getsize(tmp_path) / (1024 * 1024)
        
        os.replace(tmp_path, fpath)
        print(f"[{idx:02d}/{len(files)}] {fname}: {orig_size:.2f} MB -> {new_size:.2f} MB")

    print("\n--- Summary of final file sizes ---")
    over_limit = 0
    for fname in sorted(os.listdir(FINAL_AUDIO_DIR)):
        if fname.endswith('.mp3'):
            fp = os.path.join(FINAL_AUDIO_DIR, fname)
            sz = os.path.getsize(fp) / (1024 * 1024)
            status = "OVER LIMIT" if sz > 170 else "OK"
            if sz > 170:
                over_limit += 1
            print(f"{fname}: {sz:.2f} MB [{status}]")
            
    print(f"\nRe-encoding complete! Over limit count: {over_limit}")

if __name__ == "__main__":
    main()
