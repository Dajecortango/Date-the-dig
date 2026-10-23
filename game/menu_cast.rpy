# Cast interattivo del menu principale: i cinque personaggi in un carosello
# (uno al centro, i vicini ai lati più piccoli e spenti), vivi (respiro,
# parallasse col mouse, neve) e cliccabili (scheda personaggio).
# Gli sprite sono generati da make_gui.py (menu_cast): gui/cast_<chiave>.png,
# _hover.png, _alone.png (solo alone oro) e _ombra.png, tutti alti
# MM_ALTEZZA px + MM_MARGINE px di bordo per lato.
# Lo stato del carosello vive in variabili della screen (e, per ritrovare la
# stessa posizione tornando dalla scheda, in renpy.session): niente nello
# store, niente nei salvataggi.

default persistent.menu_animato = True

init python:
    import regia_logic as rgl

    MM_MARGINE = 40
    MM_ALTEZZA = 860

    def mm_cast():
        """Cast del carosello: (chiave, fase del respiro, profondità della
        parallasse in px), nell'ordine del giro. Lo dà il capitolo del menu
        (cast_menu= nella registrazione, es. capitoli/malandrini/capitolo.rpy);
        [] se non ne ha."""
        c = rcap.capitolo_menu(persistent.ultimo_capitolo)
        return (c.cast_menu if c is not None else None) or []

    MM_CENTRO_X = 1260      # centro dell'area a destra del pannello (600-1920)
    MM_GIRO = 0.8           # durata della rotazione animata
    MM_AUTO = 4.5           # avanzamento automatico

    # |posto| nel carosello -> (dx, zoom, alpha, saturazione, luminosità).
    MM_POSTI = {
        0: (0, 1.0, 1.0, 1.0, 0.0),
        1: (340, 0.74, 1.0, 0.45, -0.20),
        2: (485, 0.50, 0.70, 0.15, -0.34),
    }

    def mm_rel(i, centro):
        """Posto del personaggio i quando al centro c'è centro: -2..2."""
        n = len(mm_cast())
        if not n:
            return 0
        return (i - centro + n // 2) % n - n // 2

    def mm_posto(rel):
        dx, z, a, sat, lum = MM_POSTI[abs(rel)]
        return (MM_CENTRO_X + (dx if rel >= 0 else -dx), z, a, sat, lum)

    def mm_ordine(centro):
        """(i, voce del cast) dal fondo (bordi) al primo piano (centro)."""
        return sorted(enumerate(mm_cast()), key=lambda e: -abs(mm_rel(e[0], centro)))

    def mm_centro_iniziale():
        # Prima apertura della sessione: al centro il personaggio dell'ultimo
        # finale raggiunto, se ce n'e' uno.
        if "mm_carosello" not in renpy.session:
            chiave = mm_fondo_finale()[1]
            for i, (k, _fase, _prof) in enumerate(mm_cast()):
                if k == chiave:
                    return i
        return renpy.session.get("mm_carosello", 0) % (len(mm_cast()) or 1)

    def mm_fondo_finale():
        """(sfondo, chiave del cast) dell'ultimo finale, con le tabelle del
        capitolo a cui quel finale appartiene; (None, None) se non c'e'."""
        ultimo = persistent.ultimo_finale
        c = rcap.capitolo_di_finale(ultimo)
        if c is None:
            return (None, None)
        return rgl.fondo_menu(ultimo, c.finali, c.regia)

    def mm_fondo():
        """Sfondo della route dell'ultimo finale, sfocato e scurito, o None."""
        bg = mm_fondo_finale()[0]
        if bg is None:
            return None
        return Transform("bg " + bg, blur=12, matrixcolor=BrightnessMatrix(-0.45))

    ## Entrata del cast alla prima apertura del menu nella sessione: uno
    ## dopo l'altro dal basso, poi il carosello di sempre.
    def mm_entrata_attiva():
        return not renpy.session.get("mm_entrata_fatta") and not mm_movimento_ridotto()

    def mm_entrata_fatta():
        renpy.session["mm_entrata_fatta"] = True

    ## Polvere dorata che scende sul menu (stesse particelle della sala dello
    ## Svelo, effetti.rpy), costruita una volta sola.
    class _MMPolvere(NoRollback):
        def __init__(self):
            self.d = None

    _mm_polvere = _MMPolvere()

    def mm_polvere():
        if _mm_polvere.d is None:
            _mm_polvere.d = FxOrologio(_fx_polvere())
        return _mm_polvere.d

    def mm_ricorda(centro):
        renpy.session["mm_carosello"] = centro

    def mm_ruota(scope, centro, nuovo):
        """Azioni per portare il personaggio nuovo al centro. scope e' il
        dizionario delle variabili di menu_cast (locals() nella screen): la
        screen e' inclusa con use, quindi SetScreenVariable scriverebbe in
        main_menu."""
        nuovo %= (len(mm_cast()) or 1)
        return [SetDict(scope, "mm_prima", centro),
                SetDict(scope, "mm_centro", nuovo),
                Function(mm_ricorda, nuovo)]

    def mm_movimento_ridotto():
        # Preferenza "Animazioni" (screen preferences); se Ren'Py
        # aggiunge reduce_motion, rispettiamo anche quella.
        if persistent.menu_animato is False:
            return True
        return bool(getattr(_preferences, "reduce_motion", False))

    def mm_sfondo_pattern():
        # Pattern che scorre, o fermo se le animazioni del menu sono spente.
        if mm_movimento_ridotto():
            return Tile("gui/mm_pattern.png")
        return "mm_pattern_anim"

    def mm_parallasse(profondita):
        def f(trans, st, at):
            x, y = renpy.get_mouse_pos()
            trans.xoffset = -(x - 960) / 960.0 * profondita
            trans.yoffset = -(y - 540) / 540.0 * profondita * 0.3
            return 0
        return f

    def mm_schede():
        """Schede dei personaggi del capitolo del menu ({} se non ce ne sono)."""
        c = rcap.capitolo_menu(persistent.ultimo_capitolo)
        return c.schede if c is not None else {}

    def mm_finali_di(route):
        visti = persistent.finali_visti or set()
        c = rcap.capitolo_menu(persistent.ultimo_capitolo)
        finali = c.finali if c is not None else []
        return [(titolo, fid in visti) for fid, titolo, r, _ind in finali if r == route]


## Posto nel carosello. mm_slot_fermo: subito; mm_slot: ease dal posto di
## prima (la screen passa lo stato del vecchio transform al nuovo);
## mm_slot_rientro: per chi fa il giro da un bordo all'altro, sparisce e
## ricompare al nuovo posto invece di attraversare lo schermo.
transform mm_slot_fermo(x, z, a, sat, lum):
    subpixel True
    xanchor 0.5 yanchor 1.0 ypos (1080 + MM_MARGINE)
    xpos x zoom z alpha a
    matrixcolor SaturationMatrix(sat) * BrightnessMatrix(lum)

transform mm_slot(x, z, a, sat, lum):
    subpixel True
    xanchor 0.5 yanchor 1.0 ypos (1080 + MM_MARGINE)
    ease MM_GIRO xpos x zoom z alpha a matrixcolor SaturationMatrix(sat) * BrightnessMatrix(lum)

transform mm_slot_rientro(x, z, a, sat, lum):
    subpixel True
    xanchor 0.5 yanchor 1.0 ypos (1080 + MM_MARGINE)
    ease (MM_GIRO * 0.4) alpha 0.0
    xpos x zoom z
    matrixcolor SaturationMatrix(sat) * BrightnessMatrix(lum)
    ease (MM_GIRO * 0.6) alpha a

## Alone oro del personaggio al centro.
transform mm_alone_fermo(a):
    alpha a

transform mm_alone(a):
    ease MM_GIRO alpha a

## Respiro (zoom/sollevamento minimi, periodi sfasati) + parallasse col mouse.
transform mm_vivo(fase, profondita):
    subpixel True
    parallel:
        function mm_parallasse(profondita)
    parallel:
        pause fase
        block:
            ease 2.2 zoom 1.006
            ease 2.2 zoom 1.0
            repeat

transform mm_entrata(ritardo):
    alpha 0.0 yoffset 40
    pause ritardo
    ease 0.4 alpha 1.0 yoffset 0

transform mm_fumetto_in:
    alpha 0.0 yoffset 8
    ease 0.18 alpha 1.0 yoffset 0


## Neve leggera sopra il pattern, sotto il pannello.
image mm_neve = Fixed(
    SnowBlossom("gui/fiocco.png", count=26, border=40, xspeed=(15, 45),
                yspeed=(40, 80), start=8, fast=True),
    SnowBlossom(Transform("gui/fiocco.png", zoom=0.55, alpha=0.7), count=34,
                border=40, xspeed=(10, 30), yspeed=(25, 55), start=8, fast=True),
    )


screen menu_cast():

    default mm_centro = mm_centro_iniziale()
    default mm_prima = None

    $ fermo = mm_movimento_ridotto()
    $ sotto = GetTooltip("main_menu")
    ## Su touch non c'e' hover: niente giro automatico (sposterebbe il
    ## personaggio sotto il dito) e nome e route del centro sempre visibili.
    $ mm_touch = renpy.variant("touch")
    $ entrata = mm_entrata_attiva()
    if entrata:
        timer 1.3 action Function(mm_entrata_fatta)

    ## Dal fondo al primo piano: prima i bordi, poi i vicini, il centro sopra.
    ## "index chiave" lega a ogni personaggio i suoi transform anche quando
    ## l'ordine di disegno cambia.

    for i, (chiave, fase, prof) index chiave in mm_ordine(mm_centro):
        $ rel = mm_rel(i, mm_centro)
        $ posto = mm_posto(rel)
        $ al_centro = (rel == 0)
        if mm_prima is None or fermo:
            $ slot = mm_slot_fermo(*posto)
            $ alone = mm_alone_fermo(1.0 if al_centro else 0.0)
        else:
            $ alone = mm_alone(1.0 if al_centro else 0.0)
            if abs(rel - mm_rel(i, mm_prima)) > 2:
                $ slot = mm_slot_rientro(*posto)
            else:
                $ slot = mm_slot(*posto)

        fixed:
            fit_first True
            at ((slot, mm_entrata(0.1 * i)) if entrata else slot)

            fixed:
                fit_first True
                if not fermo:
                    at mm_vivo(fase, prof)

                add ("gui/cast_%s_ombra.webp" % chiave)
                add ("gui/cast_%s_alone.webp" % chiave) at alone
                imagebutton:
                    idle ("gui/cast_%s.webp" % chiave)
                    hover ("gui/cast_%s_hover.webp" % chiave)
                    focus_mask True
                    tooltip chiave
                    alt (mm_schede()[chiave]["nome"] + ((", " + mm_schede()[chiave]["route"]) if al_centro else ""))
                    action (ShowMenu("scheda_personaggio", chiave) if al_centro else mm_ruota(locals(), mm_centro, i))

    ## Avanzamento automatico, in pausa col mouse su un personaggio.
    if not fermo and sotto is None and not mm_touch:
        timer MM_AUTO repeat True action mm_ruota(locals(), mm_centro, mm_centro + 1)

    ## Frecce (a metà altezza del carosello), tastiera e pallini (sotto il
    ## pannello di sinistra, lontani dai personaggi).
    ## Su touch le frecce (76 px, ~4,7 mm) hanno un bordo toccabile in piu'.
    imagebutton:
        idle "gui/mm_freccia_sx.png"
        hover "gui/mm_freccia_sx_hover.png"
        xpos 605 xanchor 0.5 ypos 560 yanchor 0.5
        padding ((24, 24) if mm_touch else (0, 0))
        alt _("Personaggio precedente")
        action mm_ruota(locals(), mm_centro, mm_centro - 1)
    imagebutton:
        idle "gui/mm_freccia_dx.png"
        hover "gui/mm_freccia_dx_hover.png"
        xpos 1872 xanchor 0.5 ypos 560 yanchor 0.5
        padding ((24, 24) if mm_touch else (0, 0))
        alt _("Personaggio successivo")
        action mm_ruota(locals(), mm_centro, mm_centro + 1)
    ## Le frecce restano alla navigazione col focus (tastiera/gamepad tra i
    ## bottoni e il cast): il carosello gira con PagSu/PagGiu e i dorsali.
    key "K_PAGEUP" action mm_ruota(locals(), mm_centro, mm_centro - 1)
    key "K_PAGEDOWN" action mm_ruota(locals(), mm_centro, mm_centro + 1)
    key "pad_leftshoulder_press" action mm_ruota(locals(), mm_centro, mm_centro - 1)
    key "pad_rightshoulder_press" action mm_ruota(locals(), mm_centro, mm_centro + 1)

    frame:
        style "mm_pallini"
        ## Su touch i pallini sono piu' alti: la fila sale per non uscire.
        ypos (1020 if mm_touch else 1042)
        hbox:
            ## Il pallino e' 22 px: il padding allarga la parte toccabile
            ## senza cambiare il disegno (su touch ~3 mm per lato in piu').
            spacing 0
            for i, (chiave, fase, prof) in enumerate(mm_cast()):
                imagebutton:
                    idle ("gui/mm_punto_on.png" if i == mm_centro else "gui/mm_punto.png")
                    hover "gui/mm_punto_on.png"
                    padding ((24, 40) if mm_touch else (5, 4))
                    alt (_("Porta al centro ") + mm_schede()[chiave]["nome"])
                    action mm_ruota(locals(), mm_centro, i)

    ## Fumetto sopra la testa del personaggio sotto il mouse.
    for i, (chiave, fase, prof) in enumerate(mm_cast()):
        if sotto == chiave or (mm_touch and sotto is None and i == mm_centro):
            $ s = mm_schede()[chiave]
            $ px, pz, pa, psat, plum = mm_posto(mm_rel(i, mm_centro))
            frame:
                style "mm_fumetto"
                at mm_fumetto_in
                xpos max(870, min(int(px), 1650)) xanchor 0.5
                ypos int(1080 + MM_MARGINE - (MM_ALTEZZA + MM_MARGINE) * pz + 10) yanchor 1.0
                vbox:
                    spacing 4
                    text s["nome"] style "mm_fumetto_nome"
                    text s["route"] style "mm_fumetto_route"
                    if not mm_touch:
                        text s["battuta"] style "mm_fumetto_battuta"


style mm_pallini is empty
style mm_pallini:
    background Frame("gui/frame_piccolo.png", 26, 26)
    padding (24, 12, 24, 12)
    xpos 310 xanchor 0.5
    ypos 1042 yanchor 0.5

style mm_fumetto is empty
style mm_fumetto:
    background Frame("gui/frame_piccolo.png", 26, 26)
    padding (34, 22, 34, 24)
    xsize 520

style mm_fumetto_nome is text:
    font gui.name_text_font
    size 34
    color gui.accent_color

style mm_fumetto_route is text:
    font gui.interface_text_font
    size 22
    color "#f5e3b8"

style mm_fumetto_battuta is text:
    font gui.text_font
    size 23
    italic True
    color "#d9cfb8"


## Scheda personaggio: ritratto grande, route, difficoltà, profilo e finali
## sbloccati dalla galleria.
screen scheda_personaggio(chiave):

    tag menu

    $ s = mm_schede()[chiave]

    use game_menu(s["nome"]):

        hbox:
            spacing 40

            add ("gui/cast_%s.webp" % chiave):
                fit "contain"
                xysize (380, 760)
                yalign 0.0

            viewport:
                scrollbars "vertical"
                mousewheel True
                draggable True
                xsize 760
                ysize 780

                vbox:
                    spacing 14
                    xsize 720

                    text s["route"] style "scheda_route"
                    text ("Difficoltà: " + s["difficolta"]) style "scheda_voce"
                    text s["nota"] style "scheda_nota"
                    null height 6
                    text s["profilo"] style "scheda_testo"
                    text s["battuta"] style "scheda_nota"

                    null height 12
                    $ finali = mm_finali_di(s["galleria"])
                    $ n_visti = len([f for f in finali if f[1]])
                    $ n_tot = len(finali)
                    text "Finali scoperti: [n_visti] / [n_tot]" style "scheda_voce"
                    for titolo, visto in finali:
                        if visto:
                            text "◆ [titolo]" size 24 color "#e0b75a"
                        else:
                            text "◇ ???" size 24 color "#8a8578"


style scheda_route is text:
    font gui.name_text_font
    size 40
    color gui.accent_color

style scheda_voce is text:
    font gui.interface_text_font
    size 26
    color "#f5e3b8"

style scheda_nota is text:
    font gui.text_font
    size 24
    italic True
    color "#bfb39a"

style scheda_testo is text:
    font gui.text_font
    size 27
    color "#f0e6d2"
