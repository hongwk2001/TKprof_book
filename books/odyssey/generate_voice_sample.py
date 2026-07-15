import os
import asyncio
from io import BytesIO
import edge_tts
from pydub import AudioSegment
import subprocess

VOICES = {
    "Narrator": ("en-US-AndrewNeural", "This is the Narrator, voiced by Andrew Neural."),
    "Odysseus": ("en-US-BrianNeural", "I am Odysseus, king of Ithaca, voiced by Brian Neural."),
    "Telemachus": ("en-US-ChristopherNeural", "I am Telemachus, son of Odysseus, voiced by Christopher Neural."),
    "Others": ("en-US-EricNeural", "And I represent Nausicaa, Athena, and all other characters, voiced by Eric Neural.")
}

async def synthesize_segment(text, voice):
    communicate = edge_tts.Communicate(text, voice)
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    return AudioSegment.from_file(BytesIO(audio_data), format="mp3")

async def main():
    combined_audio = AudioSegment.empty()
    combined_audio += AudioSegment.silent(duration=1000) # leading silence
    
    for name, (voice, text) in VOICES.items():
        print(f"Synthesizing {name} ({voice})...")
        # Add label
        label_audio = await synthesize_segment(f"{name} voice.", "en-US-AndrewNeural")
        combined_audio += label_audio
        combined_audio += AudioSegment.silent(duration=500)
        
        # Add the actual sample text
        sample_audio = await synthesize_segment(text, voice)
        combined_audio += sample_audio
        combined_audio += AudioSegment.silent(duration=1500) # pause between voices
        
    combined_audio = combined_audio.set_frame_rate(44100).set_channels(2)
    
    # Export raw
    raw_path = "temp_voice_sample.mp3"
    combined_audio.export(raw_path, format="mp3", bitrate="256k")
    
    # Post-process
    final_path = "voice_sample.mp3"
    
    volume_norm = "loudnorm=I=-19:TP=-3.5:LRA=11"
    strip_silence = "silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0,areverse,silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0,areverse"
    leading_silence = "adelay=2000|2000"
    trailing_silence = "apad=pad_dur=2"
    
    filter_chain = f"{strip_silence},{volume_norm},{leading_silence},{trailing_silence}"
    
    cmd = [
        "ffmpeg", "-y", "-i", raw_path,
        "-af", filter_chain,
        "-ar", "44100",
        "-b:a", "256k",
        final_path
    ]
    
    subprocess.run(cmd, capture_output=True, text=True, check=True)
    os.remove(raw_path)
    print(f"Saved final voice sample to: {final_path}")

if __name__ == "__main__":
    asyncio.run(main())
