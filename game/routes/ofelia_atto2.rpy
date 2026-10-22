# Route Ofelia — Atto 2: il duello all'alba, la Fiaccolata (V/14) nelle tre
# varianti, il velo (V/26), la serra d'inverno (VI/5). Il dispatch della
# Fiaccolata e' in snodi.rpy (ev_fiaccolata / ev_luna6).

## Evento 3 — Il duello all'alba ###############################################

label ofelia_ev3:
    scene bg arena_athlion with fade
    show ofelia neutra with dissolve
    "L'arena all'alba sembra più grande: sabbia fredda, gradini vuoti, il fiato che si condensa in nuvole."
    "Ofelia ha due spade da allenamento. Non sono spuntate."
    ofelia "Dicono che tu sappia cavartela. Io dico che nessuno conosce la mia mano finché non l'ha vista dall'altra parte."
    "Mi lancia l'elsa. La afferro appena in tempo."
    ofelia "Fino al primo sangue. Non è un modo di dire."
    ofelia "Mio padre mi ha messo una spada in mano prima di una bambola. Aede ha imparato a colpire forte. Io ho imparato a colpire quando nessuno guarda."
    "Si toglie il mantello e lo piega sul gradino più basso, con calma, come se avessimo tutto il giorno. Poi si gira, e il giorno finisce."
    "Il primo colpo mi sfiora la guancia. Il secondo no. Lei è veloce, e non ha alcuna fretta di finire."
    "Paro una volta, per fortuna. Lei sorride: non per la parata, per la fortuna. La riconosce, e la disprezza."
    with hpunch
    "Cado su un ginocchio, la lama alla gola. Sopra di me, il suo respiro regolare."
    menu:
        "Ofelia non muove la spada. Attende la mia mossa."
        "Reggere il suo sguardo: «Colpisci pure. Non chiederò pietà.»":
            $ ofelia_affinity += 2
            show ofelia compiaciuta with qdiss
            ofelia "Nessuno regge. Nemmeno Aede, da bambine, e di coraggio ne ha per tre."
            "Abbassa la lama. Mi tende la mano libera, e noto che trema appena. Per l'attesa, forse. Per qualcos'altro."
        "Arrendermi con eleganza: «Hai vinto. Ma ti è costato fatica, ammettilo.»":
            $ ofelia_affinity += 1
            show ofelia imbarazzata with qdiss
            ofelia "...Fatica no. Attenzione, sì. È diverso, ma ti concedo il bluff."
            show ofelia neutra with qdiss
            "Ritira la spada. Un filo di sangue mi scende dal collo, e lei lo guarda come si guarda un conto saldato."
        "Chiedere pietà, ridendo, con le mani in alto":
            show ofelia rabbia with qdiss
            ofelia "Pietà. Quanto è umana, la parola. Rialzati. Per oggi basta così."
            "Gira sui tacchi e se ne va, lasciandomi la spada nella sabbia."
    "Il sole sale sopra i gradini. Sulla sabbia restano le nostre impronte, le sue dritte e leggere, le mie sparse come quelle di chi è scappato."
    "Riporto le lame all'armeria. Il custode le pulisce, guarda la mia guancia e scuote la testa. Non è la prima volta che lo vede."
    return



## Fiaccolata — Ofelia sola ####################################################

