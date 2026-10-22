# Dialoghi origliati: due di loro parlano di te mentre non ci sei.
# Coppie tra Caino, Druso e Ofelia (mai Aede o Icaro). Lune II-IV, una volta
# per partita, zero affinita'. Condizioni in csl.origliato_ok: entrambi ti
# conoscono (primo evento della loro route visto) e almeno uno dei due non
# ti ha chiuso la porta. Ognuna lascia un fatto, ripreso da un eco.
#   Caino e Druso: per caso, in archivio (dopo i registri).
#   Caino e Ofelia: origliando, per scelta (dopo la corte).
#   Druso e Ofelia: di seconda mano, recitata da Vanna (invito).

default orig_caino_ofelia_esito = None   # "via" | "sentito" | "scoperto"

init python:
    PRIMI_ORIGLIATI = {"caino": "caino_cap1", "druso": "druso_ev1",
                       "ofelia": "ofelia_ev1"}

    def origliato_ok(a, b):
        luna = CAL_SEQUENZA[min(store.cal_idx, len(CAL_SEQUENZA) - 1)][0]
        return csl.origliato_ok(store.eventi_visti, store.congelate, luna,
                                a, b, PRIMI_ORIGLIATI)

    EVENTI.extend([
        {"id": "orig_druso_ofelia", "label": "orig_druso_ofelia",
         "tipo": "invito", "char": None, "ritratto": "vanna",
         "titolo": "Vanna ha una storia, e due voci da fare",
         "luna_min": 2, "slot": "sera",
         "cond": lambda v: csl.origliato_ok(
             v["visti"], v["congelate"], v["luna"], "druso", "ofelia",
             PRIMI_ORIGLIATI)},
    ])

    CONSEGUENZE_VARS.append("orig_caino_ofelia_esito")

    FATTI.extend([
        {"id": "fx_orig_caino_druso", "char": None,
         "testo": "Dietro gli scaffali dell'archivio hai sentito Caino e Druso parlare di te.",
         "avviso": None,
         "cond": lambda v: "orig_caino_druso" in v["visti"]},
        {"id": "fx_orig_caino_ofelia_via", "char": None,
         "testo": "Caino e Ofelia parlavano di te, in serra. Hai scelto di non sentire.",
         "avviso": None,
         "cond": lambda v: v["orig_caino_ofelia_esito"] == "via"},
        {"id": "fx_orig_caino_ofelia", "char": None,
         "testo": "Hai origliato Caino e Ofelia in serra, mentre parlavano di te.",
         "avviso": "Ofelia se ne ricorderà.",
         "cond": lambda v: v["orig_caino_ofelia_esito"] in ("sentito", "scoperto")},
        {"id": "fx_orig_druso_ofelia", "char": None,
         "testo": "Vanna ti ha recitato una conversazione tra Druso e Ofelia. Su di te. Non sai quanto abbia inventato.",
         "avviso": None,
         "cond": lambda v: "orig_druso_ofelia" in v["visti"]},
    ])

    # Chi racconta l'eco: Ottone (archivio, ti ha visto), Caino (ti ha visto
    # andar via, o ti ha scoperto), Druso (sa cosa ha detto davvero).
    ECHI.extend([
        {"id": "echi_orig_ottone", "fatto": "fx_orig_caino_druso",
         "luoghi": ("registri",), "label": "echi_orig_ottone"},
        {"id": "echi_orig_caino_via", "fatto": "fx_orig_caino_ofelia_via",
         "luoghi": ("registri",), "label": "echi_orig_caino_via",
         "cond": lambda v: "caino" not in v["congelate"]},
        {"id": "echi_orig_ofelia", "fatto": "fx_orig_caino_ofelia",
         "luoghi": ("corte",), "label": "echi_orig_ofelia",
         "cond": lambda v: "ofelia" not in v["congelate"]},
        {"id": "echi_orig_druso", "fatto": "fx_orig_druso_ofelia",
         "luoghi": ("taverna",), "label": "echi_orig_druso",
         "cond": lambda v: "druso" not in v["congelate"]},
    ])


# Dopo le voci di economia_extra (init 1): l'esattore del debito resta primo.
init 2 python:
    ECO_DOPO_LABELS.append(("registri", "orig_caino_druso"))
    ECO_DOPO_LABELS.append(("corte", "orig_caino_ofelia"))


## Caino e Druso — per caso, in archivio ######################################

