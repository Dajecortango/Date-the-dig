# Route Icaro — eventi sul calendario, gelosia, impegno (romance e Bro).

init python:
    EVENTI.extend([
        {"id": "icaro_ev1", "label": "icaro_ev1", "tipo": "invito",
         "char": "icaro", "titolo": "Un posto al tavolo grande di Icaro",
         "luna_min": 2, "slot": "sera",
         "cond": lambda v: v["icaro_affinity"] >= 2},
        # Interludi: niente punti, solo tempo con lui. Muoiono col cuore.
        {"id": "icaro_int1", "label": "icaro_int1", "tipo": "invito",
         "char": "icaro", "titolo": "Giorno di riscossione: Icaro vuole un testimone",
         "luna_min": 2, "slot": "sera",
         "cond": lambda v: "icaro_ev1" in v["visti"]
         and "scelta_cuore" not in v["visti"]},
        # Deviazioni: non sbloccano niente, nessuna cond le richiede.
        {"id": "icaro_debito_altrui", "label": "icaro_debito_altrui",
         "tipo": "invito", "char": "icaro",
         "titolo": "Icaro riscuote a domicilio. Serve qualcuno con la lanterna",
         "luna_min": 2, "slot": "sera",
         "cond": lambda v: "icaro_int1" in v["visti"]
         and "scelta_cuore" not in v["visti"]},
        {"id": "icaro_ev2", "label": "icaro_ev2", "tipo": "invito",
         "char": "icaro", "titolo": "Icaro vuole mostrarti «una cosa di valore»",
         "luna_min": 3, "slot": "sera",
         "cond": lambda v: v["icaro_affinity"] >= 4
         and "icaro_ev1" in v["visti"]},
        {"id": "icaro_int2", "label": "icaro_int2", "tipo": "invito",
         "char": "icaro", "titolo": "Una lezione di mani al mercato coperto",
         "luna_min": 3, "slot": "sera",
         "cond": lambda v: "icaro_ev2" in v["visti"]
         and "scelta_cuore" not in v["visti"]},
        {"id": "icaro_febbre", "label": "icaro_febbre", "tipo": "invito",
         "char": "icaro", "titolo": "La fumeria è chiusa. Sulla porta: «Non bussare»",
         "luna_min": 3, "slot": "pomeriggio",
         "cond": lambda v: "icaro_ev2" in v["visti"]
         and "scelta_cuore" not in v["visti"]},
        {"id": "icaro_ev3", "label": "icaro_ev3", "tipo": "invito",
         "char": "icaro", "titolo": "Una serata placida, pipa e silenzio",
         "luna_min": 4, "slot": "sera",
         "cond": lambda v: v["icaro_affinity"] >= 6
         and "icaro_ev2" in v["visti"]},
        {"id": "icaro_int3", "label": "icaro_int3", "tipo": "invito",
         "char": "icaro", "titolo": "Una lettera di Lenora, da aprire dopo la terza pipa",
         "luna_min": 4, "slot": "sera",
         "cond": lambda v: "icaro_ev3" in v["visti"]
         and "scelta_cuore" not in v["visti"]},
        # Linea Bro (solo protagonista uomo): due scene tra soci, 0 punti.
        # Restano vive dopo la scelta del cuore solo se la route e' Icaro.
        {"id": "icaro_bro1", "label": "icaro_bro_affari", "tipo": "invito",
         "char": "icaro", "titolo": "Icaro ha un affare: gli serve un socio con la faccia seria",
         "luna_min": 3, "slot": "pomeriggio",
         "cond": lambda v: v["player_gender"] == "m"
         and "icaro_ev2" in v["visti"]
         and ("scelta_cuore" not in v["visti"]
              or v["route_attiva"] == "icaro")},
        {"id": "icaro_bro2", "label": "icaro_bro_colpo", "tipo": "invito",
         "char": "icaro", "titolo": "Stanotte Icaro riscuote. Senza bussare",
         "luna_min": 4, "slot": "sera",
         "cond": lambda v: v["player_gender"] == "m"
         and "icaro_bro1" in v["visti"]
         and ("scelta_cuore" not in v["visti"]
              or v["route_attiva"] == "icaro")},
        # Luna V, route attiva (romance e Bro): la partita grossa.
        {"id": "icaro_luna5", "label": "icaro_luna5", "tipo": "fisso",
         "char": "icaro", "luna": 5, "giorno": 26, "slot": "sera",
         "cond": lambda v: v["route_attiva"] == "icaro"
         and "icaro" not in v["congelate"]},
        # Luna VI, route attiva (romance e Bro): i conti di fine semestre.
        {"id": "icaro_luna6", "label": "icaro_luna6", "tipo": "fisso",
         "char": "icaro", "luna": 6, "giorno": 12, "slot": "sera",
         "cond": lambda v: v["route_attiva"] == "icaro"
         and "icaro" not in v["congelate"]},
    ])

    # Possessività (solo romance, protagonista donna): dopo che il suo
    # interesse e' acceso (>= ICARO_GELOSIA, come icaro_ev3), accettare
    # l'invito di un altro personaggio lo chiude per sempre. Il pianificatore
    # lo avvisa prima (cal_inviti_info, avviso "gelosia").
    ICARO_GELOSIA = 6

    def icaro_gelosia_armata(ev):
        return (ev.get("tipo") == "invito"
                and ev.get("char") not in (None, "icaro")
                and store.player_gender == "f"
                and store.icaro_affinity >= ICARO_GELOSIA
                and store.route_attiva is None
                and "icaro" not in store.congelate)

    def icaro_gelosia(ev):
        if icaro_gelosia_armata(ev):
            store.congelate.add("icaro")
            renpy.notify("Icaro non dimentica.")

    cal_post_evento_hooks.append(icaro_gelosia)


