# Route Druso — "Il cuore provocatore".
# Lucchetto a rovescio: l'affinità sale solo tenendogli testa. Per un uomo
# la salita è più ripida: due passi falsi e Druso archivia (5/5 contro 4/5).
# Gli interludi (druso_int1-3, druso_luna6) sono a punti zero: solo testo.

default druso_passi_falsi = 0
default flag_druso_coraggio = False
# Scelta davanti al Consiglio (druso_climax): "parla" | "lascia" | "battuta".
default druso_consiglio = None
default druso_sfida = None

init python:
    def druso_passo_falso():
        # I passi falsi contano solo se player_gender == "m" (rl).
        store.druso_affinity -= 1
        passi, avvisa, congela = rl.druso_passo_falso(
            store.player_gender, store.druso_passi_falsi)
        store.druso_passi_falsi = passi
        if avvisa:
            renpy.notify("Druso se la segna.")
        if congela:
            store.congelate.add("druso")

    EVENTI.extend([
        {"id": "druso_ev1", "label": "druso_ev1", "tipo": "invito",
         "char": "druso", "titolo": "Druso pretende un pubblico: serata di versi",
         "luna_min": 2, "slot": "sera",
         "cond": lambda v: v["druso_affinity"] >= 3},
        {"id": "druso_int1", "label": "druso_int1", "tipo": "invito",
         "char": "druso", "titolo": "Druso in palestra. Dice che si allena",
         "luna_min": 2, "slot": "mattina",
         "cond": lambda v: "druso_ev1" in v["visti"]
         and "scelta_cuore" not in v["visti"]},
        {"id": "druso_ev2", "label": "druso_ev2", "tipo": "invito",
         "char": "druso", "titolo": "Una scommessa che puzza di trappola",
         "luna_min": 3, "slot": "sera",
         "cond": lambda v: v["druso_affinity"] >= 6
         and "druso_ev1" in v["visti"]},
        {"id": "druso_int2", "label": "druso_int2", "tipo": "invito",
         "char": "druso", "titolo": "Cena di famiglia in taverna. Sei l'ospite",
         "luna_min": 3, "slot": "sera",
         "cond": lambda v: "druso_ev2" in v["visti"]
         and "scelta_cuore" not in v["visti"]},
        {"id": "druso_ev3", "label": "druso_ev3", "tipo": "invito",
         "char": "druso", "titolo": "Druso ti vuole con sé. Non spiega perché",
         "luna_min": 4, "slot": "pomeriggio",
         "cond": lambda v: v["druso_affinity"] >= 9
         and "druso_ev2" in v["visti"]},
        {"id": "druso_int3", "label": "druso_int3", "tipo": "invito",
         "char": "druso", "titolo": "Druso chiede lezioni. A te. Di nascosto",
         "luna_min": 4, "slot": "mattina",
         "cond": lambda v: "druso_ev3" in v["visti"]
         and "scelta_cuore" not in v["visti"]},
        {"id": "druso_ev4", "label": "druso_ev4", "tipo": "invito",
         "char": "druso", "titolo": "Notte di guardia sulle mura di Zefiro",
         "luna_min": 4, "slot": "sera",
         "cond": lambda v: v["druso_affinity"] >= 9
         and "druso_ev3" in v["visti"]
         and "scelta_cuore" not in v["visti"]},
        {"id": "druso_luna5", "label": "druso_luna5", "tipo": "fisso",
         "char": "druso", "luna": 5, "giorno": 6, "slot": "sera",
         "cond": lambda v: v["route_attiva"] == "druso"
         and "druso" not in v["congelate"]},
        {"id": "druso_luna6", "label": "druso_luna6", "tipo": "fisso",
         "char": "druso", "luna": 6, "giorno": 5, "slot": "sera",
         "cond": lambda v: v["route_attiva"] == "druso"
         and "druso" not in v["congelate"]},
    ])


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
            "Recita lo stesso. Più lento, apposta, guardandomi a ogni rima come si guarda un topo in trappola."
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
    "Eccolo: il test delle acque. Vuole vedere se sono una leva su cui fare forza."
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
            caino "Sei la prima persona che porta qui e che resta fino al dolce."
            druso "Zitto, tu. Non dar[gli_t] idee."
    hide caino with dissolve
    "Caino se ne va per primo, dopo aver pagato tutto senza dirlo. Druso se ne accorge solo all'uscita."
    show druso serio with qdiss
    druso "Ha pagato lui. Lo fa sempre. Così io resto quello che deve ringraziare."
    druso "Madre lo guarda come si guarda una spada. Me, come si guarda un debito."
    show druso ghigno with qdiss
    druso "Questo non è un verso. Non annotarlo. Se finisce in un poema, ti querelo per plagio."
    return


