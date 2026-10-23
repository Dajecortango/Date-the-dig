# Route Aede — Atto 1: prologo e capitoli 1-3.

################################################################################
## PROLOGO — Lo Svelo
################################################################################

label prologo:

    scene bg nero with fade

    "Il Nord non ti chiede chi eri. Te lo strappa di dosso, come il vento strappa il fiato sulla Via del Settentrione."

    "Tre settimane fa ho pronunciato il giuramento. Il mio nome di prima è morto in quella sala, davanti all'Autarca e ai miei nuovi fratelli."

    "Ora mi chiamo [player_name]. Primo Nome, dato da Briseide Ippodamia in persona. [figlio_t] del suo Ceppo, la madre degli orfani."

    scene bg sala_svelo with dissolve

    "Rocca Tempesta, la notte dello Svelo. La festa in maschera dove il ceto non conta: per una notte il Figlio appena adottato può urtare il gomito di un Autarca e riderci sopra."

    "Briseide mi ha spedito qui con un ordine solo: «Guarda, ascolta, non farti notare»."

    "Due comandi su tre li sto rispettando."

    "Mi infilo in un corridoio laterale per sfuggire alla calca. Lanterne basse, arazzi col leone dorato, musica lontana."

    "Un errore."

    if ngp_attivo():
        "Uno che ho la strana sensazione di aver già fatto. Il corridoio, le lanterne basse, perfino l'arazzo: tutto al suo posto, come una pagina già letta."

    show aede furia with vpunch

    "Una mano mi aggancia la spalla, il mondo ruota, la schiena sbatte contro l'arazzo. Freddo sotto il mento: una lama."

    aede "Non un fiato. Il messaggio lo consegno io, e tu lo ricevi: così muore chi vende i segreti del Ceppo di Glauco."

    pc "...credo che tu abbia sbagliato persona."

    "La maschera di lei è un intaglio di volpe. Gli occhi dietro, grigioverdi, si stringono."

    aede "Il sigillo. Mostrami il polso."

    "Le mostro il polso. Nessun sigillo. Solo il nodo di corda che Briseide fa portare ai suoi Figli nel primo anno."

    show aede sorpresa with qdiss

    "La lama si stacca. Lei fa mezzo passo indietro, e per un istante — un istante solo — la volpe vacilla."

    aede "[Un_t] novellin[fin] del Ceppo di Briseide. Nel corridoio sbagliato, nella notte sbagliata."

    pc "E tu hai quasi aperto la gola [al_t] novellin[fin] sbagliat[fin]. Siamo pari?"

    show aede irritata with qdiss

    aede "Non siamo niente. Tu non hai visto niente."

    "Si toglie la maschera per un attimo, giusto il tempo di asciugarsi la fronte. Capelli rosso fiamma, raccolti male. La riconosco: Aede, la figlia di Glauco Severo."

    "Il piccolo gioiello dell'Autarca. Quella di cui i miei fratelli di Ceppo parlano solo a voce bassa."

    "E il suo bersaglio sbagliato, stanotte, ero io."

    menu:
        aede "Allora? Cosa devo fare di te, novellin[fin]?"

        "«Il tuo segreto muore con me. Hai la mia parola.»":
            $ flag_segreto_svelo = True
            $ aede_affinity += 2

            pc "Non lo dico a nessuno. Neanche a Briseide."

            show aede neutra with qdiss

            "Mi studia a lungo. Poi rinfodera la lama, di scatto, come se la decisione la irritasse."

            aede "Parola di novellin[fin]. Bah. Per stanotte basta."

        "«Sbagli bersaglio spesso, o sono speciale?»":
            $ aede_affinity += 1

            pc "Ti capita spesso di sbagliare gola, o sono un caso speciale?"

            show aede irritata with qdiss

            aede "Continua a parlare e il bersaglio diventa giusto."

            "Ma l'angolo della bocca le si piega, appena. Se ne accorge e lo raddrizza."

        "«Glauco Severo sarà curioso di saperlo.»":
            $ aede_affinity -= 2

            pc "Glauco Severo sarà curioso di saperlo."

            show aede furia

            "La lama torna dov'era. Più vicina."

            aede "Mio padre sa già tutto quello che deve sapere. Tu invece impara questo: chi minaccia me, parla con lui. E nessuno parla con lui due volte."

    "Sparisce tra le maschere come se il corridoio l'avesse inghiottita."

    "Dovrei avere paura. Ce l'ho. Ma sotto la paura c'è altro: quella piega all'angolo della bocca non me la tolgo dalla testa."

    # Nuova partita+: da qui in poi il prologo si puo' saltare.
    $ persistent.prologo_visto = True

    return

