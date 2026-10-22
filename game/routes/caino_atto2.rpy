# Route Caino — Atto 2: capitoli 4-6.

################################################################################
## CAPITOLO 4 — Il tradimento
################################################################################

label caino_cap4:

    scene bg consiglio with fade

    "La Rocca degli Arconti. Caino mi ha voluto con sé «per i registri». I registri, scopro, sono un'arma."

    show caino neutro with dissolve

    "Davanti a noi siede un uomo con lo stemma del Ceppo di Cardia: Aulo, Filius Maior, alleato di Caino da sei anni. Lo so perché me l'ha detto Caino stesso: «Aulo è la mia mano sinistra nel Consiglio»."

    $ muovi("caino", "trema")
    "Oggi la mano sinistra trema."

    caino "Aulo. I registri della tua Contrada hanno tre buchi. Tre. Li ho trovati io, il che è un bene. Se li avesse trovati l'Arconte della Verità, saresti già nelle Segrete Silenti."

    "Aulo balbetta. Spiega. Erano prestiti, dice. Li avrebbe ricoperti, dice. Caino ascolta col mento sulla mano, paziente come un gatto sazio."

    caino "Ti credo. Davvero. Ed è per questo che mi fa male quello che devo fare."

    "E lo fa: consegna i registri al Consiglio quella sera stessa. Aulo perde il titolo, il seggio e il nome. La carica di Sovrintendente delle Contrade — quella che Aulo custodiva — passa alla Proprietà. A Caino."

    "Sei anni di alleanza, spesi in una sera, per una carica."

    scene bg studio_glauco with fade

    show caino neutro with dissolve

    "Nello studio, dopo, Caino versa due idromele come se niente fosse."

    caino "Dillo. Ce l'hai scritto in faccia, e le facce non sanno tenere i registri."

    menu:
        "Cosa dico all'uomo che ha appena venduto la sua mano sinistra?"

        "«Era tuo alleato. Sei anni. E l'hai bruciato per una carica.»":
            $ caino_fiducia += 2

            pc "Era tuo alleato. Sei anni. E l'hai bruciato per una carica. Non per giustizia: per la carica. Se la giustizia c'entrava, i buchi li avresti portati al Consiglio sei mesi fa, quando li hai trovati davvero."

            show caino sorpreso with qdiss

            "Il corno di idromele si ferma a mezz'aria."

            caino "...come sai quando li ho trovati?"

            pc "Perché i registri li tengo io, adesso. E le date di consultazione restano. I dettagli, Arconte. I dettagli possiedono le persone."

            show caino neutro with qdiss

            "Caino posa il corno. E per la prima volta da quando lo conosco, impiega più di un secondo a scegliere le parole."

            caino "Chiunque altro, con quella frase, sarebbe già rotolato giù dalle scale della Rocca. Tu invece resti a bere. Dovresti chiederti perché."

            pc "Me lo sto chiedendo."

            caino "Anche io."

        "«Hai fatto bene. Aulo era un peso.»":
            $ caino_fiducia -= 2

            pc "Hai fatto bene. Aulo era un peso. La Famiglia non ha posto per i deboli."

            show caino sarcastico with qdiss

            caino "Che discorso ammirevole. Sembro io, senza il talento."

            "Mi guarda come si guarda uno specchio sporco: con fastidio, e con il sospetto che lo sporco non sia dello specchio."

            caino "Il problema di chi mi dà sempre ragione, Figlio di Briseide, è che non mi serve: ho già me stesso per quello."

        "Tacere e bere":
            "Bevo. Il silenzio, con Caino, è l'unica frase che non può rivoltarti contro."

            show caino neutro with qdiss

            caino "Il silenzio. Di nuovo. Sai che è la cosa più onesta che ti ho visto fare?"

    return

################################################################################
## CAPITOLO 5 — La breccia
################################################################################