label ofelia_fiaccolata:
    scene bg cala_notte with fade
    "La Calà, trecento gradini di lanterne. La leggenda dice che chi la scende mano nella mano si amerà per sempre."
    show ofelia neutra with dissolve
    "Ofelia mi aspetta al primo gradino, in nero. Come se la festa fosse un lutto e lei l'unica ad averlo capito."
    ofelia "Ogni anno tre pretendenti mi chiedono la mano su questa scala. Ogni anno scendo da sola. È una tradizione anche questa."
    ofelia "Quest'anno cambio. Non montarti la testa: mi annoio in fretta."
    "Tre gradini più su, un pretendente in mantello verde stringe un mazzo di gigli. Ci guarda, guarda i gigli, e li lascia cadere nel fiume."
    ofelia "Il terzo dell'anno scorso. Ha aspettato dodici mesi per sentirsi dire di no. Glielo risparmio: è un regalo, a modo mio."
    menu:
        "Mi tende la mano col palmo in giù. Una regina che aspetta un baciamano, non una ragazza che aspetta una stretta."
        "Prenderle la mano e scendere senza dire niente":
            $ ofelia_affinity += 1
            show ofelia imbarazzata with dissolve
            "Le sue dita sono fredde. Al decimo gradino non lo sono più."
            ofelia "...niente frasi, niente leggende. Sai che a questo punto gli altri recitavano?"
            show ofelia compiaciuta with qdiss
            ofelia "Continua a tacere. Ti dona."
        "Baciarle la mano, come vuole il gesto":
            show ofelia neutra with qdiss
            ofelia "Corretto. Impeccabile. Lo faceva anche il cavallo, a modo suo."
            "Scendiamo vicini, a un palmo d'aria. Lei guarda il fiume; io guardo lei."
        "«La leggenda vale anche per chi non ci crede?»":
            show ofelia rabbia with qdiss
            ofelia "Vuoi garanzie? Va' da un notaio. Le leggende non rilasciano ricevute."
            "Scende da sola i primi cento gradini. Al centunesimo mi aspetta, senza voltarsi."
    "In fondo alla Calà il fiume si porta via i riflessi delle lanterne. Ofelia li guarda andare come si guardano i pretendenti: senza rimpianti."
    ofelia "Domani mio padre saprà. Aede lo saprà prima di lui, e Ascadeo ci avrà già scommesso sopra."
    ofelia "Lasciali parlare. Chi parla non sta guardando la mano che stringi."
    return


## Fiaccolata — a tre, con Caino ###############################################

label ofelia_fiaccolata_caino:
    scene bg cala_notte with fade
    show ofelia neutra with dissolve
    show caino neutro at left with dissolve
    "La Calà accesa da cima a fondo. Al primo gradino ci aspettano in due: Ofelia in nero, Caino col registro sotto il braccio. Anche stanotte."
    caino "La leggenda prevede due mani. Noi siamo tre contraenti. Ho controllato: nessuna clausola lo vieta."
    ofelia "Hai controllato una leggenda, Caino. Su cosa, sui registri delle nonne?"
    show caino sarcastico with qdiss
    caino "Sui registri dei matrimoni annullati. Sono molto più istruttivi."
    ofelia "E cosa dicono, i tuoi annullati?"
    caino "Che nessuno è mai sceso in tre. Quindi nessuno ha mai fallito in tre. Statisticamente, siamo imbattuti."
    show ofelia compiaciuta with qdiss
    ofelia "Decidi tu, [player_name]. Una mano a testa e tu nel mezzo. Lo vedranno tutti, sia chiaro."
    menu:
        "Mezza Zefiro sale la scala mentre noi scendiamo. Qualcuno si ferma già a guardare."
        "Prendere entrambe le mani: «Che guardino.»":
            $ ofelia_affinity += 1
            $ caino_fiducia += 1
            show caino tenero with dissolve
            caino "Annotato: dichiarazione pubblica, testimoni in numero eccessivo. Non revocabile."
            show ofelia imbarazzata with qdiss
            ofelia "...nemmeno io la revocherei. Non dirglielo."
            "Trecento gradini, tre ombre lunghe sul fiume. Un'Eparca si fa il segno degli dei; Ofelia le sorride come si sorride a un bersaglio."
        "Proporre di scendere a turno, per non dare spettacolo":
            show caino neutro with qdiss
            caino "Ragionevole. Contabile. Deludente, ma ragionevole."
            show ofelia rabbia with qdiss
            ofelia "A turno. Come in fila dal barbiere. Il secondo turno l'ho appena regalato al fiume."
            "Scendiamo in tre, separati da un palmo d'aria che tutta Zefiro sa misurare."
    "In fondo alla scala, Ofelia si ferma e guarda indietro, verso la cima. Le lanterne tremano. Da lassù, qualcuno del Ceppo ha visto tutto."
    return


## Fiaccolata — due sorelle, una mano ##########################################

