import os
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def run_step(name, cmd, cwd=SCRIPT_DIR):
    print("=" * 60)
    print(f"Running Step: {name}")
    print(f"Command: {cmd}")
    print("=" * 60)
    
    # Run the command using the active python or system command
    result = subprocess.run(cmd, shell=True, cwd=cwd)
    if result.returncode != 0:
        print(f"Error: Step '{name}' failed with exit code {result.returncode}")
        sys.exit(result.returncode)
    print(f"Step '{name}' completed successfully.\n")

def main():
    # Step 1: Dialogue Tagging
    run_step("Dialogue Tagging (Gemini-2.5-flash)", "python tag_dialogue_ko.py")
    
    # Step 2: Script Preparation
    run_step("Script JSON Preparation", "python prepare_scripts_ko.py")
    
    # Step 3: Audio Generation (edge-tts)
    run_step("Audio Generation", "python generate_audio_ko.py")
    
    # Step 4: Merging Audio Parts via ffmpeg
    print("=" * 60)
    print("Merging Audio Tracks into 4 Parts using ffmpeg")
    print("=" * 60)
    
    base_audio_dir = os.path.join(SCRIPT_DIR, "final_audio_ko")
    merged_dir = os.path.join(base_audio_dir, "merged")
    os.makedirs(merged_dir, exist_ok=True)
    
    for i in range(1, 5):
        list_file = f"part{i}_ko_list.txt"
        output_file = os.path.join("merged", f"beowulf_ko_part{i}.mp3")
        
        # We run the command inside the final_audio_ko directory so the relative paths in list files work
        cmd = f"ffmpeg -y -f concat -safe 0 -i {list_file} -c copy {output_file}"
        print(f"Merging Part {i}...")
        result = subprocess.run(cmd, shell=True, cwd=base_audio_dir)
        if result.returncode != 0:
            print(f"Error: Failed to merge Part {i}")
            sys.exit(result.returncode)
            
    print("Pipeline completed successfully!")

if __name__ == "__main__":
    main()
