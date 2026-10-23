# Route Aede — "Aede ti trascina": imprese fuori dal cortile, la ricerca dopo
# il vicolo, le sfide nel pianificatore. Tutto sapore: nessun lucchetto nuovo.
#
# 1. Imprese (pool di spada e spada_p, intercalate agli allenamenti):
#    att_spada_1, duello, TETTI, att_spada_2, MERCATO, att_spada_3, CALA,
#    att_spada_4, FIUME. Una tantum, al massimo +1 (due +1 in tutto: tetti,
#    calà). Con Aede congelata l'impresa si consuma in una riga a 0 punti.
# 2. Cerca Aede (Luna IV, dopo aede_cap4, fino alla scelta del cuore): tre
#    luoghi in tre slot diversi; quello giusto dipende dalla risposta nel
#    vicolo (aede_cerca_giusto). Sbagliato: un indizio. Giusto: una scelta
#    che diventa un fatto; il marcatore "aede_trovata" in eventi_visti spegne
#    gli altri inviti. 0 punti, char None: non tocca il cuore (aede_cap4 e'
#    gia' in rl.CUORE_REQUISITI) e vale anche a route congelata.
# 3. Sfide (Lune I-IV): inviti "scade" con char None (ritratto di Aede), cosi'
#    ofelia_scadenza (solo id "ofelia_") non le conta e non scatta il dono.
#    Lasciata cadere: l'hook aede_sfide_scadute segna "<id>_persa" in
#    eventi_visti, l'invito non torna e nasce un fatto con avviso. 0 punti.

define ascadeo = Character("Ascadeo", color="#a0522d")

