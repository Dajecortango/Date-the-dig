"""Verifica le regole pure del pacchetto grafico (game/regia_logic.py) e gli
agganci nei file .rpy (luce, regia, menu, route).

Uso: py -3 -I tests/test_regia.py
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.join(HERE, "..", "game")
# Cartella del capitolo Malandrini, relativa a GAME.
MAL_REL = os.path.join("capitoli", "malandrini")
sys.path.insert(0, HERE)
from percorsi import prepara_import  # noqa: E402
prepara_import()

import regia_logic as rl  # noqa: E402
import regia_tabelle as tab  # noqa: E402

FAILURES = []


def check(nome, got, atteso):
    ok = got == atteso
    if not ok:
        FAILURES.append(nome)
    print(f"{'PASS' if ok else 'FAIL'}: {nome}: {got!r} (atteso {atteso!r})")


def leggi(rel):
    with open(os.path.join(GAME, rel), encoding="utf-8") as f:
        return f.read()


FINALI_FINTI = [
    ("good_end", "T", "Aede", ""),
    ("druso_neutral", "T", "Druso", ""),
    ("caino_good_end", "T", "Caino", ""),
    ("finale_neutro_semestre", "T", "Semestre", ""),
]


def test_tinte():
    check("tinta neve", rl.tinta_per("esterno_neve", "mattina", tab), "#9fb8ff")
    check("tinta vicoli sera", rl.tinta_per("vicoli_zefiro", "sera", tab), "#5a6fa8")
    check("tinta vicoli mattina", rl.tinta_per("vicoli_zefiro", "mattina", tab), None)
    check("tinta sconosciuto", rl.tinta_per("palestra", "sera", tab), None)
    check("tinta None", rl.tinta_per(None, None, tab), None)
    check("tinta senza tabelle", rl.tinta_per("vicoli_zefiro", "sera", None), None)
    check("forza", rl.TINTA_FORZA, 0.18)


def test_oscurato():
    check("ascoltatore", rl.oscurato("caino", "aede", ["aede", "caino"]), True)
    check("parlante", rl.oscurato("aede", "aede", ["aede", "caino"]), False)
    check("narratore", rl.oscurato("caino", None, ["aede", "caino"]), False)
    check("uno solo", rl.oscurato("caino", "aede", ["caino"]), False)
    check("parlante fuori scena", rl.oscurato("caino", "glauco", ["aede", "caino"]), False)
    check("luce", rl.LUCE_OSCURATA, 0.75)


def test_movimenti():
    check("prima entrata", rl.movimento_per(None, "sorpresa"), None)
    check("stessa", rl.movimento_per("neutra", "neutra"), None)
    check("sorpresa", rl.movimento_per("neutra", "sorpresa"), "sobbalzo")
    check("sorpreso", rl.movimento_per("neutro", "sorpreso"), "sobbalzo")
    check("imbarazzato", rl.movimento_per("neutro", "imbarazzato"), "arretra")
    check("furioso", rl.movimento_per("freddo", "furioso"), "trema")
    check("irritata", rl.movimento_per("neutra", "irritata"), "avanza")
    check("sorriso", rl.movimento_per("neutra", "sorriso"), None)
    check("pausa", rl.MOVIMENTO_PAUSA, 3)


def test_pioggia():
    n = sum(rl.piove(l, g) for l in range(1, 7) for g in range(1, 31))
    check("pioggia ~1/3", 50 <= n <= 70, True)
    check("deterministica", rl.piove(2, 5), rl.piove(2, 5))


def test_transizioni():
    check("nero resta", rl.transizione_scene("palestra", "nero", "fade"), None)
    check("primo -> stacco", rl.transizione_scene(None, "palestra", "fade"), "stacco")
    check("diverso -> stacco", rl.transizione_scene("a", "b", "dissolve"), "stacco")
    check("stesso -> salto", rl.transizione_scene("palestra", "palestra", "dissolve"), "salto_tempo")
    check("lampo resta", rl.transizione_scene("a", "b", "lampo"), None)


def test_fondo_menu():
    fm = rl.fondo_menu
    check("neutro route", fm("druso_neutral", FINALI_FINTI, tab), ("palestra", "druso"))
    check("caino", fm("caino_good_end", FINALI_FINTI, tab), ("corridoio_ceppo", "caino"))
    check("semestre", fm("finale_neutro_semestre", FINALI_FINTI, tab), ("esterno_neve", None))
    check("nessuno", fm(None, FINALI_FINTI, tab), (None, None))
    check("ignoto", fm("boh", FINALI_FINTI, tab), (None, None))
    check("fondo senza tabelle", fm("druso_neutral", FINALI_FINTI, None), (None, None))
    check("semestre senza tabelle", fm("finale_neutro_semestre", FINALI_FINTI, None), (None, None))


def test_conteggio():
    check("inizio", rl.conteggio(3, 8, 0.0), 3)
    check("fine", rl.conteggio(3, 8, 0.6), 8)
    check("oltre", rl.conteggio(3, 8, 5.0), 8)
    m = rl.conteggio(8, 3, 0.3)
    check("meta' in discesa", 3 < m < 8, True)


def check_luce():
    try:
        luce = leggi("luce.rpy")
    except OSError:
        luce = ""
    for pezzo in ("get_say_image_tag", "NoRollback", "after_load_callbacks",
                  "rgl.tinta_per", "rgl.oscurato", "rgl.movimento_per"):
        check("luce.rpy usa " + pezzo, pezzo in luce, True)
    aede = leggi(os.path.join(MAL_REL, "routes", "aede_core.rpy"))
    check("glauco ha image=",
          bool(re.search(r'Character\("Glauco Severo"[^)]*image="glauco"', aede)), True)
    regia = leggi("regia.rpy")
    for t in ("sobbalzo", "arretra", "avanza", "trema"):
        check("regia transform " + t,
              bool(re.search(r"^transform %s\b" % t, regia, re.M)), True)


def check_textbox():
    regia = leggi("regia.rpy")
    screens = leggi("screens.rpy")
    check("pensiero definito",
          bool(re.search(r"define pensiero = Character\(None,[^)]*what_italic=True", regia)), True)
    check("ctc nestled", 'ctc_position="nestled"' in regia, True)
    check("ctc fisso rimosso", 'add "ctc_diamante" xpos' in screens, False)
    m = re.search(r"style say_dialogue:(.*?)\n##", screens, re.S)
    check("contorno dialoghi", bool(m and "outlines" in m.group(1)), True)
    check("box_entra", "transform box_entra" in screens and "at box_entra" in screens, True)
    check("cronologia corsivo", 'h.what_args.get("italic")' in screens, True)


def check_scelte():
    screens = leggi("screens.rpy")
    check("scelte in cascata", "scelta_entra(" in screens, True)
    check("suono hover scelte", 'hover_sound "audio/scelta.ogg"' in screens, True)
    check("bagliore scelte", "gui/scelta_bagliore.png" in screens, True)
    check("hover sposta", bool(re.search(r"on hover:\s*\n\s*ease 0\.12 zoom 1\.04 xoffset 10", screens)), True)


def check_calendario():
    cal = leggi(os.path.join(MAL_REL, "calendario.rpy"))
    check("pianificatore si srotola", "at (pian_fisso if pian_fermo else pian_srotola)" in cal, True)
    check("voci in cascata", "pian_voce(" in cal, True)
    check("suono carta", "audio/carta.ogg" in cal, True)
    check("sigillo nel cartello", "ceralacca_festa.png" in cal and "audio/sigillo.ogg" in cal, True)
    check("luna piu' grande", bool(re.search(r"text LUNE_NOMI\[luna\]:\s*\n(?:.*\n){0,3}?\s*size 58", cal)), True)


def check_borsa():
    b = leggi(os.path.join(MAL_REL, "borsa.rpy"))
    check("borsa usa conteggio", "rgl.conteggio(" in b, True)
    check("borsa luccichio", "gui/malandrini/scudo_luccichio.png" in b, True)
    check("borsa contatore istantaneo dopo rollback", "_bo.t0 = 0.0" in b, True)


def check_menu():
    fg = leggi("finali_galleria.rpy")
    check("ultimo finale registrato", "persistent.ultimo_finale = fid" in fg, True)
    check("default ultimo finale", "default persistent.ultimo_finale = None" in fg, True)
    mc = leggi("menu_cast.rpy")
    screens = leggi("screens.rpy")
    check("centro dal finale", "rgl.fondo_menu(" in mc, True)
    check("fondo del menu", "mm_fondo()" in screens, True)
    check("entrata in sequenza", "mm_entrata(" in mc, True)
    check("titolo che respira", "mm_titolo_respira" in screens, True)


def check_particelle():
    fx = leggi("effetti.rpy")
    righe = {(b, n) for b, n, _q in tab.EFFETTI_SFONDI}
    for bg, nome in (("studio_glauco", "braci"), ("corridoio_ceppo", "braci"),
                     ("arena_athlion", "nevischio"), ("vicoli_zefiro", "pioggia")):
        check("particelle %s su %s" % (nome, bg), (bg, nome) in righe, True)
    check("pioggia usa rgl.piove", "rgl.piove(" in fx, True)
    mal = leggi(os.path.join("capitoli", "malandrini", "capitolo.rpy"))
    check("ambiente pioggia", "audio/malandrini/amb_pioggia.ogg" in mal, True)


def check_regia_primitive():
    regia = leggi("regia.rpy")
    for nome in ("salto_tempo", "shock", "ricordo"):
        check("transizione " + nome, bool(re.search(r"^define %s = " % nome, regia, re.M)), True)
    for fn in ("camera_dentro", "camera_su", "camera_panoramica", "camera_riposo",
               "intimo", "fine_intimo"):
        check("funzione " + fn, bool(re.search(r"^    def %s\(" % fn, regia, re.M)), True)
    check("default regia_intimo", "default regia_intimo = False" in regia, True)
    check("scene azzera camera", "config.scene = _regia_scene" in regia, True)
    check("load azzera camera", "config.after_load_callbacks.append(camera_riposo_subito)" in regia, True)
    au = leggi("audio.rpy")
    check("audio concatena with_callback", "_audio_with_prec" in au, True)
    luce = leggi("luce.rpy")
    check("sfondi con fondo_fx", "fondo_fx()" in luce, True)



# --- Pacchetto estetica 2 (spec 2026-10-22-estetica-animazioni) ----------

def test_estetica2_regole():
    check("furia trema", rl.movimento_per("neutra", "furia"), "trema")
    check("minaccioso trema", rl.movimento_per("neutro", "minaccioso"), "trema")
    check("rabbia avanza ancora", rl.movimento_per("neutra", "rabbia"), "avanza")

    check("respiro a riposo", rl.respiro(0.0, 0.0), 1.0)
    valori = [rl.respiro(i * 0.01, 0.0) for i in range(int(rl.RESPIRO_PERIODO * 100) + 1)]
    check("respiro massimo", max(valori) <= 1.0 + rl.RESPIRO_AMPIEZZA + 1e-9
          and max(valori) >= 1.0 + rl.RESPIRO_AMPIEZZA - 1e-4, True)
    check("respiro minimo", min(valori) >= 1.0 - 1e-9, True)
    fasi = {rl.fase_per(t) for t in ("aede", "caino", "druso", "icaro", "ofelia")}
    check("fasi diverse", len(fasi), 5)
    check("fase in [0,1)", all(0 <= f < 1 for f in fasi), True)

    fiamme = [rl.fiamma(i * 0.05) for i in range(600)]
    check("fiamma nei limiti", all(0.97 <= f <= 1.03 for f in fiamme), True)
    check("fiamma continua",
          max(abs(a - b) for a, b in zip(fiamme, fiamme[1:])) < 0.01, True)
    veli = [rl.velo_fuoco(i * 0.05) for i in range(600)]
    check("velo nei limiti", all(0.02 <= v <= 0.06 for v in veli), True)
    check("fuoco vicoli sera", rl.fuoco_per("vicoli_zefiro", "sera", tab), True)
    check("niente fuoco vicoli mattina", rl.fuoco_per("vicoli_zefiro", "mattina", tab), False)
    check("fuoco studio", rl.fuoco_per("studio_glauco", "mattina", tab), True)
    check("niente fuoco palestra", rl.fuoco_per("palestra", "sera", tab), False)
    check("niente fuoco senza tabelle", rl.fuoco_per("studio_glauco", "sera", None), False)

    def ep(bg, slot, ctx, piove, tempesta):
        return rl.effetti_per(bg, slot, ctx, piove, tempesta, tab)
    check("asciutto da tabella", tab.EFFETTI_ASCIUTTO, (("vicoli_zefiro", "luccichii"),))
    check("effetti senza tabelle",
          rl.effetti_per("esterno_neve", None, None, False, False, None), ())
    check("effetti vicoli senza tabelle",
          rl.effetti_per("vicoli_zefiro", "sera", "fumeria", False, False, None), ())
    check("neve fitta in tempesta", ep("esterno_neve", "sera", "luna6_climax", False, True), ("neve_fitta",))
    check("neve normale", ep("esterno_neve", "sera", "luna6_climax", False, False), ("neve",))
    check("vicoli sera", ep("vicoli_zefiro", "sera", None, False, False), ("fumo", "luccichii"))
    check("vicoli pioggia", ep("vicoli_zefiro", "mattina", None, True, False), ("pioggia",))
    check("vicoli mattina asciutta", ep("vicoli_zefiro", "mattina", None, False, False), ("luccichii",))
    check("serra", ep("sala_svelo", "pomeriggio", "corte", False, False), ("foglie",))
    check("svelo senza corte", ep("sala_svelo", "sera", "svelo", False, False), ("polvere",))
    check("contesto su altro sfondo", ep("cala_notte", "mattina", "ofelia_ev3", False, False), ("lanterne",))
    check("arena", ep("arena_athlion", "pomeriggio", "athlion", False, False), ("nevischio", "scintille"))
    check("fumeria", ep("vicoli_zefiro", "sera", "fumeria", False, False), ("fumo_pipa", "luccichii"))
    check("sfondo ignoto", ep("palestra", "sera", None, False, False), ())
    check("nessuno sfondo", ep(None, None, None, False, False), ())

    for d, n in ((0, 0), (1, 2), (2, 2), (3, 3), (5, 3), (6, 4), (9, 4), (10, 5),
                 (40, 5), (-1, 1), (-2, 1), (-3, 2), (-5, 2), (-6, 3), (-30, 3)):
        check("monete per %+d" % d, rl.monete_per(d), n)
    check("lento", rl.LENTO_CPS, 0.7)


def check_estetica2_sprite():
    luce = leggi("luce.rpy")
    curva = luce.split("def _lu_curva", 1)[1].split("def ", 1)[0]
    check("curva tonfo", '"tonfo"' in curva, True)
    check("muovi definito", "def muovi(" in luce, True)
    check("respiro negli sprite", "rgl.respiro(" in luce, True)
    check("fiamma negli sprite", "rgl.fiamma(" in luce, True)
    check("velo del fuoco sullo sfondo", "rgl.velo_fuoco(" in luce, True)
    check("ombra della sagoma dietro gli sprite", "_lu_ombra(nome)" in luce, True)
    mg = open(os.path.join(HERE, "..", "make_gui.py"), encoding="utf-8").read()
    check("make_gui genera le ombre", "def ombre_sprite" in mg and "ombre_sprite()" in mg, True)
    check("ombre generate", os.path.exists(os.path.join(GAME, "gui", "ombre", "ofelia_neutra.webp")), True)
    mal = leggi(os.path.join("capitoli", "malandrini", "capitolo.rpy"))
    check("tonfo di Druso all'entrata",
          'entrate={"druso": ("tonfo", 0.3)}' in mal, True)
    check("entrate generiche in luce.rpy",
          "for tag, (mov, ritardo) in" in luce and "entrate.items()" in luce, True)


def check_estetica2_particelle():
    fx = leggi("effetti.rpy")
    fabbriche = fx.split("FX_FABBRICHE", 1)[1].split("}", 1)[0]
    for nome in ("foglie", "fumo_pipa", "scintille", "luccichii", "neve_fitta"):
        check("fabbrica " + nome, '"%s"' % nome in fabbriche, True)
    check("effetti da rgl.effetti_per", "rgl.effetti_per(" in fx, True)
    regia = leggi("regia.rpy")
    check("default regia_tempesta", "default regia_tempesta = False" in regia, True)
    scena = regia.split("def _regia_scene", 1)[1].split("def ", 1)[0]
    check("scene spegne la tempesta", "regia_tempesta = False" in scena, True)
    climax = leggi(os.path.join(MAL_REL, "routes", "aede_finali.rpy")).split("label climax:", 1)[1].split("\nlabel ", 1)[0]
    check("tempesta nel climax di Aede", "$ tempesta()" in climax, True)
    mg = open(os.path.join(HERE, "..", "make_gui.py"), encoding="utf-8").read()
    for img in ("fx_foglia.png", "fx_scintilla.png", "fx_luccichio.png"):
        check("make_gui genera " + img, img in mg, True)
        check("immagine " + img, os.path.exists(os.path.join(GAME, "gui", img)), True)


def check_estetica2_lento():
    regia = leggi("regia.rpy")
    check("lento definito", "def lento(" in regia and "def fine_lento(" in regia, True)
    check("default regia_lento", "default regia_lento = False" in regia, True)
    scena = regia.split("def _regia_scene", 1)[1].split("def ", 1)[0]
    check("scene spegne lento", "regia_lento = False" in scena, True)
    check("say_arguments_callback", "config.say_arguments_callback = _regia_say_args" in regia, True)
    check("moltiplicatore da rgl", "rgl.LENTO_CPS" in regia, True)


def check_estetica2_cartello():
    cal = leggi(os.path.join(MAL_REL, "calendario.rpy"))
    check("cartello con giorno e luna precedenti",
          "screen cartello_data(luna, giorno, festa=False, giorno_prec=None, luna_prec=None)" in cal, True)
    for t in ("giorno_esce", "giorno_entra", "luna_esce", "luna_entra"):
        check("transform " + t, "transform %s:" % t in cal, True)
    check("chiamata passa il giorno prima",
          "cartello_data(cal_luna, cal_giorno, cal_giorno_segnato(cal_luna, cal_giorno), *cal_giorno_prima)" in cal, True)


def check_estetica2_monete():
    bo = leggi(os.path.join(MAL_REL, "borsa.rpy"))
    check("numero di monete da rgl", "rgl.monete_per(" in bo, True)
    check("screen delle monete", "screen borsa_monete():" in bo, True)
    check("overlay delle monete", 'config.overlay_screens.append("borsa_monete")' in bo, True)
    reset = bo.split("def _bo_reset", 1)[1].split("def ", 1)[0]
    check("reset ferma il volo", "volo = None" in reset, True)
    check("transform moneta_vola", "transform moneta_vola(" in bo, True)
    check("transform moneta_cade", "transform moneta_cade(" in bo, True)


MUOVI_NOMI = ("sobbalzo", "arretra", "avanza", "trema", "tonfo")


def _labels_route():
    """(file, label, corpo) di ogni label nelle route."""
    out = []
    cartella = os.path.join(GAME, MAL_REL, "routes")
    for f in sorted(os.listdir(cartella)):
        if not f.endswith(".rpy"):
            continue
        src = open(os.path.join(cartella, f), encoding="utf-8").read()
        for blocco in re.split(r"\nlabel ", "\n" + src)[1:]:
            nome = re.match(r"(\w+)", blocco).group(1)
            out.append((f, nome, blocco))
    return out


def check_estetica2_scene():
    labels = _labels_route()
    n_muovi = 0
    for f, nome, corpo in labels:
        righe = corpo.split("\n")
        for i, r in enumerate(righe):
            m = re.search(r'\$ muovi\("(\w+)", "(\w+)"\)', r)
            if not m:
                continue
            n_muovi += 1
            tag, mov = m.groups()
            prima = "\n".join(righe[:i])
            check("%s:%s muovi %s nome valido" % (f, nome, tag), mov in MUOVI_NOMI, True)
            check("%s:%s muovi %s in scena" % (f, nome, tag),
                  bool(re.search(r"^\s*show %s\b" % tag, prima, re.M)), True)
    check("ci sono movimenti a mano", n_muovi >= 8, True)
    impegni = [(f, n, c) for f, n, c in labels if n.startswith("impegno_")]
    check("impegni trovati", len(impegni) >= 7, True)
    for f, nome, corpo in impegni:
        check("lento in " + nome, "$ lento()" in corpo, True)
    tutto = "\n".join(c for _f, _n, c in labels)
    check("ricordo usato", "with ricordo" in tutto, True)


def check_estetica2_revisione():
    luce = leggi("luce.rpy")
    check("niente image_size all'avvio", "renpy.image_size(" in luce, False)
    check("dimensioni dalla tabella", "gui/ombre/dimensioni.json" in luce, True)
    import json
    tab = os.path.join(GAME, "gui", "ombre", "dimensioni.json")
    dim = json.load(open(tab, encoding="utf-8")) if os.path.exists(tab) else {}
    check("tabella con ofelia neutra", isinstance(dim.get("ofelia neutra"), list), True)
    fx = leggi("effetti.rpy")
    corpo = fx.split("def effetto_corrente", 1)[1].split("def ", 1)[0]
    check("particelle ferme in skip", "renpy.is_skipping()" in corpo, True)


# --- Capitoli scalabili: codice comune senza nomi di Malandrini ----------

FILE_COMUNI = ("regia_logic.py", "effetti.rpy", "luce.rpy", "audio.rpy",
               "feedback.rpy", "regia.rpy", "capitoli.rpy", "screens.rpy",
               "menu_cast.rpy", "finali_galleria.rpy", "protagonista.rpy")
NOMI_MALANDRINI = ("aede", "caino", "druso", "icaro", "ofelia",
                   "vicoli_zefiro", "cala_notte", "esterno_neve")


def _senza_commento(riga):
    """La riga senza il commento (un # fuori dalle stringhe)."""
    quote = None
    i = 0
    while i < len(riga):
        c = riga[i]
        if quote:
            if c == "\\":
                i += 1
            elif c == quote:
                quote = None
        elif c in "\"'":
            quote = c
        elif c == "#":
            return riga[:i]
        i += 1
    return riga


def check_codice_comune_pulito():
    check("senza commento", _senza_commento('x = "#abc"  # aede'), 'x = "#abc"  ')
    nomi = re.compile(r"\b(%s)\b" % "|".join(NOMI_MALANDRINI), re.I)
    for rel in FILE_COMUNI:
        trovati = []
        for n, riga in enumerate(leggi(rel).splitlines(), 1):
            for m in nomi.finditer(_senza_commento(riga)):
                trovati.append("%d:%s" % (n, m.group(1)))
        check("codice comune pulito: " + rel, trovati, [])


def check_capitolo_regia():
    check("capitolo_regia definita", "def capitolo_regia(" in leggi("capitoli.rpy"), True)
    for rel, pezzi in (("effetti.rpy", ("rgl.effetti_per(",)),
                       ("luce.rpy", ("rgl.tinta_per(", "rgl.fuoco_per(")),
                       ("menu_cast.rpy", ("rgl.fondo_menu(",))):
        src = leggi(rel)
        for p in pezzi:
            # La chiamata con le sue righe di continuazione: le tabelle sono
            # capitolo_regia(), diretta o passata da "tab = capitolo_regia()".
            chiamate = re.findall(re.escape(p) + r"[^\n]*(?:\n[^\n]*){0,3}", src)
            # Fondo del menu: le tabelle del capitolo dell'ultimo finale
            # (rcap.capitolo_di_finale, Task 7).
            buona = lambda c: ("capitolo_regia()" in c
                               or (", tab)" in c and "tab = capitolo_regia()" in src)
                               or (", c.regia)" in c and "c = rcap.capitolo_di_finale(" in src))
            check("%s: %s con capitolo_regia()" % (rel, p),
                  bool(chiamate) and all(buona(c) for c in chiamate), True)
    fb = leggi("feedback.rpy")
    check("feedback dal capitolo", "FEEDBACK_AFFINITA" not in fb and ".affinita" in fb, True)
    check("niente side image in feedback.rpy",
          bool(re.search(r"^image side ", fb, re.M)), False)
    rit = os.path.join(GAME, "capitoli", "malandrini", "ritratti.rpy")
    rit_src = open(rit, encoding="utf-8").read() if os.path.exists(rit) else ""
    for c in ("aede", "caino", "ofelia", "druso", "icaro", "briseide", "vanna", "corrado"):
        check("ritratto " + c, 'image side %s = "gui/malandrini/portrait_%s.png"' % (c, c) in rit_src, True)
    mal = leggi(os.path.join("capitoli", "malandrini", "capitolo.rpy"))
    for p in ("regia=regia_tabelle", "ambienti=", "ambiente_pioggia=",
              "ambiente_arrivo=", "entrate=", "affinita="):
        check("registrazione Malandrini: " + p, p in mal, True)
    au = leggi("audio.rpy")
    check("audio senza AMBIENTI fissi", "AMBIENTI = {" in au, False)
    for p in (".ambienti", ".ambiente_pioggia", ".ambiente_arrivo"):
        check("audio legge " + p, p in au, True)


def main():
    check_codice_comune_pulito()
    check_capitolo_regia()
    check_luce()
    check_regia_primitive()
    check_particelle()
    check_menu()
    check_borsa()
    check_calendario()
    check_textbox()
    check_scelte()
    test_tinte()
    test_oscurato()
    test_movimenti()
    test_pioggia()
    test_transizioni()
    test_fondo_menu()
    test_conteggio()
    test_estetica2_regole()
    check_estetica2_sprite()
    check_estetica2_particelle()
    check_estetica2_lento()
    check_estetica2_cartello()
    check_estetica2_monete()
    check_estetica2_scene()
    check_estetica2_revisione()
    if FAILURES:
        print(f"{len(FAILURES)} FALLITI: {FAILURES}")
        sys.exit(1)
    print("regia ok")


if __name__ == "__main__":
    main()
