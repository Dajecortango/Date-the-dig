# Route Icaro — Atto 1: eventi 1-2 e interludi 1-2 (Lune II-III).

## Evento 1 — Il tavolo grande ###############################################

label icaro_ev1:
    scene bg vicoli_zefiro with fade
    "La fumeria dietro la Consorteria non ha insegna. Ha una porta bassa, un odore dolce di resina e una tenda che sa di soldi."
    "Dentro, il fumo sta a mezz'aria come un secondo soffitto. Sotto, i tavoli. In fondo, quello grande."
    show icaro neutro with dissolve
    "Il tavolo grande della saletta: posta alta, un mercante della Consorteria, due Eparchi, e Icaro che vince con la pazienza di un esattore."
    icaro "Siediti qui. Non per giocare: per contare. Voglio vedere se conti come guardi."
    pc "Contare cosa, di preciso?"
    icaro "Tutto. Le carte uscite, le monete nel piatto, quante volte il mercante si tocca l'orecchio."
    icaro "Se lo tocca quando bluffa. Sette volte, finora. Ha perso sei mani."
    "Mescola senza guardare il mazzo. Le carte gli scorrono tra le dita come acqua in un canale."
    "Un'Eparca gli chiede se ha mai pensato di fare il prestigiatore. Lui risponde che i prestigiatori si fanno pagare dopo. Lui, prima."
    "Tre mani dopo, il mercante — in perdita secca — ringhia che «qualcuno bara»."
    "Due monete d'argento, nel piatto, sono finite dal lato sbagliato. Il lato di Icaro. Non ho visto come."
    menu:
        "Gli occhi del tavolo cercano un colpevole. Io so chi è."
        "«Ho contato ogni carta. Tutto regolare.» (mentire per lui)":
            $ icaro_affinity += 2
            $ flag_icaro_coperto = True
            icaro "Il [figlio_t] di Briseide conta bene. Pago da bere al tavolo: la sfortuna va consolata."
            "Sotto il tavolo, il suo piede sposta la mia sedia di un palmo. Più vicina al lume, dove si vede meglio il panno."
            "Più tardi, fuori, mi mette in mano tre Scudi senza guardarmi."
            $ scudi += 3
            show icaro furbo with qdiss
            icaro "Non è un regalo. È un dividendo. I soci si pagano."
            pc "E se li rifiutassi?"
            icaro "Li rimetterei a bilancio, col dieci per cento d'interessi a tuo carico. Prendili: ti conviene."
        "Tacere e guardare altrove":
            $ icaro_affinity += 1
            "Non dico nulla. Il mercante sbollisce da solo. Icaro annota il mio silenzio come annota tutto: alla voce «utile»."
            icaro "Silenzio: buono. Hai distolto gli occhi un secondo tardi, e il mercante l'ha notato. La prossima volta, mezzo secondo prima."
        "Dare ragione al mercante":
            $ congelate.add("icaro")
            icaro "Contate pure. Tutto regolare, come sempre."
            "Il mercante mi ringrazia con una pacca sulla spalla. È l'unico, stasera, a guardarmi in faccia."
            "Regolare, adesso. E il posto al tavolo grande, per me, non esiste più. Da nessuna parte, mai più."
    "Fuori, i vicoli di Zefiro sono ancora umidi di pioggia. L'odore di resina mi resta addosso fino al mattino."
    return


## Interludio 1 — Giorno di riscossione ######################################

