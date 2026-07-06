import os
import sys
import numpy as np
import soundfile as sf
import subprocess

try:
    from kokoro import KPipeline
except ImportError:
    print("Could not import kokoro.")
    sys.exit(1)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLES_DIR = os.path.join(BASE_DIR, "samples")
os.makedirs(SAMPLES_DIR, exist_ok=True)

SAMPLE_RATE = 24000

VOICES = {
    "af_bella": "Bella (American Female)",
    "af_sarah": "Sarah (American Female)",
    "am_adam": "Adam (American Male)",
    "am_michael": "Michael (American Male)",
    "bf_emma": "Emma (British Female)",
    "bm_george": "George (British Male)",
}

def generate_sample(voice_id, voice_name):
    # 'a' for American English, 'b' for British English
    lang_code = 'b' if voice_id.startswith('b') else 'a'
    pipeline = KPipeline(lang_code=lang_code)
    
    text = f"Beowulf. This is a sample of the Kokoro voice, {voice_name}. You are about to step into the oldest and most brutal legend in the history of Western literature."
    
    print(f"Generating sample for {voice_id} ({voice_name})...")
    generator = pipeline(text, voice=voice_id, speed=1)
    
    audio_segments = []
    for gs, ps, audio in generator:
        if audio is not None and len(audio) > 0:
            audio_segments.append(audio)
            
    if audio_segments:
        merged_audio = np.concatenate(audio_segments)
        wav_path = os.path.join(SAMPLES_DIR, f"{voice_id}.wav")
        mp3_path = os.path.join(SAMPLES_DIR, f"{voice_id}.mp3")
        
        # Save WAV
        sf.write(wav_path, merged_audio, SAMPLE_RATE)
        
        # Convert to MP3
        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-i", wav_path,
            "-codec:a", "libmp3lame",
            "-b:a", "256k",
            mp3_path
        ]
        try:
            subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"Generated {mp3_path}")
            os.remove(wav_path)
        except Exception as e:
            print(f"Error converting {voice_id} to MP3: {e}")
    else:
        print(f"Failed to generate audio for {voice_id}")

if __name__ == "__main__":
    for vid, vname in VOICES.items():
        generate_sample(vid, vname)
    print("All samples generated successfully.")
