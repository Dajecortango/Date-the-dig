# Reazioni: il mondo che risponde alle scelte (pacchetto 40 consigli, punti
# 6, 7, 8). Spec: docs/superpowers/specs/2026-10-22-conseguenze-design.md e
# docs/superpowers/specs/2026-10-22-pacchetto-40-consigli-design.md.
#
# 6. Tre inviti reattivi (Lune III-IV) che scattano su combinazioni di fatti
#    di route diverse. Mai al posto di un capitolo: cond esplicita, nessun
#    capitolo riordinato, tutti muoiono con la scelta del cuore.
# 7. Il mondo va avanti: inviti offerti e mai presi diventano fatti
#    ("qualcun altro ci e' andato"), ripresi da echi in Luna V-VI.
# 8. Piu' echi: almeno 3 per personaggio, raccontati da chi puo' saperlo.
#
# I fatti nuovi hanno prefisso rea_, gli echi echi_rea_. Le scelte dei menu
# si leggono con _scelto (registro automatico di conseguenze.rpy): nessuna
# variabile nuova nello store.

init python:
    def rea_noti(*ids):
        """True se tutti i fatti sono gia' noti in questa partita (le cond
        degli eventi ricevono cal_vars(), che non espone fatti_noti)."""
        return all(i in store.fatti_noti for i in ids)

    EVENTI.extend([
        # Caino ha in mano la querela del mercante del tavolo grande: hai
        # mentito per Icaro e lavori gia' per la Proprieta'.
        {"id": "rea_caino_conto", "label": "rea_caino_conto", "tipo": "invito",
         "char": "caino", "titolo": "L'Arconte ha una querela col tuo nome sopra",
         "luna_min": 3, "slot": "pomeriggio",
         "cond": lambda v: rea_noti("icaro_coperto")
         and "caino_cap1" in v["visti"]
         and "caino" not in v["congelate"]
         and "scelta_cuore" not in v["visti"]},
        # Pandora ha segnato il tuo nome due volte: il massacro detto in
        # faccia a Caino e l'insolenza alla grata. Scrive a Briseide.
        {"id": "rea_lenora_segno", "label": "rea_lenora_segno", "tipo": "invito",
         "char": None, "ritratto": "briseide",
         "titolo": "Briseide ti convoca: una lettera dal Ramo di Lenora",
         "luna_min": 4, "slot": "mattina",
         "cond": lambda v: rea_noti("caino_massacro", "lenora_insolenza")
         and "scelta_cuore" not in v["visti"]},
        # Il lanternaio racconta ad Aede la torsione del vicolo: la sua. E
        # Druso che morde. Aede ti conosce dallo Svelo e dalla consegna.
        {"id": "rea_aede_lanternaio", "label": "rea_aede_lanternaio",
         "tipo": "invito", "char": "aede",
         "titolo": "Aede ti aspetta in cortile. Ha saputo del vicolo",
         "luna_min": 4, "slot": "mattina",
         "cond": lambda v: rea_noti("druso_lanternaio", "aede_segreto")
         and "aede_cap1" in v["visti"]
         and "aede" not in v["congelate"]
         and "scelta_cuore" not in v["visti"]},
    ])

    FATTI.extend([
        # --- Eventi reattivi (6) ---------------------------------------------
        {"id": "rea_caino_tiene", "char": "caino",
         "testo": "Davanti a Caino hai ripetuto la bugia per Icaro, parola per parola.",
         "avviso": "Caino se ne ricorderà.",
         "cond": lambda v: _scelto(v, "rea_caino_conto", "«Ho contato ogni carta")},
        {"id": "rea_caino_verita", "char": "icaro",
         "testo": "Hai detto a Caino che Icaro barava. Gratis.",
         "avviso": "Icaro se ne ricorderà.",
         "cond": lambda v: _scelto(v, "rea_caino_conto", "«Icaro ha barato")},
        {"id": "rea_lenora_due_segni", "char": None,
         "testo": "Pandora ha segnato il tuo nome due volte. Non hai ritirato niente.",
         "avviso": "Lenora se ne ricorderà.",
         "cond": lambda v: _scelto(v, "rea_lenora_segno", "«Non ritiro niente")},
        {"id": "rea_lenora_scuse", "char": None,
         "testo": "Hai scritto a Lenora una lettera di scuse, dettata da Briseide. La mano non tremava.",
         "avviso": None,
         "cond": lambda v: _scelto(v, "rea_lenora_segno", "Scrivere a Lenora")},
        {"id": "rea_aede_torsione", "char": "aede",
         "testo": "Aede ha saputo del lanternaio: la torsione del vicolo era la sua.",
         "avviso": None,
         "cond": lambda v: "rea_aede_lanternaio" in v["visti"]},
        # --- Il mondo va avanti (7): inviti mai presi ------------------------
        # Solo se la route non e' quella del personaggio: a route attiva i
        # suoi inviti restano aperti anche dopo la scelta del cuore.
        {"id": "rea_perso_aede_cap1", "char": "aede",
         "testo": "La consegna al Ceppo di Glauco l'ha portata Corrado. Aede ha scortato lui.",
         "avviso": None,
         "cond": lambda v: v["perso"]("aede_cap1") and v["route_attiva"] != "aede"},
        {"id": "rea_perso_caino_cap1", "char": "caino",
         "testo": "L'Arconte della Proprietà aveva chiesto di te per nome. Ha preso un altro scrivano.",
         "avviso": None,
         "cond": lambda v: v["perso"]("caino_cap1") and v["route_attiva"] != "caino"},
        {"id": "rea_perso_druso_ev1", "char": "druso",
         "testo": "La serata di versi di Druso ha avuto un'altra musa. L'Ode non porta il tuo nome.",
         "avviso": None,
         "cond": lambda v: v["perso"]("druso_ev1") and v["route_attiva"] != "druso"},
        {"id": "rea_perso_icaro_ev1", "char": "icaro",
         "testo": "Il posto al tavolo grande di Icaro è andato a un ragazzo del Ramo di Iperione.",
         "avviso": None,
         "cond": lambda v: v["perso"]("icaro_ev1") and v["route_attiva"] != "icaro"},
        {"id": "rea_perso_ofelia_lettera", "char": "ofelia",
         "testo": "La lettera di Ascadeo, Ofelia l'ha fatta leggere a un altro pretendente.",
         "avviso": None,
         "cond": lambda v: v["perso"]("interludio_ofelia_2")},
        # --- Scelte delle Lune II-III che tornano (8) ------------------------
        {"id": "rea_icaro_riga", "char": "icaro",
         "testo": "Nel registro nero di Icaro hai aggiunto un debito alla pagina di Druso.",
         "avviso": None,
         "cond": lambda v: _scelto(v, "icaro_int1", "Aggiungere una riga")},
        {"id": "rea_ofelia_rogo", "char": "ofelia",
         "testo": "Hai bruciato la quotazione di Ascadeo senza leggerla. Lui vi ha sentiti.",
         "avviso": None,
         "cond": lambda v: _scelto(v, "interludio_ofelia_2", "Bruciarla alla torcia")},
    ])

    ECHI.extend([
        # Reattivi.
        {"id": "echi_rea_icaro_due_volte", "fatto": "rea_caino_tiene",
         "luoghi": ("fumeria",), "label": "echi_rea_icaro_due_volte"},
        {"id": "echi_rea_icaro_pagina", "fatto": "rea_caino_verita",
         "luoghi": ("fumeria",), "label": "echi_rea_icaro_pagina"},
        {"id": "echi_rea_pandora_druso", "fatto": "rea_lenora_due_segni",
         "luoghi": ("taverna",), "label": "echi_rea_pandora_druso"},
        # Druso impara la torsione da te in druso_int3 (Luna IV): l'eco
        # aspetta la fine della fase libera per non anticiparlo.
        {"id": "echi_rea_druso_torsione", "fatto": "rea_aede_torsione",
         "luoghi": ("scudo",), "label": "echi_rea_druso_torsione",
         "cond": lambda v: "scelta_cuore" in v["visti"]},
        # Il mondo va avanti (Luna V-VI).
        {"id": "echi_rea_corrado_consegna", "fatto": "rea_perso_aede_cap1",
         "luoghi": ("studio", "studio_p"), "label": "echi_rea_corrado_consegna"},
        {"id": "echi_rea_ottone_scrivano", "fatto": "rea_perso_caino_cap1",
         "luoghi": ("registri",), "label": "echi_rea_ottone_scrivano"},
        {"id": "echi_rea_ode_altrui", "fatto": "rea_perso_druso_ev1",
         "luoghi": ("taverna",), "label": "echi_rea_ode_altrui"},
        {"id": "echi_rea_tavolo_altrui", "fatto": "rea_perso_icaro_ev1",
         "luoghi": ("fumeria",), "label": "echi_rea_tavolo_altrui"},
        {"id": "echi_rea_lettera_altrui", "fatto": "rea_perso_ofelia_lettera",
         "luoghi": ("riti",), "label": "echi_rea_lettera_altrui"},
        # Scelte delle Lune II-III.
        {"id": "echi_rea_druso_quarantatre", "fatto": "rea_icaro_riga",
         "luoghi": ("taverna",), "label": "echi_rea_druso_quarantatre"},
        {"id": "echi_rea_ascadeo_quota", "fatto": "rea_ofelia_rogo",
         "luoghi": ("riti",), "label": "echi_rea_ascadeo_quota"},
    ])


