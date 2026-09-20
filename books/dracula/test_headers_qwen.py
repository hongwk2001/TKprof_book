import os
import sys
import subprocess
import torch
import numpy as np
import soundfile as sf
from pydub import AudioSegment

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))

QWEN3_TTS_DIR = os.path.join(PROJECT_ROOT, "Qwen3-TTS")
if QWEN3_TTS_DIR not in sys.path:
    sys.path.insert(0, QWEN3_TTS_DIR)

from qwen_tts import Qwen3TTSModel

TEMP_DIR = os.path.join(SCRIPT_DIR, "temp_audio")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "final_audio")

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def apply_post_processing(raw_path, clean_path, bitrate=256):
    volume_norm = "loudnorm=I=-19:TP=-3.5:LRA=7"
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

def test_headers():
    print("==================================================")
    print("Testing Qwen3-TTS Neutral Headers (P001 - P003)...")
    print("==================================================")

    dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16

    model = Qwen3TTSModel.from_pretrained(
        "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice",
        device_map="cuda:0",
        dtype=dtype,
        attn_implementation="sdpa"
    )

    # Test dylan (calm male narrator)
    items = [
        {"text": "Chapter 1", "speaker": "dylan"},
        {"text": "Jonathan Harker's Journal", "speaker": "dylan"},
        {"text": "Kept in shorthand.", "speaker": "dylan"}
    ]

    texts = [it["text"] for it in items]
    speakers = [it["speaker"] for it in items]
    languages = ["English"] * 3

    print("Synthesizing P001, P002, P003 with Dylan Calm Narrator in Batch GPU Mode...")
    wavs, sr = model.generate_custom_voice(
        text=texts,
        language=languages,
        speaker=speakers
    )

    combined = AudioSegment.empty()
    pause = AudioSegment.silent(duration=500) # 500ms title pause

    for idx, audio_data in enumerate(wavs):
        temp_seg_path = os.path.join(TEMP_DIR, f"header_seg_{idx}.wav")
        if isinstance(audio_data, torch.Tensor):
            audio_data = audio_data.cpu().numpy()

        sf.write(temp_seg_path, audio_data, sr)
        seg_audio = AudioSegment.from_wav(temp_seg_path)
        combined += seg_audio + pause

        if os.path.exists(temp_seg_path):
            os.remove(temp_seg_path)

    raw_file = os.path.join(TEMP_DIR, "raw_test_headers.wav")
    final_file = os.path.join(OUTPUT_DIR, "test_headers_fixed.mp3")

    combined.export(raw_file, format="wav")
    success = apply_post_processing(raw_file, final_file, bitrate=256)

    if success:
        print(f"\n[SUCCESS] Generated Uncle_Martin Headers Test Track: {final_file}")

    sys.stdout.flush()
    os._exit(0)

if __name__ == "__main__":
    test_headers()
