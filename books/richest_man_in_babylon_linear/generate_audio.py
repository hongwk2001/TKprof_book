import os
import glob
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")
OUTPUT_DIR = os.path.join(BASE_DIR, "final_audio")
INTRO_PATH = os.path.join(BASE_DIR, "freesound_community-cinematic-intro-6097.mp3")

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def main():
    # Verify intro sound exists
    if not os.path.exists(INTRO_PATH):
        print(f"Error: Cinematic intro not found at {INTRO_PATH}")
        return

    # Find all chapter files
    chapter_files = glob.glob(os.path.join(CHAPTERS_DIR, "ch_*.txt"))
    chapter_files.sort()
    
    if not chapter_files:
        print("No chapters found in", CHAPTERS_DIR)
        return
        
    num_chapters = len(chapter_files)
    print(f"Found {num_chapters} chapters to generate.")
    
    for idx, txt_path in enumerate(chapter_files, 1):
        filename = os.path.basename(txt_path)
        base_name = os.path.splitext(filename)[0]
        is_last = (idx == num_chapters)
        
        # Output paths
        temp_raw = os.path.join(OUTPUT_DIR, f"temp_{base_name}.mp3")
        out_mp3 = os.path.join(OUTPUT_DIR, f"{base_name}.mp3")
        
        print(f"\n--- Processing Chapter {idx}: {filename} ---")
        print(f"1. Generating raw TTS -> {os.path.basename(temp_raw)}...")
        
        # Run edge-tts command
        tts_cmd = [
            "edge-tts",
            "--voice", "en-US-SteffanNeural",
            "--file", txt_path,
            "--write-media", temp_raw
        ]
        
        try:
            subprocess.run(tts_cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error generating raw TTS for {filename}: {e}")
            continue

        print(f"2. Mixing cinematic intro with narration -> {os.path.basename(out_mp3)}...")
        
        # Define ffmpeg inputs and filters
        ffmpeg_cmd = ["ffmpeg", "-y"]
        
        if idx == 1:
            # Full cinematic opening for Chapter 1
            filter_complex = "[0:a]afade=t=out:st=4.5:d=4[music]; [1:a]adelay=4500|4500[voice]; [music][voice]amix=inputs=2:duration=longest[a]"
            ffmpeg_cmd.extend([
                "-i", INTRO_PATH,
                "-i", temp_raw,
                "-filter_complex", filter_complex,
                "-map", "[a]",
                out_mp3
            ])
        elif is_last:
            # Short bumper at start + full cinematic outro at the end for Chapter 11
            filter_complex = "[0:a]afade=t=out:st=1:d=2.5,volume=0.6[bumper]; [1:a]adelay=1500|1500[voice]; [bumper][voice]amix=inputs=2:duration=longest[mixed]; [mixed][2:a]concat=n=2:v=0:a=1[a]"
            ffmpeg_cmd.extend([
                "-i", INTRO_PATH,
                "-i", temp_raw,
                "-i", INTRO_PATH,
                "-filter_complex", filter_complex,
                "-map", "[a]",
                out_mp3
            ])
        else:
            # Short transitional bumper for middle chapters
            filter_complex = "[0:a]afade=t=out:st=1:d=2.5,volume=0.6[music]; [1:a]adelay=1500|1500[voice]; [music][voice]amix=inputs=2:duration=longest[a]"
            ffmpeg_cmd.extend([
                "-i", INTRO_PATH,
                "-i", temp_raw,
                "-filter_complex", filter_complex,
                "-map", "[a]",
                out_mp3
            ])
        
        try:
            # Run ffmpeg with stdout/stderr suppressed to keep logs clean
            subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"Successfully compiled: {os.path.basename(out_mp3)}")
        except subprocess.CalledProcessError as e:
            print(f"Error mixing audio for {filename}: {e}")
        finally:
            # Clean up raw temp file
            if os.path.exists(temp_raw):
                os.remove(temp_raw)

if __name__ == "__main__":
    main()
