# Date the Dig — entry point.
# Setup minimo: input nome e salto alla route attiva.
# Le route vivono in game/routes/. Una route futura aggiungerà qui il bivio.

label start:

    $ player_name = renpy.input("Come ti chiama la Famiglia? (Primo Nome)", length=20)
    $ player_name = sanitize_name(player_name)

    jump prologo
