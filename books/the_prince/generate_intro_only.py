import os
import subprocess

BASE_DIR = r"/mnt/d/git_repo/TKprof_book/books/the_prince"
BUMPER_FILE = os.path.join(BASE_DIR, "freesound_community-cinematic-intro-6097.mp3")
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
    fade_start = bumper_duration - 0.5
    run_cmd(f"ffmpeg -y -t {bumper_duration} -i '{bumper}' -af 'afade=t=out:st={fade_start}:d=0.5' '{trimmed_bumper}' -loglevel error")
    
    # Use filter_complex to reduce bumper volume and concatenate, which handles mismatched sample rates
    cmd = f"ffmpeg -y -i '{trimmed_bumper}' -i '{raw_audio}' -filter_complex '[0:a]volume=0.2[b];[b][1:a]concat=n=2:v=0:a=1[outa]' -map '[outa]' '{out_file}' -loglevel error"
    run_cmd(cmd)

def main():
    ch_txt = os.path.join(BASE_DIR, "chapters", "ch_01_en.txt")
    ch_raw = os.path.join(TEMP_DIR, "raw_ch_01.mp3")
    ch_final = os.path.join(FINAL_DIR, "final_track_01.mp3")
    
    print("Generating Chapter 1 only...")
    generate_tts(ch_txt, ch_raw)
    mix_audio(BUMPER_FILE, ch_raw, ch_final, bumper_duration=2.0)
    print(f"Finished {ch_final}")

if __name__ == "__main__":
    main()
