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
    "rabbia": "avanza", "furia": "avanza", "furioso": "avanza",
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
