import os

BASE_DIR = r"d:\git_repo\TKprof_book\books\secret_garden"
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")

def main():
    print("Calculating word counts...")
    
    total_en_words = 0
    total_ko_chars = 0
    total_ko_words = 0
    
    for i in range(1, 28):
        en_path = os.path.join(CHAPTERS_DIR, f"ch_{i:02d}_en.txt")
        ko_path = os.path.join(CHAPTERS_DIR, f"ch_{i:02d}_ko.txt")
        
        if os.path.exists(en_path):
            with open(en_path, "r", encoding="utf-8") as f:
                en_text = f.read()
                words = en_text.split()
                total_en_words += len(words)
                
        if os.path.exists(ko_path):
            with open(ko_path, "r", encoding="utf-8") as f:
                ko_text = f.read()
                # Word/eojeol count
                total_ko_words += len(ko_text.split())
                # Character count without spaces
                total_ko_chars += len([c for c in ko_text if not c.isspace()])
                
    print(f"English Total Words: {total_en_words}")
    print(f"Korean Total Words (Eojeol): {total_ko_words}")
    print(f"Korean Total Characters (no spaces): {total_ko_chars}")
    
    # Estimating reading times
    # Silent reading: English average ~225 WPM, Korean average ~350 Eojeol/min
    en_silent_min = total_en_words / 225
    ko_silent_min = total_ko_words / 300
    
    # Audio narration (Audiobook runtime): English average ~155 WPM, Korean average ~220 Eojeol/min
    en_audio_min = total_en_words / 155
    ko_audio_min = total_ko_words / 200
    
    print(f"\nEstimated English Reading Time (Silent): {int(en_silent_min // 60)}h {int(en_silent_min % 60)}m")
    print(f"Estimated English Audiobook Runtime: {int(en_audio_min // 60)}h {int(en_audio_min % 60)}m")
    
    print(f"\nEstimated Korean Reading Time (Silent): {int(ko_silent_min // 60)}h {int(ko_silent_min % 60)}m")
    print(f"Estimated Korean Audiobook Runtime: {int(ko_audio_min // 60)}h {int(ko_audio_min % 60)}m")

if __name__ == "__main__":
    main()
