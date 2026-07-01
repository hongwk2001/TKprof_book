from pydub import AudioSegment

# Load the background music
print("Loading background.mp3...")
try:
    music = AudioSegment.from_mp3("background.mp3")
except Exception as e:
    print(f"Error loading music: {e}")
    exit(1)

# Extract a 15-second clip from the beginning (or from 10 seconds in to skip silence)
clip = music[10000:25000]

# Apply a 4-second fade-in and a 4-second fade-out
print("Applying fade-in and fade-out...")
faded_clip = clip.fade_in(4000).fade_out(4000)

# Save the sample
output_path = "fade_sample.mp3"
faded_clip.export(output_path, format="mp3")
print(f"Saved to {output_path}")
