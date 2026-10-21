# Route Caino — eventi sul calendario, lavoro da scrivano, impegno.

init python:
    EVENTI.extend([
        # L'Adunanza: lucchetto d'ingresso, Luna II.
        {"id": "adunanza", "label": "ev_adunanza", "tipo": "fisso",
         "char": None, "luna": 2, "giorno": 8, "slot": "sera"},
        # Inviti a soglia (solo a route aperta: "caino" non in congelate).
        {"id": "caino_cap1", "label": "caino_cap1", "tipo": "invito",
         "char": "caino", "titolo": "L'Arconte della Proprietà chiede di te",
         "luna_min": 2, "slot": "pomeriggio",
         "cond": lambda v: v["caino_fiducia"] >= 2},
        {"id": "caino_cap2", "label": "caino_cap2", "tipo": "invito",
         "char": "caino", "titolo": "Convocazione all'alba nel cortile d'armi",
         "luna_min": 2, "slot": "mattina",
         "cond": lambda v: v["caino_fiducia"] >= 4
         and "caino_cap1" in v["visti"]},
        {"id": "caino_cap3", "label": "caino_cap3", "tipo": "invito",
         "char": "caino", "titolo": "La festa di mezzo inverno a Rocca Tempesta",
         "luna_min": 3, "slot": "sera",
         "cond": lambda v: v["caino_fiducia"] >= 6
         and "caino_cap2" in v["visti"]},
        {"id": "caino_cap4", "label": "caino_cap4", "tipo": "invito",
         "char": "caino", "titolo": "Caino ti vuole in Consiglio, coi registri",
         "luna_min": 3, "slot": "pomeriggio",
         "cond": lambda v: v["caino_fiducia"] >= 8
         and "caino_cap3" in v["visti"]},
        {"id": "caino_cap5", "label": "caino_cap5", "tipo": "invito",
         "char": "caino", "titolo": "Un messaggio: gli spalti, a notte fonda",
         "luna_min": 4, "slot": "sera",
         "cond": lambda v: v["caino_fiducia"] >= 9
         and "caino_cap4" in v["visti"]
         and "scelta_cuore" not in v["visti"]},
        {"id": "caino_cap6", "label": "caino_cap6", "tipo": "invito",
         "char": "caino", "titolo": "Due pergamene sul tavolo dell'Arconte",
         "luna_min": 4, "slot": "sera",
         "cond": lambda v: v["caino_fiducia"] >= 10
         and "caino_cap5" in v["visti"]
         and "scelta_cuore" not in v["visti"]},
    ])

    # Lavoro da scrivano: si sblocca dopo l'Adunanza, resta anche a route
    # chiusa (nessun punto).
    ATTIVITA["pomeriggio"].append(
        ("registri", "I registri della Proprietà", "caino",
         ["att_registri_1", "att_registri_2", "att_registri_3"],
         lambda v: "adunanza" in v["visti"]))

# Lucchetto d'ingresso: la trappola delle Candele Spente chiude il semestre.
label ev_adunanza:
    call caino_prologo
    if caino_trappole >= 1:
        $ congelate.add("caino")
    return

label att_registri_1:
    scene bg studio_glauco with fade
    "Mezza giornata sui registri delle decime. Gli scrivani della Proprietà mi passano le colonne peggiori: sono il nuovo, e il nuovo somma."
    "Imparo più della Famiglia da tre registri che da dieci lezioni: chi paga tardi, chi paga troppo, chi non paga e non viene mai segnato."
    return

label att_registri_2:
    scene bg studio_glauco with fade
    "Un errore di riporto da tre Scudi mi costa due ore di ricontrollo. Lo trovo: non era mio. Era di uno scrivano anziano, che mi guarda storto da allora."
    "«I dettagli possiedono le persone», dice l'Arconte. I dettagli, oggi, possiedono soprattutto il mio mal di testa."
    if icaro_affinity >= 4:
        show caino sarcastico with dissolve
        caino "Mi dicono che frequenti la fumeria di mio fratello. Conta le carte, conta gli Scudi, e adesso — vedo — conta pure te."
        "Non è una domanda. È una voce aperta nel registro, in attesa di saldo."
        hide caino with dissolve
    return

label att_registri_3:
    scene bg studio_glauco with fade
    "Giornata di archivio morto: registri di dieci anni fa, inchiostro sbiadito, polvere che sa di cantina."
    "In fondo a un volume trovo una pagina strappata con cura. Qualcuno, dieci anni fa, non voleva che qualcosa tornasse. Lo segno a mente: nella Proprietà anche i buchi sono voci."
    return

# Mini-scena di impegno (scelta del cuore, fine Luna IV).
label impegno_caino:
    scene bg studio_glauco with fade
    show caino neutro with dissolve
    "Lo studio, a tarda sera. Sul tavolo, non i registri: due corni di idromele. Entrambi pieni."
    caino "Siediti. Ho fatto un inventario, stanotte. Cariche: in ordine. Scudi: in ordine. Tu: fuori inventario. E le cose fuori inventario, [player_name], mi tolgono il sonno."
    show caino neutro with qdiss
    caino "Quindi la domanda è semplice, e la faccio una volta sola: vuoi entrare nel registro che non mostro a nessuno? Rispondi adesso. Dopo, archivio."
    menu:
        "L'Arconte della Proprietà aspetta. E per la prima volta non sta recitando."
        "«Scrivimi. Penna buona, inchiostro indelebile.»":
            $ impegno_esito = True
            show caino tenero with dissolve
            caino "Indelebile. Parola grossa, nei registri. ...la parola giusta."
            "Beve. Bevo. E da stanotte il semestre ha un contraente solo."
        "«Non firmo contratti che non so leggere.»":
            $ impegno_esito = False
            $ congelate.add("caino")
            show caino freddo with qdiss
            caino "Prudente. Sempre prudente. Archiviato, Figlio di Briseide: la Proprietà ti terrà il posto da scrivano. Solo quello."
    return
