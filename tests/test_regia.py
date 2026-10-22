"""Verifica le regole pure del pacchetto grafico (game/regia_logic.py) e gli
agganci nei file .rpy (luce, regia, menu, route).

Uso: py -3 -I tests/test_regia.py
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.join(HERE, "..", "game")
sys.path.insert(0, GAME)

import regia_logic as rl  # noqa: E402

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
    check("tinta neve", rl.tinta_per("esterno_neve", "mattina"), "#9fb8ff")
    check("tinta vicoli sera", rl.tinta_per("vicoli_zefiro", "sera"), "#5a6fa8")
    check("tinta vicoli mattina", rl.tinta_per("vicoli_zefiro", "mattina"), None)
    check("tinta sconosciuto", rl.tinta_per("palestra", "sera"), None)
    check("tinta None", rl.tinta_per(None, None), None)
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
    check("furioso", rl.movimento_per("freddo", "furioso"), "avanza")
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
    check("neutro route", rl.fondo_menu("druso_neutral", FINALI_FINTI), ("palestra", "druso"))
    check("caino", rl.fondo_menu("caino_good_end", FINALI_FINTI), ("corridoio_ceppo", "caino"))
    check("semestre", rl.fondo_menu("finale_neutro_semestre", FINALI_FINTI), ("esterno_neve", None))
    check("nessuno", rl.fondo_menu(None, FINALI_FINTI), (None, None))
    check("ignoto", rl.fondo_menu("boh", FINALI_FINTI), (None, None))


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
    aede = leggi(os.path.join("routes", "aede_core.rpy"))
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
    cal = leggi("calendario.rpy")
    check("pianificatore si srotola", "at (pian_fisso if pian_fermo else pian_srotola)" in cal, True)
    check("voci in cascata", "pian_voce(" in cal, True)
    check("suono carta", "audio/carta.ogg" in cal, True)
    check("sigillo nel cartello", "ceralacca_festa.png" in cal and "audio/sigillo.ogg" in cal, True)
    check("luna piu' grande", bool(re.search(r"text LUNE_NOMI\[luna\]:\s*\n(?:.*\n){0,3}?\s*size 58", cal)), True)


def check_borsa():
    b = leggi("borsa.rpy")
    check("borsa usa conteggio", "rgl.conteggio(" in b, True)
    check("borsa luccichio", "gui/scudo_luccichio.png" in b, True)
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
    for bg, nome in (("studio_glauco", "braci"), ("corridoio_ceppo", "braci"),
                     ("arena_athlion", "nevischio"), ("vicoli_zefiro", "pioggia")):
        check("particelle %s su %s" % (nome, bg),
              bool(re.search(r'\("bg %s", "%s"' % (bg, nome), fx)), True)
    check("pioggia usa rgl.piove", "rgl.piove(" in fx, True)
    au = leggi("audio.rpy")
    check("ambiente pioggia", "audio/amb_pioggia.ogg" in au, True)


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


def main():
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
    if FAILURES:
        print(f"{len(FAILURES)} FALLITI: {FAILURES}")
        sys.exit(1)
    print("regia ok")


if __name__ == "__main__":
    main()
