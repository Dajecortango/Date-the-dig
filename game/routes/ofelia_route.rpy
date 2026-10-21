# Route Ofelia — "Tanto bella quanto letale". Difficoltà 4/5.
# Lucchetto dei mancati: Ofelia non aspetta. Ogni suo invito lasciato cadere
# costa un punto; al secondo, per lei sei già un nome tra tanti (congelata).
# Poliamore possibile solo con Aede (che NON sa e NON accetta) e con Caino
# (dichiarato). Mai con Druso o Icaro.

define ofelia = Character("Ofelia", color="#7d3c98", image="ofelia")

default ofelia_affinity = 0
default ofelia_mancati = 0
default route_seconda = None
default aede_sospetto = 0
# Esiti separati degli impegni a coppia (poliamore): Ofelia / l'altro.
default impegno_of = False
default impegno_altro = False
# Prove del poliamore segreto con Aede: cosa puo' rinfacciare nella tempesta.
default ofelia_mano_cala = False
default ofelia_in_pubblico = False

init python:
    ATTIVITA["pomeriggio"].append(
        ("corte", "La corte di Ofelia", "ofelia",
         ["att_corte_1", "att_corte_2", "att_corte_3"]))

    # Invito di Ofelia lasciato cadere (scelto altro o un'attivita'): mancato.
    # Conteggio in rlz.ofelia_esiti_scadenza: congela a ofelia_mancati >= 2
    # (rlz.OFELIA_GELO), al primo (ofelia_mancati == 1) la scena di avviso.
    def ofelia_scadenza(ids):
        for esito in rlz.ofelia_esiti_scadenza(
                ids, store.ofelia_mancati, "ofelia" in store.congelate):
            store.ofelia_mancati += 1
            store.ofelia_affinity -= 1
            if esito == "gelo":
                store.congelate.add("ofelia")
                renpy.notify("Per Ofelia sei già un nome tra tanti.")
            elif esito == "prima":
                renpy.call_in_new_context("ofelia_scadenza_prima")
            else:
                renpy.notify("Ofelia non aspetta nessuno.")

    cal_inviti_ignorati_hooks.append(ofelia_scadenza)

    # Eventi a soglia: inviti che scadono (ignorarli costa un mancato).
    EVENTI.extend([
        {"id": "ofelia_ev1", "label": "ofelia_ev1", "tipo": "invito",
         "char": "ofelia", "scade": True,
         "titolo": "Ofelia ti vuole in serra, a guardare qualcuno cadere",
         "luna_min": 1, "slot": "pomeriggio",
         "cond": lambda v: v["ofelia_affinity"] >= 2},
        {"id": "ofelia_ev2", "label": "ofelia_ev2", "tipo": "invito",
         "char": "ofelia", "scade": True,
         "titolo": "Una cena a due, con un terzo che non lo sa",
         "luna_min": 2, "slot": "sera",
         "cond": lambda v: v["ofelia_affinity"] >= 4
         and "ofelia_ev1" in v["visti"]},
        {"id": "ofelia_ev3", "label": "ofelia_ev3", "tipo": "invito",
         "char": "ofelia", "scade": True,
         "titolo": "All'alba, in arena, con due lame vere",
         "luna_min": 3, "slot": "mattina",
         "cond": lambda v: v["ofelia_affinity"] >= 6
         and "ofelia_ev2" in v["visti"]
         and "scelta_cuore" not in v["visti"]},
        # Dopo la Fiaccolata, a route attiva: farsi vedere o restare segreto.
        {"id": "ofelia_ev4", "label": "ofelia_ev4", "tipo": "fisso",
         "char": "ofelia", "luna": 5, "giorno": 26, "slot": "pomeriggio",
         "cond": lambda v: v["route_attiva"] == "ofelia"
         and "ofelia" not in v["congelate"]},
        # Interludi: inviti SENZA scadenza e con id che non inizia per
        # "ofelia_" (l'hook ofelia_scadenza non li conta). Nessun punto.
        {"id": "interludio_ofelia_1", "label": "interludio_ofelia_1",
         "tipo": "invito", "char": "ofelia",
         "titolo": "Ofelia affila le lame di suo padre, e non vuole testimoni",
         "luna_min": 2, "slot": "mattina",
         "cond": lambda v: "ofelia_ev1" in v["visti"]
         and "scelta_cuore" not in v["visti"]},
        {"id": "interludio_ofelia_2", "label": "interludio_ofelia_2",
         "tipo": "invito", "char": "ofelia",
         "titolo": "Una lettera di Ascadeo, e Ofelia che non la vuole aprire da sola",
         "luna_min": 3, "slot": "sera",
         "cond": lambda v: "ofelia_ev2" in v["visti"]
         and "scelta_cuore" not in v["visti"]},
        # Luna VI, prima del climax: la serra d'inverno, a route attiva.
        {"id": "interludio_ofelia_luna6", "label": "interludio_ofelia_luna6",
         "tipo": "fisso", "char": "ofelia",
         "luna": 6, "giorno": 5, "slot": "pomeriggio",
         "cond": lambda v: v["route_attiva"] == "ofelia"
         and "ofelia" not in v["congelate"]},
    ])


