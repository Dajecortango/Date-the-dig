# Route Ofelia — Atto 1: la corte (attivita'), eventi 1-2, interludi 1-2.

## Corte 1 — La fila ##########################################################

label att_corte_1:
    scene bg sala_svelo with fade
    show ofelia neutra with dissolve
    "La serra di Glauco in pieno inverno: fiori che non dovrebbero esistere e una fila di pretendenti che sembra voler somigliare a loro."
    "Ofelia li passa in rassegna uno per uno, e a ciascuno dedica mezzo respiro. Nessuno regge il suo sguardo oltre il secondo."
    if route_seconda == "aede":
        $ aede_sospetto += 1
        "Mi accorgo troppo tardi che una servetta ci osserva dal corridoio. Domani Aede saprà che sono passat[fin] alla serra."
    "L'aria sa di terra umida e di brace. Sotto il pavimento corrono i tubi caldi di Glauco: d'inverno, qui dentro, è sempre una primavera a pagamento."
    ofelia "Il quarto da sinistra mi ha dedicato un sonetto. Il terzo, un cavallo. Il cavallo era più eloquente."
    "Il primo della fila fa un passo avanti e si inchina troppo. Lei aspetta che si rialzi, poi gli porge il dorso della mano. Prima che lui ci arrivi, l'ha già ritirata."
    ofelia "Grazie. Il prossimo."
    if "ofelia_ev1" in eventi_visti:
        "Mi rimetto in fila, per abitudine, e Ofelia finge di non avermi visto. I pretendenti dietro di me non capiscono perché le trema un angolo della bocca."
    else:
        "Il prossimo sono io. I pretendenti dietro di me si sporgono per vedermi fallire."
    menu:
        "Tocca a me: mi guarda e aspetta."
        "«Il tuo giardino è splendido, Ofelia. Quasi quanto te.»":
            $ ofelia_affinity -= 1
            show ofelia rabbia with qdiss
            ofelia "Quasi. Che parola generosa. Prendila con te e cedi il posto al prossimo."
            "Alle mie spalle qualcuno sospira di sollievo."
        "«Non ti dirò niente di bello. Hai già sentito tutto.»":
            $ ofelia_affinity += 1
            show ofelia compiaciuta with qdiss
            ofelia "...e il bello è che è vero. Resta pure in fila. In fondo, ma resta."
            "Il poeta del sonetto mi guarda storto: gli ho appena rubato l'unica battuta."
        "Resta in silenzio a guardare i fiori":
            show ofelia neutra with qdiss
            ofelia "Almeno non mi hai rubato l'aria. Già qualcosa."
            "Indico un fiore blu, chiuso come un pugno. Lei segue il mio dito e dimentica la fila."
            ofelia "Quello l'ha piantato mio padre, il giorno che sono stata adottata. Non è mai fiorito, ma lo teniamo per ostinazione."
    return


## Corte 2 — Il guanto ########################################################

label att_corte_2:
    scene bg sala_svelo with fade
    show ofelia neutra with dissolve
    "Oggi è lei a muoversi. Attraversa la serra con un guanto in mano, e un giovane damerino le inciampa dietro, tutto occhi."
    if route_seconda == "aede":
        $ aede_sospetto += 1
        "In corridoio sento passare il mio nome tra due ancelle. La voce farà in fretta, e Aede ha l'udito fine."
    ofelia "Uno dei miei corteggiatori sostiene di aver combattuto un orso per me. È una bugia: voglio vedere fin dove arriva."
    "Il damerino si chiama Tullio, a quanto dice lui stesso, tre volte in un minuto. Ha la manica strappata con molta cura."
    "Ofelia lascia cadere il guanto sul vialetto. Lui si precipita a raccoglierlo, e glielo porge in ginocchio come una reliquia."
    ofelia "Vedi? Riporta. Questo almeno lo sa fare."
    menu:
        "Il pretendente si volta verso di me, in cerca di un alleato."
        "Dagli ragione: «Un orso, certo. Enorme.»":
            $ ofelia_affinity -= 1
            show ofelia rabbia with qdiss
            ofelia "Un altro che mi serve quello che voglio sentire. Che stanchezza."
            "Tullio mi abbraccia come un fratello d'arme. Ofelia si allontana prima che possa abbracciare anche lei."
        "«L'orso non c'era. Ma i suoi graffi sul braccio sono veri.»":
            $ ofelia_affinity += 1
            show ofelia compiaciuta with qdiss
            ofelia "Esatto! Tieni gli occhi dove servono, tu."
            show ofelia neutra with qdiss
            ofelia "Era un gatto. Non dirglielo."
            "Tullio non ha capito niente. Ofelia gli restituisce il guanto, gentile, e lo congeda con una pacca sulla testa."
        "Svignatela prima che ti tiri in mezzo":
            show ofelia neutra with qdiss
            ofelia "Prudente. Non è una virtù che apprezzo, ma almeno è onesta."
            "Dalla porta la sento ancora: «Raccontami di nuovo dell'orso, Tullio. Quanto era grosso?»"
    return


