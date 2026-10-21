# Route Ofelia — snodi di Luna V-VI: Fiaccolata della Calà (V/14) nelle tre
# varianti (Ofelia sola, a tre con Caino, a due mani con Aede), poi climax e
# finali. Il dispatch e' in snodi.rpy (ev_fiaccolata / ev_luna6).


## Fiaccolata — Ofelia sola ####################################################

label ofelia_fiaccolata:
    scene bg cala_notte with fade
    "La Calà, trecento gradini di lanterne. La leggenda dice che chi la scende mano nella mano si amerà per sempre."
    show ofelia neutra with dissolve
    "Ofelia mi aspetta al primo gradino, in nero. Come se la festa fosse un lutto e lei l'unica ad averlo capito."
    ofelia "Ogni anno tre pretendenti mi chiedono la mano su questa scala. Ogni anno scendo da sola. È una tradizione anche questa."
    ofelia "Quest'anno cambio. Non montarti la testa: mi annoio in fretta."
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
    return


## Fiaccolata — due sorelle, una mano ##########################################

label ofelia_fiaccolata_aede:
    scene bg cala_notte with fade
    show ofelia neutra with dissolve
    "La Calà accesa da cima a fondo. Ofelia mi intercetta al primo gradino, dove le lanterne fanno più ombra che luce."
    ofelia "Mia sorella è di turno, stanotte. Sorveglia la festa dall'alto della scala. Dice."
    ofelia "Sa che sei qui. Non sa di me. Sarebbe un peccato rovinarle la serata, no?"
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


################################################################################
## CLIMAX — Lo studio di Glauco, la figlia imprevedibile
################################################################################

label ofelia_climax:
    scene bg studio_glauco with fade
    show glauco neutro with dissolve
    "Lo studio di Glauco Severo. Silenzio, ordine, una candela sola. Il vino è già versato in due calici."
    glauco "Siediti, [figlio_t] di Briseide. Mia figlia dice che sei un capriccio. Io conto i capricci: questo dura da troppe Lune."
    show ofelia neutra at left with dissolve
    "Ofelia è in piedi accanto alla finestra, in nero. Non mi guarda. Guarda la candela come si guarda un bersaglio."
    glauco "Ofelia è la mia figlia imprevedibile. Al punto giusto: l'ho cresciuta così. Ogni anno tre pretendenti, ogni anno nessuno."
    show glauco minaccioso with qdiss
    glauco "Stanotte firmi la rinuncia e torni da tua madre con un dono del Ceppo. Oppure non firmi, e il dono te lo porto io."
    "La pergamena è sul tavolo, la penna accanto, già intinta. Glauco non lascia mai niente a metà."
    show ofelia compiaciuta at left with qdiss
    ofelia "Padre. Hai dimenticato una clausola."
    "Prende la pergamena e la avvicina alla candela, con la grazia con cui si porge un fazzoletto."
    show glauco furioso
    with vpunch
    "La carta prende fuoco. Ofelia la lascia cadere nel calice di suo padre, e il vino sfrigola."
    ofelia "Non scelgo pretendenti da un catalogo, padre. Li scelgo come tu scegli le lame: da come reggono il colpo."
    ofelia "Questo l'ha retto. I tuoi, no."
    if route_seconda_viva() == "caino":
        ofelia "E sì, c'è un altro contraente. Lo sai già: tieni registri migliori dei suoi. Si firma in tre, o non firma nessuno."
    show glauco deluso with qdiss
    glauco "Mi sfidi. In casa mia. Per [lui_t]."
    ofelia "Ti sorprendo, padre. È diverso. L'hai insegnato tu: un colpo che si vede arrivare non è un colpo."
    "Glauco mi guarda. Per la prima volta non come un conto da saldare, ma come una voce che non torna nel bilancio."
    glauco "E tu, [figlio_t] di Briseide? Lei ha bruciato la carta. Ora dimmi cosa resta sul tavolo."
    menu:
        "Ofelia non si volta. Aspetta, le dita ferme sullo stelo del calice. Sa cosa spera; non lo dirà."
        "Mettersi al suo fianco, senza dire niente":
            $ ofelia_affinity += 1
            show ofelia imbarazzata at left with dissolve
            "Mi alzo e vado alla finestra. Le sfioro la mano col dorso della mia. Lei non la ritira."
            ofelia "...di nuovo niente frasi. Cominci a conoscermi. È preoccupante."
            glauco "Il silenzio. Almeno questo l'hai capito prima di me."
        "Rispondere a Glauco a testa alta: «Resta lei. E resto io.»":
            show ofelia neutra at left with qdiss
            ofelia "Elegante. Un po' troppo coraggios[fin] per i miei gusti. Ma il tono era giusto."
            glauco "Il coraggio. Il difetto preferito di chi muore giovane. Vedremo."
        "Prendere le sue difese: «Non decidete voi per lei.»":
            $ ofelia_affinity -= 1
            show ofelia rabbia at left with qdiss
            ofelia "Non mi serve un avvocato, [player_name]. La carta l'ho bruciata da sola."
            ofelia "Difendimi ancora, e la prossima pergamena la firmo io. Contro di te."
            glauco "Vedi, figlia? Non ti conosce nemmeno [lui_t]."
    jump ofelia_routing

