import os
import sys
import json
import subprocess
import time
from pydub import AudioSegment

# Force UTF-8 stdout
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FINAL_DIR = os.path.join(BASE_DIR, "final_audio_ko")
TEMP_DIR = os.path.join(BASE_DIR, "temp_audio_ko")
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts_ko")

os.makedirs(FINAL_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

def run_cmd(cmd):
    attempts = 0
    while attempts < 3:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                return True
            print(f"Error executing command (attempt {attempts+1}):\n{result.stderr}")
        except subprocess.TimeoutExpired:
            print(f"Timeout expired for command (attempt {attempts+1}). Retrying...")
        attempts += 1
        time.sleep(2)
    return False

def generate_tts_segment(text, voice, speed, out_file):
    # Convert speed float (e.g. 1.05) to edge-tts rate string (e.g. "+5%")
    rate_percent = int(round((speed - 1.0) * 100))
    rate_str = f"{rate_percent:+d}%"
    
    cmd = ["edge-tts", "--text", text, "--voice", voice, f"--rate={rate_str}", "--write-media", out_file]
    return run_cmd(cmd)

def generate_single_file(text_file, out_file, voice="ko-KR-SunHiNeural"):
    if not os.path.exists(text_file):
        print(f"Skipping {text_file}, not found.")
        return False
    # If file exists, skip
    if os.path.exists(out_file):
        print(f"Skipping single file {out_file} (already generated)")
        return True
    with open(text_file, 'r', encoding='utf-8') as f:
        text = f.read().strip()
    return generate_tts_segment(text, voice, 1.0, out_file)

def generate_chapter(ch_num_str):
    track_num = int(ch_num_str) + 1
    out_mp3 = os.path.join(FINAL_DIR, f"final_track_{track_num:02d}.mp3")
    if os.path.exists(out_mp3):
        print(f"Skipping Chapter {ch_num_str} (already generated: {out_mp3})")
        return True
        
    script_path = os.path.join(SCRIPTS_DIR, f"script_ch_{ch_num_str}.json")
    if not os.path.exists(script_path):
        print(f"Script {script_path} not found.")
        return False
        
    with open(script_path, 'r', encoding='utf-8') as f:
        segments = json.load(f)
        
    print(f"Generating Chapter {ch_num_str} ({len(segments)} segments)...")
    
    final_audio = AudioSegment.empty()
    
    for i, seg in enumerate(segments):
        voice = seg["voice"]
        speed = seg["speed"]
        text = seg["text"]
        
        temp_mp3 = os.path.join(TEMP_DIR, f"seg_{i}_ko.mp3")
        
        if generate_tts_segment(text, voice, speed, temp_mp3):
            seg_audio = AudioSegment.from_mp3(temp_mp3)
            final_audio += seg_audio
            
            # 500ms pacing silence between narration/dialogue blocks
            final_audio += AudioSegment.silent(duration=500)
            
            try:
                os.remove(temp_mp3)
            except OSError:
                pass
        else:
            print(f"Warning: Failed to synthesize segment {i}")
            
    track_num = int(ch_num_str) + 1
    out_mp3 = os.path.join(FINAL_DIR, f"final_track_{track_num:02d}.mp3")
    
    print(f"Exporting {out_mp3}...")
    final_audio.export(out_mp3, format="mp3", bitrate="256k", parameters=["-ar", "44100"])
    print(f"Chapter {ch_num_str} complete!")
    return True

def main():
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "intro_outro":
            print("Generating Intro, Overview, and Closing tracks...")
            generate_single_file(os.path.join(BASE_DIR, "introduction_ko.txt"), os.path.join(FINAL_DIR, "final_track_00_intro.mp3"))
            generate_single_file(os.path.join(BASE_DIR, "overview_ko.txt"), os.path.join(FINAL_DIR, "final_track_01.mp3"))
            generate_single_file(os.path.join(BASE_DIR, "copyright_ko.txt"), os.path.join(FINAL_DIR, "closing.mp3"))
        else:
            ch_num = arg
            generate_chapter(ch_num.zfill(2))
    else:
        # Generate intro/overview
        print("Generating Intro and Overview...")
        generate_single_file(os.path.join(BASE_DIR, "introduction_ko.txt"), os.path.join(FINAL_DIR, "final_track_00_intro.mp3"))
        generate_single_file(os.path.join(BASE_DIR, "overview_ko.txt"), os.path.join(FINAL_DIR, "final_track_01.mp3"))
        
        # Generate all 27 chapters
        for i in range(1, 28):
            generate_chapter(f"{i:02d}")
            
        # Generate closing
        print("Generating Closing Track...")
        generate_single_file(os.path.join(BASE_DIR, "copyright_ko.txt"), os.path.join(FINAL_DIR, "closing.mp3"))
            
        # Generate the retail sample.mp3 from Chapter 1 (final_track_02.mp3)
        print("Generating Sample Track (sample.mp3)...")
        ch1_path = os.path.join(FINAL_DIR, "final_track_02.mp3")
        sample_out = os.path.join(FINAL_DIR, "sample.mp3")
        if os.path.exists(ch1_path):
            ch1_audio = AudioSegment.from_mp3(ch1_path)
            # Limit duration to 4m 30s (270000 ms)
            sample_audio = ch1_audio[:270000]
            sample_audio.export(sample_out, format="mp3", bitrate="256k", parameters=["-ar", "44100"])
            print(f"Sample exported to {sample_out}")

if __name__ == "__main__":
    main()
