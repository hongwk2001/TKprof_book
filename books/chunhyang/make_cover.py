"""
make_cover.py
Typographic ebook covers (1600x2560) over the opening woodblock page (leaf 1a,
scans/90001.jpg, National Museum of Korea 신수15187, KOGL Type 1).
Writes cover_bilingual.jpg, cover_en.jpg, cover_ko.jpg and source_page_1a.jpg
next to this script, where make_epub_native.py picks them up.

  python make_cover.py
"""

import os

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCAN = os.path.join(BASE_DIR, "scans", "90001.jpg")
LEAF_1A = (470, 330, 1530, 1925)  # left page of the spread, at the scan's 3000x2250 size
SERIF = r"C:\Windows\Fonts\NotoSerifKR-VF.ttf"  # SIL Open Font License
W, H = 1600, 2560

INK = (20, 22, 31)
PAPER = (243, 233, 210)
SEAL = (168, 32, 38)


def font(size, weight="Bold"):
    f = ImageFont.truetype(SERIF, size)
    f.set_variation_by_name(weight)
    return f


def background():
    im = Image.open(SCAN).crop(LEAF_1A)
    scale = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    left = (im.width - W) // 2
    im = im.crop((left, 0, left + W, H)).convert("RGB")
    im = ImageEnhance.Color(im).enhance(0.75)
    im = ImageEnhance.Brightness(im).enhance(0.8)
    # ink wash from about a third of the way down, solid at the bottom
    shade = Image.new("L", (1, H))
    for y in range(H):
        t = min(max((y - H * 0.30) / (H * 0.30), 0), 1)
        shade.putpixel((0, y), round(235 * t ** 1.3))
    shade = shade.resize((W, H))
    im = Image.composite(Image.new("RGB", (W, H), INK), im, shade)
    # soft dark edge at the top so the seal reads
    top = Image.linear_gradient("L").rotate(180).resize((W, 260)).point(lambda v: v * 0.55)
    im.paste(Image.new("RGB", (W, 260), INK), (0, 0), top)
    return im.filter(ImageFilter.GaussianBlur(0.6))


def fitted(draw, text, size, weight="Black", max_width=W - 240):
    f = font(size, weight)
    while draw.textlength(text, font=f) > max_width:
        size -= 4
        f = font(size, weight)
    return f


def seal(draw, cx, cy, size=210):
    r = size // 2
    draw.rounded_rectangle((cx - r, cy - r, cx + r, cy + r), radius=26, fill=SEAL)
    draw.rounded_rectangle((cx - r + 14, cy - r + 14, cx + r - 14, cy + r - 14), radius=16,
                           outline=PAPER, width=5)
    f = font(78, "Black")
    draw.text((cx, cy - 40), "春", font=f, fill=PAPER, anchor="mm")
    draw.text((cx, cy + 44), "香", font=f, fill=PAPER, anchor="mm")


def rule(draw, y, half=260):
    draw.line((W // 2 - half, y, W // 2 + half, y), fill=PAPER, width=3)


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
    seal(d, W - 230, 230)

    if edition == "ko":
        centered(d, 1640, "춘향전", font(330, "Black"), spacing=30)
        rule(d, 1740)
        centered(d, 1850, "열녀춘향수절가", font(70, "SemiBold"), spacing=10)
        centered(d, 1940, "완판 84장본 현대어 옮김", font(58, "Regular"))
        centered(d, 2120, "13세 이상 독자를 위한 현대어 재화", font(48, "Regular"))
    elif edition == "en":
        centered(d, 1450, "THE TALE OF", font(76, "SemiBold"), spacing=14)
        centered(d, 1660, "CHUNHYANG", fitted(d, "CHUNHYANG", 230))
        rule(d, 1780)
        centered(d, 1890, "Korea's Great Love Story,", font(70, "Regular"))
        centered(d, 1980, "Retold in Simple English", font(70, "Regular"))
        centered(d, 2140, "From the 1911 woodblock edition", font(48, "Regular"))
    else:
        centered(d, 1400, "THE TALE OF", font(70, "SemiBold"), spacing=14)
        centered(d, 1600, "CHUNHYANG", fitted(d, "CHUNHYANG", 220))
        centered(d, 1850, "춘향전", font(190, "Black"), spacing=20)
        rule(d, 1920)
        centered(d, 2030, "English–Korean Bilingual Edition", font(64, "Regular"))
        centered(d, 2115, "영한 대역판", font(64, "SemiBold"), spacing=6)

    centered(d, 2420, "TKPROF LLC", font(46, "Medium"), spacing=10)
    out = os.path.join(BASE_DIR, {"bi": "cover_bilingual.jpg", "en": "cover_en.jpg", "ko": "cover_ko.jpg"}[edition])
    im.save(out, quality=90, optimize=True)
    print(f"{edition}: {out} ({os.path.getsize(out):,} bytes)")


def make_source_page():
    """The leaf-1a image make_epub_native.py puts in "About the Source"."""
    im = Image.open(SCAN).crop(LEAF_1A)
    im = im.resize((round(im.width * 1200 / im.height), 1200), Image.LANCZOS)
    out = os.path.join(BASE_DIR, "source_page_1a.jpg")
    im.save(out, quality=80, optimize=True)
    print(f"source page: {out} ({os.path.getsize(out):,} bytes)")


if __name__ == "__main__":
    make_source_page()
    for edition in ("bi", "en", "ko"):
        make(edition)
