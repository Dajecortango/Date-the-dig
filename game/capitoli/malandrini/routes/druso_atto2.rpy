# Route Druso — Atto 2: evento 3-4, interludio 3, Lune V-VI.

## Evento 3 — Il coraggio che stupisce anche lui #############################

label druso_ev3:
    scene bg vicoli_zefiro with fade
    show druso neutro at left with dissolve
    "Mi trascina «a vedere una cosa» nei vicoli bassi di Zefiro. La cosa è un esattore dei tabarri Verdi che spreme un lanternaio: il mio, quello che fa credito a noi figli di Briseide."
    "Pomeriggio grigio. I balconi gocciolano neve sciolta. Nessuno guarda, perché a Zefiro guardare costa."
    druso "Brutto affare. Andiamocene. Non è il nostro Ceppo, non è il nostro problema, e io ci tengo ai miei denti."
    druso "Te li ho mostrati, i miei denti. Sono tutti lì. È un patrimonio di famiglia."
    "L'esattore ha un bastone ferrato. Il lanternaio ha le mani sopra la testa e un occhio già chiuso."
    menu:
        "Il lanternaio è a terra. L'esattore conta."
        "Intervieni subito":
            $ druso_affinity += 2
            $ flag_druso_coraggio = True
            with vpunch
            "Due passi, il braccio dell'esattore, la torsione che Aede insegna ai novellini. E dal nulla un ruggito."
            show druso ghigno with qdiss
            druso "TESCHIO, BRUTTO STRACCIONE!"
            "Druso, il codardo dichiarato, addosso all'esattore con tutti i suoi settanta chili, la barba e nessun piano."
            with hpunch
            "Rotolano nel fango. Druso morde. Proprio così: morde un orecchio, e l'esattore scappa urlando verso il canale."
            "Dopo, mentre il lanternaio ci benedice in tre dialetti, Druso si annusa le mani."
            show druso imbarazzato with qdiss
            druso "...non dirlo a nessuno. Il coraggio mi rovina la reputazione peggio della gratitudine."
            druso "E se lo dici, di' che l'ho fatto per noia. Che il mio corpo si è mosso da solo."
            pc "Hai morso un uomo, Druso."
            druso "Sapeva di cipolla. Sarà nel poema. Il morso, non la cipolla."
        "Dagli retta e andate via":
            $ druso_affinity -= 1
            show druso serio with qdiss
            "Ce ne andiamo, e per tutta la strada Druso non fa battute. È la cosa più vicina al disprezzo che gli abbia mai visto addosso, e non so se è per me o per sé."
            "Al ponte si ferma e guarda indietro verso il vicolo, un piede già girato."
            druso "...niente. Mi era sembrato di aver dimenticato qualcosa."
    return


## Interludio 3 — La lezione segreta #########################################

