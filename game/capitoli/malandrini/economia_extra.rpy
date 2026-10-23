# Economia, seconda infornata (pacchetto 40 consigli, punti 18-20):
# - usi degli Scudi a fine attivita' (soffiata, Ottone, orfani, scommessa);
# - il debito con Icaro (prestito in fumeria, saldo, riscossione);
# - le reazioni proprie ai doni neutri (DONI_REAZIONI).
# Logica pura in economia_logic.py (test: tests/test_economia.py).
# Le label ECO_DOPO_LABELS ricevono att_id e decidono da sole se agire.

define esattore = Character("L'esattore", color="#8a7a6a")

# Soffiate del garzone: personaggi di cui conosci il dono preferito.
default soffiate = []
default soffiata_luna = 0
default eco_ottone = False
default eco_orfani_dato = False
default scommessa_druso = None    # None | "vinta" | "persa" | "rifiutata"
default scommessa_posta = 0
# Debito con Icaro: 0 o 6 Scudi; scadenza = cal_idx limite (incluso).
default debito_icaro = 0
default debito_scadenza = 0
default debito_esito = None       # None | "saldato" | "insoluto"

init 1 python:
    from capitoli.malandrini import economia_logic as ecl

    # Riscossione prima di tutto: se il debito e' scaduto, l'esattore arriva
    # anche in fumeria, prima che Icaro possa proporre il saldo.
    ECO_DOPO_LABELS.append((None, "eco_debito_riscossione"))
    ECO_DOPO_LABELS.append(("citta", "eco_soffiata"))
    ECO_DOPO_LABELS.append(("registri", "eco_ottone"))
    ECO_DOPO_LABELS.append(("riti", "eco_orfani"))
    ECO_DOPO_LABELS.append(("scudo", "eco_scommessa"))
    ECO_DOPO_LABELS.append(("fumeria", "eco_debito_fumeria"))

    CONSEGUENZE_VARS.extend(["eco_ottone", "eco_orfani_dato", "debito_esito"])

    FATTI.extend([
        {"id": "eco_ottone_cardia", "char": "caino",
         "testo": "Davanti a un boccale, Ottone ti ha spiegato perché Cardia paga sempre il giorno prima: qualcuno alla Proprietà gli passa le date.",
         "avviso": None,
         "cond": lambda v: v["eco_ottone"]},
        {"id": "eco_orfani", "char": None,
         "testo": "Hai lasciato due Scudi nella cassa degli orfani di Briseide. Nessuno te li aveva chiesti.",
         "avviso": "Briseide se ne ricorderà.",
         "cond": lambda v: v["eco_orfani_dato"]},
        {"id": "eco_debito_saldato", "char": "icaro",
         "testo": "Hai reso a Icaro i suoi sei Scudi, puntuale. Lui ha firmato la ricevuta.",
         "avviso": "Icaro se ne ricorderà.",
         "cond": lambda v: v["debito_esito"] == "saldato"},
        {"id": "eco_debito_insoluto", "char": "icaro",
         "testo": "Non hai reso a Icaro i suoi Scudi. Il suo esattore è venuto a prenderseli, con gli interessi.",
         "avviso": "Icaro se ne ricorderà.",
         "cond": lambda v: v["debito_esito"] == "insoluto"},
    ])

    # Nuovi ricordi in borsa (borsa_vars legge debito_esito ed eco_orfani_dato).
    RICORDI.extend([
        ("ricevuta", "La ricevuta di Icaro",
         "«Saldato.» Una parola, la sua firma e un angolo strappato: il suo modo di dire che il conto è chiuso.",
         lambda v: v.get("debito_esito") == "saldato"),
        ("disegno", "Un disegno a carboncino",
         "Te l'ha dato un orfano del Ceppo, il giorno della cassa: tu, con una spada più grande di te.",
         lambda v: v.get("eco_orfani_dato")),
    ])

    def eco_data_slot(idx):
        """«Luna II, giorno 15, sera» per un indice di CAL_SEQUENZA."""
        idx = min(idx, len(CAL_SEQUENZA) - 1)
        l, g, s = CAL_SEQUENZA[idx]
        return "%s, giorno %d, %s" % (LUNE_NOMI[l], g, s)

    def eco_debiti_righe():
        """Righe della sezione «Debiti» dell'inventario: [(nome, desc)]."""
        if store.debito_icaro > 0:
            if ecl.debito_scaduto(store.debito_icaro, store.debito_scadenza,
                                  store.cal_idx):
                return [("Icaro: %d Scudi" % store.debito_icaro,
                         "Scaduto. Icaro non sollecita: manda qualcuno.")]
            return [("Icaro: %d Scudi" % store.debito_icaro,
                     "Prestito della fumeria, da rendere entro %s. Si salda in fumeria."
                     % eco_data_slot(store.debito_scadenza))]
        if store.debito_esito == "saldato":
            return [("Icaro: saldato", "Sei Scudi resi in tempo. Icaro rispetta chi paga.")]
        if store.debito_esito == "insoluto":
            return [("Icaro: riscosso a forza", "Il suo esattore ti ha svuotato la borsa. Il conto è chiuso; il ricordo no.")]
        return []

    def eco_soffiate_righe():
        return [(CAL_NOMI[c], DONI[DONI_GUSTI[c][0]][0][0].upper()
                 + DONI[DONI_GUSTI[c][0]][0][1:]
                 + (". Già consegnato un dono." if c in store.doni_dati else "."))
                for c in store.soffiate]

    # Reazioni ai doni neutri: (personaggio, dono) -> (espressione, righe).
    # Tutte le coppie tranne preferito e detestato (DONI_GUSTI).
    DONI_REAZIONI.update({
        # --- Aede -----------------------------------------------------------
        ("aede", "spillone"): ("sorpresa", [
            ("char", "Uno spillone d'acciaio. Questa è roba da mia sorella."),
            ("char", "...però punge bene. Lo tengo nella manica. Nei capelli no, scordatelo.")]),
        ("aede", "idromele"): ("neutra", [
            ("char", "Idromele. Lo bevo dopo l'allenamento, mai prima: mi rallenta il polso."),
            ("narr", "Si infila la fiasca alla cintura, come una seconda lama.")]),
        ("aede", "taccuino"): ("irritata", [
            ("char", "Un taccuino. Per scriverci cosa, i miei sentimenti?"),
            ("char", "Ci segno le stoccate che sbagli. Mi servirà tutto, il quaderno.")]),
        ("aede", "erba"): ("imbarazzata", [
            ("char", "Erba della Lumina. Ti sembro una che fuma la pipa coi figli di Lenora?"),
            ("narr", "Annusa il sacchetto. Due volte. Poi lo intasca guardando da un'altra parte.")]),
        ("aede", "vino"): ("neutra", [
            ("char", "Vino di Glostok. Mio padre ne tiene una cantina intera e non ne beve un goccio."),
            ("char", "Lo berrò io. Alla sua salute: è la cosa che gli fa più rabbia.")]),
        ("aede", "dadi"): ("sorriso", [
            ("char", "Truccati? Fammi vedere."),
            ("narr", "Li tira sul ceppo da allenamento: sei e sei. Ride, una volta sola, di gola. Poi si ricorda che ci sono anch'io, e smette.")]),
        ("aede", "ballate"): ("irritata", [
            ("char", "Mercuzio. Cavalieri che piangono in rima."),
            ("char", "Ci pareggio il piede della rastrelliera. Non prenderla male: è il posto più utile che avrà mai.")]),
        # --- Ofelia ---------------------------------------------------------
        ("ofelia", "pietra"): ("neutra", [
            ("char", "Una cote. Credi che le mie lame le affili io, o mia sorella?"),
            ("char", "Mia sorella, ovviamente. Gliela passerò. Tu non dirle da chi viene.")]),
        ("ofelia", "idromele"): ("compiaciuta", [
            ("char", "Idromele di Rurikstad. Rozzo, dolce, onesto. Tre cose che non mi si addicono."),
            ("narr", "Lo affida a un servitore. «In cantina. Dietro il Glostok, dove nessuno guarda.»")]),
        ("ofelia", "taccuino"): ("compiaciuta", [
            ("char", "Pagine bianche. Ci scriverò i nomi dei pretendenti da congedare."),
            ("char", "Il tuo lo lascio per ultimo. Non è un complimento. Non ancora.")]),
        ("ofelia", "erba"): ("neutra", [
            ("char", "Erba della Lumina. Mescolata alla terra, fa venire più scure le rose nere."),
            ("char", "Non lo sapevi. Bene: adesso lo sappiamo in due.")]),
        ("ofelia", "vino"): ("neutra", [
            ("char", "Glostok. Annata mediocre, etichetta falsa."),
            ("char", "Lo servirò ai pretendenti. Se ne accorgono in pochi: è così che li conto.")]),
        ("ofelia", "dadi"): ("compiaciuta", [
            ("char", "Dadi truccati. Che pensiero sincero."),
            ("narr", "Li rigira tra le dita guantate, poi li fa sparire nella manica. Da lì non escono più.")]),
        ("ofelia", "ballate"): ("imbarazzata", [
            ("char", "Mercuzio. Lo leggevo a dodici anni, di nascosto da Aede."),
            ("char", "Se lo racconti a qualcuno ti faccio sparire come una rima sbagliata.")]),
        # --- Caino ----------------------------------------------------------
        ("caino", "pietra"): ("neutro", [
            ("char", "Una cote di Hammergrad. Grana fine. La mia spada ringrazia; io annoto."),
            ("char", "Voce: «affilatura, omaggio». Valore stimato: una sera di favore.")]),
        ("caino", "spillone"): ("sarcastico", [
            ("char", "Uno spillone. Per i miei capelli o per la gola di qualcuno del Consiglio?"),
            ("char", "Non rispondere. Alla Rocca le risposte finiscono a verbale.")]),
        ("caino", "taccuino"): ("sorpreso", [
            ("char", "Un registro personale. Rilegato in cuoio."),
            ("char", "Sai quanti me ne hanno regalati? Nessuno. Temono tutti cosa ci scriverei.")]),
        ("caino", "erba"): ("sarcastico", [
            ("char", "Erba della Lumina. Hai sbagliato fratello, [player_name]. Quello con la pipa sta in fumeria."),
            ("char", "La tengo per lui. Un favore di Icaro vale più di qualunque erba.")]),
        ("caino", "fiori"): ("neutro", [
            ("char", "Fiori d'inverno. Gentile."),
            ("narr", "Li mette in un vaso sopra i registri delle decime. Chi viene a pagare penserà che l'Arconte ha un cuore. È il loro scopo, adesso.")]),
        ("caino", "dadi"): ("freddo", [
            ("char", "Dadi truccati. In mano all'Arconte della Proprietà."),
            ("char", "Immagina cosa direbbe Lenora. Poi immagina che li ho già chiusi in un cassetto.")]),
        ("caino", "ballate"): ("sarcastico", [
            ("char", "Mercuzio, rilegato in oro. Druso darebbe fuoco a questa stanza."),
            ("char", "Lo metto sullo scaffale più in vista. Per quando viene a chiedermi Scudi.")]),
        # --- Druso ----------------------------------------------------------
        ("druso", "pietra"): ("neutro", [
            ("char", "Una pietra. Mi regali una PIETRA."),
            ("char", "Componimento: «Mi diede una cote, e la mia lama arrossì.» ...funziona meglio di quanto vorrei.")]),
        ("druso", "spillone"): ("ghigno", [
            ("char", "Uno spillone! Per me? Per i miei boccoli?"),
            ("char", "Lo regalo a Ofelia e dico che l'ho scelto io. Grazie, novellin[fin]: mi hai appena scritto una serenata.")]),
        ("druso", "idromele"): ("ghigno", [
            ("char", "Idromele di Rurikstad! Il preferito di mio fratello."),
            ("narr", "Stappa e ne beve mezza fiasca a canna. «Così Caino non la trova piena. Educazione fraterna.»")]),
        ("druso", "erba"): ("sorpreso", [
            ("char", "Erba dolce? Hai sbagliato fratello. Ma chi sono io per rifiutare."),
            ("char", "La fumo davanti a Icaro. Piano. Molto piano.")]),
        ("druso", "vino"): ("neutro", [
            ("char", "Vino di Glostok. Bevibile. Lo bevo."),
            ("narr", "Lo stappa col pugnale. Il tappo finisce nel boccale di un passante, e Druso dedica un verso anche a lui.")]),
        ("druso", "fiori"): ("imbarazzato", [
            ("char", "Fiori. A me. In taverna. Davanti a tutti."),
            ("char", "...Silenzio, plebe! È un omaggio al poeta! Gli artisti ricevono fiori!")]),
        ("druso", "dadi"): ("ghigno", [
            ("char", "Dadi truccati! Finalmente qualcuno che mi capisce."),
            ("char", "Stasera mi riprendo tutto quello che ho perso con Icaro. Se non se ne accorge. Se ne accorge sempre.")]),
        # --- Icaro ----------------------------------------------------------
        ("icaro", "pietra"): ("neutro", [
            ("char", "Una cote. Io non affilo niente: le lame le lascio a chi ha fretta."),
            ("char", "Ma una cote di Hammergrad si rivende bene. La tengo.")]),
        ("icaro", "spillone"): ("furbo", [
            ("char", "Acciaio buono. Apre una serratura meglio di una chiave, se sai come."),
            ("narr", "Lo infila nel risvolto della giacca senza guardare. Io non lo vedrò più. Qualche serratura, temo, sì.")]),
        ("icaro", "idromele"): ("sereno", [
            ("char", "Idromele. Va d'accordo con la pipa, male con le carte."),
            ("char", "Lo berrò una sera senza carte. Ce ne sono poche.")]),
        ("icaro", "taccuino"): ("sorpreso", [
            ("char", "Un taccuino. Pagine bianche."),
            ("char", "Ci terrò i conti di chi mi deve qualcosa. Così, a occhio, la prima riga è tua.")]),
        ("icaro", "vino"): ("neutro", [
            ("char", "Glostok. Annata mediocre, valore pieno: il cambiavalute della Consorteria lo compra a qualunque prezzo."),
            ("char", "Grazie. Me l'hai regalato due volte: una a me, una al mio margine.")]),
        ("icaro", "fiori"): ("imbarazzato", [
            ("char", "Fiori. Non si rivendono, non si fumano, non si giocano."),
            ("narr", "Li tiene in mano come una carta che non sa dove mettere. Alla fine li posa accanto alla pipa. Non li butta.")]),
        ("icaro", "ballate"): ("irritato", [
            ("char", "Mercuzio. Il libro più inutile del Nord, rilegato nel metallo più utile."),
            ("char", "Stacco l'oro e il resto lo regalo a Druso. Così soffre.")]),
    })


