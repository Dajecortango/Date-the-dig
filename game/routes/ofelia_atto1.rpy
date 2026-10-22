# Route Ofelia — Atto 1: la corte (attivita'), eventi 1-2, interludi 1-2.

## Corte 1 — La fila ##########################################################

label att_corte_1:
    scene bg sala_svelo with fade
    show ofelia neutra with dissolve
    "La serra di Glauco in pieno inverno: fiori che non dovrebbero esistere e una fila di pretendenti che sembra voler somigliare a loro."
    "Ofelia li passa in rassegna come si passa un mazzo di carte scadenti. Nessuno regge il suo sguardo oltre il secondo."
    if route_seconda == "aede":
        $ aede_sospetto += 1
        "Mi accorgo troppo tardi che una servetta ci osserva dal corridoio. Domani Aede saprà che passo in serra."
    "L'aria sa di terra umida e di brace. Sotto il pavimento corrono i tubi caldi di Glauco: d'inverno, qui dentro, è sempre primavera a pagamento."
    ofelia "Il quarto da sinistra mi ha dedicato un sonetto. Il terzo, un cavallo. Il cavallo era più eloquente."
    "Il primo della fila fa un passo avanti e si inchina troppo. Lei aspetta che si rialzi, poi gli porge il dorso della mano. Non per il bacio: per congedarlo."
    ofelia "Grazie. Il prossimo."
    "Il prossimo sono io. Mi accorgo che i pretendenti dietro di me trattengono il fiato, curiosi di vedermi cadere."
    menu:
        "Mi tocca il turno: mi guarda, e aspetta."
        "«Il tuo giardino è splendido, Ofelia. Quasi quanto te.»":
            $ ofelia_affinity -= 1
            show ofelia rabbia with qdiss
            ofelia "Quasi. Che parola generosa. Prendila con te e cedi il posto al prossimo."
            "Alle mie spalle qualcuno sospira di sollievo. Un concorrente in meno."
        "«Non ti dirò niente di bello. Hai già sentito tutto.»":
            $ ofelia_affinity += 1
            show ofelia compiaciuta with qdiss
            ofelia "...e il bello è che è vero. Resta pure in fila. In fondo, ma resta."
            "Il poeta del sonetto mi fulmina con lo sguardo. Ho appena rubato la sua unica rima."
        "Restare in silenzio, a guardare i fiori":
            show ofelia neutra with qdiss
            ofelia "Almeno non mi hai rubato l'aria. Già qualcosa."
            "Indico un fiore blu, chiuso come un pugno. Lei segue il mio dito e, per un istante, dimentica la fila."
            ofelia "Quello l'ha piantato mio padre, il giorno che sono nata. Non è mai fiorito. Lo teniamo per ostinazione."
    return


## Corte 2 — Il guanto ########################################################

label att_corte_2:
    scene bg sala_svelo with fade
    show ofelia neutra with dissolve
    "Oggi è lei a muoversi. Attraversa la serra con un guanto in mano, e un giovane damerino le inciampa dietro, tutto occhi."
    if route_seconda == "aede":
        $ aede_sospetto += 1
        "In corridoio sento passare il mio nome tra due ancelle. Verrà riferito, e Aede ha l'udito fine."
    ofelia "Uno dei miei corteggiatori sostiene di aver combattuto un orso per me. Non c'era alcun orso. Il mio compito è capire fino a che punto lui lo creda."
    "Il damerino si chiama Tullio, a quanto dice lui stesso, tre volte in un minuto. Ha la manica strappata con molta cura."
    "Ofelia lascia cadere il guanto sul vialetto. Lui si precipita a raccoglierlo, e glielo porge in ginocchio come una reliquia."
    ofelia "Vedi? Riporta. Questo almeno lo sa fare."
    menu:
        "Il pretendente si volta verso di me, in cerca di un alleato."
        "Dargli ragione: «Un orso, certo. Enorme.»":
            $ ofelia_affinity -= 1
            show ofelia rabbia with qdiss
            ofelia "Un altro che mi serve quello che voglio sentire. Che stanchezza."
            "Tullio mi abbraccia come un fratello d'arme. Ofelia si allontana prima che possa abbracciare anche lei."
        "«L'orso non c'era. Ma i suoi graffi sul braccio sono veri.»":
            $ ofelia_affinity += 1
            show ofelia imbarazzata with qdiss
            ofelia "...hai notato i graffi. Gli altri guardano sempre me."
            show ofelia neutra with qdiss
            ofelia "Era un gatto. Non dirglielo."
            "Tullio non ha capito niente. Ofelia gli restituisce il guanto, gentile, e lo congeda con una pacca da padrona di cani."
        "Svignarmela prima che mi tiri in mezzo":
            show ofelia neutra with qdiss
            ofelia "Prudente. Non è una virtù che apprezzo, ma almeno è onesta."
            "Dalla porta la sento ancora: «Raccontami di nuovo i denti, Tullio. Quanti erano?»"
    return