## Evento 3 — Il coraggio che stupisce anche lui #############################

label druso_ev3:
    scene bg vicoli_zefiro with fade
    show druso neutro at left with dissolve
    "Mi trascina «a vedere una cosa» nei vicoli bassi di Zefiro. La cosa è un esattore della Malacorte che spreme un lanternaio — il mio lanternaio, quello che fa credito ai Figli di Briseide."
    "Pomeriggio grigio. I balconi gocciolano neve sciolta. Nessuno guarda, perché a Zefiro guardare costa."
    druso "Brutto affare. Andiamocene. Non è il nostro Ceppo, non è il nostro problema, e io ci tengo ai miei denti."
    druso "Te li ho mostrati, i miei denti. Sono tutti lì. È un patrimonio di famiglia."
    "L'esattore ha un bastone ferrato. Il lanternaio ha le mani sopra la testa e un occhio già chiuso."
    menu:
        "Il lanternaio è a terra. L'esattore conta."
        "Intervenire, adesso":
            $ druso_affinity += 2
            $ flag_druso_coraggio = True
            with vpunch
            "Non aspetto. Due passi, il braccio dell'esattore, la torsione che Aede insegna ai novellini. E poi — dal nulla — un ruggito."
            show druso ghigno with qdiss
            druso "TESCHIO, BRUTTO STRACCIONE!"
            "Druso. Il codardo dichiarato. Addosso all'esattore con tutti i suoi cento chili, la barba e nessun piano."
            with hpunch
            "Rotolano nel fango. Druso morde. Proprio così: morde un orecchio, e l'esattore scappa urlando verso il canale."
            "Dopo, mentre il lanternaio ci benedice in tre dialetti, Druso si guarda le mani come se non le riconoscesse."
            show druso imbarazzato with qdiss
            druso "...non dirlo a nessuno. Il coraggio mi rovina la reputazione peggio della gratitudine."
            druso "E se lo dici, di' che l'ho fatto per noia. Che mi annoiavo. Che i cento chili si sono mossi da soli."
            pc "Hai morso un uomo, Druso."
            druso "Sapeva di cipolla. Sarà nel poema. Il morso, non la cipolla."
        "Dargli retta e andarcene":
            $ druso_affinity -= 1
            show druso serio with qdiss
            "Ce ne andiamo. Druso non fa battute per tutta la strada. È la cosa più vicina al disprezzo che gli abbia mai visto addosso — e non so se è per me o per sé."
            "Al ponte si ferma, guarda indietro verso il vicolo, e per un attimo sembra sul punto di tornare."
            druso "...niente. Mi era sembrato di aver dimenticato qualcosa."
    return


## Interludio 3 — La lezione segreta #########################################

