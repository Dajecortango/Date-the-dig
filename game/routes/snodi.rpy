# Snodi comuni del semestre: scelta del cuore (fine Luna IV), Fiaccolata
# (Luna V), climax di Luna VI, finale neutro.

default semestre_concluso = False

init python:
    EVENTI.extend([
        {"id": "scelta_cuore", "label": "ev_scelta_cuore", "tipo": "fisso",
         "char": None, "luna": 4, "giorno": 28, "slot": "sera"},
        {"id": "fiaccolata", "label": "ev_fiaccolata", "tipo": "fisso",
         "char": None, "luna": 5, "giorno": 14, "slot": "sera"},
        # Il giuramento di Aede segue la Fiaccolata, solo a route attiva
        # (o seconda, nel poliamore con Ofelia) e non congelata: il vicolo
        # puo' congelare anche dopo l'impegno.
        {"id": "aede_cap6", "label": "cap6", "tipo": "fisso", "char": "aede",
         "luna": 5, "giorno": 20, "slot": "sera",
         "cond": lambda v: (v["route_attiva"] == "aede"
                            or v["route_seconda"] == "aede")
         and "aede" not in v["congelate"]
         and v["aede_sospetto"] < 2},
        {"id": "luna6_climax", "label": "ev_luna6", "tipo": "fisso",
         "char": None, "luna": 6, "giorno": 21, "slot": "sera"},
    ])

    CUORE_NOMI = {"aede": "Aede", "caino": "Caino",
                  "druso": "Druso", "icaro": "Icaro", "ofelia": "Ofelia"}

    def cuore_candidati():
        """Personaggi sopra soglia e non congelati, per la scelta del cuore."""
        f = store.player_gender == "f"
        soglie = {
            "aede": store.aede_affinity >= 8,
            "caino": store.caino_fiducia >= 10,
            "druso": store.druso_affinity >= (9 if f else 11),
            "icaro": store.icaro_affinity >= (7 if f else 6),
            "ofelia": store.ofelia_affinity >= 8,
        }
        return [c for c, ok in soglie.items()
                if ok and c not in store.congelate]

    def route_viva():
        """Route attiva e non congelata nel frattempo; altrimenti None."""
        if store.route_attiva and store.route_attiva not in store.congelate:
            return store.route_attiva
        return None

    def route_seconda_viva():
        """Seconda route del poliamore (solo con Ofelia viva), se non
        congelata nel frattempo; altrimenti None."""
        if route_viva() != "ofelia":
            return None
        if store.route_seconda and store.route_seconda not in store.congelate:
            return store.route_seconda
        return None

    def cuore_opzioni(cands):
        """Voci del menu del cuore: (testo, chiave). Oltre ai singoli, le
        coppie del poliamore se Ofelia e l'altro sono entrambi candidati."""
        opz = [(CUORE_NOMI[c], c) for c in cands]
        if "ofelia" in cands:
            for altro in ("aede", "caino"):
                if altro in cands:
                    opz.append(("Ofelia e " + CUORE_NOMI[altro],
                                "ofelia+" + altro))
        return opz


## Scelta del cuore ##########################################################

label ev_scelta_cuore:
    scene bg corridoio_ceppo with fade
    "Fine della quarta Luna. Vanna dice che a Rocca Tempesta i semestri si decidono adesso: «chi non ha scelto entro la Fiaccolata, ha scelto lo stesso»."
    python:
        cuore_lista = cuore_candidati()
    if not cuore_lista:
        "Guardo il semestre alle spalle: facce, allenamenti, serate. Nessun nome pesa più degli altri. Forse è presto. Forse sono io."
        return
    $ cuore_voci = cuore_opzioni(cuore_lista)
    if len(cuore_voci) == 1:
        $ cuore_scelto = cuore_voci[0][1]
    else:
        $ cuore_scelto = renpy.display_menu(
            [("A chi appartiene questo semestre?", None)] + cuore_voci)
    if cuore_scelto in ("ofelia+aede", "ofelia+caino"):
        $ cuore_altro = cuore_scelto.split("+")[1]
        if cuore_altro == "aede":
            call impegno_ofelia_aede
        else:
            call impegno_ofelia_caino
        if impegno_of and impegno_altro:
            $ route_attiva = "ofelia"
            $ route_seconda = cuore_altro
        elif impegno_of:
            $ route_attiva = "ofelia"
            $ route_seconda = None
        elif impegno_altro:
            $ route_attiva = cuore_altro
            $ route_seconda = None
        return
    if cuore_scelto == "aede":
        call impegno_aede
    elif cuore_scelto == "caino":
        call impegno_caino
    elif cuore_scelto == "druso":
        call impegno_druso
    elif cuore_scelto == "ofelia":
        call impegno_ofelia
    elif player_gender == "f":
        call impegno_icaro
    else:
        call impegno_bro
    if impegno_esito:
        $ route_attiva = cuore_scelto
    return