## 6. Eventi reattivi ########################################################

# Caino: la querela del tavolo grande (icaro_coperto + Proprieta').
label rea_caino_conto:
    scene bg studio_glauco with fade
    show caino neutro with dissolve
    "Lo studio dell'Arconte, a metà pomeriggio. Caino non alza gli occhi dal registro. Mi indica una sedia con la penna."
    caino "Querela della Consorteria. Un mercante, perdita secca al tavolo grande della fumeria. Accusa di baro contro mio fratello."
    caino "Un testimone, dice, ha contato ogni carta e ha giurato «tutto regolare». Il testimone ha il tuo nome. Scritto male, ma è il tuo."
    show caino sarcastico with qdiss
    caino "Le querele contro Icaro arrivano qui una volta per Luna. Le archivio. È un servizio di famiglia."
    if "caino_massacro" in fatti_noti:
        caino "All'Adunanza hai chiamato massacro una festa, davanti a me. Al tavolo di mio fratello hai chiamato regolare una truffa."
        caino "Sei sincer[fin] solo con chi non ti conviene? Mi serve saperlo."
    else:
        caino "Non mi interessa il mercante. Mi interessa quanto costi tu, quando menti per qualcuno."
    menu:
        "La penna resta sospesa sopra la colonna. Caino sorride. Il sorriso non c'entra niente."
        "«Ho contato ogni carta. Tutto regolare.»":
            $ caino_fiducia += 1
            show caino neutro with qdiss
            caino "Stesse parole, stesso ordine. Chi ricorda le proprie bugie le ha scelte, non subite."
            caino "Archiviata. Manderò a Icaro la copia, senza biglietto. Deve sapere chi gli tiene i cassetti."
        "«Icaro ha barato. Io ho mentito per lui.»":
            $ icaro_affinity -= 1
            show caino sorpreso with qdiss
            caino "...La verità. Gratis. Non succede spesso, in questa stanza."
            show caino freddo with qdiss
            caino "La terrò in un cassetto. Un giorno mio fratello avrà bisogno di ricordarsi chi tiene i cassetti."
            "Esco sapendo di aver dato a Caino una cosa che non era mia. Era di Icaro."
        "«Lo chieda a Icaro, Arconte. La querela è contro di lui.»":
            show caino sarcastico with qdiss
            caino "Rimandare la palla al Ramo. Elegante. Lo faccio anch'io, nei giorni in cui non ho voglia di lavorare."
            caino "Ma oggi lavoravo. Peccato."
    "Il corridoio della Proprietà odora di inchiostro e cera. Da qualche parte, una penna gratta il mio nome."
    return