label druso_int3:
    scene bg palestra with fade
    "Palestra della Rocca, prima dell'alba. Le torce sono ancora spente. Qualcuno ha sbarrato la porta dall'interno."
    show druso imbarazzato at left with dissolve
    "Quel qualcuno è Druso, in camicia da notte e stivali, con due spade di legno sotto il braccio."
    druso "Zitto. Non una parola. Se qualcuno chiede, sono qui per sonnambulismo."
    druso "Quella torsione. Quella del vicolo. Quella che fa Aede. Insegnamela."
    pc "Il codardo dichiarato vuole imparare a combattere?"
    show druso irritato with qdiss
    druso "Il codardo dichiarato vuole smettere di combattere a morsi. È poco elegante. E l'orecchio di quello aveva un sapore che sento ancora."
    "Gli mostro la presa. Lui sbaglia. Gli mostro di nuovo. Sbaglia peggio, ma ride."
    show icaro furbo at right with dissolve
    "Una voce dal soppalco. Icaro, seduto a gambe incrociate sulle travi, la pipa spenta tra i denti."
    icaro "Interessante. Mio fratello sveglio prima di mezzogiorno, sobrio, e in palestra. Devo avvisare un sacerdote?"
    show druso sorpreso with qdiss
    druso "Da quanto sei lì sopra, ladro di gallerie?"
    icaro "Da prima di voi. La porta l'avete sbarrata con me dentro. Errore di metodo."
    menu:
        "Icaro scende, svelto e silenzioso. Druso diventa rosso fino alla barba."
        "«Icaro, se racconti questa cosa, racconto io della tua pipa.»":
            show icaro irritato with qdiss
            icaro "...accordo. Non ho visto niente. E tu non hai visto cosa c'è nella mia pipa."
            show druso ghigno with qdiss
            druso "Guarda guarda. Ricatto di prima mattina. Mi piaci sempre di più, e non è un complimento."
        "«Resta. Ci serve qualcuno da atterrare.»":
            show icaro neutro with qdiss
            icaro "Io non mi faccio atterrare. Io osservo."
            "Osserva. Per mezz'ora corregge Druso dal bordo: il peso, il gomito, il piede. Ha ragione su tutto, ed è insopportabile."
            druso "Ecco perché madre lo adora. Ha sempre ragione e non suda mai."
        "Ignorarlo e continuare la lezione":
            "Continuo. Druso esita, poi torna alla presa. Davanti al fratello. Senza battute."
            show icaro sereno with qdiss
            icaro "...hm. Non me l'aspettavo."
            "Icaro se ne va senza dire altro. Lascia la porta aperta, apposta."
    hide icaro with dissolve
    show druso serio with qdiss
    "Quando la luce arriva alle finestre, Druso fa la torsione giusta. Una volta sola. Su di me."
    with vpunch
    "Mi ritrovo per terra con la segatura in bocca."
    show druso ghigno with qdiss
    druso "Oh. Oh! Ha funzionato! Scusa. Non scusa. Lo rifaccio?"
    druso "Non dirlo in taverna. Anzi: dillo. Ma di' che ho vinto con lo charme."
    return


## Evento 4 — La guardia #####################################################

label druso_ev4:
    scene bg vicoli_zefiro with fade
    show druso neutro at left with dissolve
    "Turno di guardia sulle mura di Zefiro, ultimo scalino prima del Nord vero. Druso si è offerto volontario. Il capoguardia ha chiesto se fosse malato."
    "Il vento arriva dai ghiacciai senza niente in mezzo. Sotto di noi, i tetti di Zefiro fumano come pentole."
    druso "Zitto, il vento ascolta. Notte lunga, lanterna corta. Si fa un patto: chi si addormenta paga il giro. O recita."
    druso "Per scaldarci, una cosa leggera. «Sulle mura di Zefiro c'è una guardia sola: ha freddo ai piedi e altro alla...» No. Non stanotte."
    "Per due ore il provocatore non provoca. Conta le torce sulla Calà, nomina le stelle sbagliate, e ogni tanto si zittisce a metà frase."
    druso "Quella è la Lepre. No, il Carro. È il Carro che insegue la Lepre. Icaro le sa tutte, io le invento. Vengono meglio."
    "Una civetta si alza dal cornicione. Druso trasale così forte che la lanterna oscilla."
    menu:
        "Un'ombra sul cammino di ronda. Druso afferra la lanterna e non fa battute."
        "«Dimmi cosa c'è. Senza rima.»":
            $ druso_affinity += 1
            show druso serio with qdiss
            druso "...ho paura del buio, ecco. Dei cento chili e della barba, del buio. Dillo e ti butto di sotto."
            druso "Da piccolo madre ci chiudeva in cantina, uno alla volta. Per temprarci. Caino ne usciva muto. Icaro ne usciva con qualcosa in tasca."
            druso "Io ne uscivo cantando. Ad alta voce, per non sentire. È lì che ho imparato a rimare."
            "Resto con lui fino all'alba, a un passo, senza dire niente. Il sole sorge sul suo ghigno: per una volta stanco, e vero."
        "Prenderlo in giro: «Il coraggioso Druso e le sue ombre»":
            $ druso_passo_falso()
            show druso irritato with qdiss
            druso "Ah. Bene. Questa me la segno nel registro delle cose che non perdono."
            "Il resto della guardia lo passa a recitare versi osceni al vento, rivolto verso la città. Mai verso di me."
            "Il capoguardia, all'alba, ci trova a dieci passi di distanza. Chiede se abbiamo litigato. Druso dice di no, troppo in fretta."
        "Mettersi in silenzio al suo fianco":
            show druso imbarazzato with qdiss
            druso "...grazie. Non lo dirò mai più. Né a te, né alla taverna."
            "L'ombra era un gatto. Lo sappiamo tutti e due. Nessuno dei due lo dice."
            "Il turno finisce all'alba. Non succede niente, ed è la cosa più importante."
    return


