"""
create_scaramouche_ko_covers.py
Generates high-resolution Korean book cover images for Scaramouche Books 1, 2, and 3
(cover_book1_ko.jpg, cover_book2_ko.jpg, cover_book3_ko.jpg).
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TARGET_W = 1600
TARGET_H = 2400

BOOKS_DATA = [
    {
        "num": 1,
        "bg_src": os.path.join(BASE_DIR, "cover_book1.jpg"),
        "title_ko": "스카라무슈 1",
        "subtitle_ko": "법의 옷 (The Robe)",
        "subtitle_en": "Scaramouche: Book 1 - The Robe",
        "out_name": "cover_book1_ko.jpg"
    },
    {
        "num": 2,
        "bg_src": os.path.join(BASE_DIR, "cover_book2.jpg"),
        "title_ko": "스카라무슈 2",
        "subtitle_ko": "배우의 신발 (The Buskin)",
        "subtitle_en": "Scaramouche: Book 2 - The Buskin",
        "out_name": "cover_book2_ko.jpg"
    },
    {
        "num": 3,
        "bg_src": os.path.join(BASE_DIR, "cover_book3.jpg"),
        "title_ko": "스카라무슈 3",
        "subtitle_ko": "검의 언어 (The Sword)",
        "subtitle_en": "Scaramouche: Book 3 - The Sword",
        "out_name": "cover_book3_ko.jpg"
    }
]

def render_cover(data):
    bg_path = data["bg_src"]
    if not os.path.exists(bg_path):
        bg_path = os.path.join(BASE_DIR, f"cover_book{data['num']}.jpg")

    bg = Image.open(bg_path).convert('RGBA')
    bg_resized = bg.resize((TARGET_W, TARGET_H), Image.Resampling.LANCZOS)

    # Dark vignette overlay for legibility
    overlay = Image.new('RGBA', (TARGET_W, TARGET_H), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)

    # Top gradient
    for y in range(750):
        progress = y / 750.0
        alpha = int(215 * (1.0 - (progress ** 1.3)))
        draw_ov.line([(0, y), (TARGET_W, y)], fill=(15, 12, 10, alpha))

    # Bottom gradient
    for y in range(1650, 2400):
        progress = (y - 1650) / 750.0
        alpha = int(220 * (progress ** 1.3))
        draw_ov.line([(0, y), (TARGET_W, y)], fill=(15, 12, 10, alpha))

    base = Image.alpha_composite(bg_resized, overlay)

    # Text & Shadow Layers
    text_layer = Image.new('RGBA', (TARGET_W, TARGET_H), (0, 0, 0, 0))
    shadow_layer = Image.new('RGBA', (TARGET_W, TARGET_H), (0, 0, 0, 0))

    draw_txt = ImageDraw.Draw(text_layer)
    draw_shd = ImageDraw.Draw(shadow_layer)

    font_badge = ImageFont.truetype('C:/Windows/Fonts/georgiab.ttf', 38)
    font_title = ImageFont.truetype('C:/Windows/Fonts/batang.ttc', 140)
    font_sub_ko = ImageFont.truetype('C:/Windows/Fonts/batang.ttc', 60)
    font_sub_en = ImageFont.truetype('C:/Windows/Fonts/georgiai.ttf', 45)
    font_author_ko = ImageFont.truetype('C:/Windows/Fonts/batang.ttc', 65)
    font_author_en = ImageFont.truetype('C:/Windows/Fonts/georgia.ttf', 42)
    font_pub = ImageFont.truetype('C:/Windows/Fonts/georgiab.ttf', 34)

    def add_text_with_glow(text, y, font, color, glow_color=(0, 0, 0, 240)):
        bbox = draw_txt.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        x = (TARGET_W - tw) // 2
        draw_shd.text((x, y), text, font=font, fill=glow_color)
        draw_txt.text((x, y), text, font=font, fill=color)

    # Top elements
    badge_str = 'T K P R O F   C L A S S I C S'
    add_text_with_glow(badge_str, 140, font_badge, (245, 225, 175, 255))

    # Golden rule lines
    draw_txt.line([(550, 205), (1050, 205)], fill=(245, 225, 175, 220), width=2)
    draw_shd.line([(550, 205), (1050, 205)], fill=(0, 0, 0, 200), width=4)

    # Title & Subtitle
    add_text_with_glow(data["title_ko"], 255, font_title, (255, 253, 245, 255), glow_color=(15, 10, 5, 240))
    add_text_with_glow(data["subtitle_ko"], 430, font_sub_ko, (240, 215, 155, 255), glow_color=(15, 10, 5, 240))
    add_text_with_glow(data["subtitle_en"], 515, font_sub_en, (220, 195, 135, 255), glow_color=(15, 10, 5, 240))

    # Gold accent ornament line
    draw_txt.line([(680, 595), (920, 595)], fill=(240, 215, 155, 180), width=2)
    draw_shd.line([(680, 595), (920, 595)], fill=(0, 0, 0, 180), width=4)

    # Bottom elements
    add_text_with_glow('라파엘 사바티니 지음 | TKPROF LLC 편역', 1980, font_author_ko, (255, 255, 255, 255))
    add_text_with_glow('Rafael Sabatini | Translated & Edited by TKPROF LLC', 2065, font_author_en, (235, 215, 170, 255))

    # Publisher logo text
    add_text_with_glow('TKPROF LLC', 2220, font_pub, (210, 210, 210, 255))

    # Outer double gold frame border
    border_margin = 45
    draw_txt.rectangle([(border_margin, border_margin), (TARGET_W - border_margin, TARGET_H - border_margin)], outline=(245, 225, 175, 140), width=2)
    draw_shd.rectangle([(border_margin, border_margin), (TARGET_W - border_margin, TARGET_H - border_margin)], outline=(0, 0, 0, 160), width=4)

    border_inner = 53
    draw_txt.rectangle([(border_inner, border_inner), (TARGET_W - border_inner, TARGET_H - border_inner)], outline=(245, 225, 175, 80), width=1)

    # Soft drop shadow via Gaussian Blur
    shadow_blurred = shadow_layer.filter(ImageFilter.GaussianBlur(radius=6))

    img_with_shadow = Image.alpha_composite(base, shadow_blurred)
    final_img = Image.alpha_composite(img_with_shadow, text_layer)

    final_rgb = final_img.convert('RGB')
    
    out_file = os.path.join(BASE_DIR, data["out_name"])
    final_rgb.save(out_file, quality=95, dpi=(300, 300))
    print(f"✅ Generated {data['out_name']} successfully.")

def main():
    for bdata in BOOKS_DATA:
        render_cover(bdata)

if __name__ == '__main__':
    main()
