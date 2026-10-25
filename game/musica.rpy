# Musica di capitolo: leitmotiv per personaggio, tema del calendario, tema
# dei finali. Canale "music" standard (cursore gia' nelle Preferenze).
#
# - La tabella e' del capitolo (capitolo().musiche): nome -> file ogg.
#   Per Malandrini i nomi sono i char delle route ("aede", "caino", ...)
#   piu' "calendario" e "finale".
# - musica(nome): dissolvenza incrociata di 2 s; se il tema e' gia' in onda
#   o il file manca (segnaposto cancellato), non fa nulla.
# - musica_silenzio(): silenzio pilotato prima di un momento chiave; il tema
#   riparte alla prossima musica(...).
# - Al menu principale la musica si spegne da sola (come l'ambiente).
# File in game/audio/<capitolo>/tema_*.ogg, generati da make_musica.py
# (segnaposto sostituibili tenendo gli stessi nomi; versioni vere con
# make_musica_elevenlabs.py).

init python:
    MUSICA_FADE = 2.0

    # Tema del menu principale (comune a tutti i capitoli): Ren'Py lo avvia
    # e lo spegne da solo. Se il segnaposto viene tolto senza sostituirlo,
    # il menu resta muto come prima.
    if renpy.loadable("audio/tema_menu.ogg"):
        config.main_menu_music = "audio/tema_menu.ogg"
        config.main_menu_music_fadein = 1.5

    def _musica_file(nome):
        cap = capitolo()
        if cap is None or not nome:
            return None
        return cap.musiche.get(nome)

    def musica(nome, fadein=MUSICA_FADE):
        """Suona il tema `nome` del capitolo con dissolvenza incrociata."""
        f = _musica_file(nome)
        if f is None or not renpy.loadable(f):
            return
        if renpy.music.get_playing(channel="music") == f:
            return
        renpy.music.play(f, channel="music", loop=True,
                         fadeout=MUSICA_FADE, fadein=fadein)

    def musica_stop(fadeout=MUSICA_FADE):
        renpy.music.stop(channel="music", fadeout=fadeout)

    def musica_silenzio():
        """Regia: la musica si spegne in fretta, la scena resta nuda."""
        musica_stop(1.0)

    def _musica_menu_principale():
        # Senza tema del menu, al menu principale la musica si spegne;
        # col tema ci pensa Ren'Py (main_menu_music).
        if store.main_menu and not config.main_menu_music:
            renpy.music.stop(channel="music", fadeout=1.0)

    config.start_interact_callbacks.append(_musica_menu_principale)
