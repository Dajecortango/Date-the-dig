# Route Ofelia — "Tanto bella quanto letale". Difficoltà 4/5.
# Lucchetto dei mancati: Ofelia non aspetta. Ogni suo invito lasciato cadere
# costa un punto; al secondo, per lei sei già un nome tra tanti (congelata).
# Poliamore possibile solo con Aede (che NON sa e NON accetta) e con Caino
# (dichiarato). Mai con Druso o Icaro.

define ofelia = Character("Ofelia", color="#7d3c98")

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
    def ofelia_scadenza(ids):
        for eid in ids:
            if not eid.startswith("ofelia_"):
                continue
            if "ofelia" in store.congelate:
                continue
            store.ofelia_mancati += 1
            store.ofelia_affinity -= 1
            if store.ofelia_mancati >= 2:
                store.congelate.add("ofelia")
                renpy.notify("Per Ofelia sei già un nome tra tanti.")
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
    ])


## Corte 1 — La fila ##########################################################

label att_corte_1:
    scene bg sala_svelo with fade
    show ofelia neutra with dissolve
    "La serra di Glauco in pieno inverno: fiori che non dovrebbero esistere e una fila di pretendenti che sembra voler somigliare a loro."
    "Ofelia li passa in rassegna come si passa un mazzo di carte scadenti. Nessuno regge il suo sguardo oltre il secondo."
    if route_seconda == "aede":
        $ aede_sospetto += 1
        "Mi accorgo troppo tardi che una servetta ci osserva dal corridoio. Domani Aede saprà che passo in serra."
    ofelia "Il quarto da sinistra mi ha dedicato un sonetto. Il terzo, un cavallo. Il cavallo era più eloquente."
    menu:
        "Mi tocca il turno: mi guarda, e aspetta."
        "«Il tuo giardino è splendido, Ofelia. Quasi quanto te.»":
            $ ofelia_affinity -= 1
            show ofelia rabbia with qdiss
            ofelia "Quasi. Che parola generosa. Prendila con te e cedi il posto al prossimo."
        "«Non ti dirò niente di bello. Hai già sentito tutto.»":
            $ ofelia_affinity += 1
            show ofelia compiaciuta with qdiss
            ofelia "...e il bello è che è vero. Resta pure in fila. In fondo, ma resta."
        "Restare in silenzio, a guardare i fiori":
            show ofelia neutra with qdiss
            ofelia "Almeno non mi hai rubato l'aria. Già qualcosa."
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
    menu:
        "Il pretendente si volta verso di me, in cerca di un alleato."
        "Dargli ragione: «Un orso, certo. Enorme.»":
            $ ofelia_affinity -= 1
            show ofelia rabbia with qdiss
            ofelia "Un altro che mi serve quello che voglio sentire. Che stanchezza."
        "«L'orso non c'era. Ma i suoi graffi sul braccio sono veri.»":
            $ ofelia_affinity += 1
            show ofelia imbarazzata with qdiss
            ofelia "...hai notato i graffi. Gli altri guardano sempre me."
            show ofelia neutra with qdiss
            ofelia "Era un gatto. Non dirglielo."
        "Svignarmela prima che mi tiri in mezzo":
            show ofelia neutra with qdiss
            ofelia "Prudente. Non è una virtù che apprezzo, ma almeno è onesta."
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
    menu:
        "Non mi guarda. Taglia, con calma, uno stelo."
        "«Vuoi che resti, o che me ne vada?»":
            $ ofelia_affinity += 1
            show ofelia compiaciuta with qdiss
            ofelia "Domanda corretta. Rimani, finché ho le forbici in mano. Dopo, vedremo."
        "«Sei la più bella di Zefiro, lo sai.»":
            $ ofelia_affinity -= 1
            show ofelia rabbia with qdiss
            ofelia "Lo so. Lo sa anche il cavallo. Esci dalla fila, per favore."
        "Aiutarla a raccogliere gli steli tagliati":
            show ofelia neutra with qdiss
            ofelia "Ti sporchi le mani per una rosa che non è tua. Strano modo di corteggiare."
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
    "Il primo colpo mi sfiora la guancia. Il secondo no. Lei è veloce, e non ha alcuna fretta di finire."
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
    return


## Impegno — La serra di sera ##################################################

label impegno_ofelia:
    scene bg sala_svelo with fade
    show ofelia neutra with dissolve
    "La serra di sera, senza pretendenti. Solo lanterne basse, e la rosa nera potata fino all'osso."
    ofelia "Ho mandato via la fila. Tutta. Il cavallo compreso."
    ofelia "Non lo faccio per nessuno, quindi ascolta bene: è una domanda sola, e non la ripeto."
    show ofelia compiaciuta with qdiss
    ofelia "Sei un interesse passeggero, [player_name]? Oppure resti anche quando smetto di essere gentile?"
    menu:
        "Mi porge le forbici. Il manico verso di me, la lama verso di lei."
        "Prendere le forbici: «Resto. Anche senza gentilezza.»":
            $ impegno_esito = True
            show ofelia imbarazzata with dissolve
            ofelia "...hai preso il manico. Gli altri afferravano sempre la lama, per farsi vedere coraggiosi."
            show ofelia neutra with qdiss
            ofelia "Bene. Da stasera la fila è chiusa. Se qualcuno chiede, sei tu il motivo. Fallo valere."
            "Non mi bacia. Mi aggiusta il colletto, lenta, come si sistema un'arma prima di appenderla. E il semestre, da stasera, ha un padrone."
        "Lasciarle le forbici: «Non ancora, Ofelia.»":
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
    show ofelia compiaciuta with qdiss
    ofelia "Tu, [player_name]. Dentro o fuori. Le mie condizioni sono semplici: niente segreti, niente pietà, niente gelosie da serva."
    menu:
        "Caino apre il registro a una pagina bianca. Aspetta la penna."
        "«Dentro. Scrivi tre nomi, Caino.»":
            $ impegno_of = True
            show ofelia imbarazzata with dissolve
            ofelia "...non hai nemmeno chiesto chi viene prima. Peccato: avevo una risposta crudele pronta."
            show ofelia neutra with qdiss
            caino "Annotato. Prima firma: Ofelia Severo. Seconda: in sospeso. Resta la mia, e quella non la mostro davanti a testimoni."
            ofelia "Allora vi lascio soli. Il tuo ragioniere ha una domanda da farti, e la fa male in pubblico."
            hide ofelia with dissolve
        "«Fuori. Non firmo per metà.»":
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
    show ofelia compiaciuta with qdiss
    ofelia "Non ti chiedo di scegliere. La sorella e te: mi va bene. Ho sempre diviso tutto con lei, tranne i segreti."
    show ofelia rabbia with qdiss
    ofelia "Aede non divide. Io sì. Non farglielo sapere."
    menu:
        "La lanterna trema appena. La sua voce no."
        "«Non lo saprà. Da me, mai.»":
            $ impegno_of = True
            show ofelia imbarazzata with dissolve
            ofelia "...mai è una parola che mi piace sentire da chi mente bene. Ricordatelo, quando la guardi negli occhi."
            show ofelia neutra with qdiss
            ofelia "Ora va'. Ti aspetta sul ballatoio, credo. Lei fa le domande ad alta voce. Io le faccio al buio."
            "Spegne l'ultima lanterna. Esco dalla serra con un segreto in tasca e la sensazione di averlo rubato a qualcuno."
        "«Non mentirò ad Aede. Né per te, né per nessuno.»":
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
