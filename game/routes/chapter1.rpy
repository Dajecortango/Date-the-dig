# Sistema a capitoli — Capitolo I: Rocca Tempesta.
# Ogni capitolo è un'espansione con più ship. Una route per personaggio.
# Per aggiungere una route: metti i suoi file in game/routes/, aggiungi la
# voce qui sotto in CAP1_ROUTES e il salto in label capitolo1_dispatch.

define CAP1_ROUTES = [
    # (id, nome, sottotitolo, disponibile)
    ("aede", "Aede", "La lama di Glauco Severo — tsundere", True),
    ("velia", "Velia Ascea", "La cacciatrice di taglie", False),
    ("luvia", "Luvia Algida", "L'alchimista sprezzante", False),
    ("teodosio", "Teodosio Byensønn", "Il Comandante delle Fenrirkard", False),
    ("mercuzio", "Mercuzio Virtuoso", "Il bardo dell'Hammergrad", False),
]


screen chapter_select():

    modal True

    add "gui/game_menu.png"

    vbox:
        align (0.5, 0.5)
        spacing 26
        xmaximum 1100

        label _("CAPITOLO I") text_size 64 text_color gui.accent_color xalign 0.5
        text _("Rocca Tempesta") size 34 color "#f0e6d2" xalign 0.5
        null height 10
        text _("Chi corteggerai, Figlio di Briseide?") size 26 color "#c9b78a" xalign 0.5
        null height 14

        for rid, nome, sub, attiva in CAP1_ROUTES:
            if attiva:
                button:
                    xfill True
                    ypadding 14
                    background Frame("gui/button/choice_idle_background.png", 24, 12)
                    hover_background Frame("gui/button/choice_hover_background.png", 24, 12)
                    action Return(rid)
                    hbox:
                        spacing 18
                        text nome size 30 color "#f5e3b8" yalign 0.5
                        text sub size 20 color "#c9b78a" yalign 0.5
            else:
                frame:
                    xfill True
                    ypadding 14
                    background Frame("gui/button/choice_idle_background.png", 24, 12)
                    hbox:
                        spacing 18
                        text nome size 30 color "#6b5f4a" yalign 0.5
                        text sub size 20 color "#564c3c" yalign 0.5
                        text _("— Prossimamente") size 20 color "#8f7f5c" yalign 0.5


label capitolo1:

    scene bg nero with fade

    centered "{size=+14}CAPITOLO I{/size}\n\n{i}Rocca Tempesta{/i}"

    call screen chapter_select

label capitolo1_dispatch:

    if _return == "aede":
        jump prologo

    # Route non ancora scritte: non si arriva qui (slot disabilitati).
    jump capitolo1
