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
         and ("scelta_cuore" not in v["visti"]
              or "caino" in (v["route_attiva"], v["route_seconda"]))},
        {"id": "caino_cap6", "label": "caino_cap6", "tipo": "invito",
         "char": "caino", "titolo": "Due pergamene sul tavolo dell'Arconte",
         "luna_min": 4, "slot": "sera",
         "cond": lambda v: v["caino_fiducia"] >= 10
         and "caino_cap5" in v["visti"]
         and ("scelta_cuore" not in v["visti"]
              or "caino" in (v["route_attiva"], v["route_seconda"]))},
        # Luna V, route attiva: la talpa nei registri (fiducia +2 / -2 / 0).
        {"id": "caino_luna5", "label": "caino_luna5", "tipo": "fisso",
         "char": "caino", "luna": 5, "giorno": 20, "slot": "pomeriggio",
         "cond": lambda v: v["route_attiva"] == "caino"
         and "caino" not in v["congelate"]},
        # Luna VI, route attiva: l'ultima pagina prima del Consiglio (0 punti).
        {"id": "caino_luna6", "label": "caino_luna6", "tipo": "fisso",
         "char": "caino", "luna": 6, "giorno": 5, "slot": "sera",
         "cond": lambda v: v["route_attiva"] == "caino"
         and "caino" not in v["congelate"]},
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
    "Il Ceppo di Cardia, per esempio, paga sempre il giorno prima della scadenza. Sempre. Nessuno è così puntuale, se non ha qualcosa da far dimenticare."
    "A metà pomeriggio uno scrivano anziano, Ottone, mi passa accanto e mi gira il calamaio dall'altra parte. Senza una parola."
    ottone "Mancin[fin], vero? Si vede dalle macchie sul polsino. Qui dentro, ragazz[fin], le macchie parlano prima di te."
    "Lo ringrazio. Lui ha già ripreso a scrivere, e la sua penna non si è mai fermata."
    "Al tramonto chiudo l'ultima colonna. Quadra. Nessuno me lo dice, ma il giorno dopo trovo sul banco un registro più grosso: alla Proprietà, il premio è il lavoro."
    return

label att_registri_2:
    scene bg studio_glauco with fade
    "Un errore di riporto da tre Scudi mi costa due ore di ricontrollo. Lo trovo: non era mio. Era di uno scrivano anziano, che mi guarda storto da allora."
    "Ottone. Lo stesso del calamaio. Correggo la riga a margine, con la mia mano, e non lo segnalo a nessuno."
    ottone "Hai visto, eh. E non hai parlato."
    pc "Tre Scudi non valgono un nemico."
    ottone "Sbagliato. Qui dentro tre Scudi valgono esattamente un nemico. Ma grazie lo stesso."
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
    "La pagina prima porta una firma che conosco: un sigillo col drago, inchiostro verde. Lo stesso drago dell'anello di Caino."
    "La pagina dopo riprende a metà di una frase. «...e pertanto la Proprietà del defunto passa alla Capofamiglia, per intero.»"
    "Del defunto. Dieci anni fa. Non c'è scritto chi."
    "Rimetto il volume dov'era, con il dorso storto come l'ho trovato, e faccio finta di niente."
    return

# Mini-scena di impegno (scelta del cuore, fine Luna IV).
label impegno_caino:
    $ lento()
    scene bg studio_glauco with fade
    $ lento()
    show caino neutro with dissolve
    "Lo studio, a tarda sera. Sul tavolo, non i registri ma due corni di idromele, entrambi pieni."
    "Le candele sono consumate fino al piattino. Non ha dormito, e non ha nemmeno finto di provarci."
    caino "Siediti. Ho fatto un inventario, stanotte. Cariche: in ordine. Scudi: in ordine."
    caino "Tu: fuori inventario. E le cose fuori inventario, [player_name], mi tolgono il sonno."
    pc "Mi hai chiamat[fin] per dirmi che non dormi?"
    show caino sarcastico with qdiss
    caino "Ti ho chiamat[fin] per smettere di dormire. È diverso. Le domande chiuse si archiviano; quelle aperte maturano interessi."
    "Fa ruotare il corno tra le dita, senza bere. Al mignolo, stasera, c'è di nuovo il sigillo col drago."
    show caino neutro with qdiss
    caino "Mia madre direbbe che sto per fare un investimento sbagliato. Mia madre non ha mai sbagliato un investimento. Né ne ha mai fatto uno che le piacesse."
    caino "Quindi la domanda è semplice, e la faccio una volta sola: vuoi entrare nel registro che non mostro a nessuno? Rispondi adesso. Dopo, archivio."
    menu:
        "Il corno smette di girare. Caino aspetta, le dita ferme sul bordo."
        "«Scrivimi. Penna buona, inchiostro indelebile.»" (peso=True):
            $ impegno_esito = True
            show caino tenero with dissolve
            caino "Indelebile. Parola grossa, nei registri. ...la parola giusta."
            "Beve. Bevo. E da stanotte il semestre ha un contraente solo."
            caino "Una clausola, però. Una sola. Se mi menti, lo saprò. Se mi dici la verità, lo saprò lo stesso: è peggio, ma mi abituerò."
            "Spegne l'ultima candela con due dita. Il registro resta aperto sul tavolo al buio, e nessuno dei due lo chiude."
        "«Non firmo contratti che non so leggere.»" (peso=True):
            $ impegno_esito = False
            $ congelate.add("caino")
            show caino freddo with qdiss
            caino "Prudente. Sempre prudente. Archiviato, [figlio_t] di Briseide: la Proprietà ti terrà il posto da scrivano. Solo quello."
            "Svuota il mio corno nel suo, senza fretta. Poi apre un registro qualsiasi e comincia a scrivere."
            "Esco. La penna non si ferma nemmeno quando chiudo la porta."
    return

