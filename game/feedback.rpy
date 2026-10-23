# Feedback sulle scelte e ritratti accanto al box.
#
# - Side image: le righe "image side <char>" sono del capitolo (per
#   Malandrini in game/capitoli/malandrini/ritratti.rpy); le Character
#   relative hanno image="<char>" (nessun ritratto per gli altri).
# - Overlay "feedback_overlay": a ogni interazione confronta le affinità di
#   store (capitolo().affinita: variabile di store, ritratto, nome) con
#   l'ultimo valore visto; se cambiano, il ritratto del personaggio
#   pulsa in un angolo con una riga breve (▲/▼), copiata anche nelle
#   Memorie. Nessun numero. Dura almeno 3.5 s, di piu' se la riga e' lunga,
#   il doppio con la lettura vocale (che la pronuncia). Nel pianificatore
#   va a destra, sotto la Borsa, per non coprire la testata.
#   Lo snapshot vive in un oggetto non-store (NoRollback, mai riassegnato):
#   non entra nei salvataggi né nel rollback. Si riallinea in silenzio al
#   menu principale (quindi a ogni nuova partita), dopo un caricamento e
#   durante/dopo un rollback (svuotando anche i popup in corso).
#   Con "Animazioni: No" il ritratto resta fermo.

## Il ritratto accanto al box solo se lo sprite di chi parla non è in scena.
define config.side_image_only_not_showing = True

init python:
    import time as _fb_time

    FEEDBACK_DURATA = 3.5

    def _fb_durata(riga):
        d = max(FEEDBACK_DURATA, FEEDBACK_DURATA + 0.05 * (len(riga) - 20))
        return d * (2 if _preferences.self_voicing else 1)

    def _fb_affinita():
        """(variabile di store, ritratto, nome) del capitolo corrente."""
        cap = capitolo()
        return cap.affinita if cap is not None else []

    def fb_ritratto(char):
        """Ritratto di char dal capitolo corrente; senza ritratto, niente."""
        cap = capitolo()
        if cap is None or cap.ritratto is None:
            return Null()
        return cap.ritratto(char)

    class _FeedbackStato(NoRollback):
        """Stato del feedback, fuori dallo store: niente save, niente rollback."""
        def __init__(self):
            self.snap = None      # dict var -> valore, None = da inizializzare
            self.voci = []        # [(serial, char, riga, su, scadenza, durata)]
            self.serial = 0
            self.pendenti = []    # avvisi delle conseguenze: [(char, riga)]

    _fb = _FeedbackStato()

    def _fb_leggi():
        return dict((v, rcap.leggi_variabile(store, v)) for v, _c, _n in _fb_affinita())

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
        da_dire = []
        suono = None
        if cur == _fb.snap and not _fb.pendenti:
            return
        for v, char, nome in _fb_affinita():
            a, b = _fb.snap.get(v), cur.get(v)
            if a is None or b is None or a == b:
                continue
            su = b > a
            # Freccia + verbi opposti: il verso si legge anche senza colore.
            # ▲/▼ ci sono in EBGaramond (non in Cinzel).
            riga = ("▲ " + nome + " ti si avvicina.") if su else ("▼ " + nome + " prende le distanze.")
            # Resta anche nelle Memorie, dopo che il riquadro sparisce.
            narrator.add_history("adv", None, riga)
            _fb.serial += 1
            _fb.voci = [x for x in _fb.voci if x[1] != char]
            _fb.voci.append((_fb.serial, char, riga, su, ora + _fb_durata(riga), _fb_durata(riga)))
            nuovi_char.add(char)
            da_dire.append(riga)
            if suono is None or not su:
                suono = "audio/affetto_su.ogg" if su else "audio/affetto_giu.ogg"
        for char, riga in _fb.pendenti:
            if char in nuovi_char:
                continue
            _fb.serial += 1
            _fb.voci.append((_fb.serial, char, riga, None, ora + _fb_durata(riga), _fb_durata(riga)))
            nuovi_char.add(char)
            da_dire.append("Nella Trama: " + riga)
            suono = "audio/sigillo.ogg"
        _fb.pendenti = []
        _fb.voci = _fb.voci[-3:]
        _fb.snap = cur
        # Lettura vocale: l'overlay non ha focus, quindi la riga si dice qui.
        if da_dire and _preferences.self_voicing:
            renpy.display.tts.speak(" ".join(r.lstrip("▲▼ ") for r in da_dire),
                                    translate=False)
        # Un solo suono per interazione: conseguenza > distanza > vicinanza.
        if suono and not renpy.is_skipping():
            renpy.play(suono)

    def _fb_scadi():
        ora = _fb_time.time()
        prima = len(_fb.voci)
        _fb.voci = [x for x in _fb.voci if x[4] > ora]
        if len(_fb.voci) != prima:
            renpy.restart_interaction()

    config.start_interact_callbacks.append(_fb_controlla)
    config.after_load_callbacks.append(_fb_reset)
    config.overlay_screens.append("feedback_overlay")


