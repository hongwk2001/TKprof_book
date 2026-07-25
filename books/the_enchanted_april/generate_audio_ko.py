import os
import sys
import json
import subprocess
from pydub import AudioSegment

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FINAL_DIR = os.path.join(BASE_DIR, "final_audio_ko")
TEMP_DIR = os.path.join(BASE_DIR, "temp_audio")
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts_ko")

os.makedirs(FINAL_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

def run_cmd(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error executing command:\n{result.stderr}")
        return False
    return True

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
    with open(text_file, 'r', encoding='utf-8') as f:
        text = f.read().strip()
    return generate_tts_segment(text, voice, 1.0, out_file)

def generate_chapter(ch_num_str):
    script_path = os.path.join(SCRIPTS_DIR, f"script_ch_{ch_num_str}.json")
    if not os.path.exists(script_path):
        print(f"Script {script_path} not found.")
        return False
        
    with open(script_path, 'r', encoding='utf-8') as f:
        segments = json.load(f)
        
    print(f"Generating Chapter {ch_num_str} ({len(segments)} segments)...")
    
    final_audio = AudioSegment.empty()
    gap_ms = 500
    
    for i, seg in enumerate(segments):
        voice = "ko-KR-SunHiNeural"
        speed = seg["speed"]
        text = seg["text"]
        
        temp_mp3 = os.path.join(TEMP_DIR, f"seg_{i}_ko.mp3")
        
        if generate_tts_segment(text, voice, speed, temp_mp3):
            seg_audio = AudioSegment.from_mp3(temp_mp3)
            final_audio += seg_audio
            final_audio += AudioSegment.silent(duration=gap_ms)
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
    return True

def main():
    if len(sys.argv) > 1:
        ch_num = sys.argv[1]
        generate_chapter(ch_num.zfill(2))
    else:
        # Generate intro/overview
        print("Generating Intro and Overview...")
        generate_single_file(os.path.join(BASE_DIR, "introduction_ko.txt"), os.path.join(FINAL_DIR, "final_track_00_intro.mp3"))
        generate_single_file(os.path.join(BASE_DIR, "overview_ko.txt"), os.path.join(FINAL_DIR, "final_track_01.mp3"))
        
        # Generate chapters 1-22
        for i in range(1, 23):
            generate_chapter(f"{i:02d}")
            
        # Generate closing
        print("Generating Closing Track...")
        generate_single_file(os.path.join(BASE_DIR, "copyright_ko.txt"), os.path.join(FINAL_DIR, "closing.mp3"))
        
        # Generate Sample
        print("Generating Sample Track...")
        intro_path = os.path.join(FINAL_DIR, "final_track_00_intro.mp3")
        ch1_path = os.path.join(FINAL_DIR, "final_track_02.mp3")
        sample_out = os.path.join(FINAL_DIR, "sample.mp3")
        
        if os.path.exists(intro_path) and os.path.exists(ch1_path):
            sample_audio = AudioSegment.from_mp3(intro_path) + AudioSegment.from_mp3(ch1_path)
            sample_audio = sample_audio[:270000] # 4m 30s max
            sample_audio.export(sample_out, format="mp3", bitrate="256k", parameters=["-ar", "44100"])
            print(f"Sample exported to {sample_out}")

if __name__ == "__main__":
    main()