################################################################################
## LUNA V — La talpa (fisso V/20 pomeriggio, fiducia +2 / -2 / 0)
################################################################################

label caino_luna5:
    scene bg studio_glauco with fade
    "Pomeriggio di neve fitta. Mi chiamano nello studio dell'Arconte con un biglietto di tre parole: «Porta il registro»."
    show caino freddo with dissolve
    "Caino non è alla scrivania. È in piedi accanto al camino, e nel camino non brucia legna: brucia carta."
    caino "Siediti. Non tu, [player_name]. Lui."
    "Dietro di me, scortato da due Fenrirkard del Ramo di Lenora, entra Ottone. Lo scrivano del calamaio. Le mani gli tremano; le nasconde nelle maniche, che tremano anch'esse."
    caino "Ottone. Dieci anni alla Proprietà. Mia madre ti assunse. Io ti ho confermato. Due firme, due generazioni."
    caino "Stamattina il Primo Arconte aveva sul tavolo le copie dei nostri registri, con le date di consultazione e rapporti con errori non ancora corretti. Scritti con la tua mano."
    if "caino_cap4" not in eventi_visti:
        "Eumene. Il Filius Maior del Ceppo di Cardia, la «mano sinistra» di Caino in Consiglio. In Luna III Caino l'ha consegnato con tre buchi nei registri, e si è preso la sua carica."
        "Io ero agli scrittoi delle decime, quella sera. Le date di consultazione, però, le ho ricopiate io: le copie passano tutte dalla mia mano."
    ottone "Arconte, io... mi hanno detto che era per l'ordine della Famiglia. Che la Verità voleva solo controllare."
    show caino furioso with vpunch
    caino "LA VERITÀ NON PAGA IN SCUDI D'ORO, OTTONE."
    "Il pugno sul tavolo fa saltare il calamaio. L'inchiostro si allarga sul legno come una macchia di sangue scuro."
    "Non l'ho mai sentito alzare la voce, nemmeno contro Druso. Le guardie guardano il soffitto."
    show caino freddo with qdiss
    caino "Perdonami. Ho alzato la voce. È un lusso che concedo a chi non deve più niente alla Proprietà."
    caino "Ottone, sai qual è la differenza tra un errore e un tradimento? L'errore si corregge a margine. Il tradimento si cancella dal registro. Con tutto il nome."
    if "att_registri_2" in eventi_visti:
        "Ottone mi cerca con gli occhi. Tre Scudi, un errore di riporto, una riga corretta a margine. Se lo ricorda anche lui."
    menu:
        "Caino si volta verso di me. Il registro che ho in mano pesa come un'accusa."
        "«Ha tradito. Ma sa chi ha pagato. Fallo parlare, prima di cancellarlo.»":
            $ caino_fiducia += 2
            $ caino_ottone = "parla"
            pc "Ha tradito, Caino. Ma sa chi l'ha pagato. Un nome ci serve più di una riga cancellata."
            show caino neutro with qdiss
            caino "Ci serve. Plurale. Lo hai detto senza accorgertene."
            ottone "Un servitore dell'Arconte della Verità. Senza stemma. Ma aveva un anello col leone d'oro, all'indice."
            "Caino e io ci guardiamo. Un leone d'oro all'indice: l'anello di tutti, a Rocca Tempesta. L'anello di chi vuole sembrare chiunque."
            caino "Un leone qualsiasi. Quindi qualcuno che sa che io guardo gli anelli. La lista dei sospetti si accorcia, e i nomi rimasti sono tutti di famiglia."
        "«Dieci anni. Concedigli l'esilio, non le Segrete.»":
            $ caino_fiducia -= 2
            $ caino_ottone = "esilio"
            pc "Dieci anni di servizio, Caino. Una sola riga sbagliata. Concedigli l'esilio, non le Segrete."
            show caino sarcastico with qdiss
            caino "Clemenza. Una moneta rara, nella Rocca. E come tutte le monete rare, qualcuno ne approfitta."
            caino "Rurikstad, Ottone. Stanotte. Se torni, non ci sarà un secondo margine."
            "Ottone esce senza voltarsi. Sulla soglia si ferma un istante, e mi fa un cenno minimo. Un grazie da tre Scudi."
        "Taci e lascia decidere l'Arconte":
            $ caino_ottone = "tace"
            "Taccio. È la sua Proprietà, il suo traditore, la sua legge."
            show caino freddo with qdiss
            caino "Il silenzio. Saggio, oggi. Le Fenrirkard sanno cosa fare."
            "Portano via Ottone. Lui non protesta: sa leggere un registro chiuso meglio di me."
    hide caino with dissolve
    "Restiamo soli. Caino prende il mio registro e lo sfoglia fino alle date incriminate. Le mie date. La mia mano."
    show caino neutro with dissolve
    caino "Lo vedi, adesso, il disegno? Le copie dicono sei mesi. Le date le hai scritte tu. Al Consiglio basterà un nome nuovo da sacrificare."
    pc "E tu lo darai, quel nome?"
    "Non risponde subito. Getta nel camino l'ultima pagina, la guarda annerirsi dai bordi verso il centro."
    show caino tenero with dissolve
    caino "Sto bruciando tutto quello che potrebbero usare contro di te. Tutto tranne una cosa. Quella devo deciderla io, davanti a tutti."
    caino "Fino ad allora, scrivi in bella grafia, [player_name]. E non firmare niente che io non abbia letto."
    return

