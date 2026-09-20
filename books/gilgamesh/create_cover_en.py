"""
create_cover_en.py
Generates high-resolution English book cover images (cover_en.png, cover_en.jpg)
for 'The Epic of Gilgamesh'.
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BG_PATH = r"C:\Users\hongw\.gemini\antigravity\brain\064036c9-4279-4f05-a462-c186ca897180\gilgamesh_bg_1786553853021.jpg"

TARGET_W = 1600
TARGET_H = 2400

def main():
    if not os.path.exists(BG_PATH):
        # Fallback to local cover_ko background if artifact path moved
        print(f"Warning: Primary BG not found at {BG_PATH}. Checking local cover images.")

    bg = Image.open(BG_PATH).convert('RGBA') if os.path.exists(BG_PATH) else Image.open(os.path.join(BASE_DIR, "cover_ko.png")).convert('RGBA')
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
    font_title = ImageFont.truetype('C:/Windows/Fonts/georgiab.ttf', 110)
    font_sub = ImageFont.truetype('C:/Windows/Fonts/georgiai.ttf', 55)
    font_author = ImageFont.truetype('C:/Windows/Fonts/georgia.ttf', 48)
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
    add_text_with_glow('The Epic of Gilgamesh', 280, font_title, (255, 253, 245, 255), glow_color=(15, 10, 5, 240))
    add_text_with_glow('Modern English Edition', 430, font_sub, (240, 215, 155, 255), glow_color=(15, 10, 5, 240))

    # Gold accent ornament line
    draw_txt.line([(680, 525), (920, 525)], fill=(240, 215, 155, 180), width=2)
    draw_shd.line([(680, 525), (920, 525)], fill=(0, 0, 0, 180), width=4)

    # Bottom elements
    add_text_with_glow('Ancient Mesopotamian Epic', 2040, font_author, (235, 215, 170, 255))

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
    
    images_dir = os.path.join(BASE_DIR, 'images')
    os.makedirs(images_dir, exist_ok=True)
    
    final_rgb.save(os.path.join(BASE_DIR, 'cover_en.png'))
    final_rgb.save(os.path.join(BASE_DIR, 'cover_en.jpg'), quality=95, dpi=(300, 300))
    final_rgb.save(os.path.join(images_dir, 'cover_en.png'))
    final_rgb.save(os.path.join(images_dir, 'cover_en.jpg'), quality=95, dpi=(300, 300))
    print("✅ Generated Gilgamesh English cover images successfully.")

if __name__ == '__main__':
    main()
