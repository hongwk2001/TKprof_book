import os
import subprocess

BASE_DIR = r"/mnt/d/git_repo/TKprof_book/books/the_prince"
BUMPER_FILE = os.path.join(BASE_DIR, "lordsonny-cinematic-hit-159487.mp3")
TEMP_DIR = os.path.join(BASE_DIR, "temp_audio")
FINAL_DIR = os.path.join(BASE_DIR, "final_audio")

VOICE = "en-GB-RyanNeural"

def run_cmd(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error executing command:\n{result.stderr}")
        raise Exception(f"Command failed: {cmd}")

def generate_tts(text_file, out_file):
    cmd = f"edge-tts --file '{text_file}' --voice {VOICE} --write-media '{out_file}'"
    run_cmd(cmd)
    return True

def mix_audio(bumper, raw_audio, out_file, bumper_duration):
    trimmed_bumper = os.path.join(TEMP_DIR, "trimmed_bumper.mp3")
    run_cmd(f"ffmpeg -y -t {bumper_duration} -i '{bumper}' '{trimmed_bumper}' -loglevel error")
    
    # Use filter_complex to concatenate, which automatically handles mismatched sample rates/channels
    cmd = f"ffmpeg -y -i '{trimmed_bumper}' -i '{raw_audio}' -filter_complex '[0:a][1:a]concat=n=2:v=0:a=1[outa]' -map '[outa]' '{out_file}' -loglevel error"
    run_cmd(cmd)

def main():
    intro_txt = os.path.join(BASE_DIR, "introduction_en.txt")
    intro_raw = os.path.join(TEMP_DIR, "raw_intro.mp3")
    intro_final = os.path.join(FINAL_DIR, "final_track_00_intro.mp3")
    
    print("Generating Intro only...")
    generate_tts(intro_txt, intro_raw)
    mix_audio(BUMPER_FILE, intro_raw, intro_final, bumper_duration=4.5)
    print(f"Finished {intro_final}")

if __name__ == "__main__":
    main()
