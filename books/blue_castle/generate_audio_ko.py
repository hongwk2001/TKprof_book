import os
import sys
import json
import asyncio
import re
from io import BytesIO
import edge_tts
from pydub import AudioSegment

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(SCRIPT_DIR, "scripts_ko")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "final_audio_ko")
TEMP_DIR = os.path.join(SCRIPT_DIR, "temp_audio_ko")
BUMPER_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "the_prince", "freesound_community-cinematic-intro-6097.mp3"))

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

async def synthesize_segment(text, voice, speed):
    for attempt in range(5):
        try:
            communicate = edge_tts.Communicate(text, voice, rate=speed)
            audio_data = b""
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_data += chunk["data"]
            if audio_data:
                # Load the audio into pydub
                return AudioSegment.from_file(BytesIO(audio_data), format="mp3")
        except Exception as e:
            print(f"      Attempt {attempt + 1} failed for voice {voice}: {e}")
            await asyncio.sleep(2)
    raise RuntimeError(f"Failed to synthesize segment after 5 attempts: text={text[:20]}...")

async def generate_chapter(ch_arg):
    if ch_arg == "intro":
        script_file = os.path.join(SCRIPTS_DIR, "script_intro.json")
        out_file = os.path.join(OUTPUT_DIR, "final_track_00_intro.mp3")
    elif ch_arg == "closing":
        script_file = os.path.join(SCRIPTS_DIR, "script_closing.json")
        out_file = os.path.join(OUTPUT_DIR, "closing.mp3")
    else:
        if ch_arg.isdigit():
            ch_arg = ch_arg.zfill(2)
        script_file = os.path.join(SCRIPTS_DIR, f"script_ch_{ch_arg}.json")
        out_file = os.path.join(OUTPUT_DIR, f"final_track_{ch_arg}.mp3")

    if os.path.exists(out_file):
        print(f"Skipping {os.path.basename(out_file)} (already generated)")
        return

    if not os.path.exists(script_file):
        print(f"File not found: {script_file}")
        return

    print(f"Generating audio for {ch_arg} from {os.path.basename(script_file)}...")

    with open(script_file, 'r', encoding='utf-8') as f:
        script = json.load(f)

    combined_audio = AudioSegment.empty()
    prev_char_type = None

    for i, segment in enumerate(script):
        text = segment['text'].strip()
        voice = segment.get('voice')
        speed = segment.get('speed', '+0%')
        char_name = segment.get('character', 'narrator')

        if not text or not re.search(r'[a-zA-Z0-9가-힣ㄱ-ㅎㅏ-ㅣ]', text):
            continue

        # Add pause before this segment if there was a previous segment
        current_char_type = "narrator" if char_name == "narrator" else "character"
        if prev_char_type is not None:
            if prev_char_type == "narrator" and current_char_type == "narrator":
                silence_duration = 300
            elif prev_char_type == "narrator" and current_char_type == "character":
                silence_duration = 500
            elif prev_char_type == "character" and current_char_type == "narrator":
                silence_duration = 500
            elif prev_char_type == "character" and current_char_type == "character":
                silence_duration = 400
            else:
                silence_duration = 300
            combined_audio += AudioSegment.silent(duration=silence_duration)

        print(f"  Segment {i + 1}/{len(script)} ({char_name} - {voice}): {text[:30]}...")
        segment_audio = await synthesize_segment(text, voice, speed)
        combined_audio += segment_audio
        prev_char_type = current_char_type

    # Upsample to 44.1kHz stereo
    combined_audio = combined_audio.set_frame_rate(44100).set_channels(2)

    # Mix in the cinematic bumper
    if os.path.exists(BUMPER_PATH):
        try:
            cinematic_clip = AudioSegment.from_mp3(BUMPER_PATH)
            if ch_arg == "intro":
                # 4.5 seconds of music at the start of the Intro track
                music_part = cinematic_clip[:4500]
                final_clip = music_part + AudioSegment.silent(duration=500) + combined_audio
            elif ch_arg == "closing":
                # Full-length music at the end of the Closing track
                final_clip = combined_audio + AudioSegment.silent(duration=500) + cinematic_clip
            else:
                # 2.0 seconds of music at the start of each chapter track
                music_part = cinematic_clip[:2000]
                final_clip = music_part + AudioSegment.silent(duration=500) + combined_audio
        except Exception as bumper_err:
            print(f"  Warning: failed to mix bumper: {bumper_err}. Using plain audio.")
            final_clip = combined_audio
    else:
        print(f"  Bumper not found at {BUMPER_PATH}. Using plain audio.")
        final_clip = combined_audio

    # Export at 256kbps MP3
    final_clip.export(out_file, format="mp3", bitrate="256k")
    print(f"Successfully generated {out_file}")

def create_filelists():
    print("Generating part list text files for merging...")
    os.makedirs(os.path.join(OUTPUT_DIR, "merged"), exist_ok=True)
    
    # 45 chapters plus intro and closing
    part1 = ["final_track_00_intro.mp3"] + [f"final_track_{i:02d}.mp3" for i in range(1, 9)]
    part2 = [f"final_track_{i:02d}.mp3" for i in range(9, 17)]
    part3 = [f"final_track_{i:02d}.mp3" for i in range(17, 25)]
    part4 = [f"final_track_{i:02d}.mp3" for i in range(25, 33)]
    part5 = [f"final_track_{i:02d}.mp3" for i in range(33, 41)]
    part6 = [f"final_track_{i:02d}.mp3" for i in range(41, 46)] + ["closing.mp3"]
    
    parts = [part1, part2, part3, part4, part5, part6]
    for idx, part in enumerate(parts, 1):
        list_file = os.path.join(OUTPUT_DIR, f"part{idx}_ko_list.txt")
        with open(list_file, "w", encoding="utf-8") as f:
            for track in part:
                f.write(f"file '{track}'\n")
        print(f"  Created {list_file}")

async def main():
    if len(sys.argv) > 1:
        ch_arg = sys.argv[1].lower()
        if ch_arg == "filelists":
            create_filelists()
        else:
            await generate_chapter(ch_arg)
    else:
        await generate_chapter("intro")
        for i in range(1, 46):
            await generate_chapter(f"{i:02d}")
        await generate_chapter("closing")
        create_filelists()

if __name__ == "__main__":
    asyncio.run(main())
