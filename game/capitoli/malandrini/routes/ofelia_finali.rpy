# Route Ofelia — climax e finali (anche poly con Caino e con Aede).
# Il dispatch del climax e' in snodi.rpy (ev_luna6).

################################################################################
## CLIMAX — Lo studio di Glauco, la figlia imprevedibile
################################################################################

label ofelia_climax:
    scene bg studio_glauco with fade
    show glauco neutro with dissolve
    "Lo studio di Glauco Severo. Silenzio, ordine, una candela sola. Il vino è già versato in due calici."
    glauco "Siediti, [figlio_t] di Briseide. Mia figlia dice che sei un capriccio. Io conto i capricci: questo dura da troppe Lune."
    show ofelia neutra at left with dissolve
    "Ofelia è in piedi accanto alla finestra, in nero. Non mi guarda. Tiene gli occhi sulla candela e non sbatte le palpebre."
    glauco "Ofelia è la mia figlia imprevedibile. Al punto giusto: l'ho cresciuta così. Ogni anno tre pretendenti, ogni anno nessuno."
    show glauco minaccioso with qdiss
    glauco "Stanotte firmi la rinuncia e torni da tua madre con un dono del Ceppo. Oppure non firmi, e il dono te lo porto io."
    "La pergamena è sul tavolo, la penna accanto, già intinta. Glauco non lascia mai niente a metà."
    glauco "Ascadeo ha scommesso su di te, sai? Contro sua sorella. Lo farò frustare per questo, o forse lo farò ricco. Dipende da come esci di qui."
    "Sulla parete alle sue spalle, le lame sono trentadue. Tutte affilate, tutte parallele. Glauco non si chiede mai chi le curi."
    "Ofelia non si muove. Il silenzio è suo: lo lascia crescere finché diventa una stanza dentro la stanza."
    "La penna gocciola sul legno. Glauco aspetta me, non lei."
    # La scelta viene prima del fuoco: il gesto del protagonista decide come
    # la carta brucia (insieme, accanto, o contro di lei).
    menu:
        "La pergamena è a un palmo dalla mia mano. La candela, a un palmo da quella di Ofelia."
        "Prendere la pergamena e porgerla a Ofelia, dal lato della candela" (peso=True):
            $ ofelia_affinity += 1
            $ ofelia_climax_gesto = "insieme"
            "Prendo la carta. Non la guardo nemmeno: la tendo verso la finestra, con l'angolo già sopra la fiamma."
            show ofelia compiaciuta at left with qdiss
            "Ofelia chiude due dita sull'altro angolo. Per un istante la teniamo in due."
            ofelia "Padre. Hai dimenticato una clausola."
        "Rispondere a Glauco a testa alta: «Non firmo. Resta lei, e resto io.»" (peso=True):
            $ ofelia_climax_gesto = "accanto"
            glauco "Coraggio. Il difetto preferito di chi muore giovane."
            show ofelia compiaciuta at left with qdiss
            ofelia "Elegante. Un po' troppo coraggios[fin] per i miei gusti. Ma il tono era giusto."
            ofelia "Padre. Hai dimenticato una clausola."
            "Prende la pergamena e la avvicina alla candela, senza fretta, tenendola per un angolo."
        "Prendere le sue difese: «Non decidete voi per lei.»" (peso=True):
            $ ofelia_affinity -= 1
            $ ofelia_climax_gesto = "contro"
            show ofelia rabbia at left with qdiss
            ofelia "Non mi serve un avvocato, [player_name]. Le mie carte le brucio da sola."
            "Mi strappa la pergamena di mano prima che io capisca di averla presa."
    show glauco furioso
    with vpunch
    "La carta prende fuoco. Ofelia la lascia cadere nel calice di suo padre, e il vino sfrigola."
    ofelia "Non scelgo pretendenti da un catalogo, padre. Li scelgo come tu scegli le lame: da come reggono il colpo."
    if ofelia_climax_gesto == "contro":
        ofelia "Questo deve ancora imparare a non pararmi i colpi. I tuoi non ci hanno nemmeno provato."
    else:
        ofelia "Questo l'ha retto. I tuoi, no."
    ofelia "Me ne hai mandati sei, padre, in sei anni. Il sonetto, il cavallo, l'uomo con l'anello. Tutti col tuo sigillo addosso, come le pecore."
    show glauco minaccioso with qdiss
    glauco "Erano alleanze. Tu li hai trattati come pretendenti."
    ofelia "E tu li hai trattati come pegni. Almeno io li guardavo in faccia, quando dicevo di no."
    if route_seconda_viva() == "caino":
        ofelia "E sì, c'è un altro contraente. Lo sai già: tieni registri migliori dei suoi. Si firma in tre, o non firma nessuno."
    show glauco deluso with qdiss
    glauco "Mi sfidi. In casa mia. Per [lui_t]."
    ofelia "Ti sorprendo, padre. È diverso. L'hai insegnato tu: un colpo che si vede arrivare non è un colpo."
    "Glauco mi guarda. Non più come un conto da saldare: come una voce che non torna nel bilancio."
    if ofelia_climax_gesto == "insieme":
        "Ofelia sposta il calice di un dito, verso di me. Nel vino galleggia ancora un angolo di carta, annerito dalla parte che tenevo io."
        glauco "L'avete bruciata in due. Il notaio dovrà inventarsi una formula."
    elif ofelia_climax_gesto == "accanto":
        glauco "Vedremo quanto dura, il tono giusto."
    else:
        show ofelia rabbia at left with qdiss
        ofelia "Difendimi ancora, e la prossima pergamena la firmo io. Contro di te."
        glauco "Vedi, figlia? Non ti conosce nemmeno [lui_t]."
    jump ofelia_routing

