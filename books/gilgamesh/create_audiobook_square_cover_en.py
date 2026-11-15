import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_COVER_EN = os.path.join(SCRIPT_DIR, "cover_en.jpg")
DST_COVER_2400 = os.path.join(SCRIPT_DIR, "cover_en_2400.jpg")

def create_square_english_cover():
    bg_path = r"C:\Users\hongw\.gemini\antigravity\brain\064036c9-4279-4f05-a462-c186ca897180\gilgamesh_bg_1786553853021.jpg"
    
    if not os.path.exists(bg_path):
        bg_path = os.path.join(SCRIPT_DIR, "cover_en.png")
    if not os.path.exists(bg_path):
        bg_path = os.path.join(SCRIPT_DIR, "cover_ko.png")

    print(f"Using background source: {bg_path}")
    bg = Image.open(bg_path).convert('RGBA')
    TARGET_SIZE = (2400, 2400)
    
    # Center crop background to 1:1 square
    w, h = bg.size
    min_dim = min(w, h)
    crop_box = ((w - min_dim) // 2, (h - min_dim) // 2, (w + min_dim) // 2, (h + min_dim) // 2)
    bg_square = bg.crop(crop_box).resize(TARGET_SIZE, Image.Resampling.LANCZOS)
    
    # Overlay gradient
    overlay = Image.new('RGBA', TARGET_SIZE, (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)

    # Top gradient
    for y in range(750):
        progress = y / 750.0
        alpha = int(215 * (1.0 - (progress ** 1.3)))
        draw_ov.line([(0, y), (2400, y)], fill=(15, 12, 10, alpha))

    # Bottom gradient
    for y in range(1650, 2400):
        progress = (y - 1650) / 750.0
        alpha = int(220 * (progress ** 1.3))
        draw_ov.line([(0, y), (2400, y)], fill=(15, 12, 10, alpha))

    base = Image.alpha_composite(bg_square, overlay)

    # Text & Shadow Layers
    text_layer = Image.new('RGBA', TARGET_SIZE, (0, 0, 0, 0))
    shadow_layer = Image.new('RGBA', TARGET_SIZE, (0, 0, 0, 0))

    draw_txt = ImageDraw.Draw(text_layer)
    draw_shd = ImageDraw.Draw(shadow_layer)

    font_badge = ImageFont.truetype('C:/Windows/Fonts/georgiab.ttf', 45)
    font_title = ImageFont.truetype('C:/Windows/Fonts/georgiab.ttf', 140)
    font_sub = ImageFont.truetype('C:/Windows/Fonts/georgiai.ttf', 75)
    font_author_en = ImageFont.truetype('C:/Windows/Fonts/georgia.ttf', 60)
    font_pub = ImageFont.truetype('C:/Windows/Fonts/georgiab.ttf', 45)

    def add_text_with_glow(text, y, font, color, glow_color=(0, 0, 0, 240)):
        bbox = draw_txt.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        x = (2400 - tw) // 2
        draw_shd.text((x, y), text, font=font, fill=glow_color)
        draw_txt.text((x, y), text, font=font, fill=color)

    add_text_with_glow('T K P R O F   C L A S S I C S', 160, font_badge, (245, 225, 175, 255))
    draw_txt.line([(700, 240), (1700, 240)], fill=(245, 225, 175, 220), width=3)

    add_text_with_glow('The Epic of Gilgamesh', 300, font_title, (255, 253, 245, 255))
    add_text_with_glow('Modern English Edition', 480, font_sub, (240, 215, 155, 255))

    add_text_with_glow('Ancient Mesopotamian Epic Audiobook', 1980, font_author_en, (235, 215, 170, 255))
    add_text_with_glow('TKPROF LLC', 2180, font_pub, (210, 210, 210, 255))

    # Outer double gold frame border
    border_margin = 60
    draw_txt.rectangle([(border_margin, border_margin), (2400 - border_margin, 2400 - border_margin)], outline=(245, 225, 175, 140), width=3)
    draw_shd.rectangle([(border_margin, border_margin), (2400 - border_margin, 2400 - border_margin)], outline=(0, 0, 0, 160), width=5)

    shadow_blurred = shadow_layer.filter(ImageFilter.GaussianBlur(radius=8))
    img_with_shadow = Image.alpha_composite(base, shadow_blurred)
    final_img = Image.alpha_composite(img_with_shadow, text_layer).convert('RGB')

    final_img.save(DST_COVER_2400, format="JPEG", quality=95, dpi=(300, 300))

    size_mb = os.path.getsize(DST_COVER_2400) / (1024 * 1024)
    print(f"✅ Generated 2400x2400 px Square English Audiobook Cover: {DST_COVER_2400} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    create_square_english_cover()
