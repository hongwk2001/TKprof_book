import os
import sys

# Add root folder to path so we can import fix_audio_quality
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fix_audio_quality import fix_audio_file
from check_audio_quality import check_file

def fix_track(filepath):
    temp_path = filepath + ".tmp.mp3"
    print(f"Fixing: {filepath} -> {temp_path}")
    
    success = fix_audio_file(filepath, temp_path)
    if success:
        check_res = check_file(temp_path)
        if check_res and check_res["status"] == "PASS":
            if os.path.exists(filepath):
                os.remove(filepath)
            os.rename(temp_path, filepath)
            print(f"Successfully fixed and verified quality for {os.path.basename(filepath)}!")
        else:
            print("Failed verification:")
            for err in check_res.get("errors", []):
                print(f"  - {err}")
            if os.path.exists(temp_path):
                os.remove(temp_path)
    else:
        print(f"Failed to fix {os.path.basename(filepath)}")

def main():
    ko_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "books", "secret_garden", "final_audio_ko"))
    
    track28_path = os.path.join(ko_dir, "final_track_28.mp3")
    sample_path = os.path.join(ko_dir, "sample.mp3")
    
    fix_track(track28_path)
    fix_track(sample_path)

if __name__ == "__main__":
    main()
