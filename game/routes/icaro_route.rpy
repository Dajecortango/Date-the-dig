# Route Icaro — "Untouchable" (romance solo per protagonista donna;
# per gli uomini la linea "Bro", stessa trama, finale platonico).
# La più difficile del gioco (5/5). Possessivo: niente poliamore, mai.

default icaro_impegnato = False
default flag_icaro_coperto = False
default icaro_partita = None        # "copre" | "smaschera" | "silenzio"
default icaro_climax_scelta = None  # "dettaglio" | "silenzio" | "accusa"

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

    # Possessività: dopo che il suo interesse e' acceso (>=6), accettare
    # l'invito di un altro personaggio lo chiude per sempre.
    def icaro_gelosia(ev):
        if (ev.get("tipo") == "invito"
                and ev.get("char") not in (None, "icaro")
                and store.icaro_affinity >= 4
                and store.route_attiva is None
                and "icaro" not in store.congelate):
            store.congelate.add("icaro")
            renpy.notify("Icaro non dimentica.")

    cal_post_evento_hooks.append(icaro_gelosia)


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
            icaro "Saresti [il_t] prim[fin]. E io non investo sulle prime volte."
        "Tacere e guardare altrove":
            $ icaro_affinity += 1
            "Non dico nulla. Il mercante sbollisce da solo. Icaro annota il mio silenzio come annota tutto: alla voce «utile»."
            icaro "Il silenzio è una moneta che pochi sanno spendere. L'hai spesa bene. Non benissimo."
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
    icaro "Il trucco non sta nelle dita. Sta nell'attenzione degli altri. È una moneta, e tutti la spendono male."
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
            icaro "...domanda sleale. Ottima. Tienila: l'hai pagata con l'unica valuta che non accetto mai."
        "Rifiutare: «Non rubo ai soci.»":
            show icaro irritato with qdiss
            icaro "I soci sono quelli a cui conviene di più rubare. Si fidano."
            "Ma intasca la moneta con un mezzo sorriso, come chi ha appena sentito una regola che non conosceva."
    "Le bancarelle sono chiuse. Icaro si incammina senza salutare, le mani in tasca. Le sue, credo."
    "A casa, nel mio borsello, trovo un bottone d'osso che non è mio. E un biglietto: «Interessi.»"
    return


## Evento 3 — La serata placida ##############################################

label icaro_ev3:
    scene bg cala_notte with fade
    show icaro sereno with dissolve
    "Un tetto sopra la Consorteria, due stuoie, la pipa. Zefiro brilla in basso come il suo magazzino: tutta roba che prima o poi, dice, sarà sua."
    icaro "Regola della serata: niente domande, niente debiti, niente contatto. Si fuma, si guarda, si tace. Chi rompe la regola paga."
    "Prepara la pipa con cura da orefice: il fornello pulito, l'erba sbriciolata tra pollice e indice, un pizzico alla volta."
    icaro "Erba delle colline di Lumina. Ne compro una libbra a stagione e non ne regalo mai. Questa è un prestito."
    "Me la passa senza che le nostre dita si sfiorino. È un gesto che ha studiato."
    "Fumiamo. Guardiamo. Taccio. Un'ora, forse due. È la cosa più vicina alla pace che il Nord mi abbia concesso."
    "Una volta, giù in strada, qualcuno urla il nome di Druso. Icaro chiude gli occhi e conta fino a dieci, a fior di labbra."
    "Al dieci l'urlo è passato. Riapre gli occhi come se niente fosse."
    if player_gender == "f":
        show icaro imbarazzato with dissolve
        icaro "...annotazione d'inventario. La tua presenza non è un passivo. Non capita. Non capita mai."
        $ icaro_affinity += 2
        "Da Icaro, è una dichiarazione d'amore in piena regola contabile."
        "Poi torna a guardare la città, e per il resto della notte non dice più niente. Il silenzio, stavolta, pesa diverso."
    else:
        show icaro imbarazzato with dissolve
        icaro "...annotazione d'inventario. Sei l'unico uomo che non mi fa venire voglia di contare l'argenteria. Tienitelo stretto."
        $ icaro_affinity += 2
        pc "Lo prendo come un complimento."
        icaro "È un'annotazione. I complimenti non li faccio. Costano."
    return


## Interludio 3 — La lettera di Lenora #######################################

