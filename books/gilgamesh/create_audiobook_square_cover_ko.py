import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_COVER = os.path.join(SCRIPT_DIR, "cover_ko.jpg")
DST_COVER_2400 = os.path.join(SCRIPT_DIR, "cover_ko_2400.jpg")
DST_COVER_AUDIO = os.path.join(SCRIPT_DIR, "cover_audio_ko.jpg")

def create_square_korean_cover():
    bg_path = r"C:\Users\hongw\.gemini\antigravity\brain\064036c9-4279-4f05-a462-c186ca897180\gilgamesh_bg_1786553853021.jpg"
    
    if os.path.exists(bg_path):
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
        font_title = ImageFont.truetype('C:/Windows/Fonts/batang.ttc', 170)
        font_sub = ImageFont.truetype('C:/Windows/Fonts/georgiai.ttf', 75)
        font_author_ko = ImageFont.truetype('C:/Windows/Fonts/batang.ttc', 70)
        font_author_en = ImageFont.truetype('C:/Windows/Fonts/georgia.ttf', 50)
        font_pub = ImageFont.truetype('C:/Windows/Fonts/georgiab.ttf', 40)

        def add_text_with_glow(text, y, font, color, glow_color=(0, 0, 0, 240)):
            bbox = draw_txt.textbbox((0, 0), text, font=font)
            tw = bbox[2] - bbox[0]
            x = (2400 - tw) // 2
            draw_shd.text((x, y), text, font=font, fill=glow_color)
            draw_txt.text((x, y), text, font=font, fill=color)

        add_text_with_glow('T K P R O F   C L A S S I C S', 160, font_badge, (245, 225, 175, 255))
        draw_txt.line([(700, 240), (1700, 240)], fill=(245, 225, 175, 220), width=3)

        add_text_with_glow('길가메시 서사시', 300, font_title, (255, 253, 245, 255))
        add_text_with_glow('The Epic of Gilgamesh', 510, font_sub, (240, 215, 155, 255))

        add_text_with_glow('스펙터클 현대 한국어판 오디오북', 1960, font_author_ko, (255, 255, 255, 255))
        add_text_with_glow('Ancient Mesopotamian Epic Audiobook', 2060, font_author_en, (235, 215, 170, 255))
        add_text_with_glow('TKPROF LLC', 2220, font_pub, (210, 210, 210, 255))

        shadow_blurred = shadow_layer.filter(ImageFilter.GaussianBlur(radius=8))
        img_with_shadow = Image.alpha_composite(base, shadow_blurred)
        final_img = Image.alpha_composite(img_with_shadow, text_layer).convert('RGB')

        final_img.save(DST_COVER_2400, format="JPEG", quality=95, dpi=(300, 300))
        final_img.save(DST_COVER_AUDIO, format="JPEG", quality=95, dpi=(300, 300))
        final_img.save(SRC_COVER, format="JPEG", quality=95, dpi=(300, 300))

        size_mb = os.path.getsize(DST_COVER_2400) / (1024 * 1024)
        print(f"✅ Generated 2400x2400 px Square Korean Audiobook Cover: {DST_COVER_2400} ({size_mb:.2f} MB)")
    else:
        # Crop cover_ko.jpg to 1:1 square
        print("Background file not found. Resizing & cropping cover_ko.jpg...")
        with Image.open(SRC_COVER) as img:
            w, h = img.size
            crop_box = (0, 0, w, w) if h >= w else (0, 0, h, h)
            img_square = img.crop(crop_box).resize((2400, 2400), Image.Resampling.LANCZOS).convert("RGB")
            img_square.save(DST_COVER_2400, format="JPEG", quality=95, dpi=(300, 300))
            img_square.save(DST_COVER_AUDIO, format="JPEG", quality=95, dpi=(300, 300))
            print(f"✅ Created 2400x2400 Square Cover: {DST_COVER_2400}")

if __name__ == "__main__":
    create_square_korean_cover()