init python:
    # Il posto giusto per cercarla, dalla risposta nel vicolo (cap4):
    # assassinio -> Marcassa; "non ho visto niente" -> cortile;
    # "chi era per te" -> Calà.
    def aede_cerca_giusto():
        if not store.flag_accetta_lavoro:
            return "marcassa"
        if csl.scelto(store.scelte_partita, "aede_cap4", "«Chi era"):
            return "cala"
        return "cortile"

    # Sfide lasciate cadere: l'invito non torna, il fatto ricorda.
    def aede_sfide_scadute(ids):
        for eid in ids:
            if eid.startswith("aede_sfida_"):
                store.eventi_visti.add(eid + "_persa")

    cal_inviti_ignorati_hooks.append(aede_sfide_scadute)

    EVENTI.extend([
        # --- Sfide (scadono: "Solo adesso") ---------------------------------
        {"id": "aede_sfida_1", "label": "aede_sfida_1", "tipo": "invito",
         "char": None, "ritratto": "aede", "scade": True,
         "titolo": "«Stanotte, sul tetto della Consorteria. Se non vieni, hai paura.»",
         "luna_min": 1, "slot": "sera",
         "cond": lambda v: "svelo" in v["visti"] and v["luna"] <= 2
         and v["aede_affinity"] >= 1
         and "aede" not in v["congelate"]
         and "aede_sfida_1_persa" not in v["visti"]},
        {"id": "aede_sfida_2", "label": "aede_sfida_2", "tipo": "invito",
         "char": None, "ritratto": "aede", "scade": True,
         "titolo": "«Il recinto dell'Athlion, oggi. Porta le gambe, se le hai.»",
         "luna_min": 2, "slot": "pomeriggio",
         "cond": lambda v: ("aede_sfida_1" in v["visti"]
                            or "aede_sfida_1_persa" in v["visti"])
         and "athlion" not in v["visti"]
         and "aede" not in v["congelate"]
         and "aede_sfida_2_persa" not in v["visti"]},
        {"id": "aede_sfida_3", "label": "aede_sfida_3", "tipo": "invito",
         "char": None, "ritratto": "aede", "scade": True,
         "titolo": "«A mezzanotte, sulle mura. Se non vieni, lo racconto a Druso.»",
         "luna_min": 3, "slot": "sera",
         "cond": lambda v: ("aede_sfida_2" in v["visti"]
                            or "aede_sfida_2_persa" in v["visti"])
         and "aede" not in v["congelate"]
         and "aede_sfida_3_persa" not in v["visti"]
         and "scelta_cuore" not in v["visti"]},
        # --- Cerca Aede (dopo il vicolo) ------------------------------------
        {"id": "aede_cerca_cortile", "label": "aede_cerca_cortile",
         "tipo": "invito", "char": None, "ritratto": "aede",
         "titolo": "Aede ti evita dal vicolo. Cercala al cortile, prima dell'alba",
         "luna_min": 4, "slot": "mattina",
         "cond": lambda v: "aede_cap4" in v["visti"]
         and "aede_trovata" not in v["visti"]
         and "scelta_cuore" not in v["visti"]},
        {"id": "aede_cerca_marcassa", "label": "aede_cerca_marcassa",
         "tipo": "invito", "char": None, "ritratto": "aede",
         "titolo": "Aede ti evita dal vicolo. Cercala nella Contrada Marcassa",
         "luna_min": 4, "slot": "pomeriggio",
         "cond": lambda v: "aede_cap4" in v["visti"]
         and "aede_trovata" not in v["visti"]
         and "scelta_cuore" not in v["visti"]},
        {"id": "aede_cerca_cala", "label": "aede_cerca_cala",
         "tipo": "invito", "char": None, "ritratto": "aede",
         "titolo": "Aede ti evita dal vicolo. Cercala sulla Calà, a lanterne accese",
         "luna_min": 4, "slot": "sera",
         "cond": lambda v: "aede_cap4" in v["visti"]
         and "aede_trovata" not in v["visti"]
         and "scelta_cuore" not in v["visti"]},
    ])

    FATTI.extend([
        # --- Sfide lasciate cadere ------------------------------------------
        {"id": "aede_sfida_tetto_persa", "char": "aede",
         "testo": "Aede ti ha sfidat[fin] sul tetto della Consorteria. Non ci sei andat[fin].",
         "avviso": "Aede se ne ricorderà.",
         "cond": lambda v: "aede_sfida_1_persa" in v["visti"]},
        {"id": "aede_sfida_recinto_persa", "char": "aede",
         "testo": "Aede ti ha aspettat[fin] al recinto dell'Athlion. Ha saltato da sola.",
         "avviso": "Aede se ne ricorderà.",
         "cond": lambda v: "aede_sfida_2_persa" in v["visti"]},
        {"id": "aede_sfida_mura_persa", "char": "aede",
         "testo": "Aede ha camminato sulle mura a mezzanotte. Senza di te.",
         "avviso": "Aede se ne ricorderà.",
         "cond": lambda v: "aede_sfida_3_persa" in v["visti"]},
        # --- Imprese --------------------------------------------------------
        {"id": "aede_mela", "char": "aede",
         "testo": "Al mercato coperto hai rubato una mela sotto il naso del mercante. Per Aede.",
         "avviso": None,
         "cond": lambda v: _scelto(v, "att_spada_mercato", "Prendi la mela")},
        {"id": "aede_fiume", "char": "aede",
         "testo": "Ti sei tuffat[fin] nel fiume gelato per una scommessa di Ascadeo. Aede ha vinto.",
         "avviso": "Ascadeo se ne ricorderà.",
         "cond": lambda v: _scelto(v, "att_spada_fiume", "Tuffati")},
        # --- Cerca Aede: il posto giusto ------------------------------------
        {"id": "aede_cerca_moneta", "char": "aede",
         "testo": "Nella Marcassa hai visto Aede lasciare monete alla casa del cambiavalute. Hai aggiunto le tue.",
         "avviso": "Aede se ne ricorderà.",
         "cond": lambda v: _scelto(v, "aede_cerca_marcassa", "Aggiungi le tue monete")},
        {"id": "aede_cerca_vista", "char": "aede",
         "testo": "Nella Marcassa hai detto ad Aede che l'avevi vista. Lei non ha negato.",
         "avviso": "Aede se ne ricorderà.",
         "cond": lambda v: _scelto(v, "aede_cerca_marcassa", "«Ti ho vista")},
        {"id": "aede_cerca_segreto", "char": "aede",
         "testo": "Nella Marcassa hai visto Aede e te ne sei andat[fin] senza farti vedere.",
         "avviso": "Aede se ne ricorderà.",
         "cond": lambda v: _scelto(v, "aede_cerca_marcassa", "Vattene prima")},
        {"id": "aede_cerca_ripresa", "char": "aede",
         "testo": "Al cortile, prima dell'alba, hai preso una spada e hai tirato di scherma con Aede finché non ha smesso di tremare.",
         "avviso": "Aede se ne ricorderà.",
         "cond": lambda v: _scelto(v, "aede_cerca_cortile", "Prendi una spada")},
        {"id": "aede_cerca_bende", "char": "aede",
         "testo": "Al cortile hai fasciato le nocche di Aede. Te l'ha lasciato fare.",
         "avviso": "Aede se ne ricorderà.",
         "cond": lambda v: _scelto(v, "aede_cerca_cortile", "Fermale le mani")},
        {"id": "aede_cerca_domanda", "char": "aede",
         "testo": "Al cortile hai chiesto ad Aede quanto le è costato il vicolo. Non ti ha risposto.",
         "avviso": "Aede se ne ricorderà.",
         "cond": lambda v: _scelto(v, "aede_cerca_cortile", "«Quanto ti è costato")},
        {"id": "aede_cerca_gradino", "char": "aede",
         "testo": "Sulla Calà ti sei sedut[fin] accanto ad Aede, un gradino sotto, e hai contato con lei.",
         "avviso": "Aede se ne ricorderà.",
         "cond": lambda v: _scelto(v, "aede_cerca_cala", "Siediti un gradino sotto")},
        {"id": "aede_cerca_baratto", "char": "aede",
         "testo": "Sulla Calà hai dato ad Aede un tuo segreto in cambio del suo silenzio.",
         "avviso": "Aede se ne ricorderà.",
         "cond": lambda v: _scelto(v, "aede_cerca_cala", "«Te ne do uno mio")},
        {"id": "aede_cerca_via", "char": "aede",
         "testo": "Sulla Calà hai preso Aede per il mantello e l'hai riportata a casa.",
         "avviso": "Aede se ne ricorderà.",
         "cond": lambda v: _scelto(v, "aede_cerca_cala", "«Vieni via")},
    ])

    # Il pianificatore: il territorio di Aede non e' piu' solo cortile.
    def _aede_rinomina_spada():
        for voci in ATTIVITA.values():
            for i, voce in enumerate(voci):
                if voce[0] in ("spada", "spada_p"):
                    voci[i] = (voce[0], "Con Aede: spada e guai") + tuple(voce[2:])


