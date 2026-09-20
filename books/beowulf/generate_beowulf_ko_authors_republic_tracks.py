import os
import sys
import asyncio
import subprocess
import soundfile as sf
import edge_tts
from pydub import AudioSegment

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
FINAL_KO_DIR = os.path.join(SCRIPT_DIR, "final_audio_ko")
TEMP_DIR = os.path.join(SCRIPT_DIR, "temp_audio")

os.makedirs(FINAL_KO_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

VOICE_KO = "ko-KR-SunHiNeural"

async def synthesize_edge(text, out_mp3_path):
    communicate = edge_tts.Communicate(text, VOICE_KO)
    await communicate.save(out_mp3_path)

def apply_acx_post_processing(raw_path, clean_path, bitrate=256):
    volume_norm = "loudnorm=I=-19:TP=-3.5:LRA=7"
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
        print(f"[ERROR] FFmpeg failed: {e.stderr}", file=sys.stderr)
        return False

def verify_audio_quality(mp3_path):
    checker_script = os.path.join(PROJECT_ROOT, "check_audio_quality.py")
    if not os.path.exists(checker_script):
        return True
    cmd = [sys.executable, checker_script, mp3_path]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"[QUALITY CHECK PASSED] {os.path.basename(mp3_path)}")
            return True
        else:
            print(f"[QUALITY CHECK WARNING] {res.stdout.strip()}")
            return False
    except Exception as e:
        print(f"[QUALITY CHECK ERROR] {e}")
        return False

def generate_opening_credits():
    print("\n--- Generating Beowulf Korean Opening Credits (Authors Republic Spec) ---")
    ko_text = "베오울프. 고대 영웅 서사시 무삭제 한국어 오디오북. 저자: 작자 미상. 낭독: 한국어 성우진."
    raw_mp3 = os.path.join(TEMP_DIR, "raw_beowulf_opening_credits.mp3")
    final_mp3 = os.path.join(FINAL_KO_DIR, "opening_credits.mp3")

    asyncio.run(synthesize_edge(ko_text, raw_mp3))
    apply_acx_post_processing(raw_mp3, final_mp3)
    verify_audio_quality(final_mp3)

def generate_closing_credits():
    print("\n--- Generating Beowulf Korean Closing Credits (Authors Republic Spec) ---")
    ko_text = "이것으로 베오울프 한국어 오디오북의 모든 낭독을 마칩니다. 저자: 작자 미상. 끝."
    raw_mp3 = os.path.join(TEMP_DIR, "raw_beowulf_closing_credits.mp3")
    final_mp3 = os.path.join(FINAL_KO_DIR, "closing_credits.mp3")

    asyncio.run(synthesize_edge(ko_text, raw_mp3))
    apply_acx_post_processing(raw_mp3, final_mp3)
    verify_audio_quality(final_mp3)

def generate_sample():
    print("\n--- Generating Beowulf Korean Retail Sample (4.5 Minutes) ---")
    ch1_path = os.path.join(FINAL_KO_DIR, "final_track_01.mp3")
    raw_sample = os.path.join(TEMP_DIR, "raw_beowulf_sample.mp3")
    final_sample = os.path.join(FINAL_KO_DIR, "sample.mp3")

    if os.path.exists(ch1_path):
        audio = AudioSegment.from_mp3(ch1_path)
        sample_audio = audio[:270000] # 4m 30s
        sample_audio.export(raw_sample, format="mp3", bitrate="256k")
        apply_acx_post_processing(raw_sample, final_sample)
        verify_audio_quality(final_sample)

def main():
    generate_opening_credits()
    generate_closing_credits()
    generate_sample()

if __name__ == "__main__":
    main()