## Corte 3 — Il lungo congedo ################################################

label att_corte_3:
    scene bg sala_svelo with fade
    show ofelia neutra with dissolve
    "Fine pomeriggio, la serra svuotata. Rimane solo lei, a potare una rosa nera con un coltellino da cucina che non è affatto da cucina."
    if route_seconda == "aede":
        $ aede_sospetto += 1
        "Mi giunge voce che Aede ha chiesto dove passo i pomeriggi. Qualcuno ha risposto: in serra."
    ofelia "Tutti mi chiedono cosa voglio. Nessuno si domanda perché lo chiedo a voce così alta. Fa parte del gioco, immagino."
    ofelia "Aede risponde con la spada. Ascadeo con una battuta e una porta che sbatte. Io poto le rose. Ognuno ha il suo modo di non parlare con nostro padre."
    "Lo stelo cade nel cesto. Lei lo segue con gli occhi come si segue un nemico che si arrende troppo presto."
    menu:
        "Non mi guarda. Taglia, con calma, uno stelo."
        "«Vuoi che resti, o che me ne vada?»":
            $ ofelia_affinity += 1
            show ofelia compiaciuta with qdiss
            ofelia "Domanda corretta. Rimani, finché ho le forbici in mano. Dopo, vedremo."
            "Resto. Lei pota altre tre rose, poi altre due. Le forbici non le posa mai."
        "«Sei la più bella di Zefiro, lo sai.»":
            $ ofelia_affinity -= 1
            show ofelia rabbia with qdiss
            ofelia "Lo so. Lo sa anche il cavallo. Esci dalla fila, per favore."
            "Il coltellino fa uno scatto secco. Una rosa intera, bocciolo compreso, finisce nel cesto."
        "Aiutarla a raccogliere gli steli tagliati":
            show ofelia neutra with qdiss
            ofelia "Ti sporchi le mani per una rosa che non è tua. Strano modo di corteggiare."
            "Una spina mi entra nel pollice. Ofelia la guarda, poi guarda me, e non dice niente. Mi passa un fazzoletto nero."
    return


## Evento 1 — Il pretendente scartato ##########################################