label druso_int3:
    scene bg palestra with fade
    "Palestra della Rocca, prima dell'alba, le torce sono ancora spente. Qualcuno ha sbarrato la porta dall'interno."
    show druso imbarazzato at left with dissolve
    "Quel qualcuno è Druso, in camicia da notte e stivali, con due spade sotto il braccio."
    druso "Zitt[fin]. Non una parola. Se qualcuno chiede, sono qui per sonnambulismo."
    druso "Quella torsione. Quella del vicolo. Quella che fa Aede. Insegnamela."
    pc "Il codardo dichiarato vuole imparare a combattere?"
    show druso irritato with qdiss
    druso "Il codardo dichiarato vuole smettere di combattere a morsi. È poco elegante. E l'orecchio di quello aveva un sapore che sento ancora."
    "Gli mostro la presa e lui sbaglia. Gliela rimostro: sbaglia peggio, ma ride."
    show icaro furbo at right with dissolve
    "Una voce dal soppalco. Icaro, seduto a gambe incrociate sulle travi, la pipa spenta tra i denti."
    icaro "Interessante. Mio fratello sveglio prima di mezzogiorno, sobrio, e in palestra. Devo avvisare un Arvale?"
    show druso sorpreso with qdiss
    druso "Da quanto sei lì sopra, ladro di galline?"
    icaro "Da prima di voi. La porta l'avete sbarrata con me dentro. Errore di distrazione."
    menu:
        "Icaro scende, svelto e silenzioso. Druso diventa rosso fino alla barba."
        "«Icaro, se racconti questa cosa, io racconto della tua pipa.»":
            show icaro irritato with qdiss
            icaro "...d'accordo. Non ho visto niente. E tu non hai visto cosa c'è nella mia pipa."
            show druso ghigno with qdiss
            druso "Guarda guarda, ricatto di prima mattina. Mi piaci sempre di più, e non è un complimento."
        "«Resta. Ci serve qualcuno da atterrare.»":
            show icaro neutro with qdiss
            icaro "Io non mi faccio atterrare. Io osservo."
            "Osserva. Per mezz'ora corregge Druso dal bordo: il peso, il gomito, il piede. Ha ragione su tutto, ed è insopportabile."
            druso "Ecco perché madre lo adora. Ha sempre ragione e non suda mai."
        "Ignoralo e continua la lezione":
            "Continuo. Druso esita, poi torna alla presa davanti al fratello e senza battute."
            show icaro sereno with qdiss
            icaro "...hm. Non me l'aspettavo."
            "Icaro se ne va senza dire altro. Lascia la porta aperta, apposta."
    hide icaro with dissolve
    show druso serio with qdiss
    "Quando la luce arriva alle finestre, Druso fa la torsione giusta. Una volta sola. Su di me."
    with vpunch
    "Mi ritrovo per terra con la segatura in bocca."
    show druso ghigno with qdiss
    druso "Oh. Oh! Ha funzionato! Scusa. No, niente scuse. Lo rifaccio?"
    druso "Non dirlo in taverna. Anzi: dillo. Ma di' che ho vinto con lo charme."
    return


## Evento 4 — La guardia #####################################################

label druso_ev4:
    scene bg vicoli_zefiro with fade
    show druso neutro at left with dissolve
    "Turno di guardia sulle mura di Zefiro, ultimo scalino prima del Nord vero. Druso si è offerto volontario. Il capoguardia ha chiesto se fosse malato."
    "Il vento arriva dai ghiacciai senza niente in mezzo. Sotto di noi, i tetti di Zefiro fumano come pentole."
    druso "Zitt[fin], il vento ascolta. Notte lunga, lanterna corta. Si fa un patto: chi si addormenta paga il giro. O recita."
    druso "Per scaldarci, una cosa leggera. «Sulle mura di Zefiro c'è una guardia sola: ha freddo ai piedi e pure alla...» No. Non stanotte."
    "Per due ore, nemmeno una strofa sconcia. Conta le torce sulla Calà, nomina le stelle sbagliate, e ogni tanto si zittisce a metà frase."
    druso "Quella è la Lepre. No, il Carro. È il Carro che insegue la Lepre. Icaro le sa tutte, io le invento. Vengono meglio."
    $ muovi("druso", "sobbalzo")
    "Una civetta si alza dal cornicione. Druso trasale così forte che la lanterna oscilla."
    menu:
        "Un'ombra sul cammino di ronda. Druso afferra la lanterna e non fa battute."
        "«Dimmi cosa c'è. Senza rima.»":
            $ druso_affinity += 1
            $ druso_cantina_detta = True
            show druso serio with qdiss
            druso "...ho paura del buio, ecco. Dillo e ti butto di sotto."
            druso "Appena adottati mia madre ci chiudeva in cantina, uno alla volta. Per temprarci. Caino ne usciva muto. Icaro ne usciva con qualcosa in tasca."
            druso "Io ne uscivo cantando ad alta voce, per farmi coraggio. È lì che ho imparato a rimare."
            "Resto con lui fino all'alba, a un passo, senza dire niente. Il sole sorge sul suo ghigno, stanco per una volta."
        "Prendilo in giro: «Il coraggioso Druso e le sue ombre»":
            $ druso_passo_falso()
            show druso irritato with qdiss
            druso "Ah. Bene. Questa me la segno nel registro delle cose che non perdono."
            "Il resto della guardia lo passa a recitare versi osceni al vento, rivolto verso la città. Mai verso di me."
            "Il capoguardia, all'alba, ci trova a dieci passi di distanza. Chiede se abbiamo litigato. Druso dice di no, troppo in fretta."
        "Mettiti in silenzio al suo fianco":
            show druso imbarazzato with qdiss
            druso "...grazie. Non lo dirò mai più. Né a te, né alla taverna."
            "L'ombra era un gatto, lo sappiamo tutti e due. Nessuno dei due lo dice."
            "Il turno finisce all'alba e non succede niente."
    return


