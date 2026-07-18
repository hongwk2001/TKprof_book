with open(r"d:\git_repo\TKprof_book\books\odyssey\chapters\ch_14_ko.txt", "r", encoding="utf-8") as f:
    content = f.read()

quotes = set()
for char in content:
    if char in ['"', '“', '”', '‘', '’']:
        quotes.add(char)
print("Quotes found in file:", quotes)

# Check if there are quotes and print first occurrences
import re
print("Matches with double straight quotes:", len(re.findall(r'"', content)))
print("Matches with curly quotes:", len(re.findall(r'[“”]', content)))
print("First 1000 characters:")
print(content[:1000])
