"""
create_cover_ko.py
Generates high-resolution Korean book cover image (cover_ko.jpg - 1600x2400)
for '블루 캐슬 (The Blue Castle)'.
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_JPG = os.path.join(BASE_DIR, "cover_ko.jpg")

TARGET_W = 1600
TARGET_H = 2400

def generate_cover():
    # Deep royal blue to twilight indigo background gradient
    cover = Image.new("RGB", (TARGET_W, TARGET_H), "#0f172a")
    draw = ImageDraw.Draw(cover)

    # Rich blue gradient fill
    top_color = (15, 23, 42)      # Deep dark slate / blue
    mid_color = (30, 58, 138)     # Royal blue
    bottom_color = (15, 23, 42)   # Deep night blue

    for y in range(TARGET_H):
        if y < TARGET_H // 2:
            r = int(top_color[0] + (mid_color[0] - top_color[0]) * (y / (TARGET_H / 2)))
            g = int(top_color[1] + (mid_color[1] - top_color[1]) * (y / (TARGET_H / 2)))
            b = int(top_color[2] + (mid_color[2] - top_color[2]) * (y / (TARGET_H / 2)))
        else:
            ratio = (y - TARGET_H / 2) / (TARGET_H / 2)
            r = int(mid_color[0] + (bottom_color[0] - mid_color[0]) * ratio)
            g = int(mid_color[1] + (bottom_color[1] - mid_color[1]) * ratio)
            b = int(mid_color[2] + (bottom_color[2] - mid_color[2]) * ratio)
        draw.line([(0, y), (TARGET_W, y)], fill=(r, g, b))

    # Decorative inner gold border frame
    margin = 80
    draw.rectangle(
        [margin, margin, TARGET_W - margin, TARGET_H - margin],
        outline="#d4af37",
        width=6
    )
    draw.rectangle(
        [margin + 16, margin + 16, TARGET_W - margin - 16, TARGET_H - margin - 16],
        outline="#93c5fd",
        width=2
    )

    # Load fonts (fallback to Batang/Georgia if system font)
    font_badge = None
    font_title = None
    font_sub = None
    font_author = None
    font_pub = None

    font_paths_ko = ['C:/Windows/Fonts/batang.ttc', 'C:/Windows/Fonts/malgun.ttf']
    font_paths_en = ['C:/Windows/Fonts/georgiab.ttf', 'C:/Windows/Fonts/georgia.ttf']

    for fp in font_paths_en:
        if os.path.exists(fp):
            font_badge = ImageFont.truetype(fp, 36)
            font_sub = ImageFont.truetype(fp, 56)
            font_pub = ImageFont.truetype(fp, 38)
            break

    for fp in font_paths_ko:
        if os.path.exists(fp):
            font_title = ImageFont.truetype(fp, 130)
            font_author = ImageFont.truetype(fp, 60)
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

    def draw_centered_text(text, y, font, fill="#ffffff"):
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        x = (TARGET_W - w) / 2
        draw.text((x, y), text, font=font, fill=fill)

    # Render Text Elements
    draw_centered_text("MODERN CLASSIC EDITION", 300, font_badge, fill="#d4af37")
    draw_centered_text("블 루 캐 슬", 750, font_title, fill="#ffffff")
    draw_centered_text("The Blue Castle", 960, font_sub, fill="#93c5fd")
    
    draw_centered_text("L. M. 몽고메리 지음", 1550, font_author, fill="#e2e8f0")
    draw_centered_text("TKPROF CLASSICS", 2050, font_pub, fill="#d4af37")

    cover.save(OUT_JPG, "JPEG", quality=95)
    print(f"✅ Generated Cover Image: {OUT_JPG} (Size: {os.path.getsize(OUT_JPG) / 1024:.1f} KB)")

if __name__ == "__main__":
    generate_cover()
