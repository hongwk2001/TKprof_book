"""
create_cover_en.py
Builds the 2400x2400 audiobook cover for the ENGLISH-ONLY Dracula edition.

Reuses the existing high-resolution artwork but masks off the old bilingual
lettering (DRACULA / 드라큘라 / "English & Korean Bilingual Edition" at the top,
"Bram Stoker (브램 스토커) | TKPROF LLC" at the bottom) behind darkened panels,
then sets fresh English-only type.

Authors Republic requirements enforced here:
  * exactly 2400 x 2400 px, RGB JPEG
  * title / author / narrator must match metadata and the spoken opening credits
  * no promotional stickers, no physical-format references
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont, ImageFilter

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DIR = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(DIR, "cover_2400x2400.jpg")
OUT_JPG = os.path.join(DIR, "cover_en_2400.jpg")

SIZE = 2400
TITLE = "DRACULA"
SUBTITLE = "Bram Stoker's Gothic Classic"
AUTHOR = "BRAM STOKER"
NARRATOR_LINE = "Narrated by Aiden AI"
PUBLISHER = "TKPROF LLC"

FONTS = r"C:\Windows\Fonts"
F_TITLE = os.path.join(FONTS, "georgiab.ttf")
F_TEXT = os.path.join(FONTS, "georgia.ttf")
F_ITAL = os.path.join(FONTS, "georgiai.ttf")

BONE = (238, 232, 224)
DIM = (196, 186, 178)
CRIMSON = (150, 26, 30)


def font(path, size):
    return ImageFont.truetype(path, size)


def centered(draw, y, text, fnt, fill, shadow=True, track=0):
    """Draw horizontally-centred text, optionally letter-spaced."""
    if track:
        widths = [draw.textlength(c, font=fnt) + track for c in text]
        total = sum(widths) - track
        x = (SIZE - total) / 2
        for c, w in zip(text, widths):
            if shadow:
                draw.text((x + 4, y + 5), c, font=fnt, fill=(0, 0, 0, 210))
            draw.text((x, y), c, font=fnt, fill=fill)
            x += w
        return
    w = draw.textlength(text, font=fnt)
    x = (SIZE - w) / 2
    if shadow:
        draw.text((x + 4, y + 5), text, font=fnt, fill=(0, 0, 0))
    draw.text((x, y), text, font=fnt, fill=fill)


def vertical_scrim(img, top_solid, top_fade, bot_solid, bot_fade, strength=255):
    """
    Darken the bands that carry the old lettering.

    Fully opaque through the text zone, then feathered so the artwork
    re-emerges instead of ending on a hard line.
    """
    scrim = Image.new("L", (1, SIZE), 0)
    px = scrim.load()
    for y in range(SIZE):
        a = 0
        if y <= top_solid:
            a = strength
        elif y <= top_fade:
            t = (y - top_solid) / float(top_fade - top_solid)
            a = int(strength * (1.0 - t) ** 1.6)
        elif y >= bot_solid:
            a = strength
        elif y >= bot_fade:
            t = (y - bot_fade) / float(bot_solid - bot_fade)
            a = int(strength * t ** 1.6)
        px[0, y] = a
    mask = scrim.resize((SIZE, SIZE))
    dark = Image.new("RGB", (SIZE, SIZE), (6, 5, 7))
    return Image.composite(dark, img, mask)


def main():
    if not os.path.exists(SRC):
        raise FileNotFoundError(SRC)

    img = Image.open(SRC).convert("RGB")
    if img.size != (SIZE, SIZE):
        img = img.resize((SIZE, SIZE), Image.Resampling.LANCZOS)

    # Old top block runs to ~y=620; old bottom block ~y=2020..2140.
    img = vertical_scrim(img, top_solid=690, top_fade=1000,
                         bot_solid=2010, bot_fade=1760)

    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=55, threshold=3))
    draw = ImageDraw.Draw(img)

    # --- frame -------------------------------------------------------------
    draw.rectangle([54, 54, SIZE - 55, SIZE - 55], outline=CRIMSON, width=7)
    draw.rectangle([86, 86, SIZE - 87, SIZE - 87], outline=(92, 78, 62), width=3)

    # --- title -------------------------------------------------------------
    centered(draw, 196, TITLE, font(F_TITLE, 300), BONE, track=16)

    draw.line([(SIZE * 0.30, 560), (SIZE * 0.70, 560)], fill=CRIMSON, width=5)
    centered(draw, 606, SUBTITLE, font(F_ITAL, 92), DIM)

    # --- author / narrator -------------------------------------------------
    centered(draw, 1946, AUTHOR, font(F_TEXT, 118), BONE, track=10)
    draw.line([(SIZE * 0.36, 2116), (SIZE * 0.64, 2116)], fill=(92, 78, 62), width=3)
    centered(draw, 2150, NARRATOR_LINE, font(F_ITAL, 84), DIM)
    centered(draw, 2268, PUBLISHER, font(F_TEXT, 58), (150, 142, 136))

    img.save(OUT_JPG, "JPEG", quality=94, subsampling=0, optimize=True)
    chk = Image.open(OUT_JPG)
    print(f"[done] {OUT_JPG}")
    print(f"       {chk.size[0]}x{chk.size[1]} {chk.mode}, "
          f"{os.path.getsize(OUT_JPG)/1024/1024:.2f} MB")


if __name__ == "__main__":
    main()