# Dopo i minigiochi (init 5: il duello a indice 1). Pool risultante:
# att_spada_1, att_spada_duello, tetti, att_spada_2, mercato, att_spada_3,
# cala, att_spada_4, fiume. spada e spada_p hanno liste distinte.
init 6 python:
    pool_aggiungi("spada", "att_spada_tetti", 2)
    pool_aggiungi("spada", "att_spada_mercato", 4)
    pool_aggiungi("spada", "att_spada_cala", 6)
    pool_aggiungi("spada", "att_spada_fiume")
    pool_aggiungi("spada_p", "att_spada_tetti", 2)
    pool_aggiungi("spada_p", "att_spada_mercato", 4)
    pool_aggiungi("spada_p", "att_spada_cala", 6)
    pool_aggiungi("spada_p", "att_spada_fiume")
    _aede_rinomina_spada()
    ATTIVITA_DESC["spada"] = "Il cortile d'armi all'alba. O dovunque lei decida di trascinarti."
    ATTIVITA_DESC["spada_p"] = "Il cortile d'armi. O un tetto, un mercato, un fiume: decide lei."


## Imprese — Aede ti trascina ################################################

# Aede congelata: l'impresa non c'e', il cortile si'.
label aede_imprese_gelo:
    scene bg palestra with fade
    show aede neutra with dissolve
    "Aede è al cortile. Mi corregge la guardia con due parole, come a un novellino qualunque."
    "Poi se ne va da sola, il mantello sulla spalla. Non mi dice dove. Non me lo dirà più."
    return

