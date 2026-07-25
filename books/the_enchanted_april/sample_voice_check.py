import os
import numpy as np
import soundfile as sf
from kokoro import KPipeline

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, "temp_audio")
os.makedirs(OUT_DIR, exist_ok=True)

SAMPLE_RATE = 24000

LINES = {
    "scrap": "Nothing. If I may make a suggestion, ladies, I suggest you don't ruin a wonderful vacation worrying about housekeeping.",
    "fisher": "You must be very cold in that. It gets much colder here once the sun goes down.",
}

# British female voices, candidates for Lady Caroline (Scrap) / Mrs. Fisher
VOICES = ["bf_alice", "bf_emma", "bf_isabella", "bf_lily"]

pipeline_b = KPipeline(lang_code='b')

def synthesize(text, voice, speed, out_wav):
    generator = pipeline_b(text, voice=voice, speed=speed)
    segments = [audio for _, _, audio in generator if audio is not None and len(audio) > 0]
    if not segments:
        print(f"  FAILED: {voice}")
        return
    merged = np.concatenate(segments)
    sf.write(out_wav, merged, SAMPLE_RATE)
    print(f"  -> {out_wav}")

for character, text in LINES.items():
    for voice in VOICES:
        out_path = os.path.join(OUT_DIR, f"sample_{character}_{voice}.wav")
        print(f"Generating {character} / {voice}...")
        synthesize(text, voice, 0.95, out_path)

print("Done. Samples saved to", OUT_DIR)
