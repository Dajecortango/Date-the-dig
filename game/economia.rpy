# Economia del semestre: Scudi, mercato coperto, doni, eventi casuali in
# città. Regola pickle: nello store girano solo stringhe (chiavi dei doni,
# id degli eventi); i dict restano nei registry di init.

default scudi = 5
# Chiave del dono in borsa (stringa) o None: se ne porta uno alla volta.
default dono_tenuto = None
# Personaggi che hanno già ricevuto un dono con punti (uno per semestre).
default doni_dati = set()
default dono_esito = "neutro"
default dono_nome = ""
default dono_chi = ""

init python:
    # Catalogo del mercato coperto: chiave -> (nome in scena, costo).
    DONI = {
        "pietra": ("una pietra da cote di Hammergrad", 3),
        "spillone": ("uno spillone da capelli in acciaio, affilato come un ago", 4),
        "idromele": ("una fiasca d'idromele di Rurikstad", 3),
        "taccuino": ("un taccuino rilegato in cuoio, pagine bianche", 2),
        "erba": ("un sacchetto d'erba dolce della Lumina", 2),
        "vino": ("una bottiglia di vino rosso di Glostok", 4),
        "fiori": ("un mazzo di fiori d'inverno", 2),
        "dadi": ("un paio di dadi d'osso, truccati", 2),
        "ballate": ("le Ballate di Mercuzio, rilegate in oro", 3),
    }
    # Gusti dai profili: (preferito, detestato).
    DONI_GUSTI = {
        "aede": ("pietra", "fiori"),      # cura le lame; odia i sentimenti in vista
        "ofelia": ("spillone", "fiori"),  # elegante e letale; i fiori li portano tutti
        "caino": ("idromele", "vino"),    # idromele di Rurikstad, odia il Glostok
        "druso": ("taccuino", "ballate"), # poeta; Mercuzio è la concorrenza
        "icaro": ("erba", "dadi"),        # la pipa; guai a dargli del baro
    }
    # Banchi del mercato, quattro oggetti per Luna.
    MERCATO_LUNE = {
        1: ["pietra", "taccuino", "fiori", "vino"],
        2: ["idromele", "erba", "spillone", "dadi"],
        3: ["spillone", "taccuino", "ballate", "erba"],
        4: ["pietra", "idromele", "fiori", "dadi"],
        5: ["spillone", "taccuino", "vino", "erba"],
        6: ["pietra", "idromele", "ballate", "fiori"],
    }

    def dono_valuta(char, chiave):
        return rlz.dono_valuta(DONI_GUSTI, char, chiave)

    def eco_spendi(n):
        store.scudi = max(0, store.scudi - n)

    # Eventi casuali delle commissioni: uno alla volta, mai ripetuti.
    CITTA_CASI = ["caso_borseggiatore", "caso_mercante", "caso_rissa",
                  "caso_borsa", "caso_campane", "caso_lanternaio"]

    def eco_pesca_citta(da_pool):
        """Pool esaurito o 40%: un evento casuale non visto (renpy.random:
        rollback-safe). Altrimenti la variante del pool."""
        return rlz.pesca_citta(CITTA_CASI, store.eventi_visti, da_pool,
                               renpy.random)

    # Il mercato si vede solo se puoi comprare qualcosa e non hai già un dono.
    ATTIVITA["pomeriggio"].append(
        ("mercato", "Il mercato coperto", None, [],
         lambda v: v["scudi"] >= 2 and v["dono_tenuto"] is None))
    ATTIVITA_RIPETIBILI["mercato"] = "eco_mercato"
    ATTIVITA_DESC["mercato"] = "Spezie, stoffe, ferraglia. Un dono giusto apre porte."


## Dopo ogni attività: paghe, giro alla taverna, dono ########################