## Luna V — La sfida dei versi (fisso V/6 sera) ##############################

label druso_luna5:
    scene bg vicoli_zefiro with fade
    "Taverna piena. Sera di sfida: due poeti, un boccale a testa, e la sala che fa da giuria."
    "Qualcuno ha scritto le quote su una lavagna. Druso parte favorito, tre a uno. Sotto, in calligrafia minuta: «Icaro punta sullo sfidante.»"
    show druso ghigno at left with easeinleft
    druso "Stasera mi batto. Non per la gloria, per il conto. Chi perde paga il giro a tutta Zefiro."
    druso "Tu sta' vicin[fin]. La spalla del poeta deve essere a portata di gomito. E di boccale, se vinco."
    "Lo sfidante è Epiro, Filius del Ramo di Iperione. Mantello pulito, voce baritonale, mani che non hanno mai alzato un boccale."
    "Druso apre la sfida con una strofa sulle vergini del Convitto di Proserpina. La sala ruggisce. Epiro sorride appena."
    "Tocca a lui. Non ride, non urla, recita piano."
    "«Poca arguzia il figlio di Lenora, non è nessuno che la onora. Grida rime nei bordelli: le sa dire solo a quelli.»"
    with hpunch
    "La sala esplode. Epiro continua, sottovoce."
    if flag_druso_coraggio:
        "La rissa nei vicoli. Il lanternaio. «Il coraggio di un giorno, comprato a credito.»"
    else:
        "I versi di Druso, uno per uno, recitati con la faccia di chi annusa del latte andato a male. Poi sua madre. «Una Capofamiglia che governa il Nord e non sa governare un figlio.»"
    show druso sorpreso with qdiss
    "Druso apre la bocca. Non esce niente."
    show druso irritato with qdiss
    druso "Io... la metrica, è zoppa. La terza strofa, zoppa..."
    "Nessuno lo sente. Al tavolo accanto, due carrettieri ripetono già la strofa di Epiro, per impararla."
    menu:
        "Epiro alza il boccale verso di me. «La sua spalla vuole dire qualcosa?»"
        "«Sì. Due versi. Poi la parola torna a lui.»":
            $ druso_sfida = "verso"
            $ druso_affinity += 1
            pc "Epiro d'Iperione, voce bella e mano vuota. Ha studiato tanto il verso: mai provato quello che conta."
            "Mezza sala ride. L'altra mezza si gira verso Druso, che ha già il boccale in mano."
            show druso ghigno with qdiss
            druso "...e la chiusa la tengo io, grazie. Epiro, caro: la tua musa è tua cugina, per questo nessuno la avvicina."
            with vpunch
            "Il tavolo trema. Epiro paga il giro."
            druso "Mi hai rubato l'attacco, linguaccia. Te lo perdono solo perché era sporco come piace a me."
            "Sulla lavagna, qualcuno cancella le quote. Icaro, dal fondo, alza la pipa verso di noi: ha perso, e sembra contento."
        "Prendilo per il braccio: «Andiamo. Non ne vale la pena.»":
            $ druso_sfida = "via"
            $ druso_passo_falso()
            show druso serio with qdiss
            "Si lascia portare fuori. È quello il peggio: si lascia portare."
            druso "Bell'uscita. Così domani Zefiro dice che il poeta l'hanno raccolto col cucchiaino."
            druso "La pietà tienila per i cani, [figlio_t] di Briseide. Io sono ancora in piedi."
            "Dietro di noi, la taverna canta la strofa di Epiro. In coro, e già stonata."
        "Resta al tavolo, in silenzio. Tocca a lui.":
            $ druso_sfida = "silenzio"
            show druso irritato with qdiss
            "Lo guardo e non mi muovo. Druso si alza, rosso fino alla barba."
            druso "Una strofa. Una sola. Epiro, il tuo Ramo ha più eunuchi che lance."
            "Fiacca. La sala ride lo stesso, per pietà. Druso paga il giro."
            druso "Comodo, il tuo silenzio. Sedut[fin] in prima fila a guardarmi annegare."
            "All'uscita però mi aspetta, e senza dire niente mi cammina accanto fino al ponte, come se dovessi ancora rispondere."
    return