label ofelia_ev1:
    scene bg sala_svelo with fade
    show ofelia neutra with dissolve
    "Ofelia mi ha fatto chiamare in serra con un biglietto di tre parole: «Vieni. Guarda. Taci.»"
    "Al centro del vialetto, un giovane in giubba nuova stringe un mazzo di rose bianche. Le mani gli tremano."
    ofelia "Dicevi, Lucio? Ripeti pure. La parte sul mio sorriso."
    "Lui ripete. Lei lo lascia finire, poi inclina la testa, come davanti a un quadro storto."
    ofelia "Ti sei preparato davanti allo specchio. Si sente dalle pause. Anche lo specchio, poveretto, ti ha detto di no."
    "Dal fondo della serra qualcuno soffoca una risata. Poi un'altra. Il ragazzo diventa rosso fino alle orecchie."
    ofelia "Le rose bianche, poi. Sono i fiori dei funerali, a Zefiro. Forse sapevi qualcosa che io ignoro."
    "Lucio apre la bocca. Non ne esce niente. Le rose, nel suo pugno, cominciano a perdere petali."
    menu:
        "Ofelia mi lancia un'occhiata di lato. Aspetta di vedere da che parte sto."
        "Ridere con gli altri: in fondo è teatro":
            $ ofelia_affinity -= 1
            show ofelia rabbia with qdiss
            ofelia "Ecco. Un coro. Sapevo che ti avrei trovat[fin] nel coro."
            "Il ragazzo mi guarda, poi guarda per terra. Esce senza le rose."
        "Fare un passo avanti: «Basta, Ofelia. Lascialo andare.»":
            $ ofelia_affinity -= 1
            show ofelia rabbia with qdiss
            ofelia "[Il_t] paladin[fin]. Che noia mortale. So umiliare un uomo da sola, grazie, senza nessuno che mi salvi."
            "Il ragazzo approfitta della pausa per scappare. Non mi ringrazia."
        "Restare immobile, senza ridere e senza intervenire":
            $ ofelia_affinity += 2
            show ofelia compiaciuta with qdiss
            ofelia "Né il coro né [il_t] paladin[fin]. Strano: sei l'unic[fin] che non ha fatto il verso a nessuno dei due."
            "Si china a raccogliere una rosa caduta e la annusa, distratta."
            ofelia "Lucio non tornerà. Se ti chiedono com'è andata, di' che il fiore era buono. Questo almeno è vero."
    "Più tardi, uscendo, incrocio i servi che spazzano il vialetto. Raccolgono petali bianchi con la stessa cura con cui si raccolgono i cocci."
    "Ofelia non si è voltata a guardarmi andare via. Ma il biglietto di tre parole, ripiegato, è ancora nella mia tasca. Non lo butto."
    return


## Evento 2 — Il rivale ########################################################

label ofelia_ev2:
    scene bg sala_svelo with fade
    show ofelia neutra with dissolve
    "Ofelia mi aspetta alla porta di una sala illuminata, avvolta in un velo scuro che fa sembrare la cena un funerale elegante."
    ofelia "Una cena. Tu mi offri il braccio, sorridi e non fai domande. Fino al dolce."
    "A capotavola siede un uomo dall'anello pesante e dal sorriso ancora più pesante. Il più alto in grado tra i suoi corteggiatori."
    "Non mi saluta. Guarda il mio braccio sotto il suo e calcola quanto valgo."
    ofelia "Un amico. Uno che da mesi non sopporta di non avermi."
    show ofelia compiaciuta with qdiss
    "Lei mi sfiora la manica con la punta delle dita. Troppo lentamente per essere vero. Troppo bene per non essere recitato."
    "Si mangia fagiano in salsa di more. L'uomo con l'anello racconta di un affare con il Ceppo di Glauco, e lo racconta guardando solo lei."
    "Ofelia ride al momento giusto. Mai un attimo prima, mai uno dopo. Sotto il tavolo, la sua scarpa preme sulla mia: ora tocca a te."
    ofelia "Mio padre dice che hai il fiuto per i buoni affari. Peccato che tu non abbia quello per le cause perse."
    menu:
        "A metà cena l'uomo aspetta una mia mossa. Ofelia, anche."
        "Stare al gioco, con stile: baciarle la mano come se fosse mia da sempre":
            $ ofelia_affinity += 2
            show ofelia imbarazzata with qdiss
            ofelia "...Non era previsto così bene. Ti avevo scelt[fin] per fare numero, e invece reciti meglio di lui."
            show ofelia compiaciuta with qdiss
            "L'uomo posa il bicchiere. Per il resto della sera non guarderà più né lei né me."
        "Dirlo in faccia, piano: «Mi stai usando, Ofelia. Lo faccio volentieri, ma voglio che tu lo sappia.»":
            $ ofelia_affinity += 1
            show ofelia neutra with qdiss
            ofelia "Lo so. Ma pochi me lo dicono prima del dolce. Lo rispetto. Non lo ripeterò."
            "Il rivale ci ha sentiti, ma non ha capito: sorride come uno che non ha ancora perso."
        "Fare una scenata: «Io che ci faccio qui? Dimmelo davanti a lui!»":
            $ ofelia_affinity -= 1
            show ofelia rabbia with qdiss
            with hpunch
            ofelia "Siediti. Ora. Mi hai fatta passare per una che deve chiedere il permesso a un ospite."
            "L'uomo con l'anello si alza, gentile come un coltello, e le offre il suo braccio. Lei lo accetta e non si volta."
    "Il dolce arriva lo stesso: una torta di castagne che nessuno tocca. La guardo raffreddarsi, e penso che Ofelia sia fatta di regole che non ha mai scritto."
    return


