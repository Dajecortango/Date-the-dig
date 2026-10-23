# Route Aede — Atto 2: capitoli 4-6.

################################################################################
## CAPITOLO 4 — Il lavoro di Aede
################################################################################

label cap4:

    scene bg vicoli_zefiro with fade

    "Contrada Marcassa, dopo il tramonto. Briseide mi ha mandato a ritirare un pagamento da un mercante di lane. Strade sbagliate, ora sbagliata."

    "Sento le voci prima di vedere niente: un uomo che supplica, a bassa voce, come chi sa che urlare è inutile."

    "Mi affaccio al vicolo. E la vedo."

    show aede neutra with dissolve

    "Aede. Senza maschera, senza fretta. Davanti a lei, in ginocchio tra le casse, un uomo di mezza età con l'anello d'oro dei cambiavalute."

    "Non è una rissa. Non è una trappola. È un lavoro."

    aede "Hai venduto i movimenti delle carovane del mio Ceppo alla Lama Nera. Due scorte morte sul Passo. Il Consiglio non lo saprà mai, perché il mio Ceppo non processa: salda."

    "L'uomo supplica ancora. Nomina dei figli, una casa a Rundeberg, cifre."

    with lampo

    "La lama è un lampo bianco. Poi il vicolo torna silenzioso."

    show aede neutra at center

    "Aede pulisce l'acciaio con un gesto che ha fatto mille volte. Poi alza gli occhi. E mi vede."

    "Non trasalisce. Non si giustifica. Mi guarda e basta, e nel suo sguardo c'è una domanda fredda: e adesso?"

    menu:
        aede "Di' qualcosa, novellin[fin]. Qualunque cosa. Ma pensala bene."

        "«Questo è... questo è assassinio.»":
            $ aede_affinity -= 3
            $ flag_accetta_lavoro = False

            pc "Questo è... questo è assassinio."

            show aede irritata with qdiss

            aede "Questo è il Nord. Questo è il mio Ceppo. Questo sono io."

            aede "Credevi di passeggiare con cosa, esattamente? Con una ricamatrice?"

            "La voce le si incrina sull'ultima parola. Stringe l'elsa finché le nocche sbiancano."

            aede "Torna dal tuo mercante di lane, [figlio_t] di Briseide. E dimentica il vicolo."

            "Mi volta le spalle. Il passo è troppo svelto, per lei."

        "«Il tuo Ceppo salda. Ho capito. Non ho visto niente.»":
            $ aede_affinity += 1
            $ flag_accetta_lavoro = True

            pc "Salda. Ho capito. Io qui non c'ero."

            show aede neutra with qdiss

            aede "Impari in fretta le regole."

            "Lo dice piatta. Ma mentre mi passa accanto rallenta di mezzo passo. Aspetta. Non dico niente, e lei riparte."

        "«Chi era per te, quest'uomo? Cosa ti costa, questo lavoro?»":
            $ aede_affinity += 3
            $ flag_accetta_lavoro = True

            pc "Chi era, per te? E a te quanto costa?"

            show aede sorpresa with qdiss

            "Si blocca. La lama, a metà del fodero, resta lì."

            show aede neutra with qdiss

            aede "Per me non era nessuno. È questo che lo rende un lavoro."

            aede "Quanto costa. Col primo non dormi per una Luna. Poi dormi. È peggio."

            "Si siede su una cassa. Io mi siedo su quella accanto, a distanza di rispetto. Restiamo così finché le lanterne della Contrada non si spengono."

            aede "Se lo racconti a qualcuno, ti ammazzo."

            pc "Lo so."

            aede "...grazie."

            "L'ha detto così piano che potrei averlo sognato."

    return

################################################################################
## CAPITOLO 5 — La Fiaccolata della Calà
################################################################################

