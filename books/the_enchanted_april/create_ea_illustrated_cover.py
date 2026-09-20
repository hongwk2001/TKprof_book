"""
create_ea_illustrated_cover.py
Composites professional typography onto flat 2D artwork
to produce a 2400x2400 square Audiobook Cover Image for '마법에 걸린 4월 (The Enchanted April)'.
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ART_SRC = r"C:\Users\hongw\.gemini\antigravity\brain\4c130b5f-99eb-4f65-9a16-5942bd9fe6f1\enchanted_april_flat_art_1to1_1786760109365.jpg"
OUT_JPG = r"C:\git_repo\TKprof_book\books\the_enchanted_april\cover_ko_audio_2400.jpg"

TARGET_W = 2400
TARGET_H = 2400

def generate_ea_cover():
    print(f"Loading artwork from {ART_SRC}...")
    with Image.open(ART_SRC) as art:
        art = art.convert("RGB")
        art = art.resize((TARGET_W, TARGET_H), Image.Resampling.LANCZOS)

        # Gradient overlays at top and bottom for readability
        overlay = Image.new("RGBA", (TARGET_W, TARGET_H), (0, 0, 0, 0))
        ol_draw = ImageDraw.Draw(overlay)

        for y in range(450):
            alpha = int(170 * (1 - y / 450))
            ol_draw.line([(0, y), (TARGET_W, y)], fill=(15, 23, 42, alpha))

        for y in range(1750, TARGET_H):
            alpha = int(220 * ((y - 1750) / 650))
            ol_draw.line([(0, y), (TARGET_W, y)], fill=(15, 23, 42, alpha))

        art = Image.alpha_composite(art.convert("RGBA"), overlay).convert("RGB")
        draw = ImageDraw.Draw(art)

        # Gold frame border
        margin = 80
        draw.rectangle(
            [margin, margin, TARGET_W - margin, TARGET_H - margin],
            outline="#d4af37",
            width=6
        )
        draw.rectangle(
            [margin + 16, margin + 16, TARGET_W - margin - 16, TARGET_H - margin - 16],
            outline="#fef08a",
            width=2
        )

        # Load fonts
        font_badge = None
        font_title = None
        font_sub = None
        font_author = None
        font_pub = None

        font_paths_ko = ['C:/Windows/Fonts/batang.ttc', 'C:/Windows/Fonts/malgun.ttf']
        font_paths_en = ['C:/Windows/Fonts/georgiab.ttf', 'C:/Windows/Fonts/georgia.ttf']

        for fp in font_paths_en:
            if os.path.exists(fp):
                font_badge = ImageFont.truetype(fp, 48)
                font_sub = ImageFont.truetype(fp, 75)
                font_pub = ImageFont.truetype(fp, 52)
                break

        for fp in font_paths_ko:
            if os.path.exists(fp):
                font_title = ImageFont.truetype(fp, 165)
                font_author = ImageFont.truetype(fp, 80)
                break

        if not font_title:
            font_title = ImageFont.load_default()
        if not font_badge:
            font_badge = ImageFont.load_default()
        if not font_sub:
            font_sub = ImageFont.load_default()
        if not font_author:
            font_author = ImageFont.load_default()
        if not font_pub:
            font_pub = ImageFont.load_default()

        def draw_centered_text_with_shadow(text, y, font, fill="#ffffff", shadow="#000000"):
            bbox = draw.textbbox((0, 0), text, font=font)
            w = bbox[2] - bbox[0]
            x = (TARGET_W - w) / 2
            draw.text((x + 4, y + 4), text, font=font, fill=shadow)
            draw.text((x, y), text, font=font, fill=fill)

        # Render Text Elements
        draw_centered_text_with_shadow("CLASSIC ROMANCE AUDIOBOOK", 180, font_badge, fill="#fef08a", shadow="#0f172a")
        draw_centered_text_with_shadow("마법에 걸린 4월", 1840, font_title, fill="#ffffff", shadow="#0f172a")
        draw_centered_text_with_shadow("The Enchanted April", 2040, font_sub, fill="#fef08a", shadow="#0f172a")
        draw_centered_text_with_shadow("엘리자베스 폰 아르님 지음  |  낭독: TKPROF AI", 2160, font_author, fill="#e2e8f0", shadow="#0f172a")

        art.save(OUT_JPG, "JPEG", quality=95)
        file_size_mb = os.path.getsize(OUT_JPG) / (1024 * 1024)
        print(f"✅ Generated Flat 2D 2400x2400 Cover Image: {OUT_JPG}")
        print(f"   Size: {file_size_mb:.2f} MB | Dimensions: 2400 x 2400 px | Color: RGB")

        return OUT_JPG

if __name__ == "__main__":
    generate_ea_cover()
