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
            # III/10: il torneo è di pomeriggio; mattina e sera restano
            # libere (la Luna III ha sei fissi, senza mattine libere era strozzata).
            {"giorno": 10, "slots": ["mattina", "pomeriggio", "sera"]},
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
        "ceppo_sera": "Il focolare, le scodelle, Vanna che parla sopra a tutti. Una sera di casa, niente di più.",
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
        "ceppo_sera": "Il focolare di Briseide. Vanna, Corrado, i Figli piccoli.",
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
                # Dopo la scelta del cuore: quanto manca al finale buono,
                # in tre gradini (routing_logic.progresso_route).
                righe.append((nome, DIARIO_PROGRESSO[char][rl.progresso_route(char, aff)]))
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

    # Diario a route attiva: lontano / vicino / raggiunto il finale buono.
    DIARIO_PROGRESSO = {
        "aede": ("Ti ha scelto. Non si fida ancora della scelta.",
                 "Abbassa la guardia con te. Solo con te, e solo un poco.",
                 "Ti guarda le spalle senza che tu lo chieda. Il Nord lo chiama giuramento."),
        "caino": ("Ti tiene vicino. Vicino non vuol dire dentro.",
                  "Ti lascia leggere i registri che non mostra a nessuno.",
                  "Ti affiderebbe la Proprietà. E qualcosa di più fragile."),
        "druso": ("Ti dedica i versi buoni. Gli altri li tiene per la piazza.",
                  "Smette di recitare quando arrivi. È la cosa più vera che fa.",
                  "Ha scritto un verso che non legge a nessuno. Parla di te."),
        "icaro": ("Ti ha fatto posto al tavolo. Non ancora nelle sue carte.",
                  "Ti mostra una mano prima di giocarla. Non lo fa con nessuno.",
                  "Ha smesso di contare quello che gli devi. Conta i giorni senza di te."),
        "ofelia": ("Ti ha scelto davanti alla serra. Aspetta di vedere se reggi.",
                   "Ti chiama per nome quando nessuno ascolta.",
                   "Ha congedato l'ultimo pretendente. Non ti dice perché. Non serve."),
    }

    def cal_rapporto_di(char):
        """La riga del Diario per char (pannello del pianificatore), o None."""
        nome = CAL_NOMI.get(char)
        for n, r in diario_rapporti():
            if n == nome:
                return r
        return None

    # Cosa rende o costa un'attivita' (etichetta a destra della voce):
    # stringa o funzione senza argomenti (economia.rpy aggiunge le sue).
    ATTIVITA_PAGA = {}
    # Riga in piu' nel pannello (es. la condizione del mercato).
    ATTIVITA_NOTA = {}

    def cal_paga(aid):
        p = ATTIVITA_PAGA.get(aid)
        return p() if callable(p) else p

    # Territori senza niente di nuovo (pool finito, nessun eco pronto). Le
    # commissioni hanno i casi, i ripetibili non hanno pool: mai esauriti.
    def cal_esauriti_di(attivita):
        return set(aid for aid, _e, _c, pool in attivita
                   if aid != "citta" and aid not in ATTIVITA_RIPETIBILI
                   and cl.territorio_esaurito(pool, store.eventi_visti,
                                              echi_pesca(aid) is not None))

    # Lune V-VI: slot senza fisso, senza inviti e con soli territori esauriti
    # non esistono (spec del calendario: i giorni vuoti non si mostrano).
    CAL_SEMPRE_VIVE = ("citta", "mercato")

    def cal_att_visibili(slot):
        return [a[:4] for a in ATTIVITA.get(slot, [])
                if len(a) < 5 or a[4](cal_vars())]

    def cal_slot_da_saltare(momento):
        if momento[0] < 5 or "scelta_cuore" not in store.eventi_visti:
            return False
        att = cal_att_visibili(momento[2])
        return cl.slot_da_saltare(
            momento[0], True, cal_trova_fisso_id(momento),
            cal_inviti_info(momento), [a[0] for a in att], cal_esauriti_di(att),
            CAL_SEMPRE_VIVE, store.dono_tenuto is not None)

    # Conto alla rovescia (da Luna III) verso la scelta del cuore, IV/28:
    # giorni salienti, non di calendario. None = non mostrarlo.
    def cal_cuore_mancano():
        if store.cal_idx >= len(CAL_SEQUENZA) or CAL_SEQUENZA[store.cal_idx][0] < 3:
            return None
        if "scelta_cuore" in store.eventi_visti:
            return None
        n = cl.momenti_fino_a(CAL_SEQUENZA, store.cal_idx, 4, 28)
        if n is None:
            return None
        if n == 0:
            return "Stasera, la scelta del cuore."
        if n == 1:
            return "Alla scelta del cuore: solo oggi."
        return "Alla scelta del cuore: %d giorni." % n

    # Riepilogo a cambio di Luna (cartello): i luoghi piu' frequentati
    # nella Luna passata e, se sono nati fatti, un rimando alla Trama.
    CAL_LUOGHI = {"spada": "cortile d'armi", "spada_p": "cortile d'armi",
                  "scudo": "palestra", "studio": "libri", "studio_p": "libri",
                  "riti": "cucine", "citta": "vicoli", "registri": "registri",
                  "taverna": "taverna", "fumeria": "fumeria",
                  "corte": "serra", "mercato": "mercato",
                  "ceppo_sera": "focolare"}

    def cal_conta_attivita(att_id):
        luoghi = store.cal_frequenze.setdefault(store.cal_luna, {})
        luoghi[att_id] = luoghi.get(att_id, 0) + 1

    def cal_riepilogo_luna(luna):
        riga = cl.riepilogo_luna(store.cal_frequenze.get(luna, {}), CAL_LUOGHI)
        idx_luna = set(i for i, m in enumerate(CAL_SEQUENZA) if m[0] == luna)
        nati = any(isinstance(n, tuple) and len(n) > 1 and n[1] in idx_luna
                   for n in store.fatti_noti.values())
        if nati:
            riga = (riga + " " if riga else "") + "Qualcuno se ne ricorderà — Trama."
        return riga

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
        "cuore": ("Fino a Luna IV, giorno 28", "Fino alla Luna IV, giorno 28",
                  "Resta fino alla scelta del cuore (Luna IV, giorno 28). Dopo, forse non tornerà."),
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
# Ultima variante pescata da cal_attivita (None = pool esaurito).
default cal_label = None
# Vero mentre il loop salta slot vuoti di Lune V-VI (una riga sola).
default cal_saltando = False
# Attivita' giocate per Luna (riepilogo del cartello): luna -> {id: volte}.
default cal_frequenze = {}
default cal_riepilogo = None
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

    # Lune V-VI: lo slot vuoto si salta (e il giorno vuoto, cartello
    # compreso); una riga sola per ogni tratto saltato.
    if cal_slot_da_saltare((cal_luna, cal_giorno, cal_slot)):
        if not cal_saltando:
            $ cal_saltando = True
            "I giorni passano uguali: allenamenti, cucine, il Nord che non chiede niente."
        jump cal_avanza
    $ cal_saltando = False

    # Riga di data a ogni cambio di giorno + nome del salvataggio.
    if cal_ultimo_giorno != (cal_luna, cal_giorno):
        # (giorno, luna) di prima per il cartello: il numero gira, la luna
        # cambia fase al primo giorno di una Luna nuova.
        $ cal_giorno_prima = ((cal_ultimo_giorno[1], cal_ultimo_giorno[0])
                              if cal_ultimo_giorno else (None, None))
        $ cal_ultimo_giorno = (cal_luna, cal_giorno)
        $ save_name = LUNE_NOMI[cal_luna] + " — giorno " + str(cal_giorno)
        # Primo giorno di una Luna nuova: una riga su quella passata.
        $ cal_riepilogo = (cal_riepilogo_luna(cal_giorno_prima[1])
                           if cal_giorno_prima[1] not in (None, cal_luna) else None)
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
        cal_att = cal_att_visibili(cal_slot)
        # Territori senza niente di nuovo: restano, ma lo dicono.
        cal_esauriti = cal_esauriti_di(cal_att)

    if not cal_inviti and not cal_att:
        jump cal_avanza

    # La pergamena si srotola (screen pianificazione); da ferma, dissolvenza.
    if mm_movimento_ridotto() or renpy.is_skipping():
        $ renpy.transition(Dissolve(0.2))
    else:
        play audio "audio/carta.ogg"
    # Primo pianificatore: la guida sopra (si salta; il "?" la riapre).
    if not persistent.guida_pianificatore:
        $ renpy.show_screen("guida_pianificatore")
    call screen pianificazione((cal_luna, cal_giorno, cal_slot), cal_inviti, cal_att, cal_esauriti)

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
    $ cal_conta_attivita(att_id)
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
    ## Primo giorno di una Luna nuova: riga sulla Luna passata (M10).
    $ cartello_riep = cal_riepilogo if (luna_prec is not None and luna_prec != luna) else None
    timer (0.05 if config.skipping else 4.0 if cartello_riep else 2.5) action Return()
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
                ## Giorno segnato: lo stesso sigillo della striscia dei giorni.
                if festa:
                    add "gui/malandrini/ceralacca_festa.png" zoom 0.14 yalign 0.5
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
                    add "gui/malandrini/ceralacca_festa.png" zoom 0.14 yalign 0.5
        if luna_prec is not None and luna_prec != luna:
            if cartello_anim:
                add ("gui/malandrini/luna_%d.png" % luna_prec) at luna_esce
                add ("gui/malandrini/luna_%d.png" % luna) at luna_entra
            else:
                add ("gui/malandrini/luna_%d.png" % luna) at luna_ferma
        add ("gui/malandrini/ceralacca_festa.png" if festa else "gui/ceralacca.png"):
            at (cartello_sigillo_fermo if (mm_movimento_ridotto() or config.skipping) else cartello_sigillo)
    if cartello_riep:
        frame:
            style "cartello_riepilogo"
            at (cartello_testo_fermo if mm_movimento_ridotto() else cartello_testo)
            text cartello_riep style "cartello_riepilogo_text"


