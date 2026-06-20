import os
import re
import json
import glob

# Heuristics for dialogue casting
FEMALE_KEYWORDS = re.compile(
    r"\b(she|her|herself|mother|elizabeth|lucie|ishtar|athena|penelope|lady|woman|girl|wife|princess|queen|sister|goddess|mrs|madam|dan)\b", 
    re.IGNORECASE
)
CHILD_KEYWORDS = re.compile(
    r"\b(tim|child|boy|girl|little|kid|young|son|daughter|childhood|baby|pip|monkey|wukong|xiaoyi|yunxia)\b", 
    re.IGNORECASE
)

# Roman numerals to words dictionary
ROMAN_TO_WORDS_EN = {
    "I": "One", "II": "Two", "III": "Three", "IV": "Four", "V": "Five",
    "VI": "Six", "VII": "Seven", "VIII": "Eight", "IX": "Nine", "X": "Ten",
    "XI": "Eleven", "XII": "Twelve", "XIII": "Thirteen", "XIV": "Fourteen",
    "XV": "Fifteen", "XVI": "Sixteen", "XVII": "Seventeen", "XVIII": "Eighteen",
    "XIX": "Nineteen", "XX": "Twenty"
}

ROMAN_TO_WORDS_KO = {
    "I": "일", "II": "이", "III": "삼", "IV": "사", "V": "오",
    "VI": "육", "VII": "칠", "VIII": "팔", "IX": "구", "X": "십",
    "XI": "십일", "XII": "십이", "XIII": "십삼", "XIV": "십사",
    "XV": "십오", "XVI": "십육", "XVII": "십칠", "XVIII": "십팔",
    "XIX": "십구", "XX": "이십"
}

def clean_phonetics(text, lang):
    """Replaces Roman numerals, abbreviations, and symbols with phonetic text."""
    if lang == "en":
        # Replace chapter headers e.g. "Chapter I:" -> "Chapter One:"
        for roman, word in ROMAN_TO_WORDS_EN.items():
            text = re.sub(rf"\bChapter {roman}\b", f"Chapter {word}", text, flags=re.IGNORECASE)
            text = re.sub(rf"\bChapter {roman}:", f"Chapter {word}:", text, flags=re.IGNORECASE)
            # Standalone roman numerals in headers
            text = re.sub(rf"## {roman}\b", f"## {word}", text)
        
        # Common abbreviations
        text = re.sub(r"\bMr\.", "Mister", text)
        text = re.sub(r"\bMrs\.", "Missus", text)
        text = re.sub(r"\bDr\.", "Doctor", text)
        text = re.sub(r"\bSt\.", "Saint", text)
        text = re.sub(r"&", "and", text)
        
    elif lang == "ko":
        # Replace chapter headers e.g. "제I장" or "제 I 장"
        for roman, word in ROMAN_TO_WORDS_KO.items():
            text = re.sub(rf"제\s*{roman}\s*장", f"제 {word} 장", text)
            text = re.sub(rf"## {roman}\b", f"## 제 {word} 장", text)
            
        text = re.sub(r"&", "그리고", text)
        
    return text