label icaro_int1:
    scene bg vicoli_zefiro with fade
    "Il martedì la fumeria non apre ai giocatori. Apre ai debitori."
    show icaro neutro with dissolve
    "Icaro siede al tavolo piccolo con un registro rilegato in cuoio nero. Accanto, la pipa spenta e un calamaio."
    icaro "Giorno di riscossione. Tu stai lì e guardi. Se qualcuno piange, non consolarlo: alza il prezzo."
    "Il primo è un apprendista della Consorteria. Deve undici Scudi. Ne porta nove e una fibbia d'ottone."
    icaro "Fibbia: uno Scudo e mezzo. Mezzo Scudo d'interessi. Sei pari. Avanti."
    "Il secondo è un Eparca col cappuccio calato. Non porta niente. Porta una storia."
    icaro "Le storie non le prendo a pegno. Hanno troppa concorrenza."
    "L'Eparca se ne va con una settimana in più e la faccia di chi l'ha pagata cara."
    pc "Quante pagine ha quel registro?"
    icaro "Trecentoventi. Ne ho usate centoquaranta. Prima dei trent'anni lo chiudo."
    show icaro furbo with qdiss
    icaro "Vuoi sapere chi c'è dentro. Te lo leggo in faccia. Pagina trentuno."
    "Gira il registro verso di me. Una colonna intera con lo stesso nome, scritto con rabbia crescente: Druso."
    icaro "Mio fratello mi deve quarantadue Scudi, una spada da parata e una cena da Corrado."
    icaro "La spada l'ha impegnata. Dice che l'ha persa in una rissa. La cena l'ha mangiata davanti a me. Il resto lo nega."
    pc "E Caino?"
    show icaro neutro with qdiss
    icaro "Caino non ha debiti. Caino ha crediti. Con tutti. Anche con me. Non è una pagina che mostro."
    menu:
        "Il registro è aperto davanti a me. Icaro aspetta di vedere dove guardo."
        "Aggiungere una riga alla pagina di Druso":
            pc "Ieri alla mensa ha bevuto il mio vino. Ha detto che pagavi tu."
            show icaro sereno with qdiss
            "Icaro intinge la penna. Scrive. Soffia sull'inchiostro con un piacere che non si prende la briga di nascondere."
            icaro "Quarantatré. Hai il senso della famiglia, [player_name]."
        "Chiudere il registro senza leggere oltre":
            "Lo chiudo io, piano, fermandomi un dito prima del suo pollice."
            show icaro sorpreso with qdiss
            icaro "Non hai cercato la tua pagina."
            pc "Ce n'è una?"
            icaro "Non ancora. Ma tutti, a questo punto, la cercano."
        "«L'Eparca aveva l'anello del Ramo. Poteva pagarti.»":
            icaro "Lo so. Gli ho dato una settimana apposta."
            icaro "Un debitore ricco che ti deve un favore vale più dei suoi Scudi. Gli Scudi si spendono. I favori fruttano."
            "Annota qualcosa a margine. Non sul debitore. Su di me, credo."
    "Riscossione finita. Icaro riaccende la pipa, e il fumo si posa sul registro come un panno sul tavolo."
    icaro "Domani dimentica tutto quello che hai visto. Tranne le cifre. Quelle restano tra noi."
    return


## Evento 2 — Gli averi ######################################################

