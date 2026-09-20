import os
import sys
import subprocess
from pydub import AudioSegment
from pydub.silence import detect_silence

FINAL_AUDIO_DIR = r'C:\git_repo\TKprof_book\books\dracula\final_audio'

TARGET_CHAPTERS = [
    ("dracula_ch_13_bilingual_sunhi.mp3", "dracula_ch_13a_bilingual_sunhi.mp3", "dracula_ch_13b_bilingual_sunhi.mp3"),
    ("dracula_ch_26_bilingual_sunhi.mp3", "dracula_ch_26a_bilingual_sunhi.mp3", "dracula_ch_26b_bilingual_sunhi.mp3"),
    ("dracula_ch_27_bilingual_sunhi.mp3", "dracula_ch_27a_bilingual_sunhi.mp3", "dracula_ch_27b_bilingual_sunhi.mp3")
]

def find_best_split_point(audio, target_ms, window_ms=60000):
    """Finds the longest silence within +/- window_ms around target_ms."""
    start_search = max(0, target_ms - window_ms)
    end_search = min(len(audio), target_ms + window_ms)
    
    search_segment = audio[start_search:end_search]
    
    # Detect silence (min 400ms silence, -40dBFS threshold)
    silences = detect_silence(search_segment, min_silence_len=400, silence_thresh=-40)
    
    if not silences:
        # Fallback to exact target_ms if no silence detected
        print(f"  [WARN] No silence found in window, using exact mid-point.")
        return target_ms
    
    # Find silence closest to middle of window
    target_offset = target_ms - start_search
    best_silence = min(silences, key=lambda s: abs(((s[0] + s[1]) // 2) - target_offset))
    split_point_ms = start_search + ((best_silence[0] + best_silence[1]) // 2)
    
    silence_dur_ms = best_silence[1] - best_silence[0]
    print(f"  [OK] Found silence at {(split_point_ms/1000)/60:.2f} mins (duration: {silence_dur_ms}ms).")
    return split_point_ms

def apply_post_processing(in_wav, out_mp3):
    """Applies ACX compliance post-processing via FFmpeg (Peak -3.5dB, RMS ~-19dB, 256k CBR, 44.1kHz)."""
    # 2 seconds leading/trailing room tone silence
    silence_pad = AudioSegment.silent(duration=2000)
    body = AudioSegment.from_file(in_wav)
    padded = silence_pad + body + silence_pad
    
    tmp_padded_wav = in_wav + ".padded.wav"
    padded.export(tmp_padded_wav, format="wav")
    
    cmd = [
        "ffmpeg", "-y",
        "-i", tmp_padded_wav,
        "-af", "loudnorm=I=-19.0:TP=-3.5:LRA=11.0",
        "-ar", "44100",
        "-ac", "1",
        "-b:a", "256k",
        "-minrate", "256k",
        "-maxrate", "256k",
        "-bufsize", "256k",
        "-c:a", "libmp3lame",
        out_mp3
    ]
    
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    if os.path.exists(tmp_padded_wav):
        os.remove(tmp_padded_wav)

def split_chapter(orig_filename, part_a_filename, part_b_filename):
    orig_path = os.path.join(FINAL_AUDIO_DIR, orig_filename)
    if not os.path.exists(orig_path):
        print(f"[ERROR] Source file missing: {orig_path}")
        return False
        
    print(f"\n--- Splitting {orig_filename} ---")
    audio = AudioSegment.from_file(orig_path)
    total_ms = len(audio)
    print(f"  Total Duration: {(total_ms/1000)/60:.2f} mins | Size: {os.path.getsize(orig_path)/1024/1024:.2f} MB")
    
    # Strip leading/trailing 2s silence from original audio before splitting
    strip_ms = 2000
    core_audio = audio[strip_ms:total_ms - strip_ms] if total_ms > 2 * strip_ms else audio
    
    mid_ms = len(core_audio) // 2
    split_ms = find_best_split_point(core_audio, mid_ms)
    
    part_a = core_audio[:split_ms]
    part_b = core_audio[split_ms:]
    
    tmp_a_wav = os.path.join(FINAL_AUDIO_DIR, "tmp_a.wav")
    tmp_b_wav = os.path.join(FINAL_AUDIO_DIR, "tmp_b.wav")
    
    part_a.export(tmp_a_wav, format="wav")
    part_b.export(tmp_b_wav, format="wav")
    
    out_a_path = os.path.join(FINAL_AUDIO_DIR, part_a_filename)
    out_b_path = os.path.join(FINAL_AUDIO_DIR, part_b_filename)
    
    print(f"  Exporting Part A -> {part_a_filename}...")
    apply_post_processing(tmp_a_wav, out_a_path)
    
    print(f"  Exporting Part B -> {part_b_filename}...")
    apply_post_processing(tmp_b_wav, out_b_path)
    
    if os.path.exists(tmp_a_wav): os.remove(tmp_a_wav)
    if os.path.exists(tmp_b_wav): os.remove(tmp_b_wav)
    
    size_a = os.path.getsize(out_a_path) / (1024 * 1024)
    size_b = os.path.getsize(out_b_path) / (1024 * 1024)
    
    print(f"  [SUCCESS] Part A: {size_a:.2f} MB | Part B: {size_b:.2f} MB")
    
    # Delete original over-limit file
    os.remove(orig_path)
    print(f"  [CLEANUP] Deleted over-limit original file: {orig_filename}")
    return True

def main():
    for orig, part_a, part_b in TARGET_CHAPTERS:
        split_chapter(orig, part_a, part_b)
        
    print("\n==========================================")
    print("All long chapters successfully split!")
    print("==========================================")

if __name__ == "__main__":
    main()