################################################################################
## LUNA VI — L'ultima pagina (fisso VI/5 sera, nessun punto)
################################################################################

label caino_luna6:
    scene bg esterno_neve with fade
    "Gli spalti della Rocca, a notte fonda. Caino mi ha mandato un biglietto senza firma: «Gli spalti. Porta freddo»."
    show caino neutro with dissolve
    "È seduto sul parapetto, il registro aperto sulle ginocchia. Una lanterna sola, schermata dal mantello."
    caino "Sedici giorni al Consiglio. Ho bruciato tutto quello che potevano usare. Resta una pagina."
    "La gira verso di me. Due colonne tirate a righello: attivo, passivo. In cima, il mio nome. Sotto, niente."
    caino "Non so dove metterti. È la prima volta in vent'anni che non so dove mettere un nome."
    show caino freddo with qdiss
    caino "Quindi lo chiedo a te, che è contro tutte le mie regole. Di che colonna sei, [player_name]?"
    menu:
        "La neve si posa sulla pagina, e Caino non la scuote via."
        "«Attivo. Mettimi dove ti serve, al Consiglio.»":
            $ caino_colonna = "attivo"
            pc "Attivo. Se al Consiglio ti serve un nome, mettimi dove ti serve."
            show caino sarcastico with qdiss
            caino "Generos[fin]. È la parola che uso per chi non ha letto le clausole."
            "Scrive il mio nome a sinistra. Poi resta con la penna alzata, come se la riga non gli tornasse."
        "«Nessuna. Non sono una voce del tuo registro.»":
            $ caino_colonna = "nessuna"
            pc "Nessuna delle due. Non sono una voce del tuo registro, Caino. Non lo sono mai stat[fin]."
            show caino sorpreso with qdiss
            "Mi guarda come si guarda un errore di somma che, ricontrollato, risulta giusto."
            caino "Allora il registro è sbagliato. Lo dico io, che non sbaglio registri."
        "Prendergli la penna, e scrivere il mio nome da sol[fin]":
            $ caino_colonna = "scrive"
            "Gli tolgo la penna di mano. Lui me la lascia, e questo da solo vale più di una firma."
            "Scrivo il mio nome a metà, a cavallo della riga. Né attivo, né passivo."
            show caino tenero with dissolve
            caino "Fuori colonna. Lo sai che l'inchiostro su una riga non si cancella senza strappare la pagina."
            pc "Lo so. Per questo l'ho fatto."
    show caino neutro with qdiss
    caino "Il ventuno, in Consiglio, non guardarmi come se sapessi già cosa dirò. Non lo so nemmeno io."
    "Chiude il registro. La neve resta dentro, tra le pagine. Non la scuote via nemmeno adesso."
    return