label caino_cap5:

    scene bg esterno_neve with fade

    "Mi convoca di notte, sugli spalti della Rocca. Niente registri stavolta: solo la neve, le lanterne di Zefiro in basso, e un uomo che per una volta non sta al centro di nessuna sala."

    show caino neutro with dissolve

    caino "Lo sai cosa si dice di te, nei corridoi? Che il Figlio di Briseide ha stregato l'Arconte della Proprietà. Che ceno con te più spesso che con i miei scrivani. Che ti ho fatto ballare."

    pc "E ti disturba?"

    caino "Mi disturba che sia vero."

    "Si appoggia al merlo. Sotto di noi, Zefiro brilla come un registro pieno di voci."

    "Ha la neve tra i capelli e non la scuote. L'Arconte che non lascia nulla al caso, stanotte, lascia cadere la neve."

    caino "Da bambino salivo qui a contare le lanterne. Ogni sera. Se il numero cambiava, volevo sapere perché."

    pc "E lo scoprivi?"

    caino "Sempre. Una morte, un debito, una fuga. Ogni lanterna spenta era una voce chiusa. Ho imparato a leggere la città prima delle lettere."

    caino "Io non ci credo, [player_name]. Ai sentimenti. Sono la moneta più falsa del Nord: tutti la spendono, nessuno la conia. Mia madre regna da prima che io nascessi, e non l'ho mai vista amare niente che non le servisse."

    caino "Quindi spiegami tu. Cosa vuoi da me? Tutti vogliono qualcosa. La carica, il favore, il seggio, la spada. Tu quale vuoi? Dimmelo e risparmiamo entrambi un inverno di finzioni."

    menu:
        "La domanda è una lama ben tenuta. E la risposta sbagliata taglia."

        "«Niente che puoi firmare. È questo che ti spaventa.»":
            $ caino_fiducia += 2

            pc "Niente che puoi firmare, Caino. Nessuna carica, nessun favore, nessun seggio. È questo che ti spaventa: non hai un registro dove scrivermi."

            show caino sorpreso with qdiss

            "Tace. L'uomo che vince ogni scontro verbale di Rocca Tempesta tace, e la neve gli si posa sulle spalle senza che se ne accorga."

            show caino neutro with qdiss

            caino "...tutti hanno un prezzo. Tutti. Se tu non ce l'hai, sei la cosa più pericolosa che sia mai entrata nella mia Proprietà."

            pc "O la prima che non ne fa parte."

        "«Voglio il tuo appoggio in Consiglio, un giorno. Almeno sono onesto.»":
            pc "Voglio il tuo appoggio in Consiglio, un giorno. Almeno sono onesto."

            show caino freddo with qdiss

            caino "Onesto. Sì. E deludente, il che è peggio."

            "Annuisce piano, come chi ritrova una moneta conosciuta. Comoda, la moneta conosciuta. Ma non vale niente di nuovo."

        "«Non lo so ancora. E non te lo dirò prima di saperlo.»":
            $ caino_fiducia += 1

            pc "Non lo so ancora. E non te lo dirò prima di saperlo per certo. Ti fidi delle risposte precise, ed è il tuo punto debole: le risposte precise si possono comprare."

            show caino sarcastico with qdiss

            caino "Dare del punto debole all'Arconte della Proprietà. Sugli spalti. Di notte. Senza testimoni. O sei coraggios[fin] o sei scem[fin]."

            pc "I dettagli possiedono le persone. Scegli tu quale dettaglio sono."

    "Il vento gira. Caino guarda Zefiro ancora un poco, poi — con la voce più piatta che ha —"

    show caino sarcastico with qdiss

    caino "Sai, è buffo. Credo di essermi innamorato di te. Perdutamente. Come mi innamoro delle decime pagate in anticipo e dei registri senza buchi. Un sentimento travolgente, da ballata di Mercuzio. Dovremmo sposarci in Cantalba, che dici?"

    menu:
        "Il tono è sbagliato. Troppo liscio. È la voce del Ballo delle Candele Spente, la voce del «preferito senza invidia»."

        "«Anch'io ti amo, Caino.»":
            $ caino_fiducia -= 2
            $ caino_trappole += 1

            pc "Anch'io ti amo, Caino."

            show caino freddo with qdiss

            "Il viso gli si chiude come un registro a fine mese."

            caino "...già. Certo. È tardi, Figlio di Briseide. La Rocca si alza presto."

            "E capisco, troppo tardi, che era l'ultima prova: voleva vedere se abboccavo alla moneta falsa. Ho abboccato."

        "«Questa era la peggiore delle tue trappole. Riprova quando fai sul serio.»":
            $ caino_fiducia += 2

            pc "Questa era la peggiore delle tue trappole, Caino. La voce era quella del Ballo delle Candele Spente: troppo liscia. Riprova quando fai sul serio. Se mai saprai farlo."

            show caino sorpreso with qdiss

            "Lunga pausa. La neve cade. E poi Caino ride — non la risata da sala piena: una corta, vera, quasi sorpresa di esistere."

            show caino neutro with qdiss

            caino "«Se mai saprai farlo». Ecco il problema, [player_name]. Comincio a volerlo imparare. E non c'è registro, carica o spada che mi abbia mai spaventato quanto questa frase."

    return

################################################################################
## CAPITOLO 6 — La prova
################################################################################