## Primo invito mancato: cosa succede a chi non si presenta ##################

label ofelia_scadenza_prima:
    scene bg corridoio_ceppo with fade
    "Il biglietto di Ofelia è ancora sul davanzale, piegato in quattro. Nessuno l'ha toccato, nessuno l'ha rispedito."
    "Stava lì ad aspettarmi, e io non mi sono presentat[fin]."
    "Vanna lo raccoglie con due dita, come si raccoglie qualcosa che potrebbe mordere."
    vanna "L'ha scritto lei, e non lo scriverà due volte. Ofelia non ripete gli inviti, [fratello_t]. Chi manca una volta è una svista. Chi manca due volte esce dalla corte."
    "Poi sorride, un po' dispiaciuta, e il biglietto sparisce nella sua manica."
    return


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


## Evento 3 — Il duello all'alba ###############################################

label ofelia_ev3:
    scene bg arena_athlion with fade
    show ofelia neutra with dissolve
    "L'arena all'alba sembra più grande: sabbia fredda, gradini vuoti, il fiato che si condensa in nuvole."
    "Ofelia ha due spade da allenamento. Non sono spuntate."
    ofelia "Dicono che tu sappia cavartela. Io dico che nessuno conosce la mia mano finché non l'ha vista dall'altra parte."
    "Mi lancia l'elsa. La afferro appena in tempo."
    ofelia "Fino al primo sangue. Non è un modo di dire."
    ofelia "Mio padre mi ha messo una spada in mano prima di una bambola. Aede ha imparato a colpire forte. Io ho imparato a colpire quando nessuno guarda."
    "Si toglie il mantello e lo piega sul gradino più basso, con calma, come se avessimo tutto il giorno. Poi si gira, e il giorno finisce."
    "Il primo colpo mi sfiora la guancia. Il secondo no. Lei è veloce, e non ha alcuna fretta di finire."
    "Paro una volta, per fortuna. Lei sorride: non per la parata, per la fortuna. La riconosce, e la disprezza."
    with hpunch
    "Cado su un ginocchio, la lama alla gola. Sopra di me, il suo respiro regolare."
    menu:
        "Ofelia non muove la spada. Attende la mia mossa."
        "Reggere il suo sguardo: «Colpisci pure. Non chiederò pietà.»":
            $ ofelia_affinity += 2
            show ofelia compiaciuta with qdiss
            ofelia "Nessuno regge. Nemmeno Aede, da bambine, e di coraggio ne ha per tre."
            "Abbassa la lama. Mi tende la mano libera, e noto che trema appena. Per l'attesa, forse. Per qualcos'altro."
        "Arrendermi con eleganza: «Hai vinto. Ma ti è costato fatica, ammettilo.»":
            $ ofelia_affinity += 1
            show ofelia imbarazzata with qdiss
            ofelia "...Fatica no. Attenzione, sì. È diverso, ma ti concedo il bluff."
            show ofelia neutra with qdiss
            "Ritira la spada. Un filo di sangue mi scende dal collo, e lei lo guarda come si guarda un conto saldato."
        "Chiedere pietà, ridendo, con le mani in alto":
            show ofelia rabbia with qdiss
            ofelia "Pietà. Quanto è umana, la parola. Rialzati. Per oggi basta così."
            "Gira sui tacchi e se ne va, lasciandomi la spada nella sabbia."
    "Il sole sale sopra i gradini. Sulla sabbia restano le nostre impronte, le sue dritte e leggere, le mie sparse come quelle di chi è scappato."
    "Riporto le lame all'armeria. Il custode le pulisce, guarda la mia guancia e scuote la testa. Non è la prima volta che lo vede."
    return


