import os
import re
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TAGGED_EN_DIR = os.path.join(BASE_DIR, "chapters", "tagged")
RAW_KO_DIR = os.path.join(BASE_DIR, "chapters")
SCRIPTS_EN_DIR = os.path.join(BASE_DIR, "scripts_en")
SCRIPTS_KO_DIR = os.path.join(BASE_DIR, "scripts_ko")

os.makedirs(SCRIPTS_EN_DIR, exist_ok=True)
os.makedirs(SCRIPTS_KO_DIR, exist_ok=True)

# English and Korean Voice Maps (All speeds reset to 1.0)
VOICE_MAP_EN = {
    "Narrator": ("af_heart", 1.0),
    "Lotty": ("af_bella", 1.0),
    "Rose": ("bf_isabella", 1.0),
    "Fisher": ("bf_alice", 1.0),
    "Scrap": ("bf_lily", 1.0),
    "Mellersh": ("bf_alice", 1.0),
    "Briggs": ("bf_isabella", 1.0),
    "Frederick": ("af_bella", 1.0),
    "Domenico": ("bf_alice", 1.0),
    "Francesca": ("af_bella", 1.0),
    "Ferdinand": ("bf_alice", 1.0),
    "Other": ("bf_alice", 1.0),
}

VOICE_MAP_KO = {
    "Narrator": ("ko-KR-InJoonNeural", 1.0),
    "Lotty": ("ko-KR-SunHiNeural", 1.0),
    "Rose": ("ko-KR-SunHiNeural", 1.0),
    "Fisher": ("ko-KR-SunHiNeural", 1.0),
    "Scrap": ("ko-KR-SunHiNeural", 1.0),
    "Mellersh": ("ko-KR-SunHiNeural", 1.0),
    "Briggs": ("ko-KR-SunHiNeural", 1.0),
    "Frederick": ("ko-KR-SunHiNeural", 1.0),
    "Domenico": ("ko-KR-SunHiNeural", 1.0),
    "Francesca": ("ko-KR-SunHiNeural", 1.0),
    "Ferdinand": ("ko-KR-SunHiNeural", 1.0),
    "Other": ("ko-KR-SunHiNeural", 1.0),
}

# Thought indicators and speech verbs for English cleanup
THOUGHT_RE = re.compile(r'\b(thought|wondered|wished|reflected|felt|recollected|silently)\b', re.IGNORECASE)
COMMON_SPOKEN = {"yes", "no", "oh", "why", "true", "well", "please", "indeed", "portraits?"}

def clean_english_paragraph(p_text):
    """
    Remove XML tags for pseudo-dialogues (short quotes) or inner thoughts.
    """
    # Find all XML tags: <Tag>text</Tag>
    pattern = re.compile(r'<(?P<tag>Lotty|Rose|Other|Fisher|Scrap|Mellersh|Briggs|Frederick|Domenico|Francesca|Ferdinand)>(?P<speech>.*?)</(?P=tag)>', re.DOTALL)
    
    def replacer(match):
        tag = match.group('tag')
        speech = match.group('speech').strip()
        
        # Strip quotes from speech to check content
        clean_speech = speech.strip('"').strip('“').strip('”').strip("'").strip('‘').strip('’')
        words = clean_speech.split()
        
        # Rule 1: Clean short pseudo-dialogues (<= 3 words) unless they are common spoken words
        lower_speech = clean_speech.lower()
        if "sì" in lower_speech or "si" in lower_speech or "ecco" in lower_speech:
            pass # Keep Italian spoken words
        elif len(words) <= 3 and lower_speech not in COMMON_SPOKEN:
            return speech
            
        # Rule 2: Clean thoughts (check surrounding context in the paragraph for thought verbs)
        start_idx = match.start()
        end_idx = match.end()
        
        # Check 45 characters before and after the XML block
        context_before = p_text[max(0, start_idx - 45):start_idx]
        context_after = p_text[end_idx:min(len(p_text), end_idx + 45)]
        
        if THOUGHT_RE.search(context_before) or THOUGHT_RE.search(context_after):
            return speech
            
        return match.group(0) # Keep tags
        
    return pattern.sub(replacer, p_text)

