# Route Icaro — Atto 2: evento 3, interludio 3, linea Bro, Lune V-VI.

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
        icaro "...annotazione d'inventario. Due ore, zero perdite. La tua presenza non è un passivo. Ricontrollo domani, per sicurezza."
        $ icaro_affinity += 2
        "Poi torna a guardare la città. La pipa, sulla stuoia, resta dalla mia parte."
    else:
        show icaro imbarazzato with dissolve
        icaro "...annotazione d'inventario. Due ore accanto a te, e non ho controllato il borsello. Neanche una volta. Tienitelo stretto."
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
            icaro "...ventitré lettere. Stessa riga, ogni volta. Questa risposta la segno a margine, con la data."
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
        icaro "Druso direbbe che adesso siamo amici. Druso esagera del sessanta per cento. Il resto, stasera, è corretto."
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
    "Il mercante apre la cassa. Paglia, porcellana, un odore di cantina. Icaro alza una tazza contro la luce. Gira il polso di un quarto, poi di un altro."
    icaro "Crepata. Questa. E questa. Il servizio vale la metà di quello che chiedi."
    "Il mercante giura sugli dei del Nord e su sua madre. Icaro aspetta che finisca, poi offre un terzo."
    menu:
        "Il mercante guarda me. Cerca un alleato, o almeno una crepa."
        "Restare zitto, braccia conserte, e guardare l'uscita":
            $ icaro_affinity += 1
            "Non dico niente. Guardo la porta del mercato come se avessi già un altro affare lì fuori."
            "Il mercante suda. Scende di prezzo due volte, da solo, senza che nessuno glielo chieda."
            show icaro furbo with qdiss
            icaro "Due ribassi, zero parole. Ottanta Scudi risparmiati con la faccia. Non la sprecare in taverna."
        "Inventare un'offerta migliore, a un altro banco":
            pc "Il banco del vetraio ci ha offerto un servizio intero per meno. Andiamo, Icaro."
            show icaro irritato with qdiss
            "Icaro mi fulmina. Mezzo secondo. Poi annuisce, grave, come se l'avesse deciso lui."
            "Il mercante cede. Fuori dal mercato, Icaro mi ferma con due dita sul petto, e le ritira subito."
            icaro "Funziona. Ma il vetraio chiude il martedì, e oggi è martedì. Se il mercante lo sapeva, eravamo fuori. Il metodo, la prossima volta, me lo dici prima."
        "Indicare il bollo sotto un piattino: è ridipinto":
            $ icaro_affinity += 1
            "Sotto un piattino il bollo di Glostok ha i bordi troppo freschi. Lo giro verso Icaro, senza una parola."
            show icaro sorpreso with qdiss
            icaro "...ridipinto. Mezzo servizio è di Glostok, mezzo di un forno qualunque."
            show icaro furbo with qdiss
            icaro "Allora lo compriamo tutto. Al prezzo del forno qualunque. Poi lo rivendiamo come di Glostok a chi non gira i piattini."
            pc "Non è onesto."
            icaro "È commercio. Dodici Scudi spesi, quaranta di rientro. Se vuoi l'onestà, è il banco dopo: chiude in perdita da tre anni."
    "Il servizio finisce nel magazzino di Icaro, contato due volte. Lui mi mette in mano una tazza. Una sola, quella senza crepe."
    icaro "La tua parte. Un servizio scompagnato perde valore: così ho un motivo per tenerti d'occhio. Finché ce l'hai tu, il servizio è completo a metà."
    show icaro sereno with qdiss
    icaro "Non è un regalo. Gli uomini non si fanno regali. È una garanzia."
    "Me la infilo in tasca. Pesa poco. Lui apre il registro e annota: data, oggetto, «in custodia»."
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
            $ icaro_affinity += 1
            "Non mi muovo. Chi scappa ha qualcosa da nascondere. Io sono una colonna del portico."
            "La guardia guarda nella mia direzione per un tempo lunghissimo. Poi sbadiglia, e riprende a dormire in piedi."
        "Fare un fischio basso, come quello dei lanternai":
            $ icaro_affinity += 1
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
    icaro "Stanotte sei rimasto, e non hai chiesto la tua parte. Avevo messo da parte dieci Scudi per trattare. Restano in tasca mia."
    "Mi passa la pipa, accesa al riparo di un portone. Il cannello verso di me, le dita lontane."
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
        "Poi mi prende la mano. Lui, che detesta il contatto. La tiene per trecento gradini, rigida e attenta. Ogni cinquanta, stringe un poco: conta anche quelli."
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
    "Icaro lo osserva tra una boccata e l'altra. Muove le labbra senza suono: conta. Al terzo giro ricomincia da capo."
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
            $ muovi("icaro", "trema")
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
        icaro "Voce Milone: chiusa con le scuse. Le scuse non si rivendono. Le ho messe a bilancio lo stesso. Cinque parole, contate."
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
            $ muovi("icaro", "avanza")
            "Batto l'acciarino. Lui si sporge, la pipa tra i denti, e la fiamma ci illumina tutti e due per un istante."
            show icaro sorpreso with qdiss
            icaro "...la accendo da solo da quando avevo dodici anni. Acciarino mio, pietra mia, ogni sera."
            icaro "Annotato. Non so ancora in che colonna."
    if player_gender == "f":
        show icaro imbarazzato with dissolve
        icaro "Il ventuno chiudo tutto. Il tavolo grande, quella notte, è riservato. Due posti."
        "Non lo dice come un invito. Mentre parla, scrive due iniziali a margine del registro. Una è la mia."
    else:
        show icaro sereno with dissolve
        icaro "Il ventuno chiudo tutto. Vieni. Porta la chiave del magazzino: voglio vedere se ce l'hai ancora."
        pc "Ce l'ho. Non l'ho mai tolta di tasca."
        icaro "Lo so. Ho controllato. Due volte."
    return