## Evento 4 — Il velo (V/26) ##################################################

label ofelia_ev4:
    scene bg vicoli_zefiro with fade
    show ofelia neutra with dissolve
    "Pomeriggio. Ofelia mi aspetta all'imbocco dei vicoli, un velo scuro sul capo e un cesto vuoto al braccio. Travestita da nessuno."
    ofelia "Dopo la Fiaccolata, Zefiro parla. Di me, di te. Mi annoia: le storie migliori dovrebbe raccontarle chi c'era."
    ofelia "Vado al mercato. Posso andarci col velo, e tu due passi dietro come un servo. Oppure senza."
    show ofelia compiaciuta with qdiss
    ofelia "Senza, ci vedranno tutti. Mio padre compreso, entro sera. Ho il vestito giusto per entrambe le versioni."
    if route_seconda == "aede":
        "Il mercato è a due vicoli dal Ceppo di Glauco. Aede ci passa ogni giorno, a quest'ora."
    elif route_seconda == "caino":
        "Dall'altra parte della strada, sotto il portico del Consiglio, Caino finge di leggere un registro. Non gira pagina da un pezzo."
    "Il vicolo odora di pane e di neve sporca. Una vecchia ci guarda dalla finestra, e Ofelia le restituisce lo sguardo finché lei non chiude le imposte."
    menu:
        "Mi porge il velo. Non si capisce se per sistemarglielo o per buttarlo."
        "Di nascosto: il velo resta, io due passi dietro":
            $ ofelia_affinity += 1
            show ofelia neutra with qdiss
            ofelia "Saggio. Un po' vigliacco, ma saggio. I segreti hanno il loro fascino: durano poco, come le rose."
            "Al mercato nessuno ci nota. Tra due banchi di spezie mi mette in mano una rosa nera, senza guardarmi."
        "Alla luce del sole: toglierle il velo e offrirle il braccio":
            $ ofelia_affinity += 2
            $ ofelia_in_pubblico = True
            if route_seconda == "aede":
                $ aede_sospetto += 1
            show ofelia imbarazzata with dissolve
            ofelia "...davanti al pescivendolo. Hai un senso dello spettacolo spaventoso."
            show ofelia compiaciuta with qdiss
            "Attraversiamo il mercato a braccetto. Le voci tacciono al nostro passaggio e riprendono più forti alle spalle."
            if route_seconda == "aede":
                "All'ultimo banco, una ragazza del Ceppo di Glauco ci riconosce e corre via. Stasera Aede saprà."
            ofelia "Adesso sei un pettegolezzo, [player_name]. Cerca di essere uno di quelli buoni."
    "Al ritorno il cesto non è più vuoto: una rosa nera, un limone, un coltello da frutta che lei ha pagato il doppio senza trattare."
    ofelia "Il coltello è per te. Non per la frutta. Lo capirai."
    return


