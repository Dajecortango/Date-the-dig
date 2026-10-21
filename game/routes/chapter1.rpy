# Capitolo I — "Malandrini".
# Dating sim a calendario: ~6 mesi nel Ceppo di Briseide, giornate in slot
# (mattina/pomeriggio/sera), attività che decidono chi frequenti. Il motore
# vive in game/calendario.rpy + game/calendario_logic.py; gli eventi delle
# route in game/routes/*_eventi.rpy e *_route.rpy; gli snodi comuni in
# game/routes/snodi.rpy.

label capitolo1:

    scene bg nero with fade

    centered "{cps=20}{size=+14}CAPITOLO I{/size}\n\n{i}Malandrini{/i}{/cps}"

    menu:
        "Chi sei, in questa storia?"

        "Un uomo":
            $ set_gender("m")

        "Una donna":
            $ set_gender("f")

    $ player_name = renpy.input("Come ti chiama la Famiglia? (Primo Nome)", length=20)
    $ player_name = sanitize_name(player_name)

    # Background del protagonista di questo capitolo.
    "Nel Nord c'è una sola Famiglia, e non è questione di sangue: è questione di giuramento."

    "Tu sei [figlio_t] adottiv[fin] di Briseide Ippodamia, la madre degli orfani, Autarca della Columna Lactaria. Il tuo nome di prima è morto; ora ti chiami [player_name]."

    "E questa, tra i malandrini di Rocca Tempesta, è la tua storia: sei Lune, un giorno alla volta."

    # Nuova partita+: con il prologo gia' visto si puo' saltare lo Svelo.
    call prologo_o_salto

    jump cal_loop
