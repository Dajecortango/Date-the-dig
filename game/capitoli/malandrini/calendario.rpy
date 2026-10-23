# Calendario dei Malandrini — integrazione Ren'Py del motore puro
# (calendario_logic.py, accanto). Qui vivono: il calendario concreto, il registry
# EVENTI (gli altri file vi aggiungono voci in init python), le attività,
# il loop del semestre e la screen di pianificazione.

init -10 python:
    from capitoli.malandrini import calendario_logic as cl
    from capitoli.malandrini import routing_logic as rl
    from capitoli.malandrini import relazioni_logic as rlz

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

    # Hook chiamati con gli id degli inviti a scadenza lasciati cadere.
    cal_inviti_ignorati_hooks = []

    # Attivita' ripetibili senza pool: id -> label giocato ogni volta.
    ATTIVITA_RIPETIBILI = {}

    # Riga mostrata quando il pool di un'attivita' senza personaggio e'
    # esaurito (i territori usano CAL_FALLBACK_AFF).
    CAL_FALLBACK = {
        "studio": "Pagine, stemmi, date. La storia della Famiglia non finisce mai; la mia pazienza sì.",
        "studio_p": "Pagine, stemmi, date. La storia della Famiglia non finisce mai; la mia pazienza sì.",
        "riti": "Brodo, cucine, voci. Il Ceppo gira anche senza di me. Ma gira meglio con me.",
        "citta": "Zefiro d'ordinanza: commissioni, saluti, scorciatoie. Nessuna lama nell'ombra, oggi.",
    }

    # Pool esaurito nel territorio di un personaggio: la riga cambia con
    # l'affinita' (bassa / media / alta, soglie del diario). 0 punti.
    CAL_AFF_VAR = {"aede": "aede_affinity", "caino": "caino_fiducia",
                   "druso": "druso_affinity", "icaro": "icaro_affinity",
                   "ofelia": "ofelia_affinity"}
    CAL_FALLBACK_AFF = {
        "spada": ("aede", 4, 8, (
            "Aede corregge la mia guardia senza guardarmi in faccia. Per lei sono ancora un bersaglio che respira.",
            "Ripresa dopo ripresa. A un certo punto Aede smette di correggermi e comincia a contrattaccare: è una promozione.",
            "Ci alleniamo senza parlare. Lei para, io affondo, e quando sbaglio sorride prima di ricordarsi di non farlo.")),
        "scudo": ("druso", 5, 9, (
            "Druso mi usa come esempio di cosa non fare. Tre volte. Con commento in rima.",
            "Druso mi mette a terra e mi tende la mano nello stesso gesto. Poi la ritira, ovviamente. Poi me la ridà.",
            "«Linguaccia, con me.» Druso mi sceglie come compagno di lotta davanti a tutti. Nessuno osa ridere. Quasi nessuno.")),
        "taverna": ("druso", 5, 9, (
            "Druso declama al tavolo grande. Io bevo a quello piccolo. Nessuno dei due finge di non saperlo.",
            "A metà serata Druso mi dedica un verso osceno. La taverna applaude. Credo sia un onore.",
            "Druso mi tiene il posto accanto al suo, col boccale già pieno. «Il mio pubblico migliore», dice. A voce alta.")),
        "fumeria": ("icaro", 4, 7, (
            "Icaro vince. Io guardo. Lui non guarda me: nel guardarmi non ci sono Scudi da guadagnare.",
            "Icaro sposta il posacenere per farmi spazio. Un gesto minimo. Da lui, un trattato.",
            "Icaro mi passa la pipa senza dire niente, e senza contare quanto ne prendo. Non l'ho mai visto farlo con nessuno.")),
        "registri": ("caino", 6, 10, (
            "Colonne, decime, inchiostro. Caino passa dietro di me senza fermarsi. Per ora sono una penna come le altre.",
            "Caino si ferma alle mie spalle, legge tre righe, ne corregge una. Poi ci ripensa e rimette la mia.",
            "Caino mi lascia il suo calamaio e il suo posto al tavolo grande. «I dettagli», dice. Sa che ricordo il resto.")),
        "corte": ("ofelia", 4, 8, (
            "La serra, i pretendenti in fila. Ofelia ne congeda tre con una frase sola. Io sono il quarto, e alla frase non arrivo nemmeno.",
            "Ofelia mi concede un giro di serra al suo fianco. Non mi parla. Ma non congeda nessuno finché non esco.",
            "Ofelia manda via tutti gli altri prima del tramonto. Restiamo noi, i fiori d'inverno e un silenzio che sembra scelto.")),
    }
    CAL_FALLBACK_AFF["spada_p"] = CAL_FALLBACK_AFF["spada"]

    def cal_fallback_testo(att_id):
        voce = CAL_FALLBACK_AFF.get(att_id)
        if voce is None:
            return CAL_FALLBACK.get(att_id, "La giornata passa come tante: fatica, abitudine, il Nord che non chiede niente.")
        char, media, alta, righe = voce
        aff = getattr(store, CAL_AFF_VAR[char], 0)
        if char in store.congelate or aff < media:
            return righe[0]
        return righe[2] if aff >= alta else righe[1]

    def cal_vars():
        """Dict passato alle cond degli eventi."""
        v = {
            "aede_affinity": store.aede_affinity,
            "caino_fiducia": getattr(store, "caino_fiducia", 0),
            "druso_affinity": store.druso_affinity,
            "icaro_affinity": store.icaro_affinity,
            "ofelia_affinity": store.ofelia_affinity,
            "ofelia_mancati": store.ofelia_mancati,
            "route_seconda": store.route_seconda,
            "aede_sospetto": store.aede_sospetto,
            "congelate": store.congelate,
            "player_gender": store.player_gender,
            "route_attiva": store.route_attiva,
            "flag_accetta_lavoro": store.flag_accetta_lavoro,
            "flag_giuramento": store.flag_giuramento,
            "scudi": store.scudi,
            "dono_tenuto": store.dono_tenuto,
            "visti": store.eventi_visti,
            "luna": CAL_SEQUENZA[min(store.cal_idx, len(CAL_SEQUENZA) - 1)][0],
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
                        and e.get("giorno") == num
                        and cl._cond_ok(e, cal_vars()) for e in EVENTI)
            out.append((num, stato, fisso))
        return out

    def cal_giorno_segnato(luna, giorno):
        """Il giorno ha un evento fisso con cond vera (il ◆ di cal_strip)."""
        return any(f for n, _s, f in cal_strip(luna, giorno) if n == giorno)

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
        "corte": "La serra, i pretendenti, e lei che sceglie.",
    }

    # Diario del semestre: stato diegetico, mai numeri.
    def diario_data():
        if store.cal_idx < len(CAL_SEQUENZA):
            l, g, s = CAL_SEQUENZA[store.cal_idx]
            return "%s — giorno %d, %s" % (LUNE_NOMI[l], g, s)
        return "Semestre concluso"

    def diario_eventi_contati():
        return sum(1 for e in EVENTI if e["id"] in store.eventi_visti)

    def diario_borsa():
        riga = "Borsa: %d Scudi" % store.scudi
        if store.dono_tenuto:
            riga += " — in borsa, %s" % DONI[store.dono_tenuto][0]
        return riga

    def diario_rapporti():
        righe = []

        def riga(nome, char, aff, soglie, segnale=None):
            alta, media, bassa = soglie
            if char in store.congelate:
                righe.append((nome, "Una porta chiusa. Da dentro."))
            elif segnale:
                righe.append((nome, segnale))
            elif store.route_attiva == char:
                righe.append((nome, alta[1]))
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
              (1, "Ti squadra come un bersaglio mobile.")),
             "Ti guarda come si guarda un conto che non torna."
             if store.route_seconda == "aede" and store.aede_sospetto >= 1
             else None)
        if "adunanza" in store.eventi_visti:
            riga("Caino", "caino", getattr(store, "caino_fiducia", 0),
                 ((10, "Ti versa l'idromele senza chiedere."),
                  (6, "Ricorda il tuo nome. E tu ricordi i suoi dettagli."),
                  (2, "Ti osserva come una moneta trovata per terra.")))
        riga("Druso", "druso", store.druso_affinity,
             ((9, "Ti chiama «linguaccia» davanti a tutti. È affetto."),
              (5, "Ti dedica i versi peggiori. Buon segno."),
              (1, "Ti punzecchia per capire se abbai o mordi.")),
             "Ti ha segnato nel registro delle cose che non perdona. Una riga sola. Per ora."
             if store.player_gender == "m" and store.druso_passi_falsi == 1
             else None)
        riga("Icaro", "icaro", store.icaro_affinity,
             ((7, "Ti lascia guardare le sue mani. Sa che vedi."),
              (4, "Non ti conta più tra i passivi."),
              (1, "Ti tollera al tavolo piccolo.")))
        riga("Ofelia", "ofelia", store.ofelia_affinity,
             ((8, "Ti concede un ballo che rifiuta a tutti. Non lo dirà mai."),
              (4, "Ricorda il tuo nome. Lo usa come una lama."),
              (1, "Ti conta tra i pretendenti. In fondo alla fila.")),
             "Ha aspettato una volta. Non aspetterà la seconda."
             if store.ofelia_mancati == 1 else None)
        return righe

    # Pannello del pianificatore: nomi, righe degli inviti, ritratto grande
    # (lo sprite del cast del menu, se c'e').
    CAL_NOMI = {"aede": "Aede", "caino": "Caino", "ofelia": "Ofelia",
                "druso": "Druso", "icaro": "Icaro"}
    # Comprimari che possono invitare (ritratto degli inviti senza route).
    CAL_NOMI_COMPRIMARI = {"vanna": "Vanna", "corrado": "Corrado",
                           "briseide": "Briseide"}
    # Testi degli avvisi sugli inviti (cal_inviti_info): riga compatta,
    # riga piena, pannello di dettaglio.
    CAL_AVVISI = {
        "scade": ("Solo adesso", "Solo adesso",
                  "Solo adesso: se scegli altro, l'invito cade."),
        "gelosia": ("Icaro lo saprà", "Icaro se ne accorgerà",
                    "Icaro se ne accorgerà: accettare chiude la sua strada."),
        "cuore": ("Fino al cuore", "Fino alla scelta del cuore",
                  "Dopo la scelta del cuore, forse non tornerà."),
    }
    CAL_INVITO_DESC = {
        "aede": "Aede non chiede mai due volte. Questa conta come una.",
        "caino": "Caino ti vuole dove può vederti. Ha le sue ragioni.",
        "ofelia": "Ofelia sceglie chi invitare. Oggi ha scelto te.",
        "druso": "Druso ti cerca a voce alta. Mezza Dignitas lo sa già.",
        "icaro": "Icaro non invita: lascia una porta socchiusa.",
    }

    # Salvataggi: la route attiva finisce nel json dello slot, cosi'
    # file_slots mostra il ritratto (FileJson(slot, "route")).
    def cal_json_route(d):
        d["route"] = getattr(store, "route_attiva", None)

    config.save_json_callbacks.append(cal_json_route)

    def cal_ritratto_grande(char):
        p = "gui/cast_%s.webp" % char if char else None
        return p if p and renpy.loadable(p) else cal_portrait(char)

    def cal_portrait(char):
        p = "gui/malandrini/portrait_%s.png" % char if char else "gui/malandrini/portrait_locked.png"
        return p if renpy.loadable(p) else "gui/malandrini/portrait_locked.png"

    def cal_azione(touch, sel, info, ritorno):
        """Azione di una voce del pianificatore. Col mouse sceglie subito
        (l'anteprima la da' l'hover); su touch il primo tocco seleziona e il
        secondo sulla stessa voce conferma."""
        if not touch or (sel is not None and sel[0] == info):
            return Return(ritorno)
        return SetScreenVariable("cal_sel", (info, ritorno))

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
        # A route attiva, gli inviti degli altri personaggi scalano a sfondo
        # (nel poliamore con Ofelia passano anche quelli della seconda).
        if store.route_attiva is not None:
            evs = [e for e in evs
                   if e.get("char") in (None, store.route_attiva,
                                        store.route_seconda)]
        # avviso: "scade" (cade se scegli altro), "gelosia" (accettarlo
        # chiude Icaro), "cuore" (Luna IV: dopo la scelta del cuore forse non
        # torna), False; solo per la screen (testi in CAL_AVVISI).
        # ritratto: chi mostrare (i comprimari senza route hanno char None).
        def _avviso(e):
            if e.get("scade"):
                return "scade"
            if icaro_gelosia_armata(e):
                return "gelosia"
            if momento[0] == 4 and e.get("char"):
                return "cuore"
            return False
        return [{"id": e["id"], "char": e.get("char"),
                 "ritratto": e.get("ritratto", e.get("char")),
                 "titolo": e.get("titolo", "Qualcuno ti cerca"),
                 "scade": bool(e.get("scade", False)),
                 "avviso": _avviso(e)} for e in evs]

    def cal_dopo_evento(eid):
        ev = cal_evento_di(eid)
        for hook in cal_post_evento_hooks:
            hook(ev)

