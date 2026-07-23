import os
import sys
import re
import json
import asyncio
import subprocess
from io import BytesIO
import edge_tts
from pydub import AudioSegment

# Force UTF-8 encoding for stdout/stderr on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CHAPTERS_DIR = os.path.join(SCRIPT_DIR, "chapters")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "final_audio")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Voice Configurations (Male Voices Only as requested)
EN_NARRATOR = "en-US-AndrewNeural"
EN_DIALOGUE = "en-US-BrianNeural"
KO_VOICE_NARRATOR = "ko-KR-InJoonNeural"
KO_VOICE_DIALOGUE = "ko-KR-HyunsuMultilingualNeural"

async def synthesize_text_segment(text, voice, speed="+0%"):
    for attempt in range(5):
        try:
            communicate = edge_tts.Communicate(text, voice, rate=speed)
            audio_data = b""
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_data += chunk["data"]
            if audio_data:
                return AudioSegment.from_file(BytesIO(audio_data), format="mp3")
        except Exception as e:
            print(f"      [Retry {attempt + 1}/5] Failed to synthesize segment: {e}")
            await asyncio.sleep(2)
    raise RuntimeError(f"Failed to synthesize segment after 5 attempts: {text[:30]}...")

def map_sequential_to_book_ch(ch_num):
    if ch_num <= 9:
        return 1, ch_num
    elif ch_num <= 20:
        return 2, ch_num - 9
    else:
        return 3, ch_num - 20

def clean_bracketed_header(filepath):
    if not os.path.exists(filepath):
        return
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    lines = content.split("\n")
    # Find the first non-empty line
    first_non_empty_idx = -1
    for idx, line in enumerate(lines):
        if line.strip():
            first_non_empty_idx = idx
            break
            
    if first_non_empty_idx != -1:
        first_line = lines[first_non_empty_idx].strip()
        if first_line.startswith("[") and first_line.endswith("]"):
            print(f"  Removing duplicate header from {os.path.basename(filepath)}: '{first_line}'")
            # Remove that line and any leading/trailing blank lines around it
            lines.pop(first_non_empty_idx)
            # Re-join
            new_content = "\n".join(lines).strip()
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content + "\n")

async def generate_ko_audio(ch_num):
    book_num, inner_ch_num = map_sequential_to_book_ch(ch_num)
    ch_str = str(inner_ch_num).zfill(2)
    txt_path = os.path.join(CHAPTERS_DIR, f"book_{book_num}", f"ch_{ch_str}_ko.txt")
    out_path = os.path.join(OUTPUT_DIR, f"track_{str(ch_num).zfill(2)}_ko.mp3")

    if not os.path.exists(txt_path):
        print(f"  [Error] Korean text file not found: {txt_path}")
        return False

    print(f"  Generating Korean audio for Chapter {ch_num} (Book {book_num} Chapter {inner_ch_num}) (Male Voices: InJoon/Hyunsu)...")
    with open(txt_path, "r", encoding="utf-8") as f:
        text = f.read().strip()

    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    combined_audio = AudioSegment.empty()

    for idx, para in enumerate(paragraphs):
        # Parse dialogue using double quotes or Korean quotes
        parts = re.split(r'("[^"]*"|“[^”]*”)', para)
        for part in parts:
            part = part.strip()
            if not part:
                continue
            if (part.startswith('"') and part.endswith('"')) or (part.startswith('“') and part.endswith('”')):
                clean_text = part.strip('"“’’”').strip()
                if clean_text:
                    seg_audio = await synthesize_text_segment(clean_text, KO_VOICE_DIALOGUE, speed="+2%")
                    combined_audio += seg_audio
            else:
                seg_audio = await synthesize_text_segment(part, KO_VOICE_NARRATOR, speed="+0%")
                combined_audio += seg_audio
            combined_audio += AudioSegment.silent(duration=300)
        combined_audio += AudioSegment.silent(duration=500)

    combined_audio = combined_audio.set_frame_rate(44100).set_channels(2)
    combined_audio.export(out_path, format="mp3", bitrate="256k")
    print(f"  ✔ Successfully exported: {out_path}")
    return True