## Fiaccolata (route attiva) #################################################

label druso_fiaccolata:
    scene bg cala_notte with fade
    show druso ghigno at left with dissolve
    "La Calà, trecento gradini di lanterne. Druso li guarda come un palco."
    "Coppie ovunque, mani intrecciate. Qualche Figlio di Glauco finge di essere lì per caso."
    druso "Guarda quanta gente innamorata. Mi viene un'ode. Si intitola «Trecento gradini per arrivare a letto stanchi»."
    druso "La leggenda dice mano nella mano. Io dico che la leggenda non ha mai visto le TUE mani: ruvide come la mia poesia."
    "Ma la mano la tende lui. Per trecento gradini non dice una sola porcheria: cammina, stringe le mie dita, e ogni venti gradini si gira a controllare che io voglia scendere ancora."
    "Al gradino cento passa Caino, solo. Vede le nostre mani. Alza un sopracciglio, uno solo, e prosegue."
    druso "Domani lo saprà tutta la Rocca. Caino non parla, ma il suo sopracciglio è un banditore."
    show druso imbarazzato with dissolve
    druso "Se lo racconti in taverna, nego. Ho una reputazione. ...al gradino duecento puoi raccontare quello che vuoi."
    menu:
        "Mi stringe la mano più forte, come se la risposta passasse da lì."
        "«Lo racconto eccome. In rima. Peggio delle tue.»":
            $ druso_affinity += 1
            show druso ghigno with qdiss
            druso "Peggio delle mie è impossibile. Ma ti concedo il tentativo. E i diritti."
        "«Non lo saprà nessuno. Promesso.»":
            show druso neutro with qdiss
            druso "Promesso. Che parola noiosa. ...tienila lo stesso."
            "Il resto della salita lo fa in silenzio. Non so se l'ho deluso o l'ho calmato. Con Druso, a volte, è uguale."
    "In cima, la nostra lanterna è l'unica storta. Druso dice che è voluto. Che è arte."
    return


## La crocetta (fisso V/20 sera) ##############################################