label ofelia_fiaccolata_aede:
    scene bg cala_notte with fade
    show ofelia neutra with dissolve
    "La Calà accesa da cima a fondo. Ofelia mi intercetta al primo gradino, dove le lanterne fanno più ombra che luce."
    ofelia "Mia sorella è di turno, stanotte. Sorveglia la festa dall'alto della scala. Dice."
    ofelia "Sa che sei qui. Non sa di me. Sarebbe un peccato rovinarle la serata, no?"
    ofelia "Da bambine scendevamo la Calà insieme, io e lei, mano nella mano. Per gioco. Lei la stringeva così forte che mi lasciava i segni."
    "Lo dice senza nostalgia. Come si cita una vecchia ferita, per far vedere che è chiusa."
    show ofelia compiaciuta with qdiss
    ofelia "Una scala, due sorelle, una mano sola. Fa' i conti, [player_name]. Io li ho già fatti."
    menu:
        "In cima alla Calà, una sagoma col fiocco del Ceppo: Aede. Ofelia mi porge la mano, lenta."
        "Andare da Aede: stanotte la mano è sua":
            show ofelia neutra with qdiss
            ofelia "Prudente. Va', allora. Ti guardo scendere con lei: mi piace sapere cosa perdo."
            hide ofelia with dissolve
            call cap5
            # Ofelia ha guardato dal basso e approva la discrezione.
            $ ofelia_affinity += 1
            "In fondo alla Calà, tra la folla, incrocio uno sguardo in nero. Ofelia mi fa un cenno minimo col mento: un applauso che nessun altro deve vedere."
        "Prendere la mano di Ofelia":
            $ ofelia_affinity += 1
            $ aede_sospetto += 2
            $ ofelia_mano_cala = True
            show ofelia imbarazzata with dissolve
            ofelia "...l'hai presa sotto i suoi occhi. O sei coraggios[fin], o non sai contare."
            show ofelia compiaciuta with qdiss
            "Scendiamo. Al decimo gradino sento uno sguardo sulla nuca, caldo come una lama lasciata al sole."
            show aede rabbia at left with dissolve
            "Mi volto. Dall'alto della Calà, Aede ci guarda. Non si muove, non dice niente. Stringe l'elsa finché le nocche diventano bianche."
            hide aede with dissolve
            ofelia "Non voltarti più. Domani farà domande, e io avrò le risposte. Tu tieni la bocca chiusa."
    return


## Evento 4 — Il velo (V/26) ##################################################

label ofelia_ev4:
    scene bg vicoli_zefiro with fade
    show ofelia neutra with dissolve
    "Pomeriggio. Ofelia mi aspetta all'imbocco dei vicoli, un velo scuro sul capo e un cesto vuoto al braccio. Travestita da nessuno."
    ofelia "Dopo la Fiaccolata, Zefiro parla. Di me, di te. Mi annoia: le storie migliori dovrebbe raccontarle chi c'era."
    ofelia "Vado al mercato. Posso andarci col velo, e tu due passi dietro come un servo. Oppure senza."
    show ofelia compiaciuta with qdiss
    ofelia "Senza, ci vedranno tutti. Mio padre compreso, entro sera. Ho il vestito giusto per entrambe le versioni."
    if route_seconda == "aede":
        "Il mercato è a due vicoli dal Ceppo di Glauco. Aede ci passa ogni giorno, a quest'ora."
    elif route_seconda == "caino":
        "Dall'altra parte della strada, sotto il portico del Consiglio, Caino finge di leggere un registro. Non gira pagina da un pezzo."
    "Il vicolo odora di pane e di neve sporca. Una vecchia ci guarda dalla finestra, e Ofelia le restituisce lo sguardo finché lei non chiude le imposte."
    menu:
        "Mi porge il velo. Non si capisce se per sistemarglielo o per buttarlo."
        "Di nascosto: il velo resta, io due passi dietro":
            $ ofelia_affinity += 1
            show ofelia neutra with qdiss
            ofelia "Saggio. Un po' vigliacco, ma saggio. I segreti hanno il loro fascino: durano poco, come le rose."
            "Al mercato nessuno ci nota. Tra due banchi di spezie mi mette in mano una rosa nera, senza guardarmi."
        "Alla luce del sole: toglierle il velo e offrirle il braccio":
            $ ofelia_affinity += 2
            $ ofelia_in_pubblico = True
            if route_seconda == "aede":
                $ aede_sospetto += 1
            show ofelia imbarazzata with dissolve
            ofelia "...davanti al pescivendolo. Hai un senso dello spettacolo spaventoso."
            show ofelia compiaciuta with qdiss
            "Attraversiamo il mercato a braccetto. Le voci tacciono al nostro passaggio e riprendono più forti alle spalle."
            if route_seconda == "aede":
                "All'ultimo banco, una ragazza del Ceppo di Glauco ci riconosce e corre via. Stasera Aede saprà."
            ofelia "Adesso sei un pettegolezzo, [player_name]. Cerca di essere uno di quelli buoni."
    "Al ritorno il cesto non è più vuoto: una rosa nera, un limone, un coltello da frutta che lei ha pagato il doppio senza trattare."
    ofelia "Il coltello è per te. Non per la frutta. Lo capirai."
    return


