from PIL import Image, ImageDraw, ImageFont
import os

image_path = r"C:\Users\hongw\.gemini\antigravity\brain\96b565ac-4763-4733-a1cb-a40d338f08be\richest_man_babylon_cover_1783004036625.png"
output_path = r"d:\git_repo\TKprof_book\books\richest_man_in_babylon\cover_with_text.png"

# Load image
img = Image.open(image_path)
draw = ImageDraw.Draw(img)

width, height = img.size

# Try to load a nice font, fallback to default
try:
    title_font = ImageFont.truetype(r"C:\Windows\Fonts\georgia.ttf", int(height * 0.08))
    author_font = ImageFont.truetype(r"C:\Windows\Fonts\georgia.ttf", int(height * 0.04))
    publisher_font = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", int(height * 0.03))
except IOError:
    try:
        title_font = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", int(height * 0.08))
        author_font = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", int(height * 0.04))
        publisher_font = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", int(height * 0.03))
    except IOError:
        title_font = ImageFont.load_default()
        author_font = ImageFont.load_default()
        publisher_font = ImageFont.load_default()

def draw_text_centered(text, y, font, fill="white", stroke_fill="black"):
    # get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) / 2
    # Add a slight shadow/stroke for readability
    draw.text((x-2, y-2), text, font=font, fill=stroke_fill)
    draw.text((x+2, y-2), text, font=font, fill=stroke_fill)
    draw.text((x-2, y+2), text, font=font, fill=stroke_fill)
    draw.text((x+2, y+2), text, font=font, fill=stroke_fill)
    draw.text((x, y), text, font=font, fill=fill)

# Draw texts
draw_text_centered("THE RICHEST MAN", height * 0.1, title_font, fill="#F0E6D2")
draw_text_centered("IN BABYLON", height * 0.18, title_font, fill="#F0E6D2")

draw_text_centered("By George S. Clason", height * 0.8, author_font, fill="white")
draw_text_centered("TKPROF LLC", height * 0.9, publisher_font, fill="#D3D3D3")

img.save(output_path)
print(f"Saved new cover to {output_path}")
