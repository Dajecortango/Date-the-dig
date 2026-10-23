"""Verifica il registro puro dei capitoli (game/capitoli_logic.py).

Uso: py -3 -I -X utf8 tests/test_capitoli.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from percorsi import prepara_import  # noqa: E402
prepara_import()

import capitoli_logic as rcap  # noqa: E402


def check(nome, ottenuto, atteso):
    if ottenuto == atteso:
        print("ok   ", nome)
    else:
        print("FAIL ", nome, "-> ottenuto", repr(ottenuto), "atteso", repr(atteso))


def solleva(fn, eccezione):
    try:
        fn()
    except eccezione:
        return True
    except Exception:
        return False
    return False


rcap.svuota()
check("registro vuoto: capitolo_menu None", rcap.capitolo_menu("a"), None)

rcap.registra(id="a", numero=2, titolo="A", funzioni={"borsa"},
              finali=[("a_fine", "Fine", "g", "i"), ("a_altro", "Altro", "g", "i")])
rcap.registra(id="b", numero=1, titolo="B")
check("ordine per numero", [c.id for c in rcap.elenco()], ["b", "a"])
check("default vuoti", (rcap.ottieni("b").finali, rcap.ottieni("b").ambienti,
                        rcap.ottieni("b").funzioni, rcap.ottieni("b").regia),
      ([], {}, frozenset(), None))
check("schede default vuote e per istanza",
      (rcap.ottieni("b").schede, rcap.ottieni("b").schede is not rcap.ottieni("a").schede),
      ({}, True))
check("id doppio", solleva(lambda: rcap.registra(id="a", numero=3), ValueError), True)
check("registra senza id", solleva(lambda: rcap.registra(numero=9), ValueError), True)
check("registra id vuoto", solleva(lambda: rcap.registra(id="", numero=9), ValueError), True)
check("cast_menu senza scheda",
      solleva(lambda: rcap.registra(id="d", numero=4, cast_menu=[("x", 0.0, 6)],
                                    schede={"y": {}}), ValueError), True)
check("cast_menu senza schede",
      solleva(lambda: rcap.registra(id="d", numero=4, cast_menu=[("x", 0.0, 6)]), ValueError), True)
check("d non registrato dopo errore", rcap.ottieni("d"), None)
check("finale doppio nella stessa registrazione",
      solleva(lambda: rcap.registra(id="e", numero=5,
                                    finali=[("e_x", "x", "g", "i"), ("e_x", "y", "g", "i")]),
              ValueError), True)
check("e non registrato dopo errore", rcap.ottieni("e"), None)


class _Ns(object):
    pass


_st = _Ns()
_st.piatta = 3
_st.zzprova = _Ns()
_st.zzprova.affinita = 5
check("leggi_variabile piatta", rcap.leggi_variabile(_st, "piatta"), 3)
check("leggi_variabile con punto", rcap.leggi_variabile(_st, "zzprova.affinita"), 5)
check("leggi_variabile mancante", rcap.leggi_variabile(_st, "zzprova.manca"), None)
check("leggi_variabile store mancante", rcap.leggi_variabile(_st, "nulla.x"), None)
check("finale gia' usato",
      solleva(lambda: rcap.registra(id="c", numero=3,
                                    finali=[("a_fine", "x", "g", "i")]), ValueError), True)
check("c non registrato dopo errore", rcap.ottieni("c"), None)
check("ha vero", rcap.ha("a", "borsa"), True)
check("ha falso", rcap.ha("a", "altro"), False)
check("ha sconosciuto", rcap.ha("zzz", "borsa"), False)
check("capitolo_menu fallback", rcap.capitolo_menu("zzz").id, "b")
check("capitolo_menu noto", rcap.capitolo_menu("a").id, "a")
check("finali_contati", rcap.finali_contati("a", {"a_fine", "x_estraneo"}), (1, 2))
check("finali_contati sconosciuto", rcap.finali_contati("zzz", {"a_fine"}), (0, 0))
check("capitolo_di_finale", rcap.capitolo_di_finale("a_fine").id, "a")
check("capitolo_di_finale nessuno", rcap.capitolo_di_finale("nessuno"), None)
rcap.svuota()
check("svuota", rcap.elenco(), [])
check("svuota: capitolo_menu None", rcap.capitolo_menu("a"), None)


# --- Sorgenti Ren'Py: registrazione di Malandrini ---
def leggi(*parti):
    from percorsi import GAME
    with open(os.path.join(GAME, *parti), encoding="utf-8") as f:
        return f.read()


_cap = leggi("capitoli", "malandrini", "capitolo.rpy") if os.path.exists(
    os.path.join(HERE, "..", "game", "capitoli", "malandrini", "capitolo.rpy")) else ""
check("capitolo.rpy: id malandrini", 'id="malandrini"' in _cap, True)
check("capitolo.rpy: ingresso capitolo1", 'ingresso="capitolo1"' in _cap, True)
check("capitolo.rpy: migra salvataggio", "_conseguenze_migra_salvataggio" in _cap, True)
_ch1 = leggi("capitoli", "malandrini", "routes", "chapter1.rpy")
_corpo = _ch1.split("label capitolo1:", 1)[1].split("\nlabel ", 1)[0]
check("capitolo1: entra_capitolo", 'entra_capitolo("malandrini")' in _corpo, True)
check("conseguenze.rpy: niente after_load diretto",
      "after_load_callbacks.append(_conseguenze_migra_salvataggio)" in leggi("capitoli", "malandrini", "conseguenze.rpy"), False)

# --- Task 6: HUD, menu di gioco e callback legati alle funzioni ----------
import glob  # noqa: E402
import re  # noqa: E402
from percorsi import MAL  # noqa: E402

_mal_src = {}
for _p in glob.glob(os.path.join(MAL, "**", "*.rpy"), recursive=True):
    with open(_p, encoding="utf-8") as _f:
        _mal_src[_p] = _f.read()
_tutto_mal = "\n".join(_mal_src.values())


def _corpo_def(nome):
    """Corpo di una def/screen di Malandrini (fino alla prossima riga con
    indentazione minore o uguale)."""
    m = re.search(r"^([ \t]*)(?:def|screen) %s\b[^\n]*\n((?:(?:\1[ \t]+[^\n]*|)\n)*)"
                  % re.escape(nome), _tutto_mal, re.M)
    return m.group(2) if m else None


for _m in re.finditer(r"config\.(?:overlay_screens|start_interact_callbacks)"
                      r"\.append\(\"?([A-Za-z_0-9]+)\"?\)", _tutto_mal):
    _c = _corpo_def(_m.group(1))
    check("callback/overlay '%s' controlla il capitolo" % _m.group(1),
          _c is not None and ("capitolo_ha(" in _c or "capitolo_corrente" in _c), True)

_bh = _corpo_def("borsa_hud_visibile") or ""
check("borsa_hud_visibile: capitolo_ha(borsa)", 'capitolo_ha("borsa")' in _bh, True)
_bm = _corpo_def("_bo_volo_attivo") or ""
check("borsa_monete (_bo_volo_attivo): capitolo_ha(borsa)", 'capitolo_ha("borsa")' in _bm, True)
_bc = _corpo_def("_bo_controlla") or ""
check("_bo_controlla: capitolo_ha(borsa)", 'capitolo_ha("borsa")' in _bc, True)

_scr = leggi("screens.rpy")
check("screens: capitolo_ha(borsa)", 'capitolo_ha("borsa")' in _scr, True)
for _f in ("diario", "cronache", "trama"):
    check("screens navigation: capitolo_ha(%s)" % _f, 'capitolo_ha("%s")' % _f in _scr, True)
check("screens: ritratto da registro", '"capitolo") or "malandrini"' in _scr and ".ritratto" in _scr, True)
check("screens: niente cal_portrait", "cal_portrait" in _scr, False)
_fb = leggi("feedback.rpy")
check("feedback: niente cal_portrait", "cal_portrait" in _fb, False)
check("feedback: ritratto del capitolo", ".ritratto" in _fb, True)
check("calendario: il json del capitolo non e' piu' di Malandrini",
      'd["capitolo"]' in leggi("capitoli", "malandrini", "calendario.rpy"), False)
check("capitoli.rpy: salva capitolo nel json",
      'd["capitolo"] = store.capitolo_corrente' in leggi("capitoli.rpy")
      and "config.save_json_callbacks.append(_capitoli_json)" in leggi("capitoli.rpy"), True)
check("capitoli.rpy: after_load aggiorna ultimo_capitolo",
      "persistent.ultimo_capitolo = store.capitolo_corrente" in
      leggi("capitoli.rpy").split("def _capitoli_dopo_caricamento", 1)[1].split("config.after_load", 1)[0], True)
check("feedback: legge le variabili con leggi_variabile",
      "rcap.leggi_variabile(store, v)" in leggi("feedback.rpy"), True)
check("capitolo.rpy: ritratto=cal_portrait", "ritratto=cal_portrait" in _cap, True)

# --- Task 7: scelta del capitolo e menu principale -----------------------
_nav = _scr.split("screen navigation():", 1)[1].split("\nscreen ", 1)[0]
check("navigation: Start apre scegli_capitolo", 'ShowMenu("scegli_capitolo")' in _nav, True)
check("navigation: niente Start() nudo", "action Start()" in _nav, False)
check("capitoli.rpy: screen scegli_capitolo",
      re.search(r"^screen scegli_capitolo\b", leggi("capitoli.rpy"), re.M) is not None, True)
_start = leggi("script.rpy").split("label start:", 1)[1].split("\nlabel ", 1)[0]
check("label start: niente jump capitolo1", "jump capitolo1" in _start, False)
check("label start: jump expression _return", "jump expression _return" in _start, True)
_mc = leggi("menu_cast.rpy")
check("menu_cast: fondo dal capitolo del finale", "capitolo_di_finale(" in _mc, True)
check("menu_cast: niente FINALI globale nel fondo", "fondo_menu(persistent.ultimo_finale, FINALI" in _mc, False)
check("main_menu: carosello solo col cast", "if mm_cast():" in _scr, True)

# --- Task 8: galleria dei finali per capitolo; schede dal capitolo ---------
_gal = leggi("finali_galleria.rpy").split("screen galleria_finali():", 1)[1]
check("galleria: rcap.elenco()", "rcap.elenco()" in _gal, True)
check("galleria: finali_contati", "finali_contati" in _gal, True)
check("galleria: niente FINALI diretto", re.search(r"\bFINALI\b|GALLERIA_ROUTE", _gal) is None, True)
_mcs = leggi("menu_cast.rpy")
check("menu_cast: niente SCHEDE locale", re.search(r"^\s*SCHEDE\s*=", _mcs, re.M) is None, True)
check("menu_cast: schede dal capitolo", ".schede" in _mcs, True)
check("menu_cast: niente FINALI globale", re.search(r"\bFINALI\b", _mcs) is None, True)
check("capitolo.rpy: schede=", "schede=" in _cap, True)

# --- Task 9: asset per capitolo -------------------------------------------
from percorsi import GAME  # noqa: E402

_rpy = {}
for _p in glob.glob(os.path.join(GAME, "**", "*.rpy"), recursive=True):
    if os.sep + "tl" + os.sep in _p:
        continue
    with open(_p, encoding="utf-8") as _f:
        _rpy[_p] = _f.read()
_cast_chiavi = ["aede", "caino", "ofelia", "druso", "icaro"]
_ritr_chiavi = _cast_chiavi + ["briseide", "vanna", "corrado", "locked"]
_pattern = {
    "gui/cast_%s.webp": ["gui/cast_%s.webp" % c for c in _cast_chiavi],
    "gui/cast_%s_ombra.webp": ["gui/cast_%s_ombra.webp" % c for c in _cast_chiavi],
    "gui/cast_%s_alone.webp": ["gui/cast_%s_alone.webp" % c for c in _cast_chiavi],
    "gui/cast_%s_hover.webp": ["gui/cast_%s_hover.webp" % c for c in _cast_chiavi],
    "gui/malandrini/portrait_%s.png": ["gui/malandrini/portrait_%s.png" % c for c in _ritr_chiavi],
    "gui/malandrini/luna_%d.png": ["gui/malandrini/luna_%d.png" % n for n in range(1, 7)],
    "gui/ombre/%s.webp": [],   # opzionale: se manca, nessuna ombra (luce.rpy)
}
def _esiste_asset(rel):
    return os.path.exists(os.path.join(GAME, rel))


_citati = set()
_dinamici = set()
for _src in _rpy.values():
    _citati |= set(re.findall(r'"((?:gui|audio)/[\w./-]+\.(?:png|webp|ogg|json))"', _src))
    _dinamici |= set(re.findall(r'"((?:gui|audio)/[\w./-]*%[sd][\w./-]*\.(?:png|webp|ogg))"', _src))
_citati.discard("gui/confirm_frame.png")   # primo di una lista di ripiego
for _rel in sorted(_citati):
    check("asset esiste: " + _rel, _esiste_asset(_rel), True)
for _d in sorted(_dinamici):
    check("pattern noto: " + _d, _d in _pattern, True)
    for _rel in _pattern.get(_d, []):
        check("asset esiste: " + _rel, _esiste_asset(_rel), True)

_img_nomi = {}
for _radice, _d, _files in os.walk(os.path.join(GAME, "images")):
    for _fn in _files:
        _nome = os.path.splitext(_fn)[0].lower()
        _img_nomi.setdefault(_nome, []).append(os.path.relpath(os.path.join(_radice, _fn), GAME))
check("immagini: nomi unici sotto images/",
      {k: v for k, v in _img_nomi.items() if len(v) > 1}, {})


# --- nuovo_capitolo.py: modello di capitolo nuovo -----------------------
import tempfile
import shutil
_RADICE = os.path.normpath(os.path.join(HERE, ".."))
if _RADICE not in sys.path:
    sys.path.insert(0, _RADICE)
import nuovo_capitolo

_tmp = tempfile.mkdtemp()
try:
    _dest = nuovo_capitolo.crea("prova", 2, "Prova", _tmp)
    _tutti = []
    for _r, _d, _fs in os.walk(_dest):
        for _fn in _fs:
            with open(os.path.join(_r, _fn), encoding="utf-8") as _f:
                _tutti.append(_f.read())
    check("modello: nessun segnaposto rimasto",
          any(s in t for t in _tutti for s in ("__ID__", "__NUMERO__", "__TITOLO__")), False)
    with open(os.path.join(_dest, "capitolo.rpy"), encoding="utf-8") as _f:
        _cap = _f.read()
    check("modello: capitolo.rpy ha l'id", 'id="prova"' in _cap, True)
    check("modello: cartelle asset",
          all(os.path.isdir(os.path.join(_tmp, a, "prova")) for a in ("images", "gui", "audio")), True)
    try:
        nuovo_capitolo.crea("prova", 2, "Prova", _tmp)
        _esito = None
    except FileExistsError:
        _esito = "FileExistsError"
    check("modello: id esistente", _esito, "FileExistsError")
    try:
        nuovo_capitolo.crea("Prova!", 2, "Prova", _tmp)
        _esito = None
    except ValueError:
        _esito = "ValueError"
    check("modello: id non valido", _esito, "ValueError")
    for _id, _tit, _nome in (("prova\n", "Prova", "id con a capo finale"),
                             ("prova2", 'Pro"va', "titolo con virgolette"),
                             ("prova2", "Pro\\va", "titolo con backslash"),
                             ("prova2", "Pro{va", "titolo con graffa"),
                             ("prova2", "Pro[va", "titolo con quadra"),
                             ("prova2", "Pro\nva", "titolo con a capo")):
        try:
            nuovo_capitolo.crea(_id, 2, _tit, _tmp)
            _esito = None
        except ValueError:
            _esito = "ValueError"
        check("modello: " + _nome, _esito, "ValueError")
finally:
    shutil.rmtree(_tmp, ignore_errors=True)