label orig_caino_druso(att_id):
    if not origliato_ok("caino", "druso"):
        return
    $ eventi_visti.add("orig_caino_druso")
    scene bg studio_glauco with dissolve
    "Fine turno in archivio. Sono in fondo, dietro il terzo scaffale, a rimettere a posto un registro che pesa come un vitello."
    "La porta dell'ufficio della Proprietà si apre. Due voci. Una precisa come un timbro, l'altra troppo alta per una stanza chiusa."
    "Uscire adesso vorrebbe dire spiegare perché ero lì, zitt[fin], al buio. Resto dove sono."
    caino "Siediti. No, non lì: quello è il registro di Aulo. Ci sei seduto sopra da un minuto."
    druso "È comodo. I crimini dei potenti hanno sempre una rilegatura migliore."
    druso "Allora. Il tuo scrivano nuovo. Quell[fin] di Briseide."
    if "caino" in congelate:
        caino "Non è più il mio scrivano. Non nel senso che conta. Ha scelto le sue colonne, io le mie."
    elif caino_fiducia >= 8:
        caino "Ricorda le cose. Ogni cosa che dico, la ritrovo intera una settimana dopo. Non so se è un pregio o una minaccia."
    else:
        caino "Lavora. Sbaglia poco. Non è ancora una voce di bilancio, è una nota a margine."
    if "caino_trappola" in fatti_noti:
        caino "All'Adunanza ci è cascat[fin], nella trappola delle Candele. Ma è tornat[fin] il giorno dopo. Annoto anche questo."
    if "druso" in congelate:
        druso "Io l'ho archiviat[fin]. Bella parola, eh? L'ho presa da te. Fa meno male che dire «mi ha deluso»."
    elif druso_affinity >= 6:
        druso "Mi tiene testa. Lo sai quanto è raro? Tu non mi tieni testa, tu mi tieni il conto."
    else:
        druso "Mi annoia ancora un po'. Ma ha una faccia che promette. Le facce che promettono sono le mie preferite: costano poco."
    if "fx_druso_quaderno" in fatti_noti:
        druso "E ha trovato il mio quaderno. Non dirlo a nessuno. Soprattutto a me."
    caino "Stai attento, Druso. Le persone che ti piacciono finiscono sempre nei tuoi versi."
    druso "E quelle che piacciono a te finiscono nei tuoi registri. Dimmi tu cosa è peggio."
    "Silenzio. Una sedia che gratta. La porta si richiude."
    "Aspetto contando fino a cento. Quando esco, Ottone è al suo banco. Non alza la testa. Ma la penna, per un istante, si ferma."
    $ conseguenze_aggiorna()
    return


## Caino e Ofelia — origliando, per scelta #####################################

label orig_caino_ofelia(att_id):
    if not origliato_ok("caino", "ofelia"):
        return
    $ eventi_visti.add("orig_caino_ofelia")
    scene bg sala_svelo with dissolve
    "Esco dalla serra per il vialetto dei limoni. A metà, due voci dietro le vetrate del retro."
    "Caino, con una pergamena in mano. Ofelia, seduta sul bordo di una vasca, che fa finta di non ascoltarlo. Il mio nome passa tra loro come una moneta."
    menu:
        "Basta avvicinarsi di tre passi, dietro i limoni, per sentire tutto."
        "Avvicinarmi, piano":
            if caino_trappole >= 2 or ofelia_mancati >= 1:
                $ orig_caino_ofelia_esito = "scoperto"
            else:
                $ orig_caino_ofelia_esito = "sentito"
            ofelia "...e non mi guarda come gli altri. Gli altri guardano il vestito. Quell[fin] guarda le mani. È irritante."
            caino "È un'abitudine da scrivano. Si guardano le mani di chi firma."
            if "ofelia" in congelate:
                ofelia "Comunque l'ho cancellat[fin]. Inchiostro rosso. È passat[fin] di moda prima di arrivarci."
            else:
                ofelia "Non l'ho ancora cancellat[fin]. Non so perché. Mi capita raramente di non sapere perché."
            if "caino" in congelate:
                caino "Io sì. Ha avuto la sua occasione con me. Non la rinnovo. Non è un contratto a rinnovo automatico."
            else:
                caino "Io non l'ho deciso. Il che, per me, è già una decisione."
            if orig_caino_ofelia_esito == "scoperto":
                with vpunch
                "Un ramo di limone mi graffia il collo. Mi scappa un fiato. Due teste si girano verso la vetrata."
                show caino sarcastico at left with dissolve
                caino "La prossima volta, scrivan[fin], porta una lanterna. Così almeno ti vediamo arrivare."
                show ofelia compiaciuta with dissolve
                ofelia "Lascialo. Chi ascolta dietro i limoni sente sempre la parte peggiore. È una punizione che si dà da sol[fin]."
            else:
                "Si alzano. Passano accanto ai limoni senza vedermi. Ofelia ride di qualcosa che Caino non ha detto."
        "Andarmene. Quello che dicono di me, se lo tengano":
            $ orig_caino_ofelia_esito = "via"
            "Giro sui tacchi. Il vialetto è lungo, e le voci mi seguono per un tratto, senza parole, come una musica da un'altra stanza."
            "Dalla vetrata, credo, qualcuno mi vede andare via. Non mi volto a controllare."
    $ conseguenze_aggiorna()
    return


