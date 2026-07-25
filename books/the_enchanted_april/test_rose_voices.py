import os
import numpy as np
import soundfile as sf
from kokoro import KPipeline

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, "temp_audio")
os.makedirs(OUT_DIR, exist_ok=True)

SAMPLE_RATE = 24000

ROSE_LINE = "I'm afraid references bring a business-like tone to our holiday that we don't want. We won't check yours, and we won't give you any of ours."

# British female voices (bf_*) and American female voices (af_*) to test
VOICES = {
    "bf_lily": "b",
    "bf_emma": "b",
    "bf_alice": "b",
    "bf_isabella": "b",
    "af_sarah": "a",
    "af_sky": "a",
    "af_aoife": "a",
    "af_heart": "a"
}

print("Generating Rose voice samples at speed 1.0...")

pipelines = {
    "a": KPipeline(lang_code="a"),
    "b": KPipeline(lang_code="b")
}

for voice_name, lang in VOICES.items():
    out_path = os.path.join(OUT_DIR, f"rose_sample_{voice_name}.wav")
    print(f"Synthesizing {voice_name}...")
    pipeline = pipelines[lang]
    generator = pipeline(ROSE_LINE, voice=voice_name, speed=1.0)
    segments = [audio for _, _, audio in generator if audio is not None and len(audio) > 0]
    if segments:
        merged = np.concatenate(segments)
        sf.write(out_path, merged, SAMPLE_RATE)
        print(f"  Saved to {out_path}")
    else:
        print(f"  Failed for {voice_name}")

print("All samples generated in temp_audio/ directory!")
