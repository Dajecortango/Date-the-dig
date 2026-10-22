# Audio: ambiente per sfondo ed effetti agganciati alla regia.
#
# - Canale "ambiente" (mixer proprio, cursore nelle Preferenze): il loop
#   segue lo sfondo in scena, controllato a ogni interazione; nel menu di
#   gioco resta com'e', al menu principale si spegne.
# - Effetti: lama sul "with lampo", colpo su vpunch/hpunch
#   (config.with_callback), monete quando cambiano gli Scudi (borsa.rpy),
#   campane all'arrivo sulla Calà.
# File in game/audio/, generati da make_audio.py (segnaposto sostituibili
# tenendo gli stessi nomi).

init python:
    renpy.music.register_channel("ambiente", mixer="ambiente", loop=True,
                                 tight=True)

    # Sfondo -> loop d'ambiente (None = silenzio).
    AMBIENTI = {
        "corridoio_ceppo": "audio/amb_camino.ogg",
        "studio_glauco": "audio/amb_camino.ogg",
        "esterno_neve": "audio/amb_vento.ogg",
        "cala_notte": "audio/amb_cala.ogg",
        "vicoli_zefiro": "audio/amb_strada.ogg",
        "palestra": "audio/amb_sala.ogg",
        "consiglio": "audio/amb_sala.ogg",
        "sala_svelo": "audio/amb_sala.ogg",
        "arena_athlion": "audio/amb_folla.ogg",
        "nero": None,
    }
    AMBIENTE_VOLUME = 0.7

    def audio_ambiente_aggiorna():
        if store._menu:
            return
        if store.main_menu:
            renpy.music.stop(channel="ambiente", fadeout=1.0)
            return
        attr = renpy.get_attributes("bg", layer="master") or ()
        voluto = AMBIENTI.get(attr[0]) if attr else None
        # Vicoli nei giorni di pioggia (effetti.rpy): la pioggia copre la strada.
        if attr and attr[0] == "vicoli_zefiro" and piove_ora():
            voluto = "audio/amb_pioggia.ogg"
        attuale = renpy.music.get_playing(channel="ambiente")
        if voluto == attuale:
            return
        if voluto is None:
            renpy.music.stop(channel="ambiente", fadeout=1.5)
        else:
            renpy.music.play(voluto, channel="ambiente", loop=True,
                             fadeout=1.5, fadein=1.5,
                             relative_volume=AMBIENTE_VOLUME)
            # La Calà: le campane suonano quando ci si arriva.
            if voluto == "audio/amb_cala.ogg" and not renpy.is_skipping():
                renpy.play("audio/campana.ogg", channel="sound")

    config.start_interact_callbacks.append(audio_ambiente_aggiorna)

    # Si concatena con un eventuale with_callback gia' presente (regia.rpy).
    _audio_with_prec = config.with_callback

    def audio_con_transizione(trans, paired):
        """config.with_callback: un suono per le transizioni di regia."""
        if not renpy.is_skipping():
            if trans is store.lampo:
                renpy.play("audio/lama.ogg", channel="sound")
            elif trans is store.vpunch or trans is store.hpunch:
                renpy.play("audio/colpo.ogg", channel="sound")
        if _audio_with_prec is not None:
            trans = _audio_with_prec(trans, paired)
        return trans

    config.with_callback = audio_con_transizione

    def audio_monete():
        if not renpy.is_skipping():
            renpy.play("audio/moneta.ogg", channel="sound")
