# Attività quotidiane del semestre — scene territorio una-tantum (pool).
# Regola: ±1 affinità a scena, mai ripetibili coi punti (anti-grind).

define icaro = Character("Icaro", color="#7fa06a", image="icaro")

init python:
    ATTIVITA["mattina"].extend([
        ("spada", "Addestramento di spada", "aede",
         ["att_spada_1", "att_spada_2", "att_spada_3", "att_spada_4"]),
        ("scudo", "Palestra: scudo e lotta", "druso",
         ["att_scudo_1", "att_scudo_2", "att_scudo_3", "att_scudo_4"]),
        ("studio", "Studio della storia della Famiglia", None,
         ["att_studio_1", "att_studio_2", "att_studio_3", "att_studio_4"]),
    ])
    ATTIVITA["pomeriggio"].extend([
        ("spada_p", "Addestramento di spada", "aede",
         ["att_spada_1", "att_spada_2", "att_spada_3", "att_spada_4"]),
        ("riti", "I riti del Ceppo di Briseide", None,
         ["att_riti_1", "att_riti_2", "att_riti_3", "att_riti_4"]),
        ("citta", "Commissioni in città", None,
         ["att_citta_1", "att_citta_2", "att_citta_3"]),
        ("studio_p", "Studio della storia della Famiglia", None,
         ["att_studio_1", "att_studio_2", "att_studio_3", "att_studio_4"]),
    ])
    ATTIVITA["sera"].extend([
        ("taverna", "Una sera alla taverna", "druso",
         ["att_taverna_1", "att_taverna_2", "att_taverna_3", "att_taverna_4"]),
        ("fumeria", "La sala da gioco e la fumeria", "icaro",
         ["att_fumeria_1", "att_fumeria_2", "att_fumeria_3", "att_fumeria_4"]),
    ])


## Spada — territorio di Aede ################################################

label att_spada_1:
    scene bg palestra with fade
    show aede neutra with dissolve
    "Il cortile d'armi all'alba. Aede è già lì, ovviamente: dicono che il maestro d'armi le abbia ceduto il turno dei novellini per disperazione."
    aede "Guardia alta. No, più alta. Il Nord non colpisce dove guardi: colpisce dove respiri."
    menu:
        "Il legno della spada da esercizio pesa più del previsto."
        "Eseguire senza discutere, fino a sbagliare di meno":
            $ aede_affinity += 1
            show aede neutra with qdiss
            aede "Meno peggio. Domani di nuovo, finché «meno peggio» non diventa «passabile»."
            "Da lei, è quasi un encomio solenne."
        "Chiederle di mostrarmi il colpo, lentamente":
            show aede irritata with qdiss
            aede "Lentamente? Il nemico non rallenta per cortesia."
            "Ma lo mostra. Due volte. E la seconda, giuro, è più lenta della prima."
        "Lamentarmi del turno all'alba":
            $ aede_affinity -= 1
            show aede irritata with qdiss
            aede "Il sole non si lamenta di sorgere. E ha più motivi di te."
    return

label att_spada_2:
    scene bg palestra with fade
    show aede neutra with dissolve
    "Oggi tocca ai bersagli di paglia. Aede li sistema a distanze irregolari, «come la Famiglia: il peso non è mai dove te lo aspetti»."
    "A metà esercizio mi accorgo che uno dei bersagli ha una moneta appesa al centro, a filo."
    menu:
        "La moneta oscilla al vento."
        "Colpire la moneta, non il bersaglio":
            $ aede_affinity += 1
            show aede sorpresa with qdiss
            "La manco di un dito. Ma la lama vibra nel punto giusto, e lei lo vede."
            aede "...era una prova per la settimana prossima. Sei in anticipo. Non montarti la testa."
        "Colpire il bersaglio, come da consegna":
            show aede neutra with qdiss
            aede "Preciso e obbediente. Briseide vi fabbrica così. Non è un difetto. Non è neanche un pregio."
    return

