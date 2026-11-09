"""
make_cover.py
Typographic ebook covers (1600x2560) for Romeo and Juliet:
a crimson-to-night wash, a gold double frame and a faint act-and-scene watermark.
Writes cover_bilingual.jpg, cover_en.jpg and cover_ko.jpg next to this script,
where make_epub_native.py picks them up.

  python make_cover.py
"""

import os
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERIF = r"C:\Windows\Fonts\NotoSerifKR-VF.ttf"  # SIL Open Font License
W, H = 1600, 2560

BLUE = (112, 22, 36)
DEEP = (28, 8, 16)
PAPER = (243, 236, 220)
YELLOW = (214, 178, 96)


def font(size, weight="Bold"):
    f = ImageFont.truetype(SERIF, size)
    f.set_variation_by_name(weight)
    return f


def background():
    # vertical wash from crimson to night, with faint paper grain
    grad = Image.linear_gradient("L").resize((W, H))
    im = Image.composite(Image.new("RGB", (W, H), DEEP), Image.new("RGB", (W, H), BLUE), grad)
    rnd = random.Random(7)
    grain = Image.new("L", (W // 4, H // 4))
    grain.putdata([rnd.randint(0, 40) for _ in range(grain.width * grain.height)])
    grain = grain.resize((W, H)).filter(ImageFilter.GaussianBlur(1.2))
    im = Image.composite(Image.new("RGB", (W, H), PAPER), im, grain.point(lambda v: v // 6))
    d = ImageDraw.Draw(im)
    # double gold frame
    d.rectangle((70, 70, W - 70, H - 70), outline=YELLOW, width=4)
    d.rectangle((92, 92, W - 92, H - 92), outline=YELLOW, width=2)
    # faint act-and-scene marks as a watermark
    wm = font(64, "Regular")
    for i, line in enumerate(("Act I · Verona", "Act II · The Balcony", "Act III · Banished",
                              "Act IV · The Potion", "Act V · The Tomb")):
        d.text((190, 250 + i * 120), line, font=wm, fill=(132, 44, 56), anchor="ls")
    return im


def fitted(draw, text, size, weight="Black", max_width=W - 300):
    f = font(size, weight)
    while draw.textlength(text, font=f) > max_width:
        size -= 4
        f = font(size, weight)
    return f


def rule(draw, y, half=260):
    draw.line((W // 2 - half, y, W // 2 + half, y), fill=YELLOW, width=3)
    draw.ellipse((W // 2 - 9, y - 9, W // 2 + 9, y + 9), fill=YELLOW)


def centered(draw, y, text, f, fill=PAPER, spacing=0):
    if spacing:
        widths = [draw.textlength(c, font=f) for c in text]
        x = W / 2 - (sum(widths) + spacing * (len(text) - 1)) / 2
        for c, w in zip(text, widths):
            draw.text((x, y), c, font=f, fill=fill, anchor="ls")
            x += w + spacing
    else:
        draw.text((W / 2, y), text, font=f, fill=fill, anchor="ms")


def make(edition):
    im = background()
    d = ImageDraw.Draw(im)

    if edition == "ko":
        centered(d, 1300, "로미오와", font(220, "Black"), spacing=20)
        centered(d, 1540, "줄리엣", font(260, "Black"), spacing=30)
        rule(d, 1660)
        centered(d, 1790, "현대어 새 번역", font(70, "SemiBold"), fill=YELLOW, spacing=6)
        centered(d, 2080, "윌리엄 셰익스피어", font(66, "Medium"), spacing=4)
    elif edition == "en":
        centered(d, 1200, "ROMEO", font(230, "Black"), spacing=12)
        centered(d, 1330, "and", font(90, "Regular"))
        centered(d, 1520, "JULIET", font(230, "Black"), spacing=12)
        rule(d, 1650)
        centered(d, 1790, "A MODERN ENGLISH EDITION", font(54, "SemiBold"), fill=YELLOW, spacing=8)
        centered(d, 2080, "William Shakespeare", font(70, "Medium"), spacing=2)
    else:
        centered(d, 1120, "ROMEO", font(190, "Black"), spacing=10)
        centered(d, 1290, "AND JULIET", fitted(d, "AND JULIET", 170))
        centered(d, 1520, "로미오와 줄리엣", fitted(d, "로미오와 줄리엣", 150), spacing=6)
        rule(d, 1650)
        centered(d, 1770, "English–Korean Bilingual Edition", font(64, "Regular"))
        centered(d, 1860, "영한 대역판", font(64, "SemiBold"), fill=YELLOW, spacing=6)
        centered(d, 2080, "Shakespeare · 셰익스피어", font(68, "Medium"), spacing=4)

    centered(d, 2400, "TKPROF LLC", font(46, "Medium"), spacing=10)
    out = os.path.join(BASE_DIR, {"bi": "cover_bilingual.jpg", "en": "cover_en.jpg", "ko": "cover_ko.jpg"}[edition])
    im.save(out, quality=90, optimize=True)
    print(f"{edition}: {out} ({os.path.getsize(out):,} bytes)")


if __name__ == "__main__":
    for edition in ("bi", "en", "ko"):
        make(edition)
