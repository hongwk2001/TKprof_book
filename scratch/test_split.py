import re

filepath = r"C:\Users\hongw\.gemini\antigravity\brain\9a5fe6dc-1f15-4d6a-8c11-a75866ccab95\.system_generated\steps\80\content.md"

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

def print_chapters(start_line, end_line, name):
    print(f"\n=== Chapters in {name} ===")
    text = "".join(lines[start_line-1:end_line])
    matches = list(re.finditer(r"\n\s*([I|V|X|L]+)\.\s", text))
    print(f"Found {len(matches)} chapters")
    if matches:
        print(f"First chapter: {matches[0].group(1)}")
        print(f"Last chapter: {matches[-1].group(1)}")

print_chapters(1530, 2429, "Of Anger Book I")
print_chapters(2430, 3659, "Of Anger Book II")
print_chapters(3660, 5135, "Of Anger Book III")
print_chapters(7898, 9076, "Of Peace of Mind")