label att_spada_3:
    scene bg palestra with fade
    show aede neutra with dissolve
    "Pioggia sottile. Gli altri novellini disertano; io no. Il cortile è solo nostro, e il silenzio ha un suono diverso."
    aede "Sai perché mi alleno anche con la pioggia? Perché chi mi vorrà morta non guarderà il cielo prima."
    menu:
        "L'acqua le cola dai capelli rossi come ruggine."
        "«Allora che piova. Facciamo due riprese in più.»":
            $ aede_affinity += 1
            show aede sorriso with dissolve
            "Due riprese in più. E alla fine, per un istante, quella piega all'angolo della bocca."
        "«Nessuno ti vuole morta, Aede.»":
            show aede irritata with qdiss
            aede "Che ne sai tu. Guardia alta."
            "La lezione dura il doppio. Credo sia il suo modo di cambiare argomento."
    if druso_affinity >= 5:
        show aede irritata with qdiss
        aede "Il figlio di Lenora ti chiama «linguaccia», in giro. Digli che qui la linguaccia impara a parlare con l'acciaio."
        "Non è gelosia. È catalogazione. Credo."
    return


## Scudo e lotta — territorio di Druso #######################################

label att_scudo_1:
    scene bg palestra with fade
    show druso ghigno at left with easeinleft
    druso "Novellin[fin]! Guarda guarda. Briseide vi manda ancora in palestra o siete venut[fin] a guardare i veri uomini?"
    "Druso fa roteare lo scudo come un piatto da taverna. Metà esibizione, metà sfida."
    menu:
        "Il ghigno aspetta una reazione. Qualunque."
        "«Veri uomini? Fammi sapere quando ne arriva uno.»":
            $ druso_affinity += 1
            show druso ghigno with qdiss
            druso "AH! Linguaccia! Mi piace. Prendi uno scudo, linguaccia, vediamo se il braccio vale la bocca."
        "Ignorarlo e prendere uno scudo in silenzio":
            druso "Silenzioso. Mh. I silenziosi o sono pericolosi o sono noiosi. Vediamo quale dei due."
        "Scusarmi e mettermi in fondo alla fila":
            $ druso_affinity -= 1
            druso "In fondo alla fila, dove non dai fastidio. Ecco, bravo. Resta lì."
            "Mi ha già archiviato. Si sente dal tono."
    return

label att_scudo_2:
    scene bg palestra with fade
    show druso ghigno at left with dissolve
    "Lezione di lotta. Druso «insegna» mettendo a terra i novellini uno a uno, con commento poetico annesso."
    druso "E anche questo giace! Componimento: «Cadde il fiore di Briseide — più lesto a terra che in amore.» Rima baciata, come piace a me."
    menu:
        "Il prossimo sono io."
        "Attaccare per primo, senza aspettare il segnale":
            $ druso_affinity += 1
            with vpunch
            "Lo prendo a metà strofa. Finisco a terra lo stesso, ma ci finisce anche lui, e la sabbia non guarda in faccia i figli di Lenora."
            druso "FALLO! Bellissimo! Ecco uno che ha capito la poesia!"
        "Aspettare il segnale, da regolamento":
            with vpunch
            "Segnale, presa, volo, sabbia. Tutto secondo regolamento, compresa la mia schiena."
            druso "Regolare e prevedibile. Il mio verso preferito: «cadde con stile»."
        "Rifiutare la lotta":
            $ druso_affinity -= 1
            druso "Si rifiuta! Oh, che peccato. Componimento breve: «No.»"
    return

label att_scudo_3:
    scene bg palestra with fade
    show druso serio at left with dissolve
    "Druso, stranamente serio, controlla le cinghie del mio scudo una a una."
    druso "Cinghia molle, braccio rotto. Te lo dico io che le ho rotte tutte e due, e non per modo di dire."
    menu:
        "È quasi premuroso. Quasi."
        "«Grazie, Druso.»":
            $ druso_affinity += 1
            show druso ghigno with qdiss
            druso "Non ringraziare, mi rovini la reputazione. Di' in giro che ti ho insultato."
        "«Chi sei e cosa hai fatto a Druso?»":
            show druso ghigno with qdiss
            druso "L'ho mangiato. Era indigesto. Guardia su, linguaccia."
    return


## Studio — la storia della Famiglia #########################################

label att_studio_1:
    scene bg studio_glauco with fade
    show corrado neutro with dissolve
    "L'archivio del Ceppo. Corrado mi fa da maestro: 63 Ceppi, 9 Rami, un Primarca per Ramo, e in cima la Capofamiglia."
    corrado "Impara gli stemmi prima dei nomi. I nomi mentono, gli stemmi mai: nessuno ricama un leone per sbaglio."
    "Tre ore di araldica. Alla fine distinguo il drago di Draken dal leone di Allmän anche a occhi chiusi."
    return