## Città: la soffiata del garzone (2 Scudi) ##################################
# Una volta per Luna, finché resta qualcuno di cui non sai il gusto.

label eco_soffiata(att_id):
    if soffiata_luna == cal_luna or scudi < ecl.SOFFIATA_COSTO:
        return
    $ eco_cand = ecl.soffiata_candidati(DONI_GUSTI, doni_dati, soffiate, congelate, eventi_visti)
    if not eco_cand:
        return
    $ soffiata_luna = cal_luna
    scene bg vicoli_zefiro with dissolve
    "Un garzone del mercato coperto mi trotta dietro per due vicoli. Ha le orecchie a sventola e l'aria di chi le usa."
    "«Due Scudi e ti dico cosa vuole davvero chi ti interessa. Io porto le ceste a tutti, e tutti parlano davanti alle ceste.»"
    menu:
        "Due Scudi per un pettegolezzo. A Zefiro è il prezzo onesto."
        "«Aede. La volpe rossa.»" if "aede" in eco_cand:
            $ eco_soff_chi = "aede"
            "«Affila la spada ogni sera con una cote spaccata in due. Davanti al banco delle pietre di Hammergrad si ferma un'ora. Poi tira dritto, come se niente.»"
        "«Ofelia, la figlia di Glauco.»" if "ofelia" in eco_cand:
            $ eco_soff_chi = "ofelia"
            "«Ha chiesto al fabbro uno spillone da capelli d'acciaio. Uno che punga davvero. Il fabbro l'ha detto a me, io lo dico a te.»"
        "«Caino. L'Arconte.»" if "caino" in eco_cand:
            $ eco_soff_chi = "caino"
            "«Al Becco Storto rimanda indietro il vino di Glostok senza assaggiarlo. Beve solo idromele di Rurikstad. Sempre, da sempre.»"
        "«Druso, il poeta.»" if "druso" in eco_cand:
            $ eco_soff_chi = "druso"
            "«Scrive sui margini dei conti della taverna, e la locandiera glieli fa pagare doppi. Gli servirebbe un taccuino. I soldi, però, li beve.»"
        "«Icaro. Quello con la pipa.»" if "icaro" in eco_cand:
            $ eco_soff_chi = "icaro"
            "«Si lamenta dell'erba della Consorteria. Vuole quella dolce della Lumina, e dice che nessuno gliela porta mai buona.»"
        "Lasciarlo parlare da solo e tenere la borsa chiusa":
            "«Peccato», dice, e sparisce dietro una cesta di cavoli. A Zefiro le notizie aspettano: tornano a costare uguale."
            return
    python:
        eco_spendi(ecl.SOFFIATA_COSTO)
        soffiate.append(eco_soff_chi)
        eco_soff_dono = DONI[DONI_GUSTI[eco_soff_chi][0]][0]
    "Due Scudi nel palmo sporco. Me lo segno in borsa: [eco_soff_dono]. Il mercato coperto, prima o poi, ce l'avrà."
    return


