# Route Aede — climax e finali.

################################################################################
## CLIMAX — Lo studio di Glauco
################################################################################

label climax:

    scene bg studio_glauco with fade

    show glauco neutro with dissolve

    "Lo studio è come lo ricordavo: silenzioso, ordinato, letale."

    glauco "Siediti, Figlio di Briseide. Il vino è buono. Bevilo adesso: dopo, uno di noi due non ne avrà più voglia."

    "Mi siedo. Non bevo."

    glauco "Mia figlia è l'opera della mia vita. L'ho raccolta che era un pugno di fame e rabbia, e ne ho fatto la lama perfetta del Nord."

    glauco "E tu, in una stagione, hai fatto ciò che vent'anni di disciplina avevano impedito: la lama ha cominciato a chiedersi perché taglia."

    show glauco minaccioso

    glauco "Una lama che si fa domande è una lama rotta. E le lame rotte, nel mio Ceppo, si rifondono."

    glauco "Perciò ho dato a mia figlia un ordine semplice. Il bersaglio sei tu. Stanotte, sotto le mura, lei salda il conto. Oppure non lo salda — e allora il conto lo saldo io, con entrambi."

    glauco "Vai pure, Figlio di Briseide. La neve stanotte è ottima per morire. O per vivere. Dipende interamente da ciò che avete costruito, tu e lei."

    scene bg esterno_neve with fade

    "Le mura esterne di Zefiro. La neve cade piatta, senza vento. Ogni passo scricchiola come un conto alla rovescia."

    show aede neutra with dissolve

    "È lì. Ferma nel bianco, il cappuccio abbassato, i capelli rossi come una ferita nella neve."

    aede "Ti ha detto tutto, vero? È il suo stile. Pulito."

    pc "Mi ha detto che il bersaglio sono io."

    aede "Il bersaglio sei tu."

    "La lama è già nella sua mano. Non l'ho vista estrarla. Non la vedo mai."

    menu:
        "La neve cade. Lei aspetta. Tutto quello che siamo stati si decide adesso."

        "Parlarle, un'ultima volta":
            pc "Qualunque cosa accada adesso, Aede: rifarei ogni gradino della Calà."

        "Restare in silenzio e guardarla negli occhi":
            "Non dico niente. Le parole, con lei, sono sempre state la moneta sbagliata. La guardo e basta, come al fondo della scala."

        "Tendere la mano, aperta":
            "Tendo la mano. Aperta, vuota, ferma nella neve. La stessa che le ho offerto sulla Calà."

    # Routing finali — ordine vincolante: good -> bad_glauco -> bad_aede -> neutral.
    if aede_affinity >= 12 and flag_giuramento and flag_accetta_lavoro:
        jump good_end
    elif not flag_segreto_svelo and aede_affinity < 6:
        jump bad_end_glauco
    elif aede_affinity < 6:
        jump bad_end_aede
    else:
        jump neutral_end

################################################################################
## GOOD END — La terza via
################################################################################

label good_end:

    show aede neutra with dissolve

    "Aede guarda la lama nella propria mano come se la vedesse per la prima volta."

    aede "Vent'anni di ordini eseguiti. Sai quante volte ho sbagliato un bersaglio, [player_name]?"

    pc "Una."

    show aede sorriso

    aede "Una. E non era un errore."

    "Apre le dita. La lama cade nella neve, dritta, e vi resta piantata come un piccolo monumento."

    show glauco minaccioso at left with dissolve

    "Glauco emerge dal bianco. Era lì da sempre, naturalmente."

    glauco "Disobbedienza."

    aede "Verità, padre. La tua lama perfetta sceglie il suo bersaglio: è questo che l'hai addestrata a fare. Scegliere meglio di chiunque."

    aede "E io scelgo lui. Davanti a te, davanti al Groviglio, davanti a ogni Asi che vorrà guardare. Se il Ceppo deve rifondermi, cominci stanotte."

    "Il silenzio dura una nevicata intera. Poi Glauco Severo fa la cosa più spaventosa che abbia mai fatto."

    show glauco neutro at left

    glauco "Vent'anni perché imparasse a disobbedirmi per qualcosa che vale. Era l'ultima lezione, figlia. L'unica che non potevo insegnarti io."

    glauco "Figlio di Briseide: la cena è al tramonto, alla tenuta del Ceppo. Non si rifiuta l'invito di Glauco Severo due volte."

    hide glauco with dissolve

    "Se ne va com'è venuto. La neve gli si richiude dietro."

    scene bg cala_notte with fade

    show aede sorriso with dissolve

    "Più tardi — molto più tardi — la Calà è spenta, la festa è lontana, i gradini sono solo gradini."

    "Li scendiamo lo stesso. Mano nella mano, dal primo all'ultimo."

    aede "Lo sai che la leggenda vale solo la notte della Fiaccolata, vero? Stanotte non conta."

    pc "Allora torniamo alla prossima Fiaccolata."

    aede "...idiota."

    "Ma le sue dita stringono le mie. E il Nord, per una volta, non ci chiede niente."

    scene bg nero with fade

    centered "{size=+10}FINE{/size}\n\nAede ha scelto il suo bersaglio.\nPer sempre."

    return

