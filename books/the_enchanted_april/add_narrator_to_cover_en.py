"""
Add the narrator credit to the English audiobook cover.

authors_republic_requirements.md:76 requires Title, Subtitle and Narrator to
match exactly across metadata, cover art and the opening/closing tracks.
cover_en_2400.jpg carries no narrator line at all -- its bottom block reads
"By Elizabeth von Arnim | TKPROF LLC", where TKPROF LLC is the publisher --
while metadata.md and both credits tracks now say TKPROF AI.

The line goes ABOVE the author block, not below it. Scanning the bottom of the
existing cover for bright pixels puts the author text at y 2160-2240 and the
inner frame rule at y~2300, leaving 50 px of clearance underneath -- not enough
for a legible second line. The band at y 2020-2150 is inside the existing dark
gradient and carries no text, so white type reads cleanly there.

The source artwork this cover was composited from is not in the repo, so this
edits the finished JPEG rather than regenerating it. cover_en_2400.jpg is left
untouched; the result is a new file.

Usage:
    ../../venv/Scripts/python.exe add_narrator_to_cover_en.py
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DIR = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(DIR, "cover_en_2400.jpg")
OUT = os.path.join(DIR, "cover_en_audio_2400.jpg")

NARRATOR = "Narrated by TKPROF AI"
BASELINE_Y = 1995          # ~120 px clear of the author block at y 2160;
                           # 2090 was tried first and sat 18 px off it
FONT_SIZE = 58             # subordinate to the ~80 px author line
FONTS = ["C:/Windows/Fonts/georgiab.ttf", "C:/Windows/Fonts/georgia.ttf"]


def main():
    im = Image.open(SRC).convert("RGB")
    w, _ = im.size
    draw = ImageDraw.Draw(im)

    font = None
    for fp in FONTS:
        if os.path.exists(fp):
            font = ImageFont.truetype(fp, FONT_SIZE)
            break
    if font is None:
        print("Georgia not found; falling back to the default bitmap font")
        font = ImageFont.load_default()

    box = draw.textbbox((0, 0), NARRATOR, font=font)
    tw = box[2] - box[0]
    x = (w - tw) // 2

    # The band sits over sunlit stone, not the dark gradient, so a single
    # offset shadow is not enough to hold white type. Ring the glyphs with
    # shadow on all sides to build a halo, then lay the text over it.
    for dx, dy in ((-3, 0), (3, 0), (0, -3), (0, 3),
                   (-2, -2), (2, -2), (-2, 2), (2, 2), (4, 4)):
        draw.text((x + dx, BASELINE_Y + dy), NARRATOR, font=font,
                  fill=(15, 23, 42))
    draw.text((x, BASELINE_Y), NARRATOR, font=font, fill=(255, 255, 255))

    im.save(OUT, "JPEG", quality=95, subsampling=0)
    print(f"wrote {os.path.basename(OUT)}  {im.size[0]}x{im.size[1]}  "
          f"{os.path.getsize(OUT) / 1048576:.2f} MB")
    print(f"text width {tw}px centred at x={x}, baseline y={BASELINE_Y}")
    print(f"colour mode {im.mode} (AR requires RGB, not CMYK)")


if __name__ == "__main__":
    main()