## Screen di pianificazione ##################################################

screen pianificazione(momento, inviti, attivita, esauriti=()):

    modal True

    ## Su touch non c'e' hover: il primo tocco seleziona la voce e riempie il
    ## pannello, il secondo tocco (o "Scegli" nel pannello) la conferma.
    ## cal_sel = (tooltip, valore di ritorno) della voce selezionata.
    default cal_sel = None
    $ cal_touch = renpy.variant("touch")
    ## Telefono: righe alte ~7,5 mm, mai compatte (il viewport scorre).
    $ cal_small = renpy.variant("small")

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
        ## Testata: la Luna al centro, Diario e guida ("?") a destra.
        fixed:
            xsize 1060
            ysize (112 if cal_small else 72)
            hbox:
                align (0.5, 0.5)
                spacing 18
                add ("gui/malandrini/luna_%d.png" % momento[0]) yalign 0.5 zoom 0.7
                label LUNE_NOMI[momento[0]] text_size 42 text_color gui.accent_color yalign 0.5
            hbox:
                align (1.0, 0.5)
                spacing 10
                textbutton _("Diario"):
                    style "cal_testata"
                    text_style "cal_testata_text"
                    alt _("Apri il Diario dei rapporti")
                    action ShowMenu("diario")
                textbutton "?":
                    style "cal_testata"
                    text_style "cal_testata_text"
                    alt _("Guida al pianificatore")
                    action Show("guida_pianificatore")

        # Striscia dei giorni salienti della Luna: il sigillo rosso segna un
        # giorno con un evento fisso (lo stesso del cartello di data).
        hbox:
            xalign 0.5
            spacing 30
            for num, stato, fisso in cal_strip(momento[0], momento[1]):
                vbox:
                    spacing 0
                    xminimum 46
                    if fisso:
                        add "gui/malandrini/ceralacca_festa.png" zoom 0.12 xalign 0.5
                    else:
                        null height 22
                    text str(num) size 26 xalign 0.5 bold (stato == "oggi") color ("#f0c75e" if stato == "oggi" else "#9a8b6c" if stato == "passato" else "#c9b78a")

        # Da Luna III: quanti giorni salienti mancano alla scelta del cuore.
        $ cal_cuore = cal_cuore_mancano()
        if cal_cuore:
            text cal_cuore size TESTO_NOTA italic True color "#e0b75a" xalign 0.5

        # Slot del giorno (dove siamo arrivati). Gli Scudi stanno nella borsa
        # a schermo (borsa.rpy).
        hbox:
            xalign 0.5
            spacing 24
            for nome_s, stato_s in cal_slot_stati(momento):
                text nome_s.capitalize() size 22 italic (stato_s == "corrente") color ("#f0e6d2" if stato_s == "corrente" else "#9a8b6c" if stato_s == "passato" else "#a89468") yalign 0.5

        add "gui/divisore.png" xalign 0.5

        ## Inviti e attivita': fino a 7 attivita' piu' gli inviti nel
        ## pomeriggio. Il viewport si stringe sul contenuto e scorre (barra
        ## miniata, nascosta se non serve) solo quando non ci sta. Con piu'
        ## di 6 voci le righe si compattano: titolo e sottotitolo su una riga.
        ## Su telefono mai compatte: righe da 120 (~7,5 mm) e il viewport
        ## scorre. Su PC, con 6 voci stanno tutte senza scorrere.
        $ cal_compatto = (not cal_small) and len(inviti) + len(attivita) > 6
        $ PIAN_RIGA_H = 120 if cal_small else 96
        viewport:
            id "cal_lista"
            xsize 1060
            ymaximum (620 if cal_small else 680)
            scrollbars "vertical"
            vscrollbar_unscrollable "hide"
            side_spacing 12
            mousewheel True
            draggable True

            vbox:
                spacing (8 if cal_compatto else 14 if cal_small else 10)
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
                        alt (inv["titolo"] + (". " + CAL_AVVISI[inv["avviso"]][1] if inv["avviso"] else ""))
                        hbox:
                            yalign 0.5
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
                    ## Territorio senza niente di nuovo: resta, attenuato.
                    $ cal_vuoto = aid in esauriti
                    $ cal_sotto = ("Il solito. Niente di nuovo, oggi." if cal_vuoto
                                   else ATTIVITA_DESC.get(aid))
                    ## Cosa rende o costa (registri, commissioni, mercato).
                    $ cal_rende = cal_paga(aid)
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
                        alt (etichetta + (". " + cal_sotto if cal_sotto else "") + (". " + cal_rende if cal_rende else ""))
                        ## Al centro la voce, a destra cosa rende o costa.
                        side "c r":
                            xfill True
                            yalign 0.5
                            spacing 12
                            hbox:
                                yalign 0.5
                                spacing 18
                                if char:
                                    add Transform(cal_portrait(char), zoom=0.36) yalign 0.5 alpha (0.6 if cal_vuoto else 1.0)
                                else:
                                    null width 58
                                if cal_compatto:
                                    hbox:
                                        yalign 0.5
                                        spacing 18
                                        text etichetta size 25 color ("#c9bfa8" if cal_vuoto else "#f0e6d2") yalign 1.0
                                        if cal_sotto:
                                            text cal_sotto size TESTO_MINUTO italic cal_vuoto color ("#968a72" if cal_vuoto else "#b3a173") yalign 1.0 yoffset -3
                                else:
                                    vbox:
                                      yalign 0.5
                                      spacing 4
                                      xmaximum 760
                                      text etichetta size 28 color ("#c9bfa8" if cal_vuoto else "#f0e6d2")
                                      if cal_sotto:
                                          text cal_sotto size TESTO_MINUTO italic cal_vuoto color ("#968a72" if cal_vuoto else "#b3a173")
                            if cal_rende:
                                text cal_rende size TESTO_MINUTO italic True color "#e0b75a" yalign 0.5
                            else:
                                null

    ## Pannello laterale.
    $ cal_tt = cal_sel[0] if (cal_touch and cal_sel) else GetTooltip("pianificazione")
    ## Su touch il ritratto cede spazio al bottone "Scegli".
    ## Su telefono, testo piu' grande: il ritratto cede ancora un po'.
    $ cal_ritratto_h = 300 if cal_small else 380 if cal_touch else 470
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
                ## Lo stato del rapporto, come nel Diario (mai numeri).
                $ cal_rapp = cal_rapporto_di(cal_chr) if cal_chr in CAL_NOMI else None
                if cal_rapp:
                    text cal_rapp style "cal_pannello_rapporto"
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
                    if cal_extra in esauriti:
                        text "Il solito. Niente di nuovo, oggi: niente scene, niente punti." style "cal_pannello_testo"
                    else:
                        text ATTIVITA_DESC.get(cal_extra, "") style "cal_pannello_testo"
                    $ cal_rende_p = cal_paga(cal_extra)
                    if cal_rende_p:
                        text cal_rende_p style "cal_pannello_avviso"
                    if cal_extra in ATTIVITA_NOTA:
                        text ATTIVITA_NOTA[cal_extra] style "cal_pannello_testo"
            if cal_touch and cal_sel:
                button:
                    style "cal_scegli"
                    alt _("Scegli questa voce")
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

