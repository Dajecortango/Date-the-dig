# Eventi incrociati — il cast si incontra. Fissi, in fase libera (Lune II-IV).
# Economia: max +1 per personaggio a evento, opzioni mutuamente esclusive.

init python:
    EVENTI.extend([
        {"id": "trio_lenora", "label": "trio_lenora", "tipo": "fisso",
         "char": None, "luna": 2, "giorno": 15, "slot": "sera"},
        {"id": "incrocio_palestra", "label": "incrocio_palestra",
         "tipo": "fisso", "char": None, "luna": 3, "giorno": 16,
         "slot": "mattina"},
        {"id": "incrocio_carte", "label": "incrocio_carte", "tipo": "fisso",
         "char": None, "luna": 4, "giorno": 11, "slot": "sera"},
        # Incroci senza punti: solo testo diverso per scelta.
        {"id": "incrocio_debiti", "label": "incrocio_debiti", "tipo": "fisso",
         "char": None, "luna": 3, "giorno": 4, "slot": "mattina"},
        {"id": "incrocio_sorelle", "label": "incrocio_sorelle",
         "tipo": "fisso", "char": None, "luna": 3, "giorno": 25,
         "slot": "mattina"},
        {"id": "incrocio_serra", "label": "incrocio_serra", "tipo": "fisso",
         "char": None, "luna": 4, "giorno": 3, "slot": "pomeriggio"},
    ])


## Luna II — I tre fratelli ##################################################

label trio_lenora:
    scene bg vicoli_zefiro with fade
    show druso ghigno at left with easeinleft
    show caino sarcastico with dissolve
    "Serata rara: i tre figli di Lenora allo stesso tavolo. Caino beve idromele, Icaro conta le vincite, Druso cerca guai."
    show icaro neutro at right with dissolve
    druso "Fratellino! Tre settimane che non ti vedo. Sai cosa significa."
    show icaro irritato with qdiss
    icaro "Significa che stavo bene. Non farlo. Lo detesto. È scritto, firmato e protocollato: LO DETESTO."
    druso "TESCHIO!"
    with vpunch
    "Il pugno parte. Icaro salva i genitali al prezzo di tre pile di monete, che rovinano sul pavimento. La taverna si tuffa a raccoglierle. Icaro emette un suono che non ha nome."
    menu:
        "Caino osserva, già divertito. Tocca a me scegliere da che parte stare."
        "Ridere con Druso, forte":
            $ icaro_affinity -= 1
            druso "ECCO! Qualcuno con il senso del teatro!"
            icaro "...e tu. Tu ridi. Annotato. Con la data."
        "Aiutare Icaro a recuperare le monete, contandole":
            $ icaro_affinity += 1
            icaro "...quarantadue, quarantatré. Tornano. Tutte. Tu sai contare sotto pressione: è la prima qualità utile che vedo stasera."
            druso "Traditore! Due contabili a un tavolo solo!"
        "Citare il Codice del Teschio: «si dichiara PRIMA di colpire»":
            $ caino_fiducia += 1
            caino "[Il_t] novellin[fin] che ricorda i codici altrui meglio dell'autore. Druso: ha ragione. Hai dichiarato a pugno già partito. Penale: paghi tu il giro."
            druso "QUESTO È UN TRIBUNALE FARSA."
    "La serata finisce con Druso che declama, Icaro che ricontrolla le pile e Caino che firma il conto del giro col nome di Druso."
    return


## Luna III — La lama e lo scudo #############################################