## Impegno (scelta del cuore) ################################################

label impegno_druso:
    scene bg vicoli_zefiro with fade
    show druso imbarazzato at left with dissolve
    "Mi aspetta fuori dalla taverna, per una volta senza pubblico. Ha in mano un foglio piegato in quattro, e l'aria di chi preferirebbe un TESCHIO."
    "Dentro, qualcuno grida il suo nome per il solito giro di versi. Lui non si gira."
    druso "Ho scritto una cosa. Non oscena. È... il problema è proprio questo, che non è oscena. Prima di dartela devo sapere se ridi."
    druso "Ci ho messo tre notti. Le altre le scrivo in tre minuti, sul tovagliolo. Questa no. Questa non voleva venire."
    "Il foglio trema appena. Il poeta del disagio altrui, in imbarazzo per la prima volta da che lo conosco."
    menu:
        "«Perché il poema più bello non nasce dall'immaginazione.»"
        "Prendere il foglio senza ridere" (peso=True):
            $ impegno_esito = True
            "Lo leggo. Parla di un percorso che si fa assieme, di un'intesa che non ha bisogno di provocazioni. Rima baciata, naturalmente."
            "Ci sono la taverna, le mura di Zefiro, il ponte sul canale. E ci sono io, senza nome, in ogni strofa."
            show druso ghigno with qdiss
            druso "Allora? Metrica zoppa? Contenuto peggio? Di' qualcosa o DICHIARO."
            pc "Bis."
            druso "...bis concesso. A vita, se serve."
            "Dentro, la taverna continua a chiamarlo. Lui le volta le spalle e mi offre il braccio, con un inchino ridicolo."
        "Restituirlo chiuso" (peso=True):
            $ impegno_esito = False
            $ congelate.add("druso")
            druso "Giusto. Che stupidaggine. Era uno scherzo, ovvio! Il finto sentimento: il mio capolavoro!"
            "Ride forte. Troppo forte. E da quella sera le sue poesie tornano oscene, e mai più su di me."
    return


## Luna V — La sfida dei versi (fisso V/6 sera) ##############################

