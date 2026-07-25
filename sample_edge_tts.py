import asyncio
import edge_tts
import argparse
import os

async def generate_speech(text: str, voice: str, output_path: str):
    """Generates audio from text using Edge-TTS and saves it to output_path."""
    print(f"Generating audio using voice '{voice}'...")
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)
    print(f"Success! Audio saved to: {os.path.abspath(output_path)}")

def main():
    parser = argparse.ArgumentParser(description="Sample speech generator using Edge-TTS")
    parser.add_argument("--text", default="Hello! This is a test of the Microsoft Edge Text-to-Speech system. It is fast and free.", help="Text to convert to speech")
    parser.add_argument("--voice", default="en-US-GuyNeural", help="Edge-TTS voice name (e.g., en-US-GuyNeural, en-GB-SoniaNeural, ko-KR-SunHiNeural)")
    parser.add_argument("--output", default="sample_edge_output.mp3", help="Output file path (.mp3 or .wav)")

    args = parser.parse_args()
    
    # Run the async function
    asyncio.run(generate_speech(args.text, args.voice, args.output))

if __name__ == "__main__":
    main()
