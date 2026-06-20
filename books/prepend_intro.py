import os
import sys
import subprocess
import asyncio
import edge_tts

# Force UTF-8 stdout/stderr to handle Korean characters in logs on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = r"d:\git_repo\thefirstaicompany\books"
TEMP_DIR = os.path.join(BASE_DIR, "temp_intro")

# Configurations for books
BOOKS_CONFIG = {
    "gilgamesh": {
        "title_en": "The Epic of Gilgamesh",
        "title_ko": "길가메시 서사시",
        "author_en": "unknown authors",
        "author_ko": "작자 미상",
        "year_en": "ancient Mesopotamia",
        "year_ko": "고대 메索포타미아",
        "files": {
            "chapters": [1, 2, 3, 4, 5, 6],
            "podcasts": [1, 2]
        }
    },
    "christmas_carol": {
        "title_en": "A Christmas Carol",
        "title_ko": "크리스마스 캐럴",
        "author_en": "Charles Dickens",
        "author_ko": "찰스 디킨스",
        "year_en": "eighteen forty-three",
        "year_ko": "십팔백사십삼년",
        "files": {
            "chapters": [1, 2, 3, 4, 5],
            "podcasts": []
        }
    }
}

VOICES = {
    "en": "en-US-JennyNeural",
    "ko": "ko-KR-HyunsuMultilingualNeural"
}

def get_intro_text(book_id, lang):
    cfg = BOOKS_CONFIG[book_id]
    if lang == "en":
        if book_id == "gilgamesh":
            return (
                f"{cfg['title_en']}, written in ancient Mesopotamia. "
                "This edition is adapted into clear, modern English, choosing content over play of words, "
                "designed for language learners and casual listeners who want to enjoy the story without grueling language barriers."
            )
        else:
            return (
                f"{cfg['title_en']}, written by {cfg['author_en']} in {cfg['year_en']}. "
                "This edition is adapted into clear, modern English, choosing content over play of words, "
                "designed for language learners and casual listeners who want to enjoy the story without grueling language barriers."
            )
    elif lang == "ko":
        return (
            f"고전 원문을 에이아이를 이용한 이천이십육년식 새 번역으로 만나는 {cfg['title_ko']}. "
            "수사적 기교보다 원작의 내용에 집중하여, 어학 학습자와 편안한 감상을 원하는 일반 청취자 모두가 쉽게 즐길 수 있도록 쉽고 직관적으로 구성했습니다."
        )

async def generate_intro_audio(text, voice, out_path):
    print(f"  Generating intro audio: '{text[:50]}...' -> {out_path}")
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(out_path)

def prepend_audio(intro_path, original_path, output_path):
    print(f"  Concatenating {intro_path} and {original_path} to {output_path}...")
    # Using ffmpeg complex filter to resample and concatenate cleanly
    cmd = [
        "ffmpeg", "-y",
        "-i", intro_path,
        "-i", original_path,
        "-filter_complex", "[0:a][1:a]concat=n=2:v=0:a=1[a]",
        "-map", "[a]",
        "-codec:a", "libmp3lame",
        "-b:a", "128k",
        output_path
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"  [Error] FFmpeg failed: {e.stderr.decode('utf-8', errors='ignore')}")
        return False

async def main():
    os.makedirs(TEMP_DIR, exist_ok=True)
    
    for book_id, config in BOOKS_CONFIG.items():
        print(f"\nProcessing book: {book_id}")
        book_dir = os.path.join(BASE_DIR, book_id)
        audio_dir = os.path.join(book_dir, "audio")
        
        # 1. Pre-generate Intro Audios
        intro_paths = {}
        for lang in ["en", "ko"]:
            intro_text = get_intro_text(book_id, lang)
            intro_file = os.path.join(TEMP_DIR, f"{book_id}_intro_{lang}.mp3")
            await generate_intro_audio(intro_text, VOICES[lang], intro_file)
            intro_paths[lang] = intro_file
            
        # 2. Process Chapters
        for ch in config["files"]["chapters"]:
            for lang in ["en", "ko"]:
                filename = f"ch_{ch:02d}_{lang}.mp3"
                original_path = os.path.join(audio_dir, filename)
                if not os.path.exists(original_path):
                    print(f"  [Warning] Original file not found: {original_path}")
                    continue
                
                temp_out = os.path.join(TEMP_DIR, f"temp_{filename}")
                success = prepend_audio(intro_paths[lang], original_path, temp_out)
                if success:
                    # Overwrite original
                    if os.path.exists(original_path):
                        os.remove(original_path)
                    os.rename(temp_out, original_path)
                    print(f"  Successfully prepended intro to {filename}")

        # 3. Process Podcasts (Gilgamesh parts)
        for part in config["files"]["podcasts"]:
            for lang in ["en", "ko"]:
                filename = f"podcast_prt_{part}_{lang}.mp3"
                original_path = os.path.join(audio_dir, filename)
                if not os.path.exists(original_path):
                    print(f"  [Warning] Original file not found: {original_path}")
                    continue
                
                temp_out = os.path.join(TEMP_DIR, f"temp_{filename}")
                success = prepend_audio(intro_paths[lang], original_path, temp_out)
                if success:
                    # Overwrite original
                    if os.path.exists(original_path):
                        os.remove(original_path)
                    os.rename(temp_out, original_path)
                    print(f"  Successfully prepended intro to {filename}")

    # Clean up temp folder
    print("\nCleaning up temporary files...")
    for f in os.listdir(TEMP_DIR):
        try:
            os.remove(os.path.join(TEMP_DIR, f))
        except:
            pass
    try:
        os.rmdir(TEMP_DIR)
    except:
        pass
        
    print("Prepend intro pipeline completed!")

if __name__ == "__main__":
    asyncio.run(main())
