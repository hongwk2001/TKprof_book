import os
import re
from html.parser import HTMLParser

BASE_DIR = r"d:\git_repo\TKprof_book\books\secret_garden"
HTML_FILE = os.path.join(BASE_DIR, "secret_garden.html")
OUTPUT_DIR = os.path.join(BASE_DIR, "chapters")

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

class SecretGardenHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_chapter = False
        self.current_chapter_num = 0
        self.chapters = {}  # chapter_num -> list of text blocks
        self.temp_text = []
        self.h2_depth = 0
        self.p_depth = 0
        self.last_tag = ""

    def handle_starttag(self, tag, attrs):
        self.last_tag = tag
        attrs_dict = dict(attrs)
        
        # Detect start of a chapter
        if tag == "div" and attrs_dict.get("class") == "chapter":
            self.in_chapter = True
            self.current_chapter_num += 1
            self.temp_text = []
            self.div_depth = 1
            
        elif self.in_chapter:
            if tag == "div":
                self.div_depth += 1
            elif tag == "h2":
                self.h2_depth += 1
            elif tag == "p":
                self.p_depth += 1
                
    def handle_endtag(self, tag):
        if self.in_chapter:
            if tag == "div":
                self.div_depth -= 1
                if self.div_depth == 0:
                    # End of chapter
                    self.in_chapter = False
                    self.chapters[self.current_chapter_num] = "".join(self.temp_text)
            elif tag == "h2":
                self.h2_depth = max(0, self.h2_depth - 1)
                # Add separator after header
                self.temp_text.append("\n\n")
            elif tag == "p":
                self.p_depth = max(0, self.p_depth - 1)
                self.temp_text.append("\n\n")
                
    def handle_data(self, data):
        if self.in_chapter:
            # Clean up the text data a bit (extra whitespace)
            clean_data = data.replace("\r", "").replace("\n", " ")
            # If we're inside h2 (header), let's keep it clean
            if self.h2_depth > 0:
                clean_data = clean_data.strip()
                if clean_data:
                    if self.temp_text:
                        self.temp_text.append(" " + clean_data)
                    else:
                        self.temp_text.append(clean_data)
            elif self.p_depth > 0:
                # Inside paragraph: append and let handling of end paragraph clean spacing
                self.temp_text.append(data)

def clean_paragraph_text(text):
    # Normalize spaces: replace multiple spaces with a single space
    lines = text.split("\n")
    cleaned_lines = []
    for line in lines:
        cleaned_line = re.sub(r'[ \t]+', ' ', line).strip()
        cleaned_lines.append(cleaned_line)
        
    text = "\n".join(cleaned_lines)
    
    # Fix standard HTML entity conversions that parser does or doesn't resolve
    replacements = {
        "&ldquo;": "“",
        "&rdquo;": "”",
        "&lsquo;": "‘",
        "&raquo;": "»",
        "&laquo;": "«",
        "&rsquo;": "’",
        "&mdash;": "—",
        "&nbsp;": " ",
        "&amp;": "&",
        "&quot;": '"',
        "&apos;": "'",
        "&lt;": "<",
        "&gt;": ">",
        "“": "“",
        "”": "”",
        "‘": "‘",
        "’": "’",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
        
    # Replace multiple empty lines with a single empty line
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def main():
    print(f"Reading {HTML_FILE}...")
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html_content = f.read()

    parser = SecretGardenHTMLParser()
    parser.feed(html_content)

    print(f"Found {len(parser.chapters)} chapters.")
    for ch_num, ch_text in parser.chapters.items():
        cleaned_text = clean_paragraph_text(ch_text)
        
        # Standardize the file naming
        output_file = os.path.join(OUTPUT_DIR, f"raw_ch_{ch_num:02d}.txt")
        with open(output_file, "w", encoding="utf-8") as out_f:
            out_f.write(cleaned_text)
        print(f"Saved Chapter {ch_num} -> {output_file}")

if __name__ == "__main__":
    main()