label ofelia_routing:
    # rl.finale_ofelia — ordine vincolante: ofelia_good_caino -> ofelia_good
    # -> ofelia_passeggero -> ofelia_bad -> ofelia_neutral.
    $ cal_finale = rl.finale_ofelia(ofelia_affinity, ofelia_mancati,
                                    route_seconda_viva(), caino_fiducia)
    jump expression cal_finale


################################################################################
## ROUTING POLY AEDE — innestato nel climax di Aede (aede_finali.rpy)
################################################################################

label ofelia_poly_aede_routing:
    # rl.finale_ofelia_poly_aede — ordine vincolante: ofelia_bad_tempesta ->
    # ofelia_good_aede -> ofelia_good (coda amara) -> routing di Aede
    # (rl.finale_aede: good_end, bad_end_glauco, bad_end_aede, neutral_end).
    $ cal_finale = rl.finale_ofelia_poly_aede(
        aede_sospetto, ofelia_affinity, ofelia_mancati, aede_affinity,
        flag_giuramento, flag_accetta_lavoro, flag_segreto_svelo)
    if cal_finale in rl.OFELIA_POLY_AEDE:
        jump expression cal_finale
    # Finali di Aede: Ofelia esce di scena prima (i finali usano glauco at left).
    "Ofelia mi guarda un'ultima volta, poi arretra nel bianco. La neve si richiude su di lei senza un rumore."
    hide ofelia with dissolve
    jump expression cal_finale


################################################################################
## GOOD END — Tanto bella quanto letale (coda amara se il poly non regge)
################################################################################

label ofelia_good:
    $ lento()
    # Prologo solo se arriviamo dal climax di Aede (neve); la coda resta su route_seconda.
    if route_seconda_viva() == "aede":
        show aede neutra with dissolve
        "Aede guarda la lama, poi guarda me. Poi guarda sua sorella, che non si è mossa di un passo."
        aede "Mio padre voleva un saldo. Non l'avrà. Non per te, [player_name]: per lei, che non mi ha mai chiesto niente."
        "Rinfodera. Si volta e se ne va nella neve, senza fretta. Non si gira."
        hide aede with dissolve
    scene bg cala_notte with fade
    $ lento()
    show ofelia neutra with dissolve
    "Più tardi, la Calà è spenta. Trecento gradini al buio: nessuna lanterna, nessuna leggenda a garantire niente."
    ofelia "Sai cosa dicono di me a Zefiro? Che sono bella. Sbagliano l'ordine: prima sono letale. La bellezza è un dettaglio."
    pc "Allora ho corso un rischio."
    show ofelia compiaciuta with qdiss
    ofelia "Il più grosso della tua vita. Te lo ricorderò ogni giorno. È il mio modo di essere affettuosa."
    "Mi tende la mano. Non col palmo in giù, stavolta: aperta, alla pari."
    show ofelia imbarazzata with dissolve
    if route_seconda == "aede":
        ofelia "Niente di sdolcinato, non chiederlo. E niente cene da mio padre, per un po'."
        ofelia "Mia sorella ha rinfoderato, stanotte. Le devo almeno questo: non sedermi accanto a te davanti a lei. Il Ceppo aspetterà."
    else:
        ofelia "Niente di sdolcinato, non chiederlo. Ma domani a cena da mio padre mi siedo accanto a te."
        ofelia "Davanti a tutto il Ceppo. Per me è come scriverlo sulle mura."
    ofelia "Ascadeo ha vinto la sua scommessa più grossa, comunque. Non dirgli niente: voglio che me lo chieda lui. Voglio vederlo pagare il disturbo."
    "Scendiamo al buio, mano nella mano. Al centesimo gradino lei ride piano, una volta sola. Non lo ammetterà mai."
    "A metà della scala si ferma. Si toglie un guanto e me lo mette in tasca, senza spiegare. È lo stesso che faceva raccogliere ai pretendenti."
    ofelia "Non lo lascerò cadere più. Non ce n'è bisogno."
    "Poi fa la cosa che la sera delle forbici non ha fatto. Mi bacia: breve, a occhi aperti, come chi vuole vedere cosa succede."
    ofelia "Quella sera ti ho fatto aspettare. Volevo sapere se aspettavi."
    ofelia "Hai aspettato. Non abituarti."
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
    $ sblocca_finale("ofelia_good")
    with lampo_oro
    centered "{cps=20}{size=+10}TANTO BELLA QUANTO LETALE{/size}\n\nOfelia ha preso sul serio un pretendente.\nUno solo. L'ultimo.{/cps}"
    return


