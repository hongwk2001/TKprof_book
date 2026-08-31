"""
create_cover_ko.py
Generates high-resolution Korean book cover images (cover_ko.png, cover_ko.jpg, cover.jpg)
for '베오울프: 스펙터클 현대 한국어판 (Beowulf)'.
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BG_PATH = r"C:\Users\hongw\.gemini\antigravity\brain\3ffc7a40-51fe-484a-8ebf-a6665ccb000c\beowulf_ko_cover_bg_1786637791624.jpg"

TARGET_W = 1600
TARGET_H = 2400

def generate_cover():
    if not os.path.exists(BG_PATH):
        print(f"Error: Background image not found at {BG_PATH}")
        return

    bg = Image.open(BG_PATH).convert('RGBA')
    bg_resized = bg.resize((TARGET_W, TARGET_H), Image.Resampling.LANCZOS)

    # Dark vignette overlays for high text legibility
    overlay = Image.new('RGBA', (TARGET_W, TARGET_H), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)

    # Top gradient
    for y in range(750):
        progress = y / 750.0
        alpha = int(210 * (1.0 - (progress ** 1.3)))
        draw_ov.line([(0, y), (TARGET_W, y)], fill=(10, 15, 25, alpha))

    # Bottom gradient
    for y in range(1600, 2400):
        progress = (y - 1600) / 800.0
        alpha = int(225 * (progress ** 1.3))
        draw_ov.line([(0, y), (TARGET_W, y)], fill=(10, 15, 25, alpha))

    base = Image.alpha_composite(bg_resized, overlay)

    # Layers for crisp text and soft drop shadows
    text_layer = Image.new('RGBA', (TARGET_W, TARGET_H), (0, 0, 0, 0))
    shadow_layer = Image.new('RGBA', (TARGET_W, TARGET_H), (0, 0, 0, 0))

    draw_txt = ImageDraw.Draw(text_layer)
    draw_shd = ImageDraw.Draw(shadow_layer)

    # Fonts
    font_badge = ImageFont.truetype('C:/Windows/Fonts/georgiab.ttf', 36)
    font_title = ImageFont.truetype('C:/Windows/Fonts/batang.ttc', 145)
    font_sub_ko = ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf', 52)
    font_sub_en = ImageFont.truetype('C:/Windows/Fonts/georgiai.ttf', 50)
    font_author = ImageFont.truetype('C:/Windows/Fonts/batang.ttc', 55)
    font_pub = ImageFont.truetype('C:/Windows/Fonts/georgiab.ttf', 36)

    def draw_centered_text(text, y, font, fill_color, glow_color=(0, 0, 0, 240)):
        bbox = draw_txt.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        x = (TARGET_W - w) // 2
        draw_shd.text((x, y), text, font=font, fill=glow_color)
        draw_txt.text((x, y), text, font=font, fill=fill_color)

    # Top elements
    badge_str = "T K P R O F   C L A S S I C S"
    draw_centered_text(badge_str, 120, font_badge, (245, 225, 175, 255))

    # Top golden accent line
    draw_txt.line([(550, 185), (1050, 185)], fill=(245, 225, 175, 220), width=2)
    draw_shd.line([(550, 185), (1050, 185)], fill=(0, 0, 0, 200), width=4)

    # Title & Subtitles
    draw_centered_text("베 오 울 프", 240, font_title, (255, 253, 245, 255), glow_color=(5, 10, 20, 250))
    draw_centered_text("스펙터클 현대 한국어판", 415, font_sub_ko, (245, 215, 150, 255), glow_color=(5, 10, 20, 250))
    draw_centered_text("Beowulf: Modern Korean Edition", 485, font_sub_en, (190, 220, 245, 240), glow_color=(5, 10, 20, 250))

    # Golden divider line below title
    draw_txt.line([(650, 565), (950, 565)], fill=(245, 225, 175, 180), width=2)
    draw_shd.line([(650, 565), (950, 565)], fill=(0, 0, 0, 180), width=4)

    # Bottom Credits
    draw_centered_text("작자 미상 지음", 1980, font_author, (255, 255, 255, 255), glow_color=(5, 10, 20, 250))
    draw_centered_text("TKPROF CLASSICS", 2200, font_pub, (245, 225, 175, 255), glow_color=(5, 10, 20, 250))

    # Double Gold Decorative Border
    outer_m = 45
    draw_txt.rectangle([(outer_m, outer_m), (TARGET_W - outer_m, TARGET_H - outer_m)], outline=(245, 225, 175, 150), width=2)
    draw_shd.rectangle([(outer_m, outer_m), (TARGET_W - outer_m, TARGET_H - outer_m)], outline=(0, 0, 0, 180), width=4)

    inner_m = 53
    draw_txt.rectangle([(inner_m, inner_m), (TARGET_W - inner_m, TARGET_H - inner_m)], outline=(245, 225, 175, 90), width=1)

    # Blur shadows for soft natural glow
    shadow_blurred = shadow_layer.filter(ImageFilter.GaussianBlur(radius=7))

    img_with_shadow = Image.alpha_composite(base, shadow_blurred)
    final_img = Image.alpha_composite(img_with_shadow, text_layer)
    final_rgb = final_img.convert('RGB')

    images_dir = os.path.join(BASE_DIR, 'images')
    os.makedirs(images_dir, exist_ok=True)

    # Save to all target locations for EPUB build & D2D upload
    final_rgb.save(os.path.join(BASE_DIR, 'cover_ko.png'))
    final_rgb.save(os.path.join(BASE_DIR, 'cover_ko.jpg'), quality=95, dpi=(300, 300))
    final_rgb.save(os.path.join(images_dir, 'cover_ko.jpg'), quality=95, dpi=(300, 300))
    final_rgb.save(os.path.join(images_dir, 'cover.jpg'), quality=95, dpi=(300, 300))

    print(f"✅ Generated Beowulf Korean Cover Images (1600x2400):")
    print(f"  - {os.path.join(BASE_DIR, 'cover_ko.jpg')}")
    print(f"  - {os.path.join(images_dir, 'cover.jpg')}")

if __name__ == '__main__':
    generate_cover()