label caino_cap6:

    scene bg studio_glauco with fade

    show caino neutro with dissolve

    "Lo studio, sette giorni dopo. Sul tavolo, due pergamene già scritte. Caino le gira verso di me come un banco di mercato."

    caino "Scegli. A sinistra: la nomina a Primo Scrivano della Proprietà. Mio braccio destro ufficiale. Carriera, Scudi, un seggio minore tra dieci anni. Firmata, manca il tuo nome."

    caino "A destra: niente. Nessuna carica, nessun titolo. Solo me. Quello che resta di me quando togli l'Arconte, e ti avverto: nessuno l'ha mai visto, nemmeno io. Potrebbe non esserci nulla."

    pc "Perché me lo chiedi adesso?"

    caino "Perché mia madre ha cominciato a farmi domande su di te. E quando Lenora fa domande, le risposte le sceglie lei, se non gliele dai prima. Devo sapere cosa sei per me, [player_name]. Stanotte."

    show druso neutro at left with dissolve

    "La porta si apre senza bussare. Druso. Niente sorriso, stavolta."

    druso "Fratello. Il Consiglio. Qualcuno ha parlato a madre dei registri di Aulo. Dicono che li hai tenuti sei mesi per tempistica politica. Chiedono una testa."

    "Caino non risponde. Druso si volta verso di me, e per una volta il gigante parla piano."

    menu:
        druso "Tu. Le date sui registri sono tue. Se resti, finisci nel calderone con lui. Posso farti uscire dalla postierla prima che la Rocca chiuda. Decidi adesso."

        "«Resto. I registri li difendo io.»":
            $ caino_fiducia += 1

            pc "Resto. I registri li ho tenuti io: li difendo io."

            druso "Spina dorsale. L'avevo detto."

        "«Portami alla postierla. Ma torno all'alba.»":
            $ caino_druso += 1

            pc "Portami alla postierla. Ma torno all'alba: non scappo, prendo fiato."

            druso "Furb[fin] e viv[fin]. È così che mi piacciono gli alleati. Vieni."

            "Alla postierla, prima di lasciarmi andare, Druso mi tiene la spalla un istante più del necessario."

            druso "Qualunque cosa succeda domani... tu un fratello ce l'hai già, in questa Rocca. Ricordatelo."

    hide druso with dissolve

    "Caino non si muove. Ma io ho tenuto i suoi registri, e so leggere anche lui, ormai: sotto il tavolo, la mano si è chiusa a pugno."

    caino "Le pergamene non scappano. Ma prima — un'ultima domanda. La più importante. Se sbagli questa, tutto il resto non conta."

    show caino neutro with qdiss

    caino "In tutti questi mesi, io ho detto di odiare una cosa sola. Una. Qual è?"

    menu:
        "Una cosa sola. Ripasso ogni sala, ogni corno, ogni sorriso."

        "«Il vino di Glostok.»":
            $ caino_fiducia += 2
            $ caino_memoria += 1

            pc "Il vino di Glostok. «Lo bevono i cambiavalute e i pentiti.» Prima frase che mi hai detto dopo avermi dato del mobile inutile."

            show caino sorpreso with qdiss

            caino "...non ti ho dato del mobile inutile."

            pc "«Educato, misurato, inutile». Adunanza. Verbale disponibile su richiesta."

            show caino neutro with qdiss

            caino "Tre cose, allora, in vita mia: l'idromele, i dettagli, e te. È la lista completa delle cose che non tradirò."

        "«I traditori.»":
            $ caino_fiducia -= 1

            pc "I traditori."

            show caino sarcastico with qdiss

            caino "Io? Odiare i traditori? Io SONO un traditore, [player_name]. È il mio mestiere. Risposta da ballata, e le ballate, nei registri, valgono zero."

        "«Tua madre.»":
            $ caino_fiducia -= 1

            pc "Tua madre."

            show caino neutro with qdiss

            caino "No. Mia madre la temo, la ammiro e la combatto. L'odio è per le cose piccole. Hai confuso la taglia del sentimento."

    "Caino si alza. Prende entrambe le pergamene, le piega, le infila nel farsetto."

    caino "Il Consiglio mi aspetta. La tua risposta — quella vera, sinistra o destra — me la darai dopo. Se dopo esisto ancora."

    "Sulla soglia si ferma. Non si volta."

    caino "Se domani qualcuno ti chiede di me, di' la verità. È l'unica moneta che non riescono a falsificare. Nemmeno io."

    "La porta si chiude. Resto sol[fin] con il calamaio, il fuoco e due solchi sul tavolo, dove prima c'erano le pergamene."

    return