label druso_crocetta:
    scene bg vicoli_zefiro with fade
    "Il Becco Storto, due settimane dopo Epiro. La taverna canta ancora la sua strofa, e quando entra Druso la canta più piano."
    if druso_sfida == "verso":
        "Quella sera ha vinto lui, con due versi miei in testa. Zefiro l'ha notato. «Il poeta ha una spalla che rima meglio di lui», dicono, e gli pagano il giro per vederlo bere."
    elif druso_sfida == "via":
        "Il poeta raccolto col cucchiaino: l'aveva previsto lui, e gliel'hanno ripetuto in tutti i dialetti del canale."
    else:
        "Ha pagato il giro a tutta Zefiro, e a Zefiro il giro è piaciuto. Adesso glielo chiedono ogni sera."
    show druso ghigno at left with easeinleft
    "Stasera sale sul tavolo con una pergamena in mano. Calligrafia minuta, nomi, frecce: l'ho vista una volta sola, su una botte, con la porta chiusa."
    druso "Signori! Basta Epiro. Stasera si legge il libro mastro di Druso, figlio di Lenora. Cose vere, coi nomi!"
    druso "L'oste: annacqua, ma con vergogna. Il capoguardia: dorme in piedi e sogna la moglie del fornaio. Il fornaio: lo sa."
    "La sala si raddrizza sulle panche. Sono due settimane che non ride con lui. Scorre il dito fino in fondo, e il dito si ferma."
    if druso_leva == "morde":
        druso "[player_name], [figlio_t] di Briseide. Accanto, una crocetta. Sapete cosa vuol dire, la crocetta? Vuol dire: morde."
        "Me l'aveva mostrata di sfuggita, come si mostra una cosa che non si fa vedere a nessuno. «Non ne ho tante, di crocette.»"
        druso "«Morde, dice la crocetta, la mia spalla prediletta: morde il cuscino, la notte, perché nessuno l'aspetta.»"
    else:
        druso "[player_name], [figlio_t] di Briseide. Accanto non c'è una crocetta. C'è scritto: abbaia."
        "Non avevo mai saputo cosa ci avesse scritto. Lo so adesso, insieme a sessanta persone."
        druso "«Abbaia, dice il mio foglio, la mia spalla prediletta: abbaia sotto il cuscino, perché nessuno l'aspetta.»"
    with hpunch
    "Il tavolo trema. È la risata che gli mancava, e gli torna il colore in faccia mentre la prende."
    "Mi cerca tra le panche. Non si scusa con gli occhi: controlla."
    menu:
        "Sessanta facce si girano. Qualcuno mi versa da bere, per vedere cosa faccio."
        "Sali sul tavolo accanto e rispondigli in rima":
            $ druso_rottura = "risposta"
            $ druso_affinity += 1
            "Il tavolo è bagnato e più alto di quanto sembrasse. Gli arrivo alla spalla."
            pc "«Druso conosce il mio letto come conosce il coraggio: per sentito dire, in rima, e sempre di passaggio.»"
            with vpunch
            "Questa volta il tavolo trema per me. Druso apre la bocca. Poi alza il boccale, senza guardarmi, e la sala decide che è finita alla pari."
        "Posa il bicchiere ed esci senza dire niente":
            $ druso_rottura = "uscita"
            $ druso_affinity -= 1
            "Non sbatto la porta. Dietro di me riprende a leggere, e il capoguardia ride più forte di tutti."
            "Tre giorni dopo trovo un angolo di pergamena sul banco dove mangio. Il mio nome, il resto strappato. Nessun biglietto."
            return
        "Ridi con gli altri e alza il bicchiere":
            $ druso_rottura = "risata"
            $ druso_passo_falso()
            "Rido. Bevo. Qualcuno mi dà una pacca sulla schiena."
            show druso serio with qdiss
            "Druso mi guarda ridere un momento di più. Poi passa al nome dopo, e non controlla più."
            return
    scene bg vicoli_zefiro with fade
    "Il retro del Becco Storto. Botti vuote, il canale ghiacciato, Lisandra che mi guarda dall'alto come una creditrice."
    show druso irritato at left with dissolve
    druso "«Per sentito dire.» Ti sei preparat[fin] o ti esce così?"
    if druso_leva == "morde":
        pc "Era l'unica riga buona che avevi scritto su di me."
    else:
        pc "Abbaia. L'hai scritto quella sera, e l'hai tenuto in tasca fino a oggi."
    "Si gratta la barba. Tira fuori la pergamena e la guarda come se fosse di un altro, poi se la rimette in tasca."
    show druso serio with qdiss
    druso "Epiro mi ha preso il nome. Mi serviva qualcosa da vendere stasera, e ho messo la mano in tasca. C'eri tu."
    druso "Non chiedermi di scusarmi. Non so come si fa, e verrebbe zoppa."
    return


## Luna VI — La lettera del Ramo (fisso VI/5 sera) ###########################