## Impegno — La serra di sera ##################################################

label impegno_ofelia:
    scene bg sala_svelo with fade
    show ofelia neutra with dissolve
    "La serra di sera, senza pretendenti. Solo lanterne basse, e la rosa nera potata fino all'osso."
    ofelia "Ho mandato via la fila. Tutta. Il cavallo compreso."
    "Sui tavoli restano i doni della stagione: sonetti arrotolati, un pugnale col manico d'avorio, un ritratto di lei che non le somiglia. Nessuno è stato aperto."
    ofelia "Mio padre li conta, sai? Ogni dono è un'alleanza mancata. Stanotte gli ho fatto perdere sei alleanze in un colpo."
    ofelia "Non lo faccio per nessuno, quindi ascolta bene: è una domanda sola, e non la ripeto."
    show ofelia compiaciuta with qdiss
    ofelia "Sei un interesse passeggero, [player_name]? Oppure resti anche quando smetto di essere gentile?"
    menu:
        "Mi porge le forbici. Il manico verso di me, la lama verso di lei."
        "Prendere le forbici: «Resto. Anche senza gentilezza.»" (peso=True):
            $ impegno_esito = True
            show ofelia imbarazzata with dissolve
            ofelia "...hai preso il manico. Gli altri afferravano sempre la lama, per farsi vedere coraggiosi."
            show ofelia neutra with qdiss
            ofelia "Bene. Da stasera la fila è chiusa. Se qualcuno chiede, sei tu il motivo. Fallo valere."
            "Non mi bacia. Mi aggiusta il colletto, lenta, come si sistema un'arma prima di appenderla. E il semestre, da stasera, ha un padrone."
        "Lasciarle le forbici: «Non ancora, Ofelia.»" (peso=True):
            $ impegno_esito = False
            $ congelate.add("ofelia")
            show ofelia rabbia with qdiss
            ofelia "Non ancora. Lo dicono tutti, prima di sparire. Almeno tu l'hai detto in faccia."
            show ofelia neutra with qdiss
            ofelia "Torna in fila, allora. In fondo. Non ti chiamerò per nome."
            "Riprende a potare. Lo stelo cade, pulito. Non alza più gli occhi."
    return


## Impegno a tre — Il contratto con Caino ######################################

label impegno_ofelia_caino:
    $ impegno_of = False
    $ impegno_altro = False
    scene bg studio_glauco with fade
    show ofelia neutra with dissolve
    "Lo studio di Glauco, a tarda sera. Ofelia siede sulla scrivania di suo padre come se fosse un trono che non le basta."
    show caino neutro at left with dissolve
    "Caino è già lì, in piedi, con un registro sotto il braccio. Non sembra sorpreso. Sembra in anticipo."
    ofelia "Vi ho convocati insieme perché odio ripetermi. Voi due mi piacete. Non mi piace scegliere."
    caino "Proposta irregolare. Tre parti, un solo oggetto contrattuale, nessun precedente a registro."
    ofelia "Nessuno è oggetto, Caino. Siamo tre firme. E io firmo per prima."
    caino "Sulla scrivania di tuo padre. Con il suo inchiostro. È quasi poetico, se si apprezza il rischio."
    ofelia "Lo apprezzo. Lo amministri tu, il rischio. Io lo indosso."
    show ofelia compiaciuta with qdiss
    ofelia "Tu, [player_name]. Dentro o fuori. Le mie condizioni sono semplici: niente segreti, niente pietà, niente gelosie da serva."
    menu:
        "Caino apre il registro a una pagina bianca. Aspetta la penna."
        "«Dentro. Scrivi tre nomi, Caino.»" (peso=True):
            $ impegno_of = True
            show ofelia imbarazzata with dissolve
            ofelia "...non hai nemmeno chiesto chi viene prima. Peccato: avevo una risposta crudele pronta."
            show ofelia neutra with qdiss
            caino "Annotato. Prima firma: Ofelia Severo. Seconda: in sospeso. Resta la mia, e quella non la mostro davanti a testimoni."
            ofelia "Allora vi lascio soli. Il tuo ragioniere ha una domanda da farti, e la fa male in pubblico."
            hide ofelia with dissolve
        "«Fuori. Non firmo per metà.»" (peso=True):
            $ congelate.add("ofelia")
            show ofelia rabbia with qdiss
            ofelia "Per metà. Che modo meschino di contare. Pensavo che almeno la matematica fosse dalla tua."
            caino "Annullato prima della firma. Il più pulito dei contratti."
            "Ofelia scende dalla scrivania e se ne va senza voltarsi. La porta dello studio si chiude piano: con lei, è peggio di uno sbattere."
            hide ofelia with dissolve
            caino "Resta. Il contratto a tre è annullato. Il mio, no: quello non l'ho ancora proposto."
    # Il partner risponde sempre, qualunque sia stato l'esito con Ofelia.
    call impegno_caino
    $ impegno_altro = impegno_esito
    if impegno_of and impegno_altro:
        "Contraente solo, ha detto. Poi ha corretto a margine, con la penna buona: due. Ofelia, dal corridoio, ha riso come una lama che si sfodera."
    $ impegno_esito = impegno_of and impegno_altro
    return