## Corte 3 — Il lungo congedo ################################################

label att_corte_3:
    scene bg sala_svelo with fade
    show ofelia neutra with dissolve
    "Fine pomeriggio, la serra è vuota. C'è soltanto lei, a potare una rosa nera con delle grosse forbici affilate."
    if route_seconda == "aede":
        $ aede_sospetto += 1
        "Mi giunge voce che Aede ha chiesto dove passo i pomeriggi. Qualcuno ha risposto: in serra."
    ofelia "Tutti mi chiedono cosa voglio. Nessuno si domanda perché li lascio chiedere a voce così alta."
    ofelia "Aede risponde con la spada. Ascadeo con una battuta e una porta che sbatte. Io poto le rose. Ognuno ha il suo modo di non parlare con nostro padre."
    "Lo stelo cade nel cesto. Lei lo segue con gli occhi fino in fondo, delusa: si è arreso troppo presto."
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
            ofelia "Lo so. Lo sa anche il cavallo. Lasciami sola, per favore."
            "Le forbici fanno uno scatto secco. Una rosa intera, bocciolo compreso, finisce nel cesto."
        "Aiutala a raccogliere gli steli tagliati":
            show ofelia neutra with qdiss
            ofelia "Ti sporchi le mani per una rosa che non è tua. Strano modo di corteggiare."
            "Una spina mi entra nel pollice. Ofelia la guarda, poi guarda me, e mi passa un fazzoletto nero."
    return


## Evento 1 — Il pretendente scartato ##########################################

label ofelia_ev1:
    scene bg sala_svelo with fade
    show ofelia neutra with dissolve
    "Ofelia mi ha fatto chiamare in serra con un biglietto di tre parole: «Vieni. Guarda. Taci.»"
    "Al centro del vialetto un giovane vestito a festa stringe un mazzo di rose bianche, e il mazzo trema."
    ofelia "Dicevi, Levi? Ripeti pure. La parte sul mio sorriso."
    "Lui ripete. Lei lo lascia finire, poi inclina la testa, come davanti a un quadro storto."
    ofelia "Ti sei preparato davanti allo specchio. Si sente dalle pause. Anche lo specchio, poveretto, ti ha detto di no."
    "Dal fondo della serra arrivano due risate soffocate. Il ragazzo diventa rosso fino alle orecchie."
    ofelia "Le rose bianche, poi. Sono i fiori dei funerali, a Zefiro. Forse sapevi qualcosa che io ignoro."
    "Levi apre la bocca e non ne esce niente. Le rose, nel suo pugno, cominciano a perdere petali."
    menu:
        "Ofelia mi lancia un'occhiata di lato. Aspetta di vedere da che parte sto."
        "Ridi con gli altri: in fondo è teatro":
            $ ofelia_affinity -= 1
            show ofelia rabbia with qdiss
            ofelia "Ecco. Un coro. Sapevo che ti avrei trovat[fin] nel coro."
            "Il ragazzo mi guarda, poi guarda per terra. Esce senza le rose."
        "Fai un passo avanti: «Basta, Ofelia. Lascialo andare.»":
            $ ofelia_affinity -= 1
            show ofelia rabbia with qdiss
            ofelia "[Il_t] paladin[fin]. Che noia mortale. Voglio umiliare un uomo da sola, grazie, non ho bisogno di qualcuno che lo salvi."
            "Il ragazzo approfitta della pausa per scappare. Non mi ringrazia."
        "Resta immobile, senza ridere e senza intervenire":
            $ ofelia_affinity += 2
            show ofelia compiaciuta with qdiss
            ofelia "Né il coro né [il_t] paladin[fin]. Resta lì. Mi servono testimoni che sappiano stare zitti."
            "Si china a raccogliere una rosa caduta e la annusa, distratta."
            ofelia "Levi non tornerà. Se ti chiedono com'è andata, di' che il fiore era profumato. Questo almeno è vero."
    "Più tardi, uscendo, incrocio i servi che spazzano il vialetto. Raccolgono petali bianchi con la stessa cura con cui si raccolgono i cocci."
    "Ofelia non si è voltata a guardarmi andare via. Il biglietto di tre parole, ripiegato, è ancora nella mia tasca."
    return