label druso_luna6:
    scene bg vicoli_zefiro with fade
    if druso_rottura == "uscita":
        "Non ci parliamo da due settimane. Stasera il garzone dell'oste mi ha portato una chiave e un biglietto con una parola sola: «Vieni.» Niente rima."
    "Il Becco Storto, a porte chiuse. L'oste è andato a dormire e ha lasciato a Druso le chiavi, una candela e una bottiglia."
    show druso serio at left with dissolve
    "Sul tavolo c'è una lettera. Cera nera, il sigillo del Ramo di Lenora: una corona."
    druso "È arrivata stamattina. L'ho aperta stasera. Il coraggio, sai, ha i suoi orari."
    druso "Convocazione. Davanti al Ramo, tra due settimane. Motivo: «condotta». Una parola sola, e ci sta dentro tutta la mia vita."
    "La candela fa tremare le ombre sulla barba. Ha l'aria di uno che non dorme da due notti."
    druso "Madre non scrive mai. Fa scrivere un segretario. Questa però l'ha firmata lei. Guarda: la L con la coda lunga."
    pc "È un buon segno o un cattivo segno?"
    druso "Con madre non ci sono segni. Ci sono solo verdetti, e i verdetti li capisci dopo."
    "Beve. Posa il bicchiere a metà e lo spinge lontano col dorso della mano."
    show druso ghigno with qdiss
    druso "Ho già pronta la difesa, comunque. In rima. Undici strofe sul decoro. Vuoi sentire l'attacco?"
    druso "«Decoro, decoro, sei come l'alloro: ti mettono in testa, ma ti secchi per colpa loro.»"
    menu:
        "Mi guarda in attesa del verdetto, come se il Consiglio fossi già io."
        "«Fa schifo. Riscrivila. Con me.»":
            $ druso_difesa = "riscrivi"
            show druso sorpreso with qdiss
            druso "...fa schifo? Undici strofe! Ottave! Ci ho perso il sonno!"
            show druso ghigno with qdiss
            druso "Hai ragione. Fa schifo. Prendi la penna, linguaccia. Se dobbiamo affondare, che sia in metrica."
            "Scriviamo fino a tardi. Lui cancella ogni mio verso, poi lo rimette, cambiandogli una parola sola per poter dire che è suo."
        "«Non portarti una poesia. Porta te stesso.»":
            $ druso_difesa = "se_stesso"
            show druso irritato with qdiss
            druso "Me stesso? Hai visto me stesso? Sono fatto di debiti, versi e paura. Non è una difesa: è una confessione."
            show druso serio with qdiss
            druso "...però è vero, maledizione. Una poesia la FISCHIANO. Uno in carne e ossa, al massimo lo impiccano."
        "Strappagli la lettera e bruciala sulla candela":
            $ druso_difesa = "brucia"
            with hpunch
            "La cera nera si scioglie. L'odore di carta bruciata riempie la taverna vuota."
            show druso sorpreso with qdiss
            druso "Hai appena bruciato una convocazione del Ramo di Lenora. Con la firma di madre sopra."
            show druso ghigno with qdiss
            druso "È la cosa più maleducata che abbia mai visto fare. Ci vado lo stesso, ovvio. Ma ci vado di umore migliore."
    show druso neutro with qdiss
    druso "Caino dice: sta' zitto. Icaro dice: scappa. Un notaio e un topo, e io dovrei dar retta a QUESTI DUE? Piuttosto mi faccio gothi."
    druso "Tu verrai? Non per difendermi. Per esserci. In fondo alla sala, dove mettono i Figli che non contano."
    pc "In fondo alla sala. Dove ti vedo."
    show druso imbarazzato with dissolve
    druso "...ecco. Sì. Quello."
    "Spegne la candela con le dita, senza fare una smorfia. Nel buio lo sento ridere piano, una volta."
    druso "Al buio non ho più paura, lo sai? Da un po'. Dipende da chi c'è."
    return


## La cantina (fisso VI/12 sera) ##############################################

label druso_cantina:
    scene bg nero with fade
    "Una scala sotto la Rocca che non conosco, stretta, con i gradini consumati al centro. Druso va avanti con una lanterna e una chiave che ha vinto a Icaro, o che Icaro gli ha lasciato vincere."
    if druso_cantina_detta:
        druso "Te l'ho raccontata sulle mura. Eccola. Volevo vedere se è diventata più piccola."
    else:
        druso "Appena adottati, madre ci chiudeva qui. Uno alla volta. Per temprarci. Caino ne usciva muto, Icaro con qualcosa in tasca."
        druso "Io ne uscivo cantando. Ecco dove ho imparato a rimare, se te lo sei mai chiest[fin]."
    "La porta è bassa. Dentro ci sono rape, botti, un odore di pietra bagnata, e una stanza grande come un letto."
    druso "Uguale. Pensavo che almeno questa me la concedesse."
    druso "Tra nove giorni mi chiama davanti al Ramo. Ti ho detto che al buio non ho più paura. L'ho detto bene, c'era pure la candela. Vediamo se è vero."
    "Soffia sulla lanterna."
    "Aspetto la canzone. Sento il grasso del lucignolo che sfrigola, una goccia da qualche parte, e nient'altro."
    menu:
        "Druso non canta. Lo sento respirare a un passo da me. Forse due."
        "Cerca la sua mano":
            $ druso_cantina_esito = "mano"
            "La trovo al secondo tentativo, dopo una botte. È fredda e non stringe. Poi stringe, e non la smette più."
            druso "Questa non si racconta."
        "Canta tu, la più oscena che conosci":
            $ druso_cantina_esito = "canta"
            "Attacco quella sulla locandiera, che ho imparato da lui a forza di sentirla. Stono al secondo verso, e lui mi corregge per principio."
            druso "Fa schifo. E la metrica è mia, ladr[fin]. Ricomincia, più piano. Qui l'eco è una spia."
            "La finiamo in due, a voce bassa, tutte le strofe."
        "Resta ferm[fin] e non dire niente":
            $ druso_cantina_esito = "fermo"
            "Conto le gocce. A quaranta perdo il conto, e ricomincio."
            druso "Sei ancora lì?"
            pc "Sì."
            druso "Bene. Non aggiungere altro. Rovini il finale."
    "Non riaccende. Risaliamo a tentoni, lui davanti, e sulla scala lo sento contare i gradini a mezza voce: gli stessi di allora, immagino."
    show druso ghigno at left with dissolve
    "In cima la luce delle torce lo prende in faccia. Si rimette il ghigno come uno si rimette il mantello."
    druso "Se lo racconti in taverna, nego. Dico che ero ubriaco, e che piangevi tu."
    return


