# Route Aede — interludi: scene di contorno tra i capitoli.

################################################################################
## INTERLUDIO 1 — Il Ceppo della madre degli orfani (dopo il prologo)
################################################################################

label interludio1:

    scene bg corridoio_ceppo with fade

    "La tenuta del Ceppo di Briseide non somiglia a una caserma, né a un palazzo. Somiglia a una cucina troppo grande dove vivono troppe persone che si vogliono bene urlando."

    show briseide neutra with dissolve

    "Briseide Ippodamia, Autarca della Columna Lactaria, madre di tutti gli orfani del Nord. Cinquanta Figli adottati in trent'anni, e ogni nome se lo ricorda, con la data e il motivo."

    briseide "Com'è andato lo Svelo, [player_name]?"

    pc "Istruttivo, madre."

    briseide "Mh. «Istruttivo». Quando un mio Figlio risponde con una parola sola, di solito ha conosciuto o una lama o una donna."

    "Non rispondo. Lei sorride come chi ha già vinto."

    briseide "Entrambe, dunque. Siediti, che ti racconto una cosa sui Ceppi di questa Famiglia."

    hide briseide with dissolve

    "Mi racconta. Dei 63 Ceppi e dei 9 Rami, uno per Primarca. Delle correnti del Consiglio, che si muovono come fiumi sotto il ghiaccio: in superficie fermi, sotto una corrente che ti porta via le gambe."

    "E del Ceppo di Glauco Severo, che nel Ramo fa il lavoro di cui nessuno parla all'Adunanza."

    show vanna neutra at left with easeinleft

    vanna "Ooh, [il_fratello_t] ha conosciuto la volpe rossa!"

    "Vanna. Sorella maggiore di Ceppo, orecchie ovunque, discrezione da ariete."

    show corrado neutro at right with easeinright

    corrado "Lascialo respirare. E tu, fratello: da quella, distanza. È la figlia di Glauco. Il {i}gioiello{/i}. Sai cosa fanno ai ladri di gioielli, da queste parti?"

    vanna "Non è rubare se il gioiello ti segue a casa, Corrado."

    corrado "È rubare peggio."

    "Litigano su di me per un'ora. Nessuno dei due ha torto. È questo il problema."

    return

################################################################################
## INTERLUDIO 2 — La taverna (dopo l'Athlion)
################################################################################

label interludio2:

    scene bg vicoli_zefiro with fade

    "La sera dopo l'Athlion, il Ceppo festeggia — vittorie altrui, birra propria — in una taverna della Contrada Lumina."

    show vanna neutra at left with dissolve
    show corrado neutro at right with dissolve

    vanna "E allora io [gli_t] dico: [fratello_t], o le parli o la smetti di fissarla come un merluzzo. E [lui_t] che fa? Entrambe le cose!"

    "Risate del tavolo. Io studio il fondo del boccale."

    corrado "Ridete, ridete. Io ho chiesto in giro, invece. Del Ceppo di Glauco. Volete sapere cosa si dice?"

    "Il tavolo si zittisce. Corrado ha il talento di guastare le feste con la verità."

    corrado "Si dice che chi entra in quel Ceppo da bambino non sceglie mai. Che il vecchio raccoglie orfani come Briseide — ma dove nostra madre cresce Figli, lui forgia attrezzi."

    corrado "E si dice che la figlia prediletta avesse sette anni al primo addestramento. Sette. Con le lame vere, perché «quelle finte insegnano bugie»."

    corrado "Gli altri due, Ofelia e Ascadeo, sono arrivati dopo. Ma è lei che il vecchio porta alle feste."

    vanna "...e la madre? Nel Ceppo di Glauco c'è una madre?"

    corrado "C'era una Filius Maior che faceva da madre a tutti. Morta quando la ragazzina ne aveva dodici. Un lavoro andato male. Da allora, dicono, Glauco raddoppiò gli addestramenti. Il lutto, nel suo Ceppo, si lavora."

    "Il boccale mi si ferma a mezz'aria."

    "Sette anni. Lame vere. Una madre persa a dodici, e un padre che risponde al dolore con la disciplina."

    if "aede_cap3" in eventi_visti:
        "Ripenso a come ha detto «il gioiello di Glauco Severo». Come se il gioiello fosse un sasso che porta in tasca da troppi anni."
    else:
        "Ripenso a lei nell'ultima frazione della staffetta. A come vince senza fermarsi a guardare chi applaude."

    vanna "[fratello_t!c]. Tutto bene?"

    pc "Sì. No. Non lo so."

    if aede_affinity >= 5:
        vanna "Benvenut[fin] nell'amore, [fratello_t]."
    else:
        vanna "Benvenut[fin] nel Nord, [fratello_t]. Qui le storie tristi si bevono, non si ascoltano."

    return

################################################################################
## INTERLUDIO 3 — Briseide e il vecchio leone (dopo il vicolo)
################################################################################

label interludio3:

    scene bg corridoio_ceppo with fade

    "Non dormo. Da tre notti, da quella del vicolo, l'alba mi trova sul ballatoio."

    show briseide neutra with dissolve

    "Briseide mi ci trova pure lei. Con due tazze di brodo caldo, perché Briseide a tutto risponde col brodo."

    briseide "I miei Figli insonni vengono in due specie: quelli che hanno fatto qualcosa, e quelli che hanno visto qualcosa. Tu che specie sei, stanotte?"

    pc "Madre... voi conoscete Glauco Severo. Da prima che io nascessi, forse."

    briseide "Dall'anno Tre della Famiglia. Sedevamo già entrambi in Consiglio quando di Ceppi ce n'erano la metà."

    pc "Che uomo è? Sotto l'Autarca, intendo. Sotto il titolo."

    "Briseide beve il suo brodo. Prende tempo come altri prendono fiato."

    briseide "Glauco Severo è l'uomo più onesto che io conosca, [player_name]. È questo che lo rende terribile."

    briseide "Non mente mai. Non odia mai. Non punisce mai per rabbia. Fa esattamente ciò che dice, sempre, e ciò che dice è esattamente ciò che la Virtù dell'Esclusività gli comanda: il Ceppo prima di tutto, il Ceppo sopra tutto."

    briseide "Io ho seppellito Figli, e ho pianto ogni fossa. Lui ha seppellito Figli, e da ogni fossa è tornato con una lezione nuova per i vivi. Non so dirti quale di noi due ami di più i propri. So dirti che il suo amore somiglia a un'incudine."

    pc "E Aede?"

    briseide "Aede è ciò che resta quando un'incudine ama un diamante per vent'anni: la cosa più dura e più luminosa del Nord."

    briseide "Vuoi un consiglio da vecchia madre? Chi vuole bene a quella ragazza non deve vincere contro il padre. Deve solo essere più paziente dell'incudine. Nessuno, finora, lo è stato."

    "Si alza, mi lascia la seconda tazza di brodo."

    briseide "E [player_name]... il mio Ceppo non forgia attrezzi. Ma neanche codardi. Qualunque cosa tu decida, decidila da [figlio_t] mi[fin]."

    return