label icaro_int3:
    scene bg vicoli_zefiro with fade
    "La fumeria è quasi vuota. Un vecchio dorme su un cuscino. Un altro gioca a solitario, e perde."
    show icaro neutro with dissolve
    "Icaro ha davanti una lettera sigillata. Ceralacca verde, lo stemma di casa. La gira tra le dita come una carta che non vuole scoprire."
    icaro "Lenora. Mia madre. Scrive una volta a Luna, a ciascuno di noi tre. Stesse parole, credo. Non ho mai controllato."
    pc "Non la apri?"
    icaro "La apro sempre. Dopo la terza pipa. Stasera sono alla seconda, e tu sei arrivat[fin] in tempo."
    "Fuma la terza. Poi rompe il sigillo con l'unghia del pollice, pulito, senza sbriciolare la cera."
    show icaro sereno with qdiss
    icaro "«Mangia. Non barare con chi non può permetterselo. Di' a Druso di scrivermi. Di' a Caino che lo so.»"
    icaro "Che cosa sappia, non lo dice mai. Caino trema lo stesso. È il talento di Lenora: debiti senza cifra."
    pc "E per te? C'è una riga solo per te?"
    "Gira il foglio. In fondo, una riga più piccola, quasi a margine."
    show icaro imbarazzato with qdiss
    icaro "«E tu, Icaro, smettila di contare tutto. Le cose migliori non si contano.»"
    icaro "Lo scrive ogni volta. Ogni volta ha torto. Ogni volta lo rileggo."
    menu:
        "Ripiega la lettera in quattro. Aspetta che io dica qualcosa, o niente."
        "«Ha torto. Tu conti, e le cose migliori le trovi lo stesso.»":
            show icaro sorpreso with qdiss
            icaro "...è la prima volta che qualcuno dà torto a Lenora davanti a me."
            icaro "Non ripeterlo davanti a lei. Né davanti a Caino. Ti farebbe pagare anche questo."
        "Non dire niente. Passargli la pipa, già carica":
            "Gliela porgo dal lato del cannello. Lui la prende senza sfiorarmi."
            show icaro sereno with qdiss
            icaro "Quarta pipa. Non è mai successo. Lenora inorridirebbe."
            "Lo dice come se fosse una buona notizia."
        "«Rispondile. Ti tengo io la lanterna.»":
            show icaro irritato with qdiss
            icaro "Rispondere a Lenora è un contratto a tempo indeterminato. Lei risponde alla risposta."
            "Ma prende la penna lo stesso. Scrive tre righe, le cancella, ne scrive una."
            icaro "Fatto. «Mangio.» Basta e avanza."
    if player_gender == "f":
        "Infila la lettera nel registro, alla pagina delle cose che non sono in vendita."
        "Me ne accorgo perché la pagina è quasi vuota. E perché lui si accorge che me ne accorgo."
    else:
        "Infila la lettera nel registro. Poi si volta verso di me, serio."
        icaro "Druso direbbe che adesso siamo amici. Druso esagera sempre. Ma stasera, per una volta, non del tutto."
    return


## Impegno (scelta del cuore) ################################################

label impegno_icaro:
    scene bg vicoli_zefiro with fade
    "La fumeria è chiusa. Ha mandato via tutti, anche il vecchio che dorme sui cuscini: un'eccezione che deve essergli costata."
    show icaro neutro with dissolve
    "Mi aspetta al tavolo piccolo, quello dove non gioca: quello dove conta. Davanti a lui, un registro aperto su una pagina bianca."
    icaro "Siediti. Non è una partita. È peggio: è una trattativa."
    icaro "Ho fatto i conti tre volte. Una compagna è un passivo: tempo, attenzioni, rischio. Ogni logica dice di non firmare."
    icaro "Ma ho un buco nel bilancio da tre Lune, e il buco ha la tua faccia. Quindi: o sei l'eccezione che conferma ogni mia regola, o sei l'errore più costoso della mia vita. Scegli tu la voce."
    pc "E se fossi l'errore?"
    icaro "Allora l'avrò scelto io. È già più di quanto concedo agli errori degli altri."
    menu:
        "La pagina bianca aspetta. Icaro non firma mai per primo."
        "«Eccezione. E sono irrevocabile, come le tue regole.»" (peso=True):
            $ impegno_esito = True
            $ icaro_impegnato = True
            show icaro sereno with dissolve
            icaro "Irrevocabile. Parola da contratto serio. ...venduto."
            "Scrive una riga sola sulla pagina bianca, e la copre con la mano prima che io possa leggerla. Sua. Come tutto ciò che conta."
            icaro "Non chiedere cosa c'è scritto. Te lo dirò quando avrà maturato gli interessi."
            "Restiamo al buio, la pipa accesa tra noi. Non mi tocca. Ma per la prima volta non si scosta, quando la mia spalla sfiora la sua."
        "«Non sono una voce del tuo inventario.»" (peso=True):
            $ impegno_esito = False
            $ congelate.add("icaro")
            icaro "Allora il bilancio torna come prima. Perfetto. Era l'ipotesi più probabile, l'avevo già scontata."
            "Lo dice piatto, senza una piega. Solo che per la prima volta da che lo conosco, sbaglia il taglio del mazzo."
            "Chiude il registro. Prima di alzarsi, però, ci passa sopra il palmo, piano. Come per lisciare una pagina che nessuno scriverà."
    return

