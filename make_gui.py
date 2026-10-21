"""Genera la GUI di Date the Dig: layout in stile Doki Doki Literature Club,
palette della Famiglia Dignitas (rosso, oro, nero). Sovrascrive game/gui/.

Uso: python make_gui.py
"""
import os
from PIL import Image, ImageChops, ImageDraw, ImageFilter

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


def diamond(d, cx, cy, r, fill):
    d.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], fill=fill)


def ornament_corners(img, inset=14, arm=34, color=ORO, w=2, diamonds=True):
    """Fregi rinascimentali: squadre d'angolo + diamante, dentro il bordo."""
    d = ImageDraw.Draw(img)
    W, H = img.size
    for cx, cy, sx, sy in [(inset, inset, 1, 1), (W - inset, inset, -1, 1),
                           (inset, H - inset, 1, -1), (W - inset, H - inset, -1, -1)]:
        d.line([(cx, cy + sy * arm), (cx, cy), (cx + sx * arm, cy)], fill=color + (255,), width=w)
        d.line([(cx + sx * 5, cy + sy * (arm - 10)), (cx + sx * 5, cy + sy * 5),
                (cx + sx * (arm - 10), cy + sy * 5)], fill=color + (160,), width=1)
        if diamonds:
            diamond(d, cx + sx * 11, cy + sy * 11, 4, color + (255,))
    return img