label att_studio_2:
    scene bg studio_glauco with fade
    show corrado neutro with dissolve
    "Oggi: le Virtù. Operosità, Esclusività, Verità. Ogni Arconte ne custodisce una, ogni processo ne invoca almeno due."
    corrado "E ricorda: la Virtù che un Dignitas predica di più è quella che teme di meno. È l'altra che lo tiene sveglio."
    "Me lo scrivo. Ho il sospetto che un giorno mi salverà la vita."
    return

label att_studio_3:
    scene bg studio_glauco with fade
    show corrado neutro with dissolve
    "Il Ballo delle Candele Spente. Il libro ne parla per tre righe asciutte; Corrado, a voce bassa, per un'ora."
    corrado "Lenora spense le candele, e con le candele una congiura intera. Nessun processo. Nessun nome. Capito perché studiamo, [fratello_t]?"
    "Capito. Nel Nord la storia non si studia per sapere com'era: si studia per sapere dove non mettere i piedi."
    return


## Riti del Ceppo di Briseide (gli interludi ricollocati) ####################

label att_riti_1:
    call interludio1
    return

label att_riti_2:
    call interludio2
    return

label att_riti_3:
    call interludio3
    return


## Commissioni in città ######################################################

label att_citta_1:
    scene bg vicoli_zefiro with fade
    "Consegne per Briseide: lana alla Contrada Lumina, lettere alla Consorteria. Zefiro mi entra nelle gambe, vicolo dopo vicolo."
    "A fine giro conosco tre scorciatoie nuove e un lanternaio che fa credito ai Figli di Briseide. Capitale, nel Nord."
    return

label att_citta_2:
    scene bg vicoli_zefiro with fade
    "Giorno di mercato. Studio i banchi come mi ha insegnato Corrado: chi paga in Scudi nuovi, chi in moneta della Lega, chi non paga e saluta."
    "«Guarda, ascolta, non farti notare.» Due su tre, come sempre."
    return


## Taverna — territorio serale di Druso ######################################

label att_taverna_1:
    scene bg vicoli_zefiro with fade
    show druso ghigno at left with easeinleft
    druso "Novellin[fin]! Siediti che declamo. Ho un componimento nuovo e nessun pubblico degno: tu farai finta di esserlo."
    "Il componimento è irripetibile. La taverna applaude, la locandiera minaccia, Druso ringrazia entrambe."
    menu:
        "Alza il boccale verso di me, in attesa di verdetto."
        "«Metrica zoppa. Il contenuto peggio. Bis.»":
            $ druso_affinity += 1
            druso "ZOPPA?! Questa zoppa ha fatto piangere un Eparca! ...il bis però te lo concedo."
        "Applaudire educatamente":
            druso "Applauso educato. La morte di ogni poeta. Bevi, che è meglio."
    if aede_affinity >= 5:
        druso "A proposito: salutami la volpe rossa. Ancora niente, tra voi? Quando ti taglia la gola, pensami."
        "Il cascamorto di Rocca Tempesta. Aede lo infilerebbe su uno spiedo. Forse è per questo che ci prova."
    return

label att_taverna_2:
    scene bg vicoli_zefiro with fade
    show druso ghigno at left with dissolve
    "Druso tiene banco su chi, tra gli avventori, reggerebbe un TESCHIO a tradimento. La classifica è dettagliata e offensiva."
    druso "E tu, novellin[fin]? Reggeresti? Ti vedo tener le mani in grembo come una vergine all'Adunanza."
    menu:
        "La taverna intera aspetta."
        "«Dichiara pure. Ma stanotte dormi con un occhio aperto.»":
            $ druso_affinity += 1
            druso "Minaccia CON stile! Finalmente! Pagherei da bere, ma pago già abbastanza dazi."
        "Cambiare discorso":
            $ druso_affinity -= 1
            druso "Cambia discorso. Come i diplomatici. E i codardi. A volte è la stessa gilda."
    return

label att_taverna_3:
    scene bg vicoli_zefiro with fade
    show druso serio at left with dissolve
    "Trovo Druso da solo, per una volta. Fissa il fondo del boccale come se ci avesse perso qualcosa."
    druso "Mio fratello Caino colleziona cariche. Icaro colleziona Scudi. Io colleziono... pubblico. Qualcuno doveva pur farlo."
    menu:
        "Non è una battuta. O non del tutto."
        "«Il pubblico si scorda. Gli amici no.»":
            $ druso_affinity += 1
            show druso imbarazzato with qdiss
            druso "Sentimentale! Che schifo. ...ripetilo."
        "«Ti compiango, figlio di Lenora.»":
            druso "Compiangimi, compiangimi. Almeno tu reciti gratis."
    return


