"""
create_illustrated_cover_ko.py
Generates high-resolution Korean book cover image (cover_ko.jpg - 1600x2400)
using the rich oil painting background illustration for '블루 캐슬 (The Blue Castle)'.
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BG_PATH = r"C:\Users\hongw\.gemini\antigravity\brain\f9b25ca0-1f2c-4482-aaf5-5fa1cd99d8ad\blue_castle_clean_bg_1786635385282.jpg"
OUT_JPG = os.path.join(BASE_DIR, "cover_ko.jpg")

TARGET_W = 1600
TARGET_H = 2400

def generate_illustrated_cover():
    if not os.path.exists(BG_PATH):
        raise FileNotFoundError(f"Background image not found at {BG_PATH}")

    bg = Image.open(BG_PATH).convert("RGBA")
    bg_resized = bg.resize((TARGET_W, TARGET_H), Image.Resampling.LANCZOS)

    # Gradient overlay to ensure text contrast at top and bottom
    overlay = Image.new("RGBA", (TARGET_W, TARGET_H), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)

    # Top gradient overlay (for title)
    for y in range(750):
        progress = y / 750.0
        alpha = int(220 * (1.0 - (progress ** 1.2)))
        draw_ov.line([(0, y), (TARGET_W, y)], fill=(12, 20, 35, alpha))

    # Bottom gradient overlay (for author and publisher)
    for y in range(1650, 2400):
        progress = (y - 1650) / 750.0
        alpha = int(230 * (progress ** 1.2))
        draw_ov.line([(0, y), (TARGET_W, y)], fill=(12, 20, 35, alpha))

    base = Image.alpha_composite(bg_resized, overlay)

    # Text & Shadow Layer
    text_layer = Image.new("RGBA", (TARGET_W, TARGET_H), (0, 0, 0, 0))
    shadow_layer = Image.new("RGBA", (TARGET_W, TARGET_H), (0, 0, 0, 0))

    draw_txt = ImageDraw.Draw(text_layer)
    draw_shd = ImageDraw.Draw(shadow_layer)

    # Fonts
    font_badge = ImageFont.truetype("C:/Windows/Fonts/georgiab.ttf", 36)
    font_title = ImageFont.truetype("C:/Windows/Fonts/batang.ttc", 135)
    font_sub = ImageFont.truetype("C:/Windows/Fonts/georgiai.ttf", 60)
    font_author = ImageFont.truetype("C:/Windows/Fonts/batang.ttc", 65)
    font_pub = ImageFont.truetype("C:/Windows/Fonts/georgiab.ttf", 36)

    def draw_text_with_shadow(text, y, font, color, shadow_color=(0, 0, 0, 220)):
        bbox = draw_txt.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        x = (TARGET_W - w) / 2
        
        # Shadow offset
        for dx, dy in [(-3, -3), (3, -3), (-3, 3), (3, 3), (0, 4), (4, 0)]:
            draw_shd.text((x + dx, y + dy), text, font=font, fill=shadow_color)
        
        draw_txt.text((x, y), text, font=font, fill=color)

    # Render Typography
    draw_text_with_shadow("MODERN CLASSIC EDITION", 220, font_badge, color="#fef08a")
    draw_text_with_shadow("블 루 캐 슬", 320, font_title, color="#ffffff")
    draw_text_with_shadow("The Blue Castle", 480, font_sub, color="#93c5fd")

    draw_text_with_shadow("L. M. 몽고메리 지음", 1920, font_author, color="#f8fafc")
    draw_text_with_shadow("TKPROF CLASSICS", 2080, font_pub, color="#fef08a")

    # Combine text with shadow
    shadow_blurred = shadow_layer.filter(ImageFilter.GaussianBlur(radius=4))
    composed = Image.alpha_composite(base, shadow_blurred)
    final_img = Image.alpha_composite(composed, text_layer).convert("RGB")

    # Save output
    final_img.save(OUT_JPG, "JPEG", quality=95)
    print(f"✅ Created Illustrated Korean Cover: {OUT_JPG} (Size: {os.path.getsize(OUT_JPG) / 1024:.1f} KB)")

if __name__ == "__main__":
    generate_illustrated_cover()
