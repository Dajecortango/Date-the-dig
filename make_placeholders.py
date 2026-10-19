"""Genera sprite e sfondi placeholder per Date the Dig.

Uso: python make_placeholders.py
Output: PNG in game/images/ con i nomi esatti usati dalle scene.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "game", "images")

SPRITE_SIZE = (700, 1400)
BG_SIZE = (1920, 1080)

SPRITES = {
    "aede": ("#c0392b", ["neutra", "irritata", "sorpresa", "imbarazzata", "sorriso", "furia"]),
    "glauco": ("#6b6b6b", ["neutro", "minaccioso"]),
    "briseide": ("#b8860b", ["neutra"]),
}

BGS = {
    "sala_svelo": "#3b2a4f",
    "arena_athlion": "#8a7a52",
    "vicoli_zefiro": "#4a5568",
    "cala_notte": "#1a2240",
    "studio_glauco": "#43322a",
    "corridoio_ceppo": "#5a4a3a",
    "esterno_neve": "#c8d4e0",
    "nero": "#000000",
}

AEDE_REF = os.path.join(
    os.environ.get("TEMP", ""), "claude",
)  # riferimento aede_black.jpg: incollato solo se trovato (facoltativo)


def font(size):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except OSError:
        return ImageFont.load_default()


def text_center(draw, xy, label, fnt, fill):
    left, top, right, bottom = draw.textbbox((0, 0), label, font=fnt)
    w, h = right - left, bottom - top
    draw.text((xy[0] - w / 2, xy[1] - h / 2), label, font=fnt, fill=fill)


def make_sprite(name, expr, color):
    img = Image.new("RGBA", SPRITE_SIZE, (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    w, h = SPRITE_SIZE
    # silhouette: testa + busto
    d.ellipse([w * 0.28, h * 0.03, w * 0.72, h * 0.25], fill=color)
    d.rounded_rectangle([w * 0.15, h * 0.26, w * 0.85, h * 0.98], 60, fill=color)
    text_center(d, (w / 2, h * 0.55), name.upper(), font(64), "#ffffff")
    text_center(d, (w / 2, h * 0.62), expr, font(48), "#ffffff")
    img.save(os.path.join(OUT, f"{name} {expr}.png"))


def make_bg(name, color):
    img = Image.new("RGB", BG_SIZE, color)
    d = ImageDraw.Draw(img)
    fill = "#ffffff" if name != "esterno_neve" else "#333333"
    if name != "nero":
        text_center(d, (BG_SIZE[0] / 2, BG_SIZE[1] / 2), name.replace("_", " "), font(96), fill)
    img.save(os.path.join(OUT, f"bg {name}.png"))


def main():
    os.makedirs(OUT, exist_ok=True)
    n = 0
    for name, (color, exprs) in SPRITES.items():
        for expr in exprs:
            make_sprite(name, expr, color)
            n += 1
    for name, color in BGS.items():
        make_bg(name, color)
        n += 1
    print(f"{n} immagini scritte in {OUT}")


if __name__ == "__main__":
    main()
