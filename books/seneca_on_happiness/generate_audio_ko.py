import os
import sys
import subprocess
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(BASE_DIR))
sys.path.append(PROJECT_ROOT)

from fix_audio_quality import fix_audio_file
from check_audio_quality import check_file

TEMP_DIR = os.path.join(BASE_DIR, "temp_audio")
FINAL_DIR = os.path.join(BASE_DIR, "final_audio")
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(FINAL_DIR, exist_ok=True)

VOICE = "ko-KR-InJoonNeural"

def run_cmd(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error executing command: {' '.join(cmd)}\n{result.stderr}")
        raise Exception(f"Command failed")

def generate_tts(text, out_raw_file):
    cmd = ["edge-tts", "--text", text, "--voice", VOICE, "--write-media", out_raw_file]
    run_cmd(cmd)

def generate_tts_file(txt_file, out_raw_file):
    if not os.path.exists(txt_file):
        return False
    cmd = ["edge-tts", "--file", txt_file, "--voice", VOICE, "--write-media", out_raw_file]
    run_cmd(cmd)
    return True

def process_track(raw_file, final_file):
    success = fix_audio_file(raw_file, final_file, bitrate=256)
    if success:
        res = check_file(final_file)
        if res and res["status"] == "PASS":
            print(f"  [PASS] {os.path.basename(final_file)} (Peak: {res['peak_db']:.2f}dB, RMS: {res['rms_db']:.2f}dB)")
        else:
            print(f"  [FAIL/WARN] {os.path.basename(final_file)}: {res.get('errors')}")
    else:
        print(f"  [ERROR] Failed to normalize {raw_file}")

def main():
    print("=== Generating Korean Audio for Seneca: Of a Happy Life ===")

    # 1. Opening Track
    opening_text = "행복한 삶에 관하여. 루키우스 안나에우스 세네카 지음. 인준 낭독."
    raw_opening = os.path.join(TEMP_DIR, "raw_opening_ko.mp3")
    final_opening = os.path.join(FINAL_DIR, "final_track_00_opening_ko.mp3")
    print("Generating Opening Track...")
    generate_tts(opening_text, raw_opening)
    process_track(raw_opening, final_opening)

    # 2. Introduction Track
    intro_txt = os.path.join(BASE_DIR, "introduction_ko.txt")
    raw_intro = os.path.join(TEMP_DIR, "raw_intro_ko.mp3")
    final_intro = os.path.join(FINAL_DIR, "final_track_01_introduction_ko.mp3")
    print("Generating Introduction Track...")
    if generate_tts_file(intro_txt, raw_intro):
        process_track(raw_intro, final_intro)

    # 3. Chapter Tracks (1 to 28)
    for i in range(1, 29):
        ch_str = str(i).zfill(2)
        txt_file = os.path.join(CHAPTERS_DIR, f"ch_{ch_str}_ko.txt")
        raw_ch = os.path.join(TEMP_DIR, f"raw_ch_{ch_str}_ko.mp3")
        track_num = str(i + 1).zfill(2)
        final_ch = os.path.join(FINAL_DIR, f"final_track_{track_num}_chapter_{ch_str}_ko.mp3")
        
        print(f"Generating Track {track_num} (Chapter {i} KO)...")
        if generate_tts_file(txt_file, raw_ch):
            process_track(raw_ch, final_ch)

    # 4. Closing Track
    closing_text = "행복한 삶에 관하여 오디오북 낭독을 마칩니다. 세네카 지음, 인준 낭독. 저작권 2026년 Antigravity Classics. 판권 소유."
    raw_closing = os.path.join(TEMP_DIR, "raw_closing_ko.mp3")
    final_closing = os.path.join(FINAL_DIR, "final_track_30_closing_ko.mp3")
    print("Generating Closing Track...")
    generate_tts(closing_text, raw_closing)
    process_track(raw_closing, final_closing)

    # 5. Retail Sample
    sample_text = "행복한 삶에 관하여. 루키우스 안나에우스 세네카 지음. 1장. 갈리오 형제여, 누구나 행복한 삶을 원하지만, 무엇이 삶을 행복하게 만드는지 아는 사람은 거의 없습니다. 사실 행복을 얻는 일은 대단히 어렵습니다."
    raw_sample = os.path.join(TEMP_DIR, "raw_sample_ko.mp3")
    final_sample = os.path.join(FINAL_DIR, "sample_ko.mp3")
    print("Generating Retail Sample...")
    generate_tts(sample_text, raw_sample)
    process_track(raw_sample, final_sample)

    print("\nKorean Audiobook generation and normalization complete!")

if __name__ == "__main__":
    main()
