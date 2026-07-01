import os
import json
import subprocess
from pydub import AudioSegment

SCRIPTS_DIR = "scripts"
TEMP_DIR = "temp_audio"
OUTPUT_DIR = "final_audio"

if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def generate_chapter(ch_num):
    script_file = os.path.join(SCRIPTS_DIR, f"script_ch_{ch_num}.json")
    if not os.path.exists(script_file):
        print(f"File not found: {script_file}")
        return
        
    with open(script_file, 'r', encoding='utf-8') as f:
        script = json.load(f)
        
    print(f"Generating audio for Chapter {ch_num} ({len(script)} segments)...")
    
    # 1. Generate all chunks
    audio_segments = []
    for i, segment in enumerate(script):
        text = segment['text']
        voice = segment['voice']
        
        # skip empty
        if not text.strip():
            continue
            
        temp_mp3 = os.path.join(TEMP_DIR, f"ch{ch_num}_{i:03d}.mp3")
        
        # run edge-tts
        cmd = [
            "edge-tts",
            "--voice", voice,
            "--text", text,
            "--write-media", temp_mp3
        ]
        
        if not os.path.exists(temp_mp3):
            subprocess.run(cmd, check=True)
            
        # load back using pydub
        clip = AudioSegment.from_mp3(temp_mp3)
        audio_segments.append(clip)
        
    # 2. Combine chunks with slight pause
    print("Combining segments...")
    combined = AudioSegment.empty()
    short_silence = AudioSegment.silent(duration=300) # 300ms pause between speakers
    
    for clip in audio_segments:
        combined += clip + short_silence
        
    # 3. Add cinematic intro + chime (no Bach bumper)
    print("Adding cinematic intro and chime...")
    cinematic = AudioSegment.from_mp3("freesound_community-cinematic-intro-6097.mp3")
    chime = AudioSegment.from_mp3("chime.mp3")
    
    # Final assembly
    # [Cinematic] -> [Chime] -> [Narration] -> [Chime]
    final_audio = cinematic + AudioSegment.silent(duration=500) + chime + AudioSegment.silent(duration=500) + combined + AudioSegment.silent(duration=500) + chime
    
    out_file = os.path.join(OUTPUT_DIR, f"final_ch_{ch_num}.mp3")
    final_audio.export(out_file, format="mp3")
    print(f"Successfully created {out_file}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        generate_chapter(sys.argv[1])
    else:
        print("Usage: python generate_audio.py <chapter_number>")