## Registri: un boccale a Ottone (2 Scudi) ###################################
# Dopo att_registri_1 (Cardia paga il giorno prima), finché Ottone e' alla
# Proprieta' (caino_luna5 lo porta via). Una volta.

label eco_ottone(att_id):
    if eco_ottone or scudi < ecl.OTTONE_COSTO:
        return
    if "att_registri_1" not in eventi_visti or "caino_luna5" in eventi_visti:
        return
    scene bg vicoli_zefiro with dissolve
    "All'uscita della Proprietà, Ottone si stringe il mantello e guarda la taverna di fronte come un registro in passivo."
    menu:
        "Trentun anni di colonne. Un boccale non gliel'ha mai offerto nessuno, si vede."
        "Offrirgli un boccale al Becco Storto (2 Scudi)":
            $ eco_spendi(ecl.OTTONE_COSTO)
            $ eco_ottone = True
            "Al secondo sorso Ottone si toglie i guanti. Al terzo, la voce."
            pc "Il Ceppo di Cardia paga sempre il giorno prima. Me ne sono accort[fin] il primo giorno."
            ottone "Lo so. Ti ho visto fermare la penna su quella riga."
            ottone "Chi paga il giorno prima sa quando arriva il controllo. E chi lo sa, ragazz[fin], l'ha sentito dire da qualcuno di dentro."
            "Abbassa la voce sul boccale, come se il boccale avesse orecchie."
            ottone "Le date di consultazione restano scritte. Basta qualcuno che le copi, e qualcuno che le compri. Alla Proprietà c'è sempre un compratore."
            "Lo dice guardando la schiuma, non me. Poi paga il suo boccale da solo, anche se l'avevo già pagato io."
            $ conseguenze_aggiorna()
        "Salutarlo e tirare dritto":
            "Gli faccio un cenno. Lui risponde alzando due dita macchiate d'inchiostro, e se ne va da solo."
    return


