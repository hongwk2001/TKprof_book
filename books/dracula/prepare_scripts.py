import os
import sys
import re
import json
import glob

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Heuristics for dialogue speaker classification in Dracula
FEMALE_KEYWORDS = re.compile(
    r"\b(she|her|herself|mina|lucie|lucy|mrs|madam|lady|woman|girl|mother|sister|bride|vampire)\b", 
    re.IGNORECASE
)

DRACULA_KEYWORDS = re.compile(
    r"\b(dracula|count|nobleman|host|master|vampire|monster)\b",
    re.IGNORECASE
)

VAN_HELSING_KEYWORDS = re.compile(
    r"\b(helsing|professor|doctor|seward|arthur|godalming|quincey|morris|renfield)\b",
    re.IGNORECASE
)

ROMAN_TO_WORDS_EN = {
    "I": "One", "II": "Two", "III": "Three", "IV": "Four", "V": "Five",
    "VI": "Six", "VII": "Seven", "VIII": "Eight", "IX": "Nine", "X": "Ten",
    "XI": "Eleven", "XII": "Twelve", "XIII": "Thirteen", "XIV": "Fourteen",
    "XV": "Fifteen", "XVI": "Sixteen", "XVII": "Seventeen", "XVIII": "Eighteen",
    "XIX": "Nineteen", "XX": "Twenty", "XXI": "Twenty-One", "XXII": "Twenty-Two",
    "XXIII": "Twenty-Three", "XXIV": "Twenty-Four", "XXV": "Twenty-Five",
    "XXVI": "Twenty-Six", "XXVII": "Twenty-Seven"
}

ROMAN_TO_WORDS_KO = {
    "I": "일", "II": "이", "III": "삼", "IV": "사", "V": "오",
    "VI": "육", "VII": "칠", "VIII": "팔", "IX": "구", "X": "십",
    "XI": "십일", "XII": "십이", "XIII": "십삼", "XIV": "십사",
    "XV": "십오", "XVI": "십육", "XVII": "십칠", "XVIII": "십팔",
    "XIX": "십구", "XX": "이십", "XXI": "이십일", "XXII": "이십이",
    "XXIII": "이십삼", "XXIV": "이십사", "XXV": "이십오",
    "XXVI": "이십육", "XXVII": "이십칠"
}

def clean_phonetics(text, lang):
    """Replaces abbreviations, symbols, and numerals with phonetic text."""
    if lang == "en":
        for roman, word in ROMAN_TO_WORDS_EN.items():
            text = re.sub(rf"\bChapter {roman}\b", f"Chapter {word}", text, flags=re.IGNORECASE)
            text = re.sub(rf"\bChapter {roman}:", f"Chapter {word}:", text, flags=re.IGNORECASE)
        
        text = re.sub(r"\bMr\.", "Mister", text)
        text = re.sub(r"\bMrs\.", "Missus", text)
        text = re.sub(r"\bDr\.", "Doctor", text)
        text = re.sub(r"\bSt\.", "Saint", text)
        text = re.sub(r"\bProf\.", "Professor", text)
        text = re.sub(r"&", "and", text)
        
    elif lang == "ko":
        for roman, word in ROMAN_TO_WORDS_KO.items():
            text = re.sub(rf"제\s*{roman}\s*장", f"제 {word} 장", text)
            text = re.sub(rf"제{roman}장", f"제 {word} 장", text)
            
        text = re.sub(r"&", "그리고", text)
        
    return text

def classify_voice_role(dialogue_text, surrounding_text, lang):
    """Classifies dialogue into roles: Dracula, Female, VanHelsing, or Male_Others/Jonathan."""
    d_lower = dialogue_text.lower()
    s_lower = surrounding_text.lower()

    if DRACULA_KEYWORDS.search(s_lower) or DRACULA_KEYWORDS.search(d_lower):
        if "count" in s_lower or "dracula" in s_lower or "백작" in s_lower:
            return "Dracula"
            
    if FEMALE_KEYWORDS.search(s_lower) or FEMALE_KEYWORDS.search(d_lower):
        return "Female"

    if VAN_HELSING_KEYWORDS.search(s_lower) or VAN_HELSING_KEYWORDS.search(d_lower):
        return "VanHelsing"

    return "Male_Others"