################################################################################
## GOOD END POLY CAINO — Il contratto a tre
################################################################################

label ofelia_good_caino:
    $ lento()
    scene bg corridoio_ceppo with fade
    $ lento()
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
    ofelia "Aggiungi una clausola, Caino. La quarta. Chi tradisce il contratto, lo dice a me prima che agli altri due."
    show caino neutro at left with qdiss
    caino "E poi?"
    ofelia "E poi niente. Lo dice a me. Il resto si vede."
    "Firmo. Ofelia firma per ultima, con un ghirigoro che occupa mezza pagina. Caino non protesta. Annota l'ora della firma, poi la sottolinea due volte."
    "Sotto le firme, in piccolo, Caino aggiunge una data e un'ora. Come se un giorno qualcuno dovesse verificare che è successo davvero."
    scene bg nero with fade
    $ sblocca_finale("ofelia_good_caino")
    with lampo_oro
    centered "{cps=20}{size=+10}IL CONTRATTO A TRE{/size}\n\nTre firme, nessuna esclusiva.\nE nessuna intenzione di rescindere.{/cps}"
    return


################################################################################
## GOOD END POLY AEDE — Le figlie di Glauco (agrodolce)
################################################################################

label ofelia_good_aede:
    $ lento()
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
    $ lento()
    show aede sorriso with dissolve
    "La cena è lunga. Aede ride, una volta, quando le verso il vino. Ofelia, dall'altro lato del tavolo, non ride mai."
    "C'è anche Ascadeo, a capotavola accanto al padre. Mi guarda, guarda le sorelle, e conta qualcosa sulle dita sotto la tovaglia."
    "A fine cena mi passa accanto e mi sussurra una cifra. Non capisco se è una vincita o un avvertimento. Forse tutte e due."
    hide aede with dissolve
    show ofelia compiaciuta with dissolve
    "Dopo, sulla Calà spenta, Ofelia mi aspetta al primo gradino. Due minuti, non uno di più."
    ofelia "Lei ti ha alla luce. Io al buio. Non lamentarti: il buio mi dona."
    show ofelia imbarazzata with qdiss
    ofelia "Non dirglielo mai. Non per lei: per me. Non sopporterei di essere perdonata."
    "Mi bacia una volta, sulla tempia, di fretta. Poi sale i gradini al contrario, verso la luce del Ceppo, senza voltarsi."
    scene bg nero with fade
    $ sblocca_finale("ofelia_good_aede")
    with lampo_oro
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
    aede "Hai sempre preso il nero, Ofelia. Lasciavi a me il rosso, e io ti ringraziavo. Che stupida."
    ofelia "Non ti ho mai tolto niente che tu avessi già."
    aede "Questa la conservo. È la più crudele che tu abbia mai detto."
    show aede furia with lampo
    aede "No. Vi voglio entrambi. E per una volta, l'ordine di mio padre e il mio coincidono."
    with vpunch
    "Non vedo il colpo. Sento il freddo, e la voce di Ofelia che grida il mio nome. Non l'avevo mai sentita gridare."
    show glauco furioso at right with dissolve
    glauco "Basta. Le mie figlie non si sgozzano tra loro per [un_t] Novellin[fin]. Il conto lo chiudo io."
    scene bg nero with lampo
    "Il Margine, dicono gli Arvali, è un fiume lento. Lo attraverso con due nomi in gola, e non so quale dire per ultimo."
    "A Zefiro, dicono, le sorelle Severo non si parlano più. Una scende la Calà da sola. L'altra non la scende più."
    $ sblocca_finale("ofelia_bad_tempesta")
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
    "Mi guarda dall'alto in basso, con calma, e arriva alle scarpe. Lì si ferma."
    ofelia "Ti ho dato sei Lune, [player_name]. Ne hai usate metà. Io non aspetto: non per crudeltà, per abitudine."
    "Raccoglie la cenere della pergamena dal fondo del calice e la sparge sul tavolo con un dito. Un gesto da bambina annoiata."
    glauco "Va', [figlio_t] di Briseide. Il dono del Ceppo te lo risparmio. Mia figlia ti ha già fatto il suo."
    scene bg cala_notte with fade
    "Una Luna dopo, la vedo sulla Calà con un pretendente nuovo. Un Asi alto, i capelli in ordine, le frasi pronte."
    show ofelia compiaciuta with dissolve
    "Mi passa accanto senza fermarsi. Un cenno, il minimo sindacale della cortesia."
    ofelia "Sei stat[fin] un interesse piacevole, [player_name]. Passeggero, ma piacevole. Non tutti arrivano a tanto."
    "Il pretendente nuovo mi guarda di sbieco, cercando di capire chi sono. Lei non glielo dice. Non vale la spesa."
    "Ai piedi della scala c'è un ragazzo che prende appunti su un libretto. Ascadeo, credo. Accanto al mio nome tira una riga."
    scene bg nero with fade
    $ sblocca_finale("ofelia_neutral")
    centered "{cps=20}{size=+10}INTERESSE PASSEGGERO{/size}\n\nOfelia scende la Calà ogni anno.\nQuest'anno, con qualcun altro.{/cps}"
    return