## Riti: la cassa degli orfani (2 Scudi) #####################################

label eco_orfani(att_id):
    if eco_orfani_dato or scudi < ecl.ORFANI_COSTO:
        return
    scene bg corridoio_ceppo with dissolve
    "Accanto alla porta della cucina, la cassa degli orfani di Briseide: legno vecchio, una fessura consumata dai pollici di chi ci ha infilato qualcosa."
    "Briseide la svuota ogni Luna, in silenzio. Nessuno sa quanto ci trova. Nessuno lo chiede."
    menu:
        "Due Scudi sono una settimana di boccali."
        "Infilare due Scudi nella fessura":
            $ eco_spendi(ecl.ORFANI_COSTO)
            $ eco_orfani_dato = True
            "Le monete cadono sul fondo con un suono povero. Doveva esserci poco, là sotto."
            "Un bambino del Ceppo, dal fondo del corridoio, mi ha visto. Torna con un foglio piegato in quattro e me lo mette in mano senza dire niente."
            "Un disegno a carboncino: io, con una spada più grande di me. Lo piego di nuovo e lo metto in borsa, accanto agli Scudi che restano."
            $ conseguenze_aggiorna()
        "Passare oltre":
            "Passo oltre. La fessura resta lì, consumata dai pollici degli altri."
    return


