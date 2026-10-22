# Route Ofelia — eventi sul calendario, primo mancato, impegni (anche a tre).

init python:
    # Eventi a soglia: inviti che scadono (ignorarli costa un mancato).
    EVENTI.extend([
        {"id": "ofelia_ev1", "label": "ofelia_ev1", "tipo": "invito",
         "char": "ofelia", "scade": True,
         "titolo": "Ofelia ti vuole in serra, a guardare qualcuno cadere",
         "luna_min": 1, "slot": "pomeriggio",
         "cond": lambda v: v["ofelia_affinity"] >= 2},
        {"id": "ofelia_ev2", "label": "ofelia_ev2", "tipo": "invito",
         "char": "ofelia", "scade": True,
         "titolo": "Una cena a due, con un terzo che non lo sa",
         "luna_min": 2, "slot": "sera",
         "cond": lambda v: v["ofelia_affinity"] >= 4
         and "ofelia_ev1" in v["visti"]},
        {"id": "ofelia_ev3", "label": "ofelia_ev3", "tipo": "invito",
         "char": "ofelia", "scade": True,
         "titolo": "All'alba, in arena, con due lame vere",
         "luna_min": 3, "slot": "mattina",
         "cond": lambda v: v["ofelia_affinity"] >= 6
         and "ofelia_ev2" in v["visti"]
         and "scelta_cuore" not in v["visti"]},
        # Dopo la Fiaccolata, a route attiva: farsi vedere o restare segreto.
        {"id": "ofelia_ev4", "label": "ofelia_ev4", "tipo": "fisso",
         "char": "ofelia", "luna": 5, "giorno": 26, "slot": "pomeriggio",
         "cond": lambda v: v["route_attiva"] == "ofelia"
         and "ofelia" not in v["congelate"]},
        # Interludi: inviti SENZA scadenza e con id che non inizia per
        # "ofelia_" (l'hook ofelia_scadenza non li conta). Nessun punto.
        {"id": "interludio_ofelia_1", "label": "interludio_ofelia_1",
         "tipo": "invito", "char": "ofelia",
         "titolo": "Ofelia affila le lame di suo padre, e non vuole testimoni",
         "luna_min": 2, "slot": "mattina",
         "cond": lambda v: "ofelia_ev1" in v["visti"]
         and "scelta_cuore" not in v["visti"]},
        {"id": "interludio_ofelia_2", "label": "interludio_ofelia_2",
         "tipo": "invito", "char": "ofelia",
         "titolo": "Una lettera di Ascadeo, e Ofelia che non la vuole aprire da sola",
         "luna_min": 3, "slot": "sera",
         "cond": lambda v: "ofelia_ev2" in v["visti"]
         and "scelta_cuore" not in v["visti"]},
        # Deviazioni: id senza "ofelia_" e senza scadenza (l'hook dei mancati
        # non le conta), nessuna cond le richiede.
        {"id": "specchio_ofelia", "label": "specchio_ofelia", "tipo": "invito",
         "char": "ofelia",
         "titolo": "Ofelia davanti allo specchio, con tre vestiti e una domanda",
         "luna_min": 2, "slot": "pomeriggio",
         "cond": lambda v: "ofelia_ev1" in v["visti"]
         and "scelta_cuore" not in v["visti"]},
        {"id": "ballo_pretendenti", "label": "ballo_pretendenti",
         "tipo": "invito", "char": "ofelia",
         "titolo": "Ricevimento in serra: Ofelia ha un gioco nuovo",
         "luna_min": 3, "slot": "sera",
         "cond": lambda v: "ofelia_ev2" in v["visti"]
         and "scelta_cuore" not in v["visti"]},
        # Luna VI, prima del climax: la serra d'inverno, a route attiva.
        {"id": "interludio_ofelia_luna6", "label": "interludio_ofelia_luna6",
         "tipo": "fisso", "char": "ofelia",
         "luna": 6, "giorno": 5, "slot": "pomeriggio",
         "cond": lambda v: v["route_attiva"] == "ofelia"
         and "ofelia" not in v["congelate"]},
    ])


## Primo invito mancato: cosa succede a chi non si presenta ##################

label ofelia_scadenza_prima:
    scene bg corridoio_ceppo with fade
    "Il biglietto di Ofelia è ancora sul davanzale, piegato in quattro. Nessuno l'ha toccato, nessuno l'ha rispedito."
    "Stava lì ad aspettarmi, e io non mi sono presentat[fin]."
    "Vanna lo raccoglie con due dita, come si raccoglie qualcosa che potrebbe mordere."
    vanna "L'ha scritto lei, e non lo scriverà due volte. Ofelia non ripete gli inviti, [fratello_t]. Chi manca una volta è una svista. Chi manca due volte esce dalla corte."
    "Poi sorride, un po' dispiaciuta, e il biglietto sparisce nella sua manica."
    return