label att_spada_tetti:
    if "aede" in congelate:
        call aede_imprese_gelo
        return
    scene bg palestra with fade
    "Il cortile è vuoto. Sulla rastrelliera, la spada di Aede e un sasso. Sotto il sasso, un biglietto."
    "Una parola sola, scritta di traverso: «Su.»"
    scene bg vicoli_zefiro with fade
    show aede neutra with dissolve
    "La trovo sui tetti della Consorteria, distesa sulle tegole come una gatta. Mi fa segno di stare giù."
    aede "Il cambiavalute con l'anello d'oro. Quello che parla con il cappuccio grigio. Guardalo."
    aede "Nessuno muore, oggi. Oggi si guarda. Chi guarda bene, dopo, sbaglia meno."
    menu:
        "Sotto di noi una lettera passa di mano. Aede non respira nemmeno."
        "Stenditi accanto a lei e conta i passi della guardia":
            $ aede_affinity += 1
            "Mi stendo. Le tegole sono fredde. Conto: quaranta passi, una pausa, quaranta passi."
            pc "La guardia si ferma al pozzo. Ogni volta. Sei respiri."
            show aede sorpresa with qdiss
            aede "...sette. Ma il pozzo l'hai visto."
            show aede neutra with qdiss
            "Non lo dice, ma resta stesa accanto a me più del necessario. Spalla contro spalla, come due che aspettano."
        "«Se è un lavoro del tuo Ceppo, non voglio esserci.»":
            show aede irritata with qdiss
            aede "Nessuno ti ha chiesto di lavorare. Ti ho chiesto di guardare. Sono due cose diverse."
            aede "Le persone che non vogliono vedere finiscono sempre sotto i tetti. Mai sopra."
            "Resto. Ma guardo le nuvole, più che il cambiavalute. Lei se ne accorge, e non dice niente."
        "«Scendiamo e gli rubiamo la lettera.»":
            show aede sorpresa with qdiss
            aede "Tu. Vuoi scendere da un tetto. In pieno giorno. Davanti al cappuccio grigio."
            show aede sorriso with dissolve
            "Per un battito le si accende qualcosa negli occhi. Poi lo spegne a mano, come una lanterna."
            show aede irritata with qdiss
            aede "Idea pessima. Mi piace. No. La prossima volta che ti viene un'idea, tienila in tasca e mostramela dopo."
    "Il cappuccio grigio sparisce in un vicolo. Aede prende nota di qualcosa, a mente."
    aede "Torniamo. Se chiedono, eravamo al cortile. E tu hai fatto schifo."
    return

label att_spada_mercato:
    if "aede" in congelate:
        call aede_imprese_gelo
        return
    scene bg vicoli_zefiro with fade
    show aede irritata with dissolve
    "Aede mi trascina al mercato coperto «per una cote, cinque minuti». Sono quaranta, e la cote è ancora sul banco."
    aede "Tre Scudi per una pietra di fiume? Il tuo Glostok la pesca con le mani. L'ho visto fare, da bambina."
    "Il mercante suda. Aede lo spolpa una moneta alla volta, senza alzare la voce, come si toglie la pelle a una mela."
    show aede neutra with qdiss
    aede "Intanto che lui conta, tu fammi vedere le mani. Una mela dal cesto. Se ti vede, non ti conosco."
    menu:
        "Il cesto è a un braccio. Il mercante, a mezzo."
        "Prendi la mela, piano, mentre lui guarda lei":
            "Gli occhi del mercante sono sulle monete. La mia mano va e torna. La mela è nella mia manica, fredda."
            show aede sorpresa with qdiss
            aede "...lenta all'andata. Buona al ritorno."
            "Me la ruba dalla manica senza che me ne accorga. Ci dà un morso. Il mercante sta ancora contando."
        "Paga la mela, a voce alta":
            pc "E una mela. Questa. La pago."
            show aede irritata with qdiss
            aede "Hai pagato una mela. Un'impresa da poema. Druso ci scriverà sopra trenta versi."
            "Ma il mercante, rinfrancato, le cede la cote a due Scudi. Aede lo guarda, poi guarda me, e non dice grazie."
        "«Una mela è da bambini. Prendo la cote.»":
            show aede sorpresa with qdiss
            "Allungo la mano verso il banco. Il mercante lascia le monete. Aede, per la prima volta, perde il filo."
            with hpunch
            "Corriamo. Lei ride: un suono corto, sorpreso, che chiude subito come una porta."
            show aede irritata with qdiss
            aede "Idiota. Adesso torno a pagarla. Ma ricordati che l'ho vista, la tua faccia, mentre la prendevi."
    show aede neutra with qdiss
    aede "Rubavo per mangiare, a sei anni. Le mele erano la parte facile. Il difficile era non farsi ringraziare."
    "Lo dice guardando la cote, non me. Poi cambia discorso, e non ci si torna più."
    return