label incrocio_palestra:
    scene bg palestra with fade
    show aede neutra with dissolve
    show druso ghigno at left with easeinleft
    "Arrivo al cortile che è già pieno: Aede contro Druso, sparring dimostrativo. Lei con la lama da esercizio, lui con lo scudo e la bocca."
    druso "Volpe rossa! Se vinco, mi concedi un ballo alla prossima festa. Se perdi, idem! Il sistema è perfetto."
    aede "Il sistema ha un difetto."
    with lampo
    show druso sorpreso with qdiss
    "Non vedo il colpo. Nessuno lo vede. Druso è a terra, lo scudo a tre metri, la lama di lei ferma a un dito dal naso."
    aede "Il difetto sei tu."
    menu:
        "Il cortile trattiene il fiato. Druso, da terra, guarda me."
        "Applaudire lei: «Pulito. Insegnamelo.»":
            $ aede_affinity += 1
            show aede sorriso with dissolve
            aede "...domani all'alba. Porta la guardia alta e zero domande."
            show druso irritato with qdiss
            druso "E NESSUNO che chieda se mi sono fatto male. Famiglia di serpi."
        "Tendere la mano a Druso con un verso: «Cadde il poeta, ma cadde rimando»":
            $ druso_affinity += 1
            show druso ghigno with qdiss
            druso "«Cadde rimando»! BELLISSIMO! Lo metto nel repertorio e non ti pago i diritti!"
            "Si rialza ridendo. Aede scuote la testa, ma non smentisce il mezzo sorriso."
        "Restare neutrale: qui si rischia la pelle":
            "Resto con le mani in tasca. Sugli spalti due ragazzi si stanno già spingendo per chi tifava chi."
    return


## Luna IV — La partita dei fratelli #########################################

label incrocio_carte:
    scene bg vicoli_zefiro with fade
    show icaro neutro with dissolve
    show caino neutro at left with dissolve
    "Il tavolo grande, posta alta: Icaro contro Caino. L'Arconte della Proprietà perde da tre mani e non è abituato."
    caino "Quarta mano. Fratello, la tua fortuna stasera è... statisticamente interessante."
    show icaro furbo with qdiss
    icaro "La fortuna è una tassa sugli sprovveduti. Tu non sei sprovveduto: quindi non è fortuna. Gioca."
    "E io, dal mio posto, l'ho visto: il taglio del mazzo. Quello che le dita non dovrebbero saper fare."
    menu:
        "Caino perde la quarta mano. Le sue dita tamburellano: sta per capire."
        "Un cenno discreto a Caino: guarda il taglio":
            $ caino_fiducia += 1
            $ icaro_affinity -= 1
            show caino sorpreso with qdiss
            caino "...ah. Ecco la statistica. Fratello: rigiochiamo con il MIO mazzo, e la Proprietà dimentica l'imposta straordinaria sulle fumerie."
            show icaro irritato with qdiss
            icaro "Estorsione. E [il_t] novellin[fin] fa la spia. Annotato. Con la data, l'ora e il taglio di capelli."
        "Tacere: al tavolo di Icaro, chi guarda non parla":
            $ icaro_affinity += 1
            "Icaro vince la quinta, la sesta, e restituisce tutto a fine serata: «prestito didattico», lo chiama. Uscendo, mi fa scivolare in tasca uno Scudo. Uno solo."
        "Proporre il doppio o niente, mazzo nuovo e mescolo io":
            "Mescolo io. Vince comunque Icaro, stavolta pulito. Caino paga, Icaro intasca, e nessuno dei due mi perdona la serata più onesta della storia del tavolo."
    return


## Luna III — Il conto di Druso ##############################################