default cal_idx = 0
default cal_ultimo_giorno = None
default cal_giorno_prima = (None, None)
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
        # (giorno, luna) di prima per il cartello: il numero gira, la luna
        # cambia fase al primo giorno di una Luna nuova.
        $ cal_giorno_prima = ((cal_ultimo_giorno[1], cal_ultimo_giorno[0])
                              if cal_ultimo_giorno else (None, None))
        $ cal_ultimo_giorno = (cal_luna, cal_giorno)
        $ save_name = LUNE_NOMI[cal_luna] + " — giorno " + str(cal_giorno)
        call screen cartello_data(cal_luna, cal_giorno, cal_giorno_segnato(cal_luna, cal_giorno), *cal_giorno_prima)
        # Voce di cronologia per il separatore di giorno (come il vecchio centered).
        $ narrator.add_history("adv", None, save_name)

    $ cal_fisso_id = cal_trova_fisso_id((cal_luna, cal_giorno, cal_slot))

    if cal_fisso_id is not None:
        $ eventi_visti.add(cal_fisso_id)
        # Contesto delle scelte registrate (conseguenze.rpy).
        $ cal_contesto = cal_fisso_id
        call expression cal_label_di(cal_fisso_id)
        $ cal_dopo_evento(cal_fisso_id)
        $ cal_contesto = "fuori"
        jump cal_avanza

    python:
        cal_inviti = cal_inviti_info((cal_luna, cal_giorno, cal_slot))
        # Inviti offerti almeno una volta (per invito_perso, conseguenze.rpy).
        inviti_mostrati.update(i["id"] for i in cal_inviti)
        # Una voce attivita' puo' avere una cond opzionale come quinto campo.
        cal_att = [a[:4] for a in ATTIVITA.get(cal_slot, [])
                   if len(a) < 5 or a[4](cal_vars())]

    if not cal_inviti and not cal_att:
        jump cal_avanza

    # La pergamena si srotola (screen pianificazione); da ferma, dissolvenza.
    if mm_movimento_ridotto() or renpy.is_skipping():
        $ renpy.transition(Dissolve(0.2))
    else:
        play audio "audio/carta.ogg"
    call screen pianificazione((cal_luna, cal_giorno, cal_slot), cal_inviti, cal_att)

    python:
        scelto = _return[1] if _return[0] == "evento" else None
        ign = cl.inviti_ignorati(cal_inviti, scelto)
        if ign:
            for hook in cal_inviti_ignorati_hooks:
                hook(ign)

    if _return[0] == "evento":
        python:
            cal_sel_id = _return[1]
            eventi_visti.add(cal_sel_id)
            cal_contesto = cal_sel_id
        call expression cal_label_di(cal_sel_id)
        $ cal_dopo_evento(cal_sel_id)
        $ cal_contesto = "fuori"
        # Dono in borsa: si offre alla fine dell'invito del personaggio.
        $ cal_sel_char = cal_evento_di(cal_sel_id).get("char")
        if cal_sel_char:
            call dono_check(cal_sel_char)
    else:
        call cal_attivita(_return[1])

    jump cal_avanza