## Interludio 1 — Le lame di Glauco (Luna II+, nessun punto) ##################

label interludio_ofelia_1:
    scene bg studio_glauco with fade
    show ofelia neutra with dissolve
    "Mattina presto. Lo studio di Glauco è vuoto del suo padrone: è al Consiglio fino a mezzogiorno, dice il biglietto. Ofelia no."
    "È seduta per terra, tra le lame di suo padre stese su un telo. Ha le maniche arrotolate e una cote in mano."
    ofelia "Chiudi la porta. Se entra un servo, ti ho chiamat[fin] per portare l'olio. Se entra mio padre, non ti ho chiamat[fin] affatto."
    "Il suono della cote sull'acciaio è regolare come un respiro. Lei non alza gli occhi."
    ofelia "Le affilo io da quando avevo nove anni. Lui crede che lo faccia il fabbro. Il fabbro è morto da sei inverni."
    ofelia "Aede le usa. Ascadeo le perde ai dadi e poi le ricompra. Io sono l'unica che sa quante sono."
    show ofelia compiaciuta with qdiss
    ofelia "Trentadue. Una ha ucciso un re, dicono. Un'altra non ha mai visto sangue. Indovina quale tiene sopra il letto."
    menu:
        "Mi porge una lama, il filo verso di sé. Aspetta."
        "«Quella che non ha mai visto sangue.»":
            show ofelia neutra with qdiss
            ofelia "Giusto. Dice che una lama pulita è una promessa. Io dico che è una minaccia che non ha ancora scelto il bersaglio."
            "Rimette la lama al suo posto sul telo. In fila con le altre, perfettamente parallela."
        "«Nessuna delle due. Glauco non dorme.»":
            show ofelia compiaciuta with qdiss
            ofelia "...questo è quasi divertente. Hai ragione, in effetti. Non l'ho mai visto dormire."
            "Per un istante ride, piano, con la cote ferma a mezz'aria. Poi ricomincia ad affilare, più svelta."
        "Prendere la cote e affilare la lama in silenzio":
            show ofelia imbarazzata with qdiss
            "La pietra scivola male, le prime volte. Ofelia mi corregge il polso con due dita, senza una parola."
            ofelia "Più lento. Il filo non si conquista: si convince."
            show ofelia neutra with qdiss
            "Lavoriamo così per un'ora, spalla contro spalla. Non le ho mai sentito un tono così basso."
    "Fuori suona mezzogiorno. Ofelia arrotola il telo con le lame dentro, veloce, come chi l'ha fatto mille volte."
    ofelia "Non è successo niente. Io ero in serra, tu eri a lezione. Le lame si sono affilate da sole."
    hide ofelia with dissolve
    "Esco dal corridoio di servizio. Ho le dita nere di olio, e nessuna voglia di lavarle."
    return


## Interludio 2 — Il libro di Ascadeo (Luna III+, nessun punto) ###############

