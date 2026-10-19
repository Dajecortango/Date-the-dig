"""Genera la GUI in stile Doki Doki Literature Club (rosa pastello, pois,
bordi arrotondati) per Date the Dig. Sovrascrive i PNG in game/gui/.

Uso: python make_gui_ddlc.py
"""
import os
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
GUI = os.path.join(HERE, "game", "gui")

ROSA = (255, 92, 141)        # accento principale
ROSA_CHIARO = (255, 176, 200)
ROSA_PALLIDO = (255, 238, 245)
ROSA_RIGHE = (255, 217, 232)
BIANCO = (255, 255, 255)


def rounded(size, radius, fill, outline=None, width=3):
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([width, width, size[0] - 1 - width, size[1] - 1 - width],
                        radius, fill=fill, outline=outline, width=width)
    return img


def pattern(size):
    """Sfondo DDLC: rosa pallido, righe diagonali, pois bianchi."""
    img = Image.new("RGB", size, ROSA_PALLIDO)
    d = ImageDraw.Draw(img)
    step = 140
    for x in range(-size[1], size[0] + size[1], step):
        d.line([(x, 0), (x + size[1], size[1])], fill=ROSA_RIGHE, width=46)
    dot = Image.new("RGBA", size, (0, 0, 0, 0))
    dd = ImageDraw.Draw(dot)
    for yy in range(40, size[1], 110):
        off = 55 if (yy // 110) % 2 else 0
        for xx in range(40 + off, size[0], 110):
            dd.ellipse([xx - 7, yy - 7, xx + 7, yy + 7], fill=(255, 255, 255, 110))
    img = Image.alpha_composite(img.convert("RGBA"), dot)
    return img


def save(img, *path):
    img.save(os.path.join(GUI, *path))


def main():
    # Menu principale: pattern + pannello sinistro + sprite di Aede a destra.
    mm = pattern((1920, 1080))
    panel = rounded((500, 920), 40, (255, 255, 255, 185), (255, 255, 255, 255), 4)
    mm.alpha_composite(panel, (60, 80))
    sprite_path = os.path.join(HERE, "game", "images", "aede neutra.png")
    if os.path.exists(sprite_path):
        spr = Image.open(sprite_path).convert("RGBA")
        # ombra morbida dietro lo sprite
        sh = Image.new("RGBA", mm.size, (0, 0, 0, 0))
        alpha = spr.split()[3].point(lambda a: a * 0.25)
        shadow = Image.new("RGBA", spr.size, (187, 59, 86, 255))
        shadow.putalpha(alpha)
        sh.alpha_composite(shadow, (950 + 14, 1080 - spr.height + 14))
        mm.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
        # toppa dietro il buco nei capelli (maschera precalcolata, clip esatto)
        hp = os.path.join(GUI, "hole_patch.png")
        if os.path.exists(hp):
            mm.alpha_composite(Image.open(hp).convert("RGBA"), (950, 1080 - spr.height))
        mm.alpha_composite(spr, (950, 1080 - spr.height))
    save(mm.convert("RGB"), "main_menu.png")

    # Menu di gioco: pattern leggermente scurito, senza sprite.
    gm = pattern((1920, 1080))
    veil = Image.new("RGBA", gm.size, (255, 255, 255, 60))
    gm.alpha_composite(veil)
    save(gm.convert("RGB"), "game_menu.png")

    # Overlay.
    save(Image.new("RGBA", (1920, 1080), (0, 0, 0, 0)), "overlay", "main_menu.png")
    save(Image.new("RGBA", (1920, 1080), (255, 245, 248, 170)), "overlay", "game_menu.png")
    save(Image.new("RGBA", (1920, 1080), (255, 238, 245, 190)), "overlay", "confirm.png")

    # Textbox: bianco traslucido arrotondato con bordo rosa.
    tb = Image.new("RGBA", (1920, 277), (0, 0, 0, 0))
    box = rounded((1840, 245), 34, (255, 255, 255, 232), ROSA_CHIARO + (255,), 4)
    tb.alpha_composite(box, (40, 16))
    save(tb, "textbox.png")

    # Namebox: nastro bianco con bordo rosa (nomi nei colori personaggio).
    save(rounded((450, 54), 24, (255, 255, 255, 245), ROSA + (255,), 3), "namebox.png")

    # Frame generico e notify/skip.
    save(rounded((900, 375), 36, (255, 255, 255, 242), ROSA_CHIARO + (255,), 4), "frame.png")
    save(rounded((1383, 64), 28, (255, 255, 255, 225), ROSA_CHIARO + (255,), 3), "notify.png")
    save(rounded((360, 64), 28, (255, 255, 255, 225), ROSA_CHIARO + (255,), 3), "skip.png")

    # Scelte: bianco con bordo rosa; hover rosa chiaro.
    save(rounded((1185, 52), 24, (255, 255, 255, 235), ROSA_CHIARO + (255,), 3),
         "button", "choice_idle_background.png")
    save(rounded((1185, 52), 24, (255, 209, 224, 245), ROSA + (255,), 3),
         "button", "choice_hover_background.png")

    # Bottoni generici.
    save(rounded((450, 49), 22, (255, 255, 255, 0)), "button", "idle_background.png")
    save(rounded((450, 49), 22, (255, 195, 215, 200), ROSA + (255,), 2),
         "button", "hover_background.png")
    save(rounded((150, 45), 20, (255, 255, 255, 0)), "button", "quick_idle_background.png")
    save(rounded((150, 45), 20, (255, 209, 224, 180)), "button", "quick_hover_background.png")

    # Slot di salvataggio.
    save(rounded((276, 206), 24, (255, 255, 255, 215), ROSA_CHIARO + (255,), 3),
         "button", "slot_idle_background.png")
    save(rounded((276, 206), 24, (255, 232, 240, 245), ROSA + (255,), 3),
         "button", "slot_hover_background.png")

    print("GUI DDLC generata in", GUI)


if __name__ == "__main__":
    main()
