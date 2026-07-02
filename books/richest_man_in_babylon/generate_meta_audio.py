import os
import json
import subprocess
from pydub import AudioSegment

TEMP_DIR = "temp_audio"
OUTPUT_DIR = "final_audio"

if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def generate_meta(name):
    script_file = os.path.join("scripts", f"script_{name}.json")
    if not os.path.exists(script_file):
        print(f"File not found: {script_file}")
        return
        
    with open(script_file, 'r', encoding='utf-8') as f:
        script = json.load(f)
        
    print(f"Generating audio for {name} ({len(script)} segments)...")
    
    audio_segments = []
    for i, segment in enumerate(script):
        text = segment['text']
        voice = segment['voice']
        
        if not text.strip():
            continue
            
        temp_mp3 = os.path.join(TEMP_DIR, f"{name}_{i:03d}.mp3")
        
        cmd = [
            "edge-tts",
            "--voice", voice,
            "--text", text,
            "--write-media", temp_mp3
        ]
        
        if not os.path.exists(temp_mp3):
            subprocess.run(cmd, check=True)
            
        clip = AudioSegment.from_mp3(temp_mp3)
        audio_segments.append(clip)
        
    print("Combining segments...")
    combined = AudioSegment.empty()
    short_silence = AudioSegment.silent(duration=300)
    
    for clip in audio_segments:
        combined += clip + short_silence
        
    out_file = os.path.join(OUTPUT_DIR, f"final_{name}.mp3")
    
    # We will just save the combined narration without the cinematic intro
    # since it's just meta text (copyright / intro)
    combined.export(out_file, format="mp3")
    print(f"Successfully created {out_file}")

if __name__ == "__main__":
    generate_meta("intro")
    generate_meta("copyright")
