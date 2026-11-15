import os
import sys
import json
import asyncio
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

# High-fidelity native voice profiles
VOICE_EN = "en-US-BrianNeural"
VOICE_KO = "ko-KR-InJoonNeural"

async def synthesize_segment(text, voice, sem):
    """Synthesizes an audio segment using high-fidelity Neural TTS."""
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

def apply_post_processing(raw_path, clean_path, bitrate=256):
    """
    Applies standard FFmpeg post-processing to satisfy ACX / Authors Republic requirements:
    - Target RMS: -19 LUFS (RMS between -23 dB and -18 dB)
    - True Peak limit: <= -3.0 dB (-3.5 dB targeted)
    - Clean silence padding: 2.0s (2000ms) at start AND end
    - Sample rate: 44,100 Hz
    - Bitrate: 256 kbps CBR MP3
    """
    volume_norm = "loudnorm=I=-19:TP=-3.5:LRA=11"
    strip_silence = "silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0,areverse,silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0,areverse"
    leading_silence = "adelay=2000|2000"
    trailing_silence = "apad=pad_dur=2"

    filter_chain = f"{strip_silence},{volume_norm},{leading_silence},{trailing_silence}"

    cmd = [
        "ffmpeg", "-y", "-threads", "8", "-i", raw_path,
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

async def generate_bilingual_sample():
    script_file = os.path.join(SCRIPTS_DIR, "sample_page1_bilingual.json")
    raw_file = os.path.join(TEMP_DIR, "raw_dracula_bilingual_sample_page1.mp3")
    final_file = os.path.join(OUTPUT_DIR, "dracula_bilingual_sample_page1.mp3")

    if not os.path.exists(script_file):
        print(f"[ERROR] Script file not found: {script_file}")
        return False

    print("==================================================")
    print("Generating Dracula Page 1 Bilingual Audiobook Track...")
    print("==================================================")

    with open(script_file, "r", encoding="utf-8") as f:
        script_items = json.load(f)

    sem = asyncio.Semaphore(25)
    tasks = []

    for item in script_items:
        text = item["text"].strip()
        lang = item.get("lang", "en")
        voice = VOICE_EN if lang == "en" else VOICE_KO

        if text:
            tasks.append(synthesize_segment(text, voice, sem))

    print(f"Synthesizing {len(tasks)} alternating English & Korean segments in parallel...")
    results = await asyncio.gather(*tasks)

    # Interleave audio segments with short natural pause
    combined = AudioSegment.empty()
    pause_between_paragraphs = AudioSegment.silent(duration=350)

    for idx, audio in enumerate(results):
        combined += audio
        if idx < len(results) - 1:
            combined += pause_between_paragraphs

    print(f"Exporting raw audio to {raw_file}...")
    combined.export(raw_file, format="mp3", bitrate="256k")

    print(f"Applying ACX/Authors Republic FFmpeg post-processing to {final_file}...")
    success = apply_post_processing(raw_file, final_file, bitrate=256)

    if success and os.path.exists(final_file):
        print(f"[SUCCESS] Generated Dracula Bilingual Sample Track: {final_file}")
        return True
    else:
        print("[ERROR] Post-processing failed.")
        return False

def main():
    asyncio.run(generate_bilingual_sample())

if __name__ == "__main__":
    main()
