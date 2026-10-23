# Conseguenze — integrazione Ren'Py del motore puro (conseguenze_logic.py).
# Qui vivono: il registro automatico delle scelte (wrapper di menu), il
# registry FATTI, il registry ECHI (scene in routes/echi.rpy), gli avvisi e
# la screen "Trama" con l'albero delle conseguenze.
# Spec: docs/superpowers/specs/2026-10-22-conseguenze-design.md

init -5 python:
    from capitoli.malandrini import conseguenze_logic as csl

    # Ogni menu del gioco passa di qui (define menu sotto): la scena non
    # cambia, la scelta finisce in scelte_partita e nelle opzioni storiche.
    def conseguenze_menu(items, **kwargs):
        rv = renpy.display_menu(items, **kwargs)
        try:
            voci = [(l, v is not None) for l, v in items]
            firma = csl.firma_menu(store.cal_contesto, voci)
            scelta = None
            for l, v in items:
                if v is not None and getattr(v, "value", v) == rv:
                    scelta = l
            opzioni = [l for l, v in items if v is not None]
            csl.registra_scelta(store.scelte_partita, persistent.opzioni_viste,
                                persistent.opzioni_scelte, firma, opzioni, scelta)
        except Exception:
            # Il registro non deve mai fermare la partita.
            pass
        return rv

    # Variabili lette dalle cond dei fatti e degli echi.
    # Lista: altri file vi aggiungono le proprie variabili (append).
    CONSEGUENZE_VARS = [
        "aede_affinity", "flag_segreto_svelo", "flag_accetta_lavoro",
        "flag_giuramento", "flag_aede_rivelato", "caino_fiducia",
        "caino_trappole", "caino_druso", "flag_druso_coraggio",
        "druso_sfida", "druso_consiglio", "flag_icaro_coperto",
        "icaro_partita", "icaro_climax_scelta", "ofelia_mancati",
        "ofelia_in_pubblico", "ofelia_mano_cala", "route_attiva",
        "player_gender",
    ]

    def conseguenze_vars():
        v = {n: getattr(store, n, None) for n in CONSEGUENZE_VARS}
        v["visti"] = store.eventi_visti
        v["congelate"] = store.congelate
        v["scelte"] = store.scelte_partita
        v["noti"] = store.fatti_noti
        v["perso"] = invito_perso
        v["luna"] = CAL_SEQUENZA[min(store.cal_idx, len(CAL_SEQUENZA) - 1)][0]
        return v

    def _scelto(v, contesto, prefisso):
        return csl.scelto(v["scelte"], contesto, prefisso)

    # Fatti: conseguenze che il mondo ricorda. Derivati dallo stato gia'
    # scritto dalle scene, mai da punti. avviso None = nessuna notifica.
    FATTI = [
        # --- Aede -----------------------------------------------------------
        {"id": "aede_segreto", "char": "aede",
         "testo": "Hai giurato ad Aede che il suo segreto muore con te.",
         "avviso": "Aede se ne ricorderà.",
         "cond": lambda v: v["flag_segreto_svelo"]},
        {"id": "aede_vicolo_coperto", "char": "aede",
         "testo": "Nel vicolo della Contrada Marcassa non hai visto niente. Per lei.",
         "avviso": "Aede se ne ricorderà.",
         "cond": lambda v: "aede_cap4" in v["visti"] and v["flag_accetta_lavoro"]},
        {"id": "aede_vicolo_assassinio", "char": "aede",
         "testo": "Hai chiamato assassinio il lavoro di Aede. Lei ti ha voltato le spalle.",
         "avviso": "Aede se ne ricorderà.",
         "cond": lambda v: "aede_cap4" in v["visti"] and not v["flag_accetta_lavoro"]},
        {"id": "aede_giuramento", "char": "aede",
         "testo": "Hai fermato Aede prima che pronunciasse il suo nome di prima.",
         "avviso": None,
         "cond": lambda v: v["flag_giuramento"]},
        {"id": "aede_nome", "char": "aede",
         "testo": "Hai ascoltato il nome di prima di Aede. E qualcuno vi ha visti.",
         "avviso": "Il Nord se ne ricorderà.",
         "cond": lambda v: v["flag_aede_rivelato"]},
        # --- Caino ----------------------------------------------------------
        {"id": "caino_trappola", "char": "caino",
         "testo": "All'Adunanza hai lodato il Ballo delle Candele Spente. Caino ti ha archiviato.",
         "avviso": "Caino se ne ricorderà.",
         "cond": lambda v: "adunanza" in v["visti"] and "caino" in v["congelate"]
         and v["caino_trappole"] >= 1},
        {"id": "caino_massacro", "char": "caino",
         "testo": "All'Adunanza hai detto a Caino che il Ballo fu un massacro. In faccia.",
         "avviso": "Caino se ne ricorderà.",
         "cond": lambda v: _scelto(v, "adunanza", "«Era un massacro")},
        {"id": "caino_teschio", "char": "caino",
         "testo": "Druso ti ha preso come testimone del Codice del Teschio.",
         "avviso": "Druso se ne ricorderà.",
         "cond": lambda v: v["caino_druso"] >= 2},
        # --- Druso ----------------------------------------------------------
        {"id": "druso_lanternaio", "char": "druso",
         "testo": "Nei vicoli di Zefiro sei intervenut[fin] per il lanternaio. E Druso ti è venuto dietro.",
         "avviso": "Zefiro se ne ricorderà.",
         "cond": lambda v: v["flag_druso_coraggio"]},
        {"id": "druso_versi", "char": "druso",
         "testo": "Alla sfida di Lisandro hai preso due versi, poi hai reso la parola a Druso.",
         "avviso": None,
         "cond": lambda v: v["druso_sfida"] == "verso"},
        {"id": "druso_via", "char": "druso",
         "testo": "Alla sfida di Lisandro hai portato via Druso per il braccio.",
         "avviso": "Druso se ne ricorderà.",
         "cond": lambda v: v["druso_sfida"] == "via"},
        {"id": "druso_silenzio", "char": "druso",
         "testo": "Alla sfida di Lisandro sei rimast[fin] in silenzio: toccava a lui.",
         "avviso": None,
         "cond": lambda v: v["druso_sfida"] == "silenzio"},
        # --- Icaro ----------------------------------------------------------
        {"id": "icaro_coperto", "char": "icaro",
         "testo": "Al tavolo grande hai mentito per Icaro: «tutto regolare».",
         "avviso": "Icaro se ne ricorderà.",
         "cond": lambda v: v["flag_icaro_coperto"]},
        {"id": "icaro_copre", "char": "icaro",
         "testo": "Hai rovesciato il bicchiere sul panno per salvare la mano di Icaro.",
         "avviso": None,
         "cond": lambda v: v["icaro_partita"] == "copre"},
        {"id": "icaro_smaschera", "char": "icaro",
         "testo": "Hai smascherato l'anello a specchio, senza dire una parola su Icaro.",
         "avviso": None,
         "cond": lambda v: v["icaro_partita"] == "smaschera"},
        # --- Ofelia ---------------------------------------------------------
        {"id": "ofelia_attesa", "char": "ofelia",
         "testo": "Ofelia ti ha aspettat[fin] una volta. Non c'eri.",
         "avviso": "Ofelia se ne ricorderà.",
         "cond": lambda v: v["ofelia_mancati"] >= 1},
        {"id": "ofelia_gelo", "char": "ofelia",
         "testo": "Ofelia non aspetta la seconda volta: sei fuori dalla sua corte.",
         "avviso": "Ofelia se ne ricorderà.",
         "cond": lambda v: v["ofelia_mancati"] >= 2},
        {"id": "ofelia_luce", "char": "ofelia",
         "testo": "Hai tolto il velo a Ofelia e le hai offerto il braccio, alla luce del sole.",
         "avviso": "Rocca Tempesta se ne ricorderà.",
         "cond": lambda v: v["ofelia_in_pubblico"]},
        # --- Comune ---------------------------------------------------------
        {"id": "lenora_insolenza", "char": None,
         "testo": "Alla grata di Lenora hai risposto con un'insolenza. Annotata, non punita.",
         "avviso": "Lenora se ne ricorderà.",
         "cond": lambda v: _scelto(v, "udienza_lenora", "«Bene.")},
        {"id": "lenora_silenzio", "char": None,
         "testo": "Alla grata di Lenora hai taciuto e chinato la testa.",
         "avviso": None,
         "cond": lambda v: _scelto(v, "udienza_lenora", "Tacere")},
    ]

    # Echi: il fatto torna in un'altra scena, raccontato da chi puo' saperlo.
    # luoghi = id di attivita' del calendario (ATTIVITA). Scene in
    # routes/echi.rpy; una volta sola per partita.
    ECHI = [
        {"id": "echi_caino_ottone", "fatto": "caino_trappola",
         "luoghi": ("registri",), "label": "echi_caino_ottone"},
        {"id": "echi_caino_corrado", "fatto": "caino_massacro",
         "luoghi": ("studio", "studio_p"), "label": "echi_caino_corrado"},
        {"id": "echi_lenora_corrado", "fatto": "lenora_insolenza",
         "luoghi": ("studio", "studio_p", "riti"), "label": "echi_lenora_corrado"},
        {"id": "echi_icaro_mercante", "fatto": "icaro_coperto",
         "luoghi": ("citta",), "label": "echi_icaro_mercante"},
        {"id": "echi_druso_lanternaio", "fatto": "druso_lanternaio",
         "luoghi": ("citta",), "label": "echi_druso_lanternaio"},
        {"id": "echi_teschio_taverna", "fatto": "caino_teschio",
         "luoghi": ("taverna",), "label": "echi_teschio_taverna"},
        {"id": "echi_aede_marcassa", "fatto": "aede_vicolo_coperto",
         "luoghi": ("riti",), "label": "echi_aede_marcassa"},
        {"id": "echi_aede_orari", "fatto": "aede_vicolo_assassinio",
         "luoghi": ("riti",), "label": "echi_aede_orari"},
        {"id": "echi_ofelia_lista", "fatto": "ofelia_gelo",
         "luoghi": ("riti",), "label": "echi_ofelia_lista"},
    ]
    # FATTI ed ECHI si estendono da altri file (FATTI.extend / ECHI.extend in
    # init python): qui niente indici precalcolati.
    def echi_label(eid):
        for e in ECHI:
            if e["id"] == eid:
                return e["label"]
        return None

    def invito_perso(eid):
        """Invito offerto almeno una volta e mai preso, a scelta del cuore
        passata: qualcun altro ci e' andato al posto tuo."""
        return (eid in store.inviti_mostrati and eid not in store.eventi_visti
                and "scelta_cuore" in store.eventi_visti)

    def pool_aggiungi(att_id, label, indice=None):
        """Inserisce una scena nel pool di un'attivita' (da init 5 in su,
        dopo che attivita.rpy ha riempito ATTIVITA)."""
        for voci in ATTIVITA.values():
            for voce in voci:
                if voce[0] == att_id and label not in voce[3]:
                    if indice is None:
                        voce[3].append(label)
                    else:
                        voce[3].insert(indice, label)
                    return
        raise KeyError(att_id)

    def conseguenze_aggiorna():
        """Dopo ogni evento e attivita': registra i fatti nuovi e avvisa."""
        nuovi = csl.nuovi_fatti(FATTI, conseguenze_vars(), store.fatti_noti)
        ctx = store.cal_contesto or "inizio"
        for fid in nuovi:
            store.fatti_noti[fid] = (ctx, store.cal_idx)
            persistent.fatti_storici.add(fid)
        if persistent.avvisi_conseguenze:
            # Stesso canale del feedback delle affinita' (feedback.rpy), che
            # scarta l'avviso se lo stesso personaggio ha gia' la sua riga.
            for f in FATTI:
                if f["id"] in nuovi and f["avviso"]:
                    feedback_avviso(f["char"], f["avviso"])

    def conseguenze_dopo_evento(ev):
        persistent.trama_visti.add(ev["id"])
        conseguenze_aggiorna()

    cal_post_evento_hooks.append(conseguenze_dopo_evento)

    def echi_pesca(att_id):
        return csl.pesca_eco(ECHI, att_id, store.fatti_noti, store.echi_visti,
                             store.cal_idx, conseguenze_vars())

    ## Albero ################################################################

    TRAMA_SCHEDE = [("comune", "Comune"), ("aede", "Aede"), ("caino", "Caino"),
                    ("druso", "Druso"), ("icaro", "Icaro"), ("ofelia", "Ofelia")]

    # Eventi senza titolo d'invito: il nome del nodo nell'albero.
    TRAMA_TITOLI = {
        "svelo": "Lo Svelo",
        "adunanza": "L'Adunanza",
        "trio_lenora": "I tre figli di Lenora",
        "incrocio_debiti": "Debiti",
        "athlion": "L'Athlion",
        "udienza_lenora": "L'udienza di Lenora",
        "incrocio_palestra": "La palestra",
        "incrocio_sorelle": "Le figlie di Glauco",
        "incrocio_serra": "La serra",
        "incrocio_carte": "Le carte",
        "rivalita": "Rivalità",
        "scelta_cuore": "La scelta del cuore",
        "fiaccolata": "La Fiaccolata della Calà",
        "aede_cap6": "Il giuramento",
        "caino_luna5": "La talpa nei registri",
        "druso_luna5": "La sfida di Lisandro",
        "druso_luna6": "Il Consiglio di Lenora",
        "icaro_luna5": "La partita",
        "icaro_luna6": "Il conto di Icaro",
        "ofelia_ev4": "Alla luce del sole",
        "interludio_ofelia_luna6": "Prima della fine",
        "luna6_climax": "Luna VI",
    }
    # Eventi comuni che aprono una route: stanno nella sua scheda.
    TRAMA_ROUTE = {"adunanza": "caino"}
    # Nodi visibili solo per un genere del protagonista.
    TRAMA_GENERE = {"icaro_bro1": "m", "icaro_bro2": "m"}

    def _trama_luna(ev):
        return ev.get("luna", ev.get("luna_min", 1))

    # Ordine del racconto: per Luna; nella stessa Luna le date fisse prima
    # degli inviti (l'Adunanza apre la route di Caino), poi l'ordine del
    # registry, che e' l'ordine delle catene cap1 -> cap2 -> ...
    def _trama_ordine(ev, i):
        return (_trama_luna(ev), ev.get("giorno", 99), i)

    def trama_nodi(scheda):
        scelti = []
        for i, ev in enumerate(EVENTI):
            dove = TRAMA_ROUTE.get(ev["id"], ev.get("char") or "comune")
            genere = TRAMA_GENERE.get(ev["id"])
            if dove != scheda or (genere and genere != store.player_gender):
                continue
            scelti.append((_trama_ordine(ev, i), ev))
        scelti.sort(key=lambda t: t[0])
        return [(ev["id"], TRAMA_TITOLI.get(ev["id"], ev.get("titolo", "Un momento del semestre")),
                 LUNE_NOMI[_trama_luna(ev)])
                for _k, ev in scelti]

    def trama_albero(scheda):
        # Copia migrata: regge anche un rollback oltre il caricamento.
        scelte = dict(store.scelte_partita)
        csl.migra_storico(scelte, {}, set(), csl.OPZIONI_RINOMINATE)
        return csl.albero(trama_nodi(scheda), store.eventi_visti,
                          persistent.trama_visti, scelte,
                          persistent.opzioni_viste, persistent.opzioni_scelte,
                          store.fatti_noti, FATTI)

    def trama_sciolti(scheda):
        char = None if scheda == "comune" else scheda
        return csl.fatti_sciolti(trama_nodi(scheda), store.fatti_noti, FATTI, char)

    def trama_conto(scheda):
        nodi = trama_nodi(scheda)
        return sum(1 for n in nodi if n[0] in store.eventi_visti), len(nodi)

