import re

html_path = 'd:/git_repo/TKprof_book/books/two_cities/original_gutenberg.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# We want to find each image and print the 300 characters preceding it to see the chapter context
matches = re.finditer(r'(?i)<img[^>]*src="images/([^"]+\.jpg)"[^>]*>', html)

print("Image Locations:")
for m in matches:
    img_name = m.group(1)
    start_pos = max(0, m.start() - 500)
    context = html[start_pos:m.start()]
    # Extract the nearest chapter heading before the image
    chapter_matches = re.findall(r'(?i)<h2[^>]*>(.*?)</h2>', html[:m.start()])
    last_chapter = chapter_matches[-1] if chapter_matches else "Unknown Chapter"
    print(f"\n--- {img_name} ---")
    print(f"Nearest Chapter: {last_chapter}")
    print(f"Context text snippet: {context[-150:].strip()}")
