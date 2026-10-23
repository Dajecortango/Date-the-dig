################################################################################
## Initialization
################################################################################

init offset = -1


################################################################################
## Styles
################################################################################

style default:
    properties gui.text_properties()
    language gui.language

style input:
    properties gui.text_properties("input", accent=True)
    adjust_spacing False

style hyperlink_text:
    properties gui.text_properties("hyperlink", accent=True)
    hover_underline True

style gui_text:
    properties gui.text_properties("interface")


style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.text_properties("button")
    yalign 0.5


style label_text is gui_text:
    properties gui.text_properties("label", accent=True)

style prompt_text is gui_text:
    properties gui.text_properties("prompt")


style bar:
    ysize gui.bar_size
    left_bar Frame("gui/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    ysize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    xsize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

## Slider: binario d'oro inciso, smalto rosso a sinistra del cursore
## (una losanga di rubino), scanalatura vuota a destra.
style slider:
    ysize gui.slider_size
    left_bar Frame("gui/slider/horizontal_[prefix_]pieno.png", gui.slider_borders, tile=gui.slider_tile)
    right_bar Frame("gui/slider/horizontal_[prefix_]vuoto.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/slider/horizontal_[prefix_]thumb.png"
    thumb_offset 18

style vslider:
    xsize gui.slider_size
    top_bar Frame("gui/slider/vertical_[prefix_]vuoto.png", gui.vslider_borders, tile=gui.slider_tile)
    bottom_bar Frame("gui/slider/vertical_[prefix_]pieno.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"
    thumb_offset 18


## Cornice miniata: gli ornamenti d'angolo stanno nei 60 px di bordo.
style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", 60, 60, tile=gui.frame_tile)



################################################################################
## In-game screens
################################################################################


## Say screen ##################################################################
##
## The say screen is used to display dialogue to the player. It takes two
## parameters, who and what, which are the name of the speaking character and
## the text to be displayed, respectively. (The who parameter can be None
## if no name is given.)
##
## This screen must create a text displayable with id "what", as Ren'Py
## uses this to manage text display. It can also create displayables with
## id "who" and id "window" to apply style properties.
##
## https://www.renpy.org/doc/html/screen_special.html#say

## Indicatore click-to-continue: diamantino oro che pulsa e ondeggia, in coda
## al testo (ctc_continua, regia.rpy).
image ctc_diamante:
    "gui/ctc.png"
    subpixel True
    parallel:
        alpha 0.2
        linear 0.7 alpha 1.0
        linear 0.7 alpha 0.2
        repeat
    parallel:
        yoffset 0
        easein 0.7 yoffset -3
        easeout 0.7 yoffset 0
        repeat

## Box che entra: sale di poco e compare quando la finestra si mostra, non a
## ogni battuta (on replace non fa niente).
transform box_entra:
    on show:
        alpha 0.0 yoffset (0 if mm_movimento_ridotto() else 20)
        easein 0.25 alpha 1.0 yoffset 0
    on replace:
        alpha 1.0 yoffset 0

## Colori dei personaggi per il diamante del namebox.
init python:
    CHAR_COLORS = {
        "Aede": "#c0392b", "Caino": "#c87a30", "Druso": "#8a9bb0",
        "Icaro": "#7fa06a", "Glauco Severo": "#6b6b6b",
        "Briseide Ippodamia": "#b8860b", "Vanna": "#8fbc8f",
        "Corrado": "#87a7c7", "Ofelia": "#7d3c98",
        "Lenora": "#a8a8c0", "Pandora": "#c98fa0",
    }

    def char_color(who):
        return CHAR_COLORS.get(who, "#d4af37")

screen say(who, what):

    window:
        id "window"
        at box_entra

        if who is not None:

            window:
                id "namebox"
                style "namebox"
                hbox:
                    spacing 10
                    text "◆" size 20 yalign 0.5 color char_color(who)
                    text who id "who"

        text what id "what"


    ## If there's a side image, display it above the text. Do not display
    ## on the phone variant - there's no room.
    if not renpy.variant("small"):
        # Ritratto di chi parla (image side <char>, feedback.rpy): sul bordo
        # destro del box, a cavallo della cornice; la namebox resta libera.
        add SideImage() xpos 1880 xanchor 1.0 ypos (1080 - gui.textbox_height + 52) yanchor 1.0


## Make the namebox available for styling through the Character object.
init python:
    config.character_id_prefixes.append('namebox')

style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label


style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    background Image("gui/textbox.png", xalign=0.5, yalign=1.0)

style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height

    background Frame("gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

style say_label:
    properties gui.text_properties("name", accent=True)
    xalign gui.name_xalign
    yalign 0.5
    outlines [(2, "#140a08", 0, 0)]

style say_dialogue:
    properties gui.text_properties("dialogue")

    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos

    adjust_spacing False
    # Contorno sottile e ombra morbida: leggibile anche sulla neve.
    outlines [(2, "#140a08", 0, 0), (3, "#14080860", 1, 2)]

## Input screen ################################################################
##
## This screen is used to display renpy.input. The prompt parameter is used
## to pass a text prompt in.
##
## This screen must create an input displayable with id "input" to accept
## the various input parameters.
##
## https://www.renpy.org/doc/html/screen_special.html#input

screen input(prompt):
    style_prefix "input"

    window:

        vbox:
            xanchor gui.dialogue_text_xalign
            xpos gui.dialogue_xpos
            xsize gui.dialogue_width
            ypos gui.dialogue_ypos

            text prompt style "input_prompt"
            input id "input"

style input_prompt is default

style input_prompt:
    xalign gui.dialogue_text_xalign
    properties gui.text_properties("input_prompt")

style input:
    xalign gui.dialogue_text_xalign
    xmaximum gui.dialogue_width


## Choice screen ###############################################################
##
## This screen is used to display the in-game choices presented by the
## menu statement. The one parameter, items, is a list of objects, each
## with caption and action fields.
##
## https://www.renpy.org/doc/html/screen_special.html#choice

screen choice(items):
    style_prefix "choice"

    $ scelte_ferme = mm_movimento_ridotto() or renpy.is_skipping()

    vbox:
        for n, i in enumerate(items):
            # peso=True (argomento di menu): scelta che pesa, diamante rosso.
            $ peso = i.kwargs.get("peso", False)
            button:
                action i.action
                # Entrano in cascata dall'alto, poi rispondono all'hover.
                at (scelta_hover_fermo if scelte_ferme else scelta_hover), (scelta_ferma if scelte_ferme else scelta_entra(n * 0.05))
                hbox:
                    xalign 0.5
                    spacing 16
                    if peso:
                        text "◆" style "choice_peso" yalign 0.5
                    # Scelta gia' presa (in questa o in una partita
                    # precedente): fogliolina d'oro e testo d'oro spento.
                    # Dice solo "gia' percorsa", mai dove porta.
                    if getattr(i, "chosen", False):
                        add "gui/scelta_vista.png" yalign 0.5 alpha 0.7
                        text i.caption style "choice_button_text" idle_color "#b3a173" hover_color "#f5e3b8" yalign 0.5
                        null width 24
                    else:
                        text i.caption style "choice_button_text" yalign 0.5
                    if peso:
                        text "◆" style "choice_peso" yalign 0.5


# Hover delle scelte: allargamento lieve e passo a destra (lo sfondo hover ha
# il bordo oro e l'alone, style choice_button).
transform scelta_hover_fermo:
    xalign 0.5

transform scelta_hover:
    xalign 0.5
    transform_anchor True
    on idle:
        ease 0.12 zoom 1.0 xoffset 0
    on hover:
        ease 0.12 zoom 1.04 xoffset 10

transform scelta_ferma:
    alpha 1.0

transform scelta_entra(ritardo):
    alpha 0.0 xoffset -16
    pause ritardo
    ease 0.18 alpha 1.0 xoffset 0

style choice_peso is default:
    font gui.text_font
    size 20
    color "#c0392b"
    outlines [(1, "#d4af37", 0, 0)]


style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos gui.scale(270)
    yanchor 0.5

    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")
    hover_background Fixed(
        Transform("gui/scelta_bagliore.png", align=(0.5, 0.5)),
        Frame("gui/button/choice_hover_background.png", gui.choice_button_borders, tile=gui.choice_button_tile))
    hover_sound "audio/scelta.ogg"

style choice_button_text is default:
    properties gui.text_properties("choice_button")


## Quick Menu screen ###########################################################
##
## The quick menu is displayed in-game to provide easy access to the
## out-of-game menus.

## Sigilli di ceralacca (make_gui.py: sigilli_quick) appuntati sul bordo
## superiore del box, a destra dello stemma; nel pianificatore scendono
## nell'angolo in basso a destra, sotto il pannello. Tooltip in italiano
## sopra il sigillo sotto il mouse.

init python:
    # (immagine in gui/quick/, tooltip)
    QUICK_SIGILLI = [
        ("indietro", _("Indietro")),
        ("memorie", _("Memorie")),
        ("salta", _("Salta")),
        ("auto", _("Avanzamento automatico")),
        ("salva", _("Salva")),
        ("qsalva", _("Salvataggio rapido")),
        ("qcarica", _("Caricamento rapido")),
        ("costumanze", _("Costumanze")),
        ("borsa", _("Borsa e oggetti")),
    ]
    # Su telefono sei sigilli, grandi abbastanza per il dito (~9 mm): i
    # salvataggi rapidi restano nel menu Salva/Carica, la Borsa si apre dalla
    # pillola degli Scudi in alto a destra.
    if renpy.variant("small"):
        QUICK_SIGILLI = [q for q in QUICK_SIGILLI
                         if q[0] not in ("qsalva", "qcarica", "borsa")]
    # Su touch non c'e' tooltip: sopra ogni sigillo un'etichetta corta (i
    # tooltip interi non ci stanno nei 96 px del sigillo).
    QUICK_ETICHETTE = {
        "indietro": _("Indietro"),
        "memorie": _("Memorie"),
        "salta": _("Salta"),
        "auto": _("Auto"),
        "salva": _("Salva"),
        "qsalva": _("Q.salva"),
        "qcarica": _("Q.carica"),
        "costumanze": _("Opzioni"),
        "borsa": _("Borsa"),
    }
    # Su telefono i sigilli (60 px nel png) si ingrandiscono: a 1920x1080
    # su un 6" servono ~112 px virtuali per un bersaglio da ~9 mm.
    QUICK_LATO = 112 if renpy.variant("small") else 60
    QUICK_SPAZIO = 14 if renpy.variant("small") else 10
    QUICK_ETICHETTA_H = 32 if renpy.variant("small") else 26

    def quick_azione(chiave):
        return {
            "indietro": Rollback(),
            "memorie": ShowMenu("history"),
            "salta": Skip(),
            "auto": Preference("auto-forward", "toggle"),
            "salva": ShowMenu("save"),
            "qsalva": QuickSave(),
            "qcarica": QuickLoad(),
            "costumanze": ShowMenu("preferences"),
            "borsa": ShowMenu("inventario"),
        }[chiave]

    def quick_posizione():
        """(x, y) dell'angolo in alto a sinistra della fila, o None se il
        menu rapido va nascosto. Nascosto solo sul cartello di data (dura un
        attimo e prosegue da solo) e sull'input del nome (salvare o tornare
        indietro a meta' digitazione non ha senso, e la fila coprirebbe il
        campo). Ovunque altro (dialoghi, scelte, transizioni, centered, nvl)
        resta alla posizione del dialogo, cosi' non salta tra una battuta e
        una pausa; nel pianificatore scende in basso."""
        if renpy.get_screen("cartello_data") or renpy.get_screen("input"):
            return None
        if renpy.get_screen("pianificazione"):
            return (min(1530 - quick_larghezza() // 2, 1890 - quick_larghezza()),
                    min(996, 1076 - QUICK_LATO))
        return (min(1130, 1880 - quick_larghezza()),
                1080 - gui.textbox_height + 14 - QUICK_LATO // 2)

    def quick_larghezza():
        n = len(QUICK_SIGILLI)
        return n * QUICK_LATO + (n - 1) * QUICK_SPAZIO

screen quick_menu():

    ## Ensure this appears on top of other screens.
    zorder 100

    $ qpos = quick_posizione() if quick_menu else None

    if qpos is not None:

        hbox:
            style_prefix "quick"
            pos qpos
            spacing QUICK_SPAZIO

            for chiave, suggerimento in QUICK_SIGILLI:
                imagebutton:
                    auto "gui/quick/" + chiave + "_%s.png"
                    action quick_azione(chiave)
                    alternate (Skip(fast=True, confirm=True) if chiave == "salta" else None)
                    tooltip suggerimento
                    at (quick_fermo if mm_movimento_ridotto() else quick_hover), quick_scala

        if renpy.variant("touch"):
            hbox:
                pos (qpos[0], qpos[1] - QUICK_ETICHETTA_H)
                spacing QUICK_SPAZIO
                for chiave, _s in QUICK_SIGILLI:
                    fixed:
                        xysize (QUICK_LATO, QUICK_ETICHETTA_H)
                        text QUICK_ETICHETTE[chiave] style "quick_etichetta_text"

        $ qtt = GetTooltip("quick_menu")
        $ qtesti = [s for _c, s in QUICK_SIGILLI]
        if qtt in qtesti:
            $ qidx = qtesti.index(qtt)
            frame:
                style "quick_tooltip"
                xpos qpos[0] + qidx * (QUICK_LATO + QUICK_SPAZIO) + QUICK_LATO // 2
                ypos qpos[1] - 6
                text qtt style "quick_tooltip_text"


transform quick_scala:
    zoom QUICK_LATO / 60.0

## Hover dei sigilli: si sollevano appena.
transform quick_fermo:
    yoffset 0

transform quick_hover:
    on idle, selected_idle, insensitive:
        ease 0.12 yoffset 0
    on hover, selected_hover:
        ease 0.12 yoffset -4


## This code ensures that the quick_menu screen is displayed in-game, whenever
## the player has not explicitly hidden the interface.
init python:
    config.overlay_screens.append("quick_menu")

default quick_menu = True

style quick_tooltip is empty
style quick_tooltip:
    xanchor 0.5
    yanchor 1.0
    background Frame("gui/frame_piccolo.png", 26, 26)
    padding (24, 10, 24, 10)

style quick_tooltip_text is gui_text
style quick_tooltip_text:
    size 21
    color "#f5e3b8"
    outlines [(2, "#140a08", 0, 0)]

style quick_etichetta_text is quick_tooltip_text
style quick_etichetta_text:
    size 14
    layout "nobreak"
    xalign 0.5
    yalign 1.0
    textalign 0.5

## Su telefono l'etichetta e' l'unica guida (niente tooltip): leggibile.
style quick_etichetta_text:
    variant "small"
    size 20

style quick_button is default
style quick_button_text is button_text

style quick_button:
    properties gui.button_properties("quick_button")

style quick_button_text:
    properties gui.text_properties("quick_button")
    outlines [(2, "#140a08", 0, 0)]


################################################################################
## Main and Game Menu Screens
################################################################################

## Navigation screen ###########################################################
##
## This screen is included in the main and game menus, and provides navigation
## to other menus, and to start the game.

screen navigation():

    vbox:
        style_prefix "navigation"

        # Centrata: nel pannello del menu principale (x 60-560) o nella
        # colonna del menu di gioco (larga 360 + margine: il nastro di
        # "Riprendi la Cronaca" ci sta).
        xpos (310 if main_menu else 200)
        xanchor 0.5
        yalign 0.5

        spacing gui.navigation_spacing

        if main_menu:

            ## Continua: carica il salvataggio più recente (pagine, auto, quick).
            $ ultimo_slot = renpy.newest_slot(r"\d+-\d+|auto-|quick-")
            if ultimo_slot is not None:
                textbutton _("Continua") action FileLoad(ultimo_slot, slot=True, confirm=False)

            textbutton _("Start") action Start()

        else:

            textbutton _("Diario") action ShowMenu("diario")

            textbutton _("Cronache") action ShowMenu("cronache")

            textbutton _("Trama") action ShowMenu("trama")

            textbutton _("Borsa") action ShowMenu("inventario")

            textbutton _("History") action ShowMenu("history")

            textbutton _("Save") action ShowMenu("save")

        textbutton _("Load") action ShowMenu("load")

        if main_menu:

            textbutton _("Finali") action ShowMenu("galleria_finali")

        textbutton _("Preferences") action ShowMenu("preferences")

        if _in_replay:

            textbutton _("End Replay") action EndReplay(confirm=True)

        elif not main_menu:

            textbutton _("Main Menu") action MainMenu()

        textbutton _("About") action ShowMenu("about")

        if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):

            ## Help isn't necessary or relevant to mobile devices.
            textbutton _("Help") action ShowMenu("help")

        if renpy.variant("pc"):

            ## The quit button is banned on iOS and unnecessary on Android and Web.
            textbutton _("Quit") action Quit(confirm=not main_menu)


style navigation_button is gui_button
style navigation_button_text is gui_button_text

style navigation_button:
    size_group "navigation"
    xalign 0.5
    properties gui.button_properties("navigation_button")

style navigation_button_text:
    xalign 0.5
    text_align 0.5
    properties gui.text_properties("navigation_button")
    outlines [(2, "#140a08", 0, 0)]


## Main Menu screen ############################################################
##
## Used to display the main menu when Ren'Py starts.
##
## https://www.renpy.org/doc/html/screen_special.html#main-menu

## Pattern del menu che scorre piano sotto il pannello fisso.
## Tre copie affiancate (Tile riempirebbe solo i 1920 px offerti, lasciando
## nero a destra quando scorre).
image mm_pattern_anim:
    Composite((3460, 1080),
        (0, 0), "gui/mm_pattern.png",
        (1540, 0), "gui/mm_pattern.png",
        (3080, 0), "gui/mm_pattern.png")
    subpixel True
    xoffset -1540
    linear 60.0 xoffset 0
    repeat

screen main_menu():

    ## This ensures that any other menu screen is replaced.
    tag menu

    add mm_sfondo_pattern()
    ## Dopo un finale: lo sfondo della sua route, sfocato (menu_cast.rpy).
    $ mm_sfondo_finale = mm_fondo()
    if mm_sfondo_finale is not None:
        add mm_sfondo_finale
    if not mm_movimento_ridotto():
        add "mm_neve"
        add mm_polvere()
    add "gui/mm_front.png"

    ## This empty frame darkens the main menu.
    frame:
        style "main_menu_frame"

    ## Cast cliccabile e vivo (game/menu_cast.rpy).
    use menu_cast

    ## The use statement includes another screen inside this one. The actual
    ## contents of the main menu are in the navigation screen.
    use navigation

    if gui.show_name:

        vbox:
            style "main_menu_vbox"

            ## Titolo con un alone oro che respira dietro.
            fixed:
                fit_first True
                xalign 0.5
                text "[config.name!t]":
                    style "main_menu_title"
                    color gui.accent_color
                    at (mm_titolo_spento if mm_movimento_ridotto() else mm_titolo_respira)
                text "[config.name!t]":
                    style "main_menu_title"

        ## Versione in fondo al pannello, lontana dal primo pulsante.
        text "[config.version]":
            style "main_menu_version"
            xpos 310 xanchor 0.5 ypos 968 yanchor 1.0


transform mm_titolo_spento:
    alpha 0.0

transform mm_titolo_respira:
    blur 8
    alpha 0.35
    block:
        ease 1.6 alpha 0.9
        ease 1.6 alpha 0.35
        repeat

style main_menu_frame is empty
style main_menu_vbox is vbox
style main_menu_text is gui_text
style main_menu_title is main_menu_text
style main_menu_version is main_menu_text

style main_menu_frame:
    xsize gui.scale(280)
    yfill True

    background "gui/overlay/main_menu.png"

style main_menu_vbox:
    xpos 310
    xanchor 0.5
    xmaximum gui.scale(420)
    ypos gui.scale(128)

style main_menu_title:
    xalign 0.5
    text_align 0.5
    color "#3f2d1a"
    size gui.scale(46)

style main_menu_version:
    xalign 0.5
    color "#6b5335"

style main_menu_text:
    properties gui.text_properties("main_menu", accent=True)

style main_menu_title:
    properties gui.text_properties("title")

style main_menu_version:
    properties gui.text_properties("version")


## Game Menu screen ############################################################
##
## This lays out the basic common structure of a game menu screen. It's called
## with the screen title, and displays the background, title, and navigation.
##
## The scroll parameter can be None, or one of "viewport" or "vpgrid".
## This screen is intended to be used with one or more children, which are
## transcluded (placed) inside it.

screen game_menu(title, scroll=None, yinitial=0.0, spacing=0):

    style_prefix "game_menu"

    ## Dal menu principale: il pannello di sinistra resta (navigazione,
    ## titolo sulla pergamena, ritorno in fondo) e il contenuto va in un
    ## riquadro a destra, senza sovrapporsi. In gioco: layout classico.
    if main_menu:
        add mm_sfondo_pattern()
        add "gui/mm_front.png"
    else:
        add gui.game_menu_background

    frame:
        style ("game_menu_outer_frame_mm" if main_menu else "game_menu_outer_frame")

        hbox:

            ## Reserve space for the navigation section.
            if not main_menu:
                frame:
                    style "game_menu_navigation_frame"

            frame:
                style ("game_menu_content_frame_mm" if main_menu else "game_menu_content_frame")

                if scroll == "viewport":

                    viewport:
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        vbox:
                            spacing spacing

                            transclude

                elif scroll == "vpgrid":

                    vpgrid:
                        cols 1
                        yinitial yinitial

                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        spacing spacing

                        transclude

                else:

                    transclude

    use navigation

    textbutton _("Return"):
        style ("return_button_mm" if main_menu else "return_button")

        action Return()

    if main_menu:
        label title style "game_menu_label_mm" text_style "game_menu_label_mm_text"
    else:
        label title

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar

style game_menu_label is gui_label
style game_menu_label_text is gui_label_text

style return_button is navigation_button
style return_button_text is navigation_button_text

style game_menu_outer_frame:
    bottom_padding gui.scale(30)
    top_padding gui.scale(120)

    background "gui/overlay/game_menu.png"

style game_menu_navigation_frame:
    xsize gui.scale(360)
    yfill True

style game_menu_content_frame:
    left_margin gui.scale(40)
    right_margin gui.scale(40)
    top_margin gui.scale(10)
    xfill True
    yfill True
    background Frame("gui/frame.png", 60, 60)
    padding (44, 34, 34, 34)

## Dal menu principale la cornice e' gia' quella esterna (outer_frame_mm).
style game_menu_content_frame_mm is game_menu_content_frame
style game_menu_content_frame_mm:
    background None
    padding (0, 0, 0, 0)

style game_menu_viewport:
    xsize gui.scale(920)

style game_menu_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side:
    spacing gui.scale(10)

style game_menu_label:
    xpos gui.scale(50)
    ysize gui.scale(120)

style game_menu_label_text:
    size gui.title_text_size
    color gui.accent_color
    yalign 0.5
    outlines [(3, "#140a08", 0, 0)]

style return_button:
    xpos 200
    xanchor 0.5
    yalign 1.0
    yoffset gui.scale(-30)

## Varianti per i menu aperti dal menu principale. Il pannello di
## mm_front.png occupa x 60-560, y 80-1000; la pergamena x 85-535, y 105-290.
style game_menu_outer_frame_mm is empty
style game_menu_outer_frame_mm:
    xpos 600
    ypos 80
    xsize 1280
    ysize 920
    background Frame("gui/frame.png", 60, 60)
    padding (20, 40, 30, 30)

style game_menu_label_mm is gui_label
style game_menu_label_mm:
    xpos 310
    xanchor 0.5
    ypos 197
    yanchor 0.5
    xmaximum 410

style game_menu_label_mm_text is gui_label_text
style game_menu_label_mm_text:
    size 42
    color "#3f2d1a"
    textalign 0.5
    xalign 0.5
    layout "subtitle"

style return_button_mm is return_button
style return_button_mm_text is return_button_text
style return_button_mm:
    xpos 310
    xanchor 0.5
    yalign 1.0
    yoffset -100


## About screen ################################################################
##
## This screen gives credit and copyright information about the game and
## Ren'Py.
##
## There's nothing special about this screen, and hence it also serves as an
## example of how to make a custom screen.

screen about():

    tag menu

    ## This use statement includes the game_menu screen inside this one.
    ## The vbox child is then included inside the viewport inside the
    ## game_menu screen.
    use game_menu(_("About"), scroll="viewport"):

        style_prefix "about"

        vbox:

            label "[config.name!t]"
            text _("Version [config.version!t]\n")

            ## gui.about is usually set in options.rpy.
            if gui.about:
                text "[gui.about!t]\n"

            text _("Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]")


style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_text_size


## Load and Save screens #######################################################
##
## These screens are responsible for letting the player save the game and
## load it again. Since they share nearly everything in common, both
## are implemented in terms of a third screen, file_slots.
##
## https://www.renpy.org/doc/html/screen_special.html#save
## https://www.renpy.org/doc/html/screen_special.html#load

screen save():

    tag menu

    use file_slots(_("Save"))


screen load():

    tag menu

    use file_slots(_("Load"))


screen file_slots(title):

    default page_name_value = FilePageNameInputValue(pattern=_("Page {}"), auto=_("Automatic saves"), quick=_("Quick saves"))

    use game_menu(title):

        fixed:

            ## This ensures the input will get the enter
            ## event before any of the buttons do.
            order_reverse True

            ## The page name, which can be edited by clicking on a button.
            button:
                style "page_label"

                key_events True
                xalign 0.5
                action page_name_value.Toggle()

                input:
                    style "page_label_text"
                    value page_name_value

            ## The grid of file slots.
            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"

                xalign 0.5
                yalign 0.5

                spacing gui.slot_spacing

                for i in range(gui.file_slot_cols * gui.file_slot_rows):

                    $ slot = i + 1

                    button:
                        action FileAction(slot)

                        has vbox

                        fixed:
                            xysize (config.thumbnail_width, config.thumbnail_height)
                            xalign 0.5
                            add FileScreenshot(slot)
                            ## Ritratto della route attiva al momento del salvataggio.
                            $ slot_route = FileJson(slot, "route")
                            if slot_route:
                                add Transform(cal_portrait(slot_route), zoom=0.36) align (1.0, 1.0) offset (6, 6)

                        text FileTime(slot, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("empty slot")):
                            style "slot_time_text"

                        text FileSaveName(slot):
                            style "slot_name_text"

                        key "save_delete" action FileDelete(slot)

            ## Buttons to access other pages.
            vbox:
                style_prefix "page"

                xalign 0.5
                yalign 1.0

                hbox:
                    xalign 0.5

                    spacing gui.page_spacing

                    textbutton _("<") action FilePagePrevious()
                    key "save_page_prev" action FilePagePrevious()

                    if config.has_autosave:
                        textbutton _("{#auto_page}A") action FilePage("auto")

                    if config.has_quicksave:
                        textbutton _("{#quick_page}Q") action FilePage("quick")

                    ## range(1, 10) gives the numbers from 1 to 9.
                    for page in range(1, 10):
                        textbutton "[page]" action FilePage(page)

                    textbutton _(">") action FilePageNext()
                    key "save_page_next" action FilePageNext()

                if config.has_sync:
                    if CurrentScreenName() == "save":
                        textbutton _("Upload Sync"):
                            action UploadSync()
                            xalign 0.5
                    else:
                        textbutton _("Download Sync"):
                            action DownloadSync()
                            xalign 0.5


style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_button
style page_button_text is gui_button_text

style slot_button is gui_button
style slot_button_text is gui_button_text
style slot_time_text is slot_button_text
style slot_name_text is slot_button_text

style page_label:
    xpadding gui.scale(50)
    ypadding gui.scale(3)

style page_label_text:
    textalign 0.5
    layout "subtitle"
    hover_color gui.hover_color

style page_button:
    properties gui.button_properties("page_button")

style page_button_text:
    properties gui.text_properties("page_button")

style slot_button:
    properties gui.button_properties("slot_button")

style slot_button_text:
    properties gui.text_properties("slot_button")

## Cornice dello slot: placca dorata, gemme negli angoli (bordi 28 px).
style slot_button:
    background Frame("gui/button/slot_[prefix_]background.png", 28, 28)

## Il nome del salvataggio (Luna e giorno, da cal_loop) in oro.
style slot_name_text:
    color "#e0b75a"
    size 17


## Preferences screen ##########################################################
##
## The preferences screen allows the player to configure the game to better
## suit themselves.
##
## https://www.renpy.org/doc/html/screen_special.html#preferences

screen preferences():

    tag menu

    use game_menu(_("Preferences"), scroll="viewport"):

        vbox:

            hbox:
                box_wrap True

                if renpy.variant("pc") or renpy.variant("web"):

                    vbox:
                        style_prefix "radio"
                        label _("Display")
                        textbutton _("Window") action Preference("display", "window")
                        textbutton _("Fullscreen") action Preference("display", "fullscreen")

                vbox:
                    style_prefix "check"
                    label _("Skip")
                    textbutton _("Unseen Text") action Preference("skip", "toggle")
                    textbutton _("After Choices") action Preference("after choices", "toggle")
                    textbutton _("Transitions") action InvertSelected(Preference("transitions", "toggle"))

                vbox:
                    style_prefix "radio"
                    xsize 340
                    label _("Animazioni")
                    textbutton _("Sì") action SetField(persistent, "menu_animato", True)
                    textbutton _("No") action SetField(persistent, "menu_animato", False)

                vbox:
                    style_prefix "radio"
                    xsize 340
                    label _("Avvisi delle conseguenze")
                    textbutton _("Sì") action SetField(persistent, "avvisi_conseguenze", True)
                    textbutton _("No") action SetField(persistent, "avvisi_conseguenze", False)

                vbox:
                    style_prefix "radio"
                    xsize 340
                    label _("Scelte a tempo")
                    textbutton _("Sì") action SetField(persistent, "scelte_a_tempo", True)
                    textbutton _("No") action SetField(persistent, "scelte_a_tempo", False)

            null height (4 * gui.pref_spacing)

            hbox:
                style_prefix "slider"
                box_wrap True

                vbox:

                    label _("Text Speed")

                    bar value Preference("text speed")

                    label _("Auto-Forward Time")

                    bar value Preference("auto-forward time")

                    label "Grandezza del testo"

                    bar value Preference("font size")

                vbox:

                    if config.has_music:
                        label _("Music Volume")

                        hbox:
                            bar value Preference("music volume")

                    if config.has_sound:

                        label _("Sound Volume")

                        hbox:
                            bar value Preference("sound volume")

                            if config.sample_sound:
                                textbutton _("Test") action Play("sound", config.sample_sound)

                    label _("Volume ambiente")

                    hbox:
                        bar value Preference("mixer ambiente volume")


                    if config.has_voice:
                        label _("Voice Volume")

                        hbox:
                            bar value Preference("voice volume")

                            if config.sample_voice:
                                textbutton _("Test") action Play("voice", config.sample_voice)

                    if config.has_music or config.has_sound or config.has_voice:
                        null height gui.pref_spacing

                        textbutton _("Mute All"):
                            action Preference("all mute", "toggle")
                            style "mute_all_button"


style pref_label is gui_label
style pref_label_text is gui_label_text
style pref_vbox is vbox

style radio_label is pref_label
style radio_label_text is pref_label_text
style radio_button is gui_button
style radio_button_text is gui_button_text
style radio_vbox is pref_vbox

style check_label is pref_label
style check_label_text is pref_label_text
style check_button is gui_button
style check_button_text is gui_button_text
style check_vbox is pref_vbox

style slider_label is pref_label
style slider_label_text is pref_label_text
style slider_slider is gui_slider
style slider_button is gui_button
style slider_button_text is gui_button_text
style slider_pref_vbox is pref_vbox

style mute_all_button is check_button
style mute_all_button_text is check_button_text

style pref_label:
    top_margin gui.pref_spacing
    bottom_margin gui.scale(2)

style pref_label_text:
    yalign 1.0

style pref_vbox:
    xsize gui.scale(290)

style radio_vbox:
    spacing gui.pref_button_spacing

style radio_button:
    properties gui.button_properties("radio_button")
    foreground "gui/button/radio_[prefix_]foreground.png"

style radio_button_text:
    properties gui.text_properties("radio_button")

style check_vbox:
    spacing gui.pref_button_spacing

style check_button:
    properties gui.button_properties("check_button")
    foreground "gui/button/check_[prefix_]foreground.png"

style check_button_text:
    properties gui.text_properties("check_button")

style slider_slider:
    xsize gui.scale(350)

style slider_button:
    properties gui.button_properties("slider_button")
    yalign 0.5
    left_margin gui.scale(10)

style slider_button_text:
    properties gui.text_properties("slider_button")

style slider_vbox:
    xsize gui.scale(450)


## History screen ##############################################################
##
## This is a screen that displays the dialogue history to the player.
## While there isn't anything special about this screen, it does have to
## access the dialogue history stored in _history_list.
##
## https://www.renpy.org/doc/html/history.html

screen history():

    tag menu

    ## Avoid predicting this screen, as it can be very large.
    predict False

    use game_menu(_("History"), scroll=("vpgrid" if gui.history_height else "viewport"), yinitial=1.0, spacing=gui.history_spacing):

        style_prefix "history"

        for h in _history_list:

            window:

                ## This lays things out properly if history_height is None.
                has fixed:
                    yfit True

                if h.who:

                    label h.who:
                        style "history_name"
                        substitute False

                        ## Take the color of the who text from the Character, if set.
                        if "color" in h.who_args:
                            text_color h.who_args["color"]

                $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                text what:
                    substitute False
                    ## I pensieri (pensiero, regia.rpy) restano in corsivo.
                    if h.what_args.get("italic"):
                        italic True
                    if "color" in h.what_args:
                        color h.what_args["color"]

        if not _history_list:
            label _("The dialogue history is empty.")


## This determines what tags are allowed to be displayed on the history
## screen.

define gui.history_allow_tags = { "alt", "noalt", "rt", "rb", "art" }


style history_window is empty

style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text

style history_label is gui_label
style history_label_text is gui_label_text

style history_window:
    xfill True
    ysize gui.history_height

style history_name:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width

style history_name_text:
    min_width gui.history_name_width
    textalign gui.history_name_xalign

style history_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    textalign gui.history_text_xalign
    layout ("subtitle" if gui.history_text_xalign else "tex")

style history_label:
    xfill True

style history_label_text:
    xalign 0.5


## Help screen #################################################################
##
## A screen that gives information about key and mouse bindings. It uses
## other screens (keyboard_help, mouse_help, and gamepad_help) to display the
## actual help.

screen help():

    tag menu

    default device = "keyboard"

    use game_menu(_("Help"), scroll="viewport"):

        style_prefix "help"

        vbox:
            spacing gui.scale(15)

            hbox:

                textbutton _("Keyboard") action SetScreenVariable("device", "keyboard")
                textbutton _("Mouse") action SetScreenVariable("device", "mouse")

                if GamepadExists():
                    textbutton _("Gamepad") action SetScreenVariable("device", "gamepad")

            if device == "keyboard":
                use keyboard_help
            elif device == "mouse":
                use mouse_help
            elif device == "gamepad":
                use gamepad_help


screen keyboard_help():

    hbox:
        label _("Enter")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Space")
        text _("Advances dialogue without selecting choices.")

    hbox:
        label _("Arrow Keys")
        text _("Navigate the interface.")

    hbox:
        label _("Escape")
        text _("Accesses the game menu.")

    hbox:
        label _("Ctrl")
        text _("Skips dialogue while held down.")

    hbox:
        label _("Tab")
        text _("Toggles dialogue skipping.")

    hbox:
        label _("Page Up")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Page Down")
        text _("Rolls forward to later dialogue.")

    hbox:
        label "H"
        text _("Hides the user interface.")

    hbox:
        label "S"
        text _("Takes a screenshot.")

    hbox:
        label "V"
        text _("Toggles assistive {a=https://www.renpy.org/l/voicing}self-voicing{/a}.")

    hbox:
        label "Shift+A"
        text _("Opens the accessibility menu.")


screen mouse_help():

    hbox:
        label _("Left Click")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Middle Click")
        text _("Hides the user interface.")

    hbox:
        label _("Right Click")
        text _("Accesses the game menu.")

    hbox:
        label _("Mouse Wheel Up")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Mouse Wheel Down")
        text _("Rolls forward to later dialogue.")


screen gamepad_help():

    hbox:
        label _("Right Trigger\nA/Bottom Button")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Left Trigger\nLeft Shoulder")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Right Shoulder")
        text _("Rolls forward to later dialogue.")

    hbox:
        label _("D-Pad, Sticks")
        text _("Navigate the interface.")

    hbox:
        label _("Start, Guide, B/Right Button")
        text _("Accesses the game menu.")

    hbox:
        label _("Y/Top Button")
        text _("Hides the user interface.")

    textbutton _("Calibrate") action GamepadCalibrate()


style help_button is gui_button
style help_button_text is gui_button_text
style help_label is gui_label
style help_label_text is gui_label_text
style help_text is gui_text

style help_button:
    properties gui.button_properties("help_button")
    xmargin gui.scale(8)

style help_button_text:
    properties gui.text_properties("help_button")

style help_label:
    xsize gui.scale(250)
    right_padding gui.scale(20)

style help_label_text:
    size gui.text_size
    xalign 1.0
    textalign 1.0



################################################################################
## Additional screens
################################################################################


## Confirm screen ##############################################################
##
## The confirm screen is called when Ren'Py wants to ask the player a yes or
## no question.
##
## https://www.renpy.org/doc/html/screen_special.html#confirm

screen confirm(message, yes_action, no_action):

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing gui.scale(30)

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing gui.scale(100)

                textbutton _("Yes") action yes_action
                textbutton _("No") action no_action

    ## Right-click and escape answer "no".
    key "game_menu" action no_action


style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text

style confirm_frame:
    background Frame([ "gui/confirm_frame.png", "gui/frame.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5

style confirm_prompt_text:
    textalign 0.5
    layout "subtitle"

style confirm_button:
    properties gui.button_properties("confirm_button")

style confirm_button_text:
    properties gui.text_properties("confirm_button")


## Skip indicator screen #######################################################
##
## The skip_indicator screen is displayed to indicate that skipping is in
## progress.
##
## https://www.renpy.org/doc/html/screen_special.html#skip-indicator

screen skip_indicator():

    zorder 100
    style_prefix "skip"

    frame:

        hbox:
            spacing gui.scale(6)

            text _("Skipping")

            text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"


## This transform is used to blink the arrows one after another.
transform delayed_blink(delay, cycle):
    alpha .5

    pause delay

    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat


style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos gui.skip_ypos
    background Frame("gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

style skip_text:
    size gui.notify_text_size

style skip_triangle:
    ## We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE
    ## glyph in it.
    font "DejaVuSans.ttf"


## Notify screen ###############################################################
##
## The notify screen is used to show the player a message. (For example,
## when the game is quicksaved or a screenshot has been taken.)
##
## https://www.renpy.org/doc/html/screen_special.html#notify-screen

screen notify(message):

    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text "[message!tq]"

    timer 3.25 action Hide('notify')


transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0


style notify_frame is empty
style notify_text is gui_text

style notify_frame:
    ypos gui.notify_ypos

    background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
    padding gui.notify_frame_borders.padding

style notify_text:
    properties gui.text_properties("notify")


## NVL screen ##################################################################
##
## This screen is used for NVL-mode dialogue and menus.
##
## https://www.renpy.org/doc/html/screen_special.html#nvl


screen nvl(dialogue, items=None):

    window:
        style "nvl_window"

        has vbox:
            spacing gui.nvl_spacing

        ## Displays dialogue in either a vpgrid or the vbox.
        if gui.nvl_height:

            vpgrid:
                cols 1
                yinitial 1.0

                use nvl_dialogue(dialogue)

        else:

            use nvl_dialogue(dialogue)

        ## Displays the menu, if given. The menu may be displayed incorrectly
        ## if config.narrator_menu is set to True.
        for i in items:

            textbutton i.caption:
                action i.action
                style "nvl_button"

    add SideImage() xalign 0.0 yalign 1.0


screen nvl_dialogue(dialogue):

    for d in dialogue:

        window:
            id d.window_id

            fixed:
                yfit gui.nvl_height is None

                if d.who is not None:

                    text d.who:
                        id d.who_id

                text d.what:
                    id d.what_id


## This controls the maximum number of NVL-mode entries that can be displayed
## at once.
define config.nvl_list_length = gui.nvl_list_length

style nvl_window is default
style nvl_entry is default

style nvl_label is say_label
style nvl_dialogue is say_dialogue

style nvl_button is button
style nvl_button_text is button_text

style nvl_window:
    xfill True
    yfill True

    background "gui/nvl.png"
    padding gui.nvl_borders.padding

style nvl_entry:
    xfill True
    ysize gui.nvl_height

style nvl_label:
    xpos gui.nvl_name_xpos
    xanchor gui.nvl_name_xalign
    ypos gui.nvl_name_ypos
    yanchor 0.0
    xsize gui.nvl_name_width
    min_width gui.nvl_name_width
    textalign gui.nvl_name_xalign

style nvl_dialogue:
    xpos gui.nvl_text_xpos
    xanchor gui.nvl_text_xalign
    ypos gui.nvl_text_ypos
    xsize gui.nvl_text_width
    min_width gui.nvl_text_width
    textalign gui.nvl_text_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_thought:
    xpos gui.nvl_thought_xpos
    xanchor gui.nvl_thought_xalign
    ypos gui.nvl_thought_ypos
    xsize gui.nvl_thought_width
    min_width gui.nvl_thought_width
    textalign gui.nvl_thought_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_button:
    properties gui.button_properties("nvl_button")
    xpos gui.nvl_button_xpos
    xanchor gui.nvl_button_xalign

style nvl_button_text:
    properties gui.text_properties("nvl_button")


## Bubble screen ###############################################################
##
## The bubble screen is used to display dialogue to the player when using
## speech bubbles. The bubble screen takes the same parameters as the say
## screen, must create a displayable with the id of "what", and can create
## displayables with the "namebox", "who", and "window" ids.
##
## https://www.renpy.org/doc/html/bubble.html#bubble-screen

screen bubble(who, what):
    style_prefix "bubble"

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "bubble_namebox"

                text who:
                    id "who"

        text what:
            id "what"

style bubble_window is empty
style bubble_namebox is empty
style bubble_who is default
style bubble_what is default

style bubble_window:
    xpadding 30
    top_padding 5
    bottom_padding 5

style bubble_namebox:
    xalign 0.5

style bubble_who:
    xalign 0.5
    textalign 0.5
    color "#000"

style bubble_what:
    align (0.5, 0.5)
    text_align 0.5
    layout "subtitle"
    color "#000"

define bubble.frame = Frame("gui/bubble.png", 55, 55, 55, 95)
define bubble.thoughtframe = Frame("gui/thoughtbubble.png", 55, 55, 55, 55)

define bubble.properties = {
    "bottom_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "bottom_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "top_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "top_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "thought" : {
        "window_background" : bubble.thoughtframe,
    }
}

define bubble.expand_area = {
    "bottom_left" : (0, 0, 0, 22),
    "bottom_right" : (0, 0, 0, 22),
    "top_left" : (0, 22, 0, 0),
    "top_right" : (0, 22, 0, 0),
    "thought" : (0, 0, 0, 0),
}



################################################################################
## Mobile Variants
################################################################################

## Il template SDK qui sostituiva il quick menu coi bottoni di testo e
## puntava a immagini gui/phone/ (bar, slider, scrollbar, radio, check) mai
## generate: su telefono la prima schermata con uno slider andava in errore.
## Su 1920x1080 lo stile PC regge anche su telefono; i testi li scala
## gui.rpy (variant small), i sigilli del quick menu QUICK_LATO.

style pref_vbox:
    variant "medium"
    xsize gui.scale(450)

## Su telefono i testi delle opzioni sono piu' grandi: colonne piu' larghe,
## o "Testo mai letto" va a capo sopra la riga sotto.
style pref_vbox:
    variant "small"
    xsize gui.scale(340)

## Il titolo sulla pergamena del menu principale, scalato, tocca il bordo.
style main_menu_title:
    variant "small"
    size gui.scale(41)

style slot_name_text:
    variant "small"
    size 20
