# API comune dei capitoli. Il registro puro vive in capitoli_logic.py; ogni
# capitolo si registra a init 10 nella propria cartella (game/capitoli/<id>/).
# Nello store resta solo l'id (stringa) del capitolo, mai l'oggetto.

init -20 python:
    import capitoli_logic as rcap

default capitolo_corrente = "malandrini"
default persistent.ultimo_capitolo = "malandrini"

init -10 python:
    def capitolo():
        return rcap.ottieni(getattr(store, "capitolo_corrente", None))

    def capitolo_regia():
        """Tabelle di regia del capitolo (per rgl.*), o None."""
        cap = capitolo()
        return cap.regia if cap is not None else None

    def capitolo_ha(funzione):
        if store.main_menu:
            return False
        return rcap.ha(store.capitolo_corrente, funzione)

    def entra_capitolo(cid):
        store.capitolo_corrente = cid
        persistent.ultimo_capitolo = cid

    def _capitoli_dopo_caricamento():
        cap = capitolo()
        if cap is None:
            return
        # Il menu segue l'ultimo capitolo giocato, anche dopo un caricamento.
        persistent.ultimo_capitolo = store.capitolo_corrente
        for f in cap.dopo_caricamento:
            f()

    config.after_load_callbacks.append(_capitoli_dopo_caricamento)

    # Il capitolo dello slot finisce nel json del salvataggio (file_slots).
    def _capitoli_json(d):
        d["capitolo"] = store.capitolo_corrente

    config.save_json_callbacks.append(_capitoli_json)

    _ROMANI = ((10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"))

    def capitolo_romano(n):
        """Numero romano (1..39 bastano); "" se n non e' positivo."""
        n = int(n or 0)
        out = ""
        for valore, cifra in _ROMANI:
            while n >= valore:
                out += cifra
                n -= valore
        return out

    def capitolo_copertina(c, w, h):
        """Illustrazione della carta del capitolo, w x h px: la copertina se
        c'e', altrimenti il fondo del menu (pattern) col cast del capitolo,
        tagliato a mezzo busto."""
        if c is not None and c.copertina:
            return Transform(Transform(c.copertina, fit="cover", xysize=(w, h)),
                             crop=(0, 0, w, h))
        parti = [Tile("gui/mm_pattern.png")]
        cast = (c.cast_menu if c is not None else None) or []
        n = len(cast)
        meta = (n - 1) / 2.0
        # Dal bordo al centro: chi sta in mezzo resta sopra e piu' acceso.
        for i in sorted(range(n), key=lambda j: -abs(j - meta)):
            img = "gui/cast_%s.webp" % cast[i][0]
            if not renpy.loadable(img):
                continue
            zoom = h * 1.3 / float(renpy.image_size(img)[1])
            lum = -0.12 * abs(i - meta)
            parti.append(Transform(img, zoom=zoom, xanchor=0.5,
                                   xpos=int(w * (i + 0.5) / n), ypos=int(h * 0.05),
                                   matrixcolor=BrightnessMatrix(lum)))
        parti.append(Solid("#140a0833"))
        return Transform(Fixed(*parti, xysize=(w, h)), crop=(0, 0, w, h))


## Scelta del capitolo ##########################################################
##
## "Start" del menu principale (screens.rpy, navigation) apre questa screen:
## una carta per capitolo registrato, poi una carta "Prossimamente" che non si
## clicca. Al menu principale la carta avvia il capitolo (Start); in gioco
## (label start, con piu' capitoli) restituisce la label d'ingresso.
## Su telefono (variante small) le carte vanno in colonna.

screen scegli_capitolo():

    tag menu

    use game_menu(_("Capitoli")):

        style_prefix "capitoli"

        $ visti = persistent.finali_visti or set()

        if renpy.variant("small"):
            viewport:
                xfill True
                yfill True
                scrollbars "vertical"
                mousewheel True
                draggable True
                pagekeys True

                vbox:
                    spacing 24
                    xfill True
                    for c in rcap.elenco():
                        use capitolo_carta(c, visti)
                    use capitolo_carta(None, visti)
        elif len(rcap.elenco()) < 3:
            ## Fino a tre carte (con "Prossimamente") stanno nel riquadro:
            ## al centro, senza scorrimento.
            hbox:
                align (0.5, 0.5)
                spacing 30
                for c in rcap.elenco():
                    use capitolo_carta(c, visti)
                use capitolo_carta(None, visti)
        else:
            viewport:
                xfill True
                ysize 640
                yalign 0.5
                scrollbars "horizontal"
                mousewheel "horizontal"
                draggable True

                hbox:
                    spacing 30
                    for c in rcap.elenco():
                        use capitolo_carta(c, visti)
                    use capitolo_carta(None, visti)


## Una carta: c e' un capitolo del registro, o None per "Prossimamente".
screen capitolo_carta(c, visti):

    $ piccolo = renpy.variant("small")
    $ arte_w, arte_h = ((360, 282) if piccolo else (340, 300))

    if c is None:
        frame:
            style "capitoli_carta_spenta"
            use capitolo_carta_corpo(None, (0, 0), arte_w, arte_h, piccolo)
    else:
        $ fv, ft = rcap.finali_contati(c.id, visti)
        button:
            style "capitoli_carta"
            alt ("Capitolo " + capitolo_romano(c.numero) + ": " + c.titolo)
            action (Start(c.ingresso) if main_menu else Return(c.ingresso))
            use capitolo_carta_corpo(c, (fv, ft), arte_w, arte_h, piccolo)


screen capitolo_carta_corpo(c, finali, arte_w, arte_h, piccolo):

    $ fv, ft = finali

    ## Telefono: illustrazione a sinistra, testi a destra. Desktop: in colonna.
    if piccolo:
        hbox:
            spacing 26
            use capitolo_carta_arte(c, arte_w, arte_h)
            vbox:
                yalign 0.5
                spacing 6
                use capitolo_carta_testi(c, fv, ft)
    else:
        vbox:
            spacing 8
            use capitolo_carta_arte(c, arte_w, arte_h)
            null height 4
            use capitolo_carta_testi(c, fv, ft)


screen capitolo_carta_arte(c, arte_w, arte_h):

    fixed:
        xysize (arte_w, arte_h)
        if c is None:
            add Tile("gui/mm_pattern.png"):
                matrixcolor SaturationMatrix(0.15)
            add Solid("#140a0866")
            add "gui/ceralacca.png":
                align (0.5, 0.5)
                zoom 0.8
                alpha 0.7
                matrixcolor SaturationMatrix(0.2)
        else:
            add capitolo_copertina(c, arte_w, arte_h)
            add "gui/ceralacca.png":
                xalign 1.0 yalign 0.0
                offset (10, -10)
                zoom 0.45


screen capitolo_carta_testi(c, fv, ft):

    if c is None:
        text _("Prossimamente") style "capitoli_titolo_spento"
        text _("Altre storie si stanno scrivendo.") style "capitoli_sottotitolo_spento"
    else:
        text ("CAPITOLO " + capitolo_romano(c.numero)) style "capitoli_numero"
        text c.titolo style "capitoli_titolo" substitute False
        if c.sottotitolo:
            text c.sottotitolo style "capitoli_sottotitolo" substitute False
        add "gui/divisore.png":
            xalign (0.0 if renpy.variant("small") else 0.5)
            zoom 0.7
        text ("Finali: %d / %d" % (fv, ft)) style "capitoli_finali"


style capitoli_viewport is viewport
style capitoli_vscrollbar is vscrollbar
style capitoli_scrollbar is scrollbar
style capitoli_vscrollbar:
    unscrollable "hide"
style capitoli_scrollbar:
    unscrollable "hide"

style capitoli_carta is empty
style capitoli_carta:
    xsize 380
    ysize 620
    padding (20, 20, 20, 24)
    background Frame("gui/frame_piccolo.png", 26, 26)
    hover_background Frame(Transform("gui/frame_piccolo.png", matrixcolor=BrightnessMatrix(0.14)), 26, 26)

style capitoli_carta_spenta is capitoli_carta
style capitoli_carta_spenta:
    background Frame(Transform("gui/frame_piccolo.png", matrixcolor=SaturationMatrix(0.0)), 26, 26)

style capitoli_numero is text:
    font gui.interface_text_font
    size 24
    color gui.accent_color
    hover_color gui.hover_color
    xalign 0.5

style capitoli_titolo is text:
    font gui.name_text_font
    size 44
    color "#f5e3b8"
    hover_color gui.hover_color
    outlines [(2, "#140a08", 0, 0)]
    xalign 0.5
    textalign 0.5

style capitoli_sottotitolo is text:
    font gui.text_font
    size 25
    italic True
    color "#d9cfb8"
    xalign 0.5
    textalign 0.5

style capitoli_finali is text:
    font gui.interface_text_font
    size 24
    color "#e0b75a"
    xalign 0.5

style capitoli_titolo_spento is capitoli_titolo:
    size 38
    color "#8a8578"
    hover_color "#8a8578"

style capitoli_sottotitolo_spento is capitoli_sottotitolo:
    color "#8a8578"

## Telefono: carte in colonna, larghe quanto il riquadro, testi piu' grandi.
style capitoli_carta:
    variant "small"
    xsize 1.0
    ysize 330
    padding (22, 22, 30, 22)

style capitoli_numero:
    variant "small"
    size 30
    xalign 0.0

style capitoli_titolo:
    variant "small"
    size 54
    xalign 0.0
    textalign 0.0

style capitoli_sottotitolo:
    variant "small"
    size 31
    xalign 0.0
    textalign 0.0

style capitoli_finali:
    variant "small"
    size 30
    xalign 0.0

style capitoli_titolo_spento:
    variant "small"
    size 50
