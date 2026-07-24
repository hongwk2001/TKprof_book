import urllib.request
import re
import os
import sys
import html as html_module

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")
os.makedirs(CHAPTERS_DIR, exist_ok=True)

ROMAN_NUMERALS = [
    "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
    "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX"
]

CHAPTER_TITLES = [
    "The Complaint of Short Life",
    "How Men Waste Time",
    "Guarding Your Life's Hours",
    "Augustus and the Longing for Leisure",
    "Cicero's Struggle with Public Life",
    "Livius Drusus and Restless Ambition",
    "The Distracted Mind",
    "The Illusion of Endless Time",
    "Living in the Present",
    "The Three Times of Life",
    "The Fear of Death",
    "The Trifles of Trivial Pursuits",
    "Pedantry vs. Wisdom",
    "Friendship with Great Minds",
    "True Immortality",
    "The Anxiety of the Busy",
    "The Sudden End of Power",
    "Paulinus' Advice to Retire",
    "The Dignity of Philosophy",
    "The Tranquil Conclusion"
]

def fetch_and_segment_all_chapters():
    headers = {'User-Agent': 'Mozilla/5.0'}

    for idx, roman in enumerate(ROMAN_NUMERALS, 1):
        ch_str = str(idx).zfill(2)
        url = f"https://en.wikisource.org/wiki/On_the_shortness_of_life/Chapter_{roman}"
        out_path = os.path.join(CHAPTERS_DIR, f"ch_{ch_str}_en.txt")
        title = CHAPTER_TITLES[idx-1]

        try:
            req = urllib.request.Request(url, headers=headers)
            html_raw = urllib.request.urlopen(req, timeout=30).read().decode('utf-8', errors='ignore')

            # Extract main content div
            body_match = re.search(r'<div class="mw-parser-output">(.*?)</div><!-- #mw-content-text -->', html_raw, re.DOTALL)
            if body_match:
                content_html = body_match.group(1)
            else:
                content_html = html_raw

            # Strip non-text elements
            content_html = re.sub(r'<table.*?>.*?</table>', '', content_html, flags=re.DOTALL)
            content_html = re.sub(r'<div class="header.*?">.*?</div>', '', content_html, flags=re.DOTALL)
            content_html = re.sub(r'<script.*?>.*?</script>', '', content_html, flags=re.DOTALL)
            content_html = re.sub(r'<style.*?>.*?</style>', '', content_html, flags=re.DOTALL)

            # Convert paragraphs and headers
            paragraphs = re.findall(r'<p.*?>(.*?)</p>', content_html, re.DOTALL)
            clean_paragraphs = []
            for p in paragraphs:
                text_p = re.sub(r'<[^>]+>', '', p)
                text_p = html_module.unescape(text_p).strip()
                # Clean up footnoted bracket numbers like [1], [2]
                text_p = re.sub(r'\[\d+\]', '', text_p)
                if text_p:
                    clean_paragraphs.append(text_p)

            body_text = "\n\n".join(clean_paragraphs)
            full_text = f"Chapter {roman}: {title}\n\n{body_text}\n"

            with open(out_path, "w", encoding="utf-8") as f:
                f.write(full_text)

            print(f"Saved Chapter {ch_str} ({roman}): {out_path} ({len(full_text)} chars)")

        except Exception as e:
            print(f"Error fetching Chapter {roman} ({url}): {e}")

if __name__ == "__main__":
    fetch_and_segment_all_chapters()