## Palestra: la scommessa su Druso (1-3 Scudi) ###############################
# L'unico azzardo del gioco, dichiarato: 50% con renpy.random. Una volta.

label eco_scommessa(att_id):
    if scommessa_druso is not None or scudi < 1:
        return
    scene bg palestra with dissolve
    show druso ghigno at left with easeinleft
    "Fine allenamento. In mezzo alla sabbia Druso sfida un gigante della Contrada Marcassa, uno con le spalle di un portone."
    "Sulle panche, i Figli delle altre Case raccolgono puntate. Lotta libera, al primo che tocca terra con la schiena."
    druso "Novellin[fin]! Punta su di me. Se perdo, ti dedico un'elegia. Se vinco, due."
    menu:
        "Il gigante si scrocchia il collo. Sembra un ponte che si assesta."
        "Puntare uno Scudo su Druso":
            $ scommessa_posta = 1
        "Puntare due Scudi su Druso" if scudi >= 2:
            $ scommessa_posta = 2
        "Puntare tre Scudi su Druso" if scudi >= 3:
            $ scommessa_posta = 3
        "Non puntare niente":
            show druso irritato with qdiss
            druso "Tirchi[fin]! Taccagn[fin]! Componimento: «Non puntò su di me: la borsa restò piena, e il cuore vuoto.»"
            "Rima libera. Come il mio Scudo, che resta dov'è."
            $ scommessa_druso = "rifiutata"
            return
    python:
        eco_delta = ecl.scommessa_delta(scommessa_posta, renpy.random.random())
        if eco_delta > 0:
            scudi += eco_delta
            scommessa_druso = "vinta"
        else:
            eco_spendi(scommessa_posta)
            scommessa_druso = "persa"
    with vpunch
    if scommessa_druso == "vinta":
        "Il gigante carica. Druso si butta di lato, gli aggancia la caviglia e lo stende come un tappeto da battere."
        show druso ghigno with qdiss
        druso "TERRA! Schiena a terra! Pagate, plebei, pagate il mio pubblico!"
        "Mi tornano in mano il doppio degli Scudi. Druso mi strizza l'occhio e dice a tutti che l'idea della caviglia era mia. Non era mia."
    else:
        "Druso parte per primo, con un urlo da poema epico. Il gigante lo solleva come un sacco di farina e lo posa sulla sabbia, quasi con garbo."
        show druso imbarazzato with qdiss
        druso "Ho... ceduto con eleganza. Per non umiliarlo. È un gesto da poeta."
        show druso ghigno with qdiss
        druso "La tua elegia te la declamo stasera. Ti costerà un boccale. Considerala una seconda scommessa."
    return


