import asyncio
import edge_tts

TEXT = "I am Arkad, the richest man in Babylon. Remember this truth: A part of all you earn is yours to keep. It should be not less than a tenth, no matter how little you earn."

VOICES = [
    "en-US-GuyNeural",
    "en-US-ChristopherNeural",
    "en-US-SteffanNeural",
    "en-GB-RyanNeural",
    "en-GB-ThomasNeural"
]

async def main():
    for voice in VOICES:
        print(f"Generating sample for {voice}...")
        communicate = edge_tts.Communicate(TEXT, voice)
        filename = f"sample_{voice.replace('en-', '').replace('Neural', '')}.mp3"
        await communicate.save(filename)
        print(f"Saved {filename}")

if __name__ == "__main__":
    asyncio.run(main())