label eco_dopo_attivita(att_id, char):
    if att_id == "registri":
        $ scudi += 2
        "A fine giornata Ottone mi conta due Scudi nel palmo. La Proprietà paga il giusto, e lo annota."
    elif att_id == "citta":
        $ scudi += 1
        "Per le commissioni, uno Scudo dalla cassa del Ceppo. Briseide non dimentica mai chi cammina per lei."
    elif att_id == "taverna" and scudi >= 1:
        menu:
            "Il boccale è vuoto. La taverna no."
            "Offrire un giro a tutto il tavolo":
                $ eco_spendi(1)
                with hpunch
                "Uno Scudo sul bancone e la taverna mi canta il nome, storpiato in tre modi diversi."
                if "druso" not in congelate:
                    druso "Un mecenate! Finalmente qualcuno che capisce come si finanzia la poesia."
            "Tenere la borsa chiusa":
                "Pago il mio e basta. Al Becco Storto la generosità si ricorda una sera; la tirchieria, una stagione."
    if char:
        call dono_check(char)
    return


## Mercato coperto ###########################################################

label eco_mercato:
    scene bg vicoli_zefiro with fade
    "Il mercato coperto di Zefiro: spezie, stoffe, ferraglia, e mercanti di Glostok che giurano su tutto tranne che sul prezzo."
    python:
        mercato_voci = [("%s — %d Scudi" % (DONI[k][0].capitalize(), DONI[k][1]), k)
                        for k in MERCATO_LUNE.get(cal_luna, MERCATO_LUNE[1])
                        if DONI[k][1] <= scudi]
        mercato_voci.append(("Guardare e basta, e non spendere niente", None))
        mercato_scelta = renpy.display_menu(mercato_voci)
    if mercato_scelta is None:
        "Giro i banchi, tocco tutto, non compro niente. Il mercante mi saluta come si saluta la pioggia."
        return
    python:
        eco_spendi(DONI[mercato_scelta][1])
        dono_tenuto = mercato_scelta
        dono_nome = DONI[mercato_scelta][0]
    "Lo avvolgo in un panno e lo metto in borsa: [dono_nome]. Adesso serve solo l'occasione giusta."
    return


## Doni ######################################################################
# Chiamato alla fine delle scene di territorio e degli inviti del personaggio.
# Al massimo un dono con punti per personaggio (doni_dati); il neutro non conta.
# A chi e' gia' in doni_dati il dono si puo' dare lo stesso, come neutro.

label dono_check(char):
    if not rlz.dono_offribile(dono_tenuto, char, doni_dati, congelate):
        return
    $ dono_nome = DONI[dono_tenuto][0]
    $ dono_chi = CAL_NOMI[char]
    menu:
        "In borsa c'è ancora [dono_nome]. Darlo a [dono_chi]?"
        "Darglielo":
            python:
                dono_esito, dono_segna = rlz.dono_consegna(DONI_GUSTI, char,
                                                           dono_tenuto,
                                                           doni_dati)
                dono_tenuto = None
                if dono_segna:
                    doni_dati.add(char)
            call expression "dono_" + char
        "Tenerlo per un'altra occasione":
            pass
    return

label dono_aede:
    if dono_esito == "ama":
        $ aede_affinity += 1
        show aede sorpresa with qdiss
        aede "Una cote di Hammergrad. Grana fine. ...chi ti ha detto che la mia si è crepata?"
        show aede sorriso with dissolve
        "Nessuno. Ma l'ho vista affilare con una pietra spaccata in due. Lei se ne accorge, e per un istante non sa dove guardare."
    elif dono_esito == "odia":
        $ aede_affinity -= 1
        show aede irritata with qdiss
        aede "Fiori. A me. Davanti al cortile intero."
        "Li regala al primo novellino che passa. Il novellino non capirà mai cos'ha fatto per meritarli."
    else:
        show aede neutra with qdiss
        aede "Mh. Grazie. Lo metto... da qualche parte."
        "Lo dice come si archivia un rapporto. Ma non lo butta."
    return