label cal_avanza:
    $ cal_idx += 1
    jump cal_loop

label cal_attivita(att_id):
    $ cal_contesto = att_id
    if att_id in ATTIVITA_RIPETIBILI:
        call expression ATTIVITA_RIPETIBILI[att_id]
        $ cal_contesto = "fuori"
        return
    python:
        cal_pool = None
        cal_att_char = None
        for slot_att in ATTIVITA.values():
            for voce in slot_att:
                if voce[0] == att_id:
                    cal_pool = voce[3]
                    cal_att_char = voce[2]
        cal_label = cl.pesca_variante(cal_pool or [], eventi_visti)
        # Commissioni: oltre al pool, gli eventi casuali (economia.rpy).
        if att_id == "citta":
            cal_label = eco_pesca_citta(cal_label)
    if cal_label is None:
        $ cal_fallback_txt = cal_fallback_testo(att_id)
        "[cal_fallback_txt]"
    else:
        $ eventi_visti.add(cal_label)
        $ cal_contesto = cal_label
        call expression cal_label
    # Fatti nuovi, poi al massimo un eco di una scelta passata (conseguenze.rpy).
    $ conseguenze_aggiorna()
    $ cal_eco = echi_pesca(att_id)
    if cal_eco is not None:
        $ echi_visti.add(cal_eco)
        call expression echi_label(cal_eco)
    $ cal_contesto = "fuori"
    # Paghe, giro alla taverna, dono al personaggio del territorio.
    call eco_dopo_attivita(att_id, cal_att_char)
    return