async def generate_en_audio(ch_num):
    book_num, inner_ch_num = map_sequential_to_book_ch(ch_num)
    ch_str = str(inner_ch_num).zfill(2)
    txt_path = os.path.join(CHAPTERS_DIR, f"book_{book_num}", f"ch_{ch_str}_en.txt")
    out_path = os.path.join(OUTPUT_DIR, f"track_{str(ch_num).zfill(2)}_en.mp3")

    if not os.path.exists(txt_path):
        print(f"  [Error] English text file not found: {txt_path}")
        return False

    print(f"  Generating English audio for Chapter {ch_num} (Book {book_num} Chapter {inner_ch_num}) (Dual Voice: Andrew/Brian)...")
    with open(txt_path, "r", encoding="utf-8") as f:
        text = f.read().strip()

    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    combined_audio = AudioSegment.empty()

    for p_idx, para in enumerate(paragraphs):
        # Parse dialogue using double-quotes
        parts = re.split(r'("[^"]*")', para)
        
        for part in parts:
            part = part.strip()
            if not part:
                continue
            
            if part.startswith('"') and part.endswith('"'):
                # Dialogue
                clean_text = part.replace('"', '').strip()
                if clean_text:
                    seg_audio = await synthesize_text_segment(clean_text, EN_DIALOGUE, speed="+2%")
                    combined_audio += seg_audio
            else:
                # Narration
                seg_audio = await synthesize_text_segment(part, EN_NARRATOR, speed="+0%")
                combined_audio += seg_audio
            
            # Short pause between segments
            combined_audio += AudioSegment.silent(duration=300)
            
        # Paragraph break pause
        combined_audio += AudioSegment.silent(duration=500)

    combined_audio = combined_audio.set_frame_rate(44100).set_channels(2)
    combined_audio.export(out_path, format="mp3", bitrate="256k")
    print(f"  ✔ Successfully exported: {out_path}")
    return True

def run_command(cmd):
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    if result.returncode != 0:
        print(f"Error executing command: {result.stderr}")
        return False
    print(result.stdout)
    return True

async def main():
    if len(sys.argv) < 2:
        print("Usage: python process_scaramouche.py <chapter_range e.g. 4-36 or single number e.g. 4>")
        sys.exit(1)

    range_str = sys.argv[1]
    if "-" in range_str:
        start, end = map(int, range_str.split("-"))
        chapters = list(range(start, end + 1))
    else:
        chapters = [int(range_str)]

    python_exe = os.path.join(SCRIPT_DIR, "..", "..", "venv", "Scripts", "python.exe")
    translate_script = os.path.join(SCRIPT_DIR, "..", "translate_book.py")
    modernize_script = os.path.join(SCRIPT_DIR, "..", "modernize_book.py")

    for ch in chapters:
        book_num, inner_ch_num = map_sequential_to_book_ch(ch)
        inner_ch_str = str(inner_ch_num).zfill(2)
        ch_str = str(ch).zfill(2)
        
        print(f"\n=================== Processing Chapter {ch_str} (Book {book_num} Chapter {inner_ch_num}) ===================")
        
        # Relative path of the raw file
        rel_raw_path = f"book_{book_num}/raw_ch_{inner_ch_str}.txt"
        
        # 1. Translate to Korean
        ko_txt_path = os.path.join(CHAPTERS_DIR, f"book_{book_num}", f"ch_{inner_ch_str}_ko.txt")
        if not os.path.exists(ko_txt_path):
            success = run_command([python_exe, translate_script, "--book", "scaramouche", "--chapters", rel_raw_path])
            if not success:
                print(f"Stopping execution due to translation failure on Chapter {ch}")
                sys.exit(1)
        else:
            print(f"  Korean translation already exists: {ko_txt_path}")

        # 2. Modernize English
        en_txt_path = os.path.join(CHAPTERS_DIR, f"book_{book_num}", f"ch_{inner_ch_str}_en.txt")
        if not os.path.exists(en_txt_path):
            success = run_command([python_exe, modernize_script, "--book", "scaramouche", "--chapters", rel_raw_path])
            if not success:
                print(f"Stopping execution due to modernization failure on Chapter {ch}")
                sys.exit(1)
        else:
            print(f"  English modernization already exists: {en_txt_path}")

        # 3. Clean up duplicated headers
        clean_bracketed_header(ko_txt_path)
        clean_bracketed_header(en_txt_path)

        # 4. Generate Audio (Korean)
        await generate_ko_audio(ch)

        # 5. Generate Audio (English)
        await generate_en_audio(ch)

    print("\nAll requested chapters processed successfully!")

if __name__ == "__main__":
    asyncio.run(main())