label icaro_ev2:
    scene bg vicoli_zefiro with fade
    show icaro neutro with dissolve
    "Mi aspetta all'angolo del vicolo dei cordai, con una lanterna schermata e un mazzo di chiavi che non tintinna."
    icaro "Niente domande sulla strada. La strada è parte del segreto."
    "Tre svolte a sinistra, due cortili, una scala che sale per poi scendere. Alla fine mi gira la testa, e lui sembra soddisfatto."
    "Mi porta in un magazzino dietro la Consorteria. Dentro: casse, stoffe, lampade di Lumina, un servizio da tè di Glostok. Tutto suo. Tutto inventariato."
    icaro "La gente colleziona titoli, favori, sentimenti. Aria. Io colleziono cose. Le cose non mentono, non ti tradiscono e non chiedono nulla: esistono, e sono mie."
    "Ogni oggetto ha un cartellino. Data, provenienza, prezzo pagato, prezzo stimato. Il secondo numero è sempre più alto del primo."
    pc "Come hai pagato tutto questo?"
    icaro "Carte, dadi, debiti altrui. Una volta, con una scommessa su quanto avrebbe resistito Druso senza parlare."
    icaro "Undici minuti. Lui giura nove. Ma la lampada di Lumina sta qui, non da lui."
    menu:
        "Me lo dice senza vergogna. È la sua visione del mondo, nuda."
        "«E ogni cosa qui dentro ha una storia. Raccontamene una.»":
            $ icaro_affinity += 2
            "Esita. Poi prende la lampada più brutta dello scaffale e racconta: la prima cosa che abbia mai vinto, a nove anni, barando contro un adulto."
            icaro "Valore di mercato: zero. Non è in vendita. Capisci la differenza, o devo rallentare?"
            pc "Capisco. È l'inventario che non mostri."
            show icaro sorpreso with qdiss
            icaro "...mh. Conti meglio del previsto."
            "Rimette la lampada sullo scaffale. Poi la sposta di un dito, più in vista."
        "«Le cose non ti terranno compagnia da vecchio.»":
            $ icaro_affinity -= 1
            show icaro irritato with qdiss
            icaro "La compagnia è una spesa. Le cose sono un attivo. Il tuo bilancio sentimentale non torna, e non è un mio problema."
            pc "E il giorno che qualcuno ti svuota il magazzino?"
            icaro "Nessuno svuota il mio magazzino. Sono io quello che svuota i magazzini."
        "Sollevare una tazza del servizio di Glostok, controluce":
            show icaro irritato with qdiss
            icaro "Giù. Piano. Quella tazza vale un mese di mensa, e le tue dita valgono meno."
            "La rimetto. Lui la gira di un quarto, finché il manico non torna esattamente dov'era."
            icaro "Le cose hanno un posto. Io lo so. Loro lo sanno. Tu stai imparando."
    "Usciamo. Chiude la porta con tre chiavi, in un ordine che non riesco a seguire."
    icaro "Se un giorno ritrovi la strada da sol[fin], dimmelo. Cambio magazzino."
    return


## Interludio 2 — Lezione di mani ############################################

label icaro_int2:
    scene bg vicoli_zefiro with fade
    "Il mercato coperto di Zefiro, all'ora in cui le bancarelle chiudono e i borseggiatori aprono."
    show icaro neutro with dissolve
    icaro "Lezione. Gratis, il che dovrebbe insospettirti."
    pc "Lezione di cosa?"
    show icaro furbo with qdiss
    "Apre la mano. Dentro c'è il mio fermaglio. Quello che avevo addosso un minuto fa."
    with vpunch
    pc "Quando...?"
    icaro "Mentre guardavi la lanterna che ti ho indicato. Si indica sempre qualcosa. La gente guarda il dito, mai l'altra mano."
    "Me lo rende. Non direttamente: lo lascia cadere nella mia tasca mentre mi passa accanto. Non lo sento entrare."
    icaro "Le dita fanno il dieci per cento. Il resto è dove guarda l'altro. Tu hai fissato la lanterna quattro secondi. Ne bastavano due."
    "Mi mostra tre cose: il passo di fianco, la spinta che sembra una scusa, la domanda che occupa la testa."
    icaro "L'ho imparato a otto anni. A nove ho smesso di farmi prendere."
    pc "E chi ti ha preso, a otto?"
    show icaro neutro with qdiss
    icaro "Caino. Mi ha restituito il borsello che gli avevo rubato. Poi mi ha chiesto il dieci per cento per non dirlo a Lenora."
    icaro "Gliel'ho pagato. È l'unico debito che abbia mai saldato in anticipo."
    menu:
        "Mi porge una moneta sul palmo aperto. «Ora tocca a te. Rubamela.»"
        "Indicare una lanterna e prendere la moneta con l'altra mano":
            "Indico. Lui non guarda la lanterna. Guarda me, divertito, e chiude la mano un attimo prima."
            icaro "Hai copiato la lezione. Ma la lezione l'ho scritta io. Non si deruba l'autore."
        "Fargli una domanda vera, e prenderla mentre risponde":
            pc "Cosa porteresti via, se il magazzino bruciasse?"
            show icaro sorpreso with qdiss
            "Ci pensa. Davvero. E per un istante, mentre pensa, la mano si apre."
            "La moneta è mia. Lui se ne accorge tre respiri dopo."
            icaro "...domanda sleale. Ottima. Tienila. Tre respiri: devo lavorarci."
        "Rifiutare: «Non rubo ai soci.»":
            show icaro irritato with qdiss
            icaro "I soci sono quelli a cui conviene di più rubare. Si fidano."
            "Ma intasca la moneta con un mezzo sorriso. Dieci passi dopo la tira fuori e la guarda di nuovo."
    "Le bancarelle sono chiuse. Icaro si incammina senza salutare, le mani in tasca. Le sue, credo."
    "A casa, nel mio borsello, trovo un bottone d'osso che non è mio. E un biglietto: «Interessi.»"
    return


