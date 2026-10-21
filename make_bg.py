"""Prepara gli sfondi di Date the Dignitas: resize/crop a 1920x1080 + color
grading unificato (dominante calda, leggero contrasto, vignetta scura) per
legare sfondi AI di batch diversi alla palette rosso-oro-nero.

Uso:
  py -3 make_bg.py <cartella_sorgenti>     installa i sorgenti in game/images
  py -3 make_bg.py --grade-only <file>...  gradua in place file gia' installati
  py -3 make_bg.py --nero                  rigenera solo "bg nero.png"

ATTENZIONE: il grading va applicato UNA sola volta, sui sorgenti originali.
Riapplicarlo a file gia' graduati somma l'effetto.
"""
import os
import re
import sys
from PIL import Image, ImageDraw, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
IMAGES = os.path.join(HERE, "game", "images")
W, H = 1920, 1080

# Sorgenti con nomi che la normalizzazione generica non copre.
MAP = {
    "bg arena": "bg arena_athlion.png",
}


def canon(filename):
    """'BG esterno neve_.jpg' -> 'bg esterno_neve.png' (nome Ren'Py canonico)."""
    stem = os.path.splitext(filename)[0]
    stem = re.sub(r"(?i)^bg[ _]*", "", stem).replace("_", " ").strip()
    key = "bg " + " ".join(stem.lower().split())
    if key in MAP:
        return MAP[key]
    return "bg " + "_".join(stem.lower().split()) + ".png"


def cover(im):
    """Resize + crop centrale a 1920x1080."""
    w, h = im.size
    scale = max(W / w, H / h)
    im = im.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
    left = (im.width - W) // 2
    top = (im.height - H) // 2
    return im.crop((left, top, left + W, top + H))


def vignette_mask(max_alpha):
    """Maschera radiale: 0 al centro, max_alpha agli angoli."""
    small = Image.new("L", (96, 54), 0)
    d = ImageDraw.Draw(small)
    cx, cy = 47.5, 26.5
    maxd = (cx ** 2 + cy ** 2) ** 0.5
    for y in range(54):
        for x in range(96):
            dist = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5 / maxd
            d.point((x, y), fill=int(max_alpha * dist ** 2.2))
    return small.resize((W, H), Image.BICUBIC)


def grade(im):
    """Dominante calda + contrasto + vignetta rosso-nera."""
    r, g, b = im.convert("RGB").split()
    r = r.point(lambda v: min(255, int(v * 1.05)))
    b = b.point(lambda v: int(v * 0.93))
    im = Image.merge("RGB", (r, g, b))
    im = ImageEnhance.Contrast(im).enhance(1.05)
    dark = Image.new("RGB", (W, H), (26, 8, 8))
    return Image.composite(dark, im, vignette_mask(80))


def make_nero():
    """'bg nero': nero con cuore caldo rosso-brace al centro, molto tenue."""
    base = Image.new("RGB", (W, H), (24, 10, 9))
    dark = Image.new("RGB", (W, H), (8, 6, 6))
    img = Image.composite(dark, base, vignette_mask(255))
    out = os.path.join(IMAGES, "bg nero.png")
    img.save(out, optimize=True)
    print("rigenerato", out)


def install(src_dir):
    for f in sorted(os.listdir(src_dir)):
        if not f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            continue
        im = Image.open(os.path.join(src_dir, f))
        out = os.path.join(IMAGES, canon(f))
        grade(cover(im)).save(out, optimize=True)
        print(f, "->", out)


def grade_only(paths):
    for p in paths:
        im = Image.open(p)
        if im.size != (W, H):
            im = cover(im)
        grade(im).save(p, optimize=True)
        print("graduato in place:", p)


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__)
    elif args[0] == "--nero":
        make_nero()
    elif args[0] == "--grade-only":
        grade_only(args[1:])
    else:
        install(args[0])
