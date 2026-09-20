import os
import sys
import asyncio
from generate_audio_qwen import generate_chapter

def main():
    print("==================================================")
    print("Dracula Full Batch Audiobook Production (GPU)")
    print("==================================================")

    lang_arg = sys.argv[1].lower() if len(sys.argv) > 1 else "both"

    langs = ["en", "ko"] if lang_arg == "both" else [lang_arg]

    for lang in langs:
        print(f"\n>>> Starting Production for Language: {lang.upper()} <<<")
        for ch in range(1, 28):
            print(f"\n--- Chapter {ch}/27 ({lang.upper()}) ---")
            success = asyncio.run(generate_chapter(lang, ch))
            if not success:
                print(f"[WARNING] Chapter {ch} ({lang}) failed. Retrying...")
                asyncio.run(generate_chapter(lang, ch))

    print("\n==================================================")
    print("🎉 All 27 Chapters Completed for Dracula!")
    print("==================================================")

if __name__ == "__main__":
    main()