style cal_scegli:
    variant "small"
    yminimum 112
    xminimum 300

style cal_pannello_rapporto is text:
    font gui.text_font
    size 22
    italic True
    color "#e0b75a"

## Bottoni della testata (Diario, ?).
style cal_testata is button:
    yalign 0.5
    xminimum 64
    padding (20, 8, 20, 8)
    background Frame("gui/button/piano_idle_background.png", 26, 26)
    hover_background Frame("gui/button/piano_hover_background.png", 26, 26)

style cal_testata:
    variant "small"
    xminimum 112
    yminimum 112

style cal_testata_text is text:
    font gui.interface_text_font
    size 24
    xalign 0.5
    yalign 0.5
    color gui.accent_color
    hover_color "#f5e3b8"

style cal_scegli_text is text:
    font gui.interface_text_font
    size 30
    xalign 0.5
    yalign 0.5
    color gui.accent_color
    hover_color "#f5e3b8"


## Guida al pianificatore ####################################################
# Al primo pianificatore (cal_loop la mostra se manca il flag), poi dal "?".
# Quattro schede, si salta in ogni momento.

default persistent.guida_pianificatore = False

init python:
    GUIDA_PIANIFICATORE = [
        ("La giornata",
         "Il semestre salta da un giorno che conta all'altro. Ogni giorno ha "
         "uno, due o tre momenti: mattina, pomeriggio, sera. In ognuno scegli "
         "una voce sola, e il tempo speso non torna."),
        ("Inviti e attività",
         "In cima, gli inviti: qualcuno ti cerca. Sotto, le attività: i "
         "territori dove trovi qualcuno e i lavori che pagano. A destra di "
         "una voce, cosa rende o costa. Un territorio che non ha più niente "
         "di nuovo lo dice: «Il solito»."),
        ("La clessidra e i sigilli",
         "La clessidra accanto a un invito vuol dire che scade. «Solo "
         "adesso»: se scegli altro, l'invito cade. «Fino alla Luna IV, "
         "giorno 28»: resta fino alla scelta del cuore, poi forse no. Un "
         "sigillo rosso sopra un giorno della striscia: quel giorno qualcosa "
         "accade comunque."),
        ("Diario, Trama, Borsa",
         "Il Diario racconta a che punto sei con ognuno: si apre dal bottone "
         "in alto. La Trama tiene le scelte che pesano (il {color=#c0392b}◆{/color} "
         "rosso accanto a una scelta) e quello che ne nasce. La Borsa tiene Scudi e doni: si "
         "apre dalla pillola in alto a destra. Il «?» riapre questa guida."),
    ]

