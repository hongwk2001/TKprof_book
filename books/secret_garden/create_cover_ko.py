"""
create_cover_ko.py
Generates high-resolution Korean book cover images (cover_ko.png, cover_ko.jpg, cover.png, cover.jpg)
for '비밀의 화원 (The Secret Garden)'.
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BG_PATH = r"C:\Users\hongw\.gemini\antigravity\brain\064036c9-4279-4f05-a462-c186ca897180\secret_garden_bg_1786553040371.jpg"

TARGET_W = 1600
TARGET_H = 2400

def main():
    if not os.path.exists(BG_PATH):
        raise FileNotFoundError(f"Background image not found at {BG_PATH}")

    bg = Image.open(BG_PATH).convert('RGBA')
    bg_resized = bg.resize((TARGET_W, TARGET_H), Image.Resampling.LANCZOS)

    # Dark vignette overlay for legibility
    overlay = Image.new('RGBA', (TARGET_W, TARGET_H), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)

    # Top gradient
    for y in range(750):
        progress = y / 750.0
        alpha = int(215 * (1.0 - (progress ** 1.3)))
        draw_ov.line([(0, y), (TARGET_W, y)], fill=(10, 20, 15, alpha))

    # Bottom gradient
    for y in range(1650, 2400):
        progress = (y - 1650) / 750.0
        alpha = int(220 * (progress ** 1.3))
        draw_ov.line([(0, y), (TARGET_W, y)], fill=(10, 20, 15, alpha))

    base = Image.alpha_composite(bg_resized, overlay)

    # Text & Shadow Layers
    text_layer = Image.new('RGBA', (TARGET_W, TARGET_H), (0, 0, 0, 0))
    shadow_layer = Image.new('RGBA', (TARGET_W, TARGET_H), (0, 0, 0, 0))

    draw_txt = ImageDraw.Draw(text_layer)
    draw_shd = ImageDraw.Draw(shadow_layer)

    font_badge = ImageFont.truetype('C:/Windows/Fonts/georgiab.ttf', 38)
    font_title = ImageFont.truetype('C:/Windows/Fonts/batang.ttc', 140)
    font_sub = ImageFont.truetype('C:/Windows/Fonts/georgiai.ttf', 65)
    font_author_ko = ImageFont.truetype('C:/Windows/Fonts/batang.ttc', 65)
    font_author_en = ImageFont.truetype('C:/Windows/Fonts/georgia.ttf', 44)
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
    add_text_with_glow('비밀의 화원', 255, font_title, (255, 253, 245, 255), glow_color=(5, 15, 10, 240))
    add_text_with_glow('The Secret Garden', 430, font_sub, (240, 215, 155, 255), glow_color=(5, 15, 10, 240))

    # Gold accent ornament line
    draw_txt.line([(680, 525), (920, 525)], fill=(240, 215, 155, 180), width=2)
    draw_shd.line([(680, 525), (920, 525)], fill=(0, 0, 0, 180), width=4)

    # Bottom elements
    add_text_with_glow('프랜시스 호지슨 버넷', 1980, font_author_ko, (255, 255, 255, 255))
    add_text_with_glow('Frances Hodgson Burnett', 2065, font_author_en, (235, 215, 170, 255))

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
    
    out_files = [
        os.path.join(BASE_DIR, 'cover_ko.png'),
        os.path.join(BASE_DIR, 'cover_ko.jpg'),
        os.path.join(BASE_DIR, 'cover.png'),
        os.path.join(BASE_DIR, 'cover.jpg')
    ]
    for out_path in out_files:
        if out_path.endswith('.jpg'):
            final_rgb.save(out_path, quality=95, dpi=(300, 300))
        else:
            final_rgb.save(out_path)

    print("Generated all cover files successfully.")

if __name__ == '__main__':
    main()
