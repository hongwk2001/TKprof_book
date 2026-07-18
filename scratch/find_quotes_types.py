import re

for ch in range(19, 25):
    path = f"books/odyssey/chapters/ch_{ch}_ko.txt"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    double_quotes = len(re.findall(r'"', content))
    curly_quotes = len(re.findall(r'[“”]', content))
    single_quotes = len(re.findall(r"'", content))
    print(f"Chapter {ch}: Double={double_quotes}, Curly={curly_quotes}, Single={single_quotes}")