# Briseide: il secondo segno di Pandora (caino_massacro + lenora_insolenza).
label rea_lenora_segno:
    scene bg corridoio_ceppo with fade
    show briseide neutra with dissolve
    "Briseide mi aspetta all'alba, in fondo al corridoio del Ceppo. Tra le dita ha una lettera col sigillo del corvo su un ramo spoglio."
    briseide "Dal Ramo di Lenora. Non da Lenora: da Pandora, che tiene il suo registro. Lenora non scrive ai Figli degli altri."
    briseide "Due righe. All'Adunanza hai chiamato massacro il Ballo delle Candele Spente, in faccia a suo figlio. Alla grata hai risposto a tono."
    briseide "Pandora ti ha segnat[fin] due volte, con lo stesso inchiostro. Sai cosa vuol dire, [player_name]?"
    pc "Che ha una buona memoria."
    briseide "Che la seconda riga è più corta della prima. Alla terza non serve più scrivere."
    menu:
        "Briseide piega la lettera in due. Non la straccia. Aspetta."
        "«Non ritiro niente. Era un massacro, e la risposta era giusta.»":
            briseide "Lo so che era giusta. Per questo Pandora l'ha scritta."
            briseide "Tienili, i tuoi due segni. Ma da oggi, quando il Ramo di Lenora ti chiama, ci vai con me."
        "Scrivere a Lenora, sotto dettatura di Briseide":
            "Briseide detta. Io scrivo. Ogni frase chiede scusa senza dire mai di cosa."
            briseide "Così. Lenora non legge le scuse: legge la calligrafia. Se trema, hai paura. Non deve tremare."
            "Non trema. Briseide la sigilla col suo anello e la affida al primo corriere per Rocca Tempesta."
        "«E al terzo segno, madre? Cosa succede?»":
            briseide "Nessuno lo sa. Chi l'ha preso non è tornato a raccontarlo."
            briseide "Il Nord è grande, e le Segrete Silenti sono profonde. Guarda, ascolta, e non farti notare. Ancora per un po'."
    "Briseide getta la lettera nel braciere. Il corvo di cera si piega, annerisce, resta intero fino all'ultimo."
    return

