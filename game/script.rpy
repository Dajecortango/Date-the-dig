# Date the Dig — entry point.
# Setup minimo: input nome e salto al capitolo attivo.
# Le route vivono in game/routes/; la selezione ship in chapter1.rpy.

label start:

    $ player_name = renpy.input("Come ti chiama la Famiglia? (Primo Nome)", length=20)
    $ player_name = sanitize_name(player_name)

    jump capitolo1