label dono_ofelia:
    if dono_esito == "ama":
        $ ofelia_affinity += 1
        show ofelia compiaciuta with qdiss
        ofelia "Un fermaglio che uccide. Finalmente un pretendente che ha guardato me, e non il mio vestito."
        "Se lo infila nei capelli senza specchio. Al primo colpo."
    elif dono_esito == "odia":
        $ ofelia_affinity -= 1
        show ofelia rabbia with qdiss
        ofelia "Fiori d'inverno. Ne ho una serra piena, [player_name]. Me li portano tutti. Credevo che tu fossi divers[fin] da tutti."
        "Li posa sul banco dei pretendenti scartati. In cima alla pila."
    else:
        show ofelia neutra with qdiss
        ofelia "Grazioso. Lo terrò finché non mi annoia."
        "Detto da lei, è quasi un contratto."
    return

label dono_caino:
    if dono_esito == "ama":
        $ caino_fiducia += 1
        show caino tenero with dissolve
        caino "Idromele di Rurikstad. Te l'ho detto una volta sola, di sfuggita, tra due decime."
        caino "I dettagli possiedono le persone. Stasera, mi sa, ne hai posseduto uno."
    elif dono_esito == "odia":
        $ caino_fiducia -= 1
        show caino freddo with qdiss
        caino "Vino di Glostok. Interessante. Ti ho detto quanto lo detesto, e tu me lo porti come un omaggio."
        "Lo posa sullo scaffale dei registri da archiviare. Sotto la lettera «D»: debiti."
    else:
        show caino neutro with qdiss
        caino "Un pensiero. Lo annoto: «data, oggetto, valore stimato». Non offenderti, annoto tutto."
    return

label dono_druso:
    if dono_esito == "ama":
        $ druso_affinity += 1
        show druso ghigno with qdiss
        druso "Un taccuino! Pagine bianche! Ho già in mente cosa ci scrivo per primo, e no, non te lo leggo. Non da sobrio."
        "Lo apre, lo annusa, lo richiude. Lo tiene in mano il resto della sera."
    elif dono_esito == "odia":
        $ druso_affinity -= 1
        show druso irritato with qdiss
        druso "MERCUZIO?! Mi regali il nemico? Quel leccapiedi che fa rimare «cuore» con «amore» da trent'anni?"
        with hpunch
        "Il volume vola fuori dalla finestra. Rilegato in oro, atterra sul tetto di fronte."
    else:
        show druso neutro with qdiss
        druso "Un regalo. Per me. Sospetto. Lo accetto, ma sappi che non ti devo niente."
    return

label dono_icaro:
    if dono_esito == "ama":
        $ icaro_affinity += 1
        show icaro sereno with dissolve
        icaro "Erba dolce della Lumina. Quella buona, non quella che vendono ai novellini."
        "Carica la pipa, accende, e mi porge il primo tiro. Poi ci ripensa e se lo fa lui. Ma l'intenzione c'era."
    elif dono_esito == "odia":
        $ icaro_affinity -= 1
        show icaro irritato with qdiss
        icaro "Dadi truccati. Per me. Spiegami bene cosa stai insinuando, che voglio metterlo per iscritto."
        "Li fa rotolare sul tavolo: sei, sei, sei. Li intasca. «Questi li confisco. Per principio.»"
    else:
        show icaro neutro with qdiss
        icaro "Lo valuto. Valore di rivendita discreto. Grazie, suppongo."
    return


## Eventi casuali delle commissioni in città (0 affinità, ±Scudi) ############

label caso_borseggiatore:
    scene bg vicoli_zefiro with fade
    "Via Lumina, ressa di mezzogiorno. Una spallata, un «scusate», e la borsa è più leggera."
    menu:
        "Il ragazzino sta già girando l'angolo."
        "Inseguirlo":
            if scudi >= 1:
                $ eco_spendi(1)
                "Lo prendo al terzo vicolo. Mi ridà la borsa, meno uno Scudo che ha già passato a un complice. Professionisti."
            else:
                "Lo prendo al terzo vicolo. Mi ridà la borsa: vuota com'era. Mi guarda con pietà sincera, da collega."
        "Lasciarlo andare":
            if scudi >= 2:
                $ eco_spendi(2)
                "Due Scudi in meno. Nel Nord la lezione si paga sempre in anticipo."
            elif scudi == 1:
                $ eco_spendi(1)
                "L'unico Scudo che avevo. Nel Nord la lezione si paga sempre in anticipo, anche a rate."
            else:
                "Si porta via una borsa vuota. Nel Nord la lezione si paga in anticipo; io, per fortuna, non avevo niente da anticipare."
    return

