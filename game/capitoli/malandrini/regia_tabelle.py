"""Tabelle di regia del capitolo Malandrini: tinte, luce del fuoco, effetti di
scena e fondi del menu. Le regole che le leggono stanno in game/regia_logic.py
(codice comune), che le riceve come ultimo parametro `tab`.
Nessuna dipendenza da Ren'Py.
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

# Route dell'ultimo finale -> sfondo del menu principale.
FONDI_ROUTE = {
    "Aede": "cala_notte",
    "Caino": "corridoio_ceppo",
    "Druso": "palestra",
    "Icaro": "vicoli_zefiro",
    "Ofelia": "consiglio",
}
# Finale del semestre (senza route): il suo sfondo, senza nessuno al centro.
FINALE_SEMESTRE = "finale_neutro_semestre"
FONDO_SEMESTRE = "esterno_neve"

# Luce del fuoco: sfondi con candele, camino, lanterne.
FUOCO = ("studio_glauco", "corridoio_ceppo", "cala_notte")
FUOCO_SOLO_SERA = ("vicoli_zefiro",)

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

# (sfondo, effetto) aggiunto dopo l'effetto di base quando non piove.
EFFETTI_ASCIUTTO = (("vicoli_zefiro", "luccichii"),)

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
