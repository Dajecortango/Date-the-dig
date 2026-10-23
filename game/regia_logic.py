"""Logica pura del pacchetto grafico: luce dei personaggi, movimenti per
espressione, meteo, transizioni delle scene, fondo del menu, contatore della
Borsa. Nessuna dipendenza da Ren'Py.
Test: py -3 -I tests/test_regia.py
"""

# Le tabelle di regia (tinte, fuoco, effetti, fondi del menu) sono del
# capitolo: le funzioni le ricevono come ultimo parametro `tab` (modulo o
# oggetto con quegli attributi). Con tab=None: nessuna corrispondenza.

TINTA_FORZA = 0.18

LUCE_OSCURATA = 0.75

MOVIMENTI = {
    "sorpresa": "sobbalzo", "sorpreso": "sobbalzo",
    "imbarazzata": "arretra", "imbarazzato": "arretra",
    "rabbia": "avanza", "furia": "trema", "furioso": "trema",
    "minaccioso": "trema",
    "irritata": "avanza", "irritato": "avanza",
}
MOVIMENTO_PAUSA = 3  # interazioni prima che lo stesso sprite si muova ancora


def _t(tab, nome, vuoto):
    """Attributo `nome` delle tabelle del capitolo, o `vuoto`."""
    if tab is None:
        return vuoto
    return getattr(tab, nome, vuoto)


def tinta_per(bg, slot, tab):
    tinte = _t(tab, "TINTE", {})
    if bg not in tinte:
        return None
    if bg in _t(tab, "TINTE_SOLO_SERA", ()) and slot != "sera":
        return None
    return tinte[bg]


def oscurato(tag, parlante, in_scena):
    return (parlante in in_scena and tag != parlante
            and len(in_scena) >= 2)


def movimento_per(vecchia, nuova):
    if vecchia is None or vecchia == nuova:
        return None
    return MOVIMENTI.get(nuova)


def piove(luna, giorno):
    return (luna * 31 + giorno * 7) % 3 == 0


def transizione_scene(bg_prec, bg_nuovo, trans):
    """Nuova transizione per una "scene bg ... with trans"; None = lasciala."""
    if bg_nuovo == "nero" or trans not in ("fade", "dissolve"):
        return None
    if bg_prec is None or bg_prec != bg_nuovo:
        return "stacco"
    return "salto_tempo"


def fondo_menu(ultimo, finali, tab):
    """(sfondo, chiave del cast) per il menu dopo il finale `ultimo`."""
    if ultimo is not None and ultimo == _t(tab, "FINALE_SEMESTRE", None):
        return (_t(tab, "FONDO_SEMESTRE", None), None)
    fondi = _t(tab, "FONDI_ROUTE", {})
    for fid, _titolo, route, _ind in finali:
        if fid == ultimo and route in fondi:
            return (fondi[route], route.lower())
    return (None, None)


def conteggio(da, a, t, durata=0.6):
    """Valore intero mostrato a t secondi dall'inizio (ease-out)."""
    if t >= durata:
        return a
    k = max(0.0, t / durata)
    k = 1.0 - (1.0 - k) ** 3
    return int(round(da + (a - da) * k))


# --- Pacchetto estetica 2 -----------------------------------------------------
import math as _m

# Respiro degli sprite: zoom 1.0 -> 1.006 -> 1.0 in ~4.2 s, fase per tag.
RESPIRO_AMPIEZZA = 0.006
RESPIRO_PERIODO = 4.2


def respiro(t, fase):
    """Zoom del respiro al tempo t (s), fase in [0, 1)."""
    k = (t / RESPIRO_PERIODO + fase) % 1.0
    return 1.0 + RESPIRO_AMPIEZZA * (0.5 - 0.5 * _m.cos(2 * _m.pi * k))


def fase_per(tag):
    """Fase del respiro, fissa per tag: due sprite non respirano insieme."""
    h = 0
    for c in tag:
        h = (h * 31 + ord(c)) % 9973
    return (h % 97) / 97.0


# Luce del fuoco: sfondi con candele, camino, lanterne (tab.FUOCO e
# tab.FUOCO_SOLO_SERA).
def fuoco_per(bg, slot, tab):
    if bg in _t(tab, "FUOCO", ()):
        return True
    return bg in _t(tab, "FUOCO_SOLO_SERA", ()) and slot == "sera"


def _rumore(t):
    """Rumore lento in [-1, 1]: somma di sinusoidi tra 0.3 e 0.8 Hz."""
    return (0.5 * _m.sin(2 * _m.pi * 0.31 * t)
            + 0.3 * _m.sin(2 * _m.pi * 0.53 * t + 1.7)
            + 0.2 * _m.sin(2 * _m.pi * 0.79 * t + 4.1))


def fiamma(t):
    """Moltiplicatore di luce degli sprite vicino al fuoco: 1 +- 3%."""
    return 1.0 + 0.03 * _rumore(t)


def velo_fuoco(t):
    """Alfa del velo caldo sullo sfondo: 0.02 - 0.06."""
    return 0.04 + 0.02 * _rumore(t)


# Effetti di scena (effetti.rpy), dalle tabelle del capitolo:
# tab.EFFETTI_SFONDI (sfondo, effetto, quando): quando = None (sempre), "sera"
# (solo di sera) o "pioggia" (nei giorni di pioggia, mai di sera); vale la
# prima riga che corrisponde. tab.EFFETTI_ASCIUTTO (sfondo, effetto): in
# aggiunta quando non piove. tab.EFFETTI_CONTESTO (contesto del calendario,
# sfondo, effetto, modo): vale solo se anche lo sfondo corrisponde; modo
# "sostituisci" o "aggiungi".


def effetti_per(bg, slot, contesto, piove, tempesta, tab):
    """Effetti da mostrare, nell'ordine di disegno."""
    base = None
    for sfondo, fx, quando in _t(tab, "EFFETTI_SFONDI", ()):
        if sfondo != bg:
            continue
        if quando == "sera" and slot != "sera":
            continue
        if quando == "pioggia" and not piove:
            continue
        base = fx
        break
    if base == "neve" and tempesta:
        base = "neve_fitta"
    effetti = [base] if base else []
    if not piove:
        for sfondo, fx in _t(tab, "EFFETTI_ASCIUTTO", ()):
            if sfondo == bg:
                effetti.append(fx)
    for ctx, sfondo, fx, modo in _t(tab, "EFFETTI_CONTESTO", ()):
        if ctx == contesto and sfondo == bg:
            if modo == "sostituisci" and base:
                effetti[0] = fx
            elif modo == "sostituisci":
                effetti.insert(0, fx)
            else:
                effetti.append(fx)
            break
    return tuple(effetti)


def monete_per(delta):
    """Quante monete volano per una variazione di Scudi."""
    if delta == 0:
        return 0
    if delta < 0:
        d = -delta
        return 1 if d <= 2 else (2 if d <= 5 else 3)
    if delta <= 2:
        return 2
    if delta <= 5:
        return 3
    if delta <= 9:
        return 4
    return 5


# Testo piu' lento nei momenti intimi (regia.rpy, lento()).
LENTO_CPS = 0.7
