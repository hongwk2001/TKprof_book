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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts_en")
FINAL_DIR = os.path.join(BASE_DIR, "final_audio")
TEMP_DIR = os.path.join(BASE_DIR, "temp_audio")

os.makedirs(FINAL_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

SAMPLE_RATE = 24000

# Voices prefixed 'a' (af_/am_) are American; 'b' (bf_/bm_) are British.
# Each Kokoro pipeline is tied to one language's g2p rules, so we need one per prefix.
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
    script_path = os.path.join(SCRIPTS_DIR, f"script_ch_{ch_num_str}.json")
    if not os.path.exists(script_path):
        print(f"Script {script_path} not found.")
        return False
        
    with open(script_path, 'r', encoding='utf-8') as f:
        segments = json.load(f)
        
    print(f"Generating Chapter {ch_num_str} ({len(segments)} segments)...")
    
    # Store generated pydub AudioSegments
    final_audio = AudioSegment.empty()
    
    for i, seg in enumerate(segments):
        char = seg["character"]
        voice = seg["voice"]
        speed = seg["speed"]
        text = seg["text"]
        
        # Temp wav file for this segment
        temp_wav = os.path.join(TEMP_DIR, f"seg_{i}.wav")
        
        if synthesize_segment(text, voice, speed, temp_wav):
            seg_audio = AudioSegment.from_wav(temp_wav)
            
            # Append to final audio
            final_audio += seg_audio
            
            # Use exactly 500ms dynamic gap as per the Authors Republic specs
            gap_ms = 500
            final_audio += AudioSegment.silent(duration=gap_ms)
            
            try:
                os.remove(temp_wav)
            except OSError as e:
                print(f"Warning: could not remove {temp_wav}: {e}")
        else:
            print(f"Warning: Failed to synthesize segment {i} ({char})")
            
    # Export final mp3
    # Note: Chapter 1 is saved as final_track_02.mp3 per typical audiobook numbering (Chapter 0/Intro is 01)
    track_num = int(ch_num_str) + 1
    out_mp3 = os.path.join(FINAL_DIR, f"final_track_{track_num:02d}.mp3")
    
    print(f"Exporting {out_mp3}...")
    final_audio.export(out_mp3, format="mp3", bitrate="256k", parameters=["-ar", "44100"])
    print(f"Chapter {ch_num_str} complete!")
    return True

def generate_single_file(text_file, out_file, voice="af_heart"):
    if not os.path.exists(text_file):
        print(f"Skipping {text_file}, not found.")
        return False
    with open(text_file, 'r', encoding='utf-8') as f:
        text = f.read().strip()
    print(f"Generating single file from {text_file}...")
    temp_wav = os.path.join(TEMP_DIR, "temp_single.wav")
    if synthesize_segment(text, voice, 1.0, temp_wav):
        seg_audio = AudioSegment.from_wav(temp_wav)
        seg_audio.export(out_file, format="mp3", bitrate="256k", parameters=["-ar", "44100"])
        try:
            os.remove(temp_wav)
        except OSError:
            pass
        return True
    return False

def main():
    import sys
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
        
        # Generate all chapters
        for i in range(1, 23):
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