label cal_fine_semestre:
    # Rete di sicurezza: se la sequenza finisce senza che Luna VI abbia
    # chiuso il semestre, chiude il finale neutro.
    if not semestre_concluso:
        call finale_neutro_semestre
    return


## Cartello di data ##########################################################
# A ogni cambio di giorno: pergamena che si srotola, Luna e giorno, ◆ se il
# giorno ha un evento fisso. Click o ~2.5 s per proseguire.

transform cartello_srotola:
    align (0.5, 0.42)
    alpha 0.0 xzoom 0.06
    easein 0.15 alpha 1.0
    easein_quart 0.45 xzoom 1.0

transform cartello_fermo:
    align (0.5, 0.42)

transform cartello_testo_fermo:
    alpha 1.0

transform cartello_testo:
    alpha 0.0
    pause 0.5
    linear 0.35 alpha 1.0

# Sigillo di ceralacca: cade sul bordo basso dopo il testo (~0.9 s), con un
# piccolo rimbalzo; rosso nei giorni segnati, bruno negli altri. Cade
# accelerando (easeout, in ATL) e rimbalza frenando (easein).
transform cartello_sigillo:
    align (0.5, 1.0) yoffset 78
    alpha 0.0 zoom 1.12
    pause 0.9
    easeout 0.18 alpha 1.0 zoom 0.66
    easein 0.1 zoom 0.7

