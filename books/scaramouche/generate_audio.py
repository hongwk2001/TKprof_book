import os
import sys
import json
import asyncio
import re
from io import BytesIO
import edge_tts
from pydub import AudioSegment

# Force UTF-8 encoding for stdout and stderr to prevent UnicodeEncodeError on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CHAPTERS_DIR = os.path.join(SCRIPT_DIR, "chapters")
TEMP_DIR = os.path.join(SCRIPT_DIR, "temp_audio")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "final_audio")

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Voice configuration mapping for Scaramouche roles
VOICES = {
    "en": {
        "Narrator": "en-US-AndrewNeural",
        "Male": "en-US-BrianNeural",
        "Female": "en-US-EmmaNeural",
        "Child": "en-US-AnaNeural"
    },
    "ko": {
        "Narrator": "ko-KR-SunHiNeural",
        "Male": "ko-KR-HyunsuMultilingualNeural",
        "Female": "ko-KR-SunHiNeural",
        "Child": "ko-KR-SunHiNeural"
    }
}

# Speed configuration mapping
SPEEDS = {
    "en": {
        "Narrator": "+0%",
        "Male": "+2%",
        "Female": "+2%",
        "Child": "+4%"
    },
    "ko": {
        "Narrator": "+0%",
        "Male": "+2%",
        "Female": "+3%",
        "Child": "+5%"
    }
}

async def synthesize_segment(text, voice, speed):
    for attempt in range(5):
        try:
            communicate = edge_tts.Communicate(text, voice, rate=speed)
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

async def generate_chapter(lang, ch_num):
    ch_str = str(ch_num).zfill(2)
    script_filename = f"ch_{ch_str}_{lang}.json"
    script_file = os.path.join(CHAPTERS_DIR, script_filename)
    
    out_filename = f"track_{ch_str}_{lang}.mp3"
    out_file = os.path.join(OUTPUT_DIR, out_filename)

    if not os.path.exists(script_file):
        print(f"Script file not found: {script_file}")
        return False

    print(f"Generating audio for Chapter {ch_num} ({lang}) from {script_filename}...")

    with open(script_file, 'r', encoding='utf-8') as f:
        script = json.load(f)

    combined_audio = AudioSegment.empty()
    prev_role = None

    for i, segment in enumerate(script):
        text = segment['text'].strip()
        role = segment.get('role', 'Narrator')
        
        # Skip headers or empty segments
        if not text or segment.get('is_header', False) or not re.search(r'[a-zA-Z0-9가-힣ㄱ-ㅎㅏ-ㅣ]', text):
            continue

        # Map to voice ID and speed based on role and language
        voice = VOICES[lang].get(role, VOICES[lang]["Narrator"])
        speed = SPEEDS[lang].get(role, SPEEDS[lang]["Narrator"])

        # Add pause before this segment if there was a previous segment
        if prev_role is not None:
            if prev_role == "Narrator" and role == "Narrator":
                silence_duration = 300
            elif prev_role == "Narrator" or role == "Narrator":
                silence_duration = 500
            else:
                silence_duration = 400
            combined_audio += AudioSegment.silent(duration=silence_duration)

        print(f"  Segment {i + 1}/{len(script)} ({role} - {voice}): {text[:40]}...")
        segment_audio = await synthesize_segment(text, voice, speed)
        combined_audio += segment_audio
        prev_role = role

    # Set frame rate to 44.1kHz and convert to stereo
    combined_audio = combined_audio.set_frame_rate(44100).set_channels(2)

    # Export raw MP3 at 256kbps
    combined_audio.export(out_file, format="mp3", bitrate="256k")
    print(f"Successfully generated raw audio track: {out_file}")
    return True

async def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_audio.py <lang: en|ko> <chapter_number: e.g. 1>")
        sys.exit(1)
        
    lang = sys.argv[1].lower()
    ch_num = int(sys.argv[2])
    
    if lang not in ["en", "ko"]:
        print("Error: Language must be 'en' or 'ko'.")
        sys.exit(1)
        
    success = await generate_chapter(lang, ch_num)
    if not success:
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())
