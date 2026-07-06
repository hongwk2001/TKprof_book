import asyncio
import os
import sys
import soundfile as sf
import numpy as np

# Ensure we can run edge-tts
try:
    import edge_tts
except ImportError:
    print("edge-tts is missing")

from kokoro_onnx import Kokoro

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ONNX_MODEL = os.path.join(BASE_DIR, "kokoro-v1.0.onnx")
VOICES_BIN = os.path.join(BASE_DIR, "voices-v1.0.bin")
OUTPUT_DIR = os.path.join(BASE_DIR, "samples")
os.makedirs(OUTPUT_DIR, exist_ok=True)

SAMPLE_TEXT = (
    "프롤로그: 최초의 왕, 실드 셰핑. 들어보라! 고대 데인족 왕들이 누렸던 "
    "그 찬란한 영광의 이야기들을! 아득한 옛날, 이 고귀한 지배자들은 수많은 "
    "영웅적 위업을 달성하며 백성을 지키고 세력을 뻗어나갔다."
)

def run_kokoro():
    print("Loading Kokoro ONNX model...")
    kokoro = Kokoro(ONNX_MODEL, VOICES_BIN)
    
    # We test Korean using the 'ko' language code
    # Kokoro multi-lingual models can process 'ko' with default voices (e.g. af_heart)
    print("Generating Kokoro sample...")
    samples, sample_rate = kokoro.create(SAMPLE_TEXT, voice="af_heart", speed=1.0, lang="ko")
    
    out_path = os.path.join(OUTPUT_DIR, "test_ko_kokoro.wav")
    sf.write(out_path, samples, sample_rate)
    print(f"Kokoro sample written to: {out_path}")

async def run_edge_tts():
    print("Generating edge-tts sample (ko-KR-SunHiNeural)...")
    out_path = os.path.join(OUTPUT_DIR, "test_ko_edge_sunhi.mp3")
    c = edge_tts.Communicate(SAMPLE_TEXT, "ko-KR-SunHiNeural")
    await c.save(out_path)
    print(f"edge-tts SunHi sample written to: {out_path}")

    print("Generating edge-tts sample (ko-KR-InJoonNeural)...")
    out_path = os.path.join(OUTPUT_DIR, "test_ko_edge_injoon.mp3")
    c = edge_tts.Communicate(SAMPLE_TEXT, "ko-KR-InJoonNeural")
    await c.save(out_path)
    print(f"edge-tts InJoon sample written to: {out_path}")

def main():
    try:
        run_kokoro()
    except Exception as e:
        print(f"Failed to generate Kokoro sample: {e}")
        
    try:
        asyncio.run(run_edge_tts())
    except Exception as e:
        print(f"Failed to generate edge-tts samples: {e}")

if __name__ == "__main__":
    main()
