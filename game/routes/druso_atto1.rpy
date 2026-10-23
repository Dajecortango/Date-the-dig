# Route Druso — Atto 1: eventi 1-2 e interludi 1-2 (Lune II-III).

## Evento 1 — Il poeta osceno ################################################

label druso_ev1:
    scene bg vicoli_zefiro with fade
    "Zefiro di sera puzza di sego, di birra e di neve sporca. La taverna del Becco Storto è l'unica luce accesa in fondo al vicolo."
    "Dentro, fumo fino alle travi. E una voce che copre tutto il resto."
    show druso ghigno at left with easeinleft
    "La taverna è sua, stasera: ha pagato un giro per comprarsi il silenzio e lo spreca subito."
    druso "Silenzio, bestie! Il genio parla e voi masticate. Chi mastica durante un'ode, la paga."
    "Cento chili di Dignitas in piedi su una panca. Barba rossiccia, camicia slacciata fino allo sterno, un boccale come scettro."
    "Druso, figlio di Lenora. Il secondo dei tre. Quello che a Rocca Tempesta nominano alzando gli occhi al cielo."
    druso "Ah! Ma guarda chi è entrat[fin]. La faccia nuova del Ceppo di Briseide. Proprio ciò che mi serviva: una musa che non ho ancora offeso."
    druso "Componimento nuovo! Titolo: «Ode [al_t] novellin[fin] di Briseide». Protagonista: presente in sala. Contenuto: indecente. Obiezioni?"
    "Trenta teste si girano verso di me. Qualcuno batte il boccale sul tavolo, già pronto a ridere."
    menu:
        "Tutti mi guardano. È esattamente ciò che vuole."
        "«Procedi. Ma se la rima è zoppa, il bis lo recito io su di te.»":
            $ druso_affinity += 1
            druso "Minaccia poetica! La più nobile delle minacce!"
            druso "«Venne dal Sud con le scarpe pulite, ma al Nord le scarpe si fanno smarrite...»"
            "Recita. È oscena, puntuale, e — maledizione — ben scritta. Rispondo con due versi improvvisati sulla sua barba. La taverna sceglie me."
            pc "«Barba di Druso, nido di ratti: ci han fatto il letto, ci han fatto i patti.»"
            "Un vecchio al bancone si soffoca con la birra. Il tavolo dei carrettieri chiede il bis."
            show druso ghigno with qdiss
            druso "Hai vinto il pubblico, linguaccia. Il pubblico è MIO. Ora o ti odio o ti tengo. Non ho ancora deciso."
            druso "Nel dubbio, siediti accanto a me. I nemici si tengono a portata di gomito."
        "Arrossire e pregarlo di smettere":
            $ druso_passo_falso()
            druso "Oh, supplica! Che noia. Le suppliche funzionano solo in chiesa, e il Nord non ne ha."
            "Recita lo stesso. Più lento, apposta, e a ogni rima mi punta il boccale in faccia."
            druso "Applausi per la musa! Muta, rossa e inutile. Come una barbabietola."
        "Rovesciargli il boccale addosso":
            $ druso_affinity += 1
            with vpunch
            "Il boccale vola. La taverna tace. Druso si lecca la birra dal baffo, lentamente, come un gatto soddisfatto."
            druso "Reazione violenta e maleducata. Da manuale. CONTINUA COSÌ."
            druso "Oste! Un boccale nuovo per [il_t] novellin[fin]. Pieno. Così la prossima volta mi colpisce meglio."
    "Più tardi, mentre la taverna si svuota, lo vedo scrivere su un tovagliolo. Si accorge che guardo e lo appallottola."
    druso "Appunti. Per la seconda strofa. Sei stat[fin] fonte d'ispirazione, non montarti la testa."
    return


## Interludio 1 — Il guerriero da esposizione ################################

