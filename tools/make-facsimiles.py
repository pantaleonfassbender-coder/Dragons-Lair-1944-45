"""Facsimiles of the Dragon's Lair documents.

- NARA RG 242, microfilm T-321 (Records of Headquarters, German Air Force High Command), roll 10
  (https://catalog.archives.gov/id/315968627): the Mistel study of 16 April 1944 (images 282-298) and the
  war diary of the operations staff, February 1945 (images 368, 418, 419, 425, 441). Positive prints.
- NARA RG 498, CSDIC (WEA) Final Report 30 on Maj Horst Hans Beeger, 21 January 1946
  (https://catalog.archives.gov/id/295816244, images 3-6).

Writes assets/file/<id>.jpg (pages, 1300 px wide) and the plate of the range map.
Downloads the TIFFs (20-48 MB each) into tools/src/ once.
Run from the repository root:  python tools/make-facsimiles.py
"""
import urllib.request
from pathlib import Path
import numpy as np
from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = None
ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "tools" / "src"
OUT = ROOT / "assets" / "file"
T321 = "https://catalog.archives.gov/medialz/dc-metro/rg-242/7788651/T321/T321-0010/T321-0010-{:05d}.tif"
CSDIC = "https://catalog.archives.gov/medialz/dc-metro/rg-498/5709637/5709637-1229-03/5709637-1229-03-{:04d}.tif"

# id, source ('t' T-321 image / 'c' CSDIC image), number
PAGES = [
    ("a1", "t", 282), ("a2", "t", 283), ("a3", "t", 284),
    ("b1", "t", 285), ("b2", "t", 286), ("b3", "t", 287),
    ("c1", "t", 288), ("c2", "t", 289), ("c3", "t", 290), ("c4", "t", 291),
    ("d1", "t", 293),
    ("k1", "t", 368), ("k2", "t", 418), ("k3", "t", 419), ("k4", "t", 425), ("k5", "t", 441),
    ("v1", "c", 4), ("v2", "c", 5),
]
MAPS = [("map3", 298)]
# detail passages: page id, name, crop as fractions of the PAGE image
DETAILS = [
    ("a3", "most", (0.0, 0.08, 1.0, 0.47)),
    ("a3", "proposal", (0.0, 0.50, 1.0, 0.80)),
    ("b2", "scapa", (0.0, 0.47, 1.0, 0.80)),
    ("b3", "remains", (0.0, 0.70, 1.0, 0.98)),
    ("c2", "attack", (0.0, 0.47, 1.0, 0.96)),
    ("k2", "drachen", (0.0, 0.60, 1.0, 0.93)),
    ("k5", "abandon", (0.0, 0.0, 1.0, 0.42)),
    ("v2", "beeger", (0.0, 0.36, 1.0, 0.56)),
]


def frame(kind, n):
    name = f"T321-0010-{n:05d}.tif" if kind == "t" else f"5709637-1229-03-{n:04d}.tif"
    p = SRC / name
    if not p.exists():
        SRC.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve((T321 if kind == "t" else CSDIC).format(n), p)
    return Image.open(p).convert("L")


def paper(im, kind):
    """Crop to the sheet: below the frame counter, inside the light area."""
    small = np.asarray(im.resize((im.width // 8, im.height // 8)))
    h = small.shape[0]
    top = int(h * (0.20 if kind == "t" else 0.13))
    band = small[top:]
    rows = np.where((band > 150).mean(axis=1) > 0.45)[0]
    cols = np.where((band > 150).mean(axis=0) > 0.45)[0]
    y0, y1 = (rows.min() + top) * 8, (rows.max() + top) * 8
    x0, x1 = cols.min() * 8, cols.max() * 8
    return im.crop((x0, y0, x1, y1))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for pid, kind, n in PAGES:
        im = paper(frame(kind, n), kind)
        im = ImageOps.autocontrast(im, cutoff=0.5)
        im = im.resize((1300, int(im.height * 1300 / im.width)), Image.LANCZOS)
        im.save(OUT / f"{pid}.jpg", quality=84)
        print(pid, im.size)
    for pid, n in MAPS:
        im = ImageOps.autocontrast(frame("t", n), cutoff=0.5)
        if pid == "map2":
            # the printed map carries the Reich eagle with a swastika in its top-left corner: masked
            w, h = im.size
            from PIL import ImageDraw
            ImageDraw.Draw(im).rectangle((0, 0, int(w * 0.16), int(h * 0.11)), fill=235)
        im = im.resize((2000, int(im.height * 2000 / im.width)), Image.LANCZOS)
        im.save(OUT / f"{pid}.jpg", quality=82)
        print(pid, im.size)
    for pid, name, (x0, y0, x1, y1) in DETAILS:
        im = Image.open(OUT / f"{pid}.jpg")
        w, h = im.size
        im.crop((int(w * x0), int(h * y0), int(w * x1), int(h * y1))).save(OUT / f"{pid}-{name}.jpg", quality=86)
        print(pid, name)


if __name__ == "__main__":
    main()
