# Echi: scelte passate che tornano in un'altra scena (registry ECHI in
# game/conseguenze.rpy). Le gioca cal_attivita a fine attivita', una volta
# sola per partita. Chi parla deve poter sapere: chi c'era, chi frequenta il
# luogo, o chi raccoglie pettegolezzi per mestiere (Vanna, Corrado, Ottone).

# Caino: caduto nella trappola delle Candele Spente (registri).
label echi_caino_ottone:
    scene bg studio_glauco with dissolve
    "A fine giornata Ottone si ferma accanto al mio banco. Guarda le colonne, non me."
    ottone "L'Arconte non passa più da questa parte della sala. Te ne sei accort[fin] anche tu."
    ottone "All'Adunanza ha fatto una domanda, e qualcuno ha annuito. Qui dentro lo sanno tutti, ragazz[fin]: quello annuisce senza sapere."
    "Riprende a scrivere. La penna gratta, e per un po' mi sembra che scriva di me."
    return

# Caino: «Era un massacro» detto in faccia all'Adunanza (studio).
label echi_caino_corrado:
    scene bg studio_glauco with dissolve
    show corrado neutro with dissolve
    corrado "Dicono che all'Adunanza tu abbia chiamato il Ballo delle Candele Spente col suo nome. Davanti al figlio di Lenora."
    corrado "Studi la storia da poco e già la usi come una lama. Non so se esserne fiero o preoccupato, [fratello_t]."
    pc "Fiero. Poi preoccupato."
    corrado "L'ordine giusto. Nella Famiglia è sempre quello."
    return

# Lenora: l'insolenza alla grata (studio o riti).
label echi_lenora_corrado:
    scene bg corridoio_ceppo with dissolve
    show corrado neutro with dissolve
    corrado "Dicono che davanti alla grata [un_t] [figlio_t] di Briseide abbia risposto a tono. Un[fin] sol[fin], su venti."
    corrado "Lenora non dimentica, [fratello_t]. Riclassifica. E i registri di Pandora non hanno gomma."
    "Lo dice serio. Poi, voltandosi, gli scappa mezzo sorriso: Corrado non ha mai risposto a tono a nessuno."
    return

# Icaro: la bugia al tavolo grande (città).
label echi_icaro_mercante:
    scene bg vicoli_zefiro with dissolve
    "Al mercato coperto un banco mi chiude la tenda in faccia. Lo riconosco: è il mercante del tavolo grande di Icaro. Quello in perdita secca."
    "«[Il_t] [figlio_t] di Briseide che conta bene», dice alla vicina. Abbastanza forte perché io senta."
    "A Zefiro una bugia costa poco. Ma la paghi a rate, e ogni banco del mercato tiene il conto."
    return

# Druso: il lanternaio dei vicoli bassi (città).
label echi_druso_lanternaio:
    scene bg vicoli_zefiro with dissolve
    "Il lanternaio dei vicoli bassi mi ferma sotto il portico. Ha ancora un occhio giallo e viola, ma sorride."
    "Mi riempie la lanterna e non vuole un soldo. «Per te e per il grosso che morde», dice."
    "Druso mi aveva chiesto di non dirlo a nessuno. Non è servito: a Zefiro i vicoli parlano da soli."
    return

# Caino e Druso: il Codice del Teschio (taverna).
label echi_teschio_taverna:
    scene bg vicoli_zefiro with dissolve
    show druso ghigno at left with easeinleft
    druso "Silenzio, plebe! Un brindisi al mio testimone del Teschio: l'unic[fin] in tutta Rocca Tempesta che sta dalla mia parte contro mio fratello!"
    "Tutta la taverna alza i boccali. Nessuno sa cosa sia il Teschio. Tutti lo temono lo stesso."
    pc "Non sto dalla parte di nessuno, Druso."
    show druso neutro at left with qdiss
    druso "Bugia. Stai dalla parte del boccale. Che è la mia."
    return

# Aede: il vicolo della Contrada Marcassa, coperto (riti).
label echi_aede_marcassa:
    scene bg corridoio_ceppo with dissolve
    show vanna neutra with dissolve
    vanna "Hai sentito? Un cambiavalute, nella Contrada Marcassa. L'hanno trovato tra le casse, con l'anello d'oro ancora al dito."
    vanna "Dicono un regolamento di conti tra usurai. Debiti, Rundeberg, la solita storia."
    "Taglio il pane per il brodo. Le mani non mi tremano. Ho detto che non avevo visto niente, e a quanto pare so mantenere la parola."
    return

# Aede: «Questo è assassinio» (riti).
label echi_aede_orari:
    scene bg corridoio_ceppo with dissolve
    show vanna neutra with dissolve
    vanna "Che hai fatto alla volpe rossa, [fratello_t]? In cortile si allena dall'altra parte, adesso. Il più lontano possibile da dove ti metti tu."
    pc "Le ho detto la verità."
    vanna "Ah. Allora è peggio di quanto pensassi."
    return