################################################################################
## PASSEGGERO — Il guanto a terra (affinita' da good, un invito mancato)
################################################################################

label ofelia_passeggero:
    show glauco neutro with qdiss
    glauco "La carta è cenere, il vino è da buttare. Il resto è affar tuo, figlia."
    hide glauco with dissolve
    "Glauco esce e lascia la porta aperta. Nel Ceppo le porte chiuse le decide lui."
    show ofelia neutra at left with qdiss
    "Ofelia resta alla finestra. Conta qualcosa sulle dita, senza fretta. Arriva a uno e si ferma."
    ofelia "Una sera, [player_name]. Ti avevo lasciato una sedia. È rimasta vuota fino a mezzanotte."
    pc "Ero..."
    ofelia "Non mi interessa dov'eri. Mi interessa che io me lo ricordo, e tu no."
    "Si sfila un guanto. Lo tiene sospeso sopra il tavolo un momento, poi lo lascia cadere tra noi."
    ofelia "Raccoglilo, se vuoi. Stavolta non è una prova. È un saluto."
    if route_seconda_viva() == "caino":
        "Nel corridoio Caino scrive una riga nel registro. Non alza la testa quando passo."
    scene bg cala_notte with fade
    "Il guanto resta nella mia tasca per tutto l'inverno. Sulla Calà Ofelia mi saluta con un cenno preciso: né freddo né caldo. Esatto."
    "A fine Luna Ascadeo mi offre da bere. Ha vinto metà della scommessa, dice. Non mi spiega quale metà."
    scene bg nero with fade
    $ sblocca_finale("ofelia_passeggero")
    centered "{cps=20}{size=+10}IL GUANTO A TERRA{/size}\n\nOfelia non aspetta due volte.\nAspetta una volta sola, e se lo ricorda.{/cps}"
    return


################################################################################
## BAD END — Il dono del Ceppo (sotto la soglia del cuore a fine route)
################################################################################

label ofelia_bad:
    show ofelia neutra at left with qdiss
    "Ofelia posa il calice. Il vino ha smesso di sfrigolare."
    ofelia "La carta l'ho bruciata per me, padre. Non per [lui_t]. Non confondere i conti."
    show glauco minaccioso with qdiss
    glauco "Allora i conti li chiudo io."
    "Glauco stacca dalla parete una lama che non avevo contato: la trentatreesima, sotto un panno. La avvolge in un drappo col fiocco del Ceppo."
    glauco "Il dono che ti avevo promesso, [figlio_t] di Briseide. Portalo a tua madre. Dille che il Ceppo ringrazia per la visita."
    glauco "E dille che il prossimo lo porto io. Senza drappo."
    "Cerco gli occhi di Ofelia. Lei guarda la candela, e la spegne con due dita. Un sibilo. Nessuna smorfia."
    ofelia "Vai, [player_name]. Prima dell'alba. Mio padre è puntuale solo con le minacce."
    scene bg vicoli_zefiro with fade
    "Lascio Zefiro col primo carro. Il drappo sul sedile accanto, il fiocco del Ceppo bene in vista: chi ci ferma sa di chi è il debito."
    "Nessuno ci ferma."
    scene bg nero with fade
    $ sblocca_finale("ofelia_bad")
    centered "{cps=20}{size=+10}IL DONO DEL CEPPO{/size}\n\nGlauco mantiene sempre le promesse.\nSoprattutto quelle che nessuno vuole.{/cps}"
    return