label impegno_bro:
    scene bg vicoli_zefiro with fade
    "La fumeria, a quest'ora, è solo fumo vecchio e sedie capovolte. Icaro ha tenuto acceso un lume solo."
    show icaro neutro with dissolve
    "Il tavolo piccolo. Icaro spinge verso di me una chiave di ferro, senza cerimonie."
    icaro "Magazzino. Copia unica. Se muoio, l'inventario va a te: Druso lo venderebbe, Caino lo tasserebbe. Tu lo conteresti. È il massimo che ho da offrire a un uomo, e non si ripete."
    pc "Druso e Caino lo sanno?"
    icaro "Druso lo saprà quando glielo dirai tu, ubriaco. Caino lo sa già. Caino sa sempre tutto: per questo non lo scelgo."
    menu:
        "La chiave pesa come un giuramento."
        "Prenderla" (peso=True):
            $ impegno_esito = True
            $ icaro_impegnato = True
            pc "La tengo. E non la conto: la custodisco."
            show icaro sereno with dissolve
            icaro "...custodire. Verbo accettabile. Fratello."
            "Accenna a tendermi la mano. Ci ripensa a metà strada e mi passa la pipa. Con lui, tra uomini, è la stessa cosa. Forse di più."
        "Rifiutarla" (peso=True):
            $ impegno_esito = False
            $ congelate.add("icaro")
            icaro "Come preferisci. L'offerta scade adesso e non rientra a listino."
            "Rimette la chiave nel taschino cucito all'interno del gilet. Non la vedrò più."
    return


## Bro 1 — Affari insieme (solo protagonista uomo) ###########################

label icaro_bro_affari:
    scene bg vicoli_zefiro with fade
    "Il mercato coperto, a metà pomeriggio. Banchi di stoffe, spezie, ferraglia. E in fondo un mercante di Glostok che vende tutto in fretta."
    show icaro neutro with dissolve
    icaro "Servizio da tè di Glostok. Trentadue pezzi. Il proprietario ha debiti di gioco, e i debiti di gioco hanno fretta."
    icaro "Io tratto. Tu stai accanto a me con la faccia di uno che ha già deciso di andarsene. Niente sorrisi. I sorrisi alzano i prezzi."
    pc "E se il mercante parla con me?"
    icaro "Non parlerà con te. Parlerà della tua faccia. È diverso."
    "Il mercante apre la cassa. Paglia, porcellana, un odore di cantina. Icaro prende una tazza e la guarda contro la luce come un gioielliere guarda un falso."
    icaro "Crepata. Questa. E questa. Il servizio vale la metà di quello che chiedi."
    "Il mercante giura sugli dei del Nord e su sua madre. Icaro aspetta che finisca, poi offre un terzo."
    menu:
        "Il mercante guarda me. Cerca un alleato, o almeno una crepa."
        "Restare zitto, braccia conserte, e guardare l'uscita":
            "Non dico niente. Guardo la porta del mercato come se avessi già un altro affare lì fuori."
            "Il mercante suda. Scende di prezzo due volte, da solo, senza che nessuno glielo chieda."
            show icaro furbo with qdiss
            icaro "Visto? La faccia giusta vale più dell'argomento giusto. Tu ce l'hai di natura. Non la sprecare in taverna."
        "Inventare un'offerta migliore, a un altro banco":
            pc "Il banco del vetraio ci ha offerto un servizio intero per meno. Andiamo, Icaro."
            show icaro irritato with qdiss
            "Icaro mi fulmina. Mezzo secondo. Poi annuisce, grave, come se l'avesse deciso lui."
            "Il mercante cede. Fuori dal mercato, Icaro mi ferma con due dita sul petto, e le ritira subito."
            icaro "Funziona. Ma l'hai improvvisato. Improvvisare è barare senza metodo. La prossima volta, il metodo me lo dici prima."
        "Indicare il bollo sotto un piattino: è ridipinto":
            "Sotto un piattino il bollo di Glostok ha i bordi troppo freschi. Lo giro verso Icaro, senza una parola."
            show icaro sorpreso with qdiss
            icaro "...ridipinto. Mezzo servizio è di Glostok, mezzo di un forno qualunque."
            show icaro furbo with qdiss
            icaro "Allora lo compriamo tutto. Al prezzo del forno qualunque. Poi lo rivendiamo come di Glostok a chi non gira i piattini."
            pc "Non è onesto."
            icaro "È commercio. L'onestà è un'altra merce: costa di più e rende di meno."
    "Il servizio finisce nel magazzino di Icaro, contato due volte. Lui mi mette in mano una tazza. Una sola, quella senza crepe."
    icaro "La tua parte. Un servizio scompagnato perde valore: così ho un motivo per tenerti d'occhio. Finché ce l'hai tu, il servizio è completo a metà."
    show icaro sereno with qdiss
    icaro "Non è un regalo. Gli uomini non si fanno regali. È una garanzia."
    "Me la infilo in tasca. Pesa poco. Lui la guarda sparire come si guarda un investimento a lungo termine."
    return


## Bro 2 — Il colpo (solo protagonista uomo) #################################

