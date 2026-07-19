import os
import sys

# Add root folder to path so we can import fix_audio_quality
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fix_audio_quality import fix_audio_file
from check_audio_quality import check_file

def main():
    sample_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "books", "secret_garden", "final_audio", "sample.mp3"))
    temp_path = sample_path + ".tmp.mp3"
    print(f"Fixing sample quality: {sample_path} -> {temp_path}")
    
    success = fix_audio_file(sample_path, temp_path)
    if success:
        check_res = check_file(temp_path)
        if check_res and check_res["status"] == "PASS":
            if os.path.exists(sample_path):
                os.remove(sample_path)
            os.rename(temp_path, sample_path)
            print("Successfully fixed and verified sample audio quality!")
        else:
            print("Failed verification:")
            for err in check_res.get("errors", []):
                print(f"  - {err}")
            if os.path.exists(temp_path):
                os.remove(temp_path)
    else:
        print("Failed to run fix_audio_file on sample.")

if __name__ == "__main__":
    main()
