# Audio: ambiente per sfondo ed effetti agganciati alla regia.
#
# - Canale "ambiente" (mixer proprio, cursore nelle Preferenze): il loop
#   segue lo sfondo in scena, controllato a ogni interazione; nel menu di
#   gioco resta com'e', al menu principale si spegne.
# - Effetti: lama sul "with lampo", colpo su vpunch/hpunch
#   (config.with_callback), monete quando cambiano gli Scudi (borsa.rpy),
#   il suono d'arrivo di un ambiente (capitolo().ambiente_arrivo).
# File in game/audio/, generati da make_audio.py (segnaposto sostituibili
# tenendo gli stessi nomi).

init python:
    renpy.music.register_channel("ambiente", mixer="ambiente", loop=True,
                                 tight=True)

    # Le tabelle sono del capitolo (capitolo()):
    #   ambienti         sfondo -> loop d'ambiente (None = silenzio);
    #   ambiente_pioggia sfondo -> loop nei giorni di pioggia (effetti.rpy);
    #   ambiente_arrivo  loop -> suono che parte quando ci si arriva.
    AMBIENTE_VOLUME = 0.7

    def audio_ambiente_aggiorna():
        if store._menu:
            return
        if store.main_menu:
            renpy.music.stop(channel="ambiente", fadeout=1.0)
            return
        cap = capitolo()
        attr = renpy.get_attributes("bg", layer="master") or ()
        bg = attr[0] if attr else None
        voluto = None
        if cap is not None and bg is not None:
            voluto = cap.ambienti.get(bg)
            # Nei giorni di pioggia la pioggia copre l'ambiente di sempre.
            if bg in cap.ambiente_pioggia and piove_ora():
                voluto = cap.ambiente_pioggia[bg]
        attuale = renpy.music.get_playing(channel="ambiente")
        if voluto == attuale:
            return
        if voluto is None:
            renpy.music.stop(channel="ambiente", fadeout=1.5)
        else:
            renpy.music.play(voluto, channel="ambiente", loop=True,
                             fadeout=1.5, fadein=1.5,
                             relative_volume=AMBIENTE_VOLUME)
            arrivo = cap.ambiente_arrivo.get(voluto)
            if arrivo and not renpy.is_skipping():
                renpy.play(arrivo)

    config.start_interact_callbacks.append(audio_ambiente_aggiorna)

    # Si concatena con un eventuale with_callback gia' presente (regia.rpy).
    _audio_with_prec = config.with_callback

    def audio_con_transizione(trans, paired):
        """config.with_callback: un suono per le transizioni di regia."""
        if not renpy.is_skipping():
            if trans is store.lampo:
                renpy.play("audio/lama.ogg")
            elif trans is store.vpunch or trans is store.hpunch:
                renpy.play("audio/colpo.ogg")
        if _audio_with_prec is not None:
            trans = _audio_with_prec(trans, paired)
        return trans

    config.with_callback = audio_con_transizione

    def audio_monete():
        if not renpy.is_skipping():
            renpy.play("audio/moneta.ogg")
