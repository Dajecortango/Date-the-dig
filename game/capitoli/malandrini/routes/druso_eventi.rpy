# Route Druso — eventi sul calendario e mini-scena di impegno.

init python:
    EVENTI.extend([
        {"id": "druso_ev1", "label": "druso_ev1", "tipo": "invito",
         "char": "druso", "titolo": "Druso pretende un pubblico: serata di versi",
         "luna_min": 2, "slot": "sera",
         "cond": lambda v: v["druso_affinity"] >= 3},
        {"id": "druso_int1", "label": "druso_int1", "tipo": "invito",
         "char": "druso", "titolo": "Druso in palestra. Dice che si allena",
         "luna_min": 2, "slot": "mattina",
         "cond": lambda v: "druso_ev1" in v["visti"]
         and "scelta_cuore" not in v["visti"]},
        # Deviazione: non sblocca niente, nessuna cond la richiede.
        {"id": "druso_quaderno", "label": "druso_quaderno", "tipo": "invito",
         "char": "druso", "titolo": "Druso ha dimenticato qualcosa al Becco Storto",
         "luna_min": 2, "slot": "pomeriggio",
         "cond": lambda v: "druso_ev1" in v["visti"]
         and "scelta_cuore" not in v["visti"]},
        {"id": "druso_ev2", "label": "druso_ev2", "tipo": "invito",
         "char": "druso", "titolo": "Una scommessa che puzza di trappola",
         "luna_min": 3, "slot": "sera",
         "cond": lambda v: v["druso_affinity"] >= 6
         and "druso_ev1" in v["visti"]},
        {"id": "druso_int2", "label": "druso_int2", "tipo": "invito",
         "char": "druso", "titolo": "Cena di famiglia in taverna. Sei l'ospite",
         "luna_min": 3, "slot": "sera",
         "cond": lambda v: "druso_ev2" in v["visti"]
         and "scelta_cuore" not in v["visti"]},
        {"id": "druso_udienza", "label": "druso_udienza", "tipo": "invito",
         "char": "druso", "titolo": "Lenora convoca Druso. Lui ti vuole fuori, ad aspettare",
         "luna_min": 3, "slot": "mattina",
         "cond": lambda v: "druso_ev2" in v["visti"]
         and "scelta_cuore" not in v["visti"]},
        {"id": "druso_ev3", "label": "druso_ev3", "tipo": "invito",
         "char": "druso", "titolo": "Druso ti vuole con sé. Non spiega perché",
         "luna_min": 4, "slot": "pomeriggio",
         "cond": lambda v: v["druso_affinity"] >= 9
         and "druso_ev2" in v["visti"]},
        {"id": "druso_int3", "label": "druso_int3", "tipo": "invito",
         "char": "druso", "titolo": "Druso chiede lezioni. A te. Di nascosto",
         "luna_min": 4, "slot": "mattina",
         "cond": lambda v: "druso_ev3" in v["visti"]
         and "scelta_cuore" not in v["visti"]},
        {"id": "druso_ev4", "label": "druso_ev4", "tipo": "invito",
         "char": "druso", "titolo": "Notte di guardia sulle mura di Zefiro",
         "luna_min": 4, "slot": "sera",
         "cond": lambda v: v["druso_affinity"] >= 9
         and "druso_ev3" in v["visti"]
         and "scelta_cuore" not in v["visti"]},
        {"id": "druso_luna5", "label": "druso_luna5", "tipo": "fisso",
         "char": "druso", "luna": 5, "giorno": 6, "slot": "sera",
         "cond": lambda v: v["route_attiva"] == "druso"
         and "druso" not in v["congelate"]},
        {"id": "druso_luna6", "label": "druso_luna6", "tipo": "fisso",
         "char": "druso", "luna": 6, "giorno": 5, "slot": "sera",
         "cond": lambda v: v["route_attiva"] == "druso"
         and "druso" not in v["congelate"]},
    ])


## Impegno (scelta del cuore) ################################################

label impegno_druso:
    $ lento()
    scene bg vicoli_zefiro with fade
    $ lento()
    show druso imbarazzato at left with dissolve
    "Mi aspetta fuori dalla taverna, per una volta senza pubblico. Ha in mano un foglio piegato in quattro, e l'aria di chi preferirebbe un TESCHIO."
    "Dentro, qualcuno grida il suo nome per il solito giro di versi. Lui non si gira."
    druso "Ho scritto una cosa. Non oscena. È... il problema è proprio questo, che non è oscena. Prima di dartela devo sapere se ridi."
    druso "Ci ho messo tre notti. Le altre le scrivo in tre minuti, sul tovagliolo. Questa no. Questa non voleva venire."
    $ muovi("druso", "trema")
    "Il foglio trema appena. Se ne accorge, lo stringe più forte, e adesso trema la mano intera."
    menu:
        "«Perché il poema più bello non nasce dall'immaginazione.»"
        "Prendere il foglio senza ridere" (peso=True):
            $ impegno_esito = True
            "Lo leggo. Non c'è una parolaccia. C'è una strada di neve fatta in due, e nessuno che spinge l'altro nel fosso. Rima baciata, naturalmente."
            "Ci sono la taverna, le mura di Zefiro, il ponte sul canale. E ci sono io, senza nome, in ogni strofa."
            show druso ghigno with qdiss
            druso "Allora? Metrica zoppa? Contenuto che arranca? Di' qualcosa o DICHIARO."
            pc "Bis."
            druso "...bis concesso. A vita, se serve."
            "Dentro, la taverna continua a chiamarlo. Lui le volta le spalle e mi offre il braccio, con un inchino ridicolo."
        "Restituirgli il foglio senza leggerlo" (peso=True):
            $ impegno_esito = False
            $ congelate.add("druso")
            druso "Giusto. Che stupidaggine. Era uno scherzo, ovvio! Il finto sentimento: il mio capolavoro!"
            "Ride forte. Troppo forte. E da quella sera le sue poesie tornano oscene, e mai più su di me."
    return


## Fatti ed echi delle deviazioni ##############################################

init python:
    CONSEGUENZE_VARS.extend(["druso_quaderno_esito", "druso_udienza_esito"])

    FATTI.extend([
        {"id": "fx_druso_quaderno", "char": "druso",
         "testo": "Hai trovato il quaderno dei versi seri di Druso, sotto la sua panca al Becco Storto.",
         "avviso": "Druso se ne ricorderà.",
         "cond": lambda v: v["druso_quaderno_esito"] is not None},
        {"id": "fx_druso_udienza", "char": "druso",
         "testo": "Hai aspettato Druso nel cortile dei carri, dopo l'udienza privata con sua madre.",
         "avviso": None,
         "cond": lambda v: v["druso_udienza_esito"] is not None},
    ])

    # Echi in Luna V-VI: chi racconta c'era (Druso) o e' di famiglia (Icaro).
    ECHI.extend([
        {"id": "echi_druso_quaderno", "fatto": "fx_druso_quaderno",
         "luoghi": ("taverna",), "label": "echi_druso_quaderno",
         "cond": lambda v: v["luna"] >= 5
         and "druso" not in v["congelate"]},
        {"id": "echi_druso_udienza", "fatto": "fx_druso_udienza",
         "luoghi": ("fumeria",), "label": "echi_druso_udienza",
         "cond": lambda v: v["luna"] >= 5
         and "druso" not in v["congelate"]},
    ])