def parse_xml_paragraph(p_text):
    """
    Parse a paragraph into text segments with speakers.
    """
    pattern = re.compile(r'<(?P<tag>Lotty|Rose|Other|Fisher|Scrap|Mellersh|Briggs|Frederick|Domenico|Francesca|Ferdinand)>(?P<speech>.*?)</(?P=tag)>|(?P<narration>(?:(?!<(?:Lotty|Rose|Other|Fisher|Scrap|Mellersh|Briggs|Frederick|Domenico|Francesca|Ferdinand)>).)+)', re.DOTALL)
    segments = []
    
    for match in pattern.finditer(p_text):
        tag = match.group('tag')
        speech = match.group('speech')
        narration = match.group('narration')
        
        if tag and speech:
            text = speech.strip()
            if text:
                segments.append({"character": tag, "text": text})
        elif narration:
            text = narration.strip()
            if text:
                segments.append({"character": "Narrator", "text": text})
                
    return segments

def extract_quotes(ko_text):
    """
    Extract quoted dialogue parts and non-dialogue parts from Korean text.
    """
    # Find quotes in Korean paragraph
    pattern = re.compile(r'(“[^”]+”|"[^"]+")|([^“”"]+)', re.DOTALL)
    parts = []
    for match in pattern.finditer(ko_text):
        quote = match.group(1)
        non_quote = match.group(2)
        if quote:
            parts.append({"is_quote": True, "text": quote.strip()})
        elif non_quote:
            text = non_quote.strip()
            if text:
                parts.append({"is_quote": False, "text": text})
    return parts

# Contextual classifier for all characters
FISHER_RE = re.compile(r'Mrs\.? Fisher')
SCRAP_RE = re.compile(r'\bScrap\b|Lady Caroline')
MELLERSH_RE = re.compile(r'\bMr\.? Wilkins\b|\bWilkins\b|\bMellersh\b')
BRIGGS_RE = re.compile(r'\bMr\.? Briggs\b|\bBriggs\b|\bThomas\b')
FREDERICK_RE = re.compile(r'\bMr\.? Arbuthnot\b|\bFrederick\b')
DOMENICO_RE = re.compile(r'\bDomenico\b')
FERDINAND_RE = re.compile(r'\bFerdinand\b|\bArundel\b')

def nearest_speaker(prev_text, next_text):
    tail = prev_text[-250:] if prev_text else ""
    head = next_text[:250] if next_text else ""

    def last_match(text, pattern):
        matches = list(pattern.finditer(text))
        return matches[-1].start() if matches else -1

    def first_match(text, pattern):
        m = pattern.search(text)
        return m.start() if m else -1

    candidates = []
    patterns = [
        ("Fisher", FISHER_RE), 
        ("Scrap", SCRAP_RE),
        ("Mellersh", MELLERSH_RE),
        ("Briggs", BRIGGS_RE),
        ("Frederick", FREDERICK_RE),
        ("Domenico", DOMENICO_RE),
        ("Ferdinand", FERDINAND_RE)
    ]
    for label, pat in patterns:
        p = last_match(tail, pat)
        if p != -1:
            candidates.append((len(tail) - p, label))
        p = first_match(head, pat)
        if p != -1:
            candidates.append((p, label))

    if not candidates:
        return None
    candidates.sort(key=lambda x: x[0])
    return candidates[0][1]