label att_spada_cala:
    if "aede" in congelate:
        call aede_imprese_gelo
        return
    scene bg cala_notte with fade
    show aede neutra with dissolve
    "La Calà. Le lanterne ancora accese, o già accese: su questa scala non si capisce mai che ora è."
    aede "Trecento gradini. Chi arriva secondo porta le spade di tutti e due per una Luna intera."
    aede "Al mio tre. Uno."
    "Non arriva al due. È già partita."
    menu:
        "Il suo mantello rosso sale a balzi, due gradini alla volta."
        "Corrile dietro e prova a batterla":
            "Ai cento la vedo. Ai duecento la sento ansimare. Agli ultimi venti le gambe non sono più mie."
            "Arrivo dieci gradini dopo di lei. Lei è piegata sulle ginocchia, e fa finta di non esserlo."
            show aede sorriso with dissolve
            aede "Le mie spade sono le due a sinistra. Oliale, già che ci sei."
        "Sali camminando. Su una scala di pietra non si corre":
            "Salgo con calma. Arrivo che lei è seduta sull'ultimo gradino da un pezzo, e conta le lanterne."
            show aede irritata with qdiss
            aede "Lent[fin], ma intero. Che è la scusa di tutti quelli che non vincono mai niente."
            "Mi passa lo stesso la borraccia. Ce l'aveva pronta."
        "«Rilancio: chi vince fa una domanda, e l'altro risponde il vero.»":
            $ aede_affinity += 1
            show aede sorpresa with qdiss
            "Si ferma al decimo gradino. Si gira. Per la prima volta un'impresa ha un prezzo che non ha scelto lei."
            show aede irritata with qdiss
            aede "Va bene. Ma vinco io."
            "Vince lei, di un gradino. Resta sull'ultimo, il fiato corto, e la domanda le resta in bocca per un tempo lunghissimo."
            show aede imbarazzata with qdiss
            aede "Perché vieni. Quando ti chiamo. Perché vieni sempre."
            pc "Perché chiami."
            "Guarda il fiume. Lo guarda così a lungo che le lanterne, sotto di noi, sembrano spegnersi una per una."
    return

label att_spada_fiume:
    if "aede" in congelate:
        call aede_imprese_gelo
        return
    scene bg esterno_neve with fade
    show aede neutra with dissolve
    "Il fiume ai piedi della Calà, gelato da riva a riva. Qualcuno ha aperto un buco nel ghiaccio, nero come un pozzo."
    ascadeo "Tre Scudi che [il_t] novellin[fin] non si tuffa. Quattro che piange."
    "Ascadeo, il fratello. Lo sento prima di vederlo: un libretto in mano, una matita dietro l'orecchio."
    aede "Io ho scommesso che ti tuffi. Non farmi perdere con lui. Mai, con lui."
    menu:
        "Il buco nel ghiaccio respira vapore."
        "Tuffati, prima di pensarci":
            with vpunch
            "Il freddo non è freddo: è un pugno in tutto il corpo, nello stesso istante."
            "Una mano mi prende per il bavero e mi tira fuori. Il mantello rosso di Aede mi cade addosso."
            show aede sorriso with dissolve
            aede "Tre Scudi, Ascadeo. E non piangeva. Segna anche quello."
            "Mi strofina le spalle con una ferocia che non ha niente di tenero. Quasi niente."
        "«Non mi tuffo per tre Scudi. Neanche per i tuoi.»":
            show aede irritata with qdiss
            aede "Allora me li paghi tu."
            "Si toglie il mantello e gli stivali, e si butta lei. Esce viola, fiera, gocciolante, e sputa acqua verso il fratello."
            aede "Con lui non perdo. Mai. Ricordatelo, la prossima volta che fai il saggio."
        "«Ci tuffiamo tutti e tre. Anche chi scommette.»":
            show aede sorpresa with qdiss
            "Ascadeo chiude il libretto. Fa un passo indietro. Aede ne fa uno avanti, verso di lui."
            with hpunch
            "Il tuffo che segue non è elegante. Il fratello urla in tre lingue. Aede ride forte, a bocca aperta, senza pensarci."
            show aede imbarazzata with qdiss
            "Poi si accorge che la guardo ridere. E smette, come chi viene sorpreso a rubare."
    return


