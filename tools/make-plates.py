"""Plates: resize the downloaded originals (tools/plates_src/, see fetch-plates.py) and the range map of
the file (assets/file/map3.jpg) into assets/plates/<id>.jpg (1600 px) and <id>_t.jpg (640 px).
Run from the repository root:  python tools/make-plates.py"""
from pathlib import Path
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "tools" / "plates_src"
OUT = ROOT / "assets" / "plates"
# id, source file, crop (fractions) or None
PLATES = [
    ("rangemap", ROOT / "assets/file/map3.jpg", None),
    ("lambholm-photo", SRC / "lambholm2.jpg", None),
    ("lambholm-map", SRC / "lambholm1.jpg", None),
    ("lyness", SRC / "scapasw2.jpg", None),
    ("chart35", SRC / "chart35.jpg", None),
    ("boom", SRC / "boom.jpg", None),
    ("wasp", SRC / "wasp.jpg", None),
    ("royaloak", SRC / "royaloak.jpg", None),
    ("blockship", SRC / "blockship.jpg", None),
    ("barrier", SRC / "barrier.jpg", None),
    ("chapel", SRC / "chapel.jpg", None),
]
OUT.mkdir(parents=True, exist_ok=True)
for pid, src, crop in PLATES:
    im = Image.open(src).convert("RGB")
    if crop:
        w, h = im.size; im = im.crop((int(w * crop[0]), int(h * crop[1]), int(w * crop[2]), int(h * crop[3])))
    big = im.copy(); big.thumbnail((1600, 1600), Image.LANCZOS); big.save(OUT / f"{pid}.jpg", quality=84)
    t = im.copy(); t.thumbnail((640, 640), Image.LANCZOS); t.save(OUT / f"{pid}_t.jpg", quality=82)
    print(pid, big.size)