# Numero del giorno che gira: il vecchio sale e sparisce, il nuovo sale dal
# basso, mentre il testo compare (pause 0.5 come cartello_testo).
transform giorno_esce:
    alpha 1.0 yoffset 0
    pause 0.55
    easeout 0.35 alpha 0.0 yoffset -24

transform giorno_entra:
    alpha 0.0 yoffset 24
    pause 0.55
    easein_quart 0.3 alpha 1.0 yoffset 0

# Primo giorno di una Luna nuova: la luna di prima sfuma nella nuova, con un
# piccolo bagliore oro.
transform luna_esce:
    align (0.5, 0.0) yoffset -64
    alpha 1.0
    pause 0.5
    linear 0.6 alpha 0.0

transform luna_entra:
    align (0.5, 0.0) yoffset -64
    alpha 0.0 zoom 0.9
    pause 0.5
    easein_quart 0.5 alpha 1.0 zoom 1.0
    matrixcolor BrightnessMatrix(0.25)
    linear 0.5 matrixcolor BrightnessMatrix(0.0)

transform luna_ferma:
    align (0.5, 0.0) yoffset -64

transform cartello_sigillo_fermo:
    align (0.5, 1.0) yoffset 78
    zoom 0.7

screen cartello_data(luna, giorno, festa=False, giorno_prec=None, luna_prec=None):

    modal True

    # Click (o tasto) per proseguire; in skip passa subito.
    key "dismiss" action Return()
    button:
        xysize (1920, 1080)
        background None
        action Return()
    timer (0.05 if config.skipping else 2.5) action Return()
    if not (config.skipping or mm_movimento_ridotto()):
        timer 1.08 action Play("audio", "audio/sigillo.ogg")

    default cartello_anim = not (config.skipping or mm_movimento_ridotto())
    fixed:
        xysize (760, 210)
        at (cartello_fermo if mm_movimento_ridotto() else cartello_srotola)
        add "gui/malandrini/cartello_data.png"
        vbox:
            align (0.5, 0.5)
            spacing 2
            at (cartello_testo_fermo if mm_movimento_ridotto() else cartello_testo)
            text LUNE_NOMI[luna]:
                xalign 0.5
                font gui.name_text_font
                size 58
                color "#4a1010"
            hbox:
                xalign 0.5
                spacing 14
                if festa:
                    text "◆" size 22 color "#c0392b" yalign 0.5
                hbox:
                    spacing 8
                    yalign 0.5
                    text "giorno" style "cartello_numero" yalign 0.5
                    if cartello_anim and giorno_prec is not None and giorno_prec != giorno:
                        fixed:
                            fit_first True
                            yalign 0.5
                            text str(giorno) style "cartello_numero" at giorno_entra
                            text str(giorno_prec) style "cartello_numero" at giorno_esce
                    else:
                        text str(giorno) style "cartello_numero" yalign 0.5
                if festa:
                    text "◆" size 22 color "#c0392b" yalign 0.5
        if luna_prec is not None and luna_prec != luna:
            if cartello_anim:
                add ("gui/malandrini/luna_%d.png" % luna_prec) at luna_esce
                add ("gui/malandrini/luna_%d.png" % luna) at luna_entra
            else:
                add ("gui/malandrini/luna_%d.png" % luna) at luna_ferma
        add ("gui/malandrini/ceralacca_festa.png" if festa else "gui/ceralacca.png"):
            at (cartello_sigillo_fermo if (mm_movimento_ridotto() or config.skipping) else cartello_sigillo)