## Cerca Aede — dopo il vicolo ###############################################

label aede_cerca_cortile:
    scene bg palestra with fade
    if aede_cerca_giusto() != "cortile":
        "Il cortile d'armi prima dell'alba. I bersagli di paglia, la rastrelliera, il pozzo. Nessun mantello rosso."
        "Il maestro d'armi spazza la sabbia e non mi guarda."
        if aede_cerca_giusto() == "marcassa":
            "«La figlia di Glauco? Viene, si allena, se ne va. Ieri ha preso il mantello grigio, quello da lavoro. Verso la Marcassa, ha detto alla guardia.»"
        else:
            "«La figlia di Glauco? Si allena con noi e poi sparisce. La sera tardi, dicono, sale e scende la Calà. Conta i gradini, come i matti.»"
        return
    "Il cortile d'armi, prima dell'alba. Il colpo arriva prima della vista: legno su paglia, sempre nello stesso punto."
    show aede rabbia with dissolve
    "Aede. Il manichino davanti a lei è ridotto a un palo. Ha le nocche aperte, e non se n'è accorta."
    aede "Va' via. Il cortile apre dopo."
    menu:
        "Un altro colpo. Lo stesso punto. Come se lì ci fosse qualcuno."
        "Prendi una spada dalla rastrelliera e mettiti in guardia":
            show aede furia with qdiss
            "Non le chiedo il permesso. Lei non me lo dà. Mi attacca e basta, forte, senza scuola."
            "Paro, cado, mi rialzo. Al decimo assalto i colpi rallentano. Al ventesimo, le tremano le braccia."
            show aede neutra with qdiss
            aede "Sei peggiorat[fin]. Domani di nuovo. Alla stessa ora."
            "Non è un ordine. È la cosa più vicina a una richiesta che le abbia mai sentito dire."
        "Fermale le mani. Le nocche sanguinano":
            show aede sorpresa with qdiss
            "Le prendo il polso. Si irrigidisce come una lama nel fodero sbagliato. Poi, non so perché, lascia fare."
            "Strappo un lembo della camicia. Fascio. Lei guarda il manichino, non me."
            show aede imbarazzata with qdiss
            aede "Se lo racconti a qualcuno, ti rompo le tue. Di nocche."
        "«Quanto ti è costato, il vicolo?»":
            show aede irritata with qdiss
            aede "Niente. Era un lavoro. Quante volte devo dirtelo."
            "Torna al manichino. Un colpo, due. Al terzo il legno si spacca, e lei resta ferma con il moncone in mano."
            show aede triste with qdiss
            "Non risponde. Ma non mi caccia. Restiamo così finché la luce non arriva al pozzo."
    $ eventi_visti.add("aede_trovata")
    return

