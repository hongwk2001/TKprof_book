import os
import sys
import numpy as np
import soundfile as sf
import subprocess

try:
    from kokoro import KPipeline
except ImportError:
    print("Could not import kokoro. Make sure it is installed.")
    sys.exit(1)

SAMPLE_RATE = 24000
VOICE = "am_michael"

def render_kokoro(text, voice):
    lang_code = 'a'
    pipeline = KPipeline(lang_code=lang_code)
    # The pipeline can handle longer texts if we pass them in.
    # We might need to split by double newlines if it's too long for the model?
    # Actually KPipeline handles text chunking internally.
    generator = pipeline(text, voice=voice, speed=1)
    
    audio_segments = []
    # Add a brief pause at the beginning
    audio_segments.append(np.zeros(int(SAMPLE_RATE * 1.0)))
    
    for gs, ps, audio in generator:
        if audio is not None and len(audio) > 0:
            audio_segments.append(audio)
            # Add a brief pause after each chunk
            audio_segments.append(np.zeros(int(SAMPLE_RATE * 0.5)))
            
    if audio_segments:
        return np.concatenate(audio_segments)
    return None

def process_file(txt_file, mp3_file):
    if not os.path.exists(txt_file):
        print(f"File {txt_file} not found.")
        return

    with open(txt_file, 'r', encoding='utf-8') as f:
        text = f.read()

    print(f"Rendering {txt_file} with {VOICE}...")
    audio = render_kokoro(text, VOICE)

    if audio is not None:
        temp_wav = mp3_file.replace(".mp3", ".wav")
        sf.write(temp_wav, audio, SAMPLE_RATE)
        
        # Convert to MP3
        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-i", temp_wav,
            "-codec:a", "libmp3lame",
            "-b:a", "128k",
            mp3_file
        ]
        
        try:
            subprocess.run(ffmpeg_cmd, check=True, capture_output=True)
            print(f"Successfully generated {mp3_file}")
            os.remove(temp_wav)
        except Exception as e:
            print(f"Failed to convert to mp3: {e}")
    else:
        print(f"Audio rendering failed for {txt_file}.")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    audio_dir = os.path.join(base_dir, "audio_archive")
    os.makedirs(audio_dir, exist_ok=True)
    
    intro_txt = os.path.join(base_dir, "introduction_en.txt")
    intro_mp3 = os.path.join(audio_dir, "introduction_en.mp3")
    
    copy_txt = os.path.join(base_dir, "copyright_en.txt")
    copy_mp3 = os.path.join(audio_dir, "copyright_en.mp3")
    
    process_file(intro_txt, intro_mp3)
    process_file(copy_txt, copy_mp3)