## Fumeria: il prestito di Icaro, e il saldo ##################################

label eco_debito_fumeria(att_id):
    if ecl.debito_offribile(debito_icaro, debito_esito, scudi, congelate):
        scene bg vicoli_zefiro with dissolve
        show icaro neutro with dissolve
        "Mentre esco, Icaro mi guarda la borsa. Non me: la borsa."
        icaro "Floscia. Si vede da qui. Chi gioca con una borsa così perde per paura, non per sfortuna."
        icaro "Cinque Scudi. Me ne rendi sei entro una Luna e mezza. Non è generosità: è un investimento a breve."
        menu:
            "Il sesto Scudo è l'interesse. Il resto, con Icaro, non è mai scritto."
            "Accettare i cinque Scudi":
                python:
                    scudi += ecl.DEBITO_PRESTITO
                    debito_icaro = ecl.DEBITO_RESTITUZIONE
                    debito_scadenza = ecl.debito_scadenza(cal_idx)
                    eco_debito_data = eco_data_slot(debito_scadenza)
                show icaro furbo with qdiss
                icaro "Scadenza: [eco_debito_data]. Me lo ricordo io, così non devi ricordartelo tu."
                "Conta le monete due volte, una nella sua mano e una nella mia. Poi se le guarda partire come si guarda un figlio andare in guerra."
            "«No, grazie. Preferisco una borsa floscia a una borsa tua.»":
                show icaro sereno with qdiss
                icaro "Saggio. Raro. Annotato."
        return
    if ecl.debito_saldabile(debito_icaro, debito_scadenza, cal_idx, scudi):
        scene bg vicoli_zefiro with dissolve
        show icaro neutro with dissolve
        $ eco_debito_data = eco_data_slot(debito_scadenza)
        "Icaro sta riaccendendo la pipa. Ho sei Scudi in borsa, e lui lo sa prima di me."
        menu:
            "Il debito scade a [eco_debito_data]. C'è ancora tempo."
            "Saldare adesso i sei Scudi":
                python:
                    eco_spendi(debito_icaro)
                    debito_icaro = 0
                    debito_esito = "saldato"
                    icaro_affinity += 1
                show icaro sereno with dissolve
                icaro "Sei. Puntuali. Nessuno mi paga puntuale: o in anticipo, per farsi benvolere, o in ritardo, per farsi odiare."
                "Mi scrive una ricevuta su un foglio di carte da gioco. «Saldato.» Poi strappa un angolo e se lo tiene: il suo, di ricordo."
                $ conseguenze_aggiorna()
            "Rimandare il saldo dei sei Scudi":
                icaro "Come vuoi. Il tempo è tuo. Gli Scudi, per ora, no."
    return


