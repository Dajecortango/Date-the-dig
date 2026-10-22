# Feedback sulle scelte e ritratti accanto al box.
#
# - Side image: "image side <char>" per i cinque personaggi datable e per
#   Briseide, Vanna e Corrado; le Character relative hanno image="<char>"
#   (nessun ritratto per gli altri).
# - Overlay "feedback_overlay": a ogni interazione confronta le affinità di
#   store con l'ultimo valore visto; se cambiano, il ritratto del personaggio
#   pulsa in un angolo con una riga breve, ~2 s. Nessun numero.
#   Lo snapshot vive in un oggetto non-store (NoRollback, mai riassegnato):
#   non entra nei salvataggi né nel rollback. Si riallinea in silenzio al
#   menu principale (quindi a ogni nuova partita), dopo un caricamento e
#   durante/dopo un rollback (svuotando anche i popup in corso).
#   Con "Animazioni: No" il ritratto resta fermo.

image side aede = "gui/portrait_aede.png"
image side caino = "gui/portrait_caino.png"
image side ofelia = "gui/portrait_ofelia.png"
image side druso = "gui/portrait_druso.png"
image side icaro = "gui/portrait_icaro.png"
# Comprimari del Ceppo di Briseide: solo ritratto, niente feedback affinita'.
image side briseide = "gui/portrait_briseide.png"
image side vanna = "gui/portrait_vanna.png"
image side corrado = "gui/portrait_corrado.png"

## Il ritratto accanto al box solo se lo sprite di chi parla non è in scena.
define config.side_image_only_not_showing = True

init python:
    import time as _fb_time

    # (variabile di store, ritratto, nome)
    FEEDBACK_AFFINITA = [
        ("aede_affinity", "aede", "Aede"),
        ("caino_fiducia", "caino", "Caino"),
        ("druso_affinity", "druso", "Druso"),
        ("icaro_affinity", "icaro", "Icaro"),
        ("ofelia_affinity", "ofelia", "Ofelia"),
    ]
    FEEDBACK_DURATA = 2.2

    class _FeedbackStato(NoRollback):
        """Stato del feedback, fuori dallo store: niente save, niente rollback."""
        def __init__(self):
            self.snap = None      # dict var -> valore, None = da inizializzare
            self.voci = []        # [(serial, char, riga, su, scadenza)]
            self.serial = 0
            self.pendenti = []    # avvisi delle conseguenze: [(char, riga)]

    _fb = _FeedbackStato()

    def _fb_leggi():
        return dict((v, getattr(store, v, None)) for v, _c, _n in FEEDBACK_AFFINITA)

    def _fb_reset():
        _fb.snap = None
        _fb.voci = []
        _fb.pendenti = []

    def feedback_avviso(char, riga):
        """Avviso di una conseguenza (conseguenze.rpy): esce con le righe di
        affinita' alla prossima interazione, e si scarta se lo stesso
        personaggio ha gia' la sua riga. char None = senza ritratto."""
        _fb.pendenti.append((char, riga))

    def _fb_controlla():
        """start_interact_callback: confronta le affinità con lo snapshot."""
        if store.main_menu or store._in_replay:
            _fb_reset()
            return
        cur = _fb_leggi()
        if (_fb.snap is None or renpy.game.after_rollback
                or renpy.in_rollback()):
            _fb.snap = cur
            _fb.voci = []
            _fb.pendenti = []
            return
        ora = _fb_time.time()
        nuovi_char = set()
        if cur == _fb.snap and not _fb.pendenti:
            return
        for v, char, nome in FEEDBACK_AFFINITA:
            a, b = _fb.snap.get(v), cur.get(v)
            if a is None or b is None or a == b:
                continue
            su = b > a
            riga = (nome + " se lo ricorderà.") if su else (nome + " non lo dimenticherà.")
            _fb.serial += 1
            _fb.voci = [x for x in _fb.voci if x[1] != char]
            _fb.voci.append((_fb.serial, char, riga, su, ora + FEEDBACK_DURATA))
            nuovi_char.add(char)
        for char, riga in _fb.pendenti:
            if char in nuovi_char:
                continue
            _fb.serial += 1
            _fb.voci.append((_fb.serial, char, riga, None, ora + FEEDBACK_DURATA))
            nuovi_char.add(char)
        _fb.pendenti = []
        _fb.voci = _fb.voci[-3:]
        _fb.snap = cur

    def _fb_scadi():
        ora = _fb_time.time()
        prima = len(_fb.voci)
        _fb.voci = [x for x in _fb.voci if x[4] > ora]
        if len(_fb.voci) != prima:
            renpy.restart_interaction()

    config.start_interact_callbacks.append(_fb_controlla)
    config.after_load_callbacks.append(_fb_reset)
    config.overlay_screens.append("feedback_overlay")


transform fb_comparsa:
    on show, start:
        alpha 0.0 xoffset -30
        ease 0.25 alpha 1.0 xoffset 0

transform fb_fermo:
    zoom 0.55 transform_anchor True

transform fb_pulsa:
    zoom 0.55 transform_anchor True
    ease 0.25 zoom 0.62
    ease 0.25 zoom 0.55
    ease 0.25 zoom 0.6
    ease 0.25 zoom 0.55

screen feedback_overlay():
    zorder 60

    if _fb.voci and not main_menu:
        timer 0.2 repeat True action Function(_fb_scadi)

        vbox:
            xpos 30 ypos 30
            spacing 10
            for serial, char, riga, su, _scad index serial in _fb.voci:
                frame at fb_comparsa:
                    background Frame("gui/frame_piccolo.png", 26, 26)
                    padding (22, 12, 30, 12)
                    hbox:
                        spacing 12
                        fixed:
                            xysize (100, 100)
                            if char:
                                add cal_portrait(char) at (fb_fermo if mm_movimento_ridotto() else fb_pulsa) align (0.5, 0.5)
                            else:
                                text "◆" size 44 color "#c0392b" align (0.5, 0.5)
                        if su is None:
                            ## Conseguenza: va nella Trama (conseguenze.rpy).
                            vbox:
                                yalign 0.5
                                text "Nella Trama" size 18 italic True color "#a89468"
                                text riga size 26 color "#d9a38a"
                        else:
                            text riga yalign 0.5 size 26 color ("#f0c75e" if su else "#d9c9a8")
