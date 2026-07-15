import os
import sys
import json
import asyncio
import re
import subprocess
from io import BytesIO
import edge_tts
from pydub import AudioSegment

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(SCRIPT_DIR, "scripts")
TEMP_DIR = os.path.join(SCRIPT_DIR, "temp_audio")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "final_audio")

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Voice mapping based on approved plan (4 Male Voices, default speed/pitch)
VOICES = {
    "Narrator": "en-US-AndrewNeural",
    "odysseus": "en-US-BrianNeural",
    "telemachus": "en-US-ChristopherNeural",
    "others": "en-US-EricNeural"
}

async def synthesize_segment(text, voice):
    # No rate/pitch change, default values
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

def apply_post_processing(raw_path, clean_path, bitrate=256):
    """
    Apply standard ffmpeg post-processing to clean and normalize the audio
    to conform to ACX/Authors Republic standards.
    """
    # Volume normalization (RMS target -19 LUFS, true peak -3.5 dB)
    volume_norm = "loudnorm=I=-19:TP=-3.5:LRA=11"
    
    # Strip existing silences at start and end
    strip_silence = "silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0,areverse,silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0,areverse"
    
    # Add leading silence (2.0s = 2000ms)
    leading_silence = "adelay=2000|2000"
    
    # Add trailing silence (2.0s)
    trailing_silence = "apad=pad_dur=2"
    
    filter_chain = f"{strip_silence},{volume_norm},{leading_silence},{trailing_silence}"
    
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
    script_file = os.path.join(SCRIPTS_DIR, f"script_ch_{ch_str}.json")
    
    raw_file = os.path.join(TEMP_DIR, f"raw_ch_{ch_str}.mp3")
    final_file = os.path.join(OUTPUT_DIR, f"final_track_{ch_str}.mp3")

    if not os.path.exists(script_file):
        print(f"Script file not found: {script_file}")
        return False

    print(f"Generating audio for Chapter {ch_num} from {script_file}...")

    with open(script_file, 'r', encoding='utf-8') as f:
        script = json.load(f)

    combined_audio = AudioSegment.empty()
    prev_role = None

    for i, segment in enumerate(script):
        text = segment['text'].strip()
        role = segment.get('character', 'Narrator')
        
        # Skip headers or empty segments
        if not text or not re.search(r'[a-zA-Z0-9]', text):
            continue

        voice = VOICES.get(role, VOICES["Narrator"])

        # Add pause before this segment if there was a previous segment (500ms)
        if prev_role is not None:
            combined_audio += AudioSegment.silent(duration=500)

        print(f"  Segment {i + 1}/{len(script)} ({role} - {voice}): {text[:40]}...")
        segment_audio = await synthesize_segment(text, voice)
        combined_audio += segment_audio
        prev_role = role

    # Set frame rate to 44.1kHz and convert to stereo
    combined_audio = combined_audio.set_frame_rate(44100).set_channels(2)

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
        print("Usage: python generate_audio.py <chapter_number|all>")
        sys.exit(1)
        
    arg = sys.argv[1].lower()
    if arg == "all":
        for ch in range(1, 25):
            success = await generate_chapter(ch)
            if not success:
                print(f"Failed to generate chapter {ch}")
                sys.exit(1)
    else:
        ch_num = int(arg)
        success = await generate_chapter(ch_num)
        if not success:
            sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())