## Evento 2 — Il rivale ########################################################

label ofelia_ev2:
    scene bg sala_svelo with fade
    show ofelia neutra with dissolve
    "Ofelia mi aspetta alla porta di una sala illuminata, avvolta in un velo scuro che fa sembrare la cena un funerale elegante."
    ofelia "Ho una cena. Tu mi offri il braccio, sorridi e non fai domande. Fino al dolce."
    "A capotavola siede un uomo dall'anello pesante e dal sorriso insistente: il più alto in grado tra i suoi corteggiatori."
    "Non mi saluta, guarda il mio braccio sotto il suo e calcola quanto valgo."
    ofelia "Un amico. Uno che da mesi non sopporta di non avermi."
    show ofelia compiaciuta with qdiss
    "Mi sfiora la manica con la punta delle dita, troppo lentamente per essere vero."
    "Si mangia fagiano in salsa di more. L'uomo con l'anello racconta di un affare con il Ceppo di Glauco, e lo racconta guardando solo lei."
    "Ofelia ride al momento giusto, mai un attimo prima. Sotto il tavolo la sua scarpa preme sulla mia: ora tocca a me."
    ofelia "Mio padre dice che hai il fiuto per i buoni affari. Peccato che tu non abbia quello per le cause perse."
    menu:
        "A metà cena l'uomo aspetta una mia mossa. Ofelia, anche."
        "Stai al gioco, con stile: baciale la mano come se fosse tua da sempre":
            $ ofelia_affinity += 2
            show ofelia compiaciuta with qdiss
            ofelia "Non avevo idea fossi così brav[fin]. Ti avevo scelt[fin] per fare numero, e invece reciti meglio di lui."
            show ofelia compiaciuta with qdiss
            "L'uomo posa il bicchiere. Per il resto della sera non guarderà più né lei né me."
        "Dille in faccia, piano: «Mi stai usando, Ofelia. Lo faccio volentieri, ma voglio che tu lo sappia.»":
            $ ofelia_affinity += 1
            show ofelia neutra with qdiss
            ofelia "Lo so. Ma pochi me lo dicono prima del dolce. Lo rispetto. Non riaccadrà."
            "Il rivale ci ha sentiti, ma non ha capito: sorride come uno che non ha ancora perso."
        "Fai una scenata: «Io che ci faccio qui? Dimmelo davanti a lui!»":
            $ ofelia_affinity -= 1
            show ofelia rabbia with qdiss
            with hpunch
            ofelia "Siediti. Ora. Mi hai fatta passare per una che deve chiedere scusa a un ospite."
            "L'uomo con l'anello si alza, gentile come un coltello, e le offre il suo braccio. Lei lo accetta e non si volta."
    "Il dolce arriva lo stesso: una torta di castagne che nessuno tocca. La guardo raffreddarsi."
    return


## Interludio 1 — Le lame di Glauco (Luna II+, nessun punto) ##################

