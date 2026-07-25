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

VOICE = "en-US-AndrewNeural"

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
    print("=== Generating Audio for Seneca: On the Shortness of Life ===")

    # 1. Opening Track (Strict Authors Republic Rule: Title, Author, Narrator only)
    opening_text = "On the Shortness of Life. Written by Lucius Annaeus Seneca. Narrated by Andrew."
    raw_opening = os.path.join(TEMP_DIR, "raw_opening.mp3")
    final_opening = os.path.join(FINAL_DIR, "final_track_00_opening.mp3")
    print("Generating Opening Track...")
    generate_tts(opening_text, raw_opening)
    process_track(raw_opening, final_opening)

    # 2. Introduction & Overview Track
    intro_txt = os.path.join(BASE_DIR, "introduction_en.txt")
    raw_intro = os.path.join(TEMP_DIR, "raw_intro.mp3")
    final_intro = os.path.join(FINAL_DIR, "final_track_01_introduction.mp3")
    print("Generating Introduction Track...")
    if generate_tts_file(intro_txt, raw_intro):
        process_track(raw_intro, final_intro)

    # 3. Chapter Tracks (1 to 20)
    chapter_titles = [
        "Chapter One: The Complaint of Short Life",
        "Chapter Two: How Men Waste Time",
        "Chapter Three: Guarding Your Life's Hours",
        "Chapter Four: Augustus and the Longing for Leisure",
        "Chapter Five: Cicero's Struggle with Public Life",
        "Chapter Six: Livius Drusus and Restless Ambition",
        "Chapter Seven: The Distracted Mind",
        "Chapter Eight: The Illusion of Endless Time",
        "Chapter Nine: Living in the Present",
        "Chapter Ten: The Three Times of Life",
        "Chapter Eleven: The Fear of Death",
        "Chapter Twelve: The Trifles of Trivial Pursuits",
        "Chapter Thirteen: Pedantry versus Wisdom",
        "Chapter Fourteen: Friendship with Great Minds",
        "Chapter Fifteen: True Immortality",
        "Chapter Sixteen: The Anxiety of the Busy",
        "Chapter Seventeen: The Sudden End of Power",
        "Chapter Eighteen: Paulinus Advice to Retire",
        "Chapter Nineteen: The Dignity of Philosophy",
        "Chapter Twenty: The Tranquil Conclusion"
    ]

    for i in range(1, 21):
        ch_str = str(i).zfill(2)
        txt_file = os.path.join(CHAPTERS_DIR, f"ch_{ch_str}_en.txt")
        raw_ch = os.path.join(TEMP_DIR, f"raw_ch_{ch_str}.mp3")
        track_num = str(i + 1).zfill(2)
        final_ch = os.path.join(FINAL_DIR, f"final_track_{track_num}_chapter_{ch_str}.mp3")
        
        print(f"Generating Track {track_num} (Chapter {i})...")
        if generate_tts_file(txt_file, raw_ch):
            process_track(raw_ch, final_ch)

    # 4. Closing Track
    closing_text = "This concludes the audiobook of On the Shortness of Life, written by Lucius Annaeus Seneca, narrated by Andrew. Copyright 2026 by Antigravity Classics. All rights reserved."
    raw_closing = os.path.join(TEMP_DIR, "raw_closing.mp3")
    final_closing = os.path.join(FINAL_DIR, f"final_track_22_closing.mp3")
    print("Generating Closing Track...")
    generate_tts(closing_text, raw_closing)
    process_track(raw_closing, final_closing)

    # 5. Retail Sample (Chapters 1 snippet)
    sample_text = "On the Shortness of Life by Lucius Annaeus Seneca. Chapter One: The Complaint of Short Life. Most human beings, Paulinus, complain about the meanness of nature, because we are born for a brief span of life, and because this allotment of time runs away so swiftly and so hurriedly. Life is long enough, and a sufficiently generous amount has been given to us for the highest achievements if it were all well invested."
    raw_sample = os.path.join(TEMP_DIR, "raw_sample.mp3")
    final_sample = os.path.join(FINAL_DIR, "sample.mp3")
    print("Generating Retail Sample...")
    generate_tts(sample_text, raw_sample)
    process_track(raw_sample, final_sample)

    print("\nAudiobook generation and normalization complete!")

if __name__ == "__main__":
    main()