# Aede: la torsione del vicolo (druso_lanternaio + aede_segreto).
label rea_aede_lanternaio:
    scene bg palestra with fade
    show aede irritata with dissolve
    "Il cortile d'armi all'alba. Aede non mi saluta. Mi lancia una spada di legno, forte, all'altezza dello stomaco."
    aede "Il lanternaio dei vicoli bassi. Ieri mi ha fermata per raccontarmi una storia. Tre volte. Con le mani."
    aede "Un esattore della Malacorte. [Un_t] novellin[fin] che gli prende il braccio e lo gira. Così."
    "Mi prende il polso e lo torce. Piano. Esattamente come nel vicolo."
    aede "La mia torsione. Quella che insegno ai novellini perché non si facciano ammazzare. Non perché vadano a cercarsela."
    show aede sorpresa with qdiss
    aede "E poi, dice, è arrivato Druso. Druso. Che morde. Me l'ha raccontato tre volte e non ci credo ancora."
    show aede neutra with qdiss
    aede "Allo Svelo hai giurato di tacere per me. Nel vicolo hai parlato con le mani per uno sconosciuto. Sei pien[fin] di sorprese, e io odio le sorprese."
    menu:
        "Mi lascia il polso. La spada di legno è ancora nel suo pugno."
        "«L'ho imparata da te. Ha funzionato.»":
            $ aede_affinity += 1
            show aede imbarazzata with qdiss
            aede "Ovvio che ha funzionato. È mia."
            aede "...Guardia alta. Se devi fare l'eroe nei vicoli, almeno fallo coi piedi giusti."
        "«Una torsione qualunque. Me la sono cavata.»":
            $ aede_affinity -= 1
            show aede rabbia with qdiss
            aede "Qualunque. La MIA torsione. Qualunque."
            with vpunch
            "Mi mette a terra in un respiro, con la stessa presa. La segatura sa di ferro."
            aede "Ecco cosa fa, una torsione qualunque. Ricordatelo."
        "«Il resto l'ha fatto Druso. A morsi.»":
            show aede sorriso with dissolve
            "Le scappa una risata. Corta, vera. Se la rimangia subito."
            show aede neutra with qdiss
            aede "La Malacorte non dimentica un orecchio, novellin[fin]. Né il tuo, né il suo. Guardatevi le spalle, tutti e due."
    "Riprendiamo la guardia. Per tutta la ripresa, Aede mi corregge solo i piedi. Il polso, dice, ormai è affar mio."
    return


