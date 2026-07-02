import os
import glob
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")
OUTPUT_DIR = os.path.join(BASE_DIR, "final_audio")

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def main():
    # Find all chapter files
    chapter_files = glob.glob(os.path.join(CHAPTERS_DIR, "ch_*.txt"))
    chapter_files.sort()
    
    if not chapter_files:
        print("No chapters found in", CHAPTERS_DIR)
        return
        
    print(f"Found {len(chapter_files)} chapters to generate.")
    
    for txt_path in chapter_files:
        filename = os.path.basename(txt_path)
        base_name = os.path.splitext(filename)[0]
        
        # Output mp3 file name
        out_mp3 = os.path.join(OUTPUT_DIR, f"{base_name}.mp3")
        
        print(f"Generating audio for {filename} -> {os.path.basename(out_mp3)}...")
        
        # Run edge-tts command
        cmd = [
            "edge-tts",
            "--voice", "en-US-SteffanNeural",
            "--file", txt_path,
            "--write-media", out_mp3
        ]
        
        try:
            subprocess.run(cmd, check=True)
            print(f"Successfully generated {out_mp3}")
        except subprocess.CalledProcessError as e:
            print(f"Error generating audio for {filename}: {e}")

if __name__ == "__main__":
    main()
