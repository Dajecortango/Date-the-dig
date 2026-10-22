init 999 python:
    config.auto_choice_delay = 0.05

label splashscreen:
    python:
        import copy
        _rea_snap = (copy.deepcopy(persistent.opzioni_viste), set(persistent.opzioni_scelte),
                     set(persistent.trama_visti), set(persistent.fatti_storici))
        _preferences.skip_unseen = True
        store._skipping = True
        _preferences.skip_after_choices = True
        renpy.config.skipping = "fast"
        rea_log = []
        fatti_noti.update({"icaro_coperto": ("icaro_ev1", 5), "caino_massacro": ("adunanza", 6),
                           "lenora_insolenza": ("udienza_lenora", 30), "druso_lanternaio": ("druso_ev3", 40),
                           "aede_segreto": ("svelo", 0)})
        eventi_visti.update(["adunanza", "caino_cap1", "icaro_ev1", "aede_cap1"])
        cal_idx = 45
        _v = cal_vars()
        for _e in EVENTI:
            if _e["id"].startswith("rea_"):
                rea_log.append("cond %s = %s" % (_e["id"], _e["cond"](_v)))
        cal_contesto = "rea_caino_conto"
        eventi_visti.add("rea_caino_conto")
    call rea_caino_conto
    $ renpy.config.skipping = "fast"
    $ cal_contesto = "rea_lenora_segno"
    $ eventi_visti.add("rea_lenora_segno")
    call rea_lenora_segno
    $ renpy.config.skipping = "fast"
    $ cal_contesto = "rea_aede_lanternaio"
    $ eventi_visti.add("rea_aede_lanternaio")
    call rea_aede_lanternaio
    python:
        conseguenze_aggiorna()
        rea_log.append("scelte: %r" % scelte_partita)
        rea_log.append("fatti rea: %r" % sorted(k for k in fatti_noti if k.startswith("rea_")))
        cal_idx = 50
        rea_eco = echi_pesca("fumeria")
        rea_log.append("eco fumeria: %r" % rea_eco)
    if rea_eco:
        $ renpy.config.skipping = "fast"
        call expression echi_label(rea_eco)
    python:
        inviti_mostrati.update(["aede_cap1x", "caino_cap1", "druso_ev1", "icaro_ev1", "interludio_ofelia_2"])
        eventi_visti.discard("caino_cap1"); eventi_visti.discard("icaro_ev1")
        eventi_visti.add("scelta_cuore")
        conseguenze_aggiorna()
        rea_log.append("fatti perso: %r" % sorted(k for k in fatti_noti if k.startswith("rea_perso")))
        cal_idx = 60
        echi_visti.add(rea_eco) if rea_eco else None
        rea_eco2 = echi_pesca("registri")
        rea_log.append("eco registri: %r" % rea_eco2)
    if rea_eco2:
        $ renpy.config.skipping = "fast"
        call expression echi_label(rea_eco2)
    python:
        rea_log.append("FINE OK")
        with open(config.basedir + "/zz_rea_log.txt", "w") as _f:
            _f.write("\n".join(rea_log))
        persistent.opzioni_viste, persistent.opzioni_scelte, persistent.trama_visti, persistent.fatti_storici = _rea_snap
        renpy.save_persistent()
        renpy.quit()