################################################################################
## CAPITOLO 1 — L'incarico
################################################################################

label cap1:

    scene bg corridoio_ceppo with fade

    "Sette giorni dopo lo Svelo, Briseide mi convoca all'alba."

    show briseide neutra with dissolve

    briseide "Il Ceppo di Glauco Severo ha chiesto un paio di mani fidate per una consegna in città. Ho fatto il tuo nome."

    pc "Il Ceppo di Glauco? Madre, io—"

    briseide "Tu guarderai, ascolterai e non ti farai notare. Come allo Svelo."

    "C'è un lampo negli occhi di Briseide che non so leggere. Sa qualcosa? Con lei è impossibile capirlo."

    briseide "La scorta ti aspetta al cancello. Porta rispetto, [player_name]. Quel Ceppo non perdona."

    scene bg vicoli_zefiro with fade

    show aede neutra with dissolve

    "Al cancello, appoggiata al muro con l'aria di chi aspetta da un'ora apposta per fartelo pesare: lei."

    aede "[Il_t] novellin[fin]. Ovviamente."

    pc "La scorta sei tu. Ovviamente."

    aede "Io non scorto te. Io scorto questa."

    "Solleva una cassetta di legno scuro, sigillata con cera e filo d'oro. Poi me la pianta tra le braccia."

    aede "Tu la porti. Io porto te. Zefiro è piena di mani leste, e la metà le conosco per nome."

    "Camminiamo. Le Contrade scorrono: Lumina coi suoi lanternai, la Consorteria coi banchi dei cambiavalute. Aede taglia la folla senza toccare nessuno, come acqua tra i sassi."

    "A un incrocio, tre tipi col cappuccio basso ci squadrano un momento di troppo. Aede neanche li guarda."

    aede "Quelli della Malacorte. Se fossero qui per noi, non li avresti visti."

    menu:
        "La cassetta pesa. Le dita mi formicolano. E la curiosità peggio."

        "Tenere il passo in silenzio, senza chiedere nulla":
            $ aede_affinity += 2

            "Stringo i denti e tengo il suo passo. Un'ora senza una domanda, senza un lamento."

            show aede neutra with qdiss

            aede "...Briseide li sceglie meno male del previsto, i suoi Figli."

            "Non si gira a dirmelo. Lo dice alla strada davanti."

        "Chiederle cosa c'è dentro la cassetta":
            "Resisto mezz'ora. Poi la lingua vince."

            pc "Cosa stiamo trasportando, di preciso?"

            show aede irritata with qdiss

            aede "Una cosa che non è affar tuo, dentro una cassetta che non è affar tuo, verso un posto che non è affar tuo."

            pc "Chiarissimo."

        "Lamentarmi del peso":
            $ aede_affinity -= 1

            pc "Potevamo prendere un carretto. O un mulo."

            show aede irritata with qdiss

            aede "Il mulo ce l'ho già. Parla pure troppo."

    scene bg studio_glauco with fade

    "La consegna finisce in una sala che non mi aspettavo: lo studio privato di Glauco Severo, nella tenuta del Ceppo."

    show glauco neutro with dissolve

    glauco "Posa pure lì, [figlio_t] di Briseide."

    "Glauco Severo non alza la voce. Non ne ha bisogno. Ogni parola arriva già pesata, come moneta d'oro contata due volte."

    glauco "Aede. Il resoconto."

    aede "Nessun contatto. Tre osservatori della Malacorte sulla Via Lumina, nessuna mossa."

    "Mentre parla con il padre, Aede cambia. La schiena più dritta, la voce più piatta. Un'arma che fa rapporto all'armaiolo."

    show glauco minaccioso with qdiss

    glauco "E quest[fin] sarebbe [il_t] giovane che si trovava nel corridoio ovest, la notte dello Svelo."

    "Il gelo mi scende dalla nuca ai talloni. Lo sa. Ovviamente lo sa."

    glauco "Mia figlia non commette errori, [figlio_t] di Briseide. Chi sostiene il contrario commette l'ultimo dei propri."

    pc "Non ho visto nessun errore, Autarca. Solo una lama molto rapida e una notte molto lunga."

    "Silenzio. Lungo. Poi Glauco fa un cenno minimo, e la porta alle mie spalle si apre da sola."

    glauco "Buona giornata, [figlio_t] di Briseide. Porta i miei rispetti alla tua Autarca."

    hide glauco with dissolve

    "Fuori, Aede mi affianca per tre passi esatti."

    aede "Hai risposto meno peggio del previsto."

    pc "Era un complimento?"

    show aede irritata with qdiss

    aede "Era una constatazione."

    "Ma di nuovo: quella piega all'angolo della bocca."

    return

