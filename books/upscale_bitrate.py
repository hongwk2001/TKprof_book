import os
import subprocess

BASE_DIR = r"d:\git_repo\thefirstaicompany\books"

BOOKS = ["gilgamesh", "christmas_carol"]

def upscale_file(filepath):
    temp_path = filepath.replace(".mp3", "_temp.mp3")
    print(f"Upscaling {os.path.basename(filepath)} to 192kbps...")
    
    cmd = [
        "ffmpeg", "-y",
        "-i", filepath,
        "-ar", "44100",
        "-codec:a", "libmp3lame",
        "-b:a", "256k",
        temp_path
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        # Overwrite original file
        if os.path.exists(filepath):
            os.remove(filepath)
        os.rename(temp_path, filepath)
        print(f"  Successfully upscaled {os.path.basename(filepath)}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  [Error] FFmpeg failed for {filepath}: {e.stderr.decode('utf-8', errors='ignore')}")
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return False

def main():
    for book in BOOKS:
        book_audio_dir = os.path.join(BASE_DIR, book, "audio")
        if not os.path.exists(book_audio_dir):
            continue
            
        print(f"\nScanning audio directory for {book}...")
        for filename in os.listdir(book_audio_dir):
            if filename.endswith(".mp3"):
                filepath = os.path.join(book_audio_dir, filename)
                upscale_file(filepath)
                
    print("\nBitrate upscaling completed!")

if __name__ == "__main__":
    main()
