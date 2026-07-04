import os
import subprocess
import glob

BASE_DIR = r"/mnt/d/git_repo/TKprof_book/books/meditations"
# The bumper file is shared, so we point to the prince folder for the mp3
BUMPER_FILE = r"/mnt/d/git_repo/TKprof_book/books/the_prince/lordsonny-cinematic-hit-159487.mp3"
TEMP_DIR = os.path.join(BASE_DIR, "temp_audio")
FINAL_DIR = os.path.join(BASE_DIR, "final_audio")
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(FINAL_DIR, exist_ok=True)

VOICE = "en-GB-RyanNeural"

def run_cmd(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error executing command:\n{result.stderr}")
        raise Exception(f"Command failed: {cmd}")

def generate_tts(text_file, out_file):
    if not os.path.exists(text_file):
        print(f"Skipping {text_file}, not found.")
        return False
    
    cmd = f"edge-tts --file '{text_file}' --voice {VOICE} --write-media '{out_file}'"
    run_cmd(cmd)
    return True

def mix_audio(bumper, raw_audio, out_file, bumper_duration, add_full_outro=False):
    # Trim the bumper to bumper_duration
    trimmed_bumper = os.path.join(TEMP_DIR, "trimmed_bumper.mp3")
    run_cmd(f"ffmpeg -y -t {bumper_duration} -i '{bumper}' '{trimmed_bumper}' -loglevel error")
    
    # Use filter_complex to concatenate, which automatically handles mismatched sample rates/channels
    inputs = f"-i '{trimmed_bumper}' -i '{raw_audio}'"
    filter_str = "[0:a]volume=0.2[b0];[b0][1:a]concat=n=2:v=0:a=1[outa]"
    if add_full_outro:
        inputs += f" -i '{bumper}'"
        filter_str = "[0:a]volume=0.2[b0];[2:a]volume=0.2[b2];[b0][1:a][b2]concat=n=3:v=0:a=1[outa]"
    
    cmd = f"ffmpeg -y {inputs} -filter_complex '{filter_str}' -map '[outa]' '{out_file}' -loglevel error"
    run_cmd(cmd)

def main():
    # 1. Generate Intro
    intro_txt = os.path.join(BASE_DIR, "introduction_en.txt")
    intro_raw = os.path.join(TEMP_DIR, "raw_intro.mp3")
    intro_final = os.path.join(FINAL_DIR, "final_track_00_intro.mp3")
    
    print("Generating Intro...")
    if generate_tts(intro_txt, intro_raw):
        mix_audio(BUMPER_FILE, intro_raw, intro_final, bumper_duration=4.5)
        print(f"Finished {intro_final}")

    # 2. Generate Chapters 1 to 12
    for i in range(1, 13):
        ch_txt = os.path.join(CHAPTERS_DIR, f"ch_{i:02d}_en.txt")
        ch_raw = os.path.join(TEMP_DIR, f"raw_ch_{i:02d}.mp3")
        ch_final = os.path.join(FINAL_DIR, f"final_track_{i:02d}.mp3")
        
        print(f"Generating Chapter {i}...")
        if generate_tts(ch_txt, ch_raw):
            add_outro = (i == 12)
            mix_audio(BUMPER_FILE, ch_raw, ch_final, bumper_duration=2.0, add_full_outro=add_outro)
            print(f"Finished {ch_final}")

    print("Audio generation complete.")

if __name__ == "__main__":
    main()