## Screen di pianificazione ##################################################

screen pianificazione(momento, inviti, attivita):

    modal True

    ## Su touch non c'e' hover: il primo tocco seleziona la voce e riempie il
    ## pannello, il secondo tocco (o "Scegli" nel pannello) la conferma.
    ## cal_sel = (tooltip, valore di ritorno) della voce selezionata.
    default cal_sel = None
    $ cal_touch = renpy.variant("touch")

    ## Pergamena che si srotola dall'alto, poi colonne e voci in cascata.
    ## Ferma con "Animazioni: No" o in skip.
    default pian_fermo = mm_movimento_ridotto() or renpy.is_skipping()

    add "gui/game_menu.png" at (pian_fisso if pian_fermo else pian_srotola)

    ## Colonna delle scelte a sinistra, pannello del personaggio a destra
    ## (si riempie all'hover via tooltip, o alla selezione su touch).
    vbox:
        at (pian_fisso if pian_fermo else pian_contenuto)
        xpos 120
        yalign 0.5
        spacing 12
        xsize 1060

        add "gui/divisore.png" xalign 0.5
        hbox:
            xalign 0.5
            spacing 18
            add ("gui/malandrini/luna_%d.png" % momento[0]) yalign 0.5 zoom 0.7
            label LUNE_NOMI[momento[0]] text_size 42 text_color gui.accent_color yalign 0.5

        # Striscia dei giorni salienti della Luna: ◆ = festa o evento segnato.
        hbox:
            xalign 0.5
            spacing 30
            for num, stato, fisso in cal_strip(momento[0], momento[1]):
                vbox:
                    spacing 0
                    xminimum 46
                    text ("◆" if fisso else " ") size 14 xalign 0.5 color "#f0c75e"
                    text str(num) size 26 xalign 0.5 bold (stato == "oggi") color ("#f0c75e" if stato == "oggi" else "#8a7a5a" if stato == "passato" else "#c9b78a")

        # Slot del giorno (dove siamo arrivati). Gli Scudi stanno nella borsa
        # a schermo (borsa.rpy).
        hbox:
            xalign 0.5
            spacing 24
            for nome_s, stato_s in cal_slot_stati(momento):
                text nome_s.capitalize() size 22 italic (stato_s == "corrente") color ("#f0e6d2" if stato_s == "corrente" else "#8a7a5a" if stato_s == "passato" else "#a89468") yalign 0.5

        add "gui/divisore.png" xalign 0.5

        ## Inviti e attivita': fino a 7 attivita' piu' gli inviti nel
        ## pomeriggio. Il viewport si stringe sul contenuto e scorre (barra
        ## miniata, nascosta se non serve) solo quando non ci sta. Con piu'
        ## di 6 voci le righe si compattano: titolo e sottotitolo su una riga.
        $ cal_compatto = len(inviti) + len(attivita) > 6
        ## Righe alte (~1 cm su telefono): con 6 voci stanno ancora tutte
        ## tra il cartello e il menu rapido senza scorrere.
        $ PIAN_RIGA_H = 96
        viewport:
            id "cal_lista"
            xsize 1060
            ymaximum 680
            scrollbars "vertical"
            vscrollbar_unscrollable "hide"
            side_spacing 12
            mousewheel True
            draggable True

            vbox:
                spacing (8 if cal_compatto else 10)
                xfill True

                for k, inv in enumerate(inviti):
                    $ cal_info = ("invito", inv["ritratto"], inv["titolo"], inv["avviso"])
                    button:
                        at (pian_fisso if pian_fermo else pian_voce(0.3 + 0.04 * k))
                        xfill True
                        yminimum (66 if cal_compatto else PIAN_RIGA_H)
                        ypadding (8 if cal_compatto else 14)
                        left_padding 26
                        right_padding 26
                        background Frame("gui/button/piano_idle_background.png", 26, 26)
                        hover_background Frame("gui/button/piano_hover_background.png", 26, 26)
                        selected_background Frame("gui/button/piano_hover_background.png", 26, 26)
                        tooltip cal_info
                        selected (cal_touch and cal_sel is not None and cal_sel[0] == cal_info)
                        action cal_azione(cal_touch, cal_sel, cal_info, ("evento", inv["id"]))
                        hbox:
                            spacing 18
                            add Transform(cal_portrait(inv["ritratto"]), zoom=0.36) yalign 0.5
                            if cal_compatto:
                                hbox:
                                    yalign 0.5
                                    spacing 16
                                    text inv["titolo"] size 25 color "#f5e3b8" yalign 0.5
                                    if inv["avviso"]:
                                        fixed:
                                            xysize (26, 26)
                                            yalign 0.5
                                            add "gui/malandrini/clessidra.png" at (clessidra_ferma if mm_movimento_ridotto() else clessidra_gira)
                                        text CAL_AVVISI[inv["avviso"]][0] size TESTO_MINUTO color "#d9a441" yalign 0.5
                            else:
                                vbox:
                                  yalign 0.5
                                  text inv["titolo"] size 28 color "#f5e3b8"
                                  if inv["avviso"]:
                                      hbox:
                                          spacing 8
                                          fixed:
                                              xysize (26, 26)
                                              yalign 0.5
                                              add "gui/malandrini/clessidra.png" at (clessidra_ferma if mm_movimento_ridotto() else clessidra_gira)
                                          text CAL_AVVISI[inv["avviso"]][1] size TESTO_MINUTO color "#d9a441" yalign 0.5

                for k, (aid, etichetta, char, _pool) in enumerate(attivita):
                    $ cal_info = ("attivita", char, etichetta, aid)
                    button:
                        at (pian_fisso if pian_fermo else pian_voce(0.3 + 0.04 * (len(inviti) + k)))
                        xfill True
                        yminimum (66 if cal_compatto else PIAN_RIGA_H)
                        ypadding (8 if cal_compatto else 14)
                        left_padding 26
                        right_padding 26
                        background Frame("gui/button/piano_idle_background.png", 26, 26)
                        hover_background Frame("gui/button/piano_hover_background.png", 26, 26)
                        selected_background Frame("gui/button/piano_hover_background.png", 26, 26)
                        tooltip cal_info
                        selected (cal_touch and cal_sel is not None and cal_sel[0] == cal_info)
                        action cal_azione(cal_touch, cal_sel, cal_info, ("att", aid))
                        hbox:
                            spacing 18
                            if char:
                                add Transform(cal_portrait(char), zoom=0.36) yalign 0.5
                            else:
                                null width 58
                            if cal_compatto:
                                hbox:
                                    yalign 0.5
                                    spacing 18
                                    text etichetta size 25 color "#f0e6d2" yalign 1.0
                                    if aid in ATTIVITA_DESC:
                                        text ATTIVITA_DESC[aid] size TESTO_MINUTO color "#8f7f5c" yalign 1.0 yoffset -3
                            else:
                                vbox:
                                  yalign 0.5
                                  spacing 4
                                  text etichetta size 28 color "#f0e6d2"
                                  if aid in ATTIVITA_DESC:
                                      text ATTIVITA_DESC[aid] size TESTO_MINUTO color "#8f7f5c"

    ## Pannello laterale.
    $ cal_tt = cal_sel[0] if (cal_touch and cal_sel) else GetTooltip("pianificazione")
    ## Su touch il ritratto cede spazio al bottone "Scegli".
    $ cal_ritratto_h = 380 if cal_touch else 470
    frame:
        style "cal_pannello"
        at (pian_fisso if pian_fermo else pian_contenuto)
        if cal_tt:
            $ cal_tipo, cal_chr, cal_titolo, cal_extra = cal_tt
            vbox:
                at cal_pannello_in
                spacing 12
                xfill True
                fixed:
                    xysize (480, cal_ritratto_h)
                    if cal_chr:
                        add cal_ritratto_grande(cal_chr):
                            fit "contain"
                            xysize (480, cal_ritratto_h)
                            align (0.5, 1.0)
                    else:
                        ## Attività senza personaggio: la luna del mese.
                        add ("gui/malandrini/luna_%d.png" % momento[0]) align (0.5, 0.6) zoom 1.5
                text CAL_NOMI.get(cal_chr, CAL_NOMI_COMPRIMARI.get(cal_chr, "Il semestre")) style "cal_pannello_nome"
                text cal_titolo style "cal_pannello_titolo"
                if cal_tipo == "invito":
                    text CAL_INVITO_DESC.get(cal_chr, "Qualcuno ti cerca. Non dice perché.") style "cal_pannello_testo"
                    if cal_extra:
                        hbox:
                            spacing 10
                            fixed:
                                xysize (30, 30)
                                yalign 0.5
                                add "gui/malandrini/clessidra.png" at (clessidra_ferma if mm_movimento_ridotto() else clessidra_gira)
                            text CAL_AVVISI[cal_extra][2] style "cal_pannello_avviso" yalign 0.5
                else:
                    text ATTIVITA_DESC.get(cal_extra, "") style "cal_pannello_testo"
            if cal_touch and cal_sel:
                button:
                    style "cal_scegli"
                    action Return(cal_sel[1])
                    text "Scegli" style "cal_scegli_text"
        else:
            vbox:
                align (0.5, 0.5)
                spacing 16
                add ("gui/malandrini/luna_%d.png" % momento[0]) xalign 0.5
                text "Come spendi questo tempo?" style "cal_pannello_titolo" xalign 0.5 textalign 0.5
                if cal_touch:
                    text "Tocca una voce per leggerla, toccala di nuovo per sceglierla." style "cal_pannello_testo" xalign 0.5 textalign 0.5


