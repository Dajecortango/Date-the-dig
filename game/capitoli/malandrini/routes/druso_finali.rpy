# Route Druso — climax e finali.

## Climax e finali ###########################################################

label druso_climax:
    scene bg consiglio with fade
    "Convocazione del Ramo di Lenora. Sala lunga, banchi di quercia, gli Arconti in fila come corvi su un ramo."
    "Il freddo della pietra sale dalle suole. Le torce bruciano basse, come se anche loro avessero paura di disturbare."
    "L'accusa la legge un Eparca, con la voce di chi recita un inventario."
    "Il secondogenito della Capofamiglia «frequenta [un_t] Figli[fin] di Briseide oltre il decoro»."
    if flag_druso_coraggio:
        "E ha fatto a botte nei vicoli per un lanternaio."
    else:
        "E compone versi che nessun Ramo dovrebbe sentire, in locali che nessun Ramo dovrebbe frequentare."
    if "druso_luna5" in eventi_visti:
        "E ha perso una sfida di versi contro Iperione. O l'ha vinta male, che per il Ramo è peggio."
    "Sul banco dei familiari, Caino siede immobile. Icaro, accanto, si studia le unghie con grande attenzione."
    show druso serio at left with dissolve
    "Druso è in piedi al centro. Niente boccale, niente pubblico amico."
    "Lenora non si vede. Siede dietro la grata in fondo alla sala, e la sala intera respira al suo ritmo."
    "Una voce, da dietro la grata. Bassa, senza fretta."
    "«Druso. Ti ascolto.»"
    show druso sorpreso with qdiss
    "Lui apre la bocca. La richiude. Le mani cercano un boccale che non c'è."
    "Poi i suoi occhi trovano i miei, in fondo, tra i Figli messi lì dove non fanno danni."
    menu:
        "Il silenzio dura un respiro di troppo. Tutti aspettano."
        "Alzarmi e parlare per lui" (peso=True):
            $ druso_consiglio = "parla"
            with vpunch
            if flag_druso_coraggio:
                pc "Il lanternaio l'ho difeso io. Druso è venuto dietro. Se c'è una colpa, è mia."
            else:
                pc "Se c'è una colpa, è anche mia."
            "Un mormorio tra i banchi. L'Eparca segna qualcosa."
            show druso irritato with qdiss
            druso "...nessuno ti ha chiesto di fare il cavaliere. Siediti."
            "Lo dice piano, a denti stretti. Ma adesso la sala guarda me, non lui."
        "Restare sedut[fin], e guardarlo. La voce è sua" (peso=True):
            $ druso_consiglio = "lascia"
            $ druso_affinity += 1
            if druso_sfida == "silenzio":
                "Non mi muovo. Lo guardo e basta, come al tavolo di Lisandro."
            else:
                "Non mi muovo. Lo guardo e basta."
            show druso serio with qdiss
            "Druso capisce. Raddrizza le spalle. Cento chili di poeta, tutti in piedi."
            druso "Madre. Ho la gola secca e niente da bere. Parlerò lo stesso."
        "Smontare la cosa con una battuta" (peso=True):
            $ druso_consiglio = "battuta"
            $ druso_affinity += 1
            pc "Oltre il decoro? Eccellenza, il decoro l'ha superato da anni. Io sono solo l'ultima tappa."
            with hpunch
            "Un Arconte tossisce per non ridere. Un altro non ci riesce."
            show druso ghigno with qdiss
            "Druso si volta verso di me. Il ghigno gli torna in faccia come una bandiera."
            druso "Sentito, madre? Mi hanno rubato la battuta. Allora la seconda la dico io."
    "La grata tace. Aspetta il verdetto, e il verdetto adesso tocca a lui."
    # Routing (rl.finale_druso): druso_good -> druso_passeggero ->
    # druso_neutral -> druso_bad.
    $ cal_finale = rl.finale_druso(druso_affinity, flag_druso_coraggio)
    jump expression cal_finale

