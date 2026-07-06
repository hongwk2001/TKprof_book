import os
import sys
import json
import numpy as np
import soundfile as sf
from pydub import AudioSegment
from kokoro_onnx import Kokoro

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(SCRIPT_DIR, "scripts")
TEMP_DIR = os.path.join(SCRIPT_DIR, "temp_audio")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "final_audio")
BUMPER_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "the_prince", "freesound_community-cinematic-intro-6097.mp3"))

ONNX_MODEL = os.path.join(SCRIPT_DIR, "kokoro-v1.0.onnx")
VOICES_BIN  = os.path.join(SCRIPT_DIR, "voices-v1.0.bin")

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

SAMPLE_RATE = 24000

# Voice -> language mapping for kokoro-onnx
VOICE_LANG = {
    "am_michael": "en-us",
    "am_adam":    "en-us",
    "af_heart":   "en-us",
    "bm_george":  "en-gb",
    "bf_emma":    "en-gb",
    "bm_lewis":   "en-gb",
}

# Initialize kokoro-onnx model (loads once, reused for all chapters)
print("Initializing Kokoro ONNX model...")
kokoro = Kokoro(ONNX_MODEL, VOICES_BIN)
print("Kokoro ONNX model loaded.")


def generate_chapter(ch_arg):
    # Normalize chapter arguments and set input/output file names
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

    audio_segments = []
    silence_300ms = np.zeros(int(SAMPLE_RATE * 0.3), dtype=np.float32)

    for i, segment in enumerate(script):
        text = segment['text'].strip()
        voice = segment.get('voice', 'am_michael')

        if not text:
            continue

        lang = VOICE_LANG.get(voice, "en-us")

        try:
            samples, sample_rate = kokoro.create(text, voice=voice, speed=1.0, lang=lang)
            if samples is not None and len(samples) > 0:
                audio_segments.append(samples)
                audio_segments.append(silence_300ms)
        except Exception as e:
            print(f"  Error on segment {i} ({voice}): {e}")

    if not audio_segments:
        print(f"No audio generated for {ch_arg}")
        return

    # Concatenate all segments (drop trailing silence)
    chapter_audio = np.concatenate(audio_segments[:-1])

    # Save to temp WAV
    temp_wav_path = os.path.join(TEMP_DIR, f"ch_{ch_arg}_temp.wav")
    sf.write(temp_wav_path, chapter_audio, SAMPLE_RATE)

    # Use pydub to upsample to 44.1kHz stereo and mix in the cinematic bumper
    try:
        chapter_clip = AudioSegment.from_wav(temp_wav_path)
        # Upsample to 44.1kHz stereo — required for true 256kbps MP3 (ACX compliant)
        chapter_clip = chapter_clip.set_frame_rate(44100).set_channels(2)

        cinematic_clip = AudioSegment.from_mp3(BUMPER_PATH)

        if ch_arg == "intro":
            # 4.5 seconds of music at the start of the Intro track
            music_part = cinematic_clip[:4500]
            final_clip = music_part + AudioSegment.silent(duration=500) + chapter_clip
        elif ch_arg == "closing":
            # Full-length music at the end of the Closing track
            final_clip = chapter_clip + AudioSegment.silent(duration=500) + cinematic_clip
        else:
            # 2.0 seconds of music at the start of each chapter track
            music_part = cinematic_clip[:2000]
            final_clip = music_part + AudioSegment.silent(duration=500) + chapter_clip

        final_clip.export(out_file, format="mp3", bitrate="256k")
        print(f"Successfully generated {out_file}")
    except Exception as e:
        print(f"Error mixing/exporting MP3 for {ch_arg}: {e}")
    finally:
        if os.path.exists(temp_wav_path):
            os.remove(temp_wav_path)


def main():
    if len(sys.argv) > 1:
        ch_arg = sys.argv[1].lower()
        generate_chapter(ch_arg)
    else:
        generate_chapter("intro")
        for i in range(44):
            generate_chapter(f"{i:02d}")
        generate_chapter("closing")


if __name__ == "__main__":
    main()