# Entra veloce e frena (easein_quart); esce da sola poco prima della scadenza (la voce
# tolta dalla lista non riceve "on hide": senza uscita sparirebbe di netto).
transform fb_comparsa(durata=FEEDBACK_DURATA):
    on show, start:
        alpha 0.0 xoffset -30
        easein_quart 0.25 alpha 1.0 xoffset 0
        pause (durata - 0.55)
        easeout 0.25 alpha 0.0 xoffset -16

transform fb_fermo:
    zoom 0.55 transform_anchor True

transform fb_fermo_diamante:
    zoom 1.0

transform fb_pulsa:
    zoom 0.55 transform_anchor True
    ease 0.25 zoom 0.62
    ease 0.25 zoom 0.55
    ease 0.25 zoom 0.6
    ease 0.25 zoom 0.55

# ▼: il ritratto scende e si spegne, niente battito allegro.
transform fb_cala:
    zoom 0.55 transform_anchor True matrixcolor SaturationMatrix(1.0)
    easein 0.35 yoffset 6 matrixcolor SaturationMatrix(0.35)

# Conseguenza: il diamante batte una volta, deciso.
transform fb_avviso:
    zoom 1.25
    easein_back 0.3 zoom 1.0

screen feedback_overlay():
    zorder 60

    if _fb.voci and not main_menu:
        timer 0.2 repeat True action Function(_fb_scadi)

        ## Nel pianificatore la testata e' in alto a sinistra: a destra,
        ## sotto la pillola della Borsa.
        $ fb_destra = renpy.get_screen("pianificazione") is not None
        vbox:
            xpos (1890 if fb_destra else 30)
            xanchor (1.0 if fb_destra else 0.0)
            ypos ((160 if renpy.variant("small") else 110) if fb_destra else 30)
            spacing 10
            for serial, char, riga, su, _scad, durata index serial in _fb.voci:
                frame at fb_comparsa(durata):
                    background Frame("gui/frame_piccolo.png", 26, 26)
                    padding (22, 12, 30, 12)
                    hbox:
                        spacing 12
                        fixed:
                            xysize (100, 100)
                            if char:
                                add fb_ritratto(char) at (fb_fermo if mm_movimento_ridotto() else fb_pulsa if su is not False else fb_cala) align (0.5, 0.5)
                            else:
                                text "◆" size 44 color "#c0392b" align (0.5, 0.5) at (fb_fermo_diamante if mm_movimento_ridotto() else fb_avviso)
                        if su is None:
                            ## Conseguenza: va nella Trama (conseguenze.rpy).
                            vbox:
                                yalign 0.5
                                text "Nella Trama" size 20 italic True color "#a89468"
                                text riga size 26 color "#d9a38a"
                        else:
                            text riga yalign 0.5 size 26 color ("#f0c75e" if su else "#d9c9a8")