label icaro_bro_colpo:
    scene bg vicoli_zefiro with fade
    "Mezzanotte nella Consorteria. Le lanterne di Lumina, qui, arrivano stanche. Icaro mi aspetta sotto un portico, senza pipa."
    show icaro neutro with dissolve
    icaro "Druso mi deve una spada da parata. L'ha impegnata al banco dei pegni dietro l'angolo. Il che vuol dire che il banco ha la MIA spada."
    pc "E il banco lo sa?"
    icaro "Il banco sa solo quello che è scritto sulla ricevuta. La ricevuta dice Druso. Io stanotte riscuoto per conto di Druso. Senza dirglielo, e senza pagare."
    icaro "Non è un furto. È una correzione d'inventario."
    "Il banco dei pegni ha una porta col catenaccio, una finestra alta e una guardia che si addormenta in piedi. Icaro li ha contati tutti e tre, da giorni."
    icaro "Io entro dalla finestra. Tu resti fuori. Ti do una regola sola: se la guardia si sveglia, non scappare. Chi scappa ha qualcosa da nascondere."
    "Si arrampica sul muro come se il muro fosse una scala. Sparisce. Io resto nel portico, con la guardia a dieci passi e il cuore in gola."
    "Poi la guardia apre un occhio. Poi l'altro."
    menu:
        "La guardia si stira. Guarda il portico. Guarda me."
        "Fingermi ubriaco e chiedere la strada per il Becco Storto":
            "Barcollo verso di lui con una canzone di Druso in bocca. Quella sulla locandiera. La conosco tutta, purtroppo."
            "La guardia ride, mi indica la strada sbagliata, mi spinge via con una pacca. Dietro di lui, la finestra si richiude piano."
        "Restare fermo nell'ombra, senza respirare":
            "Non mi muovo. Chi scappa ha qualcosa da nascondere. Io sono una colonna del portico."
            "La guardia guarda nella mia direzione per un tempo lunghissimo. Poi sbadiglia, e riprende a dormire in piedi."
        "Fare un fischio basso, come quello dei lanternai":
            "Fischio. Due note, il segnale dei lanternai di Lumina quando passa la ronda. Dalla finestra non viene più nessun rumore."
            "La guardia si guarda intorno, non vede nessuno, maledice i lanternai. Quando torna a dormire, la finestra si apre di nuovo."
    "Icaro scende dal muro con una spada avvolta in un sacco. Non ha fretta. Non ha mai fretta."
    show icaro furbo with qdiss
    icaro "Riscossa. Sul banco ho lasciato la ricevuta di Druso, firmata da me per quietanza. Domani il banco cercherà lui."
    pc "Hai incastrato tuo fratello."
    icaro "Ho incastrato il suo debito. Lui c'era già dentro. Io l'ho solo messo in ordine."
    "Ci allontaniamo per i vicoli. Al secondo angolo si ferma, srotola il sacco e mi mostra l'elsa. Dorata, pacchiana, con una gemma finta."
    show icaro sereno with qdiss
    icaro "Brutta. Vale poco. Ma è mia, e nessuno tocca ciò che è mio."
    icaro "Stanotte sei rimasto. Non hai chiesto la tua parte. Due cose che non fa nessuno."
    "Mi passa la pipa, accesa al riparo di un portone. È il suo modo di stringere la mano. Tra noi, vale di più."
    return


## Fiaccolata (route attiva) #################################################

label icaro_fiaccolata:
    scene bg cala_notte with fade
    show icaro neutro with dissolve
    "La Calà. Icaro guarda le trecento lanterne con occhio da perito: «olio per quaranta Scudi che cola verso il fiume»."
    "Intorno a noi, coppie e fratellanze scendono verso l'acqua. Lui calcola a mezza voce quanto renderebbe affittare i gradini."
    icaro "Un soldo a gradino. Entro l'alba potrei comprarmi la Calà, e farla scendere a pagamento anche a Caino."
    if player_gender == "f":
        icaro "La leggenda della mano è un contratto verbale senza testimoni né penali. Ridicolo."
        "A metà discesa si ferma. Guarda la mia mano come guarda le carte prima di scoprirle."
        "Poi mi prende la mano. Lui, che detesta il contatto. La tiene per trecento gradini, rigida e attenta, come si tiene una cosa di valore."
        show icaro imbarazzato with dissolve
        icaro "Contratto ridicolo. Ma è mio, adesso. E io non mollo ciò che è mio."
        "In fondo, quando la lanterna tocca l'acqua, non la lascia. Conta i secondi sottovoce. Al sessanta smette di contare."
    else:
        show icaro sereno with qdiss
        icaro "Scendiamo dal lato asciutto. Niente mani: la leggenda parla chiaro e io non firmo contratti ambigui. Ma il gradino accanto al mio è tuo. Listino chiuso."
        "Un ragazzo ci urta. Icaro gli sfila il borsello, lo soppesa e glielo rimette in tasca prima che se ne accorga."
        icaro "Troppo leggero. Non vale il disturbo. A differenza della compagnia."
    return


## Luna V — La partita grossa ################################################

