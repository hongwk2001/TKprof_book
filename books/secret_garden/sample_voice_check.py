import os
import numpy as np
import soundfile as sf
from kokoro import KPipeline

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, "temp_audio")
os.makedirs(OUT_DIR, exist_ok=True)

SAMPLE_RATE = 24000

# Sample lines mapping characters to standard lines
SAMPLES = {
    "mary": {
        "text": "I hate it. I've never seen such a gloomy, bare place in all my life. Why did uncle Archibald bring me here?",
        "lang": "a", # American
        "voices": ["af_nicole", "af_sarah"]
    },
    "colin": {
        "text": "I'm Colin. I'm going to stand and walk, and one day I will be a great athlete. The Magic will heal me.",
        "lang": "a", # American
        "voices": ["am_adam", "am_fenrir"]
    },
    "dickon": {
        "text": "Aye, it's alive. The plants under the soil are wick, and they'll grow beautiful roses when spring comes.",
        "lang": "b", # British
        "voices": ["bm_george", "am_michael"]
    },
    "martha": {
        "text": "Eh, you look so thin and yellow, Miss Mary. But the fresh air of the moor will soon put some color in your cheeks.",
        "lang": "b", # British
        "voices": ["bf_isabella", "bf_alice"]
    },
    "craven": {
        "text": "I thought the garden was dead. But it has come alive.",
        "lang": "b", # British
        "voices": ["bm_lewis", "bm_george"]
    }
}

# Keep pipeline instances cached
pipelines = {
    "a": KPipeline(lang_code='a'),
    "b": KPipeline(lang_code='b')
}

def synthesize(pipeline, text, voice, speed, out_wav):
    generator = pipeline(text, voice=voice, speed=speed)
    segments = [audio for _, _, audio in generator if audio is not None and len(audio) > 0]
    if not segments:
        print(f"  FAILED: {voice}")
        return False
    merged = np.concatenate(segments)
    sf.write(out_wav, merged, SAMPLE_RATE)
    print(f"  Saved: {out_wav}")
    return True

def main():
    print("Generating voice samples for The Secret Garden cast...")
    
    for char, data in SAMPLES.items():
        pipeline = pipelines[data["lang"]]
        for voice in data["voices"]:
            out_path = os.path.join(OUT_DIR, f"sample_{char}_{voice}.wav")
            print(f"Synthesizing {char} / voice: {voice}...")
            synthesize(pipeline, data["text"], voice, 0.95, out_path)
            
    print("\nGeneration completed! Samples saved to:", OUT_DIR)

if __name__ == "__main__":
    main()