## Sala da gioco e fumeria — territorio serale di Icaro ######################

label att_fumeria_1:
    scene bg vicoli_zefiro with fade
    "La saletta dietro la Consorteria: fumo dolce, carte, monete che cambiano padrone in silenzio."
    "In fondo, da solo, un uomo magro con la pipa: Icaro, il terzo figlio di Lenora. Vince tre mani su tre senza alzare la voce."
    "Mi avvicino. Mi guarda. Decide che non esisto, e torna alle carte."
    return

label att_fumeria_2:
    scene bg vicoli_zefiro with fade
    "Stavolta mi siedo al suo tavolo. Icaro non protesta: un giocatore in più è una tasca in più."
    "Perdo sette Scudi in quattro mani. Ma guardo. E a un certo punto, sul taglio del mazzo, le sue dita fanno una cosa che le dita non dovrebbero fare."
    menu:
        "Nessuno ha visto niente. Tranne me."
        "Tacere e perdere l'ottavo Scudo con dignità":
            $ icaro_affinity += 1
            "Pago. Icaro intasca. E per la prima volta i suoi occhi mi restano addosso un secondo di troppo, come su un conto che non torna."
        "Sussurrare «bel taglio» a voce bassissima":
            $ icaro_affinity += 1
            icaro "...non so di cosa parli. Ma per la cronaca: era irreprensibile."
            "Puntiglioso come un notaio. Interessante."
        "Gridare al baro":
            $ congelate.add("icaro")
            icaro "Contate le carte, signori. Tutte regolari. Il novellin[fin] ha bevuto."
            "Le carte, ovviamente, sono regolari. Adesso. La saletta ride di me, e Icaro non mi guarderà mai più."
    return

label att_fumeria_3:
    scene bg vicoli_zefiro with fade
    "Serata lenta. Icaro fuma la pipa accanto alla finestra, i piedi sul tavolo, l'aria di chi ha vinto abbastanza per oggi."
    icaro "Tu. Quell[fin] che guarda le mani invece delle carte. Siediti, se proprio devi. Ma non toccare niente di mio."
    menu:
        "Il fumo sa di resina e di quiete."
        "Sedermi e stare zitt[fin], godendomi la calma":
            $ icaro_affinity += 1
            icaro "Mh. Sai stare in silenzio. Raro. Costoso, il silenzio: quasi quanto l'erba buona."
        "Chiedergli quanto ha vinto stasera":
            icaro "Abbastanza. Che è l'unica cifra che do gratis."
    if caino_fiducia >= 4:
        icaro "Tu lavori ai registri di mio fratello. Consiglio gratuito, e da me il gratuito è raro: con Caino conta due volte. La prima per lui, la seconda per te."
    return


## Varianti aggiuntive (seconda infornata) ###################################

label att_spada_4:
    scene bg palestra with fade
    show aede neutra with dissolve
    "Giornata di manutenzione: pietra, olio, filo. Aede tratta le lame del Ceppo come Briseide tratta gli orfani: una a una, per nome."
    aede "Questa ha un dente nel filo. Chi la usa così merita di perderla. Tu come tieni la tua?"
    menu:
        "La mia spada da esercizio è nel portarack. Com'è messa?"
        "Mostrargliela: pulita, affilata, oliata ieri":
            $ aede_affinity += 1
            show aede sorriso with dissolve
            aede "...mh. Qualcuno ascolta, in questo cortile. Non montarti la testa: la pietra te la presto lo stesso."
        "Confessare che non la pulisco da una settimana":
            show aede irritata with qdiss
            aede "Una settimana. La tua lama ti odia, e io con lei. Siediti: oggi si lucida finché non ti ci specchi."
    return

label att_scudo_4:
    scene bg palestra with fade
    show druso ghigno at left with easeinleft
    druso "Novellin[fin]! Oggi lezione teorica: come NON prendere un TESCHIO. Sedia, appunti, e occhio alle mie mani che la pratica parte senza preavviso."
    "Un'ora di finte, parate basse e aneddoti osceni sui fallimenti dei suoi allievi. Alla fine le mani le ho ancora tutte, e qualcosa ho pure imparato."
    druso "Promoss[fin] con riserva. La riserva è che domani si fa sul serio."
    return

