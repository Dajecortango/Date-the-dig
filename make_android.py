"""Genera le immagini Android lette da RAPT nella cartella del progetto:
icona adattiva (volto di Caino nel medaglione oro) e presplash.

Uso: py -3 make_android.py
"""
import os

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
IMAGES = os.path.join(HERE, "game", "images", "malandrini")
FONTS = os.path.join(HERE, "game", "fonts")

ROSSO_SCURO = (74, 16, 16)
ROSSO_FONDO = (90, 21, 21)
ORO = (212, 175, 55)
ORO_CHIARO = (240, 199, 94)
NERO = (16, 12, 12)

# Icona adattiva Android: 432x432, il launcher ritaglia la forma (cerchio,
# squircle...) e mostra sicuro solo il cerchio centrale di 288 px.
ICONA = 432
SICURO = 288


def volto(sprite, lato, top_f=0.0, side_f=0.42, cx_f=0.52):
    """Testa ritagliata dallo sprite, come portrait() in make_gui.py."""
    spr = Image.open(os.path.join(IMAGES, sprite)).convert("RGBA")
    bb = spr.getbbox()
    bh = bb[3] - bb[1]
    side = int(bh * side_f)
    cx = bb[0] + int((bb[2] - bb[0]) * cx_f)
    top = bb[1] + int(bh * top_f)
    head = spr.crop((cx - side // 2, top, cx + side // 2, top + side))
    return head.resize((lato, lato), Image.LANCZOS)


def medaglione(lato):
    """Volto di Caino in un tondo nero con anello d'oro."""
    k = 4  # supersampling per bordi lisci
    L = lato * k
    img = Image.new("RGBA", (L, L), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    anello = int(L * 0.045)
    d.ellipse([0, 0, L - 1, L - 1], fill=ORO_CHIARO + (255,))
    d.ellipse([anello // 3, anello // 3, L - 1 - anello // 3, L - 1 - anello // 3], fill=ORO + (255,))
    d.ellipse([anello, anello, L - 1 - anello, L - 1 - anello], fill=NERO + (255,))

    dentro = L - 2 * anello
    head = volto("caino neutro.webp", dentro)
    mask = Image.new("L", (dentro, dentro), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, dentro - 1, dentro - 1], fill=255)
    img.paste(head, (anello, anello), ImageChops.multiply(mask, head.split()[3]))
    return img.resize((lato, lato), Image.LANCZOS)


def fondo(w, h):
    """Rosso cupo con alone caldo al centro, come il menu principale."""
    img = Image.new("RGB", (w, h), ROSSO_SCURO)
    alone = Image.new("L", (w, h), 0)
    r = int(min(w, h) * 0.42)
    ImageDraw.Draw(alone).ellipse([w // 2 - r, h // 2 - r, w // 2 + r, h // 2 + r], fill=255)
    alone = alone.filter(ImageFilter.GaussianBlur(min(w, h) * 0.18))
    return Image.composite(Image.new("RGB", (w, h), ROSSO_FONDO), img, alone)


def icona():
    fondo(ICONA, ICONA).save(os.path.join(HERE, "android-icon_background.png"))
    fg = Image.new("RGBA", (ICONA, ICONA), (0, 0, 0, 0))
    m = medaglione(SICURO)
    o = (ICONA - SICURO) // 2
    fg.alpha_composite(m, (o, o))
    fg.save(os.path.join(HERE, "android-icon_foreground.png"))


def presplash():
    """Mostrata mentre Android carica il gioco: medaglione e titolo."""
    W, H = 1920, 1080
    img = fondo(W, H).convert("RGBA")
    m = medaglione(420)
    img.alpha_composite(m, ((W - 420) // 2, 210))
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(os.path.join(FONTS, "Cinzel.ttf"), 76)
    titolo = "Date the Dignitas"
    tw = d.textlength(titolo, font=font)
    d.text(((W - tw) / 2 + 3, 703), titolo, font=font, fill=NERO + (200,))
    d.text(((W - tw) / 2, 700), titolo, font=font, fill=ORO_CHIARO + (255,))
    img.convert("RGB").save(os.path.join(HERE, "android-presplash.jpg"), quality=92)


if __name__ == "__main__":
    icona()
    presplash()
    print("generati android-icon_foreground.png, android-icon_background.png, android-presplash.jpg")