label aede_cerca_marcassa:
    scene bg vicoli_zefiro with fade
    if aede_cerca_giusto() != "marcassa":
        "La Contrada Marcassa di giorno è un'altra città: casse, facchini, il vicolo pulito come se niente fosse."
        "Nessuna traccia di lei. Un facchino mi squadra, poi sputa per terra."
        if aede_cerca_giusto() == "cortile":
            "«La rossa? Qui non si vede. Ma all'alba, dal muro del cortile d'armi, si sentono i colpi. Sempre gli stessi. Da tre giorni.»"
        else:
            "«La rossa? Qui no. L'ho vista sulla Calà, l'altra sera. Seduta a metà scala, come una che aspetta il traghetto.»"
        return
    "La Contrada Marcassa, nel pomeriggio. Il banco del cambiavalute è sbarrato, con un drappo nero sulla porta."
    show aede neutra with dissolve
    "Mantello grigio, cappuccio basso. Aede si china sulla soglia, fa scivolare qualcosa sotto la porta. Monete: lo sento dal suono."
    "Dietro la porta, la voce di un bambino. Aede si ferma con la mano ancora a terra."
    menu:
        "Non mi ha visto. Non ancora."
        "Aggiungi le tue monete, accanto alle sue":
            "Mi chino accanto a lei. Due Scudi, sotto la porta. Lei mi guarda la mano come si guarda una lama altrui."
            show aede irritata with qdiss
            aede "Non sono soldi per loro. Sono soldi per me. Non capisci niente."
            "Ma non ritira i miei. E quando si rialza, il cappuccio le copre la faccia fino al mento."
        "«Ti ho vista.»":
            show aede sorpresa with qdiss
            "Si gira di scatto. La mano va al fianco, dove la lama non c'è."
            show aede rabbia with qdiss
            aede "Hai visto una che lascia l'elemosina. Il Nord è pieno di vedove. Vai a dirlo in giro, se ti diverte."
            "Non lo nega. Se ne va senza correre. Ed è peggio che se avesse corso."
        "Vattene prima che ti veda":
            "Indietreggio fino all'angolo. Lei resta inginocchiata sulla soglia un po' troppo a lungo."
            "Non saprà mai che c'ero. Io invece non lo dimenticherò: la figlia di Glauco che paga, di nascosto, un debito che nessuno le chiede."
    $ eventi_visti.add("aede_trovata")
    return

label aede_cerca_cala:
    scene bg cala_notte with fade
    if aede_cerca_giusto() != "cala":
        "La Calà a lanterne accese. Coppie, mercanti, un vecchio con il cane. Trecento gradini, e lei su nessuno."
        if aede_cerca_giusto() == "cortile":
            "Sull'ultimo gradino qualcuno ha segnato riprese col gesso: tacche a gruppi di dieci, come al cortile. Lei conta così."
        else:
            "Una lanternaia mi ferma: «Cerchi la rossa? È scesa di qui ieri, col mantello grigio. Verso i magazzini della Marcassa.»"
        return
    "La Calà a lanterne accese. A metà scala, seduta sul gradino centoquarantadue, il mantello rosso stretto sulle ginocchia."
    show aede triste with dissolve
    aede "Centoquarantadue. Il primo era qui. Avevo quattordici anni, e lui saliva."
    show aede irritata with qdiss
    aede "Te l'ho detto nel vicolo: il primo costa tutto. Ogni tanto vengo a vedere se ho finito di pagarlo."
    menu:
        "Sotto di noi il fiume. Sopra, Zefiro che non sa niente."
        "Siediti un gradino sotto, e conta con lei":
            "Mi siedo al centoquarantuno. Non parlo. Lei conta le lanterne a mezza voce, io conto dopo di lei."
            show aede neutra with qdiss
            "A cento lanterne la sua voce smette di tremare. A centocinquanta mi appoggia la schiena contro la spalla. Per sbaglio, giura."
        "«Te ne do uno mio, di segreto. Così siamo pari.»":
            show aede sorpresa with qdiss
            "Glielo dico. Uno vero, di quelli che non ho detto a Briseide. Lei ascolta senza interrompere."
            show aede imbarazzata with qdiss
            aede "...è un segreto pessimo. Ma è tuo. Lo tengo."
            "Ce lo scambiamo come si scambiano gli ostaggi, al Nord: con cura, e senza guardarsi negli occhi."
        "«Vieni via. Non è un posto per restare.»":
            show aede irritata with qdiss
            aede "Non sei mio padre. Non sei Ofelia. Non sei nessuno, per dirmi dove stare."
            "Le prendo un lembo del mantello. Tiro, piano. Lei si alza come se fosse stata un'idea sua."
            show aede neutra with qdiss
            "Saliamo. Al trecentesimo gradino si gira a guardare la scala, una volta sola. Poi non più."
    $ eventi_visti.add("aede_trovata")
    return


## Sfide — biglietti di Aede #################################################