label druso_luna5:
    scene bg vicoli_zefiro with fade
    "Taverna piena. Sera di sfida: due poeti, un boccale a testa, e la sala che fa da giuria."
    "Qualcuno ha scritto le quote su una lavagna. Druso parte favorito, tre a uno. Sotto, in calligrafia minuta: «Icaro punta sullo sfidante.»"
    show druso ghigno at left with easeinleft
    druso "Stasera mi batto. Non per la gloria, per il conto. Chi perde paga il giro a tutta Zefiro."
    druso "Tu sta' vicin[fin]. La spalla del poeta deve essere a portata di gomito. E di boccale, se vinco."
    "Lo sfidante è Lisandro, Filius del Ramo di Iperione. Mantello pulito, voce da tempio, mani che non hanno mai alzato un boccale."
    "Druso apre la sfida con una strofa sulle vergini del tempio di Iperione. La sala ruggisce. Lisandro sorride appena."
    "Poi tocca a lui. Non ride, non urla. Recita piano."
    "«Cento chili di Lenora, e nessuno che la onora. Grida rime nei bordelli: le sa dire solo a quelli.»"
    with hpunch
    "La sala esplode. Lisandro continua, sottovoce."
    if flag_druso_coraggio:
        "La rissa nei vicoli. Il lanternaio. «Il coraggio di un giorno, comprato a credito.»"
    else:
        "I versi di Druso, uno per uno, recitati con la faccia di chi annusa del latte andato a male. Poi sua madre. «Una Capofamiglia che governa il Nord e non sa governare un figlio.»"
    show druso sorpreso with qdiss
    "Druso apre la bocca. Non esce niente."
    show druso irritato with qdiss
    druso "Io... la metrica, è zoppa. La terza strofa, zoppa..."
    "Nessuno lo sente. Per la prima volta da che lo conosco, il pubblico non è suo."
    menu:
        "Lisandro alza il boccale verso di me. «La sua spalla vuole dire qualcosa?»"
        "«Sì. Due versi. Poi la parola torna a lui.»":
            $ druso_sfida = "verso"
            $ druso_affinity += 1
            pc "Lisandro d'Iperione, voce bella e mano vuota. Ha studiato tanto il verso: mai provato quello che conta."
            "Mezza sala ride. L'altra mezza si gira verso Druso, che ha già il boccale in mano."
            show druso ghigno with qdiss
            druso "...e la chiusa la tengo io, grazie. Lisandro, caro: la tua musa è tua cugina, e lo sanno anche le galline."
            with vpunch
            "Il tavolo trema. Lisandro paga il giro senza una parola."
            druso "Mi hai rubato l'attacco, linguaccia. Te lo perdono solo perché era sporco come piace a me."
            "Sulla lavagna, qualcuno cancella le quote. Icaro, dal fondo, alza la pipa verso di noi: ha perso, e sembra contento."
        "Prenderlo per il braccio: «Andiamo. Non ne vale la pena.»":
            $ druso_sfida = "via"
            $ druso_passo_falso()
            show druso serio with qdiss
            "Si lascia portare fuori. È quello il peggio: si lascia portare."
            druso "Bell'uscita. Così domani Zefiro dice che il poeta l'hanno raccolto col cucchiaino."
            druso "La pietà tienila per i cani, [figlio_t] di Briseide. Io sono ancora in piedi."
            "Dietro di noi, la taverna canta la strofa di Lisandro. In coro, e già stonata."
        "Restare al tavolo, in silenzio. Tocca a lui.":
            $ druso_sfida = "silenzio"
            show druso irritato with qdiss
            "Lo guardo e non mi muovo. Druso si alza, rosso fino alla barba."
            druso "Una strofa. Una sola. Lisandro, il tuo Ramo ha più eunuchi che lance."
            "Fiacca. La sala ride lo stesso, per pietà. Druso paga il giro."
            druso "Comodo, il tuo silenzio. Sedut[fin] in prima fila a guardarmi annegare."
            "Ma all'uscita mi aspetta. Non dice niente. Mi cammina accanto fino al ponte, come se dovessi ancora rispondere."
    return


## Fiaccolata (route attiva) #################################################

label druso_fiaccolata:
    scene bg cala_notte with fade
    show druso ghigno at left with dissolve
    "La Calà, trecento gradini di lanterne. Druso li guarda come un palco."
    "Coppie ovunque, mani intrecciate, sciarpe. Qualche Figlio di Glauco finge di essere lì per caso."
    druso "Guarda quanta gente innamorata. Mi viene un'ode. Si intitola «Trecento gradini per arrivare a letto stanchi»."
    druso "La leggenda dice mano nella mano. Io dico che la leggenda non ha mai visto le TUE mani: ruvide come la mia poesia."
    "Ma la mano la tende lui. E per trecento gradini il provocatore più insopportabile del Nord non provoca nessuno: cammina, stringe, e ogni venti gradini controlla che io ci sia ancora."
    "Al gradino cento passa Caino, solo. Vede le nostre mani. Alza un sopracciglio, uno solo, e prosegue."
    druso "Domani lo saprà tutta la Rocca. Caino non parla, ma il suo sopracciglio è un banditore."
    show druso imbarazzato with dissolve
    druso "Se lo racconti in taverna, nego. Ho una reputazione. ...al gradino duecento puoi raccontare quello che vuoi."
    "In cima, la lanterna nostra è l'unica storta. Druso dice che è voluto. Che è arte."
    $ druso_affinity += 1
    return


## Luna VI — La lettera del Ramo (fisso VI/5 sera) ###########################

