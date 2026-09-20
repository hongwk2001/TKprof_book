import os
import sys
import asyncio
import subprocess
import torch
import soundfile as sf
import edge_tts
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

async def generate_edge_sample(text, voice_name, raw_path):
    communicate = edge_tts.Communicate(text, voice_name)
    await communicate.save(raw_path)

def generate_korean_samples():
    print("==================================================")
    print("Generating Korean Voice Samples (Qwen & Edge-TTS)...")
    print("==================================================\n")

    dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16

    print("Loading Qwen3-TTS Model on GPU...")
    model = Qwen3TTSModel.from_pretrained(
        "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice",
        device_map="cuda:0",
        dtype=dtype,
        attn_implementation="sdpa"
    )

    qwen_samples = [
        {
            "speaker": "vivian",
            "filename": "sample_voice_ko_vivian.mp3",
            "text": "안녕하세요, 저는 비비안입니다. 밝고 자연스러운 현대 한국어 억양을 들려드립니다."
        },
        {
            "speaker": "sohee",
            "filename": "sample_voice_ko_sohee.mp3",
            "text": "안녕하세요, 저는 소희입니다. 차분하고 정돈된 낭독 톤으로 오디오북에 어울리는 목소리입니다."
        },
        {
            "speaker": "ono_anna",
            "filename": "sample_voice_ko_ono_anna.mp3",
            "text": "안녕하세요, 저는 안나입니다. 맑고 온화한 낭독 스타일을 갖추고 있습니다."
        },
        {
            "speaker": "uncle_fu",
            "filename": "sample_voice_ko_uncle_fu.mp3",
            "text": "안녕하십니까, 저는 엉클 푸입니다. 중후하고 명확한 남성 낭독 목소리를 제공합니다."
        }
    ]

    for item in qwen_samples:
        spk = item["speaker"]
        fname = item["filename"]
        text = item["text"]

        raw_wav_path = os.path.join(TEMP_DIR, f"raw_{spk}.wav")
        final_mp3_path = os.path.join(OUTPUT_DIR, fname)

        print(f"Synthesizing Qwen voice sample: {spk.upper()}...")
        wavs, sr = model.generate_custom_voice(
            text=text,
            language="Korean",
            speaker=spk
        )

        audio_data = wavs[0]
        if isinstance(audio_data, torch.Tensor):
            audio_data = audio_data.cpu().numpy()

        sf.write(raw_wav_path, audio_data, sr)
        success = apply_post_processing(raw_wav_path, final_mp3_path, bitrate=256)

        if success:
            print(f"  -> Generated Qwen Sample: {final_mp3_path}")

    # Edge-TTS Korean Samples
    edge_samples = [
        {
            "voice": "ko-KR-SunHiNeural",
            "filename": "sample_voice_ko_sunhi_edge.mp3",
            "text": "안녕하세요, 저는 선희입니다. 엣지 TTS의 표준 여성 한국어 목소리입니다."
        },
        {
            "voice": "ko-KR-InJoonNeural",
            "filename": "sample_voice_ko_injoon_edge.mp3",
            "text": "안녕하세요, 저는 인준입니다. 엣지 TTS의 표준 남성 한국어 목소리입니다."
        }
    ]

    for item in edge_samples:
        voice = item["voice"]
        fname = item["filename"]
        text = item["text"]

        raw_mp3_path = os.path.join(TEMP_DIR, f"raw_{voice}.mp3")
        final_mp3_path = os.path.join(OUTPUT_DIR, fname)

        print(f"Synthesizing Edge-TTS voice sample: {voice}...")
        asyncio.run(generate_edge_sample(text, voice, raw_mp3_path))
        success = apply_post_processing(raw_mp3_path, final_mp3_path, bitrate=256)

        if success:
            print(f"  -> Generated Edge-TTS Sample: {final_mp3_path}")

    print("\n==================================================")
    print("Korean Voice Samples Generation Completed Successfully!")
    print("==================================================\n")

    sys.stdout.flush()
    os._exit(0)

if __name__ == "__main__":
    generate_korean_samples()
