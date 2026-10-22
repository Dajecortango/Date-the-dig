"""Logica pura del pacchetto grafico: luce dei personaggi, movimenti per
espressione, meteo, transizioni delle scene, fondo del menu, contatore della
Borsa. Nessuna dipendenza da Ren'Py.
Test: py -3 -I tests/test_regia.py
"""

# Sfondo -> tinta degli sprite (solo sprite: gli sfondi restano come sono).
TINTE = {
    "esterno_neve": "#9fb8ff",
    "cala_notte": "#ffb066",
    "vicoli_zefiro": "#5a6fa8",   # solo di sera
    "studio_glauco": "#ffc078",
    "corridoio_ceppo": "#ffc078",
    "arena_athlion": "#ffd9a0",
    "sala_svelo": "#f5d27a",
}
TINTE_SOLO_SERA = ("vicoli_zefiro",)
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

FONDI_ROUTE = {
    "Aede": "cala_notte",
    "Caino": "corridoio_ceppo",
    "Druso": "palestra",
    "Icaro": "vicoli_zefiro",
    "Ofelia": "consiglio",
}
FONDO_SEMESTRE = "esterno_neve"


def tinta_per(bg, slot):
    if bg not in TINTE:
        return None
    if bg in TINTE_SOLO_SERA and slot != "sera":
        return None
    return TINTE[bg]


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


def fondo_menu(ultimo, finali):
    """(sfondo, chiave del cast) per il menu dopo il finale `ultimo`."""
    if ultimo == "finale_neutro_semestre":
        return (FONDO_SEMESTRE, None)
    for fid, _titolo, route, _ind in finali:
        if fid == ultimo and route in FONDI_ROUTE:
            return (FONDI_ROUTE[route], route.lower())
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


# Luce del fuoco: sfondi con candele, camino, lanterne.
FUOCO = ("studio_glauco", "corridoio_ceppo", "cala_notte")
FUOCO_SOLO_SERA = ("vicoli_zefiro",)


def fuoco_per(bg, slot):
    if bg in FUOCO:
        return True
    return bg in FUOCO_SOLO_SERA and slot == "sera"


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


# Effetti di scena (effetti.rpy). (sfondo, effetto, quando): quando = None
# (sempre), "sera" (solo di sera) o "pioggia" (nei giorni di pioggia, mai di
# sera). Vale la prima riga che corrisponde.
EFFETTI_SFONDI = (
    ("esterno_neve", "neve", None),
    ("cala_notte", "lanterne", None),
    ("vicoli_zefiro", "fumo", "sera"),
    ("vicoli_zefiro", "pioggia", "pioggia"),
    ("sala_svelo", "polvere", None),
    ("studio_glauco", "braci", None),
    ("corridoio_ceppo", "braci", None),
    ("arena_athlion", "nevischio", None),
)

# (contesto del calendario, sfondo, effetto, modo): vale solo se anche lo
# sfondo corrisponde. modo "sostituisci" o "aggiungi".
EFFETTI_CONTESTO = (
    # La serra di Glauco (corte di Ofelia e sue scene in serra).
    ("corte", "sala_svelo", "foglie", "sostituisci"),
    ("ofelia_ev1", "sala_svelo", "foglie", "sostituisci"),
    ("specchio_ofelia", "sala_svelo", "foglie", "sostituisci"),
    ("ballo_pretendenti", "sala_svelo", "foglie", "sostituisci"),
    ("incrocio_serra", "sala_svelo", "foglie", "sostituisci"),
    # La fumeria di Icaro.
    ("fumeria", "vicoli_zefiro", "fumo_pipa", "sostituisci"),
    ("icaro_ev1", "vicoli_zefiro", "fumo_pipa", "sostituisci"),
    ("icaro_int1", "vicoli_zefiro", "fumo_pipa", "sostituisci"),
    ("icaro_luna5", "vicoli_zefiro", "fumo_pipa", "sostituisci"),
    ("icaro_febbre", "vicoli_zefiro", "fumo_pipa", "sostituisci"),
    ("athlion", "arena_athlion", "scintille", "aggiungi"),
    ("ofelia_ev3", "arena_athlion", "scintille", "aggiungi"),
)


def effetti_per(bg, slot, contesto, piove, tempesta):
    """Effetti da mostrare, nell'ordine di disegno."""
    base = None
    for sfondo, fx, quando in EFFETTI_SFONDI:
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
    if bg == "vicoli_zefiro" and not piove:
        effetti.append("luccichii")
    for ctx, sfondo, fx, modo in EFFETTI_CONTESTO:
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