label icaro_luna5:
    scene bg vicoli_zefiro with fade
    "La saletta dietro la Consorteria, porte sbarrate. Stanotte non si gioca a Scudi: si gioca a carichi, case, quote di nave."
    "Le tende pesanti coprono le finestre. Si respira resina, sudore e cera calda."
    "Al tavolo grande, due uomini del Ramo di Vittoria. Teucro, Arconte, un anello a ogni dito. E suo nipote Milone, giovane, occhi svelti."
    show icaro neutro with dissolve
    icaro "Siediti dietro di me. Non toccare niente, non dire niente. Stanotte il silenzio vale un magazzino."
    pc "E se perdi?"
    icaro "Non perdo. Ma nel caso, io non ho mai visto né te né questo tavolo."
    "Il piatto cresce mano dopo mano. Teucro ci butta la quota di un carico di sale. Icaro, l'atto del suo magazzino."
    "L'atto. La cosa che ama di più, in mezzo al panno, come un pegno qualunque."
    "Teucro gioca piano, sicuro. Vince le mani piccole, lascia le grandi. Gioca come chi sa già come finisce."
    "Icaro lo osserva tra una boccata e l'altra. Per la prima volta da che lo conosco, conta. E il conto non gli torna."
    show icaro furbo with qdiss
    "Ultima mano. Icaro riaccende la pipa, con calma. Nel gesto, una carta scivola dal polsino al palmo."
    "Io l'ho vista. E anche Milone."
    with vpunch
    "Milone batte la mano sul panno. «La manica, Icaro. Mostra la manica.»"
    show icaro irritato with qdiss
    icaro "La mia manica è sporca di cenere. Come la tua educazione."
    "Teucro sorride. E mentre tutti guardano Icaro, io guardo Teucro."
    "L'anello col castone piatto, inclinato verso il mazzo. Uno specchio. Da tutta la sera."
    menu:
        "Gli occhi della saletta sono su Icaro. I miei no."
        "Rovesciare il bicchiere sul panno: carte fradice, mano nulla":
            $ icaro_partita = "copre"
            with hpunch
            "Il vino si allarga sul panno, rosso scuro. Mazzo da buttare. Mano nulla, per regola di saletta."
            "Milone protesta. Teucro alza le spalle: senza mano, niente prova."
            show icaro neutro with qdiss
            icaro "Peccato. Avevo un punto eccellente."
            "Fuori, con l'atto del magazzino di nuovo in tasca, mi guarda storto."
            icaro "Mi hai salvato la faccia e affogato il piatto più grosso dell'anno. Bilancio: pari."
            icaro "Non aspettarti gratitudine. Non era in attivo."
            "La mattina dopo, sotto la mia porta, trovo un bicchiere nuovo. Cristallo di Glostok. Dal suo magazzino, cartellino ancora attaccato."
        "«L'anello, Arconte. Il castone. Fa da specchio dall'inizio della sera.»":
            $ icaro_partita = "smaschera"
            $ icaro_affinity += 1
            "Silenzio. Teucro copre l'anello con l'altra mano. Troppo tardi: l'hanno visto tutti."
            "Milone non parla più di maniche. A Zefiro non si accusa un baro, quando il tuo è appena stato scoperto."
            show icaro sorpreso with qdiss
            "Icaro scopre le carte. Vince. Raccoglie il piatto una moneta alla volta."
            show icaro furbo with qdiss
            icaro "Un castone piatto. Tre ore, e io l'avevo preso per cattivo gusto."
            icaro "Non hai detto una parola su di me. Hai indicato lui. È la differenza tra un testimone e un socio."
            "Fuori, mi infila in tasca una moneta del piatto. Una sola. «Ricordo. Non ricompensa.»"
        "Restare in silenzio. È la sua partita":
            $ icaro_partita = "silenzio"
            $ icaro_affinity += 1
            "Non mi muovo. Non respiro."
            show icaro neutro with qdiss
            "Icaro si sfila la giacca e rovescia le maniche sul panno. Cenere, tabacco. Niente."
            "La carta non c'è più. Dove sia finita, non lo saprò mai."
            icaro "Contate pure. Poi, Milone, mi chiederai scusa davanti a tuo zio."
            "Milone chiede scusa. Icaro vince. Ma il piatto lo raccoglie con una mano sola: l'altra trema, appena."
            icaro "Sei rimast[fin] immobile. Neanche un'occhiata alla manica. ...Lo metto a registro."
            "Sulla strada del ritorno mi cammina accanto più vicino del solito. Mezzo passo. Non di più."
    return


## Luna VI — I conti di fine semestre ########################################

