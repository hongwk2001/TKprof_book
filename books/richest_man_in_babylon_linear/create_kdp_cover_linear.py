from PIL import Image, ImageDraw, ImageFont
import os

# Paths
bg_image_path = r"C:\Users\hongw\.gemini\antigravity\brain\e0b575b9-9684-474c-9977-720c3de7f183\babylon_cover_bg_1784311094542.png"
output_path = r"d:\git_repo\TKprof_book\books\richest_man_in_babylon_linear\cover_kdp.jpg"

# Target dimensions
TARGET_WIDTH = 1600
TARGET_HEIGHT = 2560

# Load background
img = Image.open(bg_image_path)
orig_width, orig_height = img.size

# Resize and crop to fill TARGET_WIDTH x TARGET_HEIGHT
aspect_ratio_target = TARGET_WIDTH / TARGET_HEIGHT
aspect_ratio_orig = orig_width / orig_height

if aspect_ratio_orig > aspect_ratio_target:
    new_height = TARGET_HEIGHT
    new_width = int(orig_width * (TARGET_HEIGHT / orig_height))
    img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    left = (new_width - TARGET_WIDTH) // 2
    top = 0
    right = left + TARGET_WIDTH
    bottom = TARGET_HEIGHT
    img_cropped = img_resized.crop((left, top, right, bottom))
else:
    new_width = TARGET_WIDTH
    new_height = int(orig_height * (TARGET_WIDTH / orig_width))
    img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    left = 0
    top = (new_height - TARGET_HEIGHT) // 2
    right = TARGET_WIDTH
    bottom = top + TARGET_HEIGHT
    img_cropped = img_resized.crop((left, top, right, bottom))

# Create a clean RGB copy
final_img = img_cropped.convert("RGB")
draw = ImageDraw.Draw(final_img)

# Typography configuration
try:
    font_path_title = r"C:\Windows\Fonts\georgiab.ttf" # Georgia Bold
    font_path_regular = r"C:\Windows\Fonts\georgia.ttf" # Georgia Regular
    font_path_italic = r"C:\Windows\Fonts\georgiai.ttf" # Georgia Italic
    
    font_title = ImageFont.truetype(font_path_title, 110)
    font_subtitle = ImageFont.truetype(font_path_italic, 65)
    font_desc = ImageFont.truetype(font_path_regular, 38)
    font_author = ImageFont.truetype(font_path_title, 70)
    font_publisher = ImageFont.truetype(font_path_regular, 40)
except IOError:
    font_title = ImageFont.load_default()
    font_subtitle = ImageFont.load_default()
    font_desc = ImageFont.load_default()
    font_author = ImageFont.load_default()
    font_publisher = ImageFont.load_default()

def draw_text_centered_with_shadow(text, y, font, fill_color, shadow_color="#000000", shadow_offset=3):
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    x = (TARGET_WIDTH - text_w) // 2
    
    for dx in range(-shadow_offset, shadow_offset + 1):
        for dy in range(-shadow_offset, shadow_offset + 1):
            if abs(dx) + abs(dy) > 0:
                draw.text((x + dx, y + dy), text, font=font, fill=shadow_color)
                
    draw.text((x, y), text, font=font, fill=fill_color)

# Draw Title
title_color = "#F7D070"  # Rich gold
draw_text_centered_with_shadow("THE RICHEST MAN", 350, font_title, title_color)
draw_text_centered_with_shadow("IN BABYLON", 490, font_title, title_color)

# Draw Subtitle
subtitle_color = "#E6C280" # Warm gold/bronze
draw_text_centered_with_shadow("Recreated as a Novel", 640, font_subtitle, subtitle_color)

# Draw Description
desc_color = "#FFFFFF" # Silver/white
draw_text_centered_with_shadow("The Timeless Wealth Parables in a Single Chronological Story", 740, font_desc, desc_color)

# Draw Author
author_color = "#F3E5AB" # Soft cream/parchment
draw_text_centered_with_shadow("GEORGE S. CLASON", 1950, font_author, author_color)

# Draw Publisher
publisher_color = "#C0C0C0" # Silver/light gray
draw_text_centered_with_shadow("TKPROF LLC", 2150, font_publisher, publisher_color)

# Save image with 300 DPI, RGB color mode, and minimal compression (quality=95)
final_img.save(
    output_path, 
    "JPEG", 
    quality=95, 
    dpi=(300, 300)
)

print(f"Successfully generated KDP linear cover at {output_path}")