label att_studio_4:
    scene bg studio_glauco with fade
    show corrado neutro with dissolve
    "Oggi Corrado mi insegna il Margine: il fiume lento che gli Arvali dicono separi i vivi da Drakengrad, la sala del Leone dove ogni storia viene raccontata per sempre."
    corrado "Non è teologia, [fratello_t]: è contabilità. Un Dignitas si comporta bene perché qualcuno, laggiù, prende appunti."
    "Mi segno anche questa. Nel Nord perfino l'aldilà tiene i registri."
    return

label att_riti_4:
    scene bg corridoio_ceppo with fade
    show briseide neutra with dissolve
    "Giorno di brodo. Tutto il Ceppo in cucina: cinquanta Figli, un pentolone, e Briseide che comanda la brigata come un Consiglio di guerra."
    briseide "Il segreto non è la ricetta, [player_name]. È che mentre si taglia la cipolla si parla. E chi parla tagliando non mente: è impegnato."
    "Taglio cipolle per due ore. Ascolto tre segreti, un litigio e una canzone. Briseide aveva ragione, come sempre."
    return

label att_citta_3:
    scene bg vicoli_zefiro with fade
    "Commissione alla Contrada Eburnea: riportare un libro prestato. La strada passa per la Calà, trecento gradini vuoti in pieno giorno."
    "Senza lanterne è solo una scala. Eppure rallento lo stesso, al gradino duecento, senza un perché. Le leggende di Zefiro sanno aspettare."
    return

label att_taverna_4:
    scene bg vicoli_zefiro with fade
    show druso ghigno at left with easeinleft
    druso "Sedetevi, gente! Stasera si duella a versi. Chi perde paga il giro. Novellin[fin], tu sei lo sfidante."
    "La taverna ruggisce. La locandiera mette già i boccali in conto a me."
    druso "Comincio io. «Figli[fin] di Briseide, lana in testa e lana in cuore — ti sposerebbe una pecora, ma ha già un amore.»"
    "Risate. Druso si inchina a metà, sul tavolo, rischiando la vita."
    menu:
        "Tocca a me. Tutti gli occhi sono addosso."
        "«Druso Lenorio, poeta di taverna: rima con 'cena' e con 'vena', ma mai con 'sostanza'.»":
            $ druso_affinity += 1
            with hpunch
            show druso ghigno with qdiss
            druso "OH! Mi ha colpito! Dritto nell'orgoglio! Un altro giro per lo sfidante: e lo paga il perdente. Cioè io."
            "La taverna batte i boccali. Per una sera, sono dei loro."
        "Rispondere con un verso sconcio, il più sporco che mi viene":
            $ druso_affinity += 1
            with hpunch
            druso "Questa non è poesia, è un'accusa! ...ripetila più piano, che la scrivo."
            "Druso ride fino alle lacrime. La locandiera no."
        "«Io non rimo. Io pago e me ne vado.»":
            show druso ghigno with qdiss
            druso "Ritirata con onore: la peggior poesia che esista. Siediti, almeno bevi."
        "«Per favore, basta, non so far versi...»":
            $ druso_affinity -= 1
            show druso ghigno with qdiss
            druso "Supplica. Il genere meno originale. Ti do un voto: «zero», in rima con «ciao»."
    return

label att_fumeria_4:
    scene bg vicoli_zefiro with fade
    show icaro neutro with dissolve
    "Serata di inventario: Icaro conta le vincite della settimana sul tavolo piccolo. Monete in pile per taglio, per conio, per Lega."
    icaro "Non toccare. Puoi guardare. Guardare è gratis, stasera: offerta di lancio."
    menu:
        "Una pila è più corta delle altre. Lo noto. Lui nota che lo noto."
        "«Manca uno Scudo nella terza pila.»":
            $ icaro_affinity += 1
            show icaro furbo with qdiss
            icaro "...l'ho messo io da parte, per vedere chi se ne accorgeva. Tre settimane. Sei [il_t] prim[fin]."
            "Lo rimette nella pila con un mezzo sorriso. Da Icaro, è un applauso."
        "Guardare e basta, com'è gratis":
            icaro "Bravo. Il pubblico migliore è quello che non fa domande."
    return
