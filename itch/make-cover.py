"""Cover for itch.io (630 x 500): title type, the Luftwaffe's aerial photograph of Lamb Holm from its target
dossier of January 1941 (NARA, public domain) and a strip of the file of 16 April 1944.
Run from the repository root:  python itch/make-cover.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "itch" / "cover-630x500.png"
W, H = 630, 500
PAPER, INK, RED, GREY = (238, 235, 227), (31, 31, 28), (122, 43, 31), (93, 91, 85)


def font(names, size):
    for n in names:
        try:
            return ImageFont.truetype(n, size)
        except OSError:
            continue
    return ImageFont.load_default()


SERIF = ["C:/Windows/Fonts/pala.ttf", "C:/Windows/Fonts/georgia.ttf"]
SERIF_B = ["C:/Windows/Fonts/palab.ttf", "C:/Windows/Fonts/georgiab.ttf"]
SERIF_I = ["C:/Windows/Fonts/palai.ttf", "C:/Windows/Fonts/georgiai.ttf"]
MONO = ["C:/Windows/Fonts/consola.ttf", "C:/Windows/Fonts/cour.ttf"]


def main():
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    # the aerial photograph of the dossier (the photo area of the sheet)
    ph = Image.open(ROOT / "assets" / "plates" / "lambholm-photo.jpg").convert("L")
    ph = ph.crop((int(ph.width * 0.09), int(ph.height * 0.20), int(ph.width * 0.80), int(ph.height * 0.82)))
    ph = ImageOps.autocontrast(ImageOps.fit(ph, (270, 270)), cutoff=1)
    im.paste(Image.merge("RGB", (ph, ph, ph)), (W - 296, 104))
    d.rectangle([W - 296, 104, W - 27, 373], outline=INK)
    d.text((W - 161, 386), "Lamb Holm, Scapa Flow: German target dossier, 1941", font=font(SERIF_I, 12), fill=GREY, anchor="mm")
    # the file: 'bleibt Scapa Flow' as a strip
    strip = Image.open(ROOT / "assets" / "file" / "b3-remains.jpg").convert("L")
    strip = strip.crop((int(strip.width * 0.12), int(strip.height * 0.36), int(strip.width * 0.98), int(strip.height * 0.78)))
    strip = strip.resize((W, round(W * strip.height / strip.width)))
    strip = ImageOps.autocontrast(strip).point(lambda v: 150 + v * 105 // 255)
    sh = min(strip.height, 70)
    im.paste(Image.merge("RGB", (strip, strip, strip)).crop((0, 0, W, sh)), (0, H - sh - 40))
    d.rectangle([0, 0, W, 6], fill=RED)
    d.text((28, 40), "DRAGON'S LAIR", font=font(SERIF_B, 40), fill=INK)
    d.text((28, 88), "1944–45", font=font(SERIF_B, 30), fill=RED)
    d.text((28, 140), "A hypothetical campaign study", font=font(SERIF_I, 19), fill=INK)
    d.text((28, 166), "from the Luftwaffe's own file", font=font(SERIF_I, 19), fill=INK)
    d.text((28, 220), "The Mistel against", font=font(SERIF, 17), fill=GREY)
    d.text((28, 242), "the Home Fleet at Scapa Flow.", font=font(SERIF, 17), fill=GREY)
    d.text((28, 280), "Read the dossier,", font=font(SERIF, 17), fill=GREY)
    d.text((28, 302), "or take the staff's seat.", font=font(SERIF, 17), fill=GREY)
    d.rectangle([0, H - 40, W, H], fill=INK)
    d.text((W / 2, H - 20), "\u201e\u2026 bleibt Scapa Flow.\u201c  Luftwaffe Operations Staff, 16 April 1944",
           font=font(MONO, 14), fill=PAPER, anchor="mm")
    im.save(OUT)
    print(OUT.name, im.size)


if __name__ == "__main__":
    main()