label icaro_luna6:
    scene bg vicoli_zefiro with fade
    "Nove giorni alla fine del semestre. La fumeria ha riaperto, e al tavolo grande c'è un posto vuoto che nessuno osa occupare."
    show icaro neutro with dissolve
    "Icaro non gioca. Siede al tavolo piccolo con tre registri aperti, la pipa spenta, e una pila di carte che non sono da gioco."
    icaro "Chiusura di semestre. Ogni Luna faccio i conti. Ogni sei, li faccio davvero."
    pc "Posso aiutare?"
    icaro "Leggi i numeri ad alta voce. Li sento meglio di come li vedo. Non chiedermi perché."
    "Leggo. Lui ascolta a occhi chiusi, la penna sospesa. Ogni tanto corregge una cifra che non ha neanche guardato."
    if icaro_partita == "smaschera":
        icaro "Voce Teucro: chiusa. Il Ramo di Vittoria mi ha mandato una cassa di vino, «scusa non ufficiale». La rivendo."
    elif icaro_partita == "copre":
        icaro "Voce Teucro: aperta. Mi deve una rivincita, io gli devo un panno. Finché nessuno paga, siamo in equilibrio."
    elif icaro_partita == "silenzio":
        icaro "Voce Milone: chiusa con le scuse. Le scuse non si rivendono. Le ho messe a bilancio lo stesso. Le prime della mia vita."
    "Poi apre il registro di casa. Il cuoio è più vecchio, consumato agli angoli dalle mani di tre fratelli."
    icaro "Druso: quarantaquattro Scudi. Più una porta della mensa, sfondata con la testa. Gli addebito i cardini."
    icaro "Caino: niente. Caino non mi deve mai niente. È la voce che mi preoccupa di più."
    show icaro furbo with qdiss
    icaro "Lenora: una lettera senza risposta. Anzi, con una risposta di una parola. Per questa famiglia, è un record."
    "Ride, appena. Un suono breve, quasi una tosse. Se ne accorge anche lui, e smette subito."
    menu:
        "Resta una colonna vuota, in fondo alla pagina. Icaro la tiene coperta col palmo."
        "Chiedergli cosa va scritto lì":
            show icaro irritato with qdiss
            icaro "Domanda prematura. La colonna si chiude a fine semestre, non prima. Gli interessi maturano fino all'ultimo giorno."
            "Ma non toglie la mano. La preme un po' di più, come su una carta che il vento potrebbe girare."
        "Leggere il totale del semestre, come se niente fosse":
            pc "Totale: un magazzino, una lampada di Lumina, quarantaquattro Scudi di Druso."
            show icaro sereno with qdiss
            icaro "Hai dimenticato una voce."
            pc "Quale?"
            icaro "Appunto. Non si dimentica per caso. Bene così."
        "Accendergli la pipa, senza chiedere":
            "Batto l'acciarino. Lui si sporge, la pipa tra i denti, e la fiamma ci illumina tutti e due per un istante."
            show icaro sorpreso with qdiss
            icaro "...nessuno mi accende la pipa. Lo faccio da solo da quando avevo dodici anni."
            icaro "Annotato. Non so ancora in che colonna."
    if player_gender == "f":
        show icaro imbarazzato with dissolve
        icaro "Il ventuno chiudo tutto. Il tavolo grande, quella notte, è riservato. Due posti."
        "Non lo dice come un invito. Lo dice come una prenotazione già pagata. Da Icaro è peggio: è una promessa."
    else:
        show icaro sereno with dissolve
        icaro "Il ventuno chiudo tutto. Vieni. Porta la chiave del magazzino: voglio vedere se ce l'hai ancora."
        pc "Ce l'ho. Non l'ho mai tolta di tasca."
        icaro "Lo so. Ho controllato. Due volte."
    return


## Climax e finali ###########################################################

label icaro_climax:
    scene bg vicoli_zefiro with fade
    show icaro neutro with dissolve
    "Fine semestre. La saletta è vuota: il tavolo grande, stanotte, è solo nostro. Icaro mescola le carte come altri pregano."
    "Fuori, Zefiro festeggia la chiusura delle Lune. Dentro, solo il fruscio del mazzo e l'odore di resina fredda."
    "Accanto al mazzo, il registro del tavolo piccolo. Chiuso, legato con un nastro."
    if icaro_partita == "smaschera":
        icaro "Teucro ha lasciato Zefiro. Il Ramo di Vittoria l'ha richiamato a casa, «per motivi di salute». La salute di un baro scoperto è fragile."
    elif icaro_partita == "copre":
        icaro "Teucro mi deve ancora una rivincita. E il panno l'ho fatto lavare. Il conto della lavandaia è a tuo nome."
    elif icaro_partita == "silenzio":
        icaro "Milone mi saluta per strada, adesso. Con rispetto. Effetto collaterale del tuo silenzio: non l'avevo messo a bilancio."
    icaro "Ho condonato a Druso i cardini della mensa. Non dirglielo: deve credere che io sia ancora furioso. Lo tiene educato."
    show icaro sereno with qdiss
    "Accende la pipa. Il fumo sale dritto, senza fretta."
    icaro "Ho chiuso i conti del semestre. Tutti. Tranne una voce."
    icaro "Tu. Non so in che colonna metterti. E io so sempre in che colonna mettere tutto."
    "Smette di mescolare. Il mazzo resta fermo tra le sue dita: non gliel'ho mai visto fare."
    show icaro neutro with qdiss
    icaro "Domanda secca. Dimmi una cosa che hai visto di me. Una sola. Che non abbia visto nessun altro."
    menu:
        "Il mazzo è fermo. Aspetta me, per ripartire."
        "«Ti fermi mezzo respiro prima di dire la verità. Mai prima di una bugia.»" (peso=True):
            $ icaro_climax_scelta = "dettaglio"
            $ icaro_affinity += 1
            show icaro sorpreso with qdiss
            icaro "..."
            "Si guarda le mani, come se fossero di un altro."
            icaro "Mezzo respiro. Nessuno ha mai misurato mezzo respiro. Nemmeno io."
            "Ride, piano. È la seconda volta in un semestre. Stavolta non smette subito."
        "Prendergli la pipa, tirare una boccata, rendergliela. Senza una parola" (peso=True):
            $ icaro_climax_scelta = "silenzio"
            "Mi guarda fare. Non protesta, non conta, non si scosta."
            show icaro sereno with qdiss
            icaro "Il silenzio l'ho già comprato, settimane fa. Stanotte volevo il resto."
            icaro "Ma lo prendo lo stesso. Il silenzio non si svaluta."
            "Si riprende la pipa. Il cannello è ancora caldo. Non lo pulisce."
        "«Che bari anche quando giochi da solo.»" (peso=True):
            $ icaro_climax_scelta = "accusa"
            $ icaro_affinity -= 1
            with vpunch
            show icaro irritato with qdiss
            icaro "Io non baro. Io ottimizzo."
            icaro "E per la cronaca: era la risposta che avrebbe dato chiunque. Ti avevo chiesto una cosa che nessuno ha visto."
            "Ricomincia a mescolare. Più veloce di prima."
            icaro "«Ottimizzo.» Lo farò incidere sulla lapide. In piccolo, così nessuno lo contesta."
    "Il mazzo riparte. Icaro fa la sua offerta, come sempre, per ultimo."
    # Routing (rl.finale_icaro): se player_gender == "m" sempre icaro_bro_end;
    # altrimenti icaro_good -> icaro_neutral -> icaro_bad.
    $ cal_finale = rl.finale_icaro(player_gender, icaro_affinity,
                                   flag_icaro_coperto, congelate)
    jump expression cal_finale

