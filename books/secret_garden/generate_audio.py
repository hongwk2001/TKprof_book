import os
import sys
import json
import numpy as np
import soundfile as sf
from pydub import AudioSegment
import subprocess

try:
    from kokoro import KPipeline
except ImportError:
    print("Could not import kokoro. Please install it.")
    sys.exit(1)

# Force UTF-8 stdout
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts_en")
FINAL_DIR = os.path.join(BASE_DIR, "final_audio")
TEMP_DIR = os.path.join(BASE_DIR, "temp_audio")

os.makedirs(FINAL_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

SAMPLE_RATE = 24000

VOICE_GAINS = {
    "af_nicole": 5.0,  # Boost quiet voice af_nicole by 5dB
}

# Cache pipeline instances
_pipelines = {}

def get_pipeline(voice):
    lang_code = voice[0]  # 'a' or 'b'
    if lang_code not in _pipelines:
        _pipelines[lang_code] = KPipeline(lang_code=lang_code)
    return _pipelines[lang_code]

def synthesize_segment(text, voice, speed, out_wav):
    pipeline = get_pipeline(voice)
    generator = pipeline(text, voice=voice, speed=speed)
    
    audio_segments = []
    for gs, ps, audio in generator:
        if audio is not None and len(audio) > 0:
            audio_segments.append(audio)
            
    if not audio_segments:
        return False
        
    merged_audio = np.concatenate(audio_segments)
    sf.write(out_wav, merged_audio, SAMPLE_RATE)
    return True

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
        char = seg["character"]
        voice = seg["voice"]
        speed = seg["speed"]
        text = seg["text"]
        
        temp_wav = os.path.join(TEMP_DIR, f"seg_{i}.wav")
        
        if synthesize_segment(text, voice, speed, temp_wav):
            seg_audio = AudioSegment.from_wav(temp_wav)
            gain = VOICE_GAINS.get(voice, 0.0)
            if gain != 0.0:
                seg_audio = seg_audio + gain
            final_audio += seg_audio
            
            # exactly 500ms pacing silence between narration/dialogue blocks
            final_audio += AudioSegment.silent(duration=500)
            
            try:
                os.remove(temp_wav)
            except OSError:
                pass
        else:
            print(f"Warning: Failed to synthesize segment {i} ({char})")
            
    # Chapter 1 is saved as final_track_02.mp3
    track_num = int(ch_num_str) + 1
    out_mp3 = os.path.join(FINAL_DIR, f"final_track_{track_num:02d}.mp3")
    
    print(f"Exporting {out_mp3}...")
    final_audio.export(out_mp3, format="mp3", bitrate="256k", parameters=["-ar", "44100"])
    print(f"Chapter {ch_num_str} complete!")
    return True

def generate_single_file(text_file, out_file, voice="af_sarah"):
    if not os.path.exists(text_file):
        print(f"Skipping {text_file}, not found.")
        return False
    if os.path.exists(out_file):
        print(f"Skipping single file {out_file} (already generated)")
        return True
    with open(text_file, 'r', encoding='utf-8') as f:
        text = f.read().strip()
    print(f"Generating single file from {text_file}...")
    temp_wav = os.path.join(TEMP_DIR, "temp_single.wav")
    if synthesize_segment(text, voice, 1.0, temp_wav):
        seg_audio = AudioSegment.from_wav(temp_wav)
        gain = VOICE_GAINS.get(voice, 0.0)
        if gain != 0.0:
            seg_audio = seg_audio + gain
        seg_audio.export(out_file, format="mp3", bitrate="256k", parameters=["-ar", "44100"])
        try:
            os.remove(temp_wav)
        except OSError:
            pass
        return True
    return False

def main():
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "intro_outro":
            print("Generating Intro, Overview, and Closing tracks...")
            generate_single_file(os.path.join(BASE_DIR, "introduction_en.txt"), os.path.join(FINAL_DIR, "final_track_00_intro.mp3"))
            generate_single_file(os.path.join(BASE_DIR, "overview_en.txt"), os.path.join(FINAL_DIR, "final_track_01.mp3"))
            generate_single_file(os.path.join(BASE_DIR, "copyright_en.txt"), os.path.join(FINAL_DIR, "closing.mp3"))
        else:
            ch_num = arg
            generate_chapter(ch_num.zfill(2))
    else:
        # Generate intro/overview
        print("Generating Intro and Overview...")
        generate_single_file(os.path.join(BASE_DIR, "introduction_en.txt"), os.path.join(FINAL_DIR, "final_track_00_intro.mp3"))
        generate_single_file(os.path.join(BASE_DIR, "overview_en.txt"), os.path.join(FINAL_DIR, "final_track_01.mp3"))
        
        # Generate all 27 chapters
        for i in range(1, 28):
            generate_chapter(f"{i:02d}")
            
        # Generate closing
        print("Generating Closing Track...")
        generate_single_file(os.path.join(BASE_DIR, "copyright_en.txt"), os.path.join(FINAL_DIR, "closing.mp3"))
            
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