################################################################################
## CAPITOLO 2 — L'Athlion
################################################################################

label cap2:

    scene bg arena_athlion with fade

    "L'Athlion. La gara atletica annuale in onore di Allmän, dove i Ceppi si misurano senza sangue — in teoria."

    "Corsa, salto, lancio, lotta. I Rami si giocano un anno di vanterie, e gli Autarchi fingono che non conti nulla mentre contano tutto."

    show aede neutra with dissolve

    "Il Ceppo di Glauco schiera lei. La vedo nel recinto degli atleti mentre si fascia i polsi, concentrata come davanti a un bersaglio."

    "Vanna, mia sorella di Ceppo, mi dà di gomito."

    vanna "La figlia di Glauco corre l'ultima staffetta. Dicono che quest'anno il Ramo se la giochi contro i Figli di Vittoria. Tu per chi tifi, [fratello_t]?"

    pc "Io guardo, ascolto e non mi faccio notare."

    vanna "Col modo in cui la fissi, due su tre."

    menu:
        "La staffetta si avvicina. Aede è alla linea, in attesa del testimone."

        "Tifare per lei a squarciagola":
            "Quando passa, urlo il suo nome con mezzo stadio."

            show aede irritata with qdiss

            "Mi sente. Rompe il ritmo per un decimo di respiro, mi fulmina con un'occhiata, riparte più forte."

            "Vince. Ma quando viene premiata non guarda nella mia direzione neanche per sbaglio. Credo di averla imbarazzata davanti al suo Ramo."

        "Aiutarla senza farmi vedere":
            $ aede_affinity += 2

            "Noto un Figlio del Ramo rivale armeggiare vicino alla corsia di cambio: sparge sabbia fine sulla pietra, dove lei pianterà il piede."

            "Non grido. Passo di lì con la borraccia «per sbaglio» aperta, e lavo via tutto."

            show aede sorpresa with qdiss

            "Aede vince di tre lunghezze. Alla premiazione i suoi occhi trovano i miei, poi la borraccia vuota, poi di nuovo i miei."

            show aede neutra with qdiss

            "Non un grazie. Un cenno della testa, uno solo, misurato al millimetro."

        "Iscrivermi alla corsa aperta e sfidarla":
            $ aede_affinity += 2

            "C'è una corsa aperta a tutti i Figli, a fine giornata. Mi iscrivo. Lei pure, per dovere di Ceppo."

            "Arrivo quart[fin], con i polmoni in fiamme. Lei prima, ovviamente, senza fiatone."

            show aede sorriso with dissolve

            aede "Quart[fin]. Per chi ha imparato a correre tre settimane fa, è quasi non umiliante."

            pc "L'anno prossimo arrivo terzo."

            aede "L'anno prossimo ti doppio."

            "E sorride. Tutta la faccia, denti compresi. Dura un battito, poi se ne accorge e lo fa sparire come refurtiva."

        "Ignorare la gara e andarmene presto":
            $ aede_affinity -= 2

            "Me ne vado prima della staffetta. Le gare non mi sono mai interessate."

            "Il giorno dopo, Corrado mi riferisce che Aede ha vinto per il suo Ramo. E che a fine gara ha cercato qualcuno tra la folla, senza trovarlo."

            "Me lo riferisce con la faccia di chi dice: sei un idiota, [fratello_t]."

    return