label druso_int1:
    scene bg palestra with fade
    "Palestra della Rocca, prima campana. Odore di cuoio, di sudore vecchio, di segatura bagnata."
    show druso ghigno at left with easeinleft
    "Druso è seduto su una panca, accanto a un manichino. Il manichino è più sudato di lui."
    druso "Novellin[fin]! Puntuale come un debito. Ti aspettavo: mi serve un testimone."
    pc "Testimone di cosa?"
    druso "Del mio allenamento. Se nessuno mi vede allenarmi, è come se non mi fossi allenato. Filosofia."
    "Solleva una spada di legno. La guarda. La posa."
    druso "Ecco. Riscaldamento fatto. Ora la parte importante: il poema sul riscaldamento."
    "Dall'altro lato della sala, i Figli di Glauco si picchiano sul serio. Uno vola contro il muro con un rumore di sacco."
    show druso sorpreso with qdiss
    druso "Visto? Barbari. Io difendo il corpo, che è un'opera d'arte. Ci si mette anni a coltivare una pancia così."
    menu:
        "Mi porge l'altra spada di legno, con l'aria di chi spera che io rifiuti."
        "Prenderla e attaccarlo senza preavviso":
            with vpunch
            "Il colpo gli arriva sulla spalla. Druso strilla come una gallina, poi para il secondo — e il terzo, quasi bene."
            show druso irritato with qdiss
            druso "Ah, così, a tradimento! Senza il saluto! Che razza di Ceppo vi alleva?"
            "Ma ha gli occhi accesi. Per cinque scambi buoni dimentica di essere un codardo. Poi se ne ricorda e si siede."
            druso "Basta. Ho dimostrato il punto. Quale punto, non chiedere."
        "«Non mi alleno con chi ha paura di sudare.»":
            show druso ghigno with qdiss
            druso "Paura? Io? Io ho un CONTRATTO con la paura. Lei sta lontana da me, io sto lontano dai guai."
            druso "Funziona da ventisei anni. Guarda: tutti i denti. Conta, se vuoi."
            "Spalanca la bocca. Ha davvero tutti i denti. È un argomento più forte di quanto vorrei."
        "Sedermi accanto a lui e guardare gli altri":
            show druso neutro with qdiss
            "Restiamo seduti. Lui commenta ogni colpo come un cronista di tornei, in rima, a mezza voce."
            druso "«Quello là col naso storto, entro sera sarà morto.» Non letteralmente. Poeticamente."
            "Poi, senza cambiare tono:"
            druso "Mio fratello Caino si allenava qui ogni mattina. Ogni. Mattina. A dodici anni. Io leggevo, lui sanguinava."
            druso "Madre ha scelto chi guardare. Non ha scelto me. Ottima scelta: io sono più bello da lontano."
    show druso ghigno with qdiss
    druso "Ora scusami. Devo andare a raccontare in taverna di quanto mi sono allenato duro."
    "Esce col petto in fuori. La spada di legno resta sulla panca, ancora asciutta."
    return


## Evento 2 — La leva ########################################################