## Echi dei reattivi ##########################################################

# Icaro: Caino gli ha mandato la querela archiviata (fumeria).
label echi_rea_icaro_due_volte:
    scene bg vicoli_zefiro with dissolve
    show icaro neutro with dissolve
    icaro "Mio fratello mi ha mandato una querela archiviata. Senza biglietto. Con una riga sola sottolineata: «tutto regolare»."
    icaro "La stessa bugia, due volte, a due tavoli diversi. Al secondo sedeva Caino."
    show icaro sereno with qdiss
    "Sposta il posacenere per farmi spazio al tavolo grande. Non dice altro. Da lui, è un bilancio in attivo."
    return

# Icaro: Caino ha usato la verita' a cena (fumeria).
label echi_rea_icaro_pagina:
    scene bg vicoli_zefiro with dissolve
    show icaro irritato with dissolve
    icaro "A cena, mio fratello Caino ha citato una frase. «Icaro ha barato.» Ha detto che gliel'avevano regalata."
    icaro "Non mi offende la verità. Mi offende il prezzo. L'hai data via per niente. E a lui."
    "Apre il registro nero e scrive. Questa volta, credo, sulla mia pagina."
    return

# Lenora: Druso ha cenato con Pandora (taverna).
label echi_rea_pandora_druso:
    scene bg vicoli_zefiro with dissolve
    show druso ghigno at left with easeinleft
    druso "Linguaccia! Indovina con chi ho cenato. Con Pandora. Cioè: io cenavo, lei leggeva il registro."
    druso "DUE segni accanto al tuo nome, e non li hai ritirati! Io ne ho undici, ma sono figlio: i miei non contano."
    druso "Pandora dice che sei un caso interessante. A me non l'ha mai detto. Ti odio. Brindiamo."
    return

# Aede: la rossa in palestra, a correggere Druso (scudo, Luna V-VI).
label echi_rea_druso_torsione:
    scene bg palestra with dissolve
    show druso irritato at left with easeinleft
    druso "La rossa è venuta in palestra. Apposta. Mi ha messo a terra con la torsione del vicolo, davanti a tutti."
    druso "Poi ha detto: «Così la fa [il_t] novellin[fin]. Tu mordi.» Come se mordere non fosse un'arte."
    show druso ghigno at left with qdiss
    druso "L'ho odiata. Poi l'ho rifatta, sul fabbro. Non dirglielo."
    return


## 7. Il mondo va avanti (Luna V-VI) ##########################################

# Aede: la consegna di Briseide, portata da Corrado (studio).
label echi_rea_corrado_consegna:
    scene bg studio_glauco with dissolve
    show corrado neutro with dissolve
    corrado "Ricordi la consegna per il Ceppo di Glauco? Briseide aveva fatto il tuo nome. Poi, visto che tu avevi altro, ha mandato me."
    corrado "Aede mi ha scortato fino alla tenuta. Mi ha chiamato «mulo» per un'ora intera. Credo fosse affetto. Credo."
    corrado "Glauco mi ha guardato due secondi. Poi ha chiesto di te, [fratello_t]. Non ho saputo cosa rispondere."
    "Riapre il libro degli stemmi. Per un po' nessuno dei due legge."
    return