label interludio_ofelia_2:
    scene bg corridoio_ceppo with fade
    show ofelia neutra with dissolve
    "Sera. Ofelia mi aspetta in fondo al corridoio del Ceppo, sotto l'unica torcia accesa. In mano ha una lettera col sigillo rotto a metà."
    ofelia "È di Ascadeo. Mio fratello tiene un libro di scommesse sui miei pretendenti. Da tre anni. Ci guadagna più che con le lame."
    ofelia "Questa è la quotazione della settimana. Il tuo nome c'è. Non l'ho ancora letta."
    "Il sigillo è quello di Glauco, ma rovesciato. Una cosa da fratello minore: rubare lo stemma e usarlo storto."
    show ofelia compiaciuta with qdiss
    ofelia "Leggila tu. Ad alta voce. Voglio vedere che faccia fai quando scopri quanto vali sul mercato."
    "Apro. La calligrafia è svelta, piena di sottolineature. In fondo, un elenco di nomi con numeri accanto."
    "Il mio è in mezzo. Accanto, una cifra, e una nota: «Resiste più del previsto. Sospetto che le piaccia. Alzo la posta.»"
    menu:
        "Ofelia mi guarda leggere. Le braccia conserte, il mento alto."
        "Leggere tutto, nota compresa":
            show ofelia imbarazzata with qdiss
            ofelia "...«sospetto che le piaccia». Ascadeo sospetta molte cose. Perde la metà delle scommesse."
            show ofelia neutra with qdiss
            ofelia "L'altra metà, però, la vince sempre. È questo il guaio dei fratelli minori."
        "Leggere solo la cifra, e tacere la nota":
            show ofelia neutra with qdiss
            ofelia "Tutto qui? Una cifra? Ascadeo scrive sempre una nota. Gli piace sentirsi spiritoso."
            "Mi strappa la lettera di mano e legge da sola. Poi la piega in quattro, lentamente, e non commenta."
        "Bruciarla alla torcia senza leggerla":
            show ofelia rabbia with qdiss
            ofelia "Che gesto teatrale. Adesso dovrò chiederglielo a voce, e lui riderà per una settimana."
            show ofelia compiaciuta with qdiss
            ofelia "Però. Nessuno aveva mai bruciato un mio pettegolezzo prima di me. Mi hai rubato il mestiere."
    "In fondo al corridoio, una porta sbatte. Passi veloci, una risata maschile che si allontana."
    ofelia "Ecco. Ci ha sentiti. Domani la tua quota cambia, e non so in che direzione."
    hide ofelia with dissolve
    "Resto sol[fin] con la torcia. Penso a un ragazzo che non ho mai visto, chino su un libro, a scommettere su di me."
    return


## Deviazione (Luna II+) — Lo specchio #########################################

