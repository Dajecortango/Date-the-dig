# Calendario dei Malandrini — integrazione Ren'Py del motore puro
# (game/calendario_logic.py). Qui vivono: il calendario concreto, il registry
# EVENTI (gli altri file vi aggiungono voci in init python), le attività,
# il loop del semestre e la screen di pianificazione.

init -10 python:
    import calendario_logic as cl

    # 6 Lune; esistono solo i giorni/slot salienti (il resto si salta).
    # Le date fisse della spec cadono su questi giorni:
    #   Svelo I/1 sera, Adunanza II/8 sera, Athlion III/10 pomeriggio,
    #   scelta del cuore IV/28 sera, Fiaccolata V/14 sera, climax VI/21 sera.
    CAL_GIORNI = {
        1: [{"giorno": 1, "slots": ["sera"]},
            {"giorno": 6, "slots": ["mattina", "pomeriggio", "sera"]},
            {"giorno": 14, "slots": ["mattina", "pomeriggio", "sera"]},
            {"giorno": 21, "slots": ["mattina", "sera"]}],
        2: [{"giorno": 2, "slots": ["mattina", "pomeriggio"]},
            {"giorno": 8, "slots": ["sera"]},
            {"giorno": 15, "slots": ["mattina", "pomeriggio", "sera"]},
            {"giorno": 22, "slots": ["pomeriggio", "sera"]}],
        3: [{"giorno": 4, "slots": ["mattina", "pomeriggio", "sera"]},
            {"giorno": 10, "slots": ["pomeriggio"]},
            {"giorno": 16, "slots": ["mattina", "pomeriggio", "sera"]},
            {"giorno": 25, "slots": ["mattina", "sera"]}],
        4: [{"giorno": 3, "slots": ["mattina", "pomeriggio", "sera"]},
            {"giorno": 11, "slots": ["mattina", "pomeriggio", "sera"]},
            {"giorno": 18, "slots": ["mattina", "sera"]},
            {"giorno": 28, "slots": ["sera"]}],
        5: [{"giorno": 6, "slots": ["mattina", "pomeriggio", "sera"]},
            {"giorno": 14, "slots": ["sera"]},
            {"giorno": 20, "slots": ["mattina", "pomeriggio", "sera"]},
            {"giorno": 26, "slots": ["pomeriggio", "sera"]}],
        6: [{"giorno": 5, "slots": ["mattina", "pomeriggio", "sera"]},
            {"giorno": 12, "slots": ["mattina", "sera"]},
            {"giorno": 21, "slots": ["sera"]}],
    }
    CAL_SEQUENZA = cl.genera_sequenza(CAL_GIORNI)

    LUNE_NOMI = {1: "Luna I", 2: "Luna II", 3: "Luna III",
                 4: "Luna IV", 5: "Luna V", 6: "Luna VI"}

    # Registry eventi: i file delle route appendono qui (init python, offset
    # di default 0 > questo -10, quindi EVENTI esiste gia').
    EVENTI = []

    # Attivita' per slot: (id, etichetta, char | None, pool di label una-tantum)
    ATTIVITA = {"mattina": [], "pomeriggio": [], "sera": []}

    # Hook chiamati dopo ogni evento/attivita' (es. gelosia di Icaro, Task 7).
    cal_post_evento_hooks = []

    # Riga mostrata quando il pool di un'attivita' e' esaurito.
    CAL_FALLBACK = {
        "spada": "Un altro giorno di guardie e affondi. Le braccia ricordano anche quando la testa è altrove.",
        "spada_p": "Un altro giorno di guardie e affondi. Le braccia ricordano anche quando la testa è altrove.",
        "scudo": "Scudo su, scudo giù. Druso oggi tortura altri novellini: si sente da qui.",
        "studio": "Pagine, stemmi, date. La storia della Famiglia non finisce mai; la mia pazienza sì.",
        "studio_p": "Pagine, stemmi, date. La storia della Famiglia non finisce mai; la mia pazienza sì.",
        "riti": "Brodo, cucine, voci. Il Ceppo gira anche senza di me. Ma gira meglio con me.",
        "citta": "Zefiro d'ordinanza: commissioni, saluti, scorciatoie. Nessuna lama nell'ombra, oggi.",
        "registri": "Colonne che tornano, Scudi che non mancano. Giornata rara, alla Proprietà.",
        "taverna": "Boccali, cori stonati, nessuna rissa degna di nota. La locandiera ringrazia.",
        "fumeria": "Fumo dolce e carte lente. Icaro vince, come il sole sorge.",
    }

    def cal_vars():
        """Dict passato alle cond degli eventi."""
        v = {
            "aede_affinity": store.aede_affinity,
            "caino_fiducia": getattr(store, "caino_fiducia", 0),
            "druso_affinity": store.druso_affinity,
            "icaro_affinity": store.icaro_affinity,
            "congelate": store.congelate,
            "player_gender": store.player_gender,
            "route_attiva": store.route_attiva,
            "flag_accetta_lavoro": store.flag_accetta_lavoro,
            "flag_giuramento": store.flag_giuramento,
            "visti": store.eventi_visti,
        }
        return v

    # Testata del pianificatore: striscia dei giorni e slot del giorno.
    def cal_strip(luna, giorno):
        out = []
        for g in CAL_GIORNI[luna]:
            num = g["giorno"]
            stato = ("oggi" if num == giorno
                     else "passato" if num < giorno else "futuro")
            fisso = any(e["tipo"] == "fisso" and e.get("luna") == luna
                        and e.get("giorno") == num for e in EVENTI)
            out.append((num, stato, fisso))
        return out

    def cal_slot_stati(momento):
        luna, giorno, slot = momento
        slots = next(g["slots"] for g in CAL_GIORNI[luna]
                     if g["giorno"] == giorno)
        idx = slots.index(slot)
        return [(s, "corrente" if i == idx
                 else "passato" if i < idx else "futuro")
                for i, s in enumerate(slots)]

    # Sottotitoli delle attivita' nel pianificatore.
    ATTIVITA_DESC = {
        "spada": "Il cortile d'armi all'alba. C'è sempre lei.",
        "spada_p": "Il cortile d'armi. C'è sempre lei.",
        "scudo": "Scudo, lotta e la voce di Druso sopra tutto.",
        "studio": "Stemmi, Virtù e storia con Corrado.",
        "studio_p": "Stemmi, Virtù e storia con Corrado.",
        "riti": "Il brodo, le cucine, la famiglia che urla.",
        "citta": "Zefiro: consegne, vicoli, orecchie aperte.",
        "registri": "Le colonne della Proprietà. L'Arconte controlla.",
        "taverna": "Boccali e versi osceni. Druso tiene banco.",
        "fumeria": "Fumo dolce e carte. Icaro non perde mai.",
    }

    # Diario del semestre: stato diegetico, mai numeri.
    def diario_data():
        if store.cal_idx < len(CAL_SEQUENZA):
            l, g, s = CAL_SEQUENZA[store.cal_idx]
            return "%s — giorno %d, %s" % (LUNE_NOMI[l], g, s)
        return "Semestre concluso"

    def diario_eventi_contati():
        return sum(1 for e in EVENTI if e["id"] in store.eventi_visti)

    def diario_rapporti():
        righe = []

        def riga(nome, char, aff, soglie):
            alta, media, bassa = soglie
            if store.route_attiva == char:
                righe.append((nome, alta[1]))
            elif char in store.congelate:
                righe.append((nome, "Una porta chiusa. Da dentro."))
            elif aff >= alta[0]:
                righe.append((nome, alta[1]))
            elif aff >= media[0]:
                righe.append((nome, media[1]))
            elif aff >= bassa[0]:
                righe.append((nome, bassa[1]))
            else:
                righe.append((nome, "Vi conoscete di vista. Forse."))

        riga("Aede", "aede", store.aede_affinity,
             ((8, "Ti tiene il posto accanto agli allenamenti. Negherebbe."),
              (4, "Ti chiama ancora «novellin[fin]», ma con meno veleno."),
              (1, "Ti squadra come un bersaglio mobile.")))
        if "adunanza" in store.eventi_visti:
            riga("Caino", "caino", getattr(store, "caino_fiducia", 0),
                 ((10, "Ti versa l'idromele senza chiedere."),
                  (6, "Ricorda il tuo nome. E tu ricordi i suoi dettagli."),
                  (2, "Ti osserva come una moneta trovata per terra.")))
        riga("Druso", "druso", store.druso_affinity,
             ((9, "Ti chiama «linguaccia» davanti a tutti. È affetto."),
              (5, "Ti dedica i versi peggiori. Buon segno."),
              (1, "Ti punzecchia per capire se abbai o mordi.")))
        riga("Icaro", "icaro", store.icaro_affinity,
             ((7, "Ti lascia guardare le sue mani. Sa che vedi."),
              (4, "Non ti conta più tra i passivi."),
              (1, "Ti tollera al tavolo piccolo.")))
        return righe

    def cal_portrait(char):
        p = "gui/portrait_%s.png" % char if char else "gui/portrait_locked.png"
        return p if renpy.loadable(p) else "gui/portrait_locked.png"

    # I dict evento contengono lambda (cond): non devono MAI finire nello
    # store o in _return, o il salvataggio fallisce il pickle. Nello store
    # girano solo id e stringhe; i dict restano dentro queste funzioni.
    def cal_evento_di(eid):
        for e in EVENTI:
            if e["id"] == eid:
                return e
        return None

    def cal_label_di(eid):
        return cal_evento_di(eid)["label"]

    def cal_trova_fisso_id(momento):
        ev = cl.trova_fisso(momento, EVENTI, cal_vars(), store.eventi_visti)
        return ev["id"] if ev else None

    def cal_inviti_info(momento):
        evs = cl.trova_inviti(momento, EVENTI, cal_vars(), store.eventi_visti)
        # A route attiva, gli inviti degli altri personaggi scalano a sfondo.
        if store.route_attiva is not None:
            evs = [e for e in evs
                   if e.get("char") in (None, store.route_attiva)]
        return [{"id": e["id"], "char": e.get("char"),
                 "titolo": e.get("titolo", "Qualcuno ti cerca")} for e in evs]

    def cal_dopo_evento(eid):
        ev = cal_evento_di(eid)
        for hook in cal_post_evento_hooks:
            hook(ev)