## Fiaccolata della Calà #####################################################

label ev_fiaccolata:
    $ cal_route = route_viva()
    if cal_route == "aede":
        call cap5
    elif cal_route == "caino":
        call fiaccolata_caino
    elif cal_route == "druso":
        call druso_fiaccolata
    elif cal_route == "icaro":
        call icaro_fiaccolata
    elif cal_route == "ofelia" and route_seconda_viva() == "caino":
        call ofelia_fiaccolata_caino
    elif cal_route == "ofelia" and route_seconda_viva() == "aede":
        call ofelia_fiaccolata_aede
    elif cal_route == "ofelia":
        call ofelia_fiaccolata
    else:
        call fiaccolata_neutra
    return

label fiaccolata_caino:
    scene bg cala_notte with fade
    show caino neutro with dissolve
    "La Calà, trecento gradini di lanterne. Caino li scende come scende in Consiglio: contando chi lo guarda."
    caino "Lo sai cosa vale questa leggenda, a registro? Niente. Nessun atto, nessun sigillo, nessun testimone utilizzabile."
    pc "Eppure sei qui."
    show caino tenero with dissolve
    caino "Sono qui perché le cose fuori inventario, ultimamente, rendono meglio di quelle a bilancio. Dammi la mano e non farlo pesare: se mia madre lo viene a sapere, dirò che era un'operazione di mercato."
    "Mano nella mano, dal primo gradino all'ultimo. L'Arconte della Proprietà non lascia la presa nemmeno per salutare due Eparchi. I dettagli possiedono le persone."
    return

label fiaccolata_neutra:
    scene bg cala_notte with fade
    "La Fiaccolata. Scendo la Calà con Vanna e Corrado, un gradino di luce alla volta."
    vanna "Guardali, i piccioncini della Rocca. E tu niente, [fratello_t]? Nemmeno una mano da tenere?"
    corrado "Lascialo stare. C'è chi scende la Calà per la leggenda, e chi per contare i gradini. Entrambi arrivano al fiume."
    "Arrivo al fiume. Trecento gradini, nessuna mano. La leggenda, quest'anno, parla d'altro."
    return


## Luna VI — il conto del semestre ###########################################

label ev_luna6:
    $ semestre_concluso = True
    $ cal_route = route_viva()
    if cal_route == "aede":
        call climax
    elif cal_route == "caino":
        call caino_climax
    elif cal_route == "druso":
        call druso_climax
    elif cal_route == "icaro":
        call icaro_climax
    elif cal_route == "ofelia":
        if route_seconda_viva() == "aede":
            call climax
        else:
            call ofelia_climax
    else:
        call finale_neutro_semestre
    return

label finale_neutro_semestre:
    scene bg corridoio_ceppo with fade
    show briseide neutra with dissolve
    "Fine della sesta Luna. Briseide mi riceve con due tazze di brodo: il bilancio di fine semestre, nel suo Ceppo, si fa così."
    briseide "Sei mesi. Hai imparato la spada, i registri, le scorciatoie di Zefiro e — mi dicono — anche a reggere un boccale. Non hai perso il nome, non hai perso il sangue. Nel Nord si chiama buon raccolto."
    pc "E il resto, madre?"
    briseide "Il resto ha i suoi tempi. Rocca Tempesta non scappa, e nemmeno i suoi cuori: sono tutti ancora lì, più testardi di prima. Bevi il brodo, [figlio_t] mi[fin]. I semestri finiscono. Le storie no."
    scene bg nero with fade
    centered "{cps=20}{size=+10}IL SEMESTRE DEL NOVELLINO{/size}\n\nGuardare, ascoltare, non farsi notare.\nDue su tre, come sempre.{/cps}"
    return
