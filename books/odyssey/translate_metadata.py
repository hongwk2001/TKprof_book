import os
import sys
import json
import urllib.request
import urllib.error

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

import translate_back_to_en as tr

def translate_text(text, system_instruction, api_key):
    prompt = f"{system_instruction}\n\nText to translate:\n{text}"
    return tr.call_gemini_api(api_key, prompt)

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        # Load env first
        tr.load_env()
        api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("API Key not found!")
        sys.exit(1)
        
    intro_ko_path = os.path.join(BASE_DIR, "introduction_ko.txt")
    intro_en_path = os.path.join(BASE_DIR, "introduction_en.txt")
    
    copy_ko_path = os.path.join(BASE_DIR, "copyright_ko.txt")
    copy_en_path = os.path.join(BASE_DIR, "copyright_en.txt")
    
    system_instruction = (
        "You are an expert translator and editor. Translate the following Korean book matter "
        "into clear, natural, engaging, and professional English. Match the tone of a high-quality "
        "modernized classic edition for general audiences and young adults."
    )
    
    # 1. Translate Introduction
    if os.path.exists(intro_ko_path):
        print("Translating introduction...")
        with open(intro_ko_path, "r", encoding="utf-8") as f:
            intro_ko = f.read()
        intro_en = translate_text(intro_ko, system_instruction, api_key)
        if intro_en and intro_en != "QUOTA_EXHAUSTED":
            with open(intro_en_path, "w", encoding="utf-8") as f:
                f.write(intro_en)
            print("Saved introduction_en.txt")
            
    # 2. Translate Copyright
    if os.path.exists(copy_ko_path):
        print("Translating copyright/outro...")
        with open(copy_ko_path, "r", encoding="utf-8") as f:
            copy_ko = f.read()
        
        # We want to translate copyright_ko.txt into copyright_en.txt.
        # But let's refine the translation specifically for English version.
        # Note: in English version:
        # - "한국어 편역" should be "English translation and adaptation"
        # - "한국어 에디션" should be "English edition"
        # Let's instruct the model to localize the translation appropriately.
        localize_instruction = (
            "You are an expert translator and editor. Translate the following Korean book matter "
            "into clear, natural, engaging, and professional English. Make sure to adapt localized "
            "Korean references properly for the English edition. E.g., 'Korean edition/편역' should be "
            "translated as 'English edition/English translation and adaptation by TKPROF'."
        )
        copy_en = translate_text(copy_ko, localize_instruction, api_key)
        if copy_en and copy_en != "QUOTA_EXHAUSTED":
            with open(copy_en_path, "w", encoding="utf-8") as f:
                f.write(copy_en)
            print("Saved copyright_en.txt")

if __name__ == "__main__":
    main()