## Impegno a tre — Il segreto della sorella ####################################

label impegno_ofelia_aede:
    $ impegno_of = False
    $ impegno_altro = False
    scene bg sala_svelo with fade
    show ofelia neutra with dissolve
    "La serra, a notte fatta. Ofelia ha spento tutte le lanterne tranne una, quella che illumina solo le sue mani."
    ofelia "Lo so, di mia sorella. Lo sa mezza Zefiro: Aede non è mai stata brava a nascondere chi le piace."
    ofelia "E so di te. Quello lo sai solo tu, e adesso io."
    ofelia "Da bambine dividevamo la stanza, le lezioni di spada, i vestiti. Lei prendeva sempre il rosso. Io lasciavo fare, e mi tenevo il nero."
    show ofelia compiaciuta with qdiss
    ofelia "Non ti chiedo di scegliere. La sorella e te: mi va bene. Ho sempre diviso tutto con lei, tranne i segreti."
    show ofelia rabbia with qdiss
    ofelia "Aede non divide. Io sì. Non farglielo sapere."
    menu:
        "La lanterna trema appena. La sua voce no."
        "«Non lo saprà. Da me, mai.»" (peso=True):
            $ impegno_of = True
            show ofelia imbarazzata with dissolve
            ofelia "...mai è una parola che mi piace sentire da chi mente bene. Ricordatelo, quando la guardi negli occhi."
            show ofelia neutra with qdiss
            ofelia "Ora va'. Ti aspetta sul ballatoio, credo. Lei fa le domande ad alta voce. Io le faccio al buio."
            "Spegne l'ultima lanterna. Esco dalla serra con un segreto in tasca e la sensazione di averlo rubato a qualcuno."
        "«Non mentirò ad Aede. Né per te, né per nessuno.»" (peso=True):
            $ congelate.add("ofelia")
            show ofelia rabbia with qdiss
            ofelia "Leale. Che virtù noiosa. Va' da lei, allora, e dille pure tutto: tanto non ti crederà."
            "Spegne l'ultima lanterna senza aspettare che io sia uscit[fin]. Al buio, la serra profuma di qualcosa che marcisce piano."
            "Va' da lei, ha detto. Non le ho dato la soddisfazione di discutere: ci vado davvero."
    # Il partner risponde sempre, qualunque sia stato l'esito con Ofelia.
    call impegno_aede
    $ impegno_altro = impegno_esito
    if impegno_of and impegno_altro:
        "«Io non divido», ha detto. Annuisco ancora, nel buio del mio Ceppo. Da qualche parte, in una serra, qualcuno sorride."
    $ impegno_esito = impegno_of and impegno_altro
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