default cal_idx = 0
default cal_ultimo_giorno = None
default eventi_visti = set()
default congelate = set()
default route_attiva = None
default druso_affinity = 0
default icaro_affinity = 0

## Loop del semestre #########################################################

label cal_loop:

    if cal_idx >= len(CAL_SEQUENZA):
        jump cal_fine_semestre

    python:
        cal_luna, cal_giorno, cal_slot = CAL_SEQUENZA[cal_idx]

    # Riga di data a ogni cambio di giorno + nome del salvataggio.
    if cal_ultimo_giorno != (cal_luna, cal_giorno):
        $ cal_ultimo_giorno = (cal_luna, cal_giorno)
        $ save_name = LUNE_NOMI[cal_luna] + " — giorno " + str(cal_giorno)
        centered "{cps=30}[LUNE_NOMI[cal_luna]] — giorno [cal_giorno]{/cps}"

    $ cal_fisso_id = cal_trova_fisso_id((cal_luna, cal_giorno, cal_slot))

    if cal_fisso_id is not None:
        $ eventi_visti.add(cal_fisso_id)
        call expression cal_label_di(cal_fisso_id)
        $ cal_dopo_evento(cal_fisso_id)
        jump cal_avanza

    python:
        cal_inviti = cal_inviti_info((cal_luna, cal_giorno, cal_slot))
        # Una voce attivita' puo' avere una cond opzionale come quinto campo.
        cal_att = [a[:4] for a in ATTIVITA.get(cal_slot, [])
                   if len(a) < 5 or a[4](cal_vars())]

    if not cal_inviti and not cal_att:
        jump cal_avanza

    $ renpy.transition(Dissolve(0.2))
    call screen pianificazione((cal_luna, cal_giorno, cal_slot), cal_inviti, cal_att)

    if _return[0] == "evento":
        python:
            cal_sel_id = _return[1]
            eventi_visti.add(cal_sel_id)
        call expression cal_label_di(cal_sel_id)
        $ cal_dopo_evento(cal_sel_id)
    else:
        call cal_attivita(_return[1])

    jump cal_avanza

