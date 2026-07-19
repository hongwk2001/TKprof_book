import asyncio
import os
import sys
import edge_tts

# Force UTF-8 encoding for stdout and stderr to prevent UnicodeEncodeError on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CHAPTERS_DIR = os.path.join(SCRIPT_DIR, "chapters")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "final_audio")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Recommended narrator voice for Korean
VOICE = "ko-KR-SunHiNeural"

async def generate_track(ch_num):
    ch_str = str(ch_num).zfill(2)
    txt_filename = f"ch_{ch_str}_ko.txt"
    txt_path = os.path.join(CHAPTERS_DIR, txt_filename)
    out_filename = f"track_{ch_str}_ko.mp3"
    out_path = os.path.join(OUTPUT_DIR, out_filename)
    
    if not os.path.exists(txt_path):
        print(f"File not found: {txt_path}")
        return False
        
    print(f"Reading {txt_filename}...")
    with open(txt_path, "r", encoding="utf-8") as f:
        text = f.read().strip()
        
    print(f"Synthesizing Chapter {ch_num} with {VOICE}...")
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(out_path)
    print(f"✔ Success! Chapter {ch_num} saved to: {out_path}")
    return True

async def main():
    chapters = [1, 2, 3]
    for ch in chapters:
        await generate_track(ch)

if __name__ == "__main__":
    asyncio.run(main())