## Interludio Luna VI — La serra d'inverno (VI/5, nessun punto) ##############

label interludio_ofelia_luna6:
    scene bg sala_svelo with fade
    "Il quinto giorno della Luna VI la serra è chiusa a tutti. Glauco ha spento i tubi caldi: per punizione, dicono i servi. Non dicono di chi."
    show ofelia neutra with dissolve
    "Ofelia è dentro lo stesso, col mantello addosso e il fiato che fuma. Le rose nere si arrendono al freddo, una per una."
    ofelia "Me l'ha fatto sapere a cena. Senza dirlo. Mio padre non dice: spegne le stufe."
    ofelia "Sa di te. Lo sa da Lune. Aspettava di vedere se eri un capriccio. Adesso ha smesso di aspettare."
    if route_seconda_viva() == "caino":
        "Sul tavolo degli attrezzi c'è un foglio di registro, piegato a triangolo. La calligrafia minuta di Caino."
        ofelia "Il tuo ragioniere ha mandato i conti. Secondo lui Glauco ci convoca entro sedici giorni. Ha messo anche le probabilità."
        ofelia "Non le ho lette. Detesto quando ha ragione prima del tempo."
    elif route_seconda_viva() == "aede":
        "Dalla porta socchiusa arriva un rumore di passi sul ghiaino. Ofelia non si volta, ma smette di respirare finché non si allontanano."
        ofelia "Aede. Viene a controllare la serra ogni sera, da quando nostro padre è di cattivo umore. Dice che è per i ladri."
        ofelia "Non ha mai preso un ladro. Ma ha sempre preso me."
    else:
        "Non c'è nessun altro. Nemmeno i servi. Solo lei, il freddo, e io che ho ignorato il cartello alla porta."
    show ofelia compiaciuta with qdiss
    ofelia "Ho una domanda per te, e non è quella della serra di sera. Quella l'hai già superata. Questa è più piccola, e più cattiva."
    ofelia "Quando lui ti chiamerà nello studio, cosa farai con le mani?"
    menu:
        "Fuori, la neve comincia a cadere sul vetro. Il silenzio fa più rumore delle rose."
        "«Le terrò ferme. Sul tavolo, dove possa vederle.»":
            show ofelia neutra with qdiss
            ofelia "Bene. Mio padre legge le mani prima delle facce. Se tremano, ti ha già battut[fin]."
            "Mi prende un polso e lo tiene, a lungo, come un medico. Poi lo lascia andare, soddisfatta."
        "«Le terrò in tasca. Così non sa cosa stringo.»":
            show ofelia compiaciuta with qdiss
            ofelia "...questo è un trucco mio. Me l'hai rubato, o ci sei arrivat[fin] da sol[fin]? Non rispondere."
            "Si infila le mani nelle tasche del mantello, e per un attimo siamo due congiurati in una serra morta."
        "«Prenderò la tua, se me la lasci.»":
            show ofelia imbarazzata with dissolve
            ofelia "...nello studio di mio padre. Davanti a lui. Sei pazz[fin], o mi conosci troppo poco."
            show ofelia neutra with qdiss
            ofelia "Te la lascerò. Forse. Dipende da quanto mi annoi fino ad allora."
    "Ofelia raccoglie una rosa morta dal vaso più vicino. È nera, rigida di gelo, perfetta."
    ofelia "Le rose di mio padre muoiono quando lui decide. Questa no. Questa l'ho tagliata io, prima."
    "Me la mette in mano. I petali si spezzano al primo tocco, come vetro sottile."
    ofelia "Sedici giorni. Non venire a cercarmi prima. Voglio che mi manchi qualcosa, quando entro in quello studio."
    hide ofelia with dissolve
    "Esco nella neve. Il fiore blu vicino alla porta, quello che non fiorisce mai, ha un bocciolo. Piccolo. Chiuso come un pugno."
    return
