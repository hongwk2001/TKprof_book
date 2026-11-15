"""
make_cover.py
Ebook covers (1600x2560) for The Heroes: a wine-red ground with a gold double frame
and Greek-key bands, the coloured Perseus-and-Andromeda illustration from the app in a
gold-edged panel, and the title beneath it.
Writes cover_bilingual.jpg, cover_en.jpg and cover_ko.jpg next to this script,
where make_epub_native.py picks them up.

  python make_cover.py
"""

import os
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ART = r"C:\git_repo\Book_apps\the_heroes\src\main\assets\images\02_perseus_and_andromeda_color.jpg"
SERIF = r"C:\Windows\Fonts\NotoSerifKR-VF.ttf"  # SIL Open Font License
W, H = 1600, 2560

WINE = (92, 22, 30)
DEEP = (40, 8, 14)
PAPER = (246, 238, 220)
GOLD = (214, 172, 88)


def font(size, weight="Bold"):
    f = ImageFont.truetype(SERIF, size)
    f.set_variation_by_name(weight)
    return f


def meander(draw, x0, x1, y, unit=36):
    """A Greek-key band between x0 and x1, `unit` px tall, top edge at y."""
    u = unit / 4
    x = x0
    while x + unit <= x1:
        pts = [(x, y + 4 * u), (x, y), (x + 3 * u, y), (x + 3 * u, y + 3 * u), (x + u, y + 3 * u),
               (x + u, y + u), (x + 2 * u, y + u), (x + 2 * u, y + 2 * u)]
        draw.line(pts, fill=GOLD, width=4, joint="curve")
        draw.line([(x, y + 4 * u), (x + unit, y + 4 * u)], fill=GOLD, width=4)
        x += unit
    draw.line([(x0, y - 10), (x, y - 10)], fill=GOLD, width=3)


def background():
    grad = Image.linear_gradient("L").resize((W, H))
    im = Image.composite(Image.new("RGB", (W, H), DEEP), Image.new("RGB", (W, H), WINE), grad)
    rnd = random.Random(11)
    grain = Image.new("L", (W // 4, H // 4))
    grain.putdata([rnd.randint(0, 40) for _ in range(grain.width * grain.height)])
    grain = grain.resize((W, H)).filter(ImageFilter.GaussianBlur(1.2))
    im = Image.composite(Image.new("RGB", (W, H), PAPER), im, grain.point(lambda v: v // 7))
    d = ImageDraw.Draw(im)
    d.rectangle((60, 60, W - 60, H - 60), outline=GOLD, width=4)
    d.rectangle((82, 82, W - 82, H - 82), outline=GOLD, width=2)
    meander(d, 130, W - 130, 128)
    meander(d, 130, W - 130, H - 170)
    return im


def place_art(im, top=250, width=920):
    art = Image.open(ART).convert("RGB")
    art = art.resize((width, round(art.height * width / art.width)), Image.LANCZOS)
    x = (W - width) // 2
    d = ImageDraw.Draw(im)
    d.rectangle((x - 22, top - 22, x + width + 21, top + art.height + 21), fill=DEEP, outline=GOLD, width=3)
    d.rectangle((x - 8, top - 8, x + width + 7, top + art.height + 7), outline=GOLD, width=2)
    im.paste(art, (x, top))
    return top + art.height + 22


def fitted(draw, text, size, weight="Black", max_width=W - 300):
    f = font(size, weight)
    while draw.textlength(text, font=f) > max_width:
        size -= 4
        f = font(size, weight)
    return f


def rule(draw, y, half=240):
    draw.line((W // 2 - half, y, W // 2 + half, y), fill=GOLD, width=3)
    draw.polygon([(W // 2, y - 12), (W // 2 + 12, y), (W // 2, y + 12), (W // 2 - 12, y)], fill=GOLD)


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
    y = place_art(im)  # art bottom edge, about 1510
    d = ImageDraw.Draw(im)

    if edition == "ko":
        centered(d, y + 230, "그리스 영웅 이야기", fitted(d, "그리스 영웅 이야기", 160), spacing=6)
        rule(d, y + 330)
        centered(d, y + 450, "페르세우스 · 아르고 원정대 · 테세우스", fitted(d, "페르세우스 · 아르고 원정대 · 테세우스", 58, "SemiBold"), fill=GOLD)
        centered(d, y + 560, "현대어 새 번역", font(56, "Medium"), spacing=6)
        centered(d, y + 700, "찰스 킹즐리", font(66, "Medium"), spacing=6)
    elif edition == "en":
        centered(d, y + 240, "THE HEROES", fitted(d, "THE HEROES", 210), spacing=12)
        rule(d, y + 340)
        centered(d, y + 460, "GREEK FAIRY TALES", font(64, "SemiBold"), fill=GOLD, spacing=10)
        centered(d, y + 560, "A Modern English Edition", font(56, "Regular"))
        centered(d, y + 700, "Charles Kingsley", font(70, "Medium"), spacing=2)
    else:
        centered(d, y + 200, "THE HEROES", fitted(d, "THE HEROES", 170), spacing=10)
        centered(d, y + 350, "그리스 영웅 이야기", fitted(d, "그리스 영웅 이야기", 110), spacing=6)
        rule(d, y + 430)
        centered(d, y + 540, "English–Korean Bilingual Edition", font(58, "Regular"))
        centered(d, y + 625, "영한 대역판", font(58, "SemiBold"), fill=GOLD, spacing=6)
        centered(d, y + 740, "Kingsley · 킹즐리", font(64, "Medium"), spacing=4)

    centered(d, H - 215, "TKPROF LLC", font(42, "Medium"), spacing=10)
    out = os.path.join(BASE_DIR, {"bi": "cover_bilingual.jpg", "en": "cover_en.jpg", "ko": "cover_ko.jpg"}[edition])
    im.save(out, quality=90, optimize=True)
    print(f"{edition}: {out} ({os.path.getsize(out):,} bytes)")


if __name__ == "__main__":
    for edition in ("bi", "en", "ko"):
        make(edition)