def parse_chapter_text(filepath, lang):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    script_items = []
    item_id = 1
    narrator_role = "Narrator"

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Strip paragraph ID tag e.g. [P001], [P004a]
        line_clean = re.sub(r"^\[P\d+[a-z]?\]\s*", "", line).strip()
        if not line_clean:
            continue

        line_clean = clean_phonetics(line_clean, lang)

        # Check for chapter title headers
        if re.match(r"^(Chapter\s+\d+|제\s*\d+\s*장)", line_clean, re.IGNORECASE):
            script_items.append({
                "id": item_id,
                "role": narrator_role,
                "text": line_clean,
                "is_header": True
            })
            item_id += 1
            continue

        # Split narration vs quoted dialogue
        # Match both standard " quotes and curly quotes “ ”
        parts = re.split(r'("[^"]+"|[“][^”]+[”])', line_clean)

        for part in parts:
            part = part.strip()
            if not part:
                continue

            # Check that segment contains speakable letters or digits (English, Korean, numbers)
            if not re.search(r"[a-zA-Z0-9\uac00-\ud7a3]", part):
                continue

            # If segment is dialogue wrapped in double/curly quotes
            if (part.startswith('"') and part.endswith('"')) or (part.startswith('“') and part.endswith('”')):
                clean_dialogue = part.strip('"\'“”').strip()
                if not clean_dialogue or not re.search(r"[a-zA-Z0-9\uac00-\ud7a3]", clean_dialogue):
                    continue

                role = classify_voice_role(clean_dialogue, line_clean, lang)
                script_items.append({
                    "id": item_id,
                    "role": role,
                    "text": clean_dialogue,
                    "is_header": False
                })
                item_id += 1
            else:
                clean_narration = part.strip('"\'“”').strip()
                if not clean_narration or not re.search(r"[a-zA-Z0-9\uac00-\ud7a3]", clean_narration):
                    continue

                script_items.append({
                    "id": item_id,
                    "role": narrator_role,
                    "text": clean_narration,
                    "is_header": False
                })
                item_id += 1

    return script_items

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    chapters_dir = os.path.join(script_dir, "chapters")
    scripts_out_dir = os.path.join(script_dir, "scripts")
    os.makedirs(scripts_out_dir, exist_ok=True)

    print("==================================================")
    print("Preparing Dracula JSON Audio Scripts...")
    print("==================================================")

    chapter_files = glob.glob(os.path.join(chapters_dir, "ch*.txt"))
    processed_count = 0

    for filepath in sorted(chapter_files):
        filename = os.path.basename(filepath)

        # Skip raw_ch_ or backup files
        if filename.startswith("raw_") or "chunk" in filename or "scratch" in filename:
            continue

        if filename.endswith("_en.txt"):
            lang = "en"
        elif filename.endswith("_ko.txt"):
            lang = "ko"
        else:
            continue

        ch_match = re.search(r"ch(\d+)", filename)
        if not ch_match:
            continue

        ch_num = ch_match.group(1).zfill(2)
        out_filename = f"ch_{ch_num}_{lang}.json"

        script_items = parse_chapter_text(filepath, lang)

        # Write to both scripts/ directory and chapters/ directory for maximum compatibility
        out_path1 = os.path.join(scripts_out_dir, out_filename)
        out_path2 = os.path.join(chapters_dir, out_filename)

        with open(out_path1, "w", encoding="utf-8") as f:
            json.dump(script_items, f, indent=2, ensure_ascii=False)

        with open(out_path2, "w", encoding="utf-8") as f:
            json.dump(script_items, f, indent=2, ensure_ascii=False)

        print(f"[OK] Processed {filename} -> {out_filename} ({len(script_items)} segments)")
        processed_count += 1

    print(f"\nCompleted! Generated {processed_count} JSON chapter scripts.")

if __name__ == "__main__":
    main()