## Deviazione (Luna III+) — La febbre #########################################

label icaro_febbre:
    scene bg vicoli_zefiro with fade
    "La fumeria è chiusa a metà settimana. Sulla porta, un biglietto nella grafia di Icaro: «Inventario». Sotto, più piccolo: «Non bussare.»"
    "Busso. Nessuno risponde. La porta però è aperta, e Icaro non lascia mai una porta aperta."
    show icaro neutro with dissolve
    "È al tavolo piccolo, avvolto in due mantelli, col registro aperto e la pipa spenta. Ha la fronte lucida e le guance di uno che ha corso. Non ha corso."
    icaro "Ho scritto «non bussare». In quale lingua del Nord quella frase vuol dire «bussa»?"
    pc "Hai la febbre."
    icaro "Ho un inventario. La febbre è un dettaglio contabile."
    $ muovi("icaro", "trema")
    "Gli trema la penna. Rifà lo stesso numero tre volte. Al terzo lo cancella con rabbia e il foglio si strappa."
    if player_gender == "m":
        icaro "Socio. Se resti, resti zitto e conti tu. Se te ne vai, chiudi la porta. Le altre opzioni non sono a listino."
    else:
        icaro "Se resti, resti zitta e conti tu. Se te ne vai, chiudi la porta. Le altre opzioni non sono a listino."
    menu:
        "Il registro è lì. La sua mano no, non del tutto."
        "Prendere la penna e continuare l'inventario al posto suo":
            $ icaro_febbre_esito = "conta"
            $ icaro_affinity += 1
            "Gli sfilo la penna. Non protesta, il che dice più della febbre."
            "Conto. Lampade, stoffe, un servizio da tè. Lui corregge a voce bassa, a occhi chiusi, ogni volta che sbaglio. Sbaglio poco."
            show icaro sereno with qdiss
            icaro "Sette tazze, non otto. L'ottava l'ho data a Druso. Non segnarla: la considero un investimento a perdere."
            "A metà pagina si addormenta sulla sedia. Finisco l'inventario. Gli lascio il registro chiuso sotto la mano."
        "Andare a chiamare Corrado: lui sa di erbe":
            $ icaro_febbre_esito = "aiuto"
            "Torno con Corrado e una borsa di erbe che puzza di stalla. Icaro guarda la borsa, poi Corrado, poi me. In quest'ordine."
            show icaro irritato with qdiss
            icaro "Ho detto non bussare. Non ho detto «porta un erborista». Questa è inflazione."
            "Beve l'infuso lo stesso. Fa una smorfia a ogni sorso, e ogni sorso lo segna sul registro come debito verso Corrado."
        "Fare come chiede: andarmene e chiudere la porta":
            $ icaro_febbre_esito = "via"
            "Chiudo la porta piano. Dall'altra parte, la penna riprende a grattare. Poi si ferma. Poi niente."
            "La mattina dopo la fumeria è aperta. Icaro è al suo posto, pallido e perfetto, e non nomina la sera prima."
            icaro "Hai rispettato il biglietto. Rarissimo. Te lo segno."
            "Non dice in quale colonna."
    return