label druso_good:
    $ lento()
    show druso ghigno at left with qdiss
    druso "Confermo tutto, madre. Il decoro, la rissa, [il_t] Figli[fin] di Briseide. E aggiungo un componimento in tema, se il Consiglio gradisce. Rima baciata."
    "Un Eparca si alza per protestare. Caino, senza voltarsi, gli posa una mano sul braccio. L'Eparca si risiede."
    "Lo recita. Davanti a Lenora, agli Arconti, al Nord intero. Il poema non osceno. Il mio."
    "Dentro ci sono cose che sappiamo solo noi due. Nessuno in sala capisce. Io sì."
    "La sala non ride. La sala — che gli Asi la conservino — applaude."
    "Da dietro la grata, una sola parola: «Bis.»"
    show druso sorpreso with qdiss
    "Druso resta a bocca aperta. Si gira verso di me e muove le labbra, senza voce: «e adesso?»"
    "Icaro, accanto a Caino, mormora qualcosa. Dal labiale sembra «ho perso un'altra scommessa». Sembra felice."
    scene bg cala_notte with fade
    $ lento()
    show druso ghigno at left with dissolve
    druso "Hai sentito? Pubblico nuovo. Il migliore. E tutto grazie al mio talento, ovviamente."
    pc "Ovviamente."
    if druso_consiglio == "parla":
        druso "E la prossima volta che ti alzi a fare il cavaliere, ti lego alla panca. Con affetto. Con molto affetto."
    elif druso_consiglio == "battuta":
        druso "Quella sul decoro te la rubo. La metto in un poema. Tu ci metti la faccia, io la metrica."
    else:
        druso "Sei rimast[fin] sedut[fin]. Tutto il tempo. Sai quanto costa, a uno come me, sapere che qualcuno aspetta e basta?"
    "Scendiamo i gradini della Calà a passo lento. Al duecentesimo si ferma."
    show druso imbarazzato with dissolve
    druso "...e a te. Ma questo è fuori metrica."
    "Da quella sera Zefiro ha un poeta nuovo. Stesso uomo, stessa barba. Le rime oscene restano."
    "Ma alla fine di ogni serata, a voce bassa, ce n'è una che non lo è. Ed è per me."
    scene bg nero with fade
    $ sblocca_finale("druso_good")
    with lampo_oro
    centered "{cps=20}{size=+10}IL CUORE PROVOCATORE{/size}\n\nIl poema più bello non nasce dall'immaginazione.\nSi ispira alla realtà.{/cps}"
    return

label druso_neutral:
    show druso ghigno at left with qdiss
    druso "Frequentazione? Madre, io frequento TUTTI. È il mio pubblico. [Il_t] Figli[fin] di Briseide regge bene le mie rime, tutto qui."
    "Ne esce con una battuta, come sempre. Mentre la dice, non mi guarda nemmeno una volta."
    "Gli Arconti sorridono, sollevati. Un figlio che scherza è un figlio che non morde."
    if druso_consiglio == "parla":
        "Della mia difesa non dice niente. Mi passa accanto all'uscita e mi sistema il mantello, senza guardarmi."
    elif druso_consiglio == "battuta":
        "La mia battuta la ripete in taverna per settimane. La firma lui, naturalmente."
    else:
        "Io sono rimast[fin] sedut[fin]. Lui ha parlato. Solo che non ha detto la cosa che stavamo aspettando tutti e due."
    "La grata tace. Lenora non chiede altro. Il Consiglio archivia: un figlio rumoroso, niente di nuovo."
    scene bg vicoli_zefiro with fade
    show druso neutro at left with dissolve
    "Restiamo quello che eravamo: il poeta e la sua spalla. In taverna, ogni sera, il posto accanto al suo è mio."
    druso "Brindisi! Alla mia spalla, che regge tutto. Tranne la mia poesia."
    "La sala ride. Io pure. Nessuno dei due chiede di più, ad alta voce."
    "Il foglio piegato in quattro, quello delle tre notti, non lo vedo più. Forse l'ha bruciato. Forse lo tiene in tasca."
    "A volte, a fine serata, mi guarda come se avesse una strofa in gola. Poi ordina un altro giro."
    scene bg nero with fade
    $ sblocca_finale("druso_neutral")
    centered "{cps=20}{size=+10}IL POSTO ACCANTO{/size}\n\nOgni poeta ha una spalla.\nNon ogni poema ha un finale.{/cps}"
    return

