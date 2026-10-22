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
    # Rosette d'oro a quattro petali (damasco), disegnate a 2x.
    k = 2
    dot = Image.new("RGBA", (size[0] * k, size[1] * k), (0, 0, 0, 0))
    dd = ImageDraw.Draw(dot)
    for yy in range(40, size[1], 110):
        off = 55 if (yy // 110) % 2 else 0
        for xx in range(40 + off, size[0], 110):
            X, Y = xx * k, yy * k
            for ex, ey in ((0, -1), (1, 0), (0, 1), (-1, 0)):
                cx, cy = X + ex * 5 * k, Y + ey * 5 * k
                dd.ellipse([cx - 4 * k, cy - 4 * k, cx + 4 * k, cy + 4 * k], fill=ORO + (62,))
            dd.ellipse([X - 2 * k, Y - 2 * k, X + 2 * k, Y + 2 * k], fill=ORO_CHIARO + (120,))
    dot = dot.resize(size, Image.LANCZOS)
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
    """Medaglione: anello d'oro cel-shaded con contorno e quattro rubini."""
    t = Tela(PORTRAIT, PORTRAIT)
    c = PORTRAIT / 2.0
    cel(t, m_sub(m_ell(t, c, c, c - 2), m_ell(t, c, c, c - 9)), "oro",
        ombra=2.2, luce=1.6, contorno=1.6)
    colora(t, m_sub(m_ell(t, c, c, c - 5), m_ell(t, c, c, c - 6)), MAT["oro"][0], 200)
    for a in (0.25, 0.75, 1.25, 1.75):
        gemma(t, c + (c - 5.5) * math.cos(a * math.pi), c + (c - 5.5) * math.sin(a * math.pi),
              3.6, "rubino", "oro", taglio="rombo")
    scintilla(t, c - 42, c - 44, 9)
    img.alpha_composite(t.fine())
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
    """Il menu principale TRANNE il pattern (che scorre da solo) e il cast
    (che e' interattivo, in game/menu_cast.rpy): pannello laccato con cornice
    dorata miniata e pergamena, su fondo trasparente."""
    front = Tela(1920, 1080)
    cornice(500, 920, ang=60, banda=11, fondo_a=212, raggio=14, tela=front, off=(60, 80))
    for v in (-1, 1):
        girali(front, 310 + v * 14, 80 + 920 - 9.5, v, L=120)
    gemma(front, 310, 80 + 920 - 9.5, 8, "rubino", "oro", taglio="rombo")
    scintilla(front, 318, 990, 8)
    f = front.fine()
    f.alpha_composite(pergamena(450, 185).fine(), (85, 105))
    return f


# Cast del menu (carosello, game/menu_cast.rpy): (chiave, sprite), nell'ordine
# del giro. Tutti alla stessa altezza MM_ALTEZZA, cosi' a scala piena (il
# personaggio al centro) hanno lo stesso ingombro; le dimensioni ai lati le
# decide la screen con zoom.
MM_CAST = [
    ("aede", "aede neutra.webp"),
    ("ofelia", "ofelia compiaciuta.webp"),
    ("caino", "caino neutro.webp"),
    ("icaro", "icaro furbo.webp"),
    ("druso", "druso ghigno.webp"),
]
MM_ALTEZZA = 860  # altezza dello sprite a scala piena
MM_MARGINE = 40   # bordo trasparente attorno allo sprite (ombra e alone)


def menu_cast():
    """Per ogni personaggio del menu: sprite (idle), sprite schiarito con
    alone oro (hover), solo alone (_alone, per il personaggio al centro del
    carosello) e ombra sfocata, tutti sulla stessa tela (sprite + MM_MARGINE
    per lato), cosi' si sovrappongono allineati. Poi frecce e pallini."""
    M = MM_MARGINE
    for key, nome in MM_CAST:
        spr = Image.open(os.path.join(HERE, "game", "images", nome)).convert("RGBA")
        scala = MM_ALTEZZA / float(spr.height)
        spr = spr.resize((int(round(spr.width * scala)), MM_ALTEZZA), Image.LANCZOS)
        size = (spr.width + 2 * M, spr.height + 2 * M)
        alpha = spr.split()[3]

        idle = Image.new("RGBA", size, (0, 0, 0, 0))
        idle.alpha_composite(spr, (M, M))
        save(idle, "cast_%s.webp" % key)

        # Ombra: 35%, +16 px, sfocatura 7.
        sh = Image.new("RGBA", size, (0, 0, 0, 0))
        shadow = Image.new("RGBA", spr.size, (0, 0, 0, 255))
        shadow.putalpha(alpha.point(lambda a: a * 0.35))
        sh.alpha_composite(shadow, (M + 16, M + 16))
        save(sh.filter(ImageFilter.GaussianBlur(7)), "cast_%s_ombra.webp" % key)

        # Alone oro sfocato attorno alla sagoma.
        glow_a = Image.new("L", size, 0)
        glow_a.paste(alpha.filter(ImageFilter.MaxFilter(9)), (M, M))
        glow_a = glow_a.filter(ImageFilter.GaussianBlur(10)).point(
            lambda a: min(255, int(a * 0.9)))
        glow = Image.new("RGBA", size, ORO_CHIARO + (0,))
        glow.putalpha(glow_a)
        save(glow, "cast_%s_alone.webp" % key)

        # Hover: alone + sprite schiarito.
        hov = Image.new("RGBA", size, (0, 0, 0, 0))
        hov.alpha_composite(glow)
        chiaro = Image.blend(spr, Image.new("RGBA", spr.size, (255, 244, 220, 255)), 0.10)
        chiaro.putalpha(alpha)
        hov.alpha_composite(chiaro, (M, M))
        save(hov, "cast_%s_hover.webp" % key)

    menu_carosello_comandi()


def menu_carosello_comandi():
    """Frecce del carosello e pallini: disegnati in stile_menu()."""
    stile_carosello()


def fiocco():
    """Fiocco di neve per SnowBlossom: puntino crema morbido."""
    img = Image.new("RGBA", (24, 24), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([7, 7, 17, 17], fill=CREMA + (235,))
    img = img.filter(ImageFilter.GaussianBlur(1.6))
    save(img, "fiocco.png")


def cartello_data():
    """Pergamena miniata del cartello di data (cal_loop): Luna e giorno."""
    save(pergamena(760, 210).fine(), "cartello_data.png")


def maschera_diagonale():
    """Maschera per ImageDissolve: gradiente diagonale, l'alto-sinistra
    (bianco) passa per primo, come le righe diagonali del pattern."""
    W, H = 1920, 1080
    vert = Image.linear_gradient("L").resize((W, H), Image.BILINEAR)
    oriz = Image.linear_gradient("L").rotate(90).resize((W, H), Image.BILINEAR)
    grad = ImageChops.add(vert, oriz, scale=2)
    img = ImageChops.invert(grad).convert("RGB")
    save(img, "transizione_diagonale.png")


def clessidra():
    """Clessidra oro per gli inviti a scadenza nel pianificatore (ruotata
    dall'ATL clessidra_gira in calendario.rpy)."""
    S = 4                                   # supersampling
    W, H = 30, 44
    img = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Montanti e piatti.
    d.rectangle([2 * S, 0, (W - 2) * S, 4 * S], fill=ORO + (255,))
    d.rectangle([2 * S, (H - 4) * S, (W - 2) * S, H * S - 1], fill=ORO + (255,))
    # Vetro: due triangoli che si toccano al centro.
    cx, cy = W * S // 2, H * S // 2
    top = [(5 * S, 5 * S), ((W - 5) * S, 5 * S), (cx + 2 * S, cy), (cx - 2 * S, cy)]
    bot = [(cx - 2 * S, cy), (cx + 2 * S, cy), ((W - 5) * S, (H - 5) * S), (5 * S, (H - 5) * S)]
    d.polygon(top, fill=CREMA + (60,), outline=ORO_CHIARO + (255,))
    d.polygon(bot, fill=CREMA + (60,), outline=ORO_CHIARO + (255,))
    # Sabbia: poca sopra, mucchio sotto, filo al centro.
    d.polygon([(10 * S, 12 * S), ((W - 10) * S, 12 * S), (cx + S, cy - S), (cx - S, cy - S)],
              fill=ROSSO + (255,))
    d.polygon([(cx, (H - 13) * S), ((W - 7) * S, (H - 6) * S), (7 * S, (H - 6) * S)],
              fill=ROSSO + (255,))
    d.line([(cx, cy), (cx, (H - 13) * S)], fill=ROSSO + (255,), width=S)
    img = img.resize((W, H), Image.LANCZOS)
    save(img, "clessidra.png")


# Fase della luna per Luna I-VI: frazione illuminata (crescente verso il
# plenilunio del climax, Luna VI).
LUNE_FASI = {1: 0.18, 2: 0.33, 3: 0.5, 4: 0.66, 5: 0.82, 6: 1.0}


def lune():
    """gui/luna_<n>.png: disco oro con la parte in ombra scura, bordo oro."""
    import math
    S, D = 4, 72
    N = D * S
    r = N / 2.0 - 3 * S
    for n, f in LUNE_FASI.items():
        img = Image.new("RGBA", (N, N), (0, 0, 0, 0))
        px = img.load()
        xt_k = math.cos(math.pi * f)
        for y in range(N):
            v = (y + 0.5 - N / 2.0) / r
            if abs(v) >= 1:
                continue
            w = math.sqrt(1 - v * v)
            for x in range(N):
                u = (x + 0.5 - N / 2.0) / r
                if abs(u) >= w:
                    continue
                lit = u > w * xt_k          # crescente: luce a destra
                if lit:
                    # Leggera ombreggiatura verso il terminatore.
                    t = min(1.0, (u - w * xt_k) / (0.25 + 1e-6))
                    c = tuple(int(ORO[i] + (ORO_CHIARO[i] - ORO[i]) * t) for i in range(3))
                    px[x, y] = c + (255,)
                else:
                    px[x, y] = (40, 30, 26, 235)
        d = ImageDraw.Draw(img)
        c0 = N / 2.0 - r
        d.ellipse([c0, c0, N - c0, N - c0], outline=ORO + (200,), width=2 * S)
        img = img.resize((D, D), Image.LANCZOS)
        save(img, "luna_%d.png" % n)



# =============================================================================
# Stile "miniato": manoscritto rinascimentale con filtro anime.
# Contorni d'inchiostro netti, colore a bande piatte (cel shading: ombra in
# basso/destra, luce in alto/sinistra), luci speculari e scintille su oro e
# gemme, alone all'hover. Tutto disegnato a 2x (SS) e ridotto con LANCZOS.
# Le cornici sono pensate per Frame a 9 fette: ornamenti solo negli angoli,
# lati dritti. Uso: rigenera_stile().
# =============================================================================
import math

SS = 2
INK = (34, 14, 11)              # inchiostro dei contorni
ORO_SCURO = (150, 100, 28)
# materiale: (ombra, base, luce, speculare)
MAT = {
    "oro": ((160, 108, 30), (218, 174, 56), (250, 220, 124), (255, 251, 228)),
    "oro_vivo": ((198, 138, 36), (246, 204, 96), (255, 236, 162), (255, 255, 246)),
    "rosso": ((118, 24, 22), (186, 46, 38), (230, 96, 70), (255, 214, 196)),
    "lacca": ((9, 6, 6), (22, 15, 14), (40, 27, 25), (80, 56, 50)),
    "lacca_rossa": ((52, 10, 12), (84, 19, 20), (116, 32, 30), (170, 70, 60)),
    "pergamena": ((212, 186, 134), (238, 223, 186), (249, 241, 218), (255, 252, 240)),
    "rotolo": ((168, 132, 80), (204, 172, 118), (232, 208, 160), (250, 236, 206)),
    "cera": ((100, 14, 20), (166, 30, 36), (210, 70, 66), (255, 200, 190)),
    "rubino": ((98, 8, 22), (178, 24, 42), (234, 76, 84), (255, 240, 244)),
}


def _s(v):
    return int(round(v * SS))


class Tela(object):
    """Tela RGBA a SS volte la dimensione finale; coordinate in px finali."""

    def __init__(self, w, h):
        self.w, self.h = w, h
        self.img = Image.new("RGBA", (_s(w), _s(h)), (0, 0, 0, 0))

    def m(self):
        return Image.new("L", self.img.size, 0)

    def fine(self):
        return self.img.resize((self.w, self.h), Image.LANCZOS)


def _b(box):
    return [_s(box[0]), _s(box[1]), _s(box[2]) - 1, _s(box[3]) - 1]


def m_rect(t, box, r=0):
    mk = t.m()
    d = ImageDraw.Draw(mk)
    if r:
        d.rounded_rectangle(_b(box), _s(r), fill=255)
    else:
        d.rectangle(_b(box), fill=255)
    return mk


def m_poly(t, pts):
    mk = t.m()
    ImageDraw.Draw(mk).polygon([(_s(x), _s(y)) for x, y in pts], fill=255)
    return mk


def m_ell(t, cx, cy, rx, ry=None):
    ry = rx if ry is None else ry
    mk = t.m()
    ImageDraw.Draw(mk).ellipse(_b((cx - rx, cy - ry, cx + rx, cy + ry)), fill=255)
    return mk


def m_linea(t, pts, w):
    mk = t.m()
    ImageDraw.Draw(mk).line([(_s(x), _s(y)) for x, y in pts], fill=255,
                            width=max(1, _s(w)), joint="curve")
    return mk


def m_sub(a, b):
    return ImageChops.subtract(a, b)


def m_add(*ms):
    out = ms[0]
    for k in ms[1:]:
        out = ImageChops.lighter(out, k)
    return out


def m_and(a, b):
    return ImageChops.multiply(a, b)


def _sposta(mk, dx, dy):
    out = Image.new("L", mk.size, 0)
    out.paste(mk, (dx, dy))
    return out


def dilata(mk, r):
    for _ in range(max(1, _s(r))):
        mk = mk.filter(ImageFilter.MaxFilter(3))
    return mk


def colora(t, mk, rgb, a=255):
    layer = Image.new("RGBA", t.img.size, tuple(rgb) + (0,))
    layer.putalpha(mk if a >= 255 else mk.point(lambda v: v * a // 255))
    t.img.alpha_composite(layer)


def cel(t, mk, mat, ombra=2.0, luce=1.5, contorno=1.5, a=255, lati=True):
    """Riempie la maschera a bande piatte: ombra in basso (e a destra),
    luce in alto (e a sinistra), contorno d'inchiostro attorno."""
    sh, base, light, _sp = MAT[mat]
    L = Image.new("RGBA", t.img.size, (0, 0, 0, 0))
    L.paste(sh + (255,), (0, 0), mk)
    if ombra:
        k = _s(ombra)
        bm = m_and(mk, _sposta(mk, 0, -k))
        if lati:
            bm = m_and(bm, _sposta(mk, -k, 0))
        L.paste(base + (255,), (0, 0), bm)
    else:
        L.paste(base + (255,), (0, 0), mk)
    if luce:
        k = _s(luce)
        lm = m_sub(mk, _sposta(mk, 0, k))
        if lati:
            lm = m_add(lm, m_sub(mk, _sposta(mk, k, 0)))
        L.paste(light + (255,), (0, 0), lm)
    if a < 255:
        L.putalpha(L.split()[3].point(lambda v: v * a // 255))
    if contorno:
        colora(t, m_sub(dilata(mk, contorno), mk), INK)
    t.img.alpha_composite(L)


def alone(t, mk, rgb=ORO_CHIARO, r=8, forza=1.0):
    """Alone morbido (bloom) attorno alla maschera."""
    g = dilata(mk, r * 0.25).filter(ImageFilter.GaussianBlur(_s(r) * 0.5))
    g = g.point(lambda v: min(255, int(v * forza)))
    # Sfuma a zero verso i bordi dell'immagine: niente riquadri tagliati
    # quando l'alone esce dalla tela (o la Frame la stira).
    W, H = t.img.size
    k = max(2, _s(r * 0.3))
    bordo = Image.new("L", (W, H), 0)
    ImageDraw.Draw(bordo).rectangle([k, k, W - 1 - k, H - 1 - k], fill=255)
    g = m_and(g, bordo.filter(ImageFilter.GaussianBlur(k * 0.7)))
    colora(t, g, rgb)


def scintilla(t, cx, cy, r, rgb=(255, 253, 242), alone_rgb=ORO_CHIARO):
    """Scintilla anime: stella a quattro punte bianca con alone e croce."""
    colora(t, m_ell(t, cx, cy, r * 0.45).filter(ImageFilter.GaussianBlur(_s(r) * 0.45)),
           alone_rgb, 230)
    for rr, rot in ((r, 0.0), (r * 0.5, math.pi / 4)):
        k = rr * 0.17
        pts = []
        for i in range(4):
            a = rot + i * math.pi / 2
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
            b = a + math.pi / 4
            pts.append((cx + k * math.cos(b), cy + k * math.sin(b)))
        mk = m_poly(t, pts)
        colora(t, m_sub(dilata(mk, 0.5), mk), ORO_SCURO, 160)
        colora(t, mk, rgb)


def gemma(t, cx, cy, r, mat="rubino", castone="oro", taglio="tondo", luce=True):
    """Gemma incastonata: castone d'oro, pietra a bande, riflesso."""
    if taglio == "rombo":
        R = r + max(1.6, r * 0.38)
        cel(t, m_poly(t, [(cx, cy - R), (cx + R, cy), (cx, cy + R), (cx - R, cy)]),
            castone, ombra=max(0.8, r * 0.12), luce=0.8, contorno=1.2)
        gm = m_poly(t, [(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)])
    else:
        cel(t, m_ell(t, cx, cy, r + max(1.5, r * 0.32)), castone,
            ombra=max(0.8, r * 0.12), luce=0.8, contorno=1.2)
        gm = m_ell(t, cx, cy, r)
    cel(t, gm, mat, ombra=r * 0.42, luce=r * 0.14, contorno=0.6)
    if luce:
        sp = MAT[mat][3]
        colora(t, m_ell(t, cx - r * 0.32, cy - r * 0.36, r * 0.3, r * 0.2), sp)
        colora(t, m_ell(t, cx + r * 0.36, cy + r * 0.34, max(0.6, r * 0.11)), sp, 210)


def foglia(t, x0, y0, dx, dy, L, wmax, mat="oro"):
    """Foglia d'acanto stilizzata (mandorla) da (x0,y0) lungo (dx,dy)."""
    n_ = math.hypot(dx, dy)
    dx, dy = dx / n_, dy / n_
    nx, ny = -dy, dx
    sup, inf = [], []
    n = 14
    for i in range(n + 1):
        u = i / float(n)
        hw = wmax * (math.sin(math.pi * u) ** 0.8) * (1 - 0.35 * u)
        x, y = x0 + dx * L * u, y0 + dy * L * u
        sup.append((x + nx * hw, y + ny * hw))
        inf.append((x - nx * hw, y - ny * hw))
    cel(t, m_poly(t, sup + inf[::-1]), mat, ombra=0.9, luce=0.7, contorno=1.1)
    # nervatura
    colora(t, m_linea(t, [(x0 + dx * L * 0.15, y0 + dy * L * 0.15),
                          (x0 + dx * L * 0.8, y0 + dy * L * 0.8)], 0.7), MAT[mat][0])


def rosetta(t, cx, cy, r, mat="oro", centro="rubino"):
    """Rosetta rinascimentale: otto petali e gemma al centro."""
    pm = t.m()
    for i in range(8):
        a = i * math.pi / 4
        pm = m_add(pm, m_ell(t, cx + r * 0.62 * math.cos(a), cy + r * 0.62 * math.sin(a), r * 0.38))
    pm = m_add(pm, m_ell(t, cx, cy, r * 0.62))
    cel(t, pm, mat, ombra=max(0.8, r * 0.12), luce=max(0.6, r * 0.08), contorno=1.2)
    gemma(t, cx, cy, r * 0.36, centro, castone=mat)


def angolo(t, px, py, sx, sy, ang, banda, mat="oro", gem="rubino"):
    """Fregio d'angolo: rosetta sul vertice e foglie d'acanto lungo i lati
    (verso l'interno della cornice)."""
    inn = banda / 2.0 + 4.5
    L = ang - 14
    for (dx, dy, ox, oy) in ((sx, 0, 0, sy * inn), (0, sy, sx * inn, 0)):
        foglia(t, px + dx * 11 + ox, py + dy * 11 + oy, dx, dy, L, 4.8, mat)
        cx = px + dx * (11 + L + 4) + ox
        cy = py + dy * (11 + L + 4) + oy
        cel(t, m_ell(t, cx, cy, 2.2), mat, ombra=0.6, luce=0.5, contorno=1.0)
    # piastra a losanga sotto la rosetta
    R = ang * 0.46
    qx, qy = px + sx * 2, py + sy * 2
    cel(t, m_poly(t, [(qx, qy - R), (qx + R, qy), (qx, qy + R), (qx - R, qy)]), mat,
        ombra=1.2, luce=0.9, contorno=1.4)
    rosetta(t, qx, qy, ang * 0.32, mat, gem)


def cornice(w, h, ang=44, banda=8, fondo="lacca", fondo_a=236, mat="oro",
            gem="rubino", m=4, raggio=10, filetti=True, angoli=True,
            alone_rgb=None, tela=None, off=(0, 0)):
    """Cornice dorata a 9 fette su pannello laccato. Ritorna la Tela."""
    t = tela or Tela(w, h)
    ox, oy = off
    est = (ox + m, oy + m, ox + w - m, oy + h - m)
    inn = (est[0] + banda, est[1] + banda, est[2] - banda, est[3] - banda)
    me = m_rect(t, est, raggio)
    if alone_rgb:
        alone(t, me, alone_rgb, r=m * 1.6)
    if fondo:
        pan = m_rect(t, inn, max(2, raggio - banda))
        cel(t, pan, fondo, ombra=0, luce=0, contorno=0, a=fondo_a)
        # banda di luce piatta sotto il bordo superiore (cel)
        colora(t, m_and(pan, m_rect(t, (inn[0], inn[1], inn[2], inn[1] + 5))),
               MAT[fondo][2], fondo_a)
    if filetti:
        for d_, rgb, a in ((6, ORO, 190), (10, ROSSO, 210)):
            b1 = (inn[0] + d_, inn[1] + d_, inn[2] - d_, inn[3] - d_)
            b2 = (b1[0] + 1, b1[1] + 1, b1[2] - 1, b1[3] - 1)
            colora(t, m_sub(m_rect(t, b1, 4), m_rect(t, b2, 3)), rgb, a)
    ring = m_sub(me, m_rect(t, inn, max(2, raggio - banda)))
    cel(t, ring, mat, ombra=banda * 0.28, luce=banda * 0.2, contorno=1.6)
    # intarsio di smalto rosso al centro della modanatura (con filo d'inchiostro)
    q = banda * 0.36
    g1 = (est[0] + q, est[1] + q, est[2] - q, est[3] - q)
    q2 = banda - q
    g2 = (est[0] + q2, est[1] + q2, est[2] - q2, est[3] - q2)
    if banda >= 7:
        smalto = m_sub(m_rect(t, g1, max(1, raggio - q)), m_rect(t, g2, max(1, raggio - q2)))
        colora(t, m_sub(dilata(smalto, 0.6), smalto), INK)
        cel(t, smalto, "rosso", ombra=0.6, luce=0.5, contorno=0)
    else:
        g2 = (g1[0] + 1, g1[1] + 1, g1[2] - 1, g1[3] - 1)
        colora(t, m_sub(m_rect(t, g1, max(1, raggio - 2)), m_rect(t, g2, max(1, raggio - 3))),
               MAT[mat][0], 200)
    if angoli:
        c = banda / 2.0
        for px, py, sx, sy in ((est[0] + c, est[1] + c, 1, 1), (est[2] - c, est[1] + c, -1, 1),
                               (est[0] + c, est[3] - c, 1, -1), (est[2] - c, est[3] - c, -1, -1)):
            angolo(t, px, py, sx, sy, ang, banda, mat, gem)
    return t


def placca(w, h, fondo="lacca", fondo_a=232, mat="oro", g=4, smusso=9,
           banda=3.5, gemme=True, alone_rgb=None, scintille=False, filetto=True):
    """Placca a spigoli smussati (sicura per 9 fette): bottoni, slot."""
    t = Tela(w, h)
    c = smusso
    x0, y0, x1, y1 = g, g, w - g, h - g

    def ott(d):
        return [(x0 + c + d * 0.4, y0 + d), (x1 - c - d * 0.4, y0 + d), (x1 - d, y0 + c + d * 0.4),
                (x1 - d, y1 - c - d * 0.4), (x1 - c - d * 0.4, y1 - d), (x0 + c + d * 0.4, y1 - d),
                (x0 + d, y1 - c - d * 0.4), (x0 + d, y0 + c + d * 0.4)]
    me = m_poly(t, ott(0))
    if alone_rgb:
        alone(t, me, alone_rgb, r=g * 1.8, forza=1.2)
    pan = m_poly(t, ott(banda))
    cel(t, pan, fondo, ombra=0, luce=0, contorno=0, a=fondo_a)
    colora(t, m_and(pan, m_rect(t, (0, y0 + banda, w, y0 + banda + 3))), MAT[fondo][2], fondo_a)
    if filetto:
        f = m_sub(m_poly(t, ott(banda + 3)), m_poly(t, ott(banda + 4)))
        colora(t, f, ORO, 150)
    cel(t, m_sub(me, pan), mat, ombra=banda * 0.32, luce=banda * 0.25, contorno=1.4)
    if gemme:
        r = max(2.0, smusso * 0.3)
        for px, py in ((x0 + c * 0.55, y0 + c * 0.55), (x1 - c * 0.55, y0 + c * 0.55),
                       (x0 + c * 0.55, y1 - c * 0.55), (x1 - c * 0.55, y1 - c * 0.55)):
            gemma(t, px, py, r, "rubino", mat, taglio="rombo", luce=r > 2.5)
    if scintille:
        scintilla(t, x0 + c * 0.55, y0 + c * 0.55, smusso * 1.0)
        scintilla(t, x1 - c * 0.55, y1 - c * 0.55, smusso * 0.8)
    return t


def nastro(w, h, fondo="rosso", g=6, coda=16, mat="oro", alone_rgb=None,
           scintille=False, gemme=False, fondo_a=255):
    """Nastro a coda di rondine con bordi dorati (navigazione, conferme)."""
    t = Tela(w, h)
    pts = [(g, g), (w - g, g), (w - g - coda, h / 2.0), (w - g, h - g),
           (g, h - g), (g + coda, h / 2.0)]
    mk = m_poly(t, pts)
    if alone_rgb:
        alone(t, mk, alone_rgb, r=g * 1.5, forza=1.15)
    cel(t, mk, fondo, ombra=2.5, luce=1.5, contorno=1.5, a=fondo_a, lati=False)
    for y0 in (g + 2.5, h - g - 5.5):
        cel(t, m_and(mk, m_rect(t, (0, y0, w, y0 + 3))), mat, ombra=0.8, luce=0.6,
            contorno=0, lati=False)
    if gemme:
        for x in (g + coda + 10, w - g - coda - 10):
            gemma(t, x, h / 2.0, 3.6, "rubino", mat, taglio="rombo")
    if scintille:
        scintilla(t, g + coda + 4, g + 3, 9)
        scintilla(t, w - g - coda - 6, h - g - 2, 7)
        scintilla(t, w - g - 4, g + 1, 5)
    return t


def cartiglio(w, h, stato="idle", g=9, p=24):
    """Cartiglio a punte per le scelte: idle laccato, hover smalto rosso."""
    t = Tela(w, h)
    cy = h / 2.0

    def esa(d):
        return [(g + p, g + d), (w - g - p, g + d), (w - g - d * 1.7, cy),
                (w - g - p, h - g - d), (g + p, h - g - d), (g + d * 1.7, cy)]
    hov = stato == "hover"
    me = m_poly(t, esa(0))
    if hov:
        alone(t, me, ORO_CHIARO, r=g * 1.3, forza=1.25)
    pan = m_poly(t, esa(4.5))
    if hov:
        cel(t, pan, "rosso", ombra=4, luce=2.5, contorno=0, lati=False)
    else:
        cel(t, pan, "lacca", ombra=0, luce=0, contorno=0, a=235)
        colora(t, m_and(pan, m_rect(t, (0, g + 4.5, w, g + 9))), MAT["lacca"][2], 235)
    colora(t, m_sub(m_poly(t, esa(8.5)), m_poly(t, esa(9.5))), ORO_CHIARO if hov else ORO, 170)
    mat = "oro_vivo" if hov else "oro"
    cel(t, m_sub(me, pan), mat, ombra=1.4, luce=1.0, contorno=1.6, lati=False)
    for sx, x in ((1, g + p + 8), (-1, w - g - p - 8)):
        gemma(t, x, cy, 5 if hov else 4, "rubino" if hov else "lacca_rossa", mat, taglio="rombo")
        for k in (1, -1):
            cel(t, m_ell(t, x + sx * 12, cy + k * 7, 1.8), mat, ombra=0.5, luce=0, contorno=0.9)
        cel(t, m_ell(t, x + sx * 16, cy, 2.2), mat, ombra=0.5, luce=0, contorno=0.9)
    if hov:
        scintilla(t, g + 6, cy - 10, 10)
        scintilla(t, w - g - 8, cy + 9, 8)
        scintilla(t, g + p + 40, g + 1, 6)
        scintilla(t, w - g - p - 46, g + 1, 7)
    return t


def sigillo(D, stato, tipo):
    """Foreground di radio/check: castone vuoto o gemma (radio); impronta
    vuota o sigillo di ceralacca (check). stato: idle/hover/sel/sel_hover."""
    t = Tela(D, D)
    c = D / 2.0
    pieno = stato.startswith("sel")
    hov = stato.endswith("hover")
    if hov:
        alone(t, m_ell(t, c, c, D * 0.3), ORO_CHIARO, r=6, forza=1.1)
    if tipo == "radio":
        r = D * 0.2
        if pieno:
            gemma(t, c, c, r, "rubino", "oro_vivo" if hov else "oro")
            scintilla(t, c - r * 0.6, c - r * 0.7, D * 0.17)
        else:
            cel(t, m_ell(t, c, c, r + 3.5), "oro_vivo" if hov else "oro", ombra=0.8, luce=0.8, contorno=1.2)
            cel(t, m_ell(t, c, c, r), "lacca", ombra=0, luce=r * 0.4, contorno=0.6)
    else:
        r = D * 0.3
        if pieno:
            pts = []
            for i in range(40):
                a = i * 2 * math.pi / 40
                k = 1 + 0.07 * math.sin(7 * a) + 0.04 * math.sin(3 * a + 1)
                pts.append((c + r * k * math.cos(a), c + 1 + r * k * math.sin(a)))
            cel(t, m_poly(t, pts), "cera", ombra=r * 0.22, luce=r * 0.12, contorno=1.3)
            ri = r * 0.66
            colora(t, m_sub(m_ell(t, c, c + 1, ri), m_ell(t, c, c + 1, ri - 1.1)), MAT["cera"][0])
            cel(t, m_poly(t, [(c, c + 1 - ri * 0.62), (c + ri * 0.48, c + 1), (c, c + 1 + ri * 0.62),
                              (c - ri * 0.48, c + 1)]), "oro_vivo" if hov else "oro",
                ombra=0.7, luce=0.6, contorno=0.8)
            colora(t, m_ell(t, c - r * 0.45, c - r * 0.45, r * 0.18, r * 0.12), MAT["cera"][3])
            if hov:
                scintilla(t, c + r * 0.7, c - r * 0.7, D * 0.17)
        else:
            mk = m_sub(m_ell(t, c, c, r), m_ell(t, c, c, r - 2.2))
            cel(t, mk, "oro_vivo" if hov else "oro", ombra=0.6, luce=0.5, contorno=1.0)
            colora(t, m_ell(t, c, c, r - 2.2), MAT["lacca"][1], 170)
            dm = m_poly(t, [(c, c - 5), (c + 4, c), (c, c + 5), (c - 4, c)])
            colora(t, m_sub(dilata(dm, 0.8), dm), ORO, 170)
    return t.fine()


def binario(w, h, pieno, stato="idle", groove=12):
    """Binario inciso d'oro per slider e barre (orizzontale)."""
    t = Tela(w, h)
    cy = h / 2.0
    x0, x1 = 3, w - 3
    est = m_rect(t, (x0, cy - groove / 2.0 - 2.5, x1, cy + groove / 2.0 + 2.5), groove / 2.0 + 2.5)
    inn = m_rect(t, (x0 + 2.5, cy - groove / 2.0, x1 - 2.5, cy + groove / 2.0), groove / 2.0)
    if stato == "hover":
        alone(t, est, ORO_CHIARO, r=5, forza=0.8)
    cel(t, m_sub(est, inn), "oro_vivo" if stato == "hover" else "oro", ombra=1, luce=0.8,
        contorno=1.3, lati=False)
    if pieno:
        cel(t, inn, "rosso", ombra=groove * 0.3, luce=groove * 0.18, contorno=0, lati=False)
        colora(t, m_and(inn, m_rect(t, (x0 + groove * 0.6, cy - groove * 0.28,
                                        x1 - groove * 0.6, cy - groove * 0.12))),
               MAT["rosso"][3], 170)
    else:
        cel(t, inn, "lacca", ombra=0, luce=0, contorno=0, a=235)
        colora(t, m_and(inn, m_rect(t, (0, cy - groove / 2.0, w, cy - groove / 2.0 + 2.5))),
               (0, 0, 0), 200)
    return t


def ruota(img):
    return img.transpose(Image.ROTATE_90)


def vuota(w, h):
    return Image.new("RGBA", (w, h), (0, 0, 0, 0))


def stile_bottoni():
    B = "button"
    # --- Navigazione (menu principale e di gioco): nastro che si accende.
    NW, NH = 440, 54
    save(vuota(NW, NH), B, "navigation_idle_background.png")
    save(vuota(NW, NH), B, "navigation_insensitive_background.png")
    hov = nastro(NW, NH, "rosso", coda=12, alone_rgb=ORO_CHIARO, scintille=True,
                 mat="oro_vivo").fine()
    save(hov, B, "navigation_hover_background.png")
    save(hov, B, "navigation_selected_hover_background.png")
    save(nastro(NW, NH, "lacca", coda=12, gemme=True, fondo_a=235).fine(), B,
         "navigation_selected_idle_background.png")

    # --- Conferma (si / no): nastro sempre visibile.
    save(nastro(260, 50, "lacca", gemme=True, fondo_a=240).fine(), B, "confirm_idle_background.png")
    save(nastro(260, 50, "rosso", alone_rgb=ORO_CHIARO, scintille=True, mat="oro_vivo",
                gemme=True).fine(), B, "confirm_hover_background.png")

    # --- Bottoni generici (aiuto, test, ecc.): placca.
    save(vuota(120, 48), B, "idle_background.png")
    save(vuota(120, 48), B, "insensitive_background.png")
    gh = placca(120, 48, "lacca_rossa", 245, "oro_vivo", smusso=8, alone_rgb=ORO_CHIARO,
                gemme=False).fine()
    save(gh, B, "hover_background.png")
    save(gh, B, "selected_hover_background.png")
    save(placca(120, 48, "lacca", 220, smusso=8, gemme=False).fine(), B,
         "selected_idle_background.png")

    # --- Pagine dei salvataggi.
    save(vuota(48, 44), B, "page_idle_background.png")
    ph = placca(48, 44, "lacca_rossa", 245, "oro_vivo", g=3, smusso=7, banda=3, gemme=False,
                alone_rgb=ORO_CHIARO, filetto=False).fine()
    save(ph, B, "page_hover_background.png")
    save(ph, B, "page_selected_hover_background.png")
    save(placca(48, 44, "lacca", 235, g=3, smusso=7, banda=3, gemme=False,
                filetto=False).fine(), B, "page_selected_idle_background.png")

    # --- Quick menu: linguetta.
    save(vuota(120, 30), B, "quick_idle_background.png")
    qh = nastro(120, 30, "lacca_rossa", g=3, coda=8, mat="oro_vivo", alone_rgb=ORO_CHIARO).fine()
    save(qh, B, "quick_hover_background.png")
    save(qh, B, "quick_selected_hover_background.png")
    save(nastro(120, 30, "lacca", g=3, coda=8, fondo_a=220).fine(), B,
         "quick_selected_idle_background.png")

    # --- Scelte: cartiglio.
    save(cartiglio(1185, 72, "idle").fine(), B, "choice_idle_background.png")
    save(cartiglio(1185, 72, "hover").fine(), B, "choice_hover_background.png")
    ci = cartiglio(1185, 72, "idle").fine()
    ci.putalpha(ci.split()[3].point(lambda v: v * 120 // 255))
    save(ci, B, "choice_insensitive_background.png")

    # --- Slot di salvataggio.
    save(placca(276, 234, "lacca", 220, smusso=16, banda=4.5, g=3).fine(), B,
         "slot_idle_background.png")
    save(placca(276, 234, "lacca_rossa", 240, "oro_vivo", smusso=16, banda=4.5, g=3,
                alone_rgb=ORO_CHIARO, scintille=True).fine(), B, "slot_hover_background.png")

    # --- Pianificatore (calendario.rpy): placca bassa, altezza variabile.
    save(placca(400, 96, "lacca", 228, smusso=14, banda=4).fine(), B, "piano_idle_background.png")
    save(placca(400, 96, "lacca_rossa", 240, "oro_vivo", smusso=14, banda=4,
                alone_rgb=ORO_CHIARO, scintille=True).fine(), B, "piano_hover_background.png")

    # --- Radio e check (preferenze): sigilli + fascia all'hover.
    vu = vuota(120, 46)
    fascia = placca(120, 46, "lacca_rossa", 200, "oro_vivo", g=3, smusso=6, banda=2.5,
                    gemme=False, filetto=False).fine()
    for k in ("radio", "check"):
        save(vu, B, "%s_idle_background.png" % k)
        save(vu, B, "%s_selected_idle_background.png" % k)
        save(vu, B, "%s_insensitive_background.png" % k)
        save(fascia, B, "%s_hover_background.png" % k)
        save(fascia, B, "%s_selected_hover_background.png" % k)
        save(sigillo(46, "idle", k), B, "%s_foreground.png" % k)
        save(sigillo(46, "hover", k), B, "%s_hover_foreground.png" % k)
        save(sigillo(46, "sel", k), B, "%s_selected_foreground.png" % k)
        save(sigillo(46, "sel_hover", k), B, "%s_selected_hover_foreground.png" % k)


def stile_barre():
    # Slider: binario pieno (sinistra) / vuoto (destra) + gemma come cursore.
    for st in ("idle", "hover"):
        pieno = binario(300, 36, True, st).fine()
        vuoto = binario(300, 36, False, st).fine()
        save(pieno, "slider", "horizontal_%s_pieno.png" % st)
        save(vuoto, "slider", "horizontal_%s_vuoto.png" % st)
        save(vuoto, "slider", "horizontal_%s_bar.png" % st)
        save(ruota(pieno), "slider", "vertical_%s_pieno.png" % st)
        save(ruota(vuoto), "slider", "vertical_%s_vuoto.png" % st)
        save(ruota(vuoto), "slider", "vertical_%s_bar.png" % st)
        t = Tela(36, 36)
        if st == "hover":
            alone(t, m_ell(t, 18, 18, 11), ORO_CHIARO, r=6, forza=1.2)
        gemma(t, 18, 18, 9.5, "rubino", "oro_vivo" if st == "hover" else "oro", taglio="rombo")
        if st == "hover":
            scintilla(t, 12, 10, 7)
        th = t.fine()
        save(th, "slider", "horizontal_%s_thumb.png" % st)
        save(th, "slider", "vertical_%s_thumb.png" % st)

    # Barre generiche.
    save(binario(300, 25, True, groove=9).fine(), "bar", "left.png")
    save(binario(300, 25, False, groove=9).fine(), "bar", "right.png")
    save(ruota(binario(300, 25, False, groove=9).fine()), "bar", "top.png")
    save(ruota(binario(300, 25, True, groove=9).fine()), "bar", "bottom.png")

    # Scrollbar: scanalatura scura bordata d'oro, cursore a bacchetta d'oro.
    for st in ("idle", "hover"):
        L, W = 240, 18
        t = Tela(L, W)
        est = m_rect(t, (2, 3, L - 2, W - 3), 6)
        inn = m_rect(t, (4, 5, L - 4, W - 5), 4)
        cel(t, m_sub(est, inn), "oro", ombra=0.6, luce=0.5, contorno=1.0, lati=False)
        cel(t, inn, "lacca", ombra=0, luce=0, contorno=0, a=210)
        bar = t.fine()
        t = Tela(L, W)
        mk = m_rect(t, (3, 3.5, L - 3, W - 3.5), 5.5)
        if st == "hover":
            alone(t, mk, ORO_CHIARO, r=3, forza=1.0)
        cel(t, mk, "oro_vivo" if st == "hover" else "oro", ombra=2.2, luce=1.6, contorno=1.3,
            lati=False)
        colora(t, m_rect(t, (10, 6.5, L - 10, 7.8)), MAT["oro"][3], 220)
        thumb = t.fine()
        save(bar, "scrollbar", "horizontal_%s_bar.png" % st)
        save(thumb, "scrollbar", "horizontal_%s_thumb.png" % st)
        save(ruota(bar), "scrollbar", "vertical_%s_bar.png" % st)
        save(ruota(thumb), "scrollbar", "vertical_%s_thumb.png" % st)


def _scudo(cx, y0, w, h):
    """Contorno di uno scudo araldico (lati dritti, punta in basso)."""
    dx = [(cx, y0), (cx + w / 2.0, y0), (cx + w / 2.0, y0 + h * 0.5)]
    for i in range(1, 12):
        a = i / 12.0 * math.pi / 2
        dx.append((cx + w / 2.0 * math.cos(a), y0 + h * 0.5 + h * 0.5 * math.sin(a)))
    dx.append((cx, y0 + h))
    return dx + [(2 * cx - x, y) for x, y in dx[1:-1][::-1]]


def stemma(t, cx, cy, s=1.0):
    """Stemma araldico Dignitas: scudo rosso bordato d'oro, losanga di
    rubino, corona a tre punte."""
    w, h = 40 * s, 48 * s
    y0 = cy - h / 2 + 4 * s
    cel(t, m_poly(t, _scudo(cx, y0, w, h)), "oro", ombra=1.4, luce=1.2, contorno=1.6)
    k = 3.5 * s
    cel(t, m_poly(t, _scudo(cx, y0 + k, w - 2 * k, h - 2.2 * k)), "rosso", ombra=4 * s,
        luce=2 * s, contorno=0)
    gemma(t, cx, y0 + h * 0.44, 7 * s, "rubino", "oro", taglio="rombo")
    cy0 = y0 - 1 * s
    cr = [(cx - 15 * s, cy0), (cx - 16 * s, cy0 - 9 * s), (cx - 8 * s, cy0 - 4 * s), (cx, cy0 - 13 * s),
          (cx + 8 * s, cy0 - 4 * s), (cx + 16 * s, cy0 - 9 * s), (cx + 15 * s, cy0)]
    cel(t, m_poly(t, cr), "oro", ombra=1.2, luce=1.0, contorno=1.4)
    for px, py in ((cx - 16 * s, cy0 - 9 * s), (cx, cy0 - 13 * s), (cx + 16 * s, cy0 - 9 * s)):
        cel(t, m_ell(t, px, py, 2.2 * s), "oro_vivo", ombra=0.5, luce=0, contorno=1.0)
    scintilla(t, cx + 12 * s, y0 + 6 * s, 7 * s)


def girali(t, cx, cy, verso, L=110, mat="oro"):
    """Fregio orizzontale di foglie d'acanto che parte dallo stemma."""
    foglia(t, cx, cy, verso, 0, L * 0.55, 4.5, mat)
    foglia(t, cx + verso * L * 0.4, cy - 2, verso, -0.25, L * 0.4, 3.6, mat)
    foglia(t, cx + verso * L * 0.4, cy + 2, verso, 0.25, L * 0.4, 3.6, mat)
    cel(t, m_ell(t, cx + verso * (L * 0.62), cy, 2.6), mat, ombra=0.6, luce=0.5, contorno=1.0)
    cel(t, m_ell(t, cx + verso * (L * 0.85), cy - 6, 1.9), mat, ombra=0.5, luce=0, contorno=0.9)
    cel(t, m_ell(t, cx + verso * (L * 0.85), cy + 6, 1.9), mat, ombra=0.5, luce=0, contorno=0.9)


def stile_cornici():
    # Cornice generica (pannelli, conferme, pianificatore): Frame 60,60.
    save(cornice(360, 360, ang=44).fine(), "frame.png")

    # Cornice piccola (notify, feedback, pallini, fumetti): Frame 26,26.
    def piccola(w, h, a=232):
        return cornice(w, h, ang=18, banda=5, m=3, raggio=7, fondo_a=a, filetti=False).fine()
    save(piccola(160, 160), "frame_piccolo.png")
    save(piccola(300, 64, 228), "notify.png")
    save(piccola(300, 64, 228), "skip.png")

    # Textbox: cornice grande + stemma al centro del bordo superiore.
    tb = Tela(1920, 277)
    cornice(1840, 249, ang=50, banda=9, fondo_a=226, tela=tb, off=(40, 14))
    for v in (-1, 1):
        girali(tb, 960 + v * 26, 22.5, v, L=150)
    stemma(tb, 960, 26, 0.85)
    save(tb.fine(), "textbox.png")

    # Namebox: placca laccata con puntali dorati (Frame 34,10).
    t = Tela(240, 60)
    x0, x1, y0, y1, p = 4, 236, 6, 54, 14
    cy = 30

    def tar(d):
        return [(x0 + p, y0 + d), (x1 - p, y0 + d), (x1 - d * 1.6, cy), (x1 - p, y1 - d),
                (x0 + p, y1 - d), (x0 + d * 1.6, cy)]
    me, pan = m_poly(t, tar(0)), m_poly(t, tar(4))
    cel(t, pan, "lacca", ombra=0, luce=0, contorno=0, a=245)
    colora(t, m_and(pan, m_rect(t, (0, y0 + 4, 240, y0 + 8))), MAT["lacca"][2], 245)
    colora(t, m_sub(m_poly(t, tar(7)), m_poly(t, tar(8))), ORO, 140)
    cel(t, m_sub(me, pan), "oro", ombra=1.3, luce=1.0, contorno=1.5, lati=False)
    for x in (x0 + 5, x1 - 5):
        gemma(t, x, cy, 3.2, "rubino", "oro", taglio="rombo")
    save(t.fine(), "namebox.png")

    # Divisore del pianificatore.
    t = Tela(440, 30)
    for v in (-1, 1):
        colora(t, m_poly(t, [(220 + v * 14, 13.2), (220 + v * 200, 14.6), (220 + v * 200, 15.4),
                             (220 + v * 14, 16.8)]), INK)
        cel(t, m_poly(t, [(220 + v * 14, 14), (220 + v * 196, 15), (220 + v * 14, 16)]),
            "oro", ombra=0, luce=0, contorno=0)
        foglia(t, 220 + v * 14, 15, v, 0, 46, 3.6)
        cel(t, m_ell(t, 220 + v * 204, 15, 2.4), "oro", ombra=0.6, luce=0.5, contorno=1.0)
    gemma(t, 220, 15, 5.5, "rubino", "oro", taglio="rombo")
    scintilla(t, 226, 8, 6)
    save(t.fine(), "divisore.png")

    # Indicatore click-to-continue: losanga di rubino con scintilla.
    t = Tela(26, 26)
    gemma(t, 13, 14, 7, "rubino", "oro", taglio="rombo")
    scintilla(t, 9, 7, 5)
    save(t.fine(), "ctc.png")


def pergamena(w, h):
    """Pergamena miniata: rotoli cel-shaded, doppio filetto rosso e oro,
    losanghe agli angoli."""
    t = Tela(w, h)
    rw = 30
    body = (rw - 8, 9, w - rw + 8, h - 9)
    mk = m_rect(t, body, 6)
    colora(t, _sposta(mk, _s(5), _s(6)), (20, 10, 8), 110)
    cel(t, mk, "pergamena", ombra=6, luce=3, contorno=1.6, lati=False)
    for d_, rgb, wd in ((12, ROSSO, 2.2), (17, ORO, 1.4)):
        b1 = (body[0] + d_, body[1] + d_ - 4, body[2] - d_, body[3] - d_ + 4)
        b2 = (b1[0] + wd, b1[1] + wd, b1[2] - wd, b1[3] - wd)
        colora(t, m_sub(m_rect(t, b1, 3), m_rect(t, b2, 2)), rgb)
    for sx, sy, px, py in ((1, 1, body[0] + 12, body[1] + 8), (-1, 1, body[2] - 12, body[1] + 8),
                           (1, -1, body[0] + 12, body[3] - 8), (-1, -1, body[2] - 12, body[3] - 8)):
        # fioroni d'angolo miniati: due foglie d'oro e una losanga di rubino
        foglia(t, px + sx * 7, py + sy * 8.5, sx, 0, 22, 2.8)
        foglia(t, px + sx * 9.5, py + sy * 7, 0, sy, 14, 2.6)
        gemma(t, px + sx * 9, py + sy * 9, 3.2, "rubino", "oro", taglio="rombo", luce=False)
    for cx in (rw / 2.0 + 2, w - rw / 2.0 - 2):
        rm = m_rect(t, (cx - rw / 2.0, 1, cx + rw / 2.0, h - 1), rw / 2.0)
        cel(t, rm, "rotolo", ombra=rw * 0.28, luce=rw * 0.16, contorno=1.6)
        colora(t, m_rect(t, (cx - 3, 8, cx + 3, h - 8), 3), MAT["rotolo"][3], 230)
        colora(t, m_rect(t, (cx - rw / 2.0 + 2, h / 2.0 - 0.7, cx + rw / 2.0 - 2, h / 2.0 + 0.7)),
               MAT["rotolo"][0], 160)
    return t


def stile_menu():
    """Pannello del menu principale, pattern, cartello, comandi carosello."""
    f = menu_front()
    save(f, "mm_front.png")
    mm = pattern((1920, 1080))
    mm.alpha_composite(f)
    save(mm.convert("RGB"), "main_menu.png")
    save(pattern((1540, 1540)).convert("RGB"), "mm_pattern.png")
    gm = pattern((1920, 1080))
    gm.alpha_composite(Image.new("RGBA", gm.size, (0, 0, 0, 110)))
    save(gm.convert("RGB"), "game_menu.png")
    cartello_data()

    stile_carosello()


def stile_carosello():
    """Frecce del carosello (medaglione d'oro con chevron) e pallini
    (castoni vuoti / rubino)."""
    D = 76
    c = D / 2.0
    for verso, nome in ((-1, "sx"), (1, "dx")):
        for hov in (False, True):
            t = Tela(D, D)
            mat = "oro_vivo" if hov else "oro"
            if hov:
                alone(t, m_ell(t, c, c, 30), ORO_CHIARO, r=8, forza=1.2)
            cel(t, m_sub(m_ell(t, c, c, 31), m_ell(t, c, c, 25)), mat, ombra=1.6, luce=1.2,
                contorno=1.6)
            cel(t, m_ell(t, c, c, 25), "lacca_rossa" if hov else "lacca", ombra=0, luce=5,
                contorno=0, a=235)
            colora(t, m_sub(m_ell(t, c, c, 21), m_ell(t, c, c, 20)), ORO, 150)
            a = 11
            pts = [(c - verso * a * 0.45, c - a), (c + verso * a * 0.55, c),
                   (c - verso * a * 0.45, c + a)]
            cel(t, m_linea(t, pts, 6), mat, ombra=1.2, luce=0.8, contorno=1.3)
            for i in range(4):
                ang_ = i * math.pi / 2 + math.pi / 4
                cel(t, m_ell(t, c + 28 * math.cos(ang_), c + 28 * math.sin(ang_), 2.1), mat,
                    ombra=0.5, luce=0, contorno=0.9)
            if hov:
                scintilla(t, c - 16, c - 20, 9)
            save(t.fine(), "mm_freccia_%s%s.png" % (nome, "_hover" if hov else ""))
    for nome, pieno in (("mm_punto.png", False), ("mm_punto_on.png", True)):
        t = Tela(22, 22)
        if pieno:
            gemma(t, 11, 11, 5.5, "rubino", "oro_vivo", taglio="rombo")
        else:
            gemma(t, 11, 11, 4, "lacca", "oro", taglio="rombo", luce=False)
        save(t.fine(), nome)


def stile_ritratti():
    portrait("aede neutra.webp", "portrait_aede.png", top_f=0.0, side_f=0.45, cx_f=0.43)
    portrait("caino neutro.webp", "portrait_caino.png", top_f=0.0, side_f=0.42, cx_f=0.52)
    portrait("ofelia neutra.png", "portrait_ofelia.png", top_f=0.0, side_f=0.40, cx_f=0.45)
    portrait("icaro neutro.png", "portrait_icaro.png", top_f=0.15, side_f=0.42, cx_f=0.6)
    portrait("druso neutro.png", "portrait_druso.png", top_f=0.0, side_f=0.40, cx_f=0.5)
    portrait("briseide neutra.png", "portrait_briseide.png", top_f=0.0, side_f=0.36, cx_f=0.5)
    portrait("vanna neutra.png", "portrait_vanna.png", top_f=0.0, side_f=0.36, cx_f=0.5)
    portrait("corrado neutro.png", "portrait_corrado.png", top_f=0.0, side_f=0.36, cx_f=0.5)
    portrait_diamond("portrait_locked.png", (90, 30, 26, 255), (120, 100, 48, 255))


def rigenera_stile():
    """Tutta la GUI in stile miniato (bottoni, barre, cornici, menu,
    ritratti). Non tocca sprite del cast, clessidra, lune e maschera."""
    stile_bottoni()
    stile_barre()
    stile_cornici()
    stile_menu()
    stile_ritratti()


def rigenera_pianificatore():
    """Solo gli asset nuovi del Blocco P (clessidra, fasi lunari)."""
    clessidra()
    lune()


def rigenera_gioco():
    """Solo gli asset nuovi del Blocco G (cartello data, maschera)."""
    cartello_data()
    maschera_diagonale()


def rigenera_menu():
    """Solo gli asset del menu principale (pannello, cast, neve)."""
    front = menu_front()
    mm = pattern((1920, 1080))
    mm.alpha_composite(front)
    save(mm.convert("RGB"), "main_menu.png")
    save(front, "mm_front.png")
    menu_cast()
    fiocco()


# =============================================================================
# Blocco D: sigilli del menu rapido, particelle degli effetti di scena, segno
# discreto delle scelte gia' fatte. Uso: rigenera_blocco_d().
# =============================================================================

QUICK_D = 60          # lato dei sigilli del menu rapido
QUICK_AZIONI = ("indietro", "memorie", "salta", "auto", "salva",
                "qsalva", "qcarica", "costumanze", "borsa")


def _mandorla(t, x0, y0, dx, dy, L, wmax, coda=0.35):
    """Maschera a mandorla (penna, foglia) da (x0,y0) lungo (dx,dy)."""
    n_ = math.hypot(dx, dy)
    dx, dy = dx / n_, dy / n_
    nx, ny = -dy, dx
    sup, inf = [], []
    for i in range(17):
        u = i / 16.0
        hw = wmax * (math.sin(math.pi * u) ** 0.7) * (1 - coda * (1 - u))
        x, y = x0 + dx * L * u, y0 + dy * L * u
        sup.append((x + nx * hw, y + ny * hw))
        inf.append((x - nx * hw, y - ny * hw))
    return m_poly(t, sup + inf[::-1])


def _glifo(t, azione, c, s):
    """Maschera del glifo inciso nel sigillo (centro c, semi-lato s)."""
    if azione == "indietro":
        w = s * 0.26
        pts = [(c - s * 0.35, c - s * 0.32), (c + s * 0.15, c - s * 0.32)]
        cx, cy, r = c + s * 0.15, c + s * 0.14, s * 0.46
        for i in range(1, 13):
            a = -math.pi / 2 + math.pi * i / 12.0
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        pts.append((c - s * 0.45, c + s * 0.6))
        mk = m_linea(t, pts, w)
        return m_add(mk, m_poly(t, [(c - s * 0.98, c - s * 0.32), (c - s * 0.3, c - s * 0.8),
                                    (c - s * 0.3, c + s * 0.16)]))
    if azione == "memorie":
        sx = s * 0.08
        sin_ = m_poly(t, [(c - sx, c - s * 0.5), (c - s * 0.95, c - s * 0.7),
                          (c - s * 0.95, c + s * 0.5), (c - sx, c + s * 0.7)])
        des = m_poly(t, [(c + sx, c - s * 0.5), (c + s * 0.95, c - s * 0.7),
                         (c + s * 0.95, c + s * 0.5), (c + sx, c + s * 0.7)])
        mk = m_add(sin_, des)
        # righe di scrittura incise
        for k in (-0.25, 0.05, 0.35):
            for v in (-1, 1):
                mk = m_sub(mk, m_linea(t, [(c + v * s * 0.25, c + s * k - s * 0.04 * 0),
                                           (c + v * s * 0.75, c + s * (k - 0.08))], 0.9))
        return mk
    if azione == "salta":
        a = m_poly(t, [(c - s * 0.95, c - s * 0.62), (c - s * 0.02, c), (c - s * 0.95, c + s * 0.62)])
        b = m_poly(t, [(c - s * 0.05, c - s * 0.62), (c + s * 0.9, c), (c - s * 0.05, c + s * 0.62)])
        return m_add(a, b)
    if azione == "auto":
        anello = m_sub(m_ell(t, c, c, s * 0.98), m_ell(t, c, c, s * 0.76))
        tri = m_poly(t, [(c - s * 0.3, c - s * 0.45), (c + s * 0.5, c), (c - s * 0.3, c + s * 0.45)])
        return m_add(anello, tri)
    if azione == "salva":
        penna = _mandorla(t, c - s * 0.72, c + s * 0.72, 1, -1, s * 2.1, s * 0.34)
        rachide = m_linea(t, [(c - s * 0.7, c + s * 0.7), (c + s * 0.55, c - s * 0.55)], 0.8)
        mk = m_sub(penna, rachide)
        return m_add(mk, m_linea(t, [(c - s * 0.95, c + s * 0.92), (c - s * 0.2, c + s * 0.92)],
                                 s * 0.14))
    if azione in ("qsalva", "qcarica"):
        vas = m_rect(t, (c - s * 0.85, c + s * 0.6, c + s * 0.85, c + s * 0.86), s * 0.08)
        vas = m_add(vas, m_rect(t, (c - s * 0.85, c + s * 0.25, c - s * 0.62, c + s * 0.86)),
                    m_rect(t, (c + s * 0.62, c + s * 0.25, c + s * 0.85, c + s * 0.86)))
        if azione == "qsalva":
            fr = m_add(m_rect(t, (c - s * 0.15, c - s * 0.95, c + s * 0.15, c - s * 0.1)),
                       m_poly(t, [(c - s * 0.5, c - s * 0.12), (c + s * 0.5, c - s * 0.12),
                                  (c, c + s * 0.42)]))
        else:
            fr = m_add(m_rect(t, (c - s * 0.15, c - s * 0.35, c + s * 0.15, c + s * 0.42)),
                       m_poly(t, [(c - s * 0.5, c - s * 0.33), (c + s * 0.5, c - s * 0.33),
                                  (c, c - s * 0.95)]))
        return m_add(vas, fr)
    if azione == "costumanze":
        pts = []
        n = 8
        for i in range(n * 4):
            a = i * 2 * math.pi / (n * 4) + math.pi / (n * 4)
            r = s * (0.95 if (i % 4) in (1, 2) else 0.68)
            pts.append((c + r * math.cos(a), c + r * math.sin(a)))
        return m_sub(m_poly(t, pts), m_ell(t, c, c, s * 0.3))
    if azione == "borsa":
        # Borsa di cuoio legata al collo, con uno Scudo inciso sul ventre.
        corpo = m_ell(t, c, c + s * 0.3, s * 0.8, s * 0.62)
        collo = m_rect(t, (c - s * 0.26, c - s * 0.46, c + s * 0.26, c - s * 0.2))
        bocca = m_poly(t, [(c - s * 0.62, c - s * 0.95), (c + s * 0.62, c - s * 0.95),
                           (c + s * 0.26, c - s * 0.44), (c - s * 0.26, c - s * 0.44)])
        mk = m_add(corpo, collo, bocca)
        mk = m_sub(mk, m_linea(t, [(c - s * 0.4, c - s * 0.3), (c + s * 0.4, c - s * 0.3)], 1.2))
        moneta = m_sub(m_ell(t, c, c + s * 0.34, s * 0.32), m_ell(t, c, c + s * 0.34, s * 0.2))
        return m_sub(mk, moneta)
    raise ValueError(azione)


def sigillo_quick(azione, stato):
    """Sigillo di ceralacca con glifo d'oro. stato: idle / hover / selected
    (azione attiva: Salta, Auto) / insensitive."""
    D = QUICK_D
    t = Tela(D, D)
    c = D / 2.0
    r = D * 0.4
    hov = stato == "hover"
    sel = stato == "selected"
    pts = []
    for i in range(48):
        a = i * 2 * math.pi / 48
        k = 1 + 0.05 * math.sin(7 * a + 0.4) + 0.03 * math.sin(3 * a + 1.3)
        pts.append((c + r * k * math.cos(a), c + 0.5 + r * k * math.sin(a)))
    corpo = m_poly(t, pts)
    if hov or sel:
        alone(t, corpo, ORO_CHIARO, r=7 if hov else 5, forza=1.25 if hov else 0.8)
    cel(t, corpo, "cera" if (hov or sel) else "lacca_rossa", ombra=r * 0.16,
        luce=r * 0.08, contorno=1.4)
    # impronta: filo d'oro interno
    ri = r * 0.8
    mat = "oro_vivo" if (hov or sel) else "oro"
    colora(t, m_sub(m_ell(t, c, c + 0.5, ri), m_ell(t, c, c + 0.5, ri - 1.2)), MAT[mat][1], 210)
    cel(t, _glifo(t, azione, c, r * 0.56), mat, ombra=0.9, luce=0.6, contorno=1.0)
    colora(t, m_ell(t, c - r * 0.5, c - r * 0.55, r * 0.16, r * 0.1), MAT["cera"][3], 200)
    if hov:
        scintilla(t, c + r * 0.72, c - r * 0.7, 7)
    img = t.fine()
    if stato == "insensitive":
        g = img.convert("LA").convert("RGBA")
        g.putalpha(img.split()[3].point(lambda v: v * 110 // 255))
        img = g
    return img


def sigilli_quick():
    os.makedirs(os.path.join(GUI, "quick"), exist_ok=True)
    for az in QUICK_AZIONI:
        idle = sigillo_quick(az, "idle")
        hov = sigillo_quick(az, "hover")
        save(idle, "quick", "%s_idle.png" % az)
        save(hov, "quick", "%s_hover.png" % az)
        save(sigillo_quick(az, "selected"), "quick", "%s_selected_idle.png" % az)
        save(hov, "quick", "%s_selected_hover.png" % az)
        save(sigillo_quick(az, "insensitive"), "quick", "%s_insensitive.png" % az)


def borsa_hud():
    """Moneta dello Scudo e fondo della borsa a schermo (game/borsa.rpy):
    leggeri, senza cornice miniata."""
    D = 44
    t = Tela(D, D)
    c = D / 2.0
    disco = m_ell(t, c, c, D * 0.42)
    cel(t, disco, "oro", ombra=1.6, luce=1.2, contorno=1.2)
    colora(t, m_sub(m_ell(t, c, c, D * 0.33), m_ell(t, c, c, D * 0.3)), MAT["oro"][0], 200)
    rombo = m_poly(t, [(c, c - D * 0.17), (c + D * 0.12, c), (c, c + D * 0.17), (c - D * 0.12, c)])
    cel(t, rombo, "rosso", ombra=0.8, luce=0.6, contorno=0.8)
    save(t.fine(), "scudo.png")
    # Pillola scura semitrasparente, angoli tondi: si usa come Frame.
    pil = Image.new("RGBA", (64, 44), (0, 0, 0, 0))
    ImageDraw.Draw(pil).rounded_rectangle([0, 0, 63, 43], radius=21,
                                          fill=(16, 10, 10, 150),
                                          outline=ORO + (90,), width=1)
    save(pil, "borsa_pillola.png")


def particelle_effetti():
    """Particelle degli effetti di scena (game/effetti.rpy)."""
    # Lanterna di carta che sale: alone caldo, corpo arancio, cappelli scuri.
    W, H = 44, 60
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(glow).ellipse([6, 10, 38, 50], fill=150)
    glow = glow.filter(ImageFilter.GaussianBlur(7))
    lay = Image.new("RGBA", (W, H), (255, 170, 70, 0))
    lay.putalpha(glow)
    img.alpha_composite(lay)
    corpo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(corpo)
    d.rounded_rectangle([14, 19, 30, 43], 6, fill=(246, 150, 64, 255))
    d.rounded_rectangle([17, 22, 27, 40], 4, fill=(255, 214, 128, 255))
    d.ellipse([19, 26, 25, 36], fill=(255, 246, 210, 255))
    d.rectangle([15, 17, 29, 19], fill=ROSSO_SCURO + (255,))
    d.rectangle([15, 43, 29, 45], fill=ROSSO_SCURO + (255,))
    img.alpha_composite(corpo.filter(ImageFilter.GaussianBlur(0.6)))
    save(img, "fx_lanterna.png")

    # Fumo: nuvola grigia molto morbida.
    W, H = 220, 150
    m = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(m)
    for (x, y, rx, ry, a) in ((80, 82, 60, 40, 120), (130, 70, 55, 38, 110),
                              (110, 95, 70, 34, 90), (60, 64, 34, 24, 70)):
        d.ellipse([x - rx, y - ry, x + rx, y + ry], fill=a)
    m = m.filter(ImageFilter.GaussianBlur(18))
    fumo = Image.new("RGBA", (W, H), (206, 198, 186, 0))
    fumo.putalpha(m)
    save(fumo, "fx_fumo.png")

    # Polvere dorata: scintilla minuscola.
    t = Tela(22, 22)
    scintilla(t, 11, 11, 8)
    save(t.fine(), "fx_polvere.png")


def segno_scelta():
    """Segno discreto delle scelte gia' fatte: una fogliolina d'oro."""
    t = Tela(24, 24)
    cel(t, _mandorla(t, 5, 19, 1, -1, 20, 4.4, coda=0.2), "oro", ombra=0.8, luce=0.6,
        contorno=1.0)
    colora(t, m_linea(t, [(6, 18), (17, 7)], 0.6), MAT["oro"][0])
    save(t.fine(), "scelta_vista.png")


def rigenera_blocco_d():
    """Solo gli asset nuovi del Blocco D (menu rapido, effetti, scelte)."""
    sigilli_quick()
    particelle_effetti()
    segno_scelta()


def bagliore_scelta():
    """Alone oro morbido dietro la scelta in hover (1185x72 + margine)."""
    W, H = 1265, 132
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).rounded_rectangle([60, 40, W - 60, H - 40], 26, fill=120)
    m = m.filter(ImageFilter.GaussianBlur(16))
    img = Image.new("RGBA", (W, H), ORO_CHIARO + (0,))
    img.putalpha(m)
    save(img, "scelta_bagliore.png")


def ceralacca():
    """Sigillo di ceralacca del cartello del giorno: rosso nei giorni di
    festa, bruno scuro negli altri."""
    rosso = sigillo(180, "sel", "check")
    save(rosso, "ceralacca_festa.png")
    scuro = ImageChops.multiply(rosso, Image.new("RGBA", rosso.size, (120, 84, 64, 255)))
    save(scuro, "ceralacca.png")


def scudo_luccichio():
    """Riflesso diagonale che passa sullo scudo della Borsa (44x44)."""
    W = H = 44
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).polygon([(14, 0), (24, 0), (10, H), (0, H)], fill=230)
    m = m.filter(ImageFilter.GaussianBlur(2.5))
    img = Image.new("RGBA", (W, H), (255, 252, 236, 0))
    img.putalpha(m)
    save(img, "scudo_luccichio.png")


def particelle_extra():
    """Braci e gocce di pioggia (game/effetti.rpy)."""
    # Brace: puntino arancio con alone.
    W = H = 18
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).ellipse([5, 5, 13, 13], fill=255)
    m = m.filter(ImageFilter.GaussianBlur(2.2))
    img = Image.new("RGBA", (W, H), (255, 150, 60, 0))
    img.putalpha(m)
    nucleo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(nucleo).ellipse([7, 7, 11, 11], fill=(255, 226, 150, 255))
    img.alpha_composite(nucleo.filter(ImageFilter.GaussianBlur(0.6)))
    save(img, "fx_brace.png")

    # Goccia: riga sottile e chiara, leggermente obliqua (la direzione la da'
    # la velocita' nella screen).
    W, H = 8, 54
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).line([(5, 0), (3, H - 1)], fill=230, width=3)
    m = m.filter(ImageFilter.GaussianBlur(0.7))
    img = Image.new("RGBA", (W, H), (200, 214, 236, 0))
    img.putalpha(m)
    save(img, "fx_goccia.png")


def rigenera_blocco_g():
    """Solo gli asset nuovi del pacchetto grafico (scelte, cartello, Borsa,
    particelle)."""
    bagliore_scelta()
    ceralacca()
    scudo_luccichio()
    particelle_extra()


def main():
    # Menu principale: pattern + fronte. main_menu.png resta per compatibilita';
    # la screen anima mm_pattern.png (tile 1540: periodo comune di righe 140
    # e pois 110/220, quindi senza giunte) sotto mm_front.png.
    rigenera_menu()
    rigenera_gioco()
    rigenera_pianificatore()

    # Overlay.
    save(Image.new("RGBA", (1920, 1080), (0, 0, 0, 0)), "overlay", "main_menu.png")
    save(Image.new("RGBA", (1920, 1080), (16, 10, 10, 175)), "overlay", "game_menu.png")
    save(Image.new("RGBA", (1920, 1080), (16, 10, 10, 195)), "overlay", "confirm.png")

    # Icona finestra: tondo nero, doppio bordo oro, diamante.
    ic = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    d = ImageDraw.Draw(ic)
    d.ellipse([8, 8, 248, 248], fill=NERO + (255,), outline=ORO + (255,), width=10)
    d.ellipse([26, 26, 230, 230], outline=ORO + (140,), width=3)
    diamond(d, 128, 128, 54, ROSSO + (255,))
    diamond(d, 128, 128, 30, ORO + (255,))
    save(ic, "window_icon.png")

    # Bottoni, barre, cornici, textbox, ritratti: stile miniato.
    rigenera_stile()

    # Pacchetto grafico: scelte, cartello, Borsa, particelle.
    rigenera_blocco_g()

    print("GUI Dignitas generata in", GUI)


if __name__ == "__main__":
    main()
