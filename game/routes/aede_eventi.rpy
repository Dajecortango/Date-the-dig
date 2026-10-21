# Route Aede — eventi sul calendario + mini-scena di impegno.

init python:
    EVENTI.extend([
        # Lo Svelo: prologo comune, prima sera del semestre.
        {"id": "svelo", "label": "prologo", "tipo": "fisso", "char": None,
         "luna": 1, "giorno": 1, "slot": "sera"},
        # L'Athlion: festa fissa di Luna III.
        {"id": "athlion", "label": "cap2", "tipo": "fisso", "char": None,
         "luna": 3, "giorno": 10, "slot": "pomeriggio"},
        # Inviti a soglia.
        {"id": "aede_cap1", "label": "cap1", "tipo": "invito", "char": "aede",
         "titolo": "Briseide ti convoca: una consegna col Ceppo di Glauco",
         "luna_min": 1, "slot": "mattina",
         "cond": lambda v: v["aede_affinity"] >= 2},
        {"id": "aede_cap3", "label": "cap3", "tipo": "invito", "char": "aede",
         "titolo": "Aede ti cerca: le Bocche Sicofanti",
         "luna_min": 3, "slot": "pomeriggio",
         "cond": lambda v: v["aede_affinity"] >= 5
         and "aede_cap1" in v["visti"]},
        {"id": "aede_cap4", "label": "ev_aede_cap4", "tipo": "invito",
         "char": "aede", "titolo": "Un lavoro nella Contrada Marcassa",
         "luna_min": 4, "slot": "sera",
         "cond": lambda v: v["aede_affinity"] >= 7
         and "aede_cap3" in v["visti"]
         and "scelta_cuore" not in v["visti"]},
    ])

default impegno_esito = None

# Lucchetto di meta' percorso: il vicolo (cap4). Rifiutare il suo mondo
# congela la route a livello amicizia.
label ev_aede_cap4:
    call cap4
    if not flag_accetta_lavoro:
        $ congelate.add("aede")
    return

# Mini-scena di impegno (chiamata dalla scelta del cuore, fine Luna IV).
label impegno_aede:
    scene bg corridoio_ceppo with fade
    show aede imbarazzata with dissolve
    "La trovo sul ballatoio del mio Ceppo, le serrature peggiori del Nord alle spalle, l'aria di chi prova le parole da un'ora."
    aede "Novellin[fin]. Questa... cosa. Tra te e me. Ofelia e Ascadeo cominciano a farci sopra delle scommesse, e io odio le scommesse che non controllo."
    show aede irritata with qdiss
    aede "Quindi dimmelo adesso: ha un nome, oppure no? Rispondi male e ti butto dal ballatoio."
    menu:
        "Non è una minaccia. È una domanda con l'armatura."
        "«Ha un nome. Il tuo.»":
            $ impegno_esito = True
            show aede sorriso with dissolve
            aede "...risposta accettabile. L'unica, per la cronaca."
            show aede irritata with qdiss
            aede "E sia chiaro: io non divido. Né le lame, né il posto agli allenamenti, né te. Chi ti ronza intorno, da stanotte, parla con me."
            "Non mi butta dal ballatoio. Resta, invece. E il resto del semestre, da stanotte, ha una direzione sola."
        "«Non ancora. Non così.»":
            $ impegno_esito = False
            $ congelate.add("aede")
            show aede neutra with qdiss
            aede "Capito. Ritiro la domanda. Mai fatta. Guardia alta, novellin[fin]: l'addestramento resta, il resto no."
            "Se ne va dritta come una lama. E la piega all'angolo della bocca, stavolta, non c'è."
    return