screen guida_pianificatore():

    modal True
    zorder 150

    default gp = 0
    $ gp_ultima = len(GUIDA_PIANIFICATORE) - 1
    $ gp_chiudi = [SetField(persistent, "guida_pianificatore", True),
                   Hide("guida_pianificatore")]

    key "game_menu" action gp_chiudi

    add Solid("#000000b0")

    frame:
        style "cal_guida"
        vbox:
            spacing 22
            xfill True
            hbox:
                spacing 16
                text GUIDA_PIANIFICATORE[gp][0] style "cal_pannello_nome" yalign 0.5
                text "%d / %d" % (gp + 1, gp_ultima + 1) style "cal_pannello_testo" yalign 0.5
            add "gui/divisore.png" xalign 0.0
            text GUIDA_PIANIFICATORE[gp][1] style "cal_guida_testo"
            null height 6
            hbox:
                xalign 1.0
                spacing 18
                if gp < gp_ultima:
                    textbutton _("Salta"):
                        style "cal_testata"
                        text_style "cal_testata_text"
                        action gp_chiudi
                if gp > 0:
                    textbutton _("Indietro"):
                        style "cal_testata"
                        text_style "cal_testata_text"
                        action SetScreenVariable("gp", gp - 1)
                if gp < gp_ultima:
                    textbutton _("Avanti"):
                        style "cal_testata"
                        text_style "cal_testata_text"
                        action SetScreenVariable("gp", gp + 1)
                else:
                    textbutton _("Ho capito"):
                        style "cal_testata"
                        text_style "cal_testata_text"
                        action gp_chiudi