## Impegno (scelta del cuore) ################################################

label impegno_icaro:
    $ lento()
    scene bg vicoli_zefiro with fade
    $ lento()
    "La fumeria è chiusa. Ha mandato via tutti, anche il vecchio che dorme sui cuscini: un'eccezione che deve essergli costata."
    show icaro neutro with dissolve
    "Mi aspetta al tavolo piccolo, quello dove non gioca: quello dove conta. Davanti a lui, un registro aperto su una pagina bianca."
    icaro "Siediti. Non è una partita. È peggio: è una trattativa."
    icaro "Ho fatto i conti tre volte. Una compagna è un passivo: tempo, attenzioni, rischio. Ogni logica dice di non firmare."
    icaro "Ma ho un buco nel bilancio da tre Lune, e il buco ha la tua faccia. Quindi: o sei l'eccezione che conferma ogni mia regola, o sei l'errore più costoso della mia vita. Scegli tu la voce."
    pc "E se fossi l'errore?"
    icaro "Allora l'avrò scelto io. A prezzo pieno, senza trattare."
    menu:
        "La pagina bianca aspetta. Icaro non firma mai per primo."
        "«Eccezione. E sono irrevocabile, come le tue regole.»" (peso=True):
            $ impegno_esito = True
            $ icaro_impegnato = True
            show icaro sereno with dissolve
            icaro "Irrevocabile. Parola da contratto serio. ...venduto."
            "Scrive una riga sola sulla pagina bianca, e la copre con la mano prima che io possa leggerla. Sua. Come tutto ciò che conta."
            icaro "Non chiedere cosa c'è scritto. Te lo dirò quando avrà maturato gli interessi."
            "Restiamo al buio, la pipa accesa tra noi. Non mi tocca. La mia spalla sfiora la sua, e aspetto che si scosti. Non si scosta."
        "«Non sono una voce del tuo inventario.»" (peso=True):
            $ impegno_esito = False
            $ congelate.add("icaro")
            icaro "Allora il bilancio torna come prima. Perfetto. Era l'ipotesi più probabile, l'avevo già scontata."
            "Lo dice piatto, senza una piega. Poi taglia il mazzo, e una carta gli scivola sul pavimento."
            "Chiude il registro. Prima di alzarsi, però, ci passa sopra il palmo, piano. Come per lisciare una pagina che nessuno scriverà."
    return

label impegno_bro:
    $ lento()
    scene bg vicoli_zefiro with fade
    $ lento()
    "La fumeria, a quest'ora, è solo fumo vecchio e sedie capovolte. Icaro ha tenuto acceso un lume solo."
    show icaro neutro with dissolve
    "Il tavolo piccolo. Icaro spinge verso di me una chiave di ferro, senza cerimonie."
    icaro "Magazzino. Copia unica. Se muoio, l'inventario va a te: Druso lo venderebbe, Caino lo tasserebbe. Tu lo conteresti. È il massimo che ho da offrire a un uomo, e non si ripete."
    pc "Druso e Caino lo sanno?"
    icaro "Druso lo saprà quando glielo dirai tu, ubriaco. Caino lo sa già. Caino sa sempre tutto: per questo non lo scelgo."
    menu:
        "La chiave pesa come un giuramento."
        "Prendere la chiave del magazzino" (peso=True):
            $ impegno_esito = True
            $ icaro_impegnato = True
            pc "La tengo. E non la conto: la custodisco."
            show icaro sereno with dissolve
            icaro "...custodire. Verbo accettabile. Fratello."
            "Accenna a tendermi la mano. Ci ripensa a metà strada e mi passa la pipa, il cannello già pulito."
        "Lasciargli la chiave" (peso=True):
            $ impegno_esito = False
            $ congelate.add("icaro")
            icaro "Come preferisci. L'offerta scade adesso e non rientra a listino."
            "Rimette la chiave nel taschino cucito all'interno del gilet. Non la vedrò più."
    return


## Fatti ed echi delle deviazioni ##############################################

init python:
    CONSEGUENZE_VARS.extend(["icaro_debito_esito", "icaro_febbre_esito"])

    FATTI.extend([
        {"id": "fx_icaro_debito", "char": "icaro",
         "testo": "Hai visto Icaro condonare un debito ai tintori, e fingere che fosse un pettine.",
         "avviso": "Icaro se ne ricorderà.",
         "cond": lambda v: v["icaro_debito_esito"] is not None},
        {"id": "fx_icaro_febbre", "char": "icaro",
         "testo": "Hai trovato Icaro con la febbre, chiuso nella fumeria a fare l'inventario.",
         "avviso": None,
         "cond": lambda v: v["icaro_febbre_esito"] is not None},
    ])

    # La tintora ha visto chi teneva la lanterna; la febbre la sa solo Icaro.
    ECHI.extend([
        {"id": "echi_icaro_tintora", "fatto": "fx_icaro_debito",
         "luoghi": ("citta",), "label": "echi_icaro_tintora",
         "cond": lambda v: v["luna"] >= 5
         and "icaro" not in v["congelate"]},
        {"id": "echi_icaro_febbre", "fatto": "fx_icaro_febbre",
         "luoghi": ("fumeria",), "label": "echi_icaro_febbre",
         "cond": lambda v: v["luna"] >= 5
         and "icaro" not in v["congelate"]},
    ])