def build_chapter(ch_num):
    en_file = os.path.join(TAGGED_EN_DIR, f"tagged_ch_{ch_num:02d}_en.txt")
    ko_file = os.path.join(RAW_KO_DIR, f"ch_{ch_num:02d}_ko.txt")
    
    if not os.path.exists(en_file) or not os.path.exists(ko_file):
        print(f"Skipping Chapter {ch_num:02d}, files not found.")
        return
        
    en_paras = [p.strip() for p in open(en_file, encoding='utf-8').read().split('\n') if p.strip()]
    ko_paras = [p.strip() for p in open(ko_file, encoding='utf-8').read().split('\n') if p.strip()]
    
    if len(en_paras) != len(ko_paras):
        print(f"ERROR: Chapter {ch_num:02d} paragraph count mismatch! EN={len(en_paras)}, KO={len(ko_paras)}")
        return

    en_paras_segs = []
    en_final_segments = []

    # 1. First Pass: Parse and clean English paragraphs
    for i in range(len(en_paras)):
        en_raw = en_paras[i]
        en_clean = clean_english_paragraph(en_raw)
        en_segs = parse_xml_paragraph(en_clean)
        en_paras_segs.append(en_segs)
        for seg in en_segs:
            en_final_segments.append(seg)

    # 2. Classify Other characters (Fisher, Scrap, Mellersh, Briggs, etc.) in English contextually
    for i, seg in enumerate(en_final_segments):
        if seg["character"] == "Other":
            prev_text = en_final_segments[i-1]["text"] if i > 0 else ""
            next_text = en_final_segments[i+1]["text"] if i < len(en_final_segments)-1 else ""
            label = nearest_speaker(prev_text, next_text)
            if label:
                seg["character"] = label
            else:
                # Chapter-based fallback for unclassified "Other" dialogue (safely maps to the dominant male in the chapter)
                if ch_num <= 2:
                    seg["character"] = "Mellersh"
                elif ch_num == 3:
                    seg["character"] = "Briggs"
                elif ch_num in [4, 5, 6, 7]:
                    seg["character"] = "Mellersh"
                elif ch_num in [8, 9, 10]:
                    seg["character"] = "Briggs"
                elif ch_num in [11, 12, 13, 14]:
                    seg["character"] = "Mellersh"
                elif ch_num in [15, 16, 17, 18]:
                    seg["character"] = "Mellersh"
                elif ch_num in [19, 20]:
                    seg["character"] = "Briggs"
                else:
                    seg["character"] = "Frederick"

    # 3. Second Pass: Extract quotes from Korean paragraphs and map classified speakers
    ko_final_segments = []
    for i in range(len(ko_paras)):
        ko_raw = ko_paras[i]
        ko_parts = extract_quotes(ko_raw)
        en_segs = en_paras_segs[i]
        
        # Collect already-classified speakers from the English segments of this paragraph
        en_speakers = [s["character"] for s in en_segs if s["character"] != "Narrator"]
        
        ko_segs = []
        speaker_idx = 0
        
        for part in ko_parts:
            if part["is_quote"] and en_speakers:
                if speaker_idx < len(en_speakers):
                    char = en_speakers[speaker_idx]
                    speaker_idx += 1
                else:
                    char = en_speakers[-1]
                ko_segs.append({"character": char, "text": part["text"]})
            else:
                ko_segs.append({"character": "Narrator", "text": part["text"]})
                
        for seg in ko_segs:
            ko_final_segments.append(seg)

    # 4. Korean Pass: Align speakers 1-to-1 from English to Korean
    ko_idx = 0
    for en_seg in en_final_segments:
        is_dialogue = (en_seg["character"] != "Narrator")
        while ko_idx < len(ko_final_segments):
            ko_seg = ko_final_segments[ko_idx]
            ko_is_dialogue = (ko_seg["character"] != "Narrator")
            if is_dialogue == ko_is_dialogue:
                ko_seg["character"] = en_seg["character"]
                ko_idx += 1
                break
            else:
                ko_idx += 1

    # 6. Apply voice mappings and format final JSON structure
    en_json = []
    for idx, seg in enumerate(en_final_segments):
        char = seg["character"]
        voice, speed = VOICE_MAP_EN.get(char, VOICE_MAP_EN["Other"])
        en_json.append({
            "index": idx,
            "character": char,
            "sex": "female",
            "voice": voice,
            "speed": speed,
            "text": seg["text"]
        })
        
    ko_json = []
    for idx, seg in enumerate(ko_final_segments):
        char = seg["character"]
        voice, speed = VOICE_MAP_KO.get(char, VOICE_MAP_KO["Other"])
        ko_json.append({
            "index": idx,
            "character": char,
            "sex": "male" if char == "Narrator" else "female",
            "voice": voice,
            "speed": speed,
            "text": seg["text"]
        })

    # Save files
    out_en_p = os.path.join(SCRIPTS_EN_DIR, f"script_ch_{ch_num:02d}.json")
    out_ko_p = os.path.join(SCRIPTS_KO_DIR, f"script_ch_{ch_num:02d}.json")
    
    with open(out_en_p, "w", encoding="utf-8") as f:
        json.dump(en_json, f, ensure_ascii=False, indent=2)
    with open(out_ko_p, "w", encoding="utf-8") as f:
        json.dump(ko_json, f, ensure_ascii=False, indent=2)
        
    print(f"Chapter {ch_num:02d} processed: EN={len(en_json)} segs, KO={len(ko_json)} segs.")

if __name__ == "__main__":
    for c in range(1, 23):
        build_chapter(c)
