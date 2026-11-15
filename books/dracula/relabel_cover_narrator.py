"""
Re-letter the narrator credit on the Dracula audiobook cover.

The 2026-09-15 recast changed the credit from "Aiden AI" to "Fable AI and
Bella AI", but the artwork still reads the old name. Authors Republic requires
the narrator to match exactly across cover art, metadata and the credits
tracks, so the cover blocks submission until it agrees.

The source artwork is gone (it lived outside the repo), so this edits the
finished 2400x2400 JPEG in place. That is safe here only because the credit
sits on a uniform near-black field: measured background [6,6,8], text
[196,186,177], line occupying rows 2164-2228 with "TKPROF LLC" clear below at
2237. Nothing else is touched.

Usage:  venv/Scripts/python.exe books/dracula/relabel_cover_narrator.py
Writes: cover_en_2400_v2.jpg  (original left untouched)
"""
import os

from PIL import Image, ImageDraw, ImageFont

DIR = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(DIR, "cover_en_2400.jpg")
OUT = os.path.join(DIR, "cover_en_2400_v2.jpg")

TEXT = "Narrated by Fable AI and Bella AI"
FONT = r"C:\Windows\Fonts\georgiai.ttf"      # italic serif, matches the plate

BG = (6, 6, 8)                 # measured, uniform across the band
FG = (196, 186, 177)           # measured from the existing credit

# Measured row by row against the background:
#   2215-2228  narrator line body
#   2229-2245  the italic "y" descender from "by"
#   2246-2281  clean gap
#   2282-2321  TKPROF LLC (cols 1025-1373)
# A first attempt cleared only to 2233 and left the descender visible as a
# smudge. Clearing to 2250 removes it and still stops 32 rows short of
# TKPROF LLC.
BAND_TOP, BAND_BOTTOM = 2150, 2250
BASELINE_BOTTOM = 2228         # bottom of the old line's body, ignoring descender
CENTER_X = 1200                # image is 2400 wide


def main():
    im = Image.open(SRC).convert("RGB")
    assert im.size == (2400, 2400), f"unexpected size {im.size}"
    d = ImageDraw.Draw(im)

    # wipe the old credit
    d.rectangle([0, BAND_TOP, im.width, BAND_BOTTOM], fill=BG)

    # size the font so the longer name still fits inside the frame
    max_w = 1900
    size = 92
    while size > 40:
        f = ImageFont.truetype(FONT, size)
        box = d.textbbox((0, 0), TEXT, font=f)
        if (box[2] - box[0]) <= max_w:
            break
        size -= 2

    f = ImageFont.truetype(FONT, size)
    box = d.textbbox((0, 0), TEXT, font=f)
    w, h = box[2] - box[0], box[3] - box[1]
    x = CENTER_X - w // 2 - box[0]
    y = BASELINE_BOTTOM - h - box[1]

    # soft shadow, as on the rest of the plate
    d.text((x + 3, y + 3), TEXT, font=f, fill=(0, 0, 0))
    d.text((x, y), TEXT, font=f, fill=FG)

    im.save(OUT, "JPEG", quality=95, subsampling=0)
    mb = os.path.getsize(OUT) / 1048576
    print(f"[ok] {os.path.basename(OUT)}  {im.size[0]}x{im.size[1]}  "
          f"{mb:.2f} MB  font {size}px  text width {w}px")
    print(f"     \"{TEXT}\"")


if __name__ == "__main__":
    main()
