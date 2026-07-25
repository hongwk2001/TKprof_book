import os
import sys
import json
import re
import asyncio
import subprocess
from io import BytesIO
from pydub import AudioSegment
import edge_tts

# AudioSegment needs ffmpeg path
AudioSegment.converter = "ffmpeg"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
TEMP_DIR = os.path.join(BASE_DIR, "temp_audio")
OUTPUT_DIR = os.path.join(BASE_DIR, "final_audio")

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Voice casting for Korean: male only, using the 2 available male neural voices
VOICES = {
    "Narrator": "ko-KR-InJoonNeural",
    "odysseus": "ko-KR-HyunsuMultilingualNeural",
    "telemachus": "ko-KR-InJoonNeural",
    "others": "ko-KR-HyunsuMultilingualNeural"
}

async def synthesize_segment(text, voice, sem):
    async with sem:
        for attempt in range(5):
            try:
                communicate = edge_tts.Communicate(text, voice)
                audio_data = b""
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        audio_data += chunk["data"]
                if audio_data:
                    return AudioSegment.from_file(BytesIO(audio_data), format="mp3")
            except Exception as e:
                print(f"      Attempt {attempt + 1} failed for voice {voice}: {e}")
                await asyncio.sleep(2)
        raise RuntimeError(f"Failed to synthesize segment after 5 attempts: text={text[:20]}...")

def strip_silence_pydub(audio_segment, silence_thresh=-50, chunk_size=10):
    """
    Strip leading and trailing silence from an AudioSegment.
    """
    # Detect leading silence
    start_trim = 0
    while start_trim < len(audio_segment) and audio_segment[start_trim:start_trim+chunk_size].dBFS < silence_thresh:
        start_trim += chunk_size
        
    # Detect trailing silence
    end_trim = len(audio_segment)
    while end_trim > start_trim and audio_segment[end_trim-chunk_size:end_trim].dBFS < silence_thresh:
        end_trim -= chunk_size
        
    return audio_segment[start_trim:end_trim]

def apply_post_processing(raw_path, clean_path, bitrate=256):
    """
    Apply standard ffmpeg post-processing to clean and normalize the audio
    to conform to ACX/Authors Republic standards.
    """
    # Volume normalization (RMS target -19 LUFS, true peak -3.5 dB)
    volume_norm = "loudnorm=I=-19:TP=-3.5:LRA=11"
    
    # Add leading silence (2.0s = 2000ms)
    leading_silence = "adelay=2000|2000"
    
    # Add trailing silence (2.0s)
    trailing_silence = "apad=pad_dur=2"
    
    filter_chain = f"{volume_norm},{leading_silence},{trailing_silence}"
    
    cmd = [
        "ffmpeg", "-y", "-i", raw_path,
        "-af", filter_chain,
        "-ar", "44100",
        "-b:a", f"{bitrate}k",
        clean_path
    ]
    
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg post-processing failed:\n{e.stderr}", file=sys.stderr)
        return False

async def generate_chapter(ch_num):
    ch_str = str(ch_num).zfill(2)
    script_file = os.path.join(SCRIPTS_DIR, f"script_ch_{ch_str}_ko.json")
    
    raw_file = os.path.join(TEMP_DIR, f"raw_ch_ko_{ch_str}.mp3")
    final_file = os.path.join(OUTPUT_DIR, f"final_track_ko_{ch_str}.mp3")

    if os.path.exists(final_file):
        print(f"Chapter {ch_num} (Korean) already exists: {final_file}. Skipping.")
        return True

    if not os.path.exists(script_file):
        print(f"Script file not found: {script_file}")
        return False

    # Check if raw file already exists, skip synthesis
    if os.path.exists(raw_file):
        print(f"Raw audio track already exists: {raw_file}. Skipping synthesis, running post-processing directly...")
    else:
        print(f"Generating audio for Chapter {ch_num} (Korean) from {script_file}...")

        with open(script_file, 'r', encoding='utf-8') as f:
            script = json.load(f)

        # Pre-synthesize all segments in parallel using a semaphore to limit concurrency
        sem = asyncio.Semaphore(15)
        tasks = []
        
        for i, segment in enumerate(script):
            text = segment['text'].strip()
            role = segment.get('character', 'Narrator')
            
            # Skip headers or empty segments
            if not text or not re.search(r'[a-zA-Z0-9ㄱ-ㅎㅏ-ㅣ가-힣]', text):
                async def dummy(): return None
                tasks.append(dummy())
                continue

            voice = VOICES.get(role, VOICES["Narrator"])
            tasks.append(synthesize_segment(text, voice, sem))

        print(f"  Synthesizing {len(script)} segments concurrently...")
        results = await asyncio.gather(*tasks)

        combined_audio = AudioSegment.empty()
        prev_role = None

        for i, segment in enumerate(script):
            segment_audio = results[i]
            if segment_audio is None:
                continue
                
            role = segment.get('character', 'Narrator')
            if prev_role is not None:
                combined_audio += AudioSegment.silent(duration=500)
                
            combined_audio += segment_audio
            prev_role = role

        # Set frame rate to 44.1kHz and convert to stereo
        combined_audio = combined_audio.set_frame_rate(44100).set_channels(2)

        # Strip leading and trailing silences natively in Python to avoid FFmpeg reversing memory limits
        print("  Trimming leading/trailing silences in Python...")
        combined_audio = strip_silence_pydub(combined_audio)

        # Export raw MP3
        combined_audio.export(raw_file, format="mp3", bitrate="256k")
        print(f"Successfully generated raw audio track: {raw_file}")

    # Apply quality normalization and padding
    print("Applying quality post-processing...")
    if apply_post_processing(raw_file, final_file):
        print(f"Final track saved to: {final_file}")
        try:
            os.remove(raw_file)
        except OSError:
            pass
        return True
    return False

async def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_audio_ko.py <chapter_number|all>")
        sys.exit(1)

    arg = sys.argv[1].lower()
    if arg == "all":
        for ch in range(1, 25):
            success = await generate_chapter(ch)
            if not success:
                print(f"Failed to generate chapter {ch}")
                sys.exit(1)
    else:
        try:
            ch = int(arg)
            if 1 <= ch <= 24:
                success = await generate_chapter(ch)
                if not success:
                    sys.exit(1)
            else:
                print("Chapter number must be between 1 and 24")
                sys.exit(1)
        except ValueError:
            print("Invalid argument. Pass a number between 1 and 24, or 'all'.")
            sys.exit(1)

if __name__ == "__main__":
    # Standard fix for event loop policy on Windows
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
