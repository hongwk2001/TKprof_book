import os
import sys
import subprocess
import torch
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

def generate_voice_samples():
    print("==================================================")
    print("Generating Qwen3-TTS Voice Samples (Ryan, Aiden, Serena, Eric)...")
    print("==================================================\n")

    dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16

    model = Qwen3TTSModel.from_pretrained(
        "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice",
        device_map="cuda:0",
        dtype=dtype,
        attn_implementation="sdpa"
    )

    samples = [
        {
            "speaker": "ryan",
            "filename": "sample_voice_ryan.mp3",
            "text": "Hello, I am Ryan. I speak with a Standard General American accent. My tone is clear, fluent, and natural with American cadence, ideal for primary narration."
        },
        {
            "speaker": "aiden",
            "filename": "sample_voice_aiden.mp3",
            "text": "Hello, I am Aiden. I speak with a Native North American English accent. My tone is articulate, smooth, and formal, excellent for audiobook readings."
        },
        {
            "speaker": "serena",
            "filename": "sample_voice_serena.mp3",
            "text": "Hello, I am Serena. I speak with a Native US English accent. My tone is clear, expressive, and highly fluent for female narration."
        },
        {
            "speaker": "eric",
            "filename": "sample_voice_eric.mp3",
            "text": "Hello, I am Eric. I speak with a Standard US English accent. My tone is friendly, warm, and approachable."
        }
    ]

    generated_files = []

    for spk_info in samples:
        spk = spk_info["speaker"]
        fname = spk_info["filename"]
        text = spk_info["text"]

        raw_wav_path = os.path.join(TEMP_DIR, f"raw_{spk}.wav")
        final_mp3_path = os.path.join(OUTPUT_DIR, fname)

        print(f"Synthesizing voice sample for: {spk.upper()}...")
        wavs, sr = model.generate_custom_voice(
            text=text,
            language="English",
            speaker=spk
        )

        audio_data = wavs[0]
        if isinstance(audio_data, torch.Tensor):
            audio_data = audio_data.cpu().numpy()

        sf.write(raw_wav_path, audio_data, sr)
        success = apply_post_processing(raw_wav_path, final_mp3_path, bitrate=256)

        if success:
            print(f"  -> Generated: {final_mp3_path}")
            generated_files.append(final_mp3_path)

    print("\n==================================================")
    print("Voice Sample Generation Completed Successfully!")
    print("==================================================\n")

    sys.stdout.flush()
    os._exit(0)

if __name__ == "__main__":
    generate_voice_samples()
