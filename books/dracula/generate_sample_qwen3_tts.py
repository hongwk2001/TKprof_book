import os
import sys
import json
import asyncio
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

# Ensure Qwen3-TTS repo is in python path
QWEN3_TTS_DIR = os.path.join(PROJECT_ROOT, "Qwen3-TTS")
if QWEN3_TTS_DIR not in sys.path:
    sys.path.insert(0, QWEN3_TTS_DIR)

from qwen_tts import Qwen3TTSModel

SCRIPTS_DIR = os.path.join(SCRIPT_DIR, "scripts")
TEMP_DIR = os.path.join(SCRIPT_DIR, "temp_audio")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "final_audio")

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

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

def generate_qwen3_bilingual_sample():
    script_file = os.path.join(SCRIPTS_DIR, "sample_page1_bilingual.json")
    raw_file = os.path.join(TEMP_DIR, "raw_dracula_qwen3_bilingual_sample_page1.wav")
    final_file = os.path.join(OUTPUT_DIR, "dracula_qwen3_bilingual_sample_page1.mp3")

    if not os.path.exists(script_file):
        print(f"[ERROR] Script file not found: {script_file}")
        return False

    print("==================================================")
    print("Loading Official Qwen3-TTS Model on CUDA GPU...")
    print("==================================================")

    # Enable PyTorch SDPA (Scaled Dot-Product Attention / Native FlashAttention-2) & bfloat16
    dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16

    print("Loading fast Qwen3-TTS CustomVoice Model with PyTorch SDPA FlashAttention...")
    try:
        model = Qwen3TTSModel.from_pretrained(
            "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice",
            device_map="cuda:0",
            dtype=dtype,
            attn_implementation="sdpa"
        )
        print("[SUCCESS] Qwen3-TTS 0.6B Model loaded with SDPA FlashAttention!")
    except Exception as e:
        print(f"[INFO] Falling back to 1.7B SDPA model: {e}")
        model = Qwen3TTSModel.from_pretrained(
            "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice",
            device_map="cuda:0",
            dtype=dtype,
            attn_implementation="sdpa"
        )

    print("[SUCCESS] Qwen3-TTS Model loaded on GPU!")

    with open(script_file, "r", encoding="utf-8") as f:
        script_items = json.load(f)

    combined = AudioSegment.empty()
    pause_between_paragraphs = AudioSegment.silent(duration=350)

    print(f"\nSynthesizing {len(script_items)} alternating English & Korean segments...")
    print(f"Saving paragraph WAV files to: {TEMP_DIR}\n")

    for idx, item in enumerate(script_items):
        raw_text = item["text"].strip().strip("()") # Strip outer parentheses e.g. (Kept in shorthand.) -> Kept in shorthand.
        tag = item.get("tag", "P000")
        lang = item.get("lang", "en")

        language_name = "English" if lang == "en" else "Korean"
        speaker_name = "dylan" if lang == "en" else "vivian"

        temp_seg_path = os.path.join(TEMP_DIR, f"seg_{idx+1:03d}_{tag}_{lang}.wav")

        if os.path.exists(temp_seg_path) and os.path.getsize(temp_seg_path) > 1000:
            print(f"[{idx+1}/{len(script_items)}] [{tag}] [{lang}] [CACHED] Skipping existing file: {os.path.basename(temp_seg_path)}")
        else:
            print(f"[{idx+1}/{len(script_items)}] [{tag}] [{lang}] Synthesizing: {raw_text[:35]}...")
            wavs, sr = model.generate_custom_voice(
                text=raw_text,
                language=language_name,
                speaker=speaker_name
            )

            audio_data = wavs[0]
            if isinstance(audio_data, torch.Tensor):
                audio_data = audio_data.cpu().numpy()

            sf.write(temp_seg_path, audio_data, sr)
            print(f"[{idx+1}/{len(script_items)}] [{tag}] [{lang}] [SAVED] -> {temp_seg_path}")

        seg_audio = AudioSegment.from_wav(temp_seg_path)
        combined += seg_audio + pause_between_paragraphs

    print(f"\nExporting raw combined audio to {raw_file}...")
    combined.export(raw_file, format="wav")

    print(f"Applying ACX/Authors Republic FFmpeg post-processing to {final_file}...")
    success = apply_post_processing(raw_file, final_file, bitrate=256)

    if success and os.path.exists(final_file):
        print(f"[SUCCESS] Generated Genuine Qwen3-TTS Bilingual Sample Track: {final_file}")
        sys.stdout.flush()
        os._exit(0)
        return True
    else:
        print("[ERROR] Post-processing failed.")
        return False

def main():
    generate_qwen3_bilingual_sample()

if __name__ == "__main__":
    main()
