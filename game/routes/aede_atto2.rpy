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

    "La lama è un lampo bianco. Poi il vicolo torna silenzioso."

    show aede neutra at center

    "Aede pulisce l'acciaio con un gesto che ha fatto mille volte. Poi alza gli occhi. E mi vede."

    "Non trasalisce. Non si giustifica. Mi guarda e basta, e nel suo sguardo c'è una domanda fredda: e adesso?"

    menu:
        aede "Di' qualcosa, novellino. Qualunque cosa. Ma pensala bene."

        "«Questo è... questo è assassinio.»":
            $ aede_affinity -= 3
            $ flag_accetta_lavoro = False

            pc "Questo è... questo è assassinio."

            show aede irritata

            aede "Questo è il Nord. Questo è il mio Ceppo. Questo sono io."

            aede "Credevi di passeggiare con cosa, esattamente? Con una ricamatrice?"

            "La voce le si incrina sull'ultima parola. Di rabbia, mi dico. Ma non è solo rabbia."

            aede "Torna dal tuo mercante di lane, Figlio di Briseide. E dimentica il vicolo."

            "Mi volta le spalle. E per la prima volta da quando la conosco, sembra avere fretta."

        "«Il tuo Ceppo salda. Ho capito. Non ho visto niente.»":
            $ aede_affinity += 1
            $ flag_accetta_lavoro = True

            pc "Il tuo Ceppo salda. Ho capito. Non ho visto niente."

            show aede neutra

            aede "Impari in fretta le regole."

            "Lo dice piatta. Ma mentre mi passa accanto rallenta di mezzo passo, come se si aspettasse altro da me. Come se le regole, stanotte, non le bastassero."

        "«Chi era per te, quest'uomo? Cosa ti costa, questo lavoro?»":
            $ aede_affinity += 3
            $ flag_accetta_lavoro = True

            pc "Chi era per te, quest'uomo? Cosa ti costa, questo lavoro?"

            show aede sorpresa

            "Si blocca. Nessuno, capisco in quell'istante, le ha mai fatto quella domanda. Né il padre, né i fratelli, né i morti."

            show aede neutra

            aede "Per me non era nessuno. È questo che lo rende un lavoro."

            aede "Quanto costa... Il primo costa tutto. Gli altri costano il ricordo del primo."

            "Si siede su una cassa. Io mi siedo su quella accanto, a distanza di rispetto. Restiamo così finché le lanterne della Contrada non si spengono."

            aede "Se lo racconti a qualcuno, ti ammazzo."

            pc "Lo so."

            aede "...grazie."

            "L'ha detto così piano che potrei averlo sognato."

    jump interludio3

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

    aede "Non fare quella faccia, novellino. Sono qui per lavoro."

    pc "Non ho detto niente."

    aede "La tua faccia parla per tre."

    "Scendiamo insieme i primi gradini, a un braccio di distanza. Sotto di noi la scala di luci cola verso il fiume come oro fuso."

    "Vanna e Corrado ci incrociano salendo. Vanna mi fa un gesto osceno di incoraggiamento alle spalle di Aede. Corrado la trascina via per la collottola."

    menu:
        "Al trentesimo gradino, la sua mano è vicina alla mia. Non si sposta."

        "Prenderle la mano" if aede_affinity >= 8:
            $ aede_affinity += 3

            "Non chiedo il permesso. Se lo chiedessi, direbbe no per principio."

            "Le prendo la mano. Le sue dita si irrigidiscono — un istante — poi, piano, si intrecciano alle mie."

            show aede imbarazzata

            aede "Questo non significa niente. È... perché la scala è ripida."

            pc "Ripidissima."

            aede "Se cadi, ti lascio rotolare fino al fiume."

            "Ma non lascia la presa. Non la lascia per duecentosettanta gradini."

            "Al fondo della Calà, col fiume davanti e le lanterne alle spalle, si volta verso di me. E per un momento né la figlia di Glauco né l'assassina: solo Aede, con gli occhi pieni di luci."

            aede "[player_name]. Io—"

            show aede irritata

            "Un fischio dalla cima della scala. Il segnale del suo Ceppo: cambio turno."

            aede "...devo andare."

            "Sale i gradini a due a due. A metà scala si ferma, un solo istante, e si volta. Poi la notte se la riprende."

        "Prenderle la mano" if aede_affinity < 8:

            "Non chiedo il permesso. Allungo la mano verso la sua."

            show aede irritata

            "Lei la ritira con naturalezza perfetta, come se dovesse sistemarsi i capelli proprio in quell'istante."

            aede "Attento, novellino. Su questa scala i gesti hanno un significato. E tu e io non ci conosciamo abbastanza perché ne abbiano."

            "Non è crudele. È esatta. Fa più male così."

        "Camminarle accanto, senza toccarla":
            $ aede_affinity += 1

            "Scendiamo fianco a fianco, le mani a un dito di distanza, senza che nessuna delle due attraversi il confine."

            show aede neutra

            aede "Tutta Zefiro crede a questa storia della mano nella mano. Patetico."

            pc "Patetico."

            aede "...tu ci credi?"

            pc "Chiedimelo al fondo della scala."

            "Ma al fondo della scala c'è il cambio turno del suo Ceppo, e la domanda resta sui gradini, insieme alle lanterne."

        "Restare qualche gradino indietro":
            $ aede_affinity -= 2

            "Rallento. Metto distanza. La leggenda, il Ceppo, il padre: troppo, tutto insieme."

            show aede neutra

            "Lei non si volta a cercarmi. Finisce la scala da sola, dritta come una lama, e si perde tra le lanterne del fondo."

            "Corrado, più tardi, mi chiede com'è andata. Non rispondo. È andata che sono un codardo."

    jump cap6

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

    show aede imbarazzata

    aede "E io stanotte avrei voglia di darlo via. A te. Capisci cosa ti sto offrendo, [player_name]?"

    menu:
        "La capisco. Sta offrendo l'unica cosa che il giuramento le ha lasciato da offrire."

        "Fermarla. «Il tuo nome di prima è morto. Io voglio quella viva.»":
            $ flag_giuramento = True
            $ aede_affinity += 2

            "Le metto due dita sulle labbra, piano."

            pc "Il tuo nome di prima è morto. Io voglio quella viva."

            pc "Non devi comprarmi con un segreto, Aede. Non devi comprarmi affatto."

            show aede sorpresa

            "Mi fissa. Qualcosa le si scioglie nella linea delle spalle, un nodo vecchio di vent'anni."

            show aede sorriso

            aede "Sei l'unico uomo del Nord che rifiuta un tesoro per prendersi la cassaforte."

            pc "La cassaforte mi è sempre piaciuta più del tesoro."

            aede "Idiota."

            "Ma lo dice con la fronte appoggiata alla mia spalla. E il sole, quando sorge, ci trova così."

        "Ascoltarla fino in fondo":
            $ flag_giuramento = False
            $ flag_aede_rivelato = True
            $ aede_affinity += 1

            "Non la fermo. Mi racconta: un villaggio dei Collifreddi, un clan in faida, una bambina veloce di mano che rubava per mangiare. Un nome che non scriverò mai, da nessuna parte."

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

            show aede irritata

            "Si stacca dalla balaustra di scatto, come scottata."

            aede "No. No, tu non capisci niente. Io posso buttare via il mio giuramento: è mio. Ma non ti lascerò buttare il tuo per pareggiare un conto."

            aede "Il giuramento è l'unica cosa che ci rende Dignitas, [player_name]. Se lo rompi per me, un giorno mi odierai. E io—"

            "Non finisce la frase. Se ne va com'è venuta, dalle serrature peggiori del Nord."

    scene bg nero with fade

    "Due giorni dopo, un messo col leone dorato sul petto si presenta alla mia tenuta."

    "Il Ceppo di Glauco Severo convoca il Figlio di Briseide, [player_name], nello studio dell'Autarca."

    "Da solo."

    jump climax
