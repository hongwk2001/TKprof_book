import json
import glob
import re

FISHER_RE = re.compile(r'Mrs\.? Fisher')
SCRAP_RE = re.compile(r'\bScrap\b|Lady Caroline')
MALE_RE = re.compile(
    r'\bMr\.? Wilkins\b|\bWilkins\b|\bBriggs\b|\bDomenico\b|\bFrederick\b|\bFerdinand\b|'
    r'\bMellersh\b|\bthe priest\b|\bthe padrone\b|\bhe said\b|\bhe asked\b|\bhe replied\b'
)

def nearest_speaker(prev_text, next_text):
    """Look at the tail of prev_text and head of next_text (the narration
    directly touching the quote) and find whichever name is closest to the
    quote boundary on each side."""
    tail = prev_text[-250:] if prev_text else ""
    head = next_text[:250] if next_text else ""

    def last_match(text, pattern):
        matches = list(pattern.finditer(text))
        return matches[-1].start() if matches else -1

    def first_match(text, pattern):
        m = pattern.search(text)
        return m.start() if m else -1

    # distance from quote boundary: for tail, distance = len(tail) - pos (smaller = closer)
    # for head, distance = pos (smaller = closer)
    candidates = []  # (distance, label)

    for label, pat in [("fisher", FISHER_RE), ("scrap", SCRAP_RE), ("male", MALE_RE)]:
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

def main():
    files = sorted(glob.glob('scripts_en/script_ch_*.json'))
    counts = {"fisher": 0, "scrap": 0, "male": 0, "none": 0}
    changed_files = 0

    for f in files:
        data = json.load(open(f, encoding='utf-8'))
        file_changed = False
        for i, seg in enumerate(data):
            if seg.get("character") != "Other":
                continue
            prev_text = data[i-1]["text"] if i > 0 else ""
            next_text = data[i+1]["text"] if i < len(data)-1 else ""

            label = nearest_speaker(prev_text, next_text)

            if label == "fisher":
                seg["character"] = "Fisher"
                seg["voice"] = "bf_alice"
                seg["speed"] = 1.0
                file_changed = True
                counts["fisher"] += 1
            elif label == "scrap":
                seg["character"] = "Scrap"
                seg["voice"] = "bf_isabella"
                seg["speed"] = 1.0
                file_changed = True
                counts["scrap"] += 1
            elif label == "male":
                counts["male"] += 1
            else:
                counts["none"] += 1

        if file_changed:
            changed_files += 1
            with open(f, 'w', encoding='utf-8') as out:
                json.dump(data, out, ensure_ascii=False, indent=2)

    print(f"Files changed: {changed_files}")
    print(f"Reclassified -> Fisher: {counts['fisher']}")
    print(f"Reclassified -> Scrap:  {counts['scrap']}")
    print(f"Left as male Other:     {counts['male']}")
    print(f"No name match (left as Other): {counts['none']}")

if __name__ == "__main__":
    main()