## Clessidra degli inviti a scadenza: si capovolge a intervalli.
transform clessidra_ferma:
    align (0.5, 0.5)
    zoom 0.6

transform clessidra_gira:
    align (0.5, 0.5)
    zoom 0.6
    rotate 0
    block:
        pause 1.1
        ease 0.45 rotate 180
        pause 1.1
        ease 0.45 rotate 360
        rotate 0
        repeat

transform pian_fisso:
    alpha 1.0

transform pian_srotola:
    on show:
        yanchor 0.0 ypos 0 yzoom 0.04 alpha 0.5
        easein 0.35 yzoom 1.0 alpha 1.0
    on hide:
        easeout 0.2 yzoom 0.04 alpha 0.0

transform pian_contenuto:
    on show:
        alpha 0.0
        pause 0.25
        ease 0.2 alpha 1.0
    on hide:
        ease 0.15 alpha 0.0

transform pian_voce(ritardo):
    alpha 0.0 xoffset -14
    pause ritardo
    ease 0.18 alpha 1.0 xoffset 0

transform cal_pannello_in:
    alpha 0.0 xoffset 14
    ease 0.18 alpha 1.0 xoffset 0

style cal_pannello is empty
style cal_pannello:
    xpos 1240
    yalign 0.5
    xsize 580
    ysize 860
    background Frame("gui/frame.png", 60, 60)
    padding (50, 44, 50, 44)