################################################################################
## CAPITOLO 3 — L'intrigo dei Rami
################################################################################

label cap3:

    scene bg vicoli_zefiro with fade

    "Le Bocche Sicofanti. Fessure di pietra sparse per Zefiro dove chiunque può infilare una delazione anonima."

    "Qualcuno ne ha infilata una contro il mio Ceppo: un carico di Briseide sparito, e il mio nome — il mio — indicato come complice del furto."

    show aede neutra with dissolve

    "E qualcun'altra ha ricevuto l'ordine di indagare in silenzio, prima che la cosa arrivi agli Arconti."

    aede "Non ti agitare, novellin[fin]. Se ti credessi colpevole, non staremmo parlando."

    pc "E cosa staremmo facendo?"

    aede "Tu, da bersaglio, mi fai da esca. Io, da esca, prendo il pesce. Qualcuno vuole colpire Briseide passando da te, e usare il mio Ceppo come mannaia."

    "Due Rami, una sola trappola. Se la delazione regge, il mio Ceppo perde l'onore e il suo viene usato come arma. Aede l'ha capito prima di tutti."

    menu:
        aede "Il magazzino della Contrada Marcassa. Stanotte. Decidi: vieni come esca viva, o resti a dormire come esca stupida?"

        "«Vengo. Ma se è una trappola per te, chi fa da esca sono io.»":
            $ aede_affinity += 2

            pc "Vengo. E se qualcuno deve prendersi la coltellata, mettimi davanti."

            show aede sorpresa with qdiss

            aede "...sei più scem[fin] di quanto sembri."

            "Lo dice piano. Intanto mi stringe la fibbia del mantello, due strattoni secchi."

        "«Resto. Delle trappole te ne intendi più tu.»":
            pc "Resto. Delle trappole te ne intendi più tu."

            show aede neutra with qdiss

            aede "Buonsenso. Era ora. ...Peccato, però."

            "Lo dice voltandosi, troppo in fretta perché possa leggerle la faccia."

    scene bg nero with fade

    "La notte del magazzino va come doveva andare: male, poi bene."

    scene bg vicoli_zefiro with dissolve
    show aede furia with vpunch

    "Il delatore si presenta con due lame a pagamento. Aede ne disarma una prima che io finisca di capire da dove è arrivata. La seconda esita — e l'esitazione, con lei, è una resa."

    "Il delatore prova a correre. Non è veloce."

    show aede neutra with qdiss

    aede "Un Filius del Ramo di Iperione. Gioco sporco tra correnti del Consiglio. Mio padre dirà due parole al suo Autarca, e le Bocche Sicofanti dimenticheranno il tuo nome."

    pc "Così, semplicemente?"

    aede "Così, semplicemente. È il vantaggio di essere il gioiello di Glauco Severo: nessuno discute il prezzo."

    "Lo dice con una voce strana. Come se il gioiello fosse un sasso che porta in tasca da troppi anni."

    "Poi, mentre il delatore geme a terra, Aede ride. Una risata corta, vera, sorpresa di esistere."

    aede "Hai fatto la faccia del merluzzo per tutta la rissa. Tutta."

    pc "È la mia tecnica. Distraggo il nemico con l'incredulità."

    show aede sorriso with dissolve

    aede "Pessima tecnica. Non cambiarla."

    "Rientriamo che è quasi alba. E io capisco due cose: che le devo la reputazione, forse la vita."

    "E che voglio sentirla ridere ancora. Anche a costo di rifare il merluzzo."

    return
