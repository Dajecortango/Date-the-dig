# Route Caino — Atto 1: prologo e capitoli 1-3.

################################################################################
## PROLOGO — L'Adunanza
################################################################################

label caino_prologo:

    scene bg sala_svelo with fade

    "L'Adunanza annuale. Tutta la Famiglia sotto un tetto solo: Autarchi, Arconti, Eparchi, e in fondo alla sala i Figli nuovi come me, messi lì dove non facciamo danni."

    "È lì che lo vedo la prima volta: al centro esatto della sala, dove le correnti del potere si incrociano. Ride con tre Autarchi insieme, e tutti e tre credono di essere il motivo della risata."

    show caino neutro with dissolve

    "Caino. Figlio di Lenora, fratello di Druso e di Icaro. Arconte della Proprietà. Dicono che sia la spada migliore di Rocca Tempesta dopo sua madre, e la lingua migliore senza nessun dopo."

    "E a un certo punto — non so come, non so perché — quella lingua punta me."

    caino "Tu. Figlio di Briseide. Sì, tu, quello che da mezz'ora studia la sala come se dovesse comprarla."

    pc "Osservavo, Arconte. Niente di più."

    caino "«Osservavo, Arconte». Educato, misurato, inutile. Briseide vi fabbrica tutti così?"

    "Sorride mentre lo dice. Ha un sorriso facile, Caino: il tipo di sorriso che ti fa sentire importante due secondi prima di scoprire cosa ti è costato."

    "Un servo passa col vassoio. Caino scarta il vino con un gesto che è quasi un insulto."

    caino "Vino di Glostok. Lo bevono i cambiavalute e i pentiti. Io bevo idromele di Rurikstad, e chi mi conosce lo sa. Ricordatelo, Figlio di Briseide: nella Famiglia, chi ricorda i dettagli possiede le persone."

    "Prende invece un corno di idromele. Al mignolo destro gli brilla un anello: un sigillo con un drago, non un leone. Un dettaglio che stona, su un uomo che non lascia nulla al caso."

    caino "Ora dimmi una cosa, così capisco con chi parlo."

    show caino sarcastico with qdiss

    caino "Il Ballo delle Candele Spente. Che festa magnifica dev'essere stata, eh? Luci soffuse, musica, mia madre che cura ogni dettaglio. Mi spiace solo non esserci stato. Tu che ne pensi?"

    menu:
        "Qualcosa, nella sua voce, è troppo liscio per essere vero."

        "«Magnifica davvero. Peccato essermela persa.»":
            $ caino_fiducia -= 2
            $ caino_trappole += 1

            pc "Magnifica davvero. Peccato essermela persa."

            show caino neutro with qdiss

            caino "Già. Peccato."

            "Il sorriso non cambia di un millimetro. Ma qualcosa dietro gli occhi archivia: {i}questo annuisce senza sapere{/i}. E io capisco di aver perso un punto in una partita che non sapevo di giocare."

            "Solo più tardi, da Vanna, scopro cos'era il Ballo delle Candele Spente: un massacro. Ideato da Lenora. Sua madre."

        "«Era un massacro, Arconte. Lo sanno anche i nuovi.»":
            $ caino_fiducia += 2

            pc "Era un massacro, Arconte. Lo sanno anche i nuovi. Strano che il figlio della Capofamiglia se lo ricordi come una festa."

            show caino sorpreso with qdiss

            "Per un istante — mezzo battito — il sorriso si ferma."

            show caino neutro with qdiss

            caino "...Briseide vi fabbrica meglio di quanto dicessi."

            caino "Era una prova, Figlio di Briseide. La sala è piena di gente che mi dà ragione per riflesso. Tu no. Interessante."

        "Restare in silenzio e sorridere":
            $ caino_fiducia -= 1

            "Sorrido e non rispondo. La via sicura."

            show caino neutro with qdiss

            caino "Il silenzio. La risposta di chi non vuole perdere. Prudente. Noioso. Ma prudente."

    caino "Ci rivedremo, Figlio di Briseide. La Proprietà ha sempre bisogno di mani nuove. E io ho sempre bisogno di sapere cosa valgono, le mani nuove."

    hide caino with dissolve

    "Se ne va attraversando la sala come se la sala fosse sua. E il punto, mi dico, è proprio questo: un giorno potrebbe esserlo."

    return

################################################################################
## CAPITOLO 1 — La Proprietà
################################################################################