## Impegno — La serra di sera ##################################################

label impegno_ofelia:
    $ lento()
    scene bg sala_svelo with fade
    $ lento()
    show ofelia neutra with dissolve
    "La serra di sera, senza pretendenti. Solo lanterne basse, e la rosa nera potata fino all'osso."
    ofelia "Ho mandato via la fila. Tutta. Il cavallo compreso."
    "Sui tavoli restano i doni della stagione: sonetti arrotolati, un pugnale col manico d'avorio, un ritratto di lei che non le somiglia. Nessuno è stato aperto."
    ofelia "Mio padre li conta, sai? Ogni dono è un'alleanza mancata. Stanotte gli ho fatto perdere sei alleanze in un colpo."
    ofelia "Non lo faccio per nessuno, quindi ascolta bene: è una domanda sola, e non la ripeto."
    show ofelia compiaciuta with qdiss
    ofelia "Sei un interesse passeggero, [player_name]? Oppure resti anche quando smetto di essere gentile?"
    menu:
        "Mi porge le forbici. Il manico verso di me, la lama verso di lei."
        "Prendere le forbici: «Resto. Anche senza gentilezza.»" (peso=True):
            $ impegno_esito = True
            show ofelia imbarazzata with dissolve
            ofelia "...hai preso il manico. Gli altri afferravano sempre la lama, per farsi vedere coraggiosi."
            show ofelia neutra with qdiss
            ofelia "Bene. Da stasera la fila è chiusa. Se qualcuno chiede, sei tu il motivo. Fallo valere."
            "Non mi bacia. Mi aggiusta il colletto, lenta, come si sistema un'arma prima di appenderla. E il semestre, da stasera, ha un padrone."
        "Lasciarle le forbici: «Non ancora, Ofelia.»" (peso=True):
            $ impegno_esito = False
            $ congelate.add("ofelia")
            show ofelia rabbia with qdiss
            ofelia "Non ancora. Lo dicono tutti, prima di sparire. Almeno tu l'hai detto in faccia."
            show ofelia neutra with qdiss
            ofelia "Torna in fila, allora. In fondo. Non ti chiamerò per nome."
            "Riprende a potare. Lo stelo cade, pulito. Non alza più gli occhi."
    return


## Impegno a tre — Il contratto con Caino ######################################

label impegno_ofelia_caino:
    $ lento()
    $ impegno_of = False
    $ impegno_altro = False
    scene bg studio_glauco with fade
    $ lento()
    show ofelia neutra with dissolve
    "Lo studio di Glauco, a tarda sera. Ofelia siede sulla scrivania di suo padre come se fosse un trono che non le basta."
    show caino neutro at left with dissolve
    "Caino è già lì, in piedi, con un registro sotto il braccio. Non sembra sorpreso. Sembra in anticipo."
    ofelia "Vi ho convocati insieme perché odio ripetermi. Voi due mi piacete. Non mi piace scegliere."
    caino "Proposta irregolare. Tre parti, un solo oggetto contrattuale, nessun precedente a registro."
    ofelia "Nessuno è oggetto, Caino. Siamo tre firme. E io firmo per prima."
    caino "Sulla scrivania di tuo padre. Con il suo inchiostro. È quasi poetico, se si apprezza il rischio."
    ofelia "Lo apprezzo. Lo amministri tu, il rischio. Io lo indosso."
    show ofelia compiaciuta with qdiss
    ofelia "Tu, [player_name]. Dentro o fuori. Le mie condizioni sono semplici: niente segreti, niente pietà, niente gelosie da serva."
    menu:
        "Caino apre il registro a una pagina bianca. Aspetta la penna."
        "«Dentro. Scrivi tre nomi, Caino.»" (peso=True):
            $ impegno_of = True
            show ofelia imbarazzata with dissolve
            ofelia "...non hai nemmeno chiesto chi viene prima. Peccato: avevo una risposta crudele pronta."
            show ofelia neutra with qdiss
            caino "Annotato. Prima firma: Ofelia Severo. Seconda: in sospeso. Resta la mia, e quella non la mostro davanti a testimoni."
            ofelia "Allora vi lascio soli. Il tuo ragioniere ha una domanda da farti, e la fa male in pubblico."
            hide ofelia with dissolve
        "«Fuori. Non firmo per metà.»" (peso=True):
            $ congelate.add("ofelia")
            show ofelia rabbia with qdiss
            ofelia "Per metà. Che modo meschino di contare. Pensavo che almeno la matematica fosse dalla tua."
            caino "Annullato prima della firma. Il più pulito dei contratti."
            "Ofelia scende dalla scrivania e se ne va senza voltarsi. La porta dello studio si chiude piano: con lei, è peggio di uno sbattere."
            hide ofelia with dissolve
            caino "Resta. Il contratto a tre è annullato. Il mio, no: quello non l'ho ancora proposto."
    # Il partner risponde sempre, qualunque sia stato l'esito con Ofelia.
    call impegno_caino
    $ impegno_altro = impegno_esito
    if impegno_of and impegno_altro:
        "Contraente solo, ha detto. Poi ha corretto a margine, con la penna buona: due. Ofelia, dal corridoio, ha riso come una lama che si sfodera."
    $ impegno_esito = impegno_of and impegno_altro
    return