label interludio_ofelia_1:
    scene bg studio_glauco with fade
    show ofelia neutra with dissolve
    "Mattina presto. Lo studio di Glauco è vuoto del suo padrone: è al Consiglio fino a mezzogiorno, dice il biglietto. Ofelia no."
    "È seduta per terra, tra le lame di suo padre stese su un telo. Ha le maniche arrotolate e una cote in mano."
    ofelia "Chiudi la porta. Se entra un servo, ti ho chiamat[fin] per portare l'olio. Se entra mio padre, non ti ho chiamat[fin] affatto."
    "Il suono della cote sull'acciaio è regolare come un respiro. Lei non alza gli occhi."
    ofelia "Le affilo io da sempre. Lui crede che lo faccia il fabbro. Il fabbro è morto da sei inverni."
    ofelia "Aede le usa. Ascadeo le perde ai dadi e poi le ricompra. Io sono l'unica che sa quante sono."
    show ofelia compiaciuta with qdiss
    ofelia "Trentadue. Una ha ucciso un re, dicono. Un'altra non ha mai visto sangue. Indovina quale tiene sopra il letto."
    menu:
        "Mi porge una lama, il filo verso di sé. Aspetta."
        "«Quella che non ha mai visto sangue.»":
            show ofelia neutra with qdiss
            ofelia "Giusto. Dice che una lama pulita è una promessa. Io dico che è una minaccia che non ha ancora scelto il bersaglio."
            "Rimette la lama al suo posto sul telo, in fila con le altre, perfettamente parallela."
        "«Nessuna delle due. Glauco non dorme.»":
            show ofelia compiaciuta with qdiss
            ofelia "...questo è quasi divertente. Hai ragione, in effetti. Non l'ho mai visto dormire."
            "Ride, piano, con la cote ferma a mezz'aria, e ricomincia ad affilare più svelta."
        "Prendi la cote e affila la lama in silenzio":
            show ofelia imbarazzata with qdiss
            "La pietra scivola male, le prime volte. Ofelia mi corregge il polso con due dita."
            ofelia "Più lento. Il filo non si conquista: si convince."
            show ofelia neutra with qdiss
            "Lavoriamo così per un'ora, spalla contro spalla. Non le ho mai sentito un tono così basso."
    "Fuori suona mezzogiorno. Ofelia arrotola il telo con le lame dentro, in tre gesti."
    ofelia "Questa cosa non è mai successa. Io ero in serra, tu eri a lezione. Le lame si sono affilate da sole."
    hide ofelia with dissolve
    "Esco dal corridoio di servizio. Ho le dita nere di olio e nessuna voglia di lavarle."
    return


## Interludio 2 — Il libro di Ascadeo (Luna III+, nessun punto) ###############