## Interludio Luna VI — La serra d'inverno (VI/5, nessun punto) ##############

label interludio_ofelia_luna6:
    scene bg sala_svelo with fade
    "Il quinto giorno della Luna VI la serra è chiusa a tutti. Glauco ha spento i tubi caldi: per punizione, dicono i servi. Non dicono di chi."
    show ofelia neutra with dissolve
    "Ofelia è dentro lo stesso, col mantello addosso e il fiato che fuma. Le rose nere si arrendono al freddo, una per una."
    ofelia "Me l'ha fatto sapere a cena. Senza dirlo. Mio padre non dice: spegne le stufe."
    ofelia "Sa di te. Lo sa da Lune. Aspettava di vedere se eri un capriccio. Adesso ha smesso di aspettare."
    if route_seconda_viva() == "caino":
        "Sul tavolo degli attrezzi c'è un foglio di registro, piegato a triangolo. La calligrafia minuta di Caino."
        ofelia "Il tuo ragioniere ha mandato i conti. Secondo lui Glauco ci convoca entro sedici giorni. Ha messo anche le probabilità."
        ofelia "Non le ho lette. Detesto quando ha ragione prima del tempo."
    elif route_seconda_viva() == "aede":
        "Dalla porta socchiusa arriva un rumore di passi sul ghiaino. Ofelia non si volta, ma smette di respirare finché non si allontanano."
        ofelia "Aede. Viene a controllare la serra ogni sera, da quando nostro padre è di cattivo umore. Dice che è per i ladri."
        ofelia "Non ha mai preso un ladro. Ma ha sempre preso me."
    else:
        "Non c'è nessun altro. Nemmeno i servi. Solo lei, il freddo, e io che ho ignorato il cartello alla porta."
    show ofelia compiaciuta with qdiss
    ofelia "Ho una domanda per te, e non è quella della serra di sera. Quella l'hai già superata. Questa è più piccola, e più cattiva."
    ofelia "Quando lui ti chiamerà nello studio, cosa farai con le mani?"
    menu:
        "Fuori, la neve comincia a cadere sul vetro. Il silenzio fa più rumore delle rose."
        "«Le terrò ferme. Sul tavolo, dove possa vederle.»":
            show ofelia neutra with qdiss
            ofelia "Bene. Mio padre legge le mani prima delle facce. Se tremano, ti ha già battut[fin]."
            "Mi prende un polso e lo tiene, a lungo, come un medico. Poi lo lascia andare, soddisfatta."
        "«Le terrò in tasca. Così non sa cosa stringo.»":
            show ofelia compiaciuta with qdiss
            ofelia "...questo è un trucco mio. Me l'hai rubato, o ci sei arrivat[fin] da sol[fin]? Non rispondere."
            "Si infila le mani nelle tasche del mantello, e per un attimo siamo due congiurati in una serra morta."
        "«Prenderò la tua, se me la lasci.»":
            show ofelia imbarazzata with dissolve
            ofelia "...nello studio di mio padre. Davanti a lui. Sei pazz[fin], o mi conosci troppo poco."
            show ofelia neutra with qdiss
            ofelia "Te la lascerò. Forse. Dipende da quanto mi annoi fino ad allora."
    "Ofelia raccoglie una rosa morta dal vaso più vicino. È nera, rigida di gelo, perfetta."
    ofelia "Le rose di mio padre muoiono quando lui decide. Questa no. Questa l'ho tagliata io, prima."
    "Me la mette in mano. I petali si spezzano al primo tocco, come vetro sottile."
    ofelia "Sedici giorni. Non venire a cercarmi prima. Voglio che mi manchi qualcosa, quando entro in quello studio."
    hide ofelia with dissolve
    "Esco nella neve. Il fiore blu vicino alla porta, quello che non fiorisce mai, ha un bocciolo. Piccolo. Chiuso come un pugno."
    return
