import json
import os
import glob
import re

translated_blocks = []
# Just parse the parent agent's transcript because SYSTEM_MESSAGE is in the parent's log!
transcripts = glob.glob("C:/Users/hongw/.gemini/antigravity/brain/*/.system_generated/logs/transcript.jsonl")
for t in transcripts:
    with open(t, "r", encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line)
                if entry.get("role") == "user" and "content" in entry:
                    content = entry["content"]
                    if isinstance(content, list) and len(content) > 0:
                        text = content[0].get("text", "")
                        if "ko" in text and "en" in text:
                            # Try to find JSON object in the text
                            matches = re.findall(r'\{[^{}]*"en"[^{}]*"ko"[^{}]*\}', text)
                            if matches:
                                # We might have individual tag dicts or a whole dictionary.
                                # Let's just find anything that looks like JSON and parse it
                                start = text.find("{")
                                end = text.rfind("}")
                                if start != -1 and end != -1:
                                    json_str = text[start:end+1]
                                    parsed = json.loads(json_str)
                                    if isinstance(parsed, dict):
                                        translated_blocks.append(parsed)
                                    elif isinstance(parsed, list):
                                        translated_blocks.extend(parsed)
            except Exception:
                pass

print("Found translated block groups:", len(translated_blocks))

if len(translated_blocks) > 0:
    with open("books/two_cities/json/book2_ch_01.json", "r", encoding="utf-8") as f:
        book_data = json.load(f)

    flat_translations = {}
    for block in translated_blocks:
        if isinstance(block, dict):
            # Check if it is { tag: {en, ko} } or {tag, en, ko}
            if "tag" in block and "en" in block and "ko" in block:
                flat_translations[block["tag"]] = block
            else:
                for k, v in block.items():
                    if isinstance(v, dict) and "en" in v and "ko" in v:
                        flat_translations[k] = v

    update_count = 0
    for item in book_data:
        tag = item.get("tag")
        if tag in flat_translations:
            if not item.get("en") or not item.get("ko"):
                item["en"] = flat_translations[tag].get("en", "")
                item["ko"] = flat_translations[tag].get("ko", "")
                update_count += 1

    with open("books/two_cities/json/book2_ch_01.json", "w", encoding="utf-8") as f:
        json.dump(book_data, f, indent=2, ensure_ascii=False)

    print(f"Updated {update_count} blocks in book2_ch_01.json")