label interludio_ofelia_2:
    scene bg corridoio_ceppo with fade
    show ofelia neutra with dissolve
    "Sera. Ofelia mi aspetta in fondo al corridoio del Ceppo, sotto l'unica torcia accesa. In mano ha una lettera col sigillo rotto a metà."
    ofelia "È di Ascadeo. Mio fratello tiene un libro di scommesse sui miei pretendenti, da tre anni. Ci guadagna da matti."
    ofelia "Questa è la quotazione della settimana. Il tuo nome c'è. Non l'ho ancora letta."
    "Il sigillo è quello di Glauco, ma rovesciato. Una cosa tipica da figli: rubare lo stemma e usarlo storto."
    show ofelia compiaciuta with qdiss
    ofelia "Leggila tu. Ad alta voce. Voglio vedere che faccia fai quando scopri quanto vali sul mercato."
    "Apro. La calligrafia è svelta, piena di sottolineature. In fondo, un elenco di nomi con numeri accanto."
    "Il mio è in mezzo. Accanto, una cifra, e una nota: «Resiste più del previsto. Sospetto che le piaccia. Alzo la posta a dieci Lenora d'oro.»"
    menu:
        "Ofelia mi guarda leggere. Le braccia conserte, il mento alto."
        "Leggi tutto, nota compresa":
            show ofelia neutra with qdiss
            ofelia "«Sospetto che le piaccia.» Ascadeo sospetta molte cose, ma perde la metà delle scommesse."
            show ofelia neutra with qdiss
            ofelia "La metà che vince, però, è perché ha ragione. È questo il guaio di mio fratello."
        "Leggi solo la cifra, non la nota":
            show ofelia neutra with qdiss
            ofelia "Tutto qui? Una cifra? Ascadeo scrive sempre una nota. Gli piace sentirsi spiritoso."
            "Mi strappa la lettera di mano, la legge da sola e la piega in quattro, senza commenti."
        "Bruciala con la torcia senza leggerla":
            show ofelia rabbia with qdiss
            ofelia "Che gesto teatrale. Adesso dovrò chiederglielo a voce, e lui riderà per una settimana."
            show ofelia compiaciuta with qdiss
            ofelia "Però... Nessuno aveva mai bruciato un mio pettegolezzo prima di me. Mi hai rubato il mestiere."
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
    "Ofelia è davanti allo specchio con tre vestiti appesi a un gancio. Non si volta quando entro."
    ofelia "Ricevimento dai Lomor, stasera. Allora: il verde, il nero o il rosso? Dimmi la verità."
    ofelia "Prima di rispondere, sappi che la verità non mi interessa. Mi interessa vedere se hai il coraggio di dirla."
    "Prende il verde e se lo appoggia addosso, poi il nero. Il rosso non lo tocca: lo guarda, come una cosa che non si è ancora meritata."
    menu:
        "Lo specchio riflette lei, poi me dietro di lei. Aspetta."
        "«Il rosso. Ma solo se smetti di guardarlo come se dovessi chiedergli il permesso.»":
            $ ofelia_specchio_esito = "rosso"
            $ ofelia_affinity += 1
            show ofelia compiaciuta with qdiss
            ofelia "Il permesso. A un vestito."
            "Si volta, e sembra davvero offesa. Stacca il rosso dal gancio senza guardarlo più."
            ofelia "Se stasera qualcuno mi chiede chi l'ha scelto, dirò che è stato un errore. Il tuo."
        "«Stai bene con tutti e tre.»":
            $ ofelia_specchio_esito = "tutti"
            show ofelia neutra with qdiss
            ofelia "Lo dicono tutti. È per questo che non chiedo mai a nessuno."
            "Appende i vestiti al gancio, uno dopo l'altro, con la cura di chi rimette a posto la propria pazienza."
            ofelia "Puoi andare. Lo specchio, almeno, non mi adula."
        "«Chiedilo allo specchio. È lui che ti conosce da più tempo.»":
            $ ofelia_specchio_esito = "specchio"
            show ofelia imbarazzata with qdiss
            "Ride. Una risata corta, sorpresa, che le sfugge prima che possa sistemarla."
            ofelia "Lo specchio mi conosce da ventinove anni. E ancora non ha capito che il nero lo metto quando ho paura."
            "Si ferma. Prende il nero e se lo appoggia addosso, in fretta, come per coprire la frase."
    "Uscendo, passo accanto ai limoni. Uno è caduto e nessuno l'ha raccolto. In casa di Glauco, nemmeno la frutta cade per caso."
    return


## Deviazione (Luna III+) — Il ballo dei pretendenti ###########################

label ballo_pretendenti:
    scene bg sala_svelo with fade
    "Ricevimento di fine Luna nella serra di Glauco. Candele tra le foglie, musica d'archi, venti pretendenti che fingono di non contarsi."
    show ofelia compiaciuta with dissolve
    "Ofelia mi prende sottobraccio a metà sala, come se ci fossimo dati appuntamento."
    ofelia "Gioco nuovo. Stasera ne mando a casa uno, davanti a tutti. Lo scegli tu."
    ofelia "Il biondo che recita versi non suoi. Il nobile con la spilla di sua madre. Quello in fondo, che mi fissa da tre Lune e non ha mai aperto bocca."
    "Ascadeo, dall'altro lato della sala, apre il suo libretto. Ha già una colonna per il mio nome."
    menu:
        "Il braccio di Ofelia è leggero sul mio. Non lo sarà a lungo."
        "«Nessuno. Gioca da sola.»":
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
            "Non dice niente. Gli archi continuano a suonare."
            ofelia "Non ci riesco... Sarebbe la prima volta. Non ti darò questa soddisfazione."
            "Mi lascia il braccio e se ne va verso i pretendenti. Ma per tutta la sera non ne rimanda a casa nessuno."
    "In fondo alla sala Ascadeo chiude il libretto con uno scatto. Accanto al mio nome, credo, ha scritto un punto interrogativo."
    return