label druso_luna6:
    scene bg vicoli_zefiro with fade
    "Il Becco Storto, a porte chiuse. L'oste è andato a dormire e ha lasciato a Druso le chiavi, una candela e una bottiglia."
    show druso serio at left with dissolve
    "Sul tavolo c'è una lettera. Cera nera, il sigillo del Ramo di Lenora: un corvo su un ramo spoglio."
    druso "È arrivata stamattina. L'ho aperta stasera. Il coraggio, sai, ha i suoi orari."
    druso "Convocazione. Davanti al Ramo, tra due settimane. Motivo: «condotta». Una parola sola, e ci sta dentro tutta la mia vita."
    "La candela fa tremare le ombre sulla barba. Ha l'aria di uno che non dorme da due notti."
    druso "Madre non scrive mai. Fa scrivere un Eparca. Questa però l'ha firmata lei. Guarda: la L con la coda lunga."
    pc "È un buon segno o un cattivo segno?"
    druso "Con madre non ci sono segni. Ci sono solo verdetti, e i verdetti li capisci dopo."
    "Beve. Posa il bicchiere senza finirlo. È la prima volta che glielo vedo fare."
    show druso ghigno with qdiss
    druso "Ho già pronta la difesa, comunque. In rima. Undici strofe sul decoro. Vuoi sentire l'attacco?"
    druso "«Decoro, decoro, sei come l'alloro: ti mettono in testa e ti seccano in coro.»"
    menu:
        "Mi guarda in attesa del verdetto, come se il Consiglio fossi già io."
        "«Fa schifo. Riscrivila. Con me.»":
            show druso sorpreso with qdiss
            druso "...fa schifo? Undici strofe! Ottave! Ci ho perso il sonno!"
            show druso ghigno with qdiss
            druso "Hai ragione. Fa schifo. Prendi la penna, linguaccia. Se dobbiamo affondare, che sia in metrica."
            "Scriviamo fino a tardi. Lui cancella ogni mio verso, poi lo rimette, cambiandogli una parola sola per poter dire che è suo."
        "«Non portarti una poesia. Portati te stesso.»":
            show druso irritato with qdiss
            druso "Me stesso? Hai visto me stesso? Cento chili di debiti, versi e paura. Non è una difesa: è una confessione."
            show druso serio with qdiss
            druso "...però è vero. È l'unica cosa che non si può fischiare. Al massimo la si condanna."
        "Strappargli la lettera e bruciarla sulla candela":
            with hpunch
            "La cera nera sfrigola. L'odore di carta bruciata riempie la taverna vuota."
            show druso sorpreso with qdiss
            druso "Hai appena bruciato una convocazione del Ramo di Lenora. Con la firma di madre sopra."
            show druso ghigno with qdiss
            druso "È la cosa più maleducata che abbia mai visto fare. Ci vado lo stesso, ovvio. Ma ci vado di umore migliore."
    show druso neutro with qdiss
    druso "Caino mi ha detto di stare zitto. Icaro mi ha detto di scappare. Hanno ragione tutti e due, ed è per questo che non li ascolto."
    druso "Tu verrai? Non per difendermi. Per esserci. In fondo alla sala, dove mettono i Figli che non contano."
    pc "In fondo alla sala. Dove ti vedo."
    show druso imbarazzato with dissolve
    druso "...ecco. Sì. Quello."
    "Spegne la candela con le dita, senza fare una smorfia. Nel buio lo sento ridere piano, una volta."
    druso "Al buio non ho più paura, lo sai? Da un po'. Dipende da chi c'è."
    return


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
    # Routing (rl.finale_druso): druso_good -> druso_neutral -> druso_bad.
    $ cal_finale = rl.finale_druso(druso_affinity, flag_druso_coraggio)
    jump expression cal_finale

label druso_good:
    show druso ghigno at left with qdiss
    druso "Confermo tutto, madre. Il decoro, la rissa, [il_t] Figli[fin] di Briseide. E aggiungo un componimento in tema, se il Consiglio gradisce. Rima baciata."
    "Un Eparca si alza per protestare. Caino, senza voltarsi, gli posa una mano sul braccio. L'Eparca si risiede."
    "Lo recita. Davanti a Lenora, agli Arconti, al Nord intero. Il poema non osceno. Il mio."
    "Dentro ci sono cose che sappiamo solo noi due. Nessuno in sala capisce. Io sì."
    "La sala non ride. La sala — che gli Asi la conservino — applaude."
    "Da dietro la grata, una sola parola: «Bis.»"
    show druso sorpreso with qdiss
    "Druso resta a bocca aperta. Per la prima volta in vita sua, non ha la chiusa pronta."
    "Icaro, accanto a Caino, mormora qualcosa. Dal labiale sembra «ho perso un'altra scommessa». Sembra felice."
    scene bg cala_notte with fade
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
    "Ne esce con una battuta, come sempre. E come sempre, la battuta è un muro."
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
