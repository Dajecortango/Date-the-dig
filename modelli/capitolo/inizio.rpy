# Capitolo __NUMERO__ — "__TITOLO__". Punto d'ingresso: il registro lo chiama
# da "Nuova partita" (ingresso="__ID___inizio").
# set_gender e sanitize_name sono globali (game/protagonista.rpy).

label __ID___inizio:

    $ entra_capitolo("__ID__")

    scene bg nero with fade

    centered "{cps=20}{size=+14}CAPITOLO __NUMERO__{/size}\n\n{i}__TITOLO__{/i}{/cps}"

    menu:
        "Chi sei, in questa storia?"

        "Un uomo":
            $ set_gender("m")

        "Una donna":
            $ set_gender("f")

    $ player_name = renpy.input("Come ti chiami? (Primo Nome)", length=20)
    $ player_name = sanitize_name(player_name)

    "Questa e' la prima riga di [player_name]. Sostituiscila con la tua storia."

    $ sblocca_finale("__ID___fine")

    return