label incrocio_debiti:
    scene bg vicoli_zefiro with fade
    show druso ghigno at left with easeinleft
    "Il Becco Storto, mattina di paga. Druso non è ancora andato a letto: offre da bere a mezza sala con soldi che, a occhio, non sono suoi."
    show icaro neutro with dissolve
    "Poi la porta si apre, e la sala si ricorda di avere sete altrove. Icaro. Con un registro sotto il braccio."
    icaro "Fratello. Giorno di riscossione."
    druso "Fratellino! Proprio stamattina? Ho appena dichiarato la taverna zona franca. Niente creditori, niente Arconti, niente madri."
    show icaro irritato with qdiss
    icaro "Le zone franche le dichiara la Proprietà. Tu dichiari solo bancarotta, una volta a Luna."
    "Apre il registro tra i boccali. La pagina di Druso è la più lunga. Ha anche dei disegni a margine: non di Icaro."
    druso "Pago in natura. Un poema. Dodici strofe sulla tua avarizia, con dedica."
    icaro "Un poema vale zero Scudi. Un poema su di me vale meno di zero: va a debito."
    menu:
        "Druso mi guarda. Icaro pure. Il registro resta aperto in mezzo."
        "Leggere ad alta voce la pagina di Druso, cifra per cifra":
            "Leggo. La sala, che fingeva di non ascoltare, ascolta. A ogni cifra qualcuno fischia."
            show druso imbarazzato at left with qdiss
            druso "Basta, basta! Così mi rovini la reputazione. Quella da insolvente, che mi sono costruito con fatica."
            show icaro furbo with qdiss
            icaro "Il debito letto in pubblico pesa il doppio. Lezione gratuita. A registro comunque: zero Scudi, zero centesimi."
        "Proporre a Druso di pagare in versi, a chi glieli compra":
            show druso ghigno at left with qdiss
            druso "Un mercato dei versi! Genio! Chi offre per una strofa sulla locandiera?"
            "Offrono in tre. La locandiera offre di più, per non sentirla. Druso incassa quattro monete e le spinge verso Icaro con aria regale."
            show icaro neutro with qdiss
            icaro "Quattro. Acconto accettato. A matita: sulla tua pagina, quattro non si vedono nemmeno."
            icaro "Non ci prendete gusto. Nessuno dei due."
        "Chiudere il registro con una mano: «Non stamattina.»":
            icaro "Hai chiuso il mio registro. Con la mano. Nessuno tocca il mio registro."
            show druso sorpreso at left with qdiss
            druso "Mi ha difeso. Qualcuno mi ha difeso da Icaro. Segnatelo, fratellino: data, ora, e il mio stupore."
            "Icaro lo segna davvero. Poi riapre il registro più in là, dove la mia mano non arriva."
    "A mezzogiorno Druso è ancora in debito e Icaro è ancora creditore. Tutto come prima."
    "Ma bevono allo stesso tavolo, e nessuno dei due se ne va per primo."
    return


## Luna III — Il filo delle sorelle ##########################################

label incrocio_sorelle:
    scene bg palestra with fade
    show aede neutra with dissolve
    "Il cortile d'armi all'alba. Aede ha già rotto due bersagli e guarda il terzo come un debitore."
    show ofelia neutra at left with dissolve
    "Al bordo del cortile compare Ofelia. Vestita di nero, i guanti puliti, una lama avvolta in un panno sotto il braccio."
    ofelia "Sorella. La tua. Ti avevo chiesto di non usarla sui chiodi."
    aede "Non erano chiodi. Era un elmo."
    ofelia "Peggio. Il filo era una riga, adesso è una sega. Ci ho messo tre sere."
    "Ofelia svolge il panno. La lama brilla come acqua ferma. Aede la prende senza ringraziare. Ofelia non aspetta il grazie: si sta già sfilando i guanti, un dito alla volta."
    show aede irritata with qdiss
    aede "Pesa diversa."
    ofelia "Pesa giusta. Sei tu che pesi diversa. Stai caricando sul piede sinistro da una Luna: lo vedo dalle tacche."
    "Aede apre la bocca per rispondere. Poi la chiude. Si guarda il piede sinistro."
    menu:
        "Le due figlie di Glauco si fronteggiano sopra una lama. Il cortile è vuoto, a parte me."
        "Chiedere a Ofelia come si legge un filo":
            show ofelia compiaciuta at left with qdiss
            ofelia "Si passa l'unghia, piano, contro il verso. Se si ferma, il filo è vivo. Se scivola, è morto. Come certi pretendenti."
            "Mi porge la lama per provare. Aede la riprende prima che io la tocchi."
            aede "La mia lama non la tocca nessuno. Nemmeno per lezione."
        "Dare ragione ad Aede: «Pesa diversa, si vede»":
            show aede neutra with qdiss
            aede "Visto? Lo vede anche [lui_t]. E [lui_t] non vede mai niente."
            show ofelia rabbia at left with qdiss
            ofelia "Due ciechi d'accordo fanno una maggioranza, non una verità. Il piede sinistro, sorella."
        "Restare in silenzio e guardare il piede di Aede":
            "Guardo il piede. Ofelia ha ragione: il peso cade storto, appena. Da sol[fin] non l'avrei mai visto."
            show aede imbarazzata with qdiss
            aede "...smettetela di guardarmi i piedi. Tutti e due."
            "Ofelia sorride. Non a me: alla sorella che arrossisce."
    hide ofelia with dissolve
    "Ofelia se ne va com'è venuta, senza rumore. Aede rimette la guardia. Carica sul piede destro, stavolta."
    "Il terzo bersaglio non ha nessuna speranza."
    return


