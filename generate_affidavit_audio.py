import os
import re
import sys
import asyncio
import edge_tts
from io import BytesIO
from pydub import AudioSegment
from fix_audio_quality import fix_audio_file

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEXT_FILE = os.path.join(BASE_DIR, "sungmin_text_to_audio.txt")
RAW_OUTPUT = os.path.join(BASE_DIR, "raw_affidavit.mp3")
FINAL_OUTPUT = os.path.join(BASE_DIR, "kat_lynnwood_affidavit.mp3")

VOICE = "en-US-EmmaNeural"

def parse_text():
    with open(TEXT_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    cleaned_paragraphs = []
    
    for line in lines:
        line = line.strip()
        # Skip headers, page annotations, and divider lines
        if not line:
            continue
        if line.startswith("Here is the full text"):
            continue
        if line.startswith("---"):
            continue
        if line.startswith("### Page"):
            continue
            
        # Clean formatting
        line = re.sub(r'\*\*AFFIDAVIT OF KAT LYNNWOOD\*\*', 'Affidavit of Kat Lynnwood', line)
        line = line.replace(r"\s\ ", "Signed: ")
        
        cleaned_paragraphs.append(line)
        
    return "\n\n".join(cleaned_paragraphs)

async def synthesize_text(text):
    print("Synthesizing audio using edge-tts...")
    communicate = edge_tts.Communicate(text, VOICE)
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
            
    audio_seg = AudioSegment.from_file(BytesIO(audio_data), format="mp3")
    # Format to stereo, 44.1kHz
    audio_seg = audio_seg.set_frame_rate(44100).set_channels(2)
    audio_seg.export(RAW_OUTPUT, format="mp3", bitrate="256k")
    print(f"Saved raw audio to {RAW_OUTPUT}")

def run_post_processing():
    print("Running fix_audio_file on raw audio...")
    # Clean output path first if exists
    if os.path.exists(FINAL_OUTPUT):
        os.remove(FINAL_OUTPUT)
        
    try:
        success = fix_audio_file(RAW_OUTPUT, FINAL_OUTPUT)
        if success and os.path.exists(FINAL_OUTPUT):
            print(f"Post-processed audio saved to: {FINAL_OUTPUT}")
            if os.path.exists(RAW_OUTPUT):
                os.remove(RAW_OUTPUT)
            return True
        else:
            print("Error: Post-processing failed or output file not found.")
            return False
    except Exception as e:
        print(f"Post-processing failed with exception: {e}")
        return False


async def main():
    if not os.path.exists(TEXT_FILE):
        print(f"Error: Text file not found at {TEXT_FILE}")
        sys.exit(1)
        
    text = parse_text()
    print("Parsed text to read:")
    print("==================================================")
    print(text[:300] + "...")
    print("==================================================")
    
    await synthesize_text(text)
    if run_post_processing():
        print("Success! Process complete.")
        sys.exit(0)
    else:
        print("Error during post-processing.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
