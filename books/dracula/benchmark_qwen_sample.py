import os
import sys
import json
import time
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

SCRIPTS_DIR = os.path.join(SCRIPT_DIR, "scripts")
TEMP_DIR = os.path.join(SCRIPT_DIR, "temp_audio")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "final_audio")

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def apply_post_processing(raw_path, clean_path, bitrate=256):
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

def run_benchmark():
    t_start = time.perf_counter()
    print("================================================================================")
    print(" QWEN3-TTS END-TO-END WALL-CLOCK BENCHMARK (Page 1 Sample - 28 Paragraphs)")
    print(" Speakers: English = dylan | Korean = vivian")
    print("================================================================================\n")

    # Stage 1: Model Loading
    t_load_start = time.perf_counter()
    print("[1/6] Loading Qwen3-TTS Model on CUDA GPU...")
    dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16

    model = Qwen3TTSModel.from_pretrained(
        "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice",
        device_map="cuda:0",
        dtype=dtype,
        attn_implementation="sdpa"
    )
    t_load_end = time.perf_counter()
    time_load = t_load_end - t_load_start
    print(f"  -> Model Loaded in {time_load:.2f} seconds.\n")

    # Stage 2: Script Reading
    t_script_start = time.perf_counter()
    script_file = os.path.join(SCRIPTS_DIR, "sample_page1_bilingual.json")
    with open(script_file, "r", encoding="utf-8") as f:
        script_items = json.load(f)
    t_script_end = time.perf_counter()
    time_script = t_script_end - t_script_start
    print(f"[2/6] Loaded {len(script_items)} paragraph script segments ({time_script:.4f}s).\n")

    # Stage 3: GPU Generation & Disk Saving
    t_gen_start = time.perf_counter()
    print(f"[3/6] Synthesizing 28 paragraphs & saving to temp_audio...")

    combined = AudioSegment.empty()
    pause = AudioSegment.silent(duration=350)

    for idx, item in enumerate(script_items):
        raw_text = item["text"].strip().strip("()")
        tag = item.get("tag", "P000")
        lang = item.get("lang", "en")

        language_name = "English" if lang == "en" else "Korean"
        speaker_name = "dylan" if lang == "en" else "vivian"

        temp_seg_path = os.path.join(TEMP_DIR, f"seg_{idx+1:03d}_{tag}_{lang}.wav")

        t_item_start = time.perf_counter()
        wavs, sr = model.generate_custom_voice(
            text=raw_text,
            language=language_name,
            speaker=speaker_name
        )

        audio_data = wavs[0]
        if isinstance(audio_data, torch.Tensor):
            audio_data = audio_data.cpu().numpy()

        sf.write(temp_seg_path, audio_data, sr)
        t_item_end = time.perf_counter()
        dur = t_item_end - t_item_start

        print(f"  [{idx+1:02d}/28] [{tag}] [{lang}] ({dur:.2f}s) Saved -> {os.path.basename(temp_seg_path)}")

        seg_audio = AudioSegment.from_wav(temp_seg_path)
        combined += seg_audio + pause

    t_gen_end = time.perf_counter()
    time_gen = t_gen_end - t_gen_start
    print(f"  -> Total Generation & Paragraph Disk I/O: {time_gen:.2f} seconds.\n")

    # Stage 4: Stitching & Raw Audio Export
    t_stitch_start = time.perf_counter()
    raw_file = os.path.join(TEMP_DIR, "raw_dracula_qwen3_bilingual_sample_page1.wav")
    print(f"[4/6] Stitching audio segments to raw WAV: {raw_file}...")
    combined.export(raw_file, format="wav")
    t_stitch_end = time.perf_counter()
    time_stitch = t_stitch_end - t_stitch_start
    print(f"  -> Audio Stitched in {time_stitch:.2f} seconds.\n")

    # Stage 5: FFmpeg Post-Processing
    t_ffmpeg_start = time.perf_counter()
    final_file = os.path.join(OUTPUT_DIR, "dracula_qwen3_bilingual_sample_page1.mp3")
    print(f"[5/6] Applying FFmpeg ACX Loudness Normalization & 256kbps MP3 Encoding...")
    success = apply_post_processing(raw_file, final_file, bitrate=256)
    t_ffmpeg_end = time.perf_counter()
    time_ffmpeg = t_ffmpeg_end - t_ffmpeg_start
    print(f"  -> FFmpeg Post-Processing Completed in {time_ffmpeg:.2f} seconds.\n")

    # Stage 6: Audio Quality Audit
    t_audit_start = time.perf_counter()
    print("[6/6] Auditing Final Audio Quality with check_audio_quality.py...")
    audit_cmd = [sys.executable, os.path.join(PROJECT_ROOT, "check_audio_quality.py"), final_file]
    audit_res = subprocess.run(audit_cmd, capture_output=True, text=True)
    t_audit_end = time.perf_counter()
    time_audit = t_audit_end - t_audit_start

    t_total = time.perf_counter() - t_start

    print("\n================================================================================")
    print(" END-TO-END WALL-CLOCK TIMING REPORT")
    print("================================================================================")
    print(f" 1. Model Loading & GPU Init:    {time_load:6.2f} sec  ({(time_load/t_total)*100:4.1f}%)")
    print(f" 2. Script Reading:              {time_script:6.4f} sec  ({(time_script/t_total)*100:4.1f}%)")
    print(f" 3. GPU Speech Gen + Disk I/O:   {time_gen:6.2f} sec  ({(time_gen/t_total)*100:4.1f}%)")
    print(f" 4. Audio Stitching (Pydub):     {time_stitch:6.2f} sec  ({(time_stitch/t_total)*100:4.1f}%)")
    print(f" 5. FFmpeg Post-Processing:      {time_ffmpeg:6.2f} sec  ({(time_ffmpeg/t_total)*100:4.1f}%)")
    print(f" 6. Quality Audit Check:         {time_audit:6.2f} sec  ({(time_audit/t_total)*100:4.1f}%)")
    print("--------------------------------------------------------------------------------")
    print(f" TOTAL END-TO-END WALL-CLOCK:    {t_total:6.2f} sec  (100.0%)")
    print("================================================================================\n")
    print(audit_res.stdout)

    sys.stdout.flush()
    os._exit(0)

if __name__ == "__main__":
    run_benchmark()
