"""Genera la GUI di Date the Dig: layout in stile Doki Doki Literature Club,
palette della Famiglia Dignitas (rosso, oro, nero). Sovrascrive game/gui/.

Uso: python make_gui.py
"""
import os
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
GUI = os.path.join(HERE, "game", "gui")

ROSSO = (192, 57, 43)         # primario
ROSSO_SCURO = (74, 16, 16)
ROSSO_FONDO = (90, 21, 21)
ORO = (212, 175, 55)          # secondario
ORO_CHIARO = (240, 199, 94)
NERO = (16, 12, 12)
CREMA = (240, 230, 210)


def rounded(size, radius, fill, outline=None, width=3):
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([width, width, size[0] - 1 - width, size[1] - 1 - width],
                        radius, fill=fill, outline=outline, width=width)
    return img


def pattern(size):
    """Sfondo: rosso profondo, righe diagonali più scure, punti oro."""
    img = Image.new("RGB", size, ROSSO_FONDO)
    d = ImageDraw.Draw(img)
    step = 140
    for x in range(-size[1], size[0] + size[1], step):
        d.line([(x, 0), (x + size[1], size[1])], fill=ROSSO_SCURO, width=46)
    dot = Image.new("RGBA", size, (0, 0, 0, 0))
    dd = ImageDraw.Draw(dot)
    for yy in range(40, size[1], 110):
        off = 55 if (yy // 110) % 2 else 0
        for xx in range(40 + off, size[0], 110):
            dd.ellipse([xx - 6, yy - 6, xx + 6, yy + 6], fill=ORO + (70,))
    img = Image.alpha_composite(img.convert("RGBA"), dot)
    return img


def save(img, *path):
    img.save(os.path.join(GUI, *path))


def main():
    # Menu principale: pattern + pannello nero a sinistra + Aede a destra.
    mm = pattern((1920, 1080))
    panel = rounded((500, 920), 40, NERO + (205,), ORO + (255,), 4)
    mm.alpha_composite(panel, (60, 80))
    sprite_path = os.path.join(HERE, "game", "images", "aede neutra.png")
    if os.path.exists(sprite_path):
        spr = Image.open(sprite_path).convert("RGBA")
        sh = Image.new("RGBA", mm.size, (0, 0, 0, 0))
        alpha = spr.split()[3].point(lambda a: a * 0.35)
        shadow = Image.new("RGBA", spr.size, (0, 0, 0, 255))
        shadow.putalpha(alpha)
        sh.alpha_composite(shadow, (950 + 16, 1080 - spr.height + 16))
        mm.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7)))
        hp = os.path.join(GUI, "hole_patch.png")
        if os.path.exists(hp):
            mm.alpha_composite(Image.open(hp).convert("RGBA"), (950, 1080 - spr.height))
        mm.alpha_composite(spr, (950, 1080 - spr.height))
    save(mm.convert("RGB"), "main_menu.png")

    # Menu di gioco: pattern scurito.
    gm = pattern((1920, 1080))
    veil = Image.new("RGBA", gm.size, (0, 0, 0, 110))
    gm.alpha_composite(veil)
    save(gm.convert("RGB"), "game_menu.png")

    # Overlay.
    save(Image.new("RGBA", (1920, 1080), (0, 0, 0, 0)), "overlay", "main_menu.png")
    save(Image.new("RGBA", (1920, 1080), (16, 10, 10, 175)), "overlay", "game_menu.png")
    save(Image.new("RGBA", (1920, 1080), (16, 10, 10, 195)), "overlay", "confirm.png")

    # Textbox: nero traslucido arrotondato con bordo oro.
    tb = Image.new("RGBA", (1920, 277), (0, 0, 0, 0))
    box = rounded((1840, 245), 34, NERO + (218,), ORO + (255,), 4)
    tb.alpha_composite(box, (40, 16))
    save(tb, "textbox.png")

    # Namebox: nero bordato oro (i nomi restano nei colori personaggio).
    save(rounded((450, 54), 24, NERO + (240,), ORO + (255,), 3), "namebox.png")

    # Frame generico e notify/skip.
    save(rounded((900, 375), 36, NERO + (235,), ORO + (255,), 4), "frame.png")
    save(rounded((1383, 64), 28, NERO + (215,), ORO + (255,), 3), "notify.png")
    save(rounded((360, 64), 28, NERO + (215,), ORO + (255,), 3), "skip.png")

    # Scelte: nero bordo oro; hover rosso bordo oro chiaro.
    save(rounded((1185, 52), 24, NERO + (225,), ORO + (255,), 3),
         "button", "choice_idle_background.png")
    save(rounded((1185, 52), 24, (122, 31, 31, 245), ORO_CHIARO + (255,), 3),
         "button", "choice_hover_background.png")

    # Bottoni generici.
    save(rounded((450, 49), 22, (0, 0, 0, 0)), "button", "idle_background.png")
    save(rounded((450, 49), 22, ROSSO + (170,), ORO + (255,), 2),
         "button", "hover_background.png")
    save(rounded((150, 45), 20, (0, 0, 0, 0)), "button", "quick_idle_background.png")
    save(rounded((150, 45), 20, ROSSO + (150,)), "button", "quick_hover_background.png")

    # Slot di salvataggio.
    save(rounded((276, 206), 24, NERO + (205,), ORO + (255,), 3),
         "button", "slot_idle_background.png")
    save(rounded((276, 206), 24, (74, 16, 16, 240), ORO_CHIARO + (255,), 3),
         "button", "slot_hover_background.png")

    print("GUI Dignitas generata in", GUI)


if __name__ == "__main__":
    main()