label icaro_good:
    show icaro furbo with qdiss
    icaro "Ultima mano del semestre. Posta: tutto il mio inventario contro la tua parola. Carte coperte."
    "Giochiamo. E a fine mano, quando scopro le carte, capisco: ha barato. Al contrario. Per perdere."
    icaro "Hai vinto tutto. Che disastro contabile. Per fortuna il vincitore è... mio. Quindi il patrimonio non si muove."
    pc "Hai perso apposta, Icaro."
    icaro "Dimostralo. Nessuno ha mai dimostrato niente, a questo tavolo."
    pc "Ho visto la carta scivolarti nel polsino. All'incontrario: dentro, non fuori."
    show icaro sorpreso with qdiss
    icaro "...hai visto."
    "Non nega. In un semestre, è la prima volta che Icaro non nega."
    show icaro imbarazzato with dissolve
    "Poi slega il nastro del registro. Lo apre alla pagina della riga coperta. Stavolta la mano resta ferma."
    "Una riga sola, nella sua grafia stretta da notaio. «Voce unica. Non ammortizzabile. Non cedibile.»"
    if icaro_climax_scelta == "dettaglio":
        icaro "Prima di scriverla mi sono fermato mezzo respiro. Ormai sai cosa vuol dire."
    else:
        icaro "L'ho scritta in silenzio. Mi sembrava la lingua giusta, con te."
    pc "E il prezzo?"
    icaro "Fuori listino. Le cose che non si vendono non hanno un prezzo. Hanno un proprietario."
    "Non mi tocca. Sposta il mazzo di un dito verso di me, sul panno. Da Icaro, è una mano tesa."
    scene bg cala_notte with fade
    show icaro sereno with dissolve
    "Il tetto sopra la Consorteria. Due stuoie, una pipa sola, e la regola cambiata: si fuma a turno."
    "Mi passa la pipa. Le nostre dita si toccano, stavolta. Non la ritira."
    icaro "Annotazione d'inventario. Contatto: accettato. Una persona sola. Non allargarti."
    "Non lo dimostrerò mai. Ma la lampada più brutta del magazzino, da quella notte, sta sul mio davanzale. Non è in vendita."
    scene bg nero with fade
    $ sblocca_finale("icaro_good")
    with lampo_oro
    centered "{cps=20}{size=+10}UNTOUCHABLE{/size}\n\nL'eccezione che conferma ogni regola.\nE non è in vendita.{/cps}"
    return

label icaro_neutral:
    show icaro furbo with qdiss
    icaro "Proposta: socio al dieci per cento. Tu guardi le mani, io taglio il mazzo. Niente sentimenti: rendono poco e costano troppo."
    if icaro_climax_scelta == "accusa":
        icaro "E prima che tu lo dica: no, il contratto non è truccato. Leggilo due volte, visto che ti piace accusare."
    elif icaro_climax_scelta == "dettaglio":
        icaro "Hai l'occhio giusto. Mezzo respiro, l'hai detto tu. È per questo che ti pago: per guardare."
    else:
        icaro "Sai tacere. In un socio vale più del capitale."
    icaro "Contratto in triplice copia. Una a te, una a me, una a Caino. Lui le copie non le perde mai."
    "Il registro resta legato. Non lo apre, e non lo sposta dal suo lato del tavolo."
    "Accetto. È il massimo che il suo bilancio concede, e il dieci per cento di Icaro vale più del cento per cento di molti."
    show icaro neutro with qdiss
    "Da allora, ogni fine Luna, una busta sotto la mia porta. Cifra esatta al centesimo, mai un biglietto."
    "Una volta, dentro, c'è una moneta in più. La riporto. La riprende senza commentare."
    "Qualche volta, a fine mano, mi guarda come si guarda una carta scartata troppo presto. Poi rimescola."
    "Al tavolo grande ho un posto. Il tavolo piccolo, quello dove conta, resta suo."
    scene bg nero with fade
    $ sblocca_finale("icaro_neutral")
    centered "{cps=20}{size=+10}IL SOCIO{/size}\n\nDieci per cento.\nPagato puntualmente, ogni Luna.{/cps}"
    return