## Deviazione (Luna II+) — Il debito di un altro ###############################

label icaro_debito_altrui:
    scene bg vicoli_zefiro with fade
    "Vicolo dei tintori, dopo il tramonto. L'acqua dei canali di scolo è blu, poi rossa, poi di nessun colore."
    show icaro neutro with dissolve
    icaro "Riscossione a domicilio. Il debitore non viene, quindi vado io. Tu tieni la lanterna e la bocca chiusa."
    "La porta è bassa. Dentro: una stanza sola, un telaio fermo, una donna con le mani viola fino ai polsi. Due bambini dietro la tenda fingono di dormire."
    "La donna mette sul tavolo tre monete e un pettine d'osso. Ne deve diciotto."
    icaro "Pettine d'osso, lavoro di Glostok. Due Scudi. Tre più due fa cinque."
    "Apre il registro. Intinge la penna. Scrive, a lungo, molto più a lungo di quanto serva per un cinque."
    icaro "Saldato. Il resto l'ha pagato il pettine. Era un pettine molto prezioso."
    "La donna non capisce. Io sì. Icaro chiude il registro prima che lei possa leggere."
    scene bg vicoli_zefiro with fade
    show icaro irritato with dissolve
    "Fuori, nel vicolo, si accende la pipa con troppa attenzione. Non mi guarda."
    icaro "Non hai visto niente. Un creditore indulgente è un creditore morto: domani avrei la fila fino al canale."
    menu:
        "Il fumo sale dritto. Lui aspetta una risposta senza chiederla."
        "«Il pettine valeva mezzo Scudo. L'osso era di vacca, non di Glostok.»":
            $ icaro_debito_esito = "dettaglio"
            $ icaro_affinity += 1
            show icaro sorpreso with qdiss
            icaro "...hai guardato i denti del pettine."
            show icaro furbo with qdiss
            icaro "Allora sai anche che ho barato contro me stesso. Tredici Scudi di perdita, volontaria. Tienilo per te."
        "Restare in silenzio e passargli la lanterna":
            $ icaro_debito_esito = "silenzio"
            "Gli porgo la lanterna. Lui la prende. Le nostre dita non si toccano: Icaro non sbaglia mai le distanze."
            show icaro sereno with qdiss
            icaro "Bene. Silenzio senza fattura. Lo annoto."
        "«Lo racconterò a Druso. Gli farà bene sapere che hai un cuore.»":
            $ icaro_debito_esito = "minaccia"
            show icaro irritato with qdiss
            icaro "Druso non ci crederebbe. E se ci credesse, verrebbe a chiedermi uno sconto sui suoi quarantadue Scudi."
            icaro "Quindi no. Non lo racconterai. Ti costerebbe quarantadue Scudi di imbarazzo, a te, non a me."
    "Torniamo verso la fumeria. A un angolo si ferma, torna indietro di tre passi e lascia un'altra moneta sul davanzale dei tintori."
    icaro "Interessi negativi. Una pratica contabile modernissima. Non provare a capirla."
    return