# Caino: il posto da scrivano che l'Arconte ti aveva offerto (registri).
label echi_rea_ottone_scrivano:
    scene bg studio_glauco with dissolve
    "Ottone mi gira il calamaio dalla parte giusta senza alzare gli occhi. Poi parla piano, come si legge una nota a margine."
    ottone "A inizio semestre l'Arconte aveva chiesto di te. Per nome. Non sei venut[fin]."
    ottone "Ha preso il nipote di un Eparca. Il primo giorno gli ha versato il vino di Glostok. Adesso copia decime in cantina."
    ottone "Era il tuo posto, ragazz[fin]. Qui dentro i posti vuoti non restano vuoti. Restano di qualcun altro."
    return

# Druso: l'Ode a un'altra musa (taverna).
label echi_rea_ode_altrui:
    scene bg vicoli_zefiro with dissolve
    "Al Becco Storto, a metà serata, il tavolo dei carrettieri attacca un coro. Lo sanno tutti a memoria."
    show druso ghigno at left with easeinleft
    druso "«Ode alla novellina del Ramo di Vittoria»! In piedi, musa! Gli altri: bevete e invidiate!"
    "Lei, a un tavolo d'angolo, ride più forte di tutti. La serata di versi di Druso: un pubblico, una musa. Io avevo altro da fare."
    "Indecente, puntuale, ben scritta. Doveva avere il mio nome."
    return

# Icaro: il posto al tavolo grande (fumeria).
label echi_rea_tavolo_altrui:
    scene bg vicoli_zefiro with dissolve
    show icaro neutro with dissolve
    "Al tavolo grande, accanto a Icaro, siede un ragazzo del Ramo di Iperione. Conta le carte muovendo le labbra."
    "Era il posto che Icaro mi aveva offerto. Non ci sono andat[fin]."
    icaro "Conta male. Ma conta per me, e quando sbaglia, sbaglia dalla mia parte."
    show icaro furbo with qdiss
    icaro "Non guardarlo così. Le sedie vuote non fruttano interessi."
    return

# Ofelia: la lettera di Ascadeo letta da un altro (riti, Vanna).
label echi_rea_lettera_altrui:
    scene bg corridoio_ceppo with dissolve
    show vanna neutra with dissolve
    vanna "Sai che Ofelia ha fatto leggere a voce alta una lettera di suo fratello Ascadeo? Sotto la torcia, in fondo al corridoio di Glauco."
    vanna "L'ha letta un pretendente del Ramo di Vittoria. Nota compresa. Ascadeo l'ha quotato il doppio, per una settimana."
    vanna "Poi Ofelia l'ha cancellato. Ma per una settimana ha valso il doppio di te, [fratello_t]."
    "Quella lettera, Ofelia l'aveva chiesta a me. Avevo altro da fare."
    return


## 8. Scelte che tornano ######################################################

# Icaro: la riga aggiunta alla pagina di Druso (taverna).
label echi_rea_druso_quarantatre:
    scene bg vicoli_zefiro with dissolve
    show druso irritato at left with easeinleft
    druso "Quarantatré! QUARANTATRÉ! Mio fratello mi ha sventolato il registro sotto il naso. «Il vino della mensa», dice. Testimone: tu."
    pc "Hai bevuto il mio vino, Druso."
    show druso ghigno at left with qdiss
    druso "E con gusto! Ma farmelo mettere a registro da Icaro... questa è crudeltà vera. Mi commuove."
    druso "Oste! Il giro di stasera lo paga Icaro. Pagina trentuno."
    return

# Ofelia: la lettera bruciata e la voce nuova nel libro di Ascadeo (riti).
label echi_rea_ascadeo_quota:
    scene bg corridoio_ceppo with dissolve
    show vanna neutra with dissolve
    vanna "Ascadeo, il fratello minore di Ofelia, ha aperto una voce nuova nel suo libro di scommesse. Una voce sola, per un nome solo."
    vanna "«Brucia le lettere.» Accanto, la quota. Dicono che sia salita. Dicono che Ofelia, leggendola, abbia riso."
    vanna "Che lettere bruci, [fratello_t]? E perché non le bruci con me?"
    return
