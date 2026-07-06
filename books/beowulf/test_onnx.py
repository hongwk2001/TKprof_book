from kokoro_onnx import Kokoro
import soundfile as sf

k = Kokoro("books/beowulf/kokoro-v1.0.onnx", "books/beowulf/voices-v1.0.bin")
samples, sr = k.create("Hello world.", voice="am_michael", speed=1.0, lang="en-us")
print(f"OK - samples: {len(samples)}, sample_rate: {sr}")
sf.write("books/beowulf/temp_audio/test_onnx.wav", samples, sr)
print("Test WAV written successfully.")
