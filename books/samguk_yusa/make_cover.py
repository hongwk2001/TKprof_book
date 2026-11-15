"""
make_cover.py
Typographic ebook covers (1600x2560) on the app's 단청 green (#1B4D3E), with a
三國遺事 seal. Writes cover_bilingual.jpg, cover_en.jpg and cover_ko.jpg next to
this script, where make_epub_native.py picks them up.

  python make_cover.py
"""

import os
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERIF = r"C:\Windows\Fonts\NotoSerifKR-VF.ttf"  # SIL Open Font License
W, H = 1600, 2560

GREEN = (27, 77, 62)
DEEP = (12, 36, 29)
PAPER = (243, 233, 210)
GOLD = (201, 168, 92)
SEAL = (168, 32, 38)


def font(size, weight="Bold"):
    f = ImageFont.truetype(SERIF, size)
    f.set_variation_by_name(weight)
    return f


def background():
    # vertical wash from 단청 green to deep green, with faint paper grain
    grad = Image.linear_gradient("L").resize((W, H))
    im = Image.composite(Image.new("RGB", (W, H), DEEP), Image.new("RGB", (W, H), GREEN), grad)
    rnd = random.Random(7)
    grain = Image.new("L", (W // 4, H // 4))
    grain.putdata([rnd.randint(0, 40) for _ in range(grain.width * grain.height)])
    grain = grain.resize((W, H)).filter(ImageFilter.GaussianBlur(1.2))
    im = Image.composite(Image.new("RGB", (W, H), PAPER), im, grain.point(lambda v: v // 6))
    d = ImageDraw.Draw(im)
    # double gold frame
    d.rectangle((70, 70, W - 70, H - 70), outline=GOLD, width=4)
    d.rectangle((92, 92, W - 92, H - 92), outline=GOLD, width=2)
    # faint large hanja title as a watermark down the right side
    wm = font(210, "Black")
    for i, c in enumerate("三國遺事"):  # stops above the highest title line (y≈1100)
        d.text((W - 290, 250 + i * 240), c, font=wm, fill=(40, 96, 79), anchor="mm")
    return im


def fitted(draw, text, size, weight="Black", max_width=W - 300):
    f = font(size, weight)
    while draw.textlength(text, font=f) > max_width:
        size -= 4
        f = font(size, weight)
    return f


def seal(draw, cx, cy, size=230):
    r = size // 2
    draw.rounded_rectangle((cx - r, cy - r, cx + r, cy + r), radius=26, fill=SEAL)
    draw.rounded_rectangle((cx - r + 14, cy - r + 14, cx + r - 14, cy + r - 14), radius=16,
                           outline=PAPER, width=5)
    f = font(74, "Black")
    for (dx, dy), c in zip(((40, -42), (40, 44), (-40, -42), (-40, 44)), "三國遺事"):
        draw.text((cx + dx, cy + dy), c, font=f, fill=PAPER, anchor="mm")


def rule(draw, y, half=260):
    draw.line((W // 2 - half, y, W // 2 + half, y), fill=GOLD, width=3)


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
    seal(d, 290, 290)

    if edition == "ko":
        centered(d, 1500, "삼국유사", font(300, "Black"), spacing=24)
        rule(d, 1610)
        centered(d, 1730, "기이편 · 권1–2", font(76, "SemiBold"), spacing=6)
        centered(d, 1830, "현대어 옮김", font(64, "Regular"))
        centered(d, 2060, "일연 지음", font(64, "Medium"), spacing=6)
    elif edition == "en":
        centered(d, 1380, "SAMGUK YUSA", fitted(d, "SAMGUK YUSA", 200))
        rule(d, 1500)
        centered(d, 1620, "Memorabilia of the", font(76, "Regular"))
        centered(d, 1720, "Three Kingdoms", font(76, "Regular"))
        centered(d, 1860, "THE BOOK OF MARVELS", font(56, "SemiBold"), fill=GOLD, spacing=8)
        centered(d, 2080, "Iryeon", font(70, "Medium"), spacing=6)
    else:
        centered(d, 1280, "SAMGUK YUSA", fitted(d, "SAMGUK YUSA", 180))
        centered(d, 1540, "삼국유사", font(210, "Black"), spacing=18)
        rule(d, 1640)
        centered(d, 1760, "English–Korean Bilingual Edition", font(64, "Regular"))
        centered(d, 1850, "영한 대역판", font(64, "SemiBold"), spacing=6)
        centered(d, 2080, "Iryeon · 일연", font(64, "Medium"), spacing=4)

    centered(d, 2400, "TKPROF LLC", font(46, "Medium"), spacing=10)
    out = os.path.join(BASE_DIR, {"bi": "cover_bilingual.jpg", "en": "cover_en.jpg", "ko": "cover_ko.jpg"}[edition])
    im.save(out, quality=90, optimize=True)
    print(f"{edition}: {out} ({os.path.getsize(out):,} bytes)")


if __name__ == "__main__":
    for edition in ("bi", "en", "ko"):
        make(edition)