label caino_cap1:

    scene bg corridoio_ceppo with fade

    show briseide neutra with dissolve

    briseide "L'Arconte della Proprietà ha chiesto di te. Per nome."

    pc "Per nome?"

    briseide "Per nome. [player_name], del Ceppo di Briseide. Quando Caino chiede per nome, ha già deciso a cosa gli servi. Scoprilo prima che lo decida del tutto: è l'unico vantaggio che avrai."

    scene bg studio_glauco with fade

    show caino neutro with dissolve

    "Lo studio dell'Arconte della Proprietà è l'opposto di quello di Glauco: caldo, pieno, teatrale. Registri ovunque, mappe dei Ceppi, e una spada appesa dove chiunque entri deve vederla."

    caino "Il Figlio che non annuisce. Entra. Ho un problema di aritmetica e tutti i miei scrivani hanno già sbagliato la risposta."

    "Il problema di aritmetica è un registro delle decime di tre Contrade. Lavoriamo un'ora: lui parla, io conto, lui controlla il mio contare fingendo di non farlo."

    caino "Passabile. Briseide ti presta a buon mercato o devo firmare qualcosa?"

    "Un servo entra con un vassoio: due coppe già piene."

    menu:
        "Vino rosso. Di Glostok, dal sigillo sulla brocca."

        "Fermare il servo: «L'Arconte beve idromele di Rurikstad.»":
            $ caino_fiducia += 2
            $ caino_memoria += 1

            pc "Aspetta. L'Arconte beve idromele di Rurikstad. Il vino di Glostok lo bevono i cambiavalute e i pentiti."

            show caino sorpreso with qdiss

            "Caino si volta lentamente. Mi guarda come si guarda una moneta trovata per terra: con sospetto, e con interesse."

            show caino neutro with qdiss

            caino "...hai ricordato. Parola per parola."

            caino "Sai quanti, in questa Rocca, ricordano quello che dico quando non sto minacciando nessuno? Due. Mia madre. E adesso tu."

        "Prendere la coppa e ringraziare":
            $ caino_fiducia -= 1

            "Prendo la coppa. Caino guarda la sua senza toccarla, poi guarda me, e qualcosa negli occhi gli si spegne di un grado."

            show caino freddo with qdiss

            caino "Salute, Figlio di Briseide. Al vino di Glostok e a chi non ascolta."

        "Aspettare di vedere se la beve":
            "Aspetto. Caino lascia la coppa dov'è, senza commentare. Il servo la riporta via."

            caino "Prudente. Sempre prudente. Prima o poi dovrai scegliere qualcosa, sai."

    caino "Torna domani. La Proprietà ha un lavoro vero per te. E il lavoro vero, qui dentro, è l'unico complimento che faccio."

    return

################################################################################
## CAPITOLO 2 — TESCHIO
################################################################################