label caso_mercante:
    scene bg vicoli_zefiro with fade
    "Un mercante di Glostok urla contro un cambiavalute della Consorteria: gli ha dato moneta della Lega tosata ai bordi."
    menu:
        "Conosco la moneta buona. Corrado me l'ha fatta pesare per un'ora."
        "Dimostrare la truffa con la bilancia del banco":
            $ scudi += 2
            "Il cambiavalute paga, il mercante mi infila due Scudi in mano. «Per l'occhio», dice."
        "Tirare dritto":
            "Non sono affari miei. A Zefiro, chi fa affari di tutti finisce senza affari propri."
    return

label caso_rissa:
    scene bg vicoli_zefiro with fade
    "Davanti al Becco Storto, due carrettieri si prendono a pugni per una precedenza. Un barile rotola verso di me."
    menu:
        "Il barile ha l'aria di essere pieno."
        "Fermarlo prima che si sfasci":
            with vpunch
            $ scudi += 1
            "Lo fermo con la spalla. Il proprietario mi ringrazia con uno Scudo e una bestemmia, in quest'ordine."
        "Scansarmi":
            with hpunch
            "Il barile esplode contro il muro. Birra ovunque, anche su di me."
            if scudi >= 1:
                $ eco_spendi(1)
                "Il lavandaio vuole uno Scudo per il mantello. Pago."
            else:
                "Il lavandaio vuole uno Scudo per il mantello. Non ce l'ho: il mantello puzzerà di birra fino alla prossima pioggia."
    return

label caso_borsa:
    scene bg vicoli_zefiro with fade
    "Sotto un banco della Contrada Marcassa, nel fango, una borsa di cuoio. Dentro, tre Scudi e un sigillo della Malacorte."
    menu:
        "Nessuno guarda. Per ora."
        "Tenere gli Scudi, lasciare il sigillo":
            $ scudi += 3
            "Tre Scudi in tasca, il sigillo di nuovo nel fango. Chi l'ha perso non verrà a chiedermelo. Spero."
        "Consegnare tutto alla guardia della Contrada":
            $ scudi += 1
            "La guardia intasca la borsa e mi lancia uno Scudo «di ringraziamento». Il resto, immagino, lo ringrazia lui."
    return

label caso_campane:
    scene bg vicoli_zefiro with fade
    "Un banco di tre campane all'angolo della Consorteria. «Trova la biglia, raddoppia lo Scudo!» La biglia, ovviamente, non è sotto nessuna."
    menu:
        "Le mani del banditore sono veloci. Non quanto quelle di Icaro."
        "Puntare uno Scudo" if scudi >= 1:
            $ eco_spendi(1)
            "Perdo. Il banditore sorride. Avevo visto la biglia sparire nella manica, ma qui la vista non basta: serve la manica."
        "Dirgli a mezza voce che ho visto la manica":
            $ scudi += 1
            "Mi infila uno Scudo in mano senza smettere di girare le campane. «Per il silenzio.» Zefiro ha un listino per tutto."
    return

label caso_lanternaio:
    scene bg vicoli_zefiro with fade
    "Il lanternaio che fa credito ai Figli di Briseide è in cima alla scala, una lanterna in mano e la scala che balla."
    menu:
        "Sotto, nessuno tiene la scala."
        "Tenergliela finché non scende":
            $ scudi += 1
            "Scende, mi guarda, mi lascia uno Scudo. «Debito saldato», dice. Non sapevo di averne uno."
        "Comprargli una lanterna nuova per il Ceppo" if scudi >= 2:
            $ eco_spendi(2)
            "Due Scudi per una lanterna di vetro di Glostok. Briseide la appenderà in cucina, e la chiamerà «la lanterna di [player_name]»."
    return