label icaro_bad:
    show icaro irritato with qdiss
    icaro "Il posto al tavolo era in prova. La prova è scaduta. Niente di personale: è che il personale, con te, non ha mai aperto."
    if icaro_climax_scelta == "accusa":
        icaro "E chi mi dà del baro al mio tavolo non ci si siede due volte. È la regola più vecchia della casa."
    "Spinge il registro dal suo lato. Il nastro resta chiuso: la riga che c'era sopra, se c'era, non la leggerò mai."
    icaro "Domani cambio le serrature della fumeria. Non è contro di te. È contro chiunque."
    "Mi alzo. Non protesto: coi bari inguaribili non si vince, e con Icaro non si pareggia nemmeno."
    show icaro neutro with qdiss
    "Sulla soglia mi volto. Lui sta già mescolando per la prossima mano. Contro nessuno."
    "Un'occhiata rapida al posto vuoto. Poi segna qualcosa a margine del registro. Una voce chiusa, credo. In perdita."
    "In strada mi frugo le tasche, per abitudine. Manca una moneta. Una sola. L'ultimo interesse."
    scene bg nero with fade
    $ sblocca_finale("icaro_bad")
    centered "{cps=20}{size=+10}FUORI LISTINO{/size}\n\nIcaro non perde mai.\nNemmeno quando vinci.{/cps}"
    return

label icaro_bro_end:
    if rl.finale_bro(icaro_affinity, icaro_impegnato) == "icaro_bro_listino":
        icaro "Il semestre chiude in attivo: un fratello acquisito, costo zero, rendita perpetua. Il miglior affare che io non abbia mai pianificato."
        if icaro_climax_scelta == "dettaglio":
            icaro "Mezzo respiro. Nemmeno Caino se n'è accorto, e Caino conta i respiri della gente per mestiere."
        elif icaro_climax_scelta == "silenzio":
            icaro "E la pipa me l'hai resa intera. In questa famiglia nessuno restituisce quello che prende. Nessuno."
        else:
            icaro "Mi hai dato del baro. Lo tollero da un fratello solo, e una volta sola. La tua l'hai spesa."
        show icaro sereno with dissolve
        "Slega il nastro del registro e lo gira verso di me. Una pagina, una riga."
        "«Fratello. Nessuna contropartita.» Sotto, la sua firma. E lo spazio per la mia."
        "Firmo. Lui soffia sull'inchiostro, chiude il registro e torna a mescolare, come se niente fosse."
        icaro "Druso pretenderà di firmare anche lui. Gli dirò che la pagina è finita."
        icaro "Caino lo saprà entro l'alba. Lascialo sapere. Per una volta, è un credito che non può riscuotere."
        icaro "Domani sera, stesso tavolo. Tu guardi le mani degli altri. Le mie no: sono di famiglia."
        "La chiave del magazzino resta nella mia tasca. Il gradino accanto al suo resta mio. Nel Nord, è più di quanto ottenga chiunque."
        scene bg nero with fade
        $ sblocca_finale("icaro_bro_listino")
        centered "{cps=20}{size=+10}LISTINO CHIUSO{/size}\n\n{i}Finale Bro{/i}\n\nNon tutto ciò che è prezioso si tocca.{/cps}"
    else:
        icaro "Buon semestre, [figlio_t] di Briseide. Il tavolo grande apre a chi conta. Torna quando conti."
        if icaro_climax_scelta == "accusa":
            icaro "E la prossima volta che mi dai del baro, porta le prove. Non le troverai, ma almeno sarà sportivo."
        "Il registro resta legato. Se lo infila sotto il braccio e si alza per primo."
        "Spinge la mia sedia sotto il tavolo con la punta dello stivale. Posto libero. Rientra a listino."
        "Alla porta si ferma, la pipa tra i denti. Non si volta."
        icaro "Niente di personale. Il personale è un lusso, e io i lussi li compro solo a prezzo di saldo."
        "Esce. Sul panno ha lasciato il mazzo, tagliato perfetto. Da Icaro, vuol dire che non c'è altro da aggiungere."
        scene bg nero with fade
        $ sblocca_finale("icaro_bro_conti")
        centered "{cps=20}{size=+10}CONTI APERTI{/size}\n\nIl tavolo grande resta dov'era.\nTu no.{/cps}"
    return