label aede_sfida_1:
    scene bg vicoli_zefiro with fade
    "Il tetto della Consorteria, a mezzanotte. Sotto di me, i banchi chiusi dei cambiavalute. Sopra, il vento."
    show aede neutra with dissolve
    "Aede cammina sul colmo come su una strada. Si ferma a metà, a braccia larghe."
    aede "Sei venut[fin]. Peccato: avevo già pronta la frase per domani mattina."
    menu:
        "Il colmo è largo quanto un piede. Il mio."
        "Cammina sul colmo fino a lei":
            "Tre passi buoni, due pessimi. Al sesto lei mi prende per il bavero e mi rimette in asse."
            aede "Hai paura?"
            pc "Sì."
            show aede sorriso with dissolve
            aede "Bene. Chi non ne ha, di solito cade. Gli altri arrivano."
        "Siediti sulle tegole e guardala":
            "Mi siedo. Lei alza un sopracciglio, poi viene a sedersi a un braccio da me."
            aede "Quella è Lumina. Quella là in fondo, la Marcassa. Di notte Zefiro dice la verità: guarda dove si accendono le luci."
        "«Sono qui. La prossima volta il tetto lo scelgo io.»":
            show aede sorpresa with qdiss
            aede "Tu. Scegliere un tetto."
            show aede irritata with qdiss
            aede "Va bene. Ma se è basso, ti butto di sotto lo stesso."
    "Restiamo lassù finché la guardia non cambia turno. Poi lei sparisce giù per una grondaia, senza salutare."
    return

label aede_sfida_2:
    scene bg arena_athlion with fade
    show aede neutra with dissolve
    "Il recinto dell'Athlion, deserto. La fossa del salto è piena di neve vecchia, la sabbia del lancio è gelata."
    if "aede_sfida_1_persa" in eventi_visti:
        show aede irritata with qdiss
        aede "Sul tetto, l'altra notte, c'era solo il vento. Gli ho spiegato io chi sei. Non gli sei piaciut[fin]."
    aede "Il salto. Con la spada al fianco, come all'Athlion vero. Chi tocca la neve offre da bere."
    menu:
        "La fossa sembra più larga di quanto dovrebbe."
        "Salta per prim[fin]":
            with vpunch
            "Atterro con un piede oltre e uno dentro. La neve mi arriva al ginocchio."
            show aede sorriso with dissolve
            aede "Mezzo boccale, allora. Il piede buono lo pago io."
        "Guardala saltare, prima":
            "Lei prende la rincorsa e vola. Atterra lontano, pulita, e si gira con l'aria di chi ha vinto un torneo."
            aede "Così. Adesso tocca a te, e niente scuse sul vento."
            "Salto. Non così. Ma lei, per una volta, non commenta."
        "«Saltiamo insieme. Chi atterra prima paga.»":
            show aede sorpresa with qdiss
            "Partiamo insieme. Atterriamo insieme, in un groviglio di gomiti e neve."
            show aede imbarazzata with qdiss
            aede "Pareggio. Non vale. Togliti da sopra il mio mantello."
    return

label aede_sfida_3:
    scene bg esterno_neve with fade
    show aede neutra with dissolve
    "Le mura di Zefiro, a mezzanotte. La guardia dorme in piedi, appoggiata alla lancia. Aede le passa davanti senza nemmeno abbassare la voce."
    if "aede_sfida_2_persa" in eventi_visti:
        show aede irritata with qdiss
        aede "Al recinto ho saltato da sola. Due volte. La seconda per farti un dispetto che non hai visto."
    aede "Di là ci sono i Collifreddi. Da quassù, col cielo pulito, si vede il fumo dei villaggi."
    "Lo dice piano. Come chi indica una casa senza dire che ci ha abitato."
    menu:
        "Il vento porta odore di legna bruciata, lontano."
        "«Da quale villaggio vieni?»":
            show aede irritata with qdiss
            aede "Da uno che non c'è più. Fine della storia."
            show aede triste with qdiss
            "Poi, dopo un po', alza il braccio e indica un punto nel buio. Non dice il nome. Ma lo indica."
        "Raccogli la neve dal parapetto e tiragliela":
            with hpunch
            "La prendo in pieno sulla nuca. Il silenzio dura un battito."
            show aede furia with qdiss
            "Poi la guerra. Due Figli del Nord che si rincorrono sulle mura, e una guardia che continua a dormire."
        "Resta in silenzio e guarda il fumo con lei":
            "Non chiedo niente. Guardiamo il fumo finché il freddo non ci entra negli stivali."
            show aede neutra with qdiss
            aede "Sei l'unic[fin] che non chiede. Non so se è un pregio. Lo sto ancora decidendo."
    return