label ofelia_routing:
    # Ordine vincolante: good poly Caino -> good -> neutral.
    if ofelia_affinity >= 11 and ofelia_mancati <= 1 and route_seconda_viva() == "caino" and caino_fiducia >= 12:
        jump ofelia_good_caino
    elif ofelia_affinity >= 11 and ofelia_mancati <= 1:
        jump ofelia_good
    else:
        jump ofelia_neutral


################################################################################
## ROUTING POLY AEDE — innestato nel climax di Aede (aede_finali.rpy)
################################################################################

label ofelia_poly_aede_routing:
    # Ordine vincolante: tempesta -> good a due -> good sola (coda amara) ->
    # routing Aede esistente, ricopiato senza il good (gestito qui sopra).
    if aede_sospetto >= 2:
        jump ofelia_bad_tempesta
    elif ofelia_affinity >= 11 and ofelia_mancati <= 1 and aede_affinity >= 12 and flag_giuramento and flag_accetta_lavoro:
        jump ofelia_good_aede
    elif ofelia_affinity >= 11 and ofelia_mancati <= 1:
        jump ofelia_good
    # Finali di Aede: Ofelia esce di scena prima (i finali usano glauco at left).
    "Ofelia mi guarda un'ultima volta, poi arretra nel bianco. La neve si richiude su di lei senza un rumore."
    hide ofelia with dissolve
    if aede_affinity >= 12 and flag_giuramento and flag_accetta_lavoro:
        jump good_end
    elif not flag_segreto_svelo and aede_affinity < 3:
        jump bad_end_glauco
    elif aede_affinity < 3:
        jump bad_end_aede
    else:
        jump neutral_end


################################################################################
## GOOD END — Tanto bella quanto letale (coda amara se il poly non regge)
################################################################################

label ofelia_good:
    # Prologo solo se arriviamo dal climax di Aede (neve); la coda resta su route_seconda.
    if route_seconda_viva() == "aede":
        show aede neutra with dissolve
        "Aede guarda la lama, poi guarda me. Poi guarda sua sorella, che non si è mossa di un passo."
        aede "Mio padre voleva un saldo. Non l'avrà. Non per te, [player_name]: per lei, che non mi ha mai chiesto niente."
        "Rinfodera. Si volta e se ne va nella neve, senza fretta. Non si gira."
        hide aede with dissolve
    scene bg cala_notte with fade
    show ofelia neutra with dissolve
    "Più tardi, la Calà è spenta. Trecento gradini al buio: nessuna lanterna, nessuna leggenda a garantire niente."
    ofelia "Sai cosa dicono di me a Zefiro? Che sono bella. Sbagliano l'ordine: prima sono letale. La bellezza è un dettaglio."
    pc "Allora ho corso un rischio."
    show ofelia compiaciuta with qdiss
    ofelia "Il più grosso della tua vita. Te lo ricorderò ogni giorno. È il mio modo di essere affettuosa."
    "Mi tende la mano. Non col palmo in giù, stavolta: aperta, alla pari."
    show ofelia imbarazzata with dissolve
    ofelia "Niente di sdolcinato, non chiederlo. Ma domani a cena da mio padre mi siedo accanto a te."
    ofelia "Davanti a tutto il Ceppo. Per me è come scriverlo sulle mura."
    "Scendiamo al buio, mano nella mano. Al centesimo gradino lei ride piano, una volta sola. Non lo ammetterà mai."
    if route_seconda == "aede":
        scene bg esterno_neve with fade
        "Qualche notte dopo, sulle mura, vedo una sagoma col fiocco del Ceppo. Ferma nella neve, a guardare la città."
        "Aede non ne parlerà mai, né con me né con sua sorella. È l'unico colpo che le ho risparmiato, e pesa più di tutti."
    elif route_seconda == "caino":
        scene bg vicoli_zefiro with fade
        show caino freddo at left with dissolve
        "Caino lo incrocio davanti al Consiglio. Ha il registro aperto e una riga già tirata."
        caino "Contratto a tre: risolto per inadempienza. Nessuna penale. Ho controllato."
        "Chiude il registro con un colpo secco. Le dita gli tremano appena: la prima voce del suo bilancio che non torna."
        hide caino with dissolve
    scene bg nero with fade
    centered "{cps=20}{size=+10}TANTO BELLA QUANTO LETALE{/size}\n\nOfelia ha preso sul serio un pretendente.\nUno solo. L'ultimo.{/cps}"
    return