label caino_cap2:

    scene bg palestra with fade

    "Il cortile d'armi del Ramo di Lenora, l'alba dopo. Mi hanno detto di presentarmi presto. Non mi hanno detto per cosa."

    show caino neutro with dissolve

    "Caino è a torso di camicia, al centro del cortile. Ai suoi piedi, due blocchi di marmo bianco con maniglie di ferro incassate."

    caino "Ventiquattro chili l'uno. Marmo delle Cimebianche, tagliato male apposta: il peso non è mai dove te lo aspetti. Come la Famiglia."

    "Li solleva. E comincia — che gli Asi mi fulminino — a fare alzate laterali. Le braccia dritte, il marmo che sale fino alla linea delle spalle, scende, risale. Il respiro regolare come un conto."

    caino "Dodici... tredici... il potere, Figlio di Briseide, è questo... quattordici... peso morto che impari a sollevare... con grazia..."

    show druso ghigno at left with easeinleft

    "Una voce tuona dall'arcata."

    druso "FRATELLO!"

    "Druso. Più largo di Caino di una spanna, la barba più selvaggia, il sorriso più facile ancora."

    druso "TESCHIO!"

    "E prima che io capisca cosa significa, Druso scaglia un pugno diretto ai genitali di Caino. Caino — con quarantotto chili di marmo in mano — ruota sul fianco, para col blocco sinistro, e il pugno di Druso incontra la pietra."

    with hpunch

    druso "AAAH! Figlio di—"

    caino "Di Lenora. Come te. Quindici."

    "Caino posa i blocchi, e con lo stesso movimento tira un calcio secco all'inguine del fratello. Druso lo blocca con entrambe le mani per un pelo."

    caino "TESCHIO."

    druso "Parato! Non vale, avevi ancora il marmo in mano quando ho dichiarato!"

    caino "Il Codice del Teschio non dice niente sul marmo. L'ho scritto io, lo saprò."

    "I due si abbracciano ridendo come due orsi. Io resto sulla soglia, con la precisa sensazione di aver visto un rito più antico e più sacro dell'Adunanza."

    druso "E questo chi è? Il famoso Figlio di Briseide che non annuisce?"

    druso "Quaranta Scudi, fratello. Me li devi da tre lune: hai scommesso che il Ciambellano di Glostok non sarebbe durato un anno, ed è ancora lì."

    caino "Quaranta Scudi che diventeranno venti, perché la metà la persi per colpa del tuo consiglio sbagliato sul torneo. Dettagli, fratello. I dettagli possiedono le persone."

    menu:
        druso "Novellin[fin]! Fai da testimone: ha detto quaranta o non ha detto quaranta?"

        "«Quaranta. E il Codice del Teschio non parla di sconti.»":
            $ caino_druso += 1
            $ caino_fiducia += 1

            pc "Quaranta. E se il Codice del Teschio l'ha scritto lui, varrà anche sui debiti: niente sconti non dichiarati."

            show druso ghigno with qdiss

            druso "AH! Mi piace! Briseide, benedetta donna, finalmente uno con la spina dorsale!"

            show caino sarcastico with qdiss

            caino "Traditore. Sei nel mio studio da un giorno e già testimoni per il nemico."

            "Ma ride. Rido anche io. È impossibile non ridere, in mezzo a questi due."

        "«Non ho sentito niente. Io conto solo registri.»":
            $ caino_fiducia += 1

            pc "Non ho sentito niente, io conto solo registri. E nei registri della Proprietà questo debito non esiste."

            show caino neutro with qdiss

            caino "Risposta da politico. Forse ti ho sottovalutato."

            druso "Risposta da vigliacco! Quaranta Scudi, pagherai, legislatore dei miei—"

            caino "TESCHIO."

            druso "NO—"

            with vpunch

    "Stavolta Druso non para."

    "Quando il cortile si svuota, Caino mi trattiene con un gesto."

    show druso ghigno at left with qdiss
    show caino sarcastico with qdiss

    caino "Mio fratello. Un idiota magnifico. Il preferito di nostra madre, lo dico senza un filo di invidia: a lui il cuore di Lenora, a me solo i suoi incarichi, i suoi segreti e il suo seggio in Consiglio, un giorno. Vedi quanto ci ho perso."

    menu:
        "Di nuovo quella voce troppo liscia."

        "«Certo. Si vede che non t'importa affatto.»":
            $ caino_fiducia -= 2
            $ caino_trappole += 1

            pc "Certo. Si vede che non t'importa affatto."

            show caino neutro with qdiss

            caino "Già. Per niente."

            "Archiviato: {i}annuisce senza capire{/i}. Due a zero per lui, e io continuo a non sapere a che gioco giochiamo."

        "«Hai appena detto il contrario di quello che pensi. Di nuovo.»":
            $ caino_fiducia += 2

            pc "Hai appena detto il contrario di quello che pensi. Di nuovo. Il preferito sei tu, e la cosa ti pesa più dei tuoi blocchi di marmo."

            show caino sorpreso with qdiss

            "Silenzio. Druso, dall'arcata, fischia piano."

            show caino neutro with qdiss

            caino "...Druso. Il Figlio di Briseide resta a pranzo."

            druso "Lo so, fratello. L'ho capito prima di te."

    return

################################################################################
## CAPITOLO 3 — Il ballo
################################################################################