label specchio_ofelia:
    scene bg sala_svelo with fade
    "Il retro della serra, dove Glauco fa crescere le piante che non mostra. Tra due limoni, uno specchio alto quanto una porta."
    show ofelia neutra with dissolve
    "Ofelia è davanti allo specchio con tre vestiti appesi a un ramo. Non si volta quando entro."
    ofelia "Ricevimento dagli Asi, stasera. Il verde, il nero o il rosso. Dimmi la verità."
    ofelia "Prima di rispondere, sappi che la verità non mi interessa. Mi interessa vedere se hai il coraggio di dirla."
    "Prende il verde, se lo appoggia addosso. Poi il nero. Il rosso non lo tocca: lo guarda soltanto, come una cosa che non si è ancora meritata."
    menu:
        "Lo specchio riflette lei, poi me dietro di lei. Aspetta."
        "«Il rosso. Ma solo se smetti di guardarlo come se dovessi chiedergli il permesso.»":
            $ ofelia_specchio_esito = "rosso"
            $ ofelia_affinity += 1
            show ofelia compiaciuta with qdiss
            ofelia "Il permesso. A un vestito."
            "Si volta. Per un istante sembra davvero offesa. Poi stacca il rosso dal ramo senza guardarlo più."
            ofelia "Se stasera qualcuno mi chiede chi l'ha scelto, dirò che è stato un errore. Il tuo."
        "«Stai bene con tutti e tre.»":
            $ ofelia_specchio_esito = "tutti"
            show ofelia neutra with qdiss
            ofelia "Lo dicono tutti. È per questo che non chiedo mai a nessuno."
            "Appende i vestiti al ramo, uno dopo l'altro, con la cura di chi rimette a posto la propria pazienza."
            ofelia "Puoi andare. Lo specchio, almeno, non mi adula."
        "«Chiedilo allo specchio. È lui che ti conosce da più tempo.»":
            $ ofelia_specchio_esito = "specchio"
            show ofelia imbarazzata with qdiss
            "Ride. Una risata corta, sorpresa, che le sfugge prima che possa sistemarla."
            ofelia "Lo specchio mi conosce da diciannove anni. E ancora non ha capito che il nero lo metto quando ho paura."
            "Si accorge di averlo detto. Prende il nero e se lo appoggia addosso, in fretta, come per coprire la frase."
    "Uscendo, passo accanto ai limoni. Uno è caduto e nessuno l'ha raccolto. In casa di Glauco, nemmeno la frutta cade per caso."
    return


## Deviazione (Luna III+) — Il ballo dei pretendenti ###########################

label ballo_pretendenti:
    scene bg sala_svelo with fade
    "Ricevimento di fine Luna nella serra di Glauco. Candele tra le foglie, musica d'archi, venti pretendenti che fingono di non contarsi."
    show ofelia compiaciuta with dissolve
    "Ofelia mi prende sottobraccio a metà sala, come se ci fossimo dati appuntamento. Non ci siamo dati appuntamento."
    ofelia "Gioco nuovo. Stasera ne rimando a casa uno. Davanti a tutti. Lo scegli tu."
    ofelia "Il biondo che recita versi non suoi. Il Lumina con la spilla di sua madre. Quello in fondo, che mi fissa da tre Lune e non ha mai aperto bocca."
    "Ascadeo, dall'altro lato della sala, apre il suo libretto. Ha già una colonna per il mio nome."
    menu:
        "Il braccio di Ofelia è leggero sul mio. Non lo sarà a lungo."
        "«Nessuno. Il tuo gioco, giocalo da sola.»":
            $ ofelia_ballo_esito = "rifiuto"
            show ofelia neutra with qdiss
            ofelia "Una coscienza. A una festa. Che cosa fuori moda."
            "Mi lascia il braccio. Dieci minuti dopo il biondo esce dalla serra con la faccia di uno che ha appena sentito recitare i suoi versi meglio di lui."
        "«Il biondo. Chi ruba versi, ruba anche il resto.»":
            $ ofelia_ballo_esito = "biondo"
            ofelia "Motivazione accettabile. Esecuzione: mia."
            "Lo raggiunge, gli sussurra due frasi. Il biondo diventa grigio, poi bianco, poi assente."
            show ofelia compiaciuta with qdiss
            ofelia "Visto? Basta poco. Adesso sei complice, e i complici non tornano indietro."
        "«Me. Rimandami a casa davanti a tutti, se ci riesci.»":
            $ ofelia_ballo_esito = "me"
            $ ofelia_affinity += 1
            show ofelia imbarazzata with qdiss
            "Per un istante non dice niente. Gli archi continuano a suonare, ignari."
            ofelia "Non ci riesco. Sarebbe la prima volta. Non ti darò la soddisfazione di saperlo."
            "Mi lascia il braccio e se ne va verso i pretendenti. Ma per tutta la sera non ne rimanda a casa nessuno."
    "In fondo alla sala Ascadeo chiude il libretto con uno scatto. Accanto al mio nome, credo, ha scritto un punto interrogativo."
    return
