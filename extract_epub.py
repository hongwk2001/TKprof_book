import os
import zipfile
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = []
    def handle_data(self, d):
        self.text.append(d)
    def get_data(self):
        return ''.join(self.text)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

epub_path = r"d:\git_repo\TKprof_book\books\think_and_grow_rich\napoleon-hill_think-and-grow-rich.epub"
out_path = r"d:\git_repo\TKprof_book\books\think_and_grow_rich\think_and_grow_rich_raw.txt"

all_text = []

try:
    with zipfile.ZipFile(epub_path, 'r') as epub:
        # Get all html/xhtml files in the epub
        html_files = [f for f in epub.namelist() if f.endswith('.html') or f.endswith('.xhtml') or f.endswith('.htm')]
        # Sort them (this may not perfectly match the spine, but it's close enough for raw extraction if they are named sequentially)
        html_files.sort()
        
        for file in html_files:
            html_content = epub.read(file).decode('utf-8', errors='ignore')
            text = strip_tags(html_content)
            all_text.append(text)
            
    with open(out_path, 'w', encoding='utf-8') as out:
        out.write("\n\n".join(all_text))
        
    print(f"Successfully extracted text to {os.path.basename(out_path)}")
except Exception as e:
    print(f"Error extracting EPUB: {e}")