label caino_cap3:

    scene bg sala_svelo with fade

    "Festa di mezzo inverno a Rocca Tempesta. La sala grande, le lanterne, e la Famiglia che danza come se non si spiasse a vicenda da cento anni."

    show caino neutro with dissolve

    "Caino balla come combatte: in anticipo su tutti. Tre dame di tre Ceppi diversi si sono già alternate al suo braccio, e ognuna è tornata al suo posto convinta di avergli strappato un segreto."

    caino "Figlio di Briseide. Sai ballare o Briseide vi insegna solo l'aritmetica?"

    pc "L'aritmetica è una danza, Arconte. Solo più lenta."

    caino "Risposta da scrivano con ambizioni. Vediamo la pratica."

    "Mi tende la mano. E la sala intera — lo sento sulla pelle — smette per un istante di respirare: l'Arconte della Proprietà non invita i Figli nuovi."

    menu:
        "La musica riparte."

        "Accettare e lasciarlo condurre":
            $ caino_fiducia += 2

            "Accetto. Conduce lui, ovviamente: ogni passo è un contratto, ogni giro una clausola. Ma a metà danza succede una cosa strana — smette di guardare la sala e guarda me."

            show caino neutro with qdiss

            caino "Curioso. Di solito a questo punto i miei partner contano i passi o contano i vantaggi. Tu che conti?"

            pc "Niente. È questo il bello della danza: è l'unica cosa che non serve a niente."

            "Non risponde. Ma per quattro battute intere, l'Arconte della Proprietà balla senza guardare nessun altro nella sala."

        "Accettare, ma giocare a condurre io":
            $ caino_fiducia += 2

            "Accetto — e al terzo passo gli rubo la conduzione. Un furto piccolo, tecnico, visibile solo a noi due."

            show caino sorpreso with qdiss

            caino "...questo era il mio tempo."

            pc "Era. I dettagli possiedono le persone, Arconte."

            show caino sarcastico with qdiss

            caino "Rubare le mie massime per usarle contro di me. C'è della Proprietà in te, Figlio di Briseide. Forse troppa."

            "Ma non si riprende la conduzione. Per tutta la danza."

        "Rifiutare con un inchino":
            $ caino_fiducia -= 2

            "Mi inchino e rifiuto. La mano di Caino resta tesa nel vuoto per un secondo — un secondo che la sala intera vede."

            show caino freddo with qdiss

            caino "Prudenza, di nuovo. Un giorno, Figlio di Briseide, la prudenza ti salverà la vita. E sarà l'unica cosa che avrai salvato."

    show druso ghigno at left with easeinleft

    "Tra una danza e l'altra, Druso mi intercetta al tavolo lungo, due boccali in mano e il fiato di chi ha già vinto tre brindisi."

    druso "Novellin[fin]! Mio fratello balla, io bevo. Ognuno il suo talento. Gara: chi finisce il boccale per ultimo paga il prossimo giro E balla con la vedova Tersicore."

    menu:
        "Il boccale è grande quanto un elmo."

        "Accettare la gara":
            $ caino_druso += 1

            "Accetto. Perdo. Pago. E la vedova Tersicore, giuro, balla meglio di metà sala."

            druso "Hai perso con onore e pagato senza piangere. Nel mio Codice personale, vali già più di mezzo Consiglio."

            "Da quella sera, Druso mi saluta per nome. Tutte le volte. Anche in mezzo alla folla."

        "Declinare con diplomazia":
            pc "La Proprietà mi vuole sobrio, temo."

            druso "«La Proprietà mi vuole sobrio». Parli già come lui. Che gli Asi ci salvino, due Caino."

    hide druso with dissolve

    "Più tardi, al tavolo dell'idromele, mi raggiunge con due corni. Me ne porge uno."

    show caino neutro with qdiss

    caino "Una domanda, prima che la serata finisca. Guardami le mani."

    "Le guardo. Le dita lunghe, i calli della spada. Nessun anello."

    caino "All'Adunanza, la sera che ci siamo conosciuti, portavo un anello. Se mi dici qual era e dov'era, questo idromele lo paghi con la risposta. Se sbagli, resti a bocca asciutta e io archivio."

    menu:
        "Chiudo gli occhi. La sala, il vassoio, il corno di idromele, la mano..."

        "«Un sigillo col drago. Al mignolo destro.»":
            $ caino_fiducia += 2
            $ caino_memoria += 1

            pc "Un sigillo con un drago. Al mignolo destro. Stonava: un drago, su un uomo del leone."

            show caino sorpreso with qdiss

            "Caino resta immobile. Poi, piano, mi mette il corno in mano."

            show caino neutro with qdiss

            caino "Il drago è Draken, il Mutevole. L'anello era di mio padre. Non lo sa nessuno, perché nessuno guarda davvero."

            caino "Tre. Siamo in tre, adesso, a ricordare quello che dico. E uno dei tre comincia a preoccuparmi."

        "«Un leone d'oro, all'indice.»":
            $ caino_fiducia -= 1

            pc "Un leone d'oro. All'indice."

            show caino sarcastico with qdiss

            caino "Un leone. Certo. Come tutti, ovvio, prevedibile. Hai guardato senza vedere, Figlio di Briseide."

            "Si riprende il corno e lo beve lui, fino in fondo, guardandomi negli occhi. Archiviato."

        "«Non portavi anelli.»":
            $ caino_fiducia -= 1

            pc "Non portavi anelli. Le mani di uno spadaccino."

            show caino sarcastico with qdiss

            caino "Poetico. E sbagliato. La poesia è l'ultima difesa di chi non ricorda."

    return