define menu = conseguenze_menu

default cal_contesto = None
default scelte_partita = {}
default fatti_noti = {}
default echi_visti = set()
default inviti_mostrati = set()
default persistent.opzioni_viste = {}
default persistent.opzioni_scelte = set()
default persistent.trama_visti = set()
default persistent.fatti_storici = set()
default persistent.avvisi_conseguenze = True


## Screen Trama ###############################################################

screen trama(scheda="comune"):

    tag menu

    default trama_scheda = scheda

    use game_menu(_("Trama")):

        vbox:
            spacing 16

            hbox:
                spacing 6
                box_wrap True
                for sid, nome in TRAMA_SCHEDE:
                    textbutton nome:
                        style "cronache_tab"
                        text_style "cronache_tab_text"
                        selected (sid == trama_scheda)
                        action SetScreenVariable("trama_scheda", sid)

            $ trama_n, trama_tot = trama_conto(trama_scheda)
            text "Momenti vissuti: [trama_n] / [trama_tot]  ·  ◆ questa partita  ·  ◇ un'altra partita  ·  in oro la tua scelta" size TESTO_NOTA italic True color "#8f7f5c"

            add "gui/divisore.png" xalign 0.0

            viewport:
                ysize (560 if renpy.variant("small") else 600)
                scrollbars "vertical"
                vscrollbar_unscrollable "hide"
                mousewheel True
                draggable True

                vbox:
                    spacing 14
                    xfill True

                    for eid, titolo, luna, stato, menu_nodo, nati in trama_albero(trama_scheda):
                        vbox:
                            spacing 6
                            hbox:
                                spacing 12
                                if stato == "ignoto":
                                    text "— ? —" style "trama_nodo" color "#6b5f4a"
                                else:
                                    text ("◆" if stato == "vissuto" else "◇") size 22 color ("#c0392b" if stato == "vissuto" else "#8f7f5c") yoffset 6
                                    text titolo style "trama_nodo" color ("#f0c75e" if stato == "vissuto" else "#a89468")
                                text luna size TESTO_NOTA italic True color "#8a7a5a" yalign 0.5
                            for didascalia, righe in menu_nodo:
                                vbox:
                                    xoffset 38
                                    spacing 2
                                    for testo, st in righe:
                                        text ("› " + testo) style "trama_opzione" color ("#f0c75e" if st == "scelta" else "#a89468" if st == "passata" else "#5e5442")
                            for fatto in nati:
                                text ("◆ " + fatto) style "trama_fatto" xoffset 38
                            if eid in ("aede_cap4", "adunanza") and trama_scheda in congelate and eid in eventi_visti:
                                text "La porta si è chiusa." style "trama_fatto" xoffset 38 color "#c0392b"

                    $ trama_resto = trama_sciolti(trama_scheda)
                    if trama_resto:
                        null height 8
                        text "Altre conseguenze" style "trama_nodo"
                        for fatto in trama_resto:
                            text ("◆ " + fatto) style "trama_fatto" xoffset 38


style trama_nodo is text
style trama_nodo:
    font gui.name_text_font
    size 28
    color gui.accent_color
    outlines [(2, "#140a08", 0, 0)]

style trama_opzione is text
style trama_opzione:
    font gui.text_font
    size 23

style trama_fatto is text
style trama_fatto:
    font gui.text_font
    size 23
    italic True
    color "#d9a38a"


# Opzioni di menu riscritte: lo storico (persistent e salvataggi) passa ai
# testi nuovi, cosi' la Trama non sdoppia i nodi. Mappa in conseguenze_logic.
init 999 python:
    if persistent.opzioni_viste is not None and persistent.opzioni_scelte is not None:
        csl.migra_storico({}, persistent.opzioni_viste,
                          persistent.opzioni_scelte, csl.OPZIONI_RINOMINATE)

    def _conseguenze_migra_salvataggio():
        csl.migra_storico(store.scelte_partita, {}, set(),
                          csl.OPZIONI_RINOMINATE)