label druso_ev2:
    scene bg vicoli_zefiro with fade
    "Il retro del Becco Storto: botti vuote, un gatto senza un orecchio, una porta che dà sul canale ghiacciato."
    show druso neutro at left with dissolve
    "Druso, stranamente sobrio, mi aspetta nel retro della taverna con una pergamena di scommesse."
    druso "Chiudi la porta. No, non per quello. Per quello ti avrei portat[fin] in un posto più comodo."
    "Srotola la pergamena sulla botte. Nomi, cifre, frecce. Una calligrafia minuta, ordinata, sorprendente."
    druso "Tu credi che io passi le serate a bere. Io passo le serate ad ascoltare chi beve. È diverso. Costa uguale."
    druso "Senti qua. Un Eparca della Consorteria paga bene per sapere chi, nel tuo Ceppo, firma le lettere di Briseide quando lei è fuori città. Io lo so che lo sai. E tu sai che pagherei."
    "Fa girare una moneta sulla botte. Non la guarda: guarda me."
    druso "Pensaci. Soldi veri, niente sangue. Un nome solo, e domani ti offro io da bere per una Luna intera."
    menu:
        "Il ghigno è a mezza via tra scherzo e agguato."
        "«Vendimi pure. Ma ricorda che poi la leva si gira.»":
            $ druso_affinity += 2
            show druso ghigno with qdiss
            druso "...risposta da fratello di Ceppo. O da nemico serio. In entrambi i casi: rispetto."
            druso "Era una prova, ovvio. L'Eparca esiste, la paga pure. Il mio rifiuto gliel'ho già venduto a caro prezzo."
            "Arrotola la pergamena e me la mostra di sfuggita. In fondo c'è il mio nome, con una crocetta accanto."
            druso "Crocetta vuol dire: morde. Non ne ho tante, di crocette. Mio fratello Icaro ne ha una. Caino due."
        "Dirgli il nome: in fondo siamo amici":
            $ druso_passo_falso()
            $ druso_affinity -= 1
            druso "...l'hai detto davvero. Oh, povero tesoro. No, il nome non lo userò. Ma adesso so che sei un cane che non abbaia neanche."
            "Scrive qualcosa sulla pergamena. Non vedo cosa. Vedo solo che non è una crocetta."
        "Minacciarlo: se parla, lo denuncio al Consiglio":
            $ druso_passo_falso()
            druso "DENUNCIA! Al CONSIGLIO! Dove siede mia madre! Ti prego, fallo, voglio il posto in prima fila!"
            druso "Le minacce mi fanno l'effetto del vino caldo. Vieni qui, minacciami ancora, che ho freddo."
    "Il gatto senza orecchio salta sulla botte e si siede sulla pergamena. Druso non lo scaccia."
    druso "Lui sì che sa tenere un segreto. Si chiama Lisandro. Per offendere qualcuno che conoscerai."
    return


## Interludio 2 — Cena di famiglia ###########################################

label druso_int2:
    scene bg vicoli_zefiro with fade
    "Il Becco Storto, tavolo d'angolo. Tre boccali, un quarto vuoto, e una tovaglia vera: qualcuno ha corrotto l'oste."
    show druso ghigno at left with easeinleft
    druso "Benvenut[fin] alla cena dei figli di Lenora! Tradizione antica. L'ho inventata martedì."
    show caino freddo at right with dissolve
    "Caino è già seduto. Schiena dritta, mantello chiuso, la faccia di chi è stato trascinato lì sotto minaccia."
    caino "Mi ha detto che c'era una questione di famiglia urgente."
    druso "E c'è! La famiglia ha fame. Icaro arriva tardi, come sempre. Probabilmente sta rubando il dessert altrove."
    caino "E [lui_t] perché è qui?"
    druso "Pubblico. Una cena di famiglia senza pubblico è solo un litigio con le posate."
    "L'oste porta stufato di cervo. Druso ne serve tre porzioni, la più grande a sé, la più piccola a Caino."
    druso "Caino, racconta [al_t] nostr[fin] ospite di quando a nove anni hai sfidato un orso. E hai perso. Contro un orso finto."
    show caino sarcastico with qdiss
    caino "Racconta tu di quando a undici anni sei svenuto alla vista di un'anatra sgozzata."
    druso "Era un'anatra GRANDE. E mi guardava."
    menu:
        "Tutti e due si girano verso di me, come se toccasse a me dare il voto."
        "«Da qui sembra che il vero orso sia l'anatra.»":
            show druso irritato with qdiss
            druso "Ah, si coalizzano! Il Ceppo di Briseide e il Ceppo dei fratelli ingrati. Oste, del veleno!"
            show caino neutro with qdiss
            "Caino fa una cosa che non gli ho mai visto fare: sbuffa dal naso. È, credo, una risata."
            caino "Tienil[fin]. Almeno uno di noi due ti risponde a tono."
        "«Druso, i versi sull'anatra li hai scritti, vero?»":
            show druso ghigno with qdiss
            druso "Undici strofe. Ottave. «Anatra mia, sventrata e santa, che ancor nei sogni il collo mi pianta.»"
            caino "Me le recitava sotto la porta, la notte. Per anni."
            druso "Il pubblico va formato da piccolo."
        "Mangiare in silenzio e lasciarli scannare":
            "Lo stufato è buono. I fratelli si insultano per mezz'ora, a turno, con la precisione di chi si allena da sempre."
            show caino neutro with qdiss
            caino "Annoto: arrivat[fin] al dolce. Nel registro delle tue cene, Druso, non risultano precedenti."
            druso "Zitto, tu. Non dar[gli_t] idee."
    hide caino with dissolve
    "Caino se ne va per primo, dopo aver pagato tutto senza dirlo. Druso se ne accorge solo all'uscita."
    show druso serio with qdiss
    druso "Ha pagato lui. Lo fa sempre. Così io resto quello che deve ringraziare."
    druso "Madre a lui lo LUCIDA, come una spada. A me mi CONTA, come un debito. Uno in vetrina, l'altro in cantina."
    show druso ghigno with qdiss
    druso "Questo non è un verso. Non annotarlo. Se finisce in un poema, ti querelo per plagio."
    return