## Deviazione (Luna III+) — L'udienza privata ##################################

label druso_udienza:
    scene bg esterno_neve with fade
    "Rocca Tempesta, cortile dei carri. La neve è battuta, sporca di fango e di paglia. Druso mi ha chiesto di aspettarlo qui. «Fuori. Lontano dalle finestre.»"
    "Sua madre l'ha convocato, e non all'udienza dei Figli, quella con la grata e la fila: da solo, nella stanza dove Lenora riceve chi le deve qualcosa."
    "Passa una campana intera. Un carro parte, un altro arriva. Conto i corvi sulle merlature: undici, poi nove."
    show druso serio at left with dissolve
    "Esce senza boccale e senza ghigno. Cammina dritto, troppo dritto, come chi ha bevuto e non vuole farlo vedere. Solo che non ha bevuto."
    druso "Eccoti. Bene. Hai le mani fredde? Le mie sono di qualcun altro, al momento."
    "Si siede su uno scranno accanto a un carro, di spalle alla Rocca. Ogni tanto si volta a controllare che sia ancora lì."
    menu:
        "Druso non parla. Per lui, è un sintomo grave."
        "Raccogli una palla di neve e tiragliela in faccia":
            $ druso_udienza_esito = "neve"
            $ druso_affinity += 1
            with hpunch
            "Lo prendo in pieno. La neve gli si infila nella barba e nel colletto."
            show druso sorpreso with qdiss
            druso "Tu... davanti alla ROCCA... a un figlio di LENORA..."
            show druso ghigno with qdiss
            "Due palle tornano indietro prima che io finisca di ridere. La terza ha dentro un sasso. Dice che è stato un incidente artistico."
            druso "Grazie. Avevo bisogno di colpire qualcosa che non fosse mia madre."
        "«Cosa ti ha detto?»":
            $ druso_udienza_esito = "chiesto"
            druso "Che ho una vita di rime e zero di Virtù. Che il Ramo ha bisogno di un figlio, non di un giullare."
            druso "E che Caino, alla mia età, aveva già una carica. Lo dice sempre. Ormai è una rima obbligata."
            "Ride male, ma ride. Si alza e si scrolla la neve dai calzoni."
            druso "Non chiedermelo più, però. Le domande sincere mi fanno venire l'orticaria."
        "Siediti accanto a lui e aspetta":
            $ druso_udienza_esito = "aspettato"
            "Mi siedo accanto a lui. Non dico niente, e il niente dura a lungo."
            show druso neutro with qdiss
            druso "Lo sai cosa mi ha chiesto? Se ho qualcuno. Qualcuno di serio."
            druso "Le ho detto di no. Le ho mentito, credo. O forse no. Non lo so ancora."
            "Si alza per primo. Non mi guarda, ma mi porge la mano per tirarmi su."
    "Torniamo verso Zefiro insieme. A metà strada riprende a cantare, stonato, una canzone oscena sulla moglie di un Eparca."
    return