## Luna IV — L'imposta sulla primavera #######################################

label incrocio_serra:
    scene bg sala_svelo with fade
    show ofelia neutra with dissolve
    "La serra di Glauco, pomeriggio di corte. I pretendenti in fila, i fiori in posa. Ofelia annoiata con eleganza."
    show caino neutro at left with dissolve
    "In fondo alla fila compare un uomo con un registro sotto il braccio. Non porta fiori. Porta un calamaio."
    caino "Proprietà. Accertamento. Tubi caldi sotto il pavimento, legna d'inverno, fiori fuori stagione. Primavera a pagamento: qualcuno la paga?"
    ofelia "Caino. Sei in fila. Aspetta il tuo turno come gli altri."
    caino "Io non sono un pretendente. Sono un creditore. È più onesto."
    show ofelia compiaciuta with qdiss
    ofelia "È più noioso. Ma te lo concedo: almeno non mi porti un sonetto."
    "La fila si apre come un mare. Nessuno vuole stare tra la figlia di Glauco e l'Arconte della Proprietà."
    caino "Quanta legna brucia questa stanza, Ofelia? A Luna. Cifra esatta."
    ofelia "Abbastanza da scaldare la tua imposta finché non si scioglie."
    menu:
        "Si guardano come due lame che si conoscono. Io sono in fila, due posti più indietro."
        "Contare a voce alta le bocche di calore, per Caino":
            "Conto. Undici bocche nel pavimento, due per fila, una sotto il fiore blu. Caino annota senza guardarmi."
            show caino sarcastico at left with qdiss
            caino "Undici. La serra di Glauco ha appena trovato un perito. Ofelia, il tuo pretendente lavora per me."
            show ofelia rabbia with qdiss
            ofelia "Il mio pretendente è in fila. Lavora per me. Torna al tuo posto, [player_name]: il quarto da sinistra ti fissa."
        "Prendere le parti di Ofelia: «La primavera non si tassa»":
            ofelia "Sentito, Arconte? La primavera non si tassa. Lo faccio scrivere sulla porta."
            show caino freddo at left with qdiss
            caino "Tutto si tassa. Anche la primavera, anche le frasi fatte. La tua, [player_name], la metto a registro gratis."
        "Chiedere a Caino quanto vale, a registro, un fiore che non fiorisce":
            show caino sorpreso at left with qdiss
            caino "...niente. Una spesa senza rendita. A bilancio, una perdita pura."
            show ofelia neutra with qdiss
            ofelia "Allora lascialo fuori dal tuo registro. Le perdite pure, qui, le teniamo per ostinazione."
            "Caino guarda il fiore blu. Chiude il calamaio. Per una volta, non scrive niente."
    "Caino se ne va prima che la corte finisca. Sul tavolino dei doni lascia una ricevuta: «Accertamento rinviato»."
    "Ofelia la infila tra i sonetti. È il primo dono, oggi, che non butta."
    return
