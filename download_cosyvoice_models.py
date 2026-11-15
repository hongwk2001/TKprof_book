import os
import sys

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from modelscope import snapshot_download

def download():
    models_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pretrained_models")
    os.makedirs(models_dir, exist_ok=True)
    
    print("==================================================")
    print("Downloading Qwen CosyVoice2 Model Checkpoint...")
    print("==================================================")
    
    try:
        model_dir = os.path.join(models_dir, "CosyVoice2-0.5B")
        print(f"Downloading FunAudioLLM/CosyVoice2-0.5B to {model_dir}...")
        snapshot_download('FunAudioLLM/CosyVoice2-0.5B', local_dir=model_dir)
        print("[SUCCESS] CosyVoice2-0.5B downloaded successfully!")
    except Exception as e:
        print(f"[WARNING] Failed to download CosyVoice2-0.5B: {e}")
        print("Downloading FunAudioLLM/CosyVoice-300M-Instruct fallback...")
        model_dir = os.path.join(models_dir, "CosyVoice-300M-Instruct")
        snapshot_download('iic/CosyVoice-300M-Instruct', local_dir=model_dir)
        print("[SUCCESS] CosyVoice-300M-Instruct downloaded successfully!")

if __name__ == "__main__":
    download()