################################################################################
## NEUTRAL END — L'inganno
################################################################################

label neutral_end:

    show aede neutra with dissolve

    aede "Mio padre vuole un saldo. E avrà un saldo."

    "Si muove prima che io possa rispondere. Il pomo della lama — non il filo — mi prende alla tempia. Il mondo diventa neve."

    scene bg nero with fade

    "Mi sveglio su un carro di lane, fuori dalle mura, con un bernoccolo epico e una lettera cucita nel mantello."

    "{i}«Per mio padre sei morto congelato nel fosso, e il fosso non si controlla. È il migliore dei miei lavori: il primo bersaglio sbagliato di proposito.{/i}"

    "{i}Non tornare a cercarmi. Ma se un giorno una lama ti salva la vita da un tetto di Zefiro, non chiederti di chi è.{/i}"

    "{i}L'amica che non hai mai avuto. — A.»{/i}"

    scene bg vicoli_zefiro with fade

    "Torno alla mia tenuta per vie lunghe. Briseide non fa domande: sa già, come sempre."

    "E negli anni, ogni tanto, una moneta della Lega con un graffio a forma di volpe compare sul mio davanzale. Nessun biglietto. Nessuna firma."

    "Non serve. So di chi è la mano. La più veloce del Nord."

    scene bg nero with fade

    centered "{size=+10}FINE{/size}\n\nNon tutti i debiti si saldano col sangue.\nAlcuni si saldano con l'assenza."

    return

################################################################################
## BAD END — La lama di Aede
################################################################################

label bad_end_aede:

    show aede neutra with dissolve

    aede "Sai qual è la differenza tra te e tutti gli altri bersagli, [player_name]?"

    "La neve scricchiola. Un passo. Non vedo la lama. Non la vedo mai."

    aede "Nessuna. È questo che non hai mai capito."

    "Freddo sotto il mento. Come la prima notte, allo Svelo. Il cerchio si chiude."

    show aede furia

    aede "Dovevi guardare, ascoltare e non farti notare. Te l'avevano detto."

    scene bg nero with fade

    "Il Margine, dicono gli Arvali, è un fiume lento. I Dignitas meritevoli lo attraversano verso Drakengrad, la sala del Leone, dove ogni storia viene raccontata per sempre."

    "Chissà se qualcuno, laggiù, racconterà la mia: la storia del novellino che amò la lama, e la lama saldò il conto."

    centered "{size=+10}FINE{/size}\n\nIl Nord non perdona.\nLei meno di tutti."

    return

################################################################################
## BAD END — La mano di Glauco
################################################################################

label bad_end_glauco:

    show aede neutra with dissolve

    "Aede non si muove. La lama le pende dalla mano come un pensiero incompiuto."

    aede "Non ci riesco."

    "Lo dice piano, stupita di se stessa. E nella neve alle mie spalle, una voce pesata come oro contato:"

    show glauco minaccioso at left with dissolve

    glauco "Lo sapevo prima di darle l'ordine, Figlio di Briseide. Era l'ultima verifica, e l'avete fallita entrambi."

    glauco "Mia figlia non commette errori. Quando li commette, li erediti tu."

    "Non vedo il gesto. Con lui non lo vede nessuno."

    scene bg nero with fade

    "L'ultima cosa che sento è la voce di lei che urla il mio nome — il mio Primo Nome, quello vero, l'unico che ho."

    "Gli Arvali dicono che chi muore nella neve attraversa il Margine senza freddo. Mentono. Ma è un freddo breve."

    "E a Drakengrad, nella sala del Leone, c'è un posto anche per le storie finite male. Il Nord le preferisce: insegnano meglio."

    centered "{size=+10}FINE{/size}\n\n«Chi minaccia me, parla con lui.\nE nessuno parla con lui due volte.»"

    return