## Riscossione: debito scaduto, alla prima fine attivita' ####################

label eco_debito_riscossione(att_id):
    if not ecl.debito_scaduto(debito_icaro, debito_scadenza, cal_idx):
        return
    scene bg vicoli_zefiro with dissolve
    "Sulla strada del ritorno, un uomo mi si affianca. Cappotto buono, mani pulite, un'educazione che non ammette repliche."
    esattore "[Il_t] [figlio_t] di Briseide. Il signor Icaro le manda i suoi saluti, e il conto. Sei Scudi, scaduti."
    if scudi >= debito_icaro:
        esattore "Vedo che li ha. Non è venut[fin] a portarli. Il signor Icaro lo considera peggio che non averli."
    else:
        esattore "Vedo che non li ha. Il signor Icaro lo aveva previsto. Lo prevede sempre."
    with hpunch
    python:
        eco_riscosso = scudi
        scudi = 0
        debito_icaro = 0
        debito_esito = "insoluto"
        icaro_affinity -= 1
    if eco_riscosso:
        "Mi prende la borsa, la svuota sul palmo, me la rende. [eco_riscosso] Scudi: debito, interessi, e il disturbo di essere venuto."
    else:
        "Mi prende la borsa, la rovescia: niente. Me la rende con una piega che vale più di uno schiaffo."
    esattore "Il conto è chiuso. La memoria del signor Icaro, invece, resta aperta."
    $ conseguenze_aggiorna()
    return