style cal_pannello_nome is text:
    font gui.name_text_font
    size 38
    color gui.accent_color

style cal_pannello_titolo is text:
    font gui.text_font
    size 27
    color "#f5e3b8"

style cal_pannello_testo is text:
    font gui.text_font
    size 23
    italic True
    color "#c9b78a"

style cal_pannello_avviso is text:
    font gui.text_font
    size 21
    color "#e0b75a"

style cal_scegli is button:
    xalign 0.5
    yalign 1.0
    xminimum 260
    padding (40, 14, 40, 14)
    background Frame("gui/button/piano_idle_background.png", 26, 26)
    hover_background Frame("gui/button/piano_hover_background.png", 26, 26)

style cal_scegli_text is text:
    font gui.interface_text_font
    size 30
    xalign 0.5
    color gui.accent_color
    hover_color "#f5e3b8"


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

            text diario_borsa() size 22 color "#8f7f5c"

            null height 10

            hbox:
                spacing 12
                textbutton _("Apri le Cronache"):
                    style "cronache_tab"
                    text_style "cronache_tab_text"
                    action ShowMenu("cronache")
                textbutton _("Apri la Trama"):
                    style "cronache_tab"
                    text_style "cronache_tab_text"
                    action ShowMenu("trama")
                textbutton _("Apri la Borsa"):
                    style "cronache_tab"
                    text_style "cronache_tab_text"
                    action ShowMenu("inventario")


style cartello_numero is text
style cartello_numero:
    font gui.text_font
    size 32
    italic True
    color "#5a4426"