## Druso e Ofelia — di seconda mano, recitata da Vanna #########################

label orig_druso_ofelia:
    scene bg corridoio_ceppo with fade
    show vanna neutra with dissolve
    "Vanna mi blocca in corridoio con due tazze di brodo e l'aria di chi ha una storia troppo buona per tenerla una notte in più."
    vanna "Siediti. Ieri sera, al Becco Storto. Druso e Ofelia allo stesso tavolo. Lo so, lo so. Ma è successo."
    vanna "Faccio io le voci. Lui così."
    "Gonfia il petto, abbassa la voce di un'ottava, batte un boccale immaginario sul tavolo."
    vanna "«Ofelia! Il tuo pretendente preferito della settimana? No, aspetta: ce l'ho io, il nome. È [il_t] mi[fin]. Di Briseide.»"
    "Poi si raddrizza, alza il mento, e diventa un'altra persona. Fa quasi paura quanto le riesce."
    if "ofelia" in congelate:
        vanna "«Tuo? Tienil[fin]. Io l'ho già restituit[fin] al mittente. Senza nemmeno aprire il pacco.»"
    else:
        vanna "«Tuo? Ah, Druso. Tu tieni le persone come i boccali: finché sono piene.»"
    if "druso" in congelate:
        vanna "E lui, più piano: «Infatti l'ho posato. Vuoto. Non ho più sete.»"
    else:
        vanna "E lui, più piano: «Questo no. Questo lo tengo anche vuoto.»"
    "Vanna mi guarda da sopra la tazza. Aspetta che io dica qualcosa."
    pc "E poi?"
    vanna "E poi Ofelia ha pagato il conto. Di tutti. Druso dice che è stato il momento più umiliante della sua vita, e lo racconta a chiunque."
    vanna "Una parte è vera. Quale, non te lo dico. Una sorella deve pur avere dei segreti."
    return


## Echi ########################################################################

# Ottone ti ha visto uscire dagli scaffali (registri).
label echi_orig_ottone:
    scene bg studio_glauco with dissolve
    ottone "Il terzo scaffale. Quello dei registri di Aulo. È un buon posto per non farsi vedere."
    ottone "Io ci stavo, trent'anni fa. Si sentono cose che poi non si possono dimenticare. Ma non si possono nemmeno dire."
    "Torna alle sue colonne. Non aggiunge altro, e non serve."
    return

# Caino ti ha visto andar via dalla serra (registri).
label echi_orig_caino_via:
    scene bg studio_glauco with dissolve
    show caino neutro with dissolve
    caino "In serra, l'altro giorno. Te ne sei andat[fin] dal vialetto dei limoni. Ti ho visto dalla vetrata."
    caino "La maggior parte delle persone si sarebbe avvicinata. Annoto: sa quando non leggere un documento. Rarissimo."
    return

# Ofelia sa che hai origliato (corte).
label echi_orig_ofelia:
    scene bg sala_svelo with dissolve
    show ofelia neutra with dissolve
    if orig_caino_ofelia_esito == "scoperto":
        ofelia "I limoni del vialetto. Li ho fatti potare. Non per te: per il prossimo che ci si nasconde dietro."
    else:
        ofelia "Il giorno che Caino è venuto in serra, qualcuno ha calpestato le aiuole dei limoni. Il giardiniere giura che non è stato lui."
        "Mi guarda le scarpe. A lungo."
    return

# Druso conferma una frase della recita di Vanna e ne smentisce un'altra (taverna).
label echi_orig_druso:
    scene bg vicoli_zefiro with dissolve
    show druso ghigno at left with dissolve
    druso "Vanna ti ha fatto il numero di me e Ofelia, vero? Lo fa a tutto il Ceppo. Le viene meglio Ofelia che me, ed è un'offesa."
    if "druso" in congelate:
        druso "Il conto l'ha pagato lei, questo è vero. Il resto se l'è inventato. Io non dico mai «non ho più sete». Mai."
    else:
        druso "La frase sul boccale vuoto l'ho detta, sì. Il conto, invece, l'ho pagato io. Ofelia ha solo finto di cercare la borsa."
    return