################################################################################
## GOOD END POLY CAINO — Il contratto a tre
################################################################################

label ofelia_good_caino:
    scene bg corridoio_ceppo with fade
    show caino neutro at left with dissolve
    "Fuori dallo studio, nel corridoio del Ceppo, Caino aspetta con la schiena al muro e il registro sotto il braccio."
    caino "Sei uscit[fin] viv[fin]. Ottimo. Avevo preparato due versioni del necrologio: le archivio entrambe."
    show ofelia compiaciuta with dissolve
    ofelia "Mio padre ha bruciato la carta? No: l'ho bruciata io. Annotalo, Caino. La storia la scrive chi c'era."
    show caino sarcastico at left with qdiss
    caino "Annotato. Con un asterisco: «a fuoco, nel vino del Capo Famiglia». Il notaio piangerà."
    "Caino estrae una pergamena dal registro. Tre righe, tre spazi per la firma. Uno è già firmato, in una calligrafia minuta e ostinata."
    caino "Contratto a tre. Clausole: niente bugie, niente esclusive, niente sentimentalismi in pubblico."
    show ofelia imbarazzata with qdiss
    ofelia "La terza la violi tu per primo, Caino. Ti ho visto arrossire sulla Calà."
    show caino tenero at left with dissolve
    caino "...era il riverbero delle lanterne. Firma, [player_name]. Prima che cambi idea. O prima che la cambi lei."
    "Firmo. Ofelia firma per ultima, con un ghirigoro che occupa mezza pagina. Caino non protesta: la guarda come si guarda un bilancio in attivo."
    scene bg nero with fade
    centered "{cps=20}{size=+10}IL CONTRATTO A TRE{/size}\n\nTre firme, nessuna esclusiva.\nE nessuna intenzione di rescindere.{/cps}"
    return


################################################################################
## GOOD END POLY AEDE — Le figlie di Glauco (agrodolce)
################################################################################

label ofelia_good_aede:
    show aede neutra with dissolve
    "Aede guarda la lama nella propria mano. Poi la lascia cadere nella neve, dritta, come una piccola lapide."
    aede "Vent'anni di ordini. Il primo che rifiuto, lo rifiuto per te. Mio padre se ne farà una ragione."
    show ofelia neutra at left with qdiss
    ofelia "Se ne farà due, sorella. Ero qui per lo stesso motivo."
    show aede sorpresa with qdiss
    aede "Tu? Per [un_t] Novellin[fin]? Tu che scendi la Calà da sola da cinque anni?"
    ofelia "Per nostro padre. Qualcuno doveva dirgli di no, e tu eri lenta. Non farti idee."
    "Ofelia mente, con eleganza, senza guardarmi. Aede le crede: tra sorelle vince sempre la verità più comoda."
    show glauco neutro at right with dissolve
    "Glauco emerge dal bianco. Guarda le sue due figlie disarmate, ferme tra me e lui."
    glauco "Due figlie, due lame, un bersaglio solo. E nessuna delle due che colpisce. Ho educato benissimo, o malissimo."
    glauco "Cena al tramonto, [figlio_t] di Briseide. Siederai tra le mie figlie. Spero tu sappia tenere il coltello dalla parte giusta."
    hide glauco with dissolve
    scene bg cala_notte with fade
    show aede sorriso with dissolve
    "La cena è lunga. Aede ride, una volta, quando le verso il vino. Ofelia, dall'altro lato del tavolo, non ride mai."
    hide aede with dissolve
    show ofelia compiaciuta with dissolve
    "Dopo, sulla Calà spenta, Ofelia mi aspetta al primo gradino. Due minuti, non uno di più."
    ofelia "Lei ti ha alla luce. Io al buio. Non lamentarti: il buio mi dona."
    show ofelia imbarazzata with qdiss
    ofelia "Non dirglielo mai. Non per lei: per me. Non sopporterei di essere perdonata."
    scene bg nero with fade
    centered "{cps=20}{size=+10}LE FIGLIE DI GLAUCO{/size}\n\nDue lame, un solo bersaglio.\nUna sola lo sa.{/cps}"
    return