def classify_voice_role(dialogue_text, surrounding_text, lang, book_name, chapter_num=1):
    """Uses keywords to classify who is speaking: Child, Female, Father, or Male (default)."""
    dialogue = dialogue_text.lower()
    surrounding = surrounding_text.lower()

    if book_name == "hong_gildong":
        # Custom logic for Gildong
        if "minister" in surrounding or "hong" in surrounding or "판서" in surrounding or "꾸짖었다" in surrounding or "엄하게" in surrounding:
            if "knelt" in surrounding or "무릎을" in surrounding or "corrected" in surrounding:
                return "Male" # Gildong
            return "Father"
        if "gildong" in surrounding or "길동" in surrounding or "whispered" in surrounding or "대감" in dialogue or "lord" in dialogue:
            return "Male"
        if "minister" in surrounding or "hong" in surrounding or "대감" in surrounding or "판서" in surrounding:
            return "Father"
        return "Male"

    elif book_name == "frankenstein":
        # Custom logic for Frankenstein
        if chapter_num == 0:
            return "Victor"
        elif chapter_num in [3, 4]:
            return "Creature"
        return "Victor"

    elif book_name == "gilgamesh":
        # 1. Dialogue-based exact/high-precision matching (checks dialogue text first)
        d_lower = dialogue.lower()
        
        # Gilgamesh dialogue
        if any(k in d_lower for k in [
            "go to the temple of ishtar", "이슈타르 신전으로 가서",
            "step aside", "길을 비켜라",
            "rise, my brother", "일어나라, 내 형제여",
            "my brother, in the mountains", "나의 형제여, 서쪽 산맥",
            "do not speak of danger", "위험을 말하지 말게",
            "o mountain, bring me a dream", "오 산이시여, 저에게 꿈을",
            "stand strong, my brother", "굳세게 서라, 내 형제여",
            "should we let him go", "그를 살려주어야 할까",
            "why should i marry you", "내가 왜 당신과 결혼해야",
            "my friend, who ran with", "가젤들과 함께 달리고",
            "will i die like enkidu", "나도 엔키두처럼 죽을 운명",
            "i search for utnapishtim", "우트나피쉬팀을 찾고",
            "though there be darkness", "어둠과 슬픔이 있을지라도",
            "tavern keeper, why do you", "여관 주인이여, 왜 문을",
            "why should my cheeks", "내가 어찌 슬프지 않겠소",
            "my brother is dead, and i cannot rest", "내 형제가 죽었는데 내가 어찌",
            "but how did you obtain eternal life", "하지만 어떻게 영생을 얻었습니까",
            "i only slept for a moment", "잠시 졸았을 뿐이오",
            "what shall i do, utnapishtim", "내가 어찌해야 합니까, 우트나피쉬팀",
            "urshanabi! this is the plant of youth", "우르샤나비! 이것이 젊음의",
            "for whom have my hands suffered", "내가 누구를 위해 손에 피를",
            "climb upon the walls of uruk", "우루크의 성벽에 올라가 보아라"
        ]):
            return "Gilgamesh"
            
        # Enkidu dialogue
        if any(k in d_lower for k in [
            "the animals have fled. i am alone", "동물들이 달아나 버렸소. 나 혼자 남았소",
            "this is not right", "이것은 옳지 않소",
            "i will not move", "비키지 않겠소",
            "i know that forest", "나는 그 숲을 알고 있네",
            "do not fear, my friend", "두려워하지 말게, 내 친구여",
            "my friend, he is too powerful", "내 친구여, 그는 너무 강하네",
            "do not listen to his words", "그의 말을 듣지 마십시오",
            "strike now, gilgamesh", "지금 베어라, 길가메시",
            "if i could catch you", "내가 너를 잡을 수만 있다면",
            "my brother, i saw the house of darkness", "내 형제여, 한 번 가면 돌아올 수 없는"
        ]):
            return "Enkidu"
            
        # Shamhat dialogue
        if any(k in d_lower for k in [
            "you are not alone, enkidu", "당신은 혼자가 아니에요, 엔키두",
            "look at yourself. you are wise", "자신을 보세요. 당신은 지혜롭고"
        ]):
            return "Shamhat"
            
        # Ishtar dialogue
        if any(k in d_lower for k in [
            "marry me, gilgamesh", "나와 결혼해 주오",
            "father! gilgamesh has insulted me", "아버지! 길가메시가 나를 모욕"
        ]):
            return "Ishtar"
            
        # Utnapishtim dialogue
        if any(k in d_lower for k in [
            "nothing lasts forever", "영원한 것은 아무것도 없네",
            "reveal to you a secret", "비밀을 들려주겠네",
            "i built the ark as ea commanded", "나는 에아가 명령한 대로 방주를 지었네",
            "when the gods saw the destruction", "신들이 그 파괴를 보았을 때",
            "if you think you can conquer death", "그대가 죽음을 극복할 수 있다고 믿는다면",
            "i will tell you a secret, gilgamesh", "자네에게 비밀을 하나 알려주겠네, 길가메시여"
        ]):
            return "Utnapishtim"
            
        # Utnapishtim's Wife dialogue
        if any(k in d_lower for k in [
            "bake a loaf of bread", "그가 자는 동안 하루에 한 덩이",
            "he has traveled so far", "그가 이토록 먼 길을 여행하며"
        ]):
            return "Utnapishtim_Wife"
            
        # Huwawa dialogue
        if any(k in d_lower for k in [
            "who has entered my forest", "누가 내 숲에 들어왔느냐",
            "gilgamesh, spare my life", "길가메시여, 내 목숨을 살려주시오"
        ]):
            return "Huwawa"
            
        # ScorpionMan dialogue
        if any(k in d_lower for k in [
            "he who comes is of royal blood", "다가오는 자의 핏줄이 심상치",
            "why have you traveled so far", "왜 이 금지된 땅까지",
            "no mortal has ever walked", "어떤 인간도 이 길을 걸어간",
            "go in safety, gilgamesh", "안전하게 가십시오, 길가메시"
        ]):
            return "ScorpionMan"
            
        # Siduri dialogue
        if any(k in d_lower for k in [
            "if you are indeed gilgamesh, why are", "그대가 정말 길가메시라면, 왜 뺨이",
            "why do you chase the wind", "왜 바람을 쫓아 헤매십니까",
            "only the sun god shamash", "오직 태양신 샤마시만이"
        ]):
            return "Siduri"
            
        # Urshanabi dialogue
        if any(k in d_lower for k in [
            "the waters of death are deadly to touch", "죽음의 물은 손만 닿아도 치명적"
        ]):
            return "Urshanabi"
            
        # Hunter dialogue
        if any(k in d_lower for k in [
            "father, there is a giant wild man", "아버지, 산속에 거대한 야생인"
        ]):
            return "Hunter"
            
        # Father dialogue
        if any(k in d_lower for k in [
            "my son, go to uruk", "내 아들아, 우루크로 가서"
        ]):
            return "Father"

        # Narrator dialogue (for prayers or general quotes meant for narrator)
        if any(k in d_lower for k in [
            "o gods, you created", "오 신들이시여, 당신께서",
            "aruru, you created gilgamesh", "아루루여, 그대가 길가메시",
            "they have slain the guardian", "그들이 백향목 숲의 파수꾼"
        ]):
            return "Narrator"

        # 2. Narration/Surrounding text backups if dialogue matching wasn't hit
        # (Useful as a general fallback for any missed dialogue)
        if chapter_num == 1:
            if "they prayed" in surrounding or "기도했습니다" in surrounding or "기도했다" in surrounding:
                return "Narrator"
            if "the gods said" in surrounding or "신들은" in surrounding:
                return "Narrator"
            if "told his father" in surrounding or "아버지에게 말" in surrounding:
                return "Hunter"
            if "father replied" in surrounding or "아버지가 대답" in surrounding:
                return "Father"
            if "king smiled and said" in surrounding or "미소를 지으며 말" in surrounding:
                return "Gilgamesh"
            if "looked at her and said" in surrounding or "바라보며" in surrounding:
                return "Enkidu"
            if "she said" in surrounding or "shamhat smiled" in surrounding or "샴하트는" in surrounding or "그녀는" in surrounding:
                return "Shamhat"
        elif chapter_num == 2:
            if "whispering in astonishment" in surrounding or "속삭였습니다" in surrounding:
                return "Narrator"
            if "enkidu" in surrounding or "엔키두" in surrounding:
                return "Enkidu"
            if "gilgamesh" in surrounding or "길가메시" in surrounding or "he said" in surrounding or "말했습니다" in surrounding:
                return "Gilgamesh"
        elif chapter_num == 3:
            if "huwawa" in surrounding or "후와와" in surrounding:
                return "Huwawa"
            if any(k in surrounding for k in ["enkidu said", "enkidu whispered", "enkidu warned", "enkidu warning", "엔키두"]):
                return "Enkidu"
            if "praying" in surrounding or "gilgamesh" in surrounding or "길가메시" in surrounding or "기도" in surrounding:
                return "Gilgamesh"
        elif chapter_num == 4:
            if "ishtar" in surrounding or "she screamed" in surrounding or "이슈타르" in surrounding or "비명" in surrounding:
                return "Ishtar"
            if "enlil" in surrounding or "엔릴" in surrounding:
                return "Narrator"
            if "enkidu" in surrounding or "엔키두" in surrounding:
                return "Enkidu"
            if "gilgamesh" in surrounding or "길가메시" in surrounding or "he cried" in surrounding:
                return "Gilgamesh"
        elif chapter_num == 5:
            if "scorpion-man" in surrounding or "scorpion-men" in surrounding or "전갈" in surrounding:
                return "ScorpionMan"
            if "siduri" in surrounding or "시두리" in surrounding:
                return "Siduri"
            if "ferryman" in surrounding or "urshanabi" in surrounding or "사공" in surrounding or "우르샤나비" in surrounding:
                return "Urshanabi"
            if "gilgamesh" in surrounding or "길가메시" in surrounding:
                return "Gilgamesh"
        elif chapter_num == 6:
            if "wife" in surrounding or "아내" in surrounding:
                return "Utnapishtim_Wife"
            if "utnapishtim" in surrounding or "우트나피쉬팀" in surrounding:
                return "Utnapishtim"
            else:
                return "Gilgamesh"

        return "Gilgamesh"

    elif book_name == "christmas_carol":
        d_lower = dialogue.lower()
        s_lower = surrounding.lower()

        # 1. Fred (Nephew)
        if any(k in s_lower for k in ["nephew", "fred", "조카"]):
            return "Fred"
        if any(k in d_lower for k in [
            "merry christmas, uncle", "즐거운 성탄절 보내세요, 삼촌",
            "don't be angry", "화내지 마세요",
            "dine with us", "저희와 함께 저녁 식사",
            "why cannot we be friends", "왜 우리는 친구가 될 수 없나요",
            "god bless it", "신의 가호가 있기를"
        ]):
            return "Fred"

        # 2. Bob Cratchit (Clerk)
        if any(k in s_lower for k in ["clerk", "cratchit", "서기", "밥 크래칫"]):
            return "BobCratchit"
        if any(k in d_lower for k in ["only once a year", "일 년에 한 번뿐", "merry christmas, sir", "즐거운 성탄절 되세요, 사장님"]):
            return "BobCratchit"

        # 3. Portly Gentlemen (Charity collectors)
        if any(k in s_lower for k in ["gentleman", "gentlemen", "신사"]):
            return "Gentleman"
        if any(k in d_lower for k in [
            "scrooge and marley", "스크루지와 마리",
            "poor and needy", "가난하고 어려운 이들",
            "many thousands lack", "수만 명의 사람들이",
            "we choose this time", "저희가 이 시기를 택한 것은",
            "few pounds", "몇 파운드"
        ]):
            return "Gentleman"

        # 4. Marley's Ghost
        if any(k in s_lower for k in ["marley", "ghost", "유령", "말리"]):
            # Make sure it's not the other ghosts
            if not any(kg in s_lower for kg in ["past", "present", "yet to come", "과거", "현재", "미래"]):
                return "Marley"
        if any(k in d_lower for k in [
            "toothpick", "이쑤시개",
            "i wear the chain", "내가 만든 사슬",
            "captive in chains", "사슬에 묶인 죄인",
            "business! mankind was my business", "사업! 인간성이 내 사업",
            "three spirits", "세 명의 유령",
            "my time is almost up", "내 시간이 거의 끝났다",
            "without their visits", "그들의 방문 없이는",
            "expect the first tomorrow", "내일 첫 번째 유령이",
            "expect the second", "두 번째 유령은",
            "remember what has passed", "우리 사이에 있었던 일을 기억하게"
        ]):
            return "Marley"

        # 5. Ghost of Christmas Past
        if any(k in s_lower for k in ["past ghost", "ghost of christmas past", "과거의 유령"]):
            return "PastGhost"
        if any(k in d_lower for k in ["rise! and walk with me", "일어나서 나와 함께 걸읍시다"]):
            return "PastGhost"

        # 6. Ghost of Christmas Present
        if any(k in s_lower for k in ["present ghost", "ghost of christmas present", "현재의 유령"]):
            return "PresentGhost"
        if any(k in d_lower for k in ["touch my robe", "내 옷자락을 잡으시오"]):
            return "PresentGhost"

        # 7. Fezziwig
        if any(k in s_lower for k in ["fezziwig", "페지위그"]):
            return "Fezziwig"
        if any(k in d_lower for k in ["no more work tonight", "오늘 밤은 일 끝이다", "clear the room", "방을 치우자"]):
            return "Fezziwig"

        # 8. Belle
        if any(k in s_lower for k in ["belle", "벨", "former love"]):
            return "Belle"
        if any(k in d_lower for k in ["another idol has displaced me", "다른 우상이 나를 대체해", "our contract was an old one", "우리의 약속은 아주 오래전에"]):
            return "Belle"

        # 9. Mrs. Cratchit
        if any(k in s_lower for k in ["mrs. cratchit", "크래칫 부인"]):
            return "MrsCratchit"

        # 10. Tiny Tim
        if any(k in s_lower for k in ["tiny tim", "타이니 팀", "tim"]):
            return "TinyTim"
        if any(k in d_lower for k in ["god bless us every one", "모든 이에게 신의 축복이"]):
            return "TinyTim"

        # 11. Old Joe
        if any(k in s_lower for k in ["old joe", "늙은 조", "pawnbroker"]):
            return "OldJoe"

        # 12. Mrs. Dilber / Charwoman
        if any(k in s_lower for k in ["dilber", "딜버", "charwoman", "laundress", "빨래방 여인"]):
            return "MrsDilber"

        # 13. Boy
        if any(k in s_lower for k in ["boy", "소년"]):
            return "Boy"
        if any(k in d_lower for k in ["intelligent boy", "똑똑한 소년", "who, me", "저요", "turkey", "칠면조"]):
            return "Boy"

        # Default male character dialog is Scrooge
        return "Scrooge"

    # Default logic for other books:
    # Check child keywords first
    if CHILD_KEYWORDS.search(dialogue_text) or CHILD_KEYWORDS.search(surrounding_text):
        return "Child"
    # Check female keywords
    if FEMALE_KEYWORDS.search(dialogue_text) or FEMALE_KEYWORDS.search(surrounding_text):
        return "Female"
    # Default to Male
    return "Male"

