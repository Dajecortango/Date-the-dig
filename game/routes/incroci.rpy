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
    ])


## Luna II — I tre fratelli ##################################################

label trio_lenora:
    scene bg vicoli_zefiro with fade
    show druso ghigno at left with easeinleft
    show caino sarcastico with dissolve
    "Serata rara: i tre figli di Lenora allo stesso tavolo. Caino beve idromele, Icaro conta le vincite, Druso cerca guai."
    show icaro neutro at right with dissolve
    druso "Fratellino! Tre settimane che non ti vedo. Sai cosa significa."
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
            caino "Il novellino che ricorda i codici altrui meglio dell'autore. Druso: ha ragione. Hai dichiarato a pugno già partito. Penale: paghi tu il giro."
            druso "QUESTO È UN TRIBUNALE FARSA."
    "La serata finisce con Druso che declama, Icaro che ricontrolla le pile e Caino che sorride come chi ha già archiviato tutto. Una famiglia, a modo loro."
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
    "Non vedo il colpo. Nessuno lo vede. Druso è a terra, lo scudo a tre metri, la lama di lei ferma a un dito dal naso."
    aede "Il difetto sei tu."
    menu:
        "Il cortile trattiene il fiato. Druso, da terra, guarda me."
        "Applaudire lei: «Pulito. Insegnamelo.»":
            $ aede_affinity += 1
            show aede sorriso with dissolve
            aede "...domani all'alba. Porta la guardia alta e zero domande."
            druso "E NESSUNO che chieda se mi sono fatto male. Famiglia di serpi."
        "Tendere la mano a Druso con un verso: «Cadde il poeta, ma cadde rimando»":
            $ druso_affinity += 1
            druso "«Cadde rimando»! BELLISSIMO! Lo metto nel repertorio e non ti pago i diritti!"
            "Si rialza ridendo. Aede scuote la testa, ma non smentisce il mezzo sorriso."
        "Restare neutrale: qui si rischia la pelle":
            "Scelta saggia. I duelli dei Dignitas finiscono; le loro faide sugli spalti, mai."
    return


## Luna IV — La partita dei fratelli #########################################

label incrocio_carte:
    scene bg vicoli_zefiro with fade
    show icaro neutro with dissolve
    show caino neutro at left with dissolve
    "Il tavolo grande, posta alta: Icaro contro Caino. L'Arconte della Proprietà perde da tre mani e non è abituato."
    caino "Quarta mano. Fratello, la tua fortuna stasera è... statisticamente interessante."
    icaro "La fortuna è una tassa sugli sprovveduti. Tu non sei sprovveduto: quindi non è fortuna. Gioca."
    "E io, dal mio posto, l'ho visto: il taglio del mazzo. Quello che le dita non dovrebbero saper fare."
    menu:
        "Caino perde la quarta mano. Le sue dita tamburellano: sta per capire."
        "Un cenno discreto a Caino: guarda il taglio":
            $ caino_fiducia += 1
            $ icaro_affinity -= 1
            caino "...ah. Ecco la statistica. Fratello: rigiochiamo con il MIO mazzo, e la Proprietà dimentica l'imposta straordinaria sulle fumerie."
            icaro "Estorsione. E il novellino fa la spia. Annotato. Con la data, l'ora e il taglio di capelli."
        "Tacere: al tavolo di Icaro, chi guarda non parla":
            $ icaro_affinity += 1
            "Icaro vince la quinta, la sesta, e restituisce tutto a fine serata: «prestito didattico», lo chiama. Uscendo, mi fa un cenno. Il silenzio paga."
        "Proporre il doppio o niente, mazzo nuovo e mescolo io":
            "Mescolo io. Vince comunque Icaro, stavolta pulito. Caino paga, Icaro intasca, e nessuno dei due mi perdona la serata più onesta della storia del tavolo."
    return