# Ofelia: fuori dalla corte dopo il secondo invito mancato (riti).
label echi_ofelia_lista:
    scene bg corridoio_ceppo with dissolve
    show vanna neutra with dissolve
    vanna "Notizie dalla serra, [fratello_t]. Ofelia ha cancellato un nome dalla lista dei pretendenti. Con l'inchiostro rosso, davanti a tutti."
    vanna "Indovina quale."
    "Non serve indovinare. Ofelia non ripete gli inviti. Lo sapevo, e ho lasciato cadere il secondo lo stesso."
    return

# Druso: il quaderno dei versi seri (taverna, Luna V+).
label echi_druso_quaderno:
    scene bg vicoli_zefiro with dissolve
    show druso ghigno at left with dissolve
    if druso_quaderno_esito == "detto":
        druso "Pagina sette. L'ho rifatta. «Tempesta» adesso fa rima con «resta». Non dire niente, la faccia che fai basta."
    elif druso_quaderno_esito == "chiuso" and "druso_luna5" in eventi_visti:
        druso "Sai cosa ho capito, alla sfida dei versi? Che nessuno restituisce chiuso un quaderno aperto. Tu l'hai fatto. Ci sto ancora pensando."
    elif druso_quaderno_esito == "chiuso":
        druso "Nessuno restituisce chiuso un quaderno aperto. Tu l'hai fatto. Ci sto ancora pensando."
    else:
        druso "Il quaderno sotto la panca. L'ho spostato. Qualcuno l'aveva rimesso al contrario, e io lo lascio sempre dritto."
        "Non mi guarda mentre lo dice. Beve. Lo sa."
    return

# Druso: l'udienza privata, raccontata dal fratello (fumeria, Luna V+).
label echi_druso_udienza:
    scene bg vicoli_zefiro with dissolve
    show icaro neutro with dissolve
    icaro "Madre ha chiesto a Druso se ha qualcuno di serio. Lui è tornato a casa con la neve nella barba e ha cantato per tre giorni."
    if druso_udienza_esito == "neve":
        icaro "Dice che qualcuno gli ha tirato una palla di neve davanti alla Rocca. Vorrei sapere chi. Per mandargli un conto, o un regalo."
    else:
        icaro "Dice che qualcuno l'ha aspettato nel cortile dei carri. In famiglia, nessuno aspetta nessuno. Annoto."
    return

# Icaro: la tintora del condono riconosce chi teneva la lanterna (citta').
label echi_icaro_tintora:
    scene bg vicoli_zefiro with dissolve
    "Al mercato una donna con le mani viola fino ai polsi mi ferma per la manica. La tintora del vicolo."
    "«Lei era con il signor Icaro. Il pettine, quel pettine... valeva così tanto?»"
    if icaro_debito_esito == "dettaglio":
        "Ho visto i denti di quel pettine. Le dico di sì. Valeva moltissimo."
    else:
        "Le dico di sì. Mi stringe la mano con le dita viola e se ne va prima che io possa aggiungere altro."
    return

# Icaro: la febbre, ricordata da lui solo (fumeria, Luna V+).
label echi_icaro_febbre:
    scene bg vicoli_zefiro with dissolve
    show icaro furbo with dissolve
    if icaro_febbre_esito == "conta":
        icaro "Il servizio da tè: sette tazze. L'inventario l'hai chiuso tu, quella sera. Nessuno mi ha mai corretto un totale. Lo tengo così."
    elif icaro_febbre_esito == "aiuto":
        icaro "Corrado mi ha mandato il conto dell'infuso. L'ho pagato. È la prima volta che pago una cosa che non volevo."
    else:
        icaro "Il biglietto «Non bussare» l'ho tolto dalla porta. Nessuno lo leggeva comunque. Tranne te."
    return

# Ofelia: lo specchio e i tre vestiti (corte, Luna V+).
label echi_ofelia_specchio:
    scene bg sala_svelo with dissolve
    show ofelia neutra with dissolve
    if ofelia_specchio_esito == "rosso":
        ofelia "Il rosso l'ho rimesso, ieri. Nessuno mi ha chiesto chi l'aveva scelto. Peccato: avevo la risposta pronta."
    elif ofelia_specchio_esito == "specchio":
        ofelia "Quella cosa sul nero. Dimenticala. Lo specchio l'ha già fatto."
    else:
        ofelia "Stai bene con tutti e tre, mi hai detto. Ho buttato il verde. Così adesso hai torto almeno su uno."
    return

# Ofelia: il ballo dei pretendenti, raccontato da Vanna (riti, Luna V+).
label echi_ofelia_ballo:
    scene bg corridoio_ceppo with dissolve
    show vanna neutra with dissolve
    if ofelia_ballo_esito == "me":
        vanna "Al ballo di Glauco, dicono, Ofelia non ha rimandato a casa nessuno. Prima volta in tre anni. Ascadeo ha perso una scommessa grossa."
        vanna "E dicono che è colpa tua. Non chiedermi chi lo dice. Lo dicono tutti."
    elif ofelia_ballo_esito == "biondo":
        vanna "Il ragazzo biondo dei versi rubati ha lasciato Zefiro. Sua madre dice che l'aria del Sud gli fa bene. Al Sud, i versi altrui costano meno."
    else:
        vanna "Al ballo di Glauco qualcuno ha detto no a Ofelia. Davanti a tutti. Mezza serra non parla d'altro, l'altra metà ne scrive."
    return
