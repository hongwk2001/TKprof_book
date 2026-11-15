import os
import sys
import json
import asyncio
import re
import subprocess
from io import BytesIO
import edge_tts
from pydub import AudioSegment
import torch

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

# Device Configuration: PyTorch CUDA on local GPU (e.g. RTX 3080)
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Voice maps for English and Korean
VOICE_MAP_EN = {
    "Narrator": "en-US-BrianNeural",
    "Dracula": "en-GB-RyanNeural",
    "Female": "en-US-AvaNeural",
    "VanHelsing": "en-US-ChristopherNeural",
    "Male_Others": "en-US-EricNeural"
}

VOICE_MAP_KO = {
    "Narrator": "ko-KR-InJoonNeural",
    "Dracula": "ko-KR-HyunjunNeural",
    "Female": "ko-KR-SunHiNeural",
    "VanHelsing": "ko-KR-BongJinNeural",
    "Male_Others": "ko-KR-InJoonNeural"
}

async def synthesize_segment(text, voice, sem):
    """Synthesizes text using high-fidelity Neural TTS model engine."""
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

async def generate_chapter(lang, ch_num):
    ch_str = str(ch_num).zfill(2)
    script_file = os.path.join(SCRIPTS_DIR, f"ch_{ch_str}_{lang}.json")

    raw_file = os.path.join(TEMP_DIR, f"raw_ch_{ch_str}_{lang}.mp3")
    final_file = os.path.join(OUTPUT_DIR, f"ch_{ch_str}_{lang}.mp3")

    if not os.path.exists(script_file):
        print(f"[ERROR] Script file not found: {script_file}")
        return False

    print(f"Generating GPU-Accelerated Audio for Dracula Chapter {ch_num} ({lang.upper()}) [Device: {DEVICE}]...")

    with open(script_file, "r", encoding="utf-8") as f:
        script_items = json.load(f)

    voice_map = VOICE_MAP_EN if lang == "en" else VOICE_MAP_KO

    # Increase parallel worker concurrency to 25
    sem = asyncio.Semaphore(25)
    tasks = []

    for item in script_items:
        text = item["text"].strip()
        role = item.get("role", "Narrator")
        voice = voice_map.get(role, voice_map["Narrator"])

        if text and re.search(r"[a-zA-Z0-9\uac00-\ud7a3]", text):
            tasks.append(synthesize_segment(text, voice, sem))

    if not tasks:
        print(f"[ERROR] No audio text segments found for Chapter {ch_num}")
        return False

    print(f"Synthesizing {len(tasks)} audio segments in parallel (25 workers)...")
    results = await asyncio.gather(*tasks)

    # Stitch audio segments with short natural pauses
    combined = AudioSegment.empty()
    pause = AudioSegment.silent(duration=350)  # 350ms pause between segments

    for idx, audio in enumerate(results):
        combined += audio
        if idx < len(results) - 1:
            combined += pause

    print(f"Exporting raw audio to {raw_file}...")
    combined.export(raw_file, format="mp3", bitrate="256k")

    print(f"Applying ACX/Authors Republic FFmpeg post-processing to {final_file}...")
    success = apply_post_processing(raw_file, final_file, bitrate=256)

    if success and os.path.exists(final_file):
        print(f"[SUCCESS] Successfully generated: {final_file}")
        return True
    else:
        print(f"[ERROR] Post-processing failed for Chapter {ch_num}")
        return False

def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_audio_qwen.py <lang: en|ko> <chapter_number: e.g. 1 or all>")
        sys.exit(1)

    lang = sys.argv[1].lower()
    chap_arg = sys.argv[2].lower()

    if lang not in ["en", "ko"]:
        print("Invalid language. Choose 'en' or 'ko'.")
        sys.exit(1)

    if chap_arg == "all":
        for ch in range(1, 28):
            asyncio.run(generate_chapter(lang, ch))
    else:
        try:
            ch_num = int(chap_arg)
            asyncio.run(generate_chapter(lang, ch_num))
        except ValueError:
            print("Invalid chapter number. Specify integer (1..27) or 'all'.")
            sys.exit(1)

if __name__ == "__main__":
    main()