def parse_chapter_text(filepath, lang, book_name):
    """Parses raw chapter text into structured JSON script entries."""
    # Extract chapter index
    chapter_num = 1
    match = re.search(r"ch_(\d+)", os.path.basename(filepath))
    if match:
        chapter_num = int(match.group(1))

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Phonetic cleanups
    content = clean_phonetics(content, lang)
    
    # Split content into paragraphs
    paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
    
    script_items = []
    item_id = 1
    
    for para in paragraphs:
        # Determine narrator role
        narrator_role = "Narrator"
        if book_name == "frankenstein":
            narrator_role = "Walton" if chapter_num == 0 else "Victor"

        # Check if paragraph is a header (e.g. starting with # or ##)
        if para.startswith("#"):
            header_text = para.replace("#", "").strip()
            script_items.append({
                "id": item_id,
                "role": narrator_role,
                "text": header_text,
                "is_header": True
            })
            item_id += 1
            continue
            
        # Parse quotes in paragraph
        parts = re.split(r'(".*?")', para)
        
        # Determine paragraph role first (since one paragraph has only one speaker)
        dialogue_parts = [p.strip('"').strip() for p in parts if p.startswith('"') and p.endswith('"') and p.strip('"').strip()]
        narration_parts = [p.strip() for p in parts if not (p.startswith('"') and p.endswith('"')) and p.strip()]
        
        para_dialogue = " ".join(dialogue_parts)
        para_narration = " ".join(narration_parts)
        
        # Classify the role for the entire paragraph
        para_role = narrator_role
        if dialogue_parts:
            # It contains dialogue, determine speaker
            para_role = classify_voice_role(para_dialogue, para_narration, lang, book_name, chapter_num)
            
        for part_idx, part in enumerate(parts):
            if not part:
                continue
                
            if part.startswith('"') and part.endswith('"'):
                clean_dialogue = part.strip('"').strip()
                if not clean_dialogue:
                    continue
                
                script_items.append({
                    "id": item_id,
                    "role": para_role,
                    "text": clean_dialogue,
                    "is_header": False
                })
                item_id += 1
            else:
                clean_narration = part.strip()
                if not clean_narration:
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
    base_dir = r"d:\git_repo\thefirstaicompany\books"
    print("Starting chapter script preparation...")
    
    # Find all chapter files across the 10 books
    chapter_files = glob.glob(os.path.join(base_dir, "*", "chapters", "ch_*.txt"))
    
    processed_count = 0
    for filepath in chapter_files:
        filename = os.path.basename(filepath)
        book_dir = os.path.dirname(os.path.dirname(filepath))
        
        # Determine language from filename
        if filename.endswith("_en.txt"):
            lang = "en"
        elif filename.endswith("_ko.txt"):
            lang = "ko"
        else:
            continue
            
        output_filename = filename.replace(".txt", ".json")
        output_path = os.path.join(os.path.dirname(filepath), output_filename)
        
        book_name = os.path.basename(book_dir)
        print(f"Processing {book_name} / {filename}...")
        script_items = parse_chapter_text(filepath, lang, book_name)
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(script_items, f, indent=2, ensure_ascii=False)
            
        processed_count += 1
        
    print(f"\nDone! Successfully prepared {processed_count} JSON chapter scripts.")

if __name__ == "__main__":
    main()