label cap5:

    scene bg cala_notte with fade

    "La Calà: la scalinata vecchia che scende dalla Contrada Eburnea al fiume, trecento gradini consumati."

    "Una notte all'anno, la Fiaccolata. Lanterne su ogni gradino, e la leggenda che tutta Zefiro finge di non prendere sul serio prendendola malissimo sul serio:"

    "chi percorre la Calà mano nella mano, si amerà per sempre."

    show aede neutra with dissolve

    "Lei è lì. Non per la leggenda, dice: il Ceppo di Glauco sorveglia la festa, e a lei è toccato il turno. Dice."

    aede "Non fare quella faccia, novellin[fin]. Sono qui per lavoro."

    pc "Non ho detto niente."

    aede "La tua faccia parla per tre."

    "Scendiamo insieme i primi gradini, a un braccio di distanza. Sotto di noi la scala di luci cola verso il fiume come oro fuso."

    "Vanna e Corrado ci incrociano salendo. Vanna mi fa un gesto osceno di incoraggiamento alle spalle di Aede. Corrado la trascina via per la collottola."

    menu:
        "Al trentesimo gradino, la sua mano è vicina alla mia. Non si sposta."

        "Prenderle la mano" if aede_affinity >= 8:
            $ aede_affinity += 3
            $ aede_mano_cala = "presa"

            "Non chiedo il permesso. Se lo chiedessi, direbbe no per principio."

            "Le prendo la mano. Le sue dita si irrigidiscono — un istante — poi, piano, si intrecciano alle mie."

            show aede imbarazzata with qdiss

            aede "Questo non significa niente. È... perché la scala è ripida."

            pc "Ripidissima."

            aede "Se cadi, ti lascio rotolare fino al fiume."

            "Ma non lascia la presa. Non la lascia per duecentosettanta gradini."

            "Al fondo della Calà, col fiume davanti e le lanterne alle spalle, si volta verso di me. E per un momento né la figlia di Glauco né l'assassina: solo Aede, con gli occhi pieni di luci."

            aede "[player_name]. Io—"

            show aede irritata with qdiss

            "Un fischio dalla cima della scala. Il segnale del suo Ceppo: cambio turno."

            aede "...devo andare."

            "Sale i gradini a due a due. A metà scala si ferma, un solo istante, e si volta. Poi la notte se la riprende."

        "Prenderle la mano" if aede_affinity < 8:
            $ aede_mano_cala = "rifiutata"

            "Non chiedo il permesso. Allungo la mano verso la sua."

            show aede irritata with qdiss

            "Lei la ritira con naturalezza perfetta, come se dovesse sistemarsi i capelli proprio in quell'istante."

            aede "Giù le mani, novellin[fin]. Su questa scala una mano vuol dire una cosa. E noi due quella cosa non siamo."

            "Senza cattiveria. Un taglio pulito, di quelli che bruciano dopo."

        "Camminarle accanto, senza toccarla":
            $ aede_affinity += 1
            $ aede_mano_cala = "accanto"

            "Scendiamo fianco a fianco, le mani a un dito di distanza, senza che nessuna delle due attraversi il confine."

            show aede neutra with qdiss

            aede "Tutta Zefiro crede a questa storia della mano nella mano. Patetico."

            pc "Patetico."

            aede "...tu ci credi?"

            pc "Chiedimelo al fondo della scala."

            "Ma al fondo della scala c'è il cambio turno del suo Ceppo, e la domanda resta sui gradini, insieme alle lanterne."

        "Restare qualche gradino indietro":
            $ aede_affinity -= 2
            $ aede_mano_cala = "indietro"

            "Rallento. Metto distanza. La leggenda, il Ceppo, il padre: troppo, tutto insieme."

            show aede neutra with qdiss

            "Lei non si volta a cercarmi. Finisce la scala da sola, dritta come una lama, e si perde tra le lanterne del fondo."

            "Corrado, più tardi, mi chiede com'è andata. Non rispondo. È andata che sono [un_t] codard[fin]."

    return

################################################################################
## CAPITOLO 6 — Il giuramento
################################################################################