## Deviazione (Luna II+) — Il quaderno ########################################

label druso_quaderno:
    scene bg vicoli_zefiro with fade
    "Il Becco Storto a metà pomeriggio è un'altra taverna: panche rovesciate, l'oste che conta i boccali, un gatto senza orecchio sul bancone."
    "Sotto la panca di Druso, incastrato tra due assi, c'è un quaderno. Rilegato in pelle, consumato agli angoli, con una macchia di vino a forma di isola."
    "Dentro, i tovaglioli. Tutti quelli che appallottola quando lo guardo, spianati con cura e cuciti uno dopo l'altro."
    "Il primo verso che leggo non ha una sola parolaccia. Parla di una finestra a Rocca Tempesta, e di un bambino che aspetta che la madre si affacci."
    "Chiudo. Riapro. È scritto bene. È scritto meglio di qualunque cosa abbia mai sentito in questa taverna."
    show druso sorpreso at left with easeinleft
    druso "Oste! Hai visto un... ah."
    "Si ferma a metà della sala. Guarda il quaderno, poi me, poi di nuovo il quaderno. Si gratta la barba con tutte e due le mani."
    menu:
        "Il quaderno è aperto sulle mie ginocchia. Lui non si avvicina."
        "«Pagina sette: la rima con \"tempesta\" zoppica. Il resto è bello da far schifo.»":
            $ druso_quaderno_esito = "detto"
            $ druso_affinity += 1
            show druso irritato with qdiss
            druso "Zoppica? ZOPPICA? Quella rima mi è costata tre notti e un litigio con l'oste!"
            "Mi strappa il quaderno, lo apre a pagina sette, legge muovendo le labbra."
            show druso ghigno with qdiss
            druso "...zoppica. Maledett[fin]. Hai letto tutto e hai pure ragione."
            druso "Bene. Adesso sei complice. I complici leggono le bozze. Le bozze fanno schifo. È una condanna, non un onore."
        "Chiuderlo e porgerglielo. Senza una parola":
            $ druso_quaderno_esito = "chiuso"
            "Lo chiudo, ci passo sopra il palmo, glielo tendo. Lui lo prende per un angolo, con due dita, e se lo ficca sotto la camicia."
            show druso serio with qdiss
            druso "Nessuno restituisce chiuso un quaderno aperto. O sei un santo o sei un bugiardo."
            druso "Non dirmi quale. Santo fa rima con pianto, bugiardo con lardo, e stasera non ho fame né dell'uno né dell'altro."
        "Rimetterlo sotto la panca prima che si avvicini":
            $ druso_quaderno_esito = "nascosto"
            "Lo infilo di nuovo tra le assi con un colpo di tallone. Lui non ha visto. Credo."
            show druso neutro with qdiss
            druso "Niente. Cercavo... il mio talento. L'avevo lasciato qui ieri sera."
            "Si siede proprio su quella panca. Ci resta tutta la sera, come una chioccia sulle uova."
    "Quando esco, Lisandro il gatto mi segue fino alla porta. Ha l'aria di chi sa tutto e lo venderà a caro prezzo."
    return
