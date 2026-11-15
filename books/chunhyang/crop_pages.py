"""Crop each scanned spread into its two printed pages for transcription.

Each museum image is an open spread: the right page is the back (b) of one
leaf, the left page the front (a) of the next. Crops go to crops/ (git-ignored).
    python crop_pages.py 90002 90010
"""
import pathlib
import sys

from PIL import Image

HERE = pathlib.Path(__file__).parent
RIGHT = (1430, 480, 2560, 1920)  # x0, y0, x1, y1 at the scans' 3000x2250 size
LEFT = (380, 480, 1570, 1920)


def main(first, last):
    out = HERE / "crops"
    out.mkdir(exist_ok=True)
    for n in range(first, last + 1):
        im = Image.open(HERE / "scans" / f"{n}.jpg")
        for side, box in (("R", RIGHT), ("L", LEFT)):
            im.crop(box).save(out / f"{n}{side}.jpg", quality=92)


if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2] if len(sys.argv) > 2 else sys.argv[1]))
