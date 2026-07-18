import re
import json
import os

def guess_speaker(context, quote_text):
    # Heuristic speaker detection based on preceding context
    context_lower = context.lower()
    
    # If the quote itself contains clues
    # Odysseus (오디세우스)
    # Telemachus (텔레마코스)
    # Others (페넬로페, 에우리클레이아, 유모, 에우마이오스 등)
    
    # Check context (last 100 chars of preceding text)
    last_context = context_lower[-120:] if len(context_lower) > 120 else context_lower
    
    if "텔레마코스가" in last_context or "텔레마코스도" in last_context or "텔레마코스는" in last_context or "아들이 말했다" in last_context:
        return "telemachus"
    elif "오디세우스가" in last_context or "오디세우스는" in last_context or "그가 말했다" in last_context or "그가 대답했다" in last_context or "이방인이" in last_context or "손님이 대답했다" in last_context or "손님이 말했다" in last_context or "오디세우스도" in last_context:
        return "odysseus"
    elif "페넬로페" in last_context or "유모" in last_context or "에우리클레이아" in last_context or "멜란토" in last_context or "에우리노메" in last_context:
        return "others"
    
    # Fallback default
    return "others"

def process_chapters():
    data = {}
    for ch in range(19, 25):
        file_path = f"books/odyssey/chapters/ch_{ch}_ko.txt"
        if not os.path.exists(file_path):
            continue
            
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Split using quote pattern
        pattern = r'("[^"]*"|“[^”]*”)'
        parts = re.split(pattern, content)
        
        quotes = []
        for i in range(1, len(parts), 2):
            quote = parts[i]
            # Context is the preceding part
            context = parts[i-1]
            guessed = guess_speaker(context, quote)
            quotes.append({
                "index": i // 2,
                "quote": quote,
                "guessed": guessed,
                "context_preview": context[-80:].strip() if len(context) > 80 else context.strip()
            })
            
        data[f"ch_{ch}"] = quotes
        
    with open("scratch/guessed_quotes.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Guessed quotes written to scratch/guessed_quotes.json")

if __name__ == "__main__":
    process_chapters()