style cal_guida is empty
style cal_guida:
    align (0.5, 0.5)
    xsize 1100
    background Frame("gui/frame.png", 60, 60)
    padding (60, 50, 60, 50)

style cal_guida_testo is text:
    font gui.text_font
    size 28
    color "#f0e6d2"
    line_spacing 4


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

            text "Momenti del semestre vissuti: [diario_eventi_contati()]" size 22 color "#b3a173"

            text diario_borsa() size 22 color "#b3a173"

            null height 10

            hbox:
                spacing 12
                textbutton _("Apri le Cronache"):
                    style "cronache_tab"
                    text_style "cronache_tab_text"
                    action ShowMenu("cronache", da="diario")
                textbutton _("Apri la Trama"):
                    style "cronache_tab"
                    text_style "cronache_tab_text"
                    action ShowMenu("trama", da="diario")
                textbutton _("Apri la Borsa"):
                    style "cronache_tab"
                    text_style "cronache_tab_text"
                    action ShowMenu("inventario", da="diario")


style cartello_riepilogo is empty
style cartello_riepilogo:
    xalign 0.5
    ypos 680
    xmaximum 1100
    background Frame("gui/frame_piccolo.png", 26, 26)
    padding (36, 16, 36, 16)

style cartello_riepilogo_text is text:
    font gui.text_font
    size 28
    italic True
    color "#f5e3b8"
    textalign 0.5
    xalign 0.5

style cartello_numero is text
style cartello_numero:
    font gui.text_font
    size 32
    italic True
    color "#5a4426"
