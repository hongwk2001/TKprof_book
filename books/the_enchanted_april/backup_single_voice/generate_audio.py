import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FINAL_DIR = os.path.join(BASE_DIR, "final_audio")
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")

os.makedirs(FINAL_DIR, exist_ok=True)

VOICE = "en-GB-RyanNeural"

def run_cmd(cmd):
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error executing command:\n{result.stderr}")
        raise Exception(f"Command failed: {cmd}")

def generate_tts(text_file, out_file):
    if not os.path.exists(text_file):
        print(f"Skipping {text_file}, not found.")
        return False
    
    cmd = ["edge-tts", "--file", text_file, "--voice", VOICE, "--write-media", out_file]
    run_cmd(cmd)
    return True

def main():
    # 1. Generate Intro (Short Credits)
    intro_txt = os.path.join(BASE_DIR, "introduction_en.txt")
    intro_final = os.path.join(FINAL_DIR, "final_track_00_intro.mp3")
    
    print("Generating Intro...")
    if generate_tts(intro_txt, intro_final):
        print(f"Finished {intro_final}")

    # 1b. Generate Overview (Introduction Content)
    overview_txt = os.path.join(BASE_DIR, "overview_en.txt")
    overview_final = os.path.join(FINAL_DIR, "final_track_01.mp3")
    
    print("Generating Overview...")
    if generate_tts(overview_txt, overview_final):
        print(f"Finished {overview_final}")

    # 2. Generate Chapters 1 to 22
    for i in range(1, 23):
        ch_txt = os.path.join(CHAPTERS_DIR, f"ch_{i:02d}_en.txt")
        # Shift output chapter files down by 1 (e.g. ch 1 -> track 02)
        ch_final = os.path.join(FINAL_DIR, f"final_track_{i+1:02d}.mp3")
        
        print(f"Generating Chapter {i} (saved as track {i+1})...")
        if generate_tts(ch_txt, ch_final):
            print(f"Finished {ch_final}")

    # 3. Generate Closing Track
    closing_txt = os.path.join(BASE_DIR, "copyright_en.txt")
    closing_final = os.path.join(FINAL_DIR, "closing.mp3")
    
    print("Generating Closing Track...")
    if generate_tts(closing_txt, closing_final):
        print(f"Finished {closing_final}")

    # 4. Generate Sample Track (Intro + Chapter 1, cut to < 5 mins)
    sample_final = os.path.join(FINAL_DIR, "sample.mp3")
    print("Generating Sample Track...")
    sample_cmd = [
        "ffmpeg", "-y",
        "-i", intro_final,
        "-i", os.path.join(FINAL_DIR, "final_track_02.mp3"),
        "-filter_complex", "[0:a][1:a]concat=n=2:v=0:a=1[outa]",
        "-map", "[outa]",
        "-t", "270", # Limit duration to 4m 30s (under 5 minutes)
        "-ar", "44100",
        "-b:a", "256k",
        sample_final,
        "-loglevel", "error"
    ]
    run_cmd(sample_cmd)
    print(f"Finished {sample_final}")

    print("Audio generation complete.")

if __name__ == "__main__":
    main()