label cal_avanza:
    $ cal_idx += 1
    jump cal_loop

label cal_attivita(att_id):
    python:
        cal_pool = None
        for slot_att in ATTIVITA.values():
            for voce in slot_att:
                if voce[0] == att_id:
                    cal_pool = voce[3]
        cal_label = cl.pesca_variante(cal_pool or [], eventi_visti)
    if cal_label is None:
        $ cal_fallback_txt = CAL_FALLBACK.get(att_id, "La giornata passa come tante: fatica, abitudine, il Nord che non chiede niente.")
        "[cal_fallback_txt]"
        return
    $ eventi_visti.add(cal_label)
    call expression cal_label
    return

label cal_fine_semestre:
    # Rete di sicurezza: se la sequenza finisce senza che Luna VI abbia
    # chiuso il semestre, chiude il finale neutro.
    if not semestre_concluso:
        call finale_neutro_semestre
    return


## Screen di pianificazione ##################################################

screen pianificazione(momento, inviti, attivita):

    modal True

    add "gui/game_menu.png"

    vbox:
        align (0.5, 0.5)
        spacing 18
        xmaximum 1100

        add Solid("#d4af37", xsize=320, ysize=2) xalign 0.5
        label LUNE_NOMI[momento[0]] text_size 44 text_color gui.accent_color xalign 0.5

        # Striscia dei giorni salienti della Luna: ◆ = festa o evento segnato.
        hbox:
            xalign 0.5
            spacing 30
            for num, stato, fisso in cal_strip(momento[0], momento[1]):
                vbox:
                    spacing 0
                    xminimum 46
                    text ("◆" if fisso else " ") size 14 xalign 0.5 color "#f0c75e"
                    text str(num) size 26 xalign 0.5 bold (stato == "oggi") color ("#f0c75e" if stato == "oggi" else "#6b5f4a" if stato == "passato" else "#c9b78a")

        # Slot del giorno: dove siamo arrivati.
        hbox:
            xalign 0.5
            spacing 24
            for nome_s, stato_s in cal_slot_stati(momento):
                text nome_s.capitalize() size 22 italic (stato_s == "corrente") color ("#f0e6d2" if stato_s == "corrente" else "#6b5f4a" if stato_s == "passato" else "#a89468")

        add Solid("#d4af37", xsize=320, ysize=2) xalign 0.5
        null height 6

        for inv in inviti:
            button:
                xfill True
                ypadding 8
                background Frame("gui/button/choice_idle_background.png", 24, 12)
                hover_background Frame("gui/button/choice_hover_background.png", 24, 12)
                action Return(("evento", inv["id"]))
                hbox:
                    spacing 18
                    add Transform(cal_portrait(inv["char"]), zoom=0.4) yalign 0.5
                    text inv["titolo"] size 26 color "#f5e3b8" yalign 0.5

        for aid, etichetta, char, _pool in attivita:
            button:
                xfill True
                ypadding 8
                background Frame("gui/button/choice_idle_background.png", 24, 12)
                hover_background Frame("gui/button/choice_hover_background.png", 24, 12)
                action Return(("att", aid))
                hbox:
                    spacing 18
                    if char:
                        add Transform(cal_portrait(char), zoom=0.3) yalign 0.5
                    vbox:
                        yalign 0.5
                        spacing 2
                        text etichetta size 26 color "#f0e6d2"
                        if aid in ATTIVITA_DESC:
                            text ATTIVITA_DESC[aid] size 17 color "#8f7f5c"

        null height 6
        frame:
            xfill True
            ypadding 8
            background Frame("gui/button/choice_idle_background.png", 24, 12)
            hbox:
                spacing 18
                add Transform(cal_portrait("ofelia"), zoom=0.4, alpha=0.55) yalign 0.5
                text "Ofelia" size 26 color "#6b5f4a" yalign 0.5
                text "— Prossimamente" size 20 color "#8f7f5c" yalign 0.5


## Diario del semestre #######################################################

screen diario():

    tag menu

    use game_menu(_("Diario"), scroll="viewport"):

        vbox:
            spacing 16
            xfill True

            text diario_data() size 32 color gui.accent_color

            null height 10

            for nome, riga in diario_rapporti():
                hbox:
                    spacing 14
                    text nome size 26 color "#f5e3b8" min_width 160
                    text riga size 24 color "#c9b78a"

            null height 14

            text "Momenti del semestre vissuti: [diario_eventi_contati()]" size 22 color "#8f7f5c"