def parchment(w, h):
    """Pergamena orizzontale con rotoli alle estremità."""
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    roll_w = 34
    body = [roll_w - 6, 10, w - roll_w + 6, h - 10]
    # ombra del corpo
    d.rounded_rectangle([body[0] + 5, body[1] + 7, body[2] + 5, body[3] + 7],
                        10, fill=(30, 20, 10, 120))
    # corpo
    d.rounded_rectangle(body, 10, fill=(232, 213, 168, 255),
                        outline=(154, 124, 76, 255), width=2)
    # ombreggiatura tenue verso i rotoli e ai bordi alto/basso
    for k in range(14):
        a = 36 - k * 2
        if a <= 0:
            break
        d.line([(body[0] + k, body[1] + 2), (body[0] + k, body[3] - 2)], fill=(154, 124, 76, a))
        d.line([(body[2] - k, body[1] + 2), (body[2] - k, body[3] - 2)], fill=(154, 124, 76, a))
    d.line([(body[0] + 6, body[1] + 3), (body[2] - 6, body[1] + 3)], fill=(154, 124, 76, 50), width=3)
    d.line([(body[0] + 6, body[3] - 3), (body[2] - 6, body[3] - 3)], fill=(154, 124, 76, 50), width=3)
    # bordo interno decorativo
    d.rounded_rectangle([body[0] + 10, body[1] + 8, body[2] - 10, body[3] - 8],
                        8, outline=(154, 124, 76, 160), width=1)
    # rotoli laterali
    for cx in (roll_w // 2 + 2, w - roll_w // 2 - 2):
        d.rounded_rectangle([cx - roll_w // 2, 0, cx + roll_w // 2, h], roll_w // 2,
                            fill=(196, 168, 118, 255), outline=(122, 96, 58, 255), width=2)
        d.rounded_rectangle([cx - 5, 4, cx + 5, h - 4], 5, fill=(232, 213, 168, 255))
    return img


def ornament_sides(img, color=ORO):
    """Diamante centrale sui lati corti (per nastri e namebox)."""
    d = ImageDraw.Draw(img)
    W, H = img.size
    diamond(d, 16, H // 2, 5, color + (255,))
    diamond(d, W - 16, H // 2, 5, color + (255,))
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


PORTRAIT = 160


def portrait_base():
    """Tondo nero con doppio bordo oro, stesso linguaggio di window_icon."""
    img = Image.new("RGBA", (PORTRAIT, PORTRAIT), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([2, 2, PORTRAIT - 3, PORTRAIT - 3], fill=NERO + (255,))
    return img


def portrait_rings(img):
    d = ImageDraw.Draw(img)
    d.ellipse([2, 2, PORTRAIT - 3, PORTRAIT - 3], outline=ORO + (255,), width=4)
    d.ellipse([10, 10, PORTRAIT - 11, PORTRAIT - 11], outline=ORO + (120,), width=2)
    return img


def portrait(sprite_name, out_name, top_f=0.0, side_f=0.42, cx_f=0.5):
    """Ritaglia la testa dallo sprite e la monta nel tondo bordato oro.
    top_f/side_f/cx_f: frazioni del bounding box (verticale, lato, centro x)."""
    path = os.path.join(HERE, "game", "images", sprite_name)
    spr = Image.open(path).convert("RGBA")
    bb = spr.getbbox()
    bh = bb[3] - bb[1]
    side = int(bh * side_f)
    cx = bb[0] + int((bb[2] - bb[0]) * cx_f)
    top = bb[1] + int(bh * top_f)
    head = spr.crop((cx - side // 2, top, cx + side // 2, top + side))
    head = head.resize((PORTRAIT - 12, PORTRAIT - 12), Image.LANCZOS)

    img = portrait_base()
    circle = Image.new("L", (PORTRAIT - 12, PORTRAIT - 12), 0)
    ImageDraw.Draw(circle).ellipse([0, 0, PORTRAIT - 13, PORTRAIT - 13], fill=255)
    img.paste(head, (6, 6), ImageChops.multiply(circle, head.split()[3]))
    portrait_rings(img)
    save(img, out_name)


def portrait_diamond(out_name, outer, inner):
    """Tondo con diamante: segnaposto (route bloccate o sprite mancante)."""
    img = portrait_base()
    d = ImageDraw.Draw(img)
    c = PORTRAIT // 2
    diamond(d, c, c, 34, outer)
    diamond(d, c, c, 18, inner)
    portrait_rings(img)
    save(img, out_name)


def menu_front():
    """Tutto il menu principale TRANNE il pattern (che scorre da solo):
    pannello, pergamena, ombra e sprite di Aede, su fondo trasparente."""
    front = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    panel = rounded((500, 920), 40, NERO + (205,), ORO + (255,), 4)
    ornament_corners(panel, inset=18, arm=40)
    front.alpha_composite(panel, (60, 80))
    front.alpha_composite(parchment(450, 185), (85, 105))
    sprite_path = os.path.join(HERE, "game", "images", "aede neutra.png")
    if os.path.exists(sprite_path):
        spr = Image.open(sprite_path).convert("RGBA")
        sh = Image.new("RGBA", front.size, (0, 0, 0, 0))
        alpha = spr.split()[3].point(lambda a: a * 0.35)
        shadow = Image.new("RGBA", spr.size, (0, 0, 0, 255))
        shadow.putalpha(alpha)
        sh.alpha_composite(shadow, (950 + 16, 1080 - spr.height + 16))
        front.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7)))
        hp = os.path.join(GUI, "hole_patch.png")
        if os.path.exists(hp):
            front.alpha_composite(Image.open(hp).convert("RGBA"), (950, 1080 - spr.height))
        front.alpha_composite(spr, (950, 1080 - spr.height))
    return front


def main():
    # Menu principale: pattern + fronte. main_menu.png resta per compatibilita';
    # la screen anima mm_pattern.png (tile 1540: periodo comune di righe 140
    # e pois 110/220, quindi senza giunte) sotto mm_front.png.
    front = menu_front()
    mm = pattern((1920, 1080))
    mm.alpha_composite(front)
    save(mm.convert("RGB"), "main_menu.png")
    save(pattern((1540, 1540)).convert("RGB"), "mm_pattern.png")
    save(front, "mm_front.png")

    # Indicatore click-to-continue: diamantino oro.
    ctc = Image.new("RGBA", (26, 26), (0, 0, 0, 0))
    d = ImageDraw.Draw(ctc)
    diamond(d, 13, 13, 10, ORO + (255,))
    diamond(d, 13, 13, 5, ROSSO + (255,))
    save(ctc, "ctc.png")

    # Menu di gioco: pattern scurito.
    gm = pattern((1920, 1080))
    veil = Image.new("RGBA", gm.size, (0, 0, 0, 110))
    gm.alpha_composite(veil)
    save(gm.convert("RGB"), "game_menu.png")

    # Overlay.
    save(Image.new("RGBA", (1920, 1080), (0, 0, 0, 0)), "overlay", "main_menu.png")
    save(Image.new("RGBA", (1920, 1080), (16, 10, 10, 175)), "overlay", "game_menu.png")
    save(Image.new("RGBA", (1920, 1080), (16, 10, 10, 195)), "overlay", "confirm.png")

    # Textbox: nero traslucido arrotondato con bordo oro e fregi d'angolo.
    tb = Image.new("RGBA", (1920, 277), (0, 0, 0, 0))
    box = rounded((1840, 245), 34, NERO + (218,), ORO + (255,), 4)
    ornament_corners(box, inset=16, arm=30)
    tb.alpha_composite(box, (40, 16))
    save(tb, "textbox.png")

    # Namebox: nero bordato oro con diamanti laterali.
    nb = rounded((450, 54), 24, NERO + (240,), ORO + (255,), 3)
    ornament_sides(nb)
    save(nb, "namebox.png")

    # Frame generico e notify/skip.
    fr = rounded((900, 375), 36, NERO + (235,), ORO + (255,), 4)
    ornament_corners(fr, inset=16, arm=28)
    save(fr, "frame.png")
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

    # Icona finestra: tondo nero, doppio bordo oro, diamante.
    ic = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    d = ImageDraw.Draw(ic)
    d.ellipse([8, 8, 248, 248], fill=NERO + (255,), outline=ORO + (255,), width=10)
    d.ellipse([26, 26, 230, 230], outline=ORO + (140,), width=3)
    diamond(d, 128, 128, 54, ROSSO + (255,))
    diamond(d, 128, 128, 30, ORO + (255,))
    save(ic, "window_icon.png")

    # Ritratti per la selezione route.
    portrait("aede neutra.png", "portrait_aede.png", top_f=0.0, side_f=0.45, cx_f=0.43)
    portrait("caino neutro.png", "portrait_caino.png", top_f=0.0, side_f=0.42, cx_f=0.52)
    portrait("ofelia neutra.png", "portrait_ofelia.png", top_f=0.0, side_f=0.40, cx_f=0.45)
    # Icaro e Druso: sprite ancora placeholder, diamanti finche' non c'e' l'arte.
    portrait_diamond("portrait_icaro.png", (127, 160, 106, 255), ORO + (255,))
    portrait_diamond("portrait_druso.png", (138, 155, 176, 255), ORO + (255,))
    portrait_diamond("portrait_locked.png", (90, 30, 26, 255), (120, 100, 48, 255))

    print("GUI Dignitas generata in", GUI)


if __name__ == "__main__":
    main()