label cap6:

    scene bg corridoio_ceppo with fade

    "Mi trova lei, stavolta. Alla tenuta del mio Ceppo, su un ballatoio che guarda i tetti di Zefiro, un'ora prima dell'alba."

    show aede neutra with dissolve

    aede "Non riuscivo a dormire. E la tua tenuta ha le serrature peggiori del Nord, sappilo."

    pc "Lo riferirò a Briseide."

    aede "Non lo riferirai."

    "Si appoggia alla balaustra accanto a me. Per un po' guardiamo i tetti scurirsi e poi accendersi di brace, a oriente."

    aede "Questa notte, vent'anni fa, io avevo un altro nome."

    "Il cuore mi si ferma. Il giuramento. Il tabù dei tabù: nessun Dignitas rivela la vita di prima. Proclamarla è morte; ascoltarla, forse peggio."

    aede "Non l'ho mai detto a nessuno. Mio padre lo sa senza che io l'abbia detto, perché mio padre sa tutto. Ma dirlo... dirlo è un'altra cosa. Dirlo è darlo via."

    show aede imbarazzata with qdiss

    aede "E io stanotte avrei voglia di darlo via. A te. Capisci cosa ti sto offrendo, [player_name]?"

    menu:
        "Ha le mani strette sulla balaustra. Le nocche bianche."

        "Fermarla. «Il tuo nome di prima è morto. Io voglio quella viva.»":
            $ flag_giuramento = True
            $ aede_affinity += 2

            "Le metto due dita sulle labbra, piano."

            pc "Il tuo nome di prima è morto. Io voglio quella viva."

            pc "Non devi comprarmi con un segreto, Aede. Non devi comprarmi affatto."

            show aede sorpresa with qdiss

            "Mi fissa. Qualcosa le si scioglie nella linea delle spalle, un nodo vecchio di vent'anni."

            show aede sorriso with dissolve

            aede "Rifiuti il tesoro e ti prendi la cassaforte. Che razza di ladr[fin]..."

            pc "La cassaforte mi è sempre piaciuta più del tesoro."

            aede "Idiota."

            "Ma lo dice con la fronte appoggiata alla mia spalla. E il sole, quando sorge, ci trova così."

        "Ascoltarla fino in fondo":
            $ flag_giuramento = False
            $ flag_aede_rivelato = True
            $ aede_affinity += 1

            with ricordo

            "Non la fermo. Mi racconta: un villaggio dei Collifreddi, un clan in faida, una bambina veloce di mano che rubava per mangiare. Un nome che non scriverò mai, da nessuna parte."

            $ muovi("aede", "trema")
            "Quando finisce, trema. Io le copro le spalle col mio mantello."

            "E dal buio del cortile, sotto di noi, qualcosa si muove. Una sagoma ferma, grigia, paziente."

            show glauco minaccioso with dissolve

            "Glauco Severo. Che guarda il ballatoio. Che ha sentito, o sa senza aver bisogno di sentire."

            hide glauco with dissolve

            "Quando riguardo il cortile, non c'è più nessuno. Aede non l'ha visto. Io non dormirò mai più."

        "Fermarla e offrirle il mio, di passato":
            $ flag_giuramento = False
            $ aede_affinity -= 1

            pc "Allora facciamo a metà. Il tuo segreto per il mio. Anch'io avevo un nome, prima."

            show aede irritata with qdiss

            "Si stacca dalla balaustra di scatto, come scottata."

            aede "No. No, tu non capisci niente. Io posso buttare via il mio giuramento: è mio. Ma non ti lascerò buttare il tuo per pareggiare un conto."

            aede "Senza giuramento siamo ladri col mantello, [player_name]. Se lo rompi per me, un giorno mi odierai. E io—"

            "Non finisce la frase. Se ne va com'è venuta, dalle serrature peggiori del Nord."

    scene bg nero with fade

    "Due giorni dopo, un messo col leone dorato sul petto si presenta alla mia tenuta."

    "Il Ceppo di Glauco Severo convoca [il_t] [figlio_t] di Briseide, [player_name], nello studio dell'Autarca."

    "Da sol[fin]."

    return

################################################################################
## LUNA VI — La palestra al buio (fisso VI/12 sera, nessun punto)
################################################################################

label aede_luna6:

    scene bg corridoio_ceppo with fade

    show vanna neutra at left with dissolve

    "La convocazione di Glauco è per il ventuno. Mancano nove giorni, e Aede è sparita."

    vanna "Tre volte nello studio di suo padre, in una settimana. Tre. L'ultima è uscita senza mantello, con la neve che c'era."

    vanna "E stamattina il suo Ceppo ha fatto affilare una lama sola. Una, [fratello_t]. Le altre le lasciano spuntate."

    hide vanna with dissolve

    scene bg palestra with fade

    "La trovo dove sapevo di trovarla: in palestra, a quest'ora, con una lanterna sola e il fantoccio di paglia già mezzo sventrato."

    show aede neutra with dissolve

    "Non si volta. Sente i miei passi dalla soglia, lo so dal modo in cui la stoccata successiva arriva più bassa."

    aede "Non stasera, [player_name]."

    menu:
        "La lama si ferma a un dito dalla paglia. Aspetta che io faccia qualcosa."

        "Prendere una spada di legno e allenarmi accanto a lei, in silenzio":
            $ aede_luna6_esito = "resta"
            "Prendo una spada dalla rastrelliera. Mi metto al fantoccio accanto. Non dico niente."
            show aede irritata with qdiss
            aede "Il gomito. Lo alzi sempre, quando sei stanc[fin]."
            "Lo abbasso. Andiamo avanti così fino a che la lanterna non comincia a fumare. Lei non mi manda via. Non mi guarda nemmeno."

        "«Cosa ti ha ordinato tuo padre?»":
            $ aede_luna6_esito = "chiede"
            pc "Cosa ti ha ordinato tuo padre, Aede?"
            show aede rabbia with vpunch
            "La lama entra nella paglia fino all'elsa."
            aede "Non chiedermelo. Se te lo dico, diventa vero. E le cose vere, io le eseguo."
            show aede triste with qdiss
            aede "Il ventuno. Vai da lui. Ascolta tutto. Poi decidi tu cosa sono."

        "Lasciarle la sala, e andarmene":
            $ aede_luna6_esito = "lascia"
            "Mi volto. Sulla soglia mi fermo un istante, poi tiro dritto."
            show aede triste with qdiss
            aede "...grazie."
            "Lo dice al fantoccio, non a me. Dietro di me ricominciano le stoccate. Più veloci. Più storte."

    return