## Impegno a tre — Il segreto della sorella ####################################

label impegno_ofelia_aede:
    $ lento()
    $ impegno_of = False
    $ impegno_altro = False
    scene bg sala_svelo with fade
    $ lento()
    show ofelia neutra with dissolve
    "La serra, a notte fatta. Ofelia ha spento tutte le lanterne tranne una, quella che illumina solo le sue mani."
    ofelia "Lo so, di mia sorella. Lo sa mezza Zefiro: Aede non è mai stata brava a nascondere chi le piace."
    ofelia "E so di te. Quello lo sai solo tu, e adesso io."
    ofelia "Da bambine dividevamo la stanza, le lezioni di spada, i vestiti. Lei prendeva sempre il rosso. Io lasciavo fare, e mi tenevo il nero."
    show ofelia compiaciuta with qdiss
    ofelia "Non ti chiedo di scegliere. La sorella e te: mi va bene. Ho sempre diviso tutto con lei, tranne i segreti."
    show ofelia rabbia with qdiss
    ofelia "Aede non divide. Io sì. Non farglielo sapere."
    menu:
        "La lanterna trema appena. La sua voce no."
        "«Non lo saprà. Da me, mai.»" (peso=True):
            $ impegno_of = True
            show ofelia imbarazzata with dissolve
            ofelia "...mai è una parola che mi piace sentire da chi mente bene. Ricordatelo, quando la guardi negli occhi."
            show ofelia neutra with qdiss
            ofelia "Ora va'. Ti aspetta sul ballatoio, credo. Lei fa le domande ad alta voce. Io le faccio al buio."
            "Spegne l'ultima lanterna. Esco dalla serra con un segreto in tasca e la sensazione di averlo rubato a qualcuno."
        "«Non mentirò ad Aede. Né per te, né per nessuno.»" (peso=True):
            $ congelate.add("ofelia")
            show ofelia rabbia with qdiss
            ofelia "Leale. Che virtù noiosa. Va' da lei, allora, e dille pure tutto: tanto non ti crederà."
            "Spegne l'ultima lanterna senza aspettare che io sia uscit[fin]. Al buio, la serra profuma di qualcosa che marcisce piano."
            "Va' da lei, ha detto. Non le ho dato la soddisfazione di discutere: ci vado davvero."
    # Il partner risponde sempre, qualunque sia stato l'esito con Ofelia.
    call impegno_aede
    $ impegno_altro = impegno_esito
    if impegno_of and impegno_altro:
        "«Io non divido», ha detto. Annuisco ancora, nel buio del mio Ceppo. Da qualche parte, in una serra, qualcuno sorride."
    $ impegno_esito = impegno_of and impegno_altro
    return


## Fatti ed echi delle deviazioni ##############################################

init python:
    CONSEGUENZE_VARS.extend(["ofelia_specchio_esito", "ofelia_ballo_esito"])

    FATTI.extend([
        {"id": "fx_ofelia_specchio", "char": "ofelia",
         "testo": "Ofelia ti ha chiesto quale vestito mettere. Voleva sapere se avevi il coraggio di dire la verità.",
         "avviso": None,
         "cond": lambda v: v["ofelia_specchio_esito"] is not None},
        {"id": "fx_ofelia_ballo", "char": "ofelia",
         "testo": "Al ricevimento in serra Ofelia ti ha fatto scegliere il pretendente da rimandare a casa.",
         "avviso": "Ofelia se ne ricorderà.",
         "cond": lambda v: v["ofelia_ballo_esito"] is not None},
    ])

    # Chi racconta: lo specchio lo sa solo Ofelia (corte); il ballo era
    # pubblico e Vanna raccoglie pettegolezzi per mestiere (riti).
    ECHI.extend([
        {"id": "echi_ofelia_specchio", "fatto": "fx_ofelia_specchio",
         "luoghi": ("corte",), "label": "echi_ofelia_specchio",
         "cond": lambda v: v["luna"] >= 5
         and "ofelia" not in v["congelate"]},
        {"id": "echi_ofelia_ballo", "fatto": "fx_ofelia_ballo",
         "luoghi": ("riti",), "label": "echi_ofelia_ballo",
         "cond": lambda v: v["luna"] >= 5
         and "ofelia" not in v["congelate"]},
    ])