################################################################################
## BAD END — La tempesta
################################################################################

label ofelia_bad_tempesta:
    show aede neutra with dissolve
    "Aede guarda Ofelia. Poi guarda me. Il silenzio della neve si fa pesante come una lastra."
    if ofelia_mano_cala and ofelia_in_pubblico:
        aede "Sulla Calà. Sotto i miei occhi. E al mercato, a braccetto, come due sposi."
    elif ofelia_mano_cala:
        aede "Sulla Calà. Sotto i miei occhi. Mano nella mano, come vuole la leggenda."
    elif ofelia_in_pubblico:
        aede "Al mercato, a braccetto, come due sposi. Una ragazza del mio Ceppo vi ha visti. E non era la prima volta."
    else:
        aede "Me l'hanno detto. Le ancelle, le serve, i corridoi. Tutta Rocca Tempesta lo sa, e io per ultima."
    aede "Credevate che la lama migliore del Nord non sapesse contare fino a due?"
    show ofelia rabbia at left with qdiss
    ofelia "Sorella. Abbassa la lama. Non è [lui_t] che vuoi."
    show aede furia with lampo
    aede "No. Vi voglio entrambi. E per una volta, l'ordine di mio padre e il mio coincidono."
    with vpunch
    "Non vedo il colpo. Sento il freddo, e la voce di Ofelia che grida il mio nome. Non l'avevo mai sentita gridare."
    show glauco furioso at right with dissolve
    glauco "Basta. Le mie figlie non si sgozzano tra loro per [un_t] Novellin[fin]. Il conto lo chiudo io."
    scene bg nero with lampo
    "Il Margine, dicono gli Arvali, è un fiume lento. Lo attraverso con due nomi in gola, e non so quale dire per ultimo."
    "A Zefiro, dicono, le sorelle Severo non si parlano più. Una scende la Calà da sola. L'altra non la scende più."
    centered "{cps=20}{size=+10}LA TEMPESTA{/size}\n\nNon si ama una figlia di Glauco di nascosto.\nNon due volte.{/cps}"
    return


################################################################################
## NEUTRAL END — Interesse passeggero
################################################################################

label ofelia_neutral:
    show glauco neutro with qdiss
    glauco "Visto, figlia? Un bel gesto, la carta bruciata. Peccato per il pubblico."
    show ofelia neutra at left with qdiss
    ofelia "Hai ragione, padre. Per una volta."
    "Mi guarda come si guarda un vestito della stagione scorsa: bello, certo. Ma la stagione è finita."
    scene bg cala_notte with fade
    "Una Luna dopo, la vedo sulla Calà con un pretendente nuovo. Un Asi alto, i capelli in ordine, le frasi pronte."
    show ofelia compiaciuta with dissolve
    "Mi passa accanto senza fermarsi. Un cenno, il minimo sindacale della cortesia."
    ofelia "Sei stat[fin] un interesse piacevole, [player_name]. Passeggero, ma piacevole. Non tutti arrivano a tanto."
    scene bg nero with fade
    centered "{cps=20}{size=+10}INTERESSE PASSEGGERO{/size}\n\nOfelia scende la Calà ogni anno.\nQuest'anno, con qualcun altro.{/cps}"
    return