label druso_bad:
    show druso serio at left with qdiss
    druso "Chi? Quell[fin]? Madre, ti prego. Un cane che abbaia, al mio seguito. Il pubblico non si sceglie."
    "Lo dice guardandomi. E il ghigno, stavolta, non arriva agli occhi."
    if druso_consiglio == "parla":
        druso "E se parla per me, è perché non ha niente da dire per sé."
    "Gli Arconti ridono. È la risata che lui voleva, e la paga con me."
    "Da dietro la grata, Lenora non dice niente. Non serve."
    "All'uscita Caino mi passa accanto senza fermarsi. Dice solo: «Mio fratello sceglie sempre la risata. Io non mi ci sono mai abituato.»"
    scene bg vicoli_zefiro with fade
    "In taverna il mio posto accanto al suo lo prende qualcun altro. Poi un altro ancora."
    "Da quella sera le sue provocazioni tornano a essere solo crudeli, e io torno a essere solo pubblico."
    if "druso_luna5" in eventi_visti:
        "Una volta, tardi, lo sento recitare la strofa di Lisandro. Quella sui cento chili. La dice lui, su di sé, e la sala applaude."
    "Il gioco crudo e duro ha dato il suo verdetto: non l'ho retto."
    scene bg nero with fade
    $ sblocca_finale("druso_bad")
    centered "{cps=20}{size=+10}IL CANE CHE ABBAIA{/size}\n\nDruso testa le acque di tutti.\nNon tutti galleggiano.{/cps}"
    return

## Finale passeggero — La rima che manca ######################################

label druso_passeggero:
    $ lento()
    show druso serio at left with qdiss
    druso "Madre. [Il_t] Figli[fin] di Briseide mi è car[fin]. Lo dico davanti al Consiglio, e senza rima."
    "Lo dice bene. Pulito, coraggioso. Una frase sola, e la sala la sente tutta."
    "La grata tace, poi archivia. Un figlio che ha detto una cosa vera: per una volta basta."
    scene bg vicoli_zefiro with fade
    $ lento()
    show druso neutro at left with dissolve
    druso "Ti voglio bene, lo sai. Te l'ho appena detto a mezzo Nord."
    if "druso_ev3" in eventi_visti:
        druso "Ma quando c'era da sporcarsi le mani, nei vicoli, col lanternaio, tu guardavi. Mi è piaciuto, il tuo sguardo. Non mi è bastato."
    else:
        druso "Ma quando c'era da rischiare sul serio, tu eri sempre un passo indietro. A guardare. Mi è piaciuto, il tuo sguardo. Non mi è bastato."
    if druso_consiglio == "parla":
        druso "E stanotte ti sei alzat[fin] a parlare per me. Proprio quando, per una volta, toccava a me."
    druso "A me serve uno che si butta nel FOSSO prima che io arrivi alla rima. Tu aspetti la chiusa, col fazzoletto in mano. Brav[fin]. Noios[fin]. Car[fin]."
    "Ride, per non lasciare la frase nuda. Mi dà una pacca sulla spalla. Pesa come tutte le sue pacche, e non di più."
    scene bg vicoli_zefiro with fade
    $ lento()
    "Una Luna dopo, in taverna, Druso legge un componimento serio. La sala tace, il che in taverna è un miracolo."
    show druso imbarazzato at left with dissolve
    "A metà alza gli occhi. Non verso di me: verso il fondo, dove Pandora tiene il registro aperto sul braccio e finge di non ascoltare."
    "Finisce. Applausi. Mi cerca, mi fa l'occhiolino da vecchio amico, e torna a guardare lei."
    show icaro furbo with dissolve
    icaro "Scommessa vinta. Avevo dato Pandora a tre contro uno. Non prenderla sul personale: i miei quaderni non hanno una colonna per le persone gentili."
    scene bg nero with fade
    $ sblocca_finale("druso_passeggero")
    centered "{cps=20}{size=+10}LA RIMA CHE MANCA{/size}\n\nDruso ti ha voluto bene ad alta voce.\nIl poema, l'ha scritto per un'altra.{/cps}"
    return
