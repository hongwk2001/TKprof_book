import os
from pydub import AudioSegment

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FINAL_DIR = os.path.join(BASE_DIR, "books", "secret_garden", "final_audio")

def main():
    ch1_path = os.path.join(FINAL_DIR, "final_track_02.mp3")
    sample_out = os.path.join(FINAL_DIR, "sample.mp3")
    
    if not os.path.exists(ch1_path):
        print("Error: final_track_02.mp3 not found!")
        return
        
    print("Loading normalized final_track_02.mp3...")
    audio = AudioSegment.from_mp3(ch1_path)
    
    # Slicing: take the first 4m 28s (268,000 ms)
    # The first 2.0s is already leading silence.
    print("Slicing first 268 seconds...")
    cut_audio = audio[:268000]
    
    # Apply fade out on the last 4 seconds (from 264s to 268s)
    print("Applying fade out...")
    faded_audio = cut_audio.fade_out(4000)
    
    # Append exactly 2 seconds of clean silence (2000 ms)
    print("Adding trailing silence...")
    silence = AudioSegment.silent(duration=2000, frame_rate=44100)
    final_sample = faded_audio + silence
    
    print(f"Exporting to {sample_out}...")
    final_sample.export(sample_out, format="mp3", bitrate="256k", parameters=["-ar", "44100"])
    print("Sample track generation completed!")

if __name__ == "__main__":
    main()
