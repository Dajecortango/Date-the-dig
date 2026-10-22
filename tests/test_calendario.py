"""Verifica il motore puro del calendario (game/calendario_logic.py).

Uso: py -3 -I tests/test_calendario.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "game"))

import calendario_logic as cl  # noqa: E402
import relazioni_logic as rlz  # noqa: E402
import routing_logic as rl  # noqa: E402

FAILURES = []


def check(nome, got, atteso):
    ok = got == atteso
    if not ok:
        FAILURES.append(nome)
    print(f"{'PASS' if ok else 'FAIL'}: {nome}: {got!r} (atteso {atteso!r})")


CAL = {
    1: [{"giorno": 3, "slots": ["mattina", "sera"]},
        {"giorno": 9, "slots": ["pomeriggio"]}],
    2: [{"giorno": 1, "slots": ["sera"]}],
}


def test_sequenza():
    check("sequenza ordinata con skip", cl.genera_sequenza(CAL),
          [(1, 3, "mattina"), (1, 3, "sera"), (1, 9, "pomeriggio"), (2, 1, "sera")])


def test_fisso():
    ev = {"id": "svelo", "label": "prologo", "tipo": "fisso", "char": None,
          "luna": 1, "giorno": 3, "slot": "mattina"}
    ev_cond = dict(ev, id="mai", cond=lambda v: False)
    check("fisso trovato", cl.trova_fisso((1, 3, "mattina"), [ev], {}, set()), ev)
    check("fisso gia' visto", cl.trova_fisso((1, 3, "mattina"), [ev], {}, {"svelo"}), None)
    check("fisso altro momento", cl.trova_fisso((1, 3, "sera"), [ev], {}, set()), None)
    check("fisso cond falsa", cl.trova_fisso((1, 3, "mattina"), [ev_cond], {}, set()), None)


def test_inviti():
    inv = {"id": "aede_cap1", "label": "cap1", "tipo": "invito", "char": "aede",
           "luna_min": 1, "slot": "sera", "cond": lambda v: v["aede_affinity"] >= 2}
    vars_ok = {"aede_affinity": 2, "congelate": set()}
    vars_poca = {"aede_affinity": 1, "congelate": set()}
    vars_gelo = {"aede_affinity": 5, "congelate": {"aede"}}
    check("invito a soglia", cl.trova_inviti((1, 3, "sera"), [inv], vars_ok, set()), [inv])
    check("invito slot sbagliato", cl.trova_inviti((1, 3, "mattina"), [inv], vars_ok, set()), [])
    check("invito sotto soglia", cl.trova_inviti((1, 3, "sera"), [inv], vars_poca, set()), [])
    check("invito char congelato", cl.trova_inviti((1, 3, "sera"), [inv], vars_gelo, set()), [])
    check("invito gia' visto", cl.trova_inviti((1, 3, "sera"), [inv], vars_ok, {"aede_cap1"}), [])
    inv_any = dict(inv, id="x", slot=None)
    check("invito slot None ovunque",
          cl.trova_inviti((1, 3, "mattina"), [inv_any], vars_ok, set()), [inv_any])
    inv_tardi = dict(inv, id="y", luna_min=2)
    check("invito luna futura", cl.trova_inviti((1, 3, "sera"), [inv_tardi], vars_ok, set()), [])


def test_pool():
    check("pool pesca prima non vista", cl.pesca_variante(["a", "b"], {"a"}), "b")
    check("pool esaurito", cl.pesca_variante(["a", "b"], {"a", "b"}), None)
    check("pool da zero", cl.pesca_variante(["a", "b"], set()), "a")


def check_wiring():
    """calendario.rpy deve contenere loop, screen e import del motore."""
    rpy = os.path.join(HERE, "..", "game", "calendario.rpy")
    with open(rpy, encoding="utf-8") as f:
        src = f.read()
    for frammento in ("label cal_loop", "screen pianificazione",
                      "import calendario_logic", "def cal_strip",
                      "def cal_slot_stati", "ATTIVITA_DESC", "save_name"):
        check("wiring: " + frammento, frammento in src, True)
    scr = open(os.path.join(HERE, "..", "game", "screens.rpy"),
               encoding="utf-8").read()
    for frammento in ("ctc_diamante", "mm_pattern_anim", "char_color",
                      'getattr(i, "chosen", False)'):
        check("screens: " + frammento, frammento in scr, True)


def check_eventi_aede():
    """aede_eventi.rpy registra gli id attesi; niente jump di catena residui."""
    ev = open(os.path.join(HERE, "..", "game", "routes", "aede_eventi.rpy"),
              encoding="utf-8").read()
    for eid in ('"svelo"', '"athlion"', '"aede_cap1"', '"aede_cap3"',
                '"aede_cap4"'):
        check("evento aede " + eid, eid in ev, True)
    check("impegno_aede esiste", "label impegno_aede" in ev, True)
    for f in ("aede_atto1.rpy", "aede_atto2.rpy", "aede_interludi.rpy"):
        src = open(os.path.join(HERE, "..", "game", "routes", f),
                   encoding="utf-8").read()
        check("niente jump di catena in " + f,
              any(x in src for x in ("jump cap", "jump interludio", "jump climax")),
              False)


def check_eventi_caino():
    ev = open(os.path.join(HERE, "..", "game", "routes", "caino_eventi.rpy"),
              encoding="utf-8").read()
    for eid in ('"adunanza"', '"caino_cap1"', '"caino_cap2"', '"caino_cap3"',
                '"caino_cap4"', '"caino_cap5"', '"caino_cap6"'):
        check("evento caino " + eid, eid in ev, True)
    check("impegno_caino esiste", "label impegno_caino" in ev, True)
    for f in ("caino_atto1.rpy", "caino_atto2.rpy"):
        src = open(os.path.join(HERE, "..", "game", "routes", f),
                   encoding="utf-8").read()
        check("niente jump di catena in " + f, "jump caino_cap" in src
              or "jump caino_climax" in src, False)


def _route(nome):
    """Tutti i file di una route (nome_*.rpy) concatenati."""
    cartella = os.path.join(HERE, "..", "game", "routes")
    return "\n".join(
        open(os.path.join(cartella, f), encoding="utf-8").read()
        for f in sorted(os.listdir(cartella))
        if f.startswith(nome + "_") and f.endswith(".rpy"))


def check_eventi_druso():
    ev = _route("druso")
    for eid in ('"druso_ev1"', '"druso_ev2"', '"druso_ev3"', '"druso_ev4"',
                '"druso_luna5"'):
        check("evento druso " + eid, eid in ev, True)
    check("druso_ev4 richiede ev3", '"druso_ev3" in v["visti"]' in ev, True)
    check("druso_ev4 muore dopo scelta_cuore",
          '"scelta_cuore" not in v["visti"]' in ev, True)
    for lbl in ("impegno_druso", "druso_fiaccolata", "druso_climax",
                "druso_good", "druso_neutral", "druso_bad"):
        check("label " + lbl, "label " + lbl + ":" in ev, True)
    check("passi falsi via routing_logic",
          "rl.druso_passo_falso(" in ev and "druso_passi_falsi" in ev, True)
    check("passi falsi solo per uomini",
          (rl.druso_passo_falso("f", 0), rl.druso_passo_falso("m", 0)),
          ((0, False, False), (1, True, False)))


def check_eventi_icaro():
    ev = _route("icaro")
    for eid in ('"icaro_ev1"', '"icaro_ev2"', '"icaro_ev3"', '"icaro_luna5"'):
        check("evento icaro " + eid, eid in ev, True)
    for lbl in ("impegno_icaro", "impegno_bro", "icaro_fiaccolata",
                "icaro_luna5", "icaro_climax", "icaro_good", "icaro_bro_end"):
        check("label " + lbl, "label " + lbl + ":" in ev, True)
    check("gate di genere sul climax", "rl.finale_icaro(player_gender" in ev
          and rl.finale_icaro("m", 20, True, set()) == "icaro_bro_end", True)
    check("hook gelosia registrato",
          "cal_post_evento_hooks.append(icaro_gelosia)" in ev, True)


def check_snodi():
    ev = open(os.path.join(HERE, "..", "game", "routes", "snodi.rpy"),
              encoding="utf-8").read()
    for eid in ('"scelta_cuore"', '"fiaccolata"', '"aede_cap6"',
                '"luna6_climax"'):
        check("evento snodo " + eid, eid in ev, True)
    for ramo in ('cal_route == "aede"', 'cal_route == "caino"',
                 'cal_route == "druso"', 'cal_route == "icaro"'):
        check("dispatch " + ramo, ev.count(ramo) >= 2, True)
    for lbl in ("fiaccolata_caino", "fiaccolata_neutra",
                "finale_neutro_semestre", "ev_scelta_cuore"):
        check("label " + lbl, "label " + lbl + ":" in ev, True)
    check("pari merito scelto dal giocatore", "renpy.display_menu" in ev, True)
    check("candidata ofelia soglia 8",
          (rl.cuore_soglie(True)["ofelia"], rl.cuore_soglie(False)["ofelia"]),
          (8, 8))
    check("candidati dalla fonte unica", "rl.cuore_candidati(cal_vars())" in ev,
          True)
    check("niente soglie del cuore copiate in snodi",
          any(x in ev for x in ("(9 if f else 11)", "(7 if f else 6)",
                                "store.ofelia_affinity >= 8",
                                "store.caino_fiducia >= 10")),
          False)
    check("coppie poly", '"ofelia+aede"' in ev and '"ofelia+caino"' in ev, True)
    check("route_seconda impostata", "route_seconda =" in ev, True)
    check("aede_cap6 anche da seconda", 'v["route_seconda"] == "aede"' in ev, True)
    cap6 = ev.split('"id": "aede_cap6"')[1].split("},")[0]
    check("aede_cap6 salta se sospetto", 'v["aede_sospetto"] < 2' in cap6, True)
    cal = _leggi("calendario.rpy")
    check("cal_vars aede_sospetto", '"aede_sospetto": store.aede_sospetto' in cal, True)
    check("dispatch ofelia", ev.count('cal_route == "ofelia"') >= 2, True)
    import re
    epi = ev.split("label epilogo_semestre:")[1]
    check("epilogo: niente soglie scritte a mano",
          re.findall(r"(?:affinity|fiducia) >= \d", epi), [])
    check("epilogo: soglie dalla fonte unica",
          'ep_soglie = rl.cuore_soglie(player_gender == "f")' in epi
          and "ep_media = rl.EPILOGO_MEDIA" in epi, True)
    check("epilogo: Bro via rl.finale_bro",
          "rl.finale_bro(icaro_affinity, icaro_impegnato)" in epi, True)
    check("epilogo: riga di Aede nella coda amara",
          'if "aede" in epilogo_scelti and epilogo_finale == "ofelia_good":'
          in epi, True)


def check_label_esistenti():
    """Ogni label registrato in un evento o in un pool attivita' esiste."""
    import glob
    import re
    gioco = ""
    for f in glob.glob(os.path.join(HERE, "..", "game", "**", "*.rpy"),
                       recursive=True):
        gioco += open(f, encoding="utf-8").read()
    riferiti = set(re.findall(r'"label":\s*"(\w+)"', gioco))
    riferiti |= set(re.findall(r'"(att_\w+)"', gioco))
    definiti = set(re.findall(r"(?m)^label (\w+)", gioco))
    mancanti = sorted(riferiti - definiti)
    check("label referenziati tutti definiti", mancanti, [])


def _leggi(nome):
    return open(os.path.join(HERE, "..", "game", nome), encoding="utf-8").read()


def check_store_picklabile():
    """C1: nessun dict evento (con lambda) deve finire nello store o in
    _return: la screen ritorna id, il loop maneggia solo id/label."""
    cal = _leggi("calendario.rpy")
    # Il ritorno passa da cal_azione (selezione su touch), ma resta la tupla
    # ("evento", id): mai il dict inv.
    check("screen ritorna id non dict",
          'cal_azione(cal_touch, cal_sel, cal_info, ("evento", inv["id"]))' in cal, True)
    check("niente dict evento in _return", 'Return(("evento", ev))' in cal, False)
    check("loop usa cal_fisso_id", "cal_fisso_id" in cal, True)
    check("niente cal_evento_corrente", "cal_evento_corrente" in cal, False)
    check("niente inviti_fatti", "inviti_fatti" in cal, False)
    check("info inviti espone scade", '"scade": bool(e.get("scade", False))' in cal, True)
    check("info inviti: avviso solo per la screen", '"avviso": _avviso(e)' in cal, True)
    check("loop chiama hook scadenza", "cal_inviti_ignorati_hooks" in cal, True)


def _max_punti(var):
    """Somma dei massimi incrementi per label: tetto teorico dell'affinita'."""
    import glob
    import re
    tot = 0
    for f in glob.glob(os.path.join(HERE, "..", "game", "**", "*.rpy"),
                       recursive=True):
        src = open(f, encoding="utf-8").read()
        for chunk in re.split(r"(?m)^label ", src)[1:]:
            inc = [int(n) for n in re.findall(var + r" \+= (\d+)", chunk)]
            if inc:
                tot += max(inc)
    return tot


def check_economia_punti():
    """C2/C3: ogni soglia registrata deve essere raggiungibile."""
    druso_max = _max_punti("druso_affinity")
    icaro_max = _max_punti("icaro_affinity")
    check("druso: soglia impegno uomo (11) raggiungibile", druso_max >= 11, True)
    check("druso: good end (16) raggiungibile", druso_max >= 16, True)
    check("druso good end soglia 16", rl.GOOD["druso"], 16)
    check("icaro: good end (13) raggiungibile", icaro_max >= 13, True)
    check("icaro good end soglia 13", rl.GOOD["icaro"], 13)
    check("soglie druso 9F/11M",
          (rl.cuore_soglie(True)["druso"], rl.cuore_soglie(False)["druso"]),
          (9, 11))
    check("soglie icaro 7F/6M",
          (rl.cuore_soglie(True)["icaro"], rl.cuore_soglie(False)["icaro"]),
          (7, 6))
    check("soglie aede 8, caino 10",
          (rl.cuore_soglie(True)["aede"], rl.cuore_soglie(False)["caino"]),
          (8, 10))
    ofelia_max = _max_punti("ofelia_affinity")
    check("ofelia: impegno (8) raggiungibile", ofelia_max >= 8, True)
    check("ofelia: good end (12) raggiungibile", ofelia_max >= 12, True)
    # Percorso segreto con Aede: corte/eventi pre-cuore danno al massimo 9,
    # la mano di Aede sulla Calà +1, il climax di Aede non tocca Ofelia ma
    # ev4 (+2) si'; il dono preferito +1. Budget 9 + 1 + 2 + 1 = 13: il good
    # (>= 12) tollera un errore solo se anche il ramo "mano di Aede" premia
    # Ofelia.
    fin = _route("ofelia")
    fiac_aede = fin.split("label ofelia_fiaccolata_aede:")[1].split("\nlabel ")[0]
    ramo_aede = fiac_aede.split("call cap5")[1].split('"Prendere la mano di Ofelia"')[0]
    check("ofelia: mano di Aede premia la discrezione",
          "ofelia_affinity += 1" in ramo_aede, True)
    # Good end alzati di 1 per il dono preferito (uno per personaggio).
    check("aede: good end (13) raggiungibile", _max_punti("aede_affinity") >= 13, True)
    check("aede good end soglia 13", rl.GOOD["aede"], 13)
    check("caino: good end (13) raggiungibile", _max_punti("caino_fiducia") >= 13, True)
    check("caino good end soglia 13", rl.GOOD["caino"], 13)
    check("ofelia good end soglia 12", rl.GOOD["ofelia"], 12)
    check("poly aede: good Aede a 13 (12 non basta)",
          (rl.finale_ofelia_poly_aede(0, 0, 0, 13, True, True, True),
           rl.finale_ofelia_poly_aede(0, 0, 0, 12, True, True, True)),
          ("good_end", "neutral_end"))
    check("ofelia: good con Caino a 13",
          (rl.finale_ofelia(12, 0, "caino", 13),
           rl.finale_ofelia(12, 0, "caino", 12)),
          ("ofelia_good_caino", "ofelia_good"))
    ic = _route("icaro")
    for soglia in (">= 2", ">= 4", ">= 6"):
        check("icaro scala eventi " + soglia,
              '"icaro_affinity"] ' + soglia in ic.replace("v[", "["), True)


def check_economia_scudi():
    """Blocco C: Scudi, mercato, doni (un += 1 per personaggio), casuali."""
    import re
    eco = _leggi("economia.rpy")
    check("scudi iniziali 5", "default scudi = 5" in eco, True)
    check("registri +2", "scudi += 2" in eco.split("label eco_dopo_attivita")[1]
          .split('"citta"')[0], True)
    check("mercato condizionato", 'v["scudi"] >= 2' in eco, True)
    for ch, var in (("aede", "aede_affinity"), ("caino", "caino_fiducia"),
                    ("druso", "druso_affinity"), ("icaro", "icaro_affinity"),
                    ("ofelia", "ofelia_affinity")):
        corpo = eco.split("label dono_%s:" % ch)[1].split("\nlabel ")[0]
        check("dono %s: +1 e -1" % ch,
              (var + " += 1" in corpo, var + " -= 1" in corpo), (True, True))
        check("dono %s nei gusti" % ch, '"%s": (' % ch in eco, True)
    check("un dono con punti per personaggio", "doni_dati.add(char)" in eco, True)
    casi = re.findall(r"(?m)^label (caso_\w+):", eco)
    check("6 eventi casuali", len(casi), 6)
    check("casuali senza affinita'",
          re.search(r"(affinity|fiducia) [+-]=",
                    eco.split("label caso_borseggiatore:")[1]) is None, True)
    check("casuali con renpy.random",
          "rlz.pesca_citta(CITTA_CASI, store.eventi_visti, da_pool," in eco
          and "renpy.random)" in eco, True)
    check("doni via relazioni_logic",
          "rlz.dono_offribile(" in eco and "rlz.dono_consegna(" in eco, True)
    cal = _leggi("calendario.rpy")
    borsa = _leggi("borsa.rpy")
    check("borsa a schermo nel pianificatore",
          'renpy.get_screen("pianificazione")' in borsa
          and 'config.overlay_screens.append("borsa_hud")' in borsa, True)
    check("inventario dal menu rapido",
          '"borsa": ShowMenu("inventario")' in _leggi("screens.rpy"), True)
    check("borsa nel diario", "def diario_borsa" in cal, True)
    check("fallback per affinita'", "CAL_FALLBACK_AFF" in cal, True)


def check_prerequisiti_sequenza():
    """I1/I3: i capitoli alti richiedono il precedente visto; le scene di
    livello impegno muoiono dopo la scelta del cuore."""
    ae = _leggi(os.path.join("routes", "aede_eventi.rpy"))
    ca = _leggi(os.path.join("routes", "caino_eventi.rpy"))
    check("aede_cap3 richiede cap1", '"aede_cap1" in v["visti"]' in ae, True)
    check("aede_cap4 richiede cap3", '"aede_cap3" in v["visti"]' in ae, True)
    for prev, testo in [("caino_cap1", ca), ("caino_cap2", ca),
                        ("caino_cap3", ca), ("caino_cap4", ca),
                        ("caino_cap5", ca)]:
        check("catena caino richiede " + prev,
              '"%s" in v["visti"]' % prev in testo, True)
    for eid in ("aede_cap4", "caino_cap5", "caino_cap6"):
        pass
    check("caino_cap5/6 muoiono dopo scelta_cuore",
          ca.count('"scelta_cuore" not in v["visti"]') >= 2, True)
    check("aede_cap4 muore dopo scelta_cuore",
          '"scelta_cuore" not in v["visti"]' in ae, True)
    of = _route("ofelia")
    check("ofelia_ev2 richiede ev1", '"ofelia_ev1" in v["visti"]' in of, True)
    check("ofelia_ev3 richiede ev2", '"ofelia_ev2" in v["visti"]' in of, True)
    check("ofelia_ev3 muore dopo scelta_cuore", '"scelta_cuore" not in v["visti"]' in of, True)


def check_congelamento_route_attiva():
    """I2: route attiva ma congelata -> niente giuramento ne' climax romance."""
    sn = _leggi(os.path.join("routes", "snodi.rpy"))
    check("dispatch usa route_viva", "route_viva()" in sn, True)
    check("aede_cap6 esclude congelata",
          '"aede" not in v["congelate"]' in sn, True)
    check("seconda viva esclude congelata", "def route_seconda_viva" in sn, True)
    cal = _leggi("calendario.rpy")
    check("filtro inviti con seconda", "store.route_seconda" in cal, True)


def check_incroci():
    ev = _leggi(os.path.join("routes", "incroci.rpy"))
    for eid in ('"trio_lenora"', '"incrocio_palestra"', '"incrocio_carte"'):
        check("evento incrocio " + eid, eid in ev, True)


def _cal_giorni():
    """CAL_GIORNI letto da calendario.rpy (literal Python)."""
    import ast
    cal = _leggi("calendario.rpy")
    testo = cal.split("CAL_GIORNI = ")[1].split("\n    CAL_SEQUENZA")[0]
    return ast.literal_eval(testo)


def _eventi_registrati():
    """Tutti i dict evento (fissi e inviti) dei .rpy, letti come testo:
    {id: {"tipo", "luna", "giorno", "slot", "luna_min", "cond"}}."""
    import glob
    import re
    out = {}
    for f in glob.glob(os.path.join(HERE, "..", "game", "**", "*.rpy"),
                       recursive=True):
        src = open(f, encoding="utf-8").read()
        pezzi = re.split(r'(?=\{"id": ")', src)[1:]
        for p in pezzi:
            p = p.split("])")[0].split("\n\n")[0]
            eid = re.match(r'\{"id": "(\w+)"', p).group(1)
            tipo = re.search(r'"tipo": "(\w+)"', p)
            if not tipo:
                continue
            num = lambda k: (int(re.search(r'"%s": (\d+)' % k, p).group(1))
                             if re.search(r'"%s": (\d+)' % k, p) else None)
            slot = re.search(r'"slot": "(\w+)"', p)
            cond = p.split('"cond":')[1] if '"cond":' in p else ""
            out[eid] = {"tipo": tipo.group(1), "luna": num("luna"),
                        "giorno": num("giorno"), "luna_min": num("luna_min"),
                        "slot": slot.group(1) if slot else None, "cond": cond}
    return out


def check_capienza_inviti():
    """Capienza statica degli slot prima della scelta del cuore (IV/28).

    Per ogni invito a scadenza (cond che finisce con
    `"scelta_cuore" not in v["visti"]`, senza un `or` che lo tenga vivo)
    si ricostruisce la catena dei prerequisiti (`"x" in v["visti"]` tra
    inviti). Per ogni tipo di slot e per ogni membro m della catena su quello
    slot: i membri con luna_min >= m.luna_min devono stare nei momenti liberi
    di quel tipo da m.luna_min a IV/28. Libero = esiste in CAL_GIORNI e non
    ha un evento fisso (qualunque fisso, anche condizionato: ipotesi
    prudente, la rivalita' scatta proprio a chi corteggia).

    Ipotesi (controllo necessario, non sufficiente): ogni catena e'
    considerata da sola (non si contano le catene di altri personaggi che
    competono per gli stessi slot); si ignora l'ordine fra slot di tipo
    diverso (es. un pomeriggio che deve precedere una sera); le soglie di
    affinita' si assumono raggiunte in tempo."""
    giorni = _cal_giorni()
    eventi = _eventi_registrati()
    fissi = {(e["luna"], e["giorno"], e["slot"]) for e in eventi.values()
             if e["tipo"] == "fisso"}
    esistenti = {(l, g["giorno"], s) for l, gg in giorni.items()
                 for g in gg for s in g["slots"]}
    check("fissi su momenti esistenti",
          sorted(m for m in fissi if m not in esistenti), [])
    scelta = (4, 28, "sera")
    liberi = sorted(m for m in esistenti - fissi if m < scelta)
    inviti = {k: e for k, e in eventi.items() if e["tipo"] == "invito"}
    import re
    scadenza = re.compile(r'"scelta_cuore" not in v\["visti"\]\s*\}')
    a_scadenza = sorted(k for k, e in inviti.items()
                        if scadenza.search(e["cond"] + "}"))
    check("inviti a scadenza trovati", len(a_scadenza) >= 8, True)
    for eid in a_scadenza:
        catena, coda = [], [eid]
        while coda:
            c = coda.pop()
            if c in catena or c not in inviti:
                continue
            catena.append(c)
            coda += re.findall(r'"(\w+)" in v\["visti"\]', inviti[c]["cond"])
        ok = True
        for m in catena:
            slot, lm = inviti[m]["slot"], inviti[m]["luna_min"]
            if slot is None:
                continue
            serve = sum(1 for x in catena if inviti[x]["slot"] == slot
                        and inviti[x]["luna_min"] >= lm)
            ci_sono = sum(1 for l, g, s in liberi if s == slot and l >= lm)
            if serve > ci_sono:
                ok = False
                print("  capienza: %s richiede %d %s da Luna %d, liberi %d"
                      % (eid, serve, slot, lm, ci_sono))
        check("capienza catena " + eid, ok, True)


def test_scadenza():
    a = {"id": "of1", "scade": True}
    b = {"id": "ae1"}
    c = {"id": "of2", "scade": True}
    check("scadenza: scelto altro", cl.inviti_ignorati([a, b], "ae1"), ["of1"])
    check("scadenza: scelto lei", cl.inviti_ignorati([a, b], "of1"), [])
    check("scadenza: attivita'", cl.inviti_ignorati([a, b, c], None), ["of1", "of2"])
    check("scadenza: nessuna", cl.inviti_ignorati([b], None), [])


def test_scadenza_ofelia():
    """Inviti a scadenza: conteggio, gelo a 2, id non di Ofelia ignorati,
    stop una volta congelata."""
    es = rlz.ofelia_esiti_scadenza
    check("ofelia: primo mancato", es(["ofelia_ev1"], 0, False), ["prima"])
    check("ofelia: secondo mancato congela", es(["ofelia_ev2"], 1, False),
          ["gelo"])
    check("ofelia: due insieme da zero", es(["ofelia_ev1", "ofelia_ev2"], 0,
                                            False), ["prima", "gelo"])
    check("ofelia: dopo il gelo non conta piu'",
          es(["ofelia_ev1", "ofelia_ev2", "ofelia_ev3"], 0, False),
          ["prima", "gelo"])
    check("ofelia: gia' congelata", es(["ofelia_ev3"], 2, True), [])
    check("ofelia: id non di Ofelia ignorati",
          es(["aede_cap1", "interludio_ofelia_1", "druso_ev1"], 0, False), [])
    check("ofelia: misti", es(["caino_cap2", "ofelia_ev2"], 0, False),
          ["prima"])
    check("ofelia: nessun id", es([], 1, False), [])
    # Catena completa sullo stato: mancati e affinita' come in ofelia_scadenza.
    mancati, aff, gelo = 0, 7, False
    for lotto in (["ofelia_ev1"], ["aede_cap1"], ["ofelia_ev2"], ["ofelia_ev3"]):
        for esito in es(lotto, mancati, gelo):
            mancati += 1
            aff -= 1
            gelo = gelo or esito == "gelo"
    check("ofelia: stato dopo la catena", (mancati, aff, gelo), (2, 5, True))


def test_cuore():
    """Scelta del cuore: candidati, opzioni, coppia, rivali, route vive."""
    def v(f=True, cong=(), **aff):
        base = {"aede_affinity": 0, "caino_fiducia": 0, "druso_affinity": 0,
                "icaro_affinity": 0, "ofelia_affinity": 0}
        base.update(aff)
        base["player_gender"] = "f" if f else "m"
        base["congelate"] = set(cong)
        return base
    check("cuore: nessuno", rl.cuore_candidati(v()), [])
    check("cuore: soglie esatte donna",
          rl.cuore_candidati(v(aede_affinity=8, caino_fiducia=10,
                               druso_affinity=9, icaro_affinity=7,
                               ofelia_affinity=8)),
          ["aede", "caino", "druso", "icaro", "ofelia"])
    check("cuore: sotto soglia di uno, donna",
          rl.cuore_candidati(v(aede_affinity=7, caino_fiducia=9,
                               druso_affinity=8, icaro_affinity=6,
                               ofelia_affinity=7)), [])
    check("cuore: uomo druso 11 / icaro 6",
          (rl.cuore_candidati(v(False, druso_affinity=10, icaro_affinity=6)),
           rl.cuore_candidati(v(False, druso_affinity=11))),
          (["icaro"], ["druso"]))
    check("cuore: congelato escluso",
          rl.cuore_candidati(v(cong=["ofelia"], ofelia_affinity=12,
                               aede_affinity=9)), ["aede"])
    nomi = {"aede": "Aede", "caino": "Caino", "druso": "Druso",
            "icaro": "Icaro", "ofelia": "Ofelia"}
    check("opzioni: singolo", rl.cuore_opzioni(["druso"], nomi),
          [("Druso", "druso")])
    check("opzioni: coppie poly",
          rl.cuore_opzioni(["aede", "caino", "ofelia"], nomi),
          [("Aede", "aede"), ("Caino", "caino"), ("Ofelia", "ofelia"),
           ("Ofelia e Aede", "ofelia+aede"), ("Ofelia e Caino", "ofelia+caino")])
    check("opzioni: niente poly con Druso/Icaro",
          rl.cuore_opzioni(["druso", "icaro", "ofelia"], nomi),
          [("Druso", "druso"), ("Icaro", "icaro"), ("Ofelia", "ofelia")])
    check("opzioni: niente poly senza Ofelia",
          rl.cuore_opzioni(["aede", "caino"], nomi),
          [("Aede", "aede"), ("Caino", "caino")])
    check("coppia: entrambi", rl.risolvi_coppia(True, True, "aede"),
          ("ofelia", "aede"))
    check("coppia: solo Ofelia", rl.risolvi_coppia(True, False, "caino"),
          ("ofelia", None))
    check("coppia: solo l'altro", rl.risolvi_coppia(False, True, "caino"),
          ("caino", None))
    check("coppia: nessuno", rl.risolvi_coppia(False, False, "aede"), None)
    check("rivali: i due piu' alti per margine",
          rl.rivali_cuore(v(aede_affinity=9, druso_affinity=12,
                            ofelia_affinity=8)), ["druso", "aede"])
    check("rivali: uno solo sopra", rl.rivali_cuore(v(aede_affinity=9)), None)
    check("rivali: pari margine, ordine fisso",
          rl.rivali_cuore(v(caino_fiducia=10, aede_affinity=8)),
          ["aede", "caino"])
    check("route viva", (rl.route_viva("druso", set()),
                         rl.route_viva("druso", {"druso"}),
                         rl.route_viva(None, set())), ("druso", None, None))
    check("seconda viva", (rl.route_seconda_viva("ofelia", "caino", set()),
                           rl.route_seconda_viva("ofelia", "caino", {"caino"}),
                           rl.route_seconda_viva("ofelia", "aede", {"ofelia"}),
                           rl.route_seconda_viva("aede", "caino", set())),
          ("caino", None, None, None))


def test_doni():
    gusti = {"aede": ("pietra", "fiori"), "druso": ("taccuino", "ballate")}
    check("dono: preferito", rlz.dono_consegna(gusti, "aede", "pietra"),
          ("ama", True))
    check("dono: detestato", rlz.dono_consegna(gusti, "aede", "fiori"),
          ("odia", True))
    check("dono: neutro non consuma",
          rlz.dono_consegna(gusti, "druso", "pietra"), ("neutro", False))
    check("dono: offribile", rlz.dono_offribile("pietra", "aede", set(), set()),
          True)
    check("dono: niente in borsa", rlz.dono_offribile(None, "aede", set(),
                                                      set()), False)
    check("dono: gia' dato resta offribile (come neutro)",
          rlz.dono_offribile("pietra", "aede", {"aede"}, set()), True)
    check("dono: gia' dato -> neutro senza punti",
          rlz.dono_consegna(gusti, "aede", "pietra", {"aede"}),
          ("neutro", False))
    check("dono: gia' dato, anche il detestato e' neutro",
          rlz.dono_consegna(gusti, "aede", "fiori", {"aede"}),
          ("neutro", False))
    # Il dono non resta bloccato in borsa: con tutti i personaggi gia' in
    # doni_dati, darlo svuota dono_tenuto e il mercato torna visibile.
    tenuto, dati = "pietra", {"aede", "druso"}
    if rlz.dono_offribile(tenuto, "aede", dati, set()):
        esito, segna = rlz.dono_consegna(gusti, "aede", tenuto, dati)
        tenuto = None
    check("dono: borsa liberata, niente punti", (tenuto, esito, segna),
          (None, "neutro", False))
    check("dono: mercato di nuovo visibile",
          '"scudi"] >= 2 and v["dono_tenuto"] is None' in _leggi("economia.rpy")
          and tenuto is None, True)
    check("dono: il gioco passa doni_dati alla consegna",
          "dono_tenuto,\n" in _leggi("economia.rpy")
          and "doni_dati)" in _leggi("economia.rpy"), True)
    check("dono: altri ancora liberi",
          rlz.dono_offribile("pietra", "druso", {"aede"}, set()), True)
    check("dono: congelato", rlz.dono_offribile("pietra", "aede", set(),
                                                {"aede"}), False)
    # Massimo un +1 per personaggio: due preferiti di fila.
    dati, punti = set(), 0
    for _ in range(2):
        if rlz.dono_offribile("pietra", "aede", dati, set()):
            esito, segna = rlz.dono_consegna(gusti, "aede", "pietra", dati)
            punti += 1 if esito == "ama" else 0
            if segna:
                dati.add("aede")
    check("dono: limite +1 a semestre", punti, 1)
    # Il catalogo del gioco: ogni personaggio ha un preferito e un detestato
    # che esistono e sono diversi.
    eco = _leggi("economia.rpy")
    for ch in ("aede", "caino", "druso", "icaro", "ofelia"):
        check("dono %s gusti nel catalogo" % ch,
              '"%s": (' % ch in eco, True)


class _Rnd(object):
    """Finto renpy.random: tiro fisso, choice = primo; conta i tiri."""
    def __init__(self, tiro):
        self.tiro, self.tiri = tiro, 0

    def random(self):
        self.tiri += 1
        return self.tiro

    def choice(self, seq):
        return seq[0]


def test_casuali():
    casi = ["caso_a", "caso_b"]
    check("casuali: pool esaurito -> caso",
          rlz.pesca_citta(casi, set(), None, _Rnd(0.9)), "caso_a")
    check("casuali: tiro basso -> caso",
          rlz.pesca_citta(casi, set(), "citta_1", _Rnd(0.39)), "caso_a")
    check("casuali: tiro alto -> pool",
          rlz.pesca_citta(casi, set(), "citta_1", _Rnd(0.4)), "citta_1")
    check("casuali: una-tantum (visti esclusi)",
          rlz.pesca_citta(casi, {"caso_a"}, None, _Rnd(0.0)), "caso_b")
    check("casuali: tutti visti -> pool",
          rlz.pesca_citta(casi, {"caso_a", "caso_b"}, "citta_2", _Rnd(0.0)),
          "citta_2")
    check("casuali: tutti visti e pool esaurito",
          rlz.pesca_citta(casi, {"caso_a", "caso_b"}, None, _Rnd(0.0)), None)
    r = _Rnd(0.0)
    rlz.pesca_citta(casi, set(), None, r)
    check("casuali: niente tiro a pool esaurito", r.tiri, 0)
    # Simulazione: nessun caso si ripete finche' ce ne sono di liberi.
    visti, usciti = set(), []
    for _ in range(4):
        c = rlz.pesca_citta(casi, visti, None, _Rnd(0.0))
        if c:
            visti.add(c)
            usciti.append(c)
    check("casuali: mai ripetuti", usciti, ["caso_a", "caso_b"])


def check_eventi_ofelia():
    ev = _route("ofelia")
    check("hook scadenza registrato",
          "cal_inviti_ignorati_hooks.append(ofelia_scadenza)" in ev, True)
    check("scadenza via relazioni_logic", "rlz.ofelia_esiti_scadenza(" in ev,
          True)
    check("congela a 2 mancati", rlz.ofelia_esiti_scadenza(["ofelia_ev1"], 1,
                                                          False), ["gelo"])
    check("territorio corte", '"corte", "La corte di Ofelia", "ofelia"' in ev, True)
    for lbl in ("att_corte_1", "att_corte_2", "att_corte_3"):
        check("label " + lbl, "label " + lbl + ":" in ev, True)
    for eid in ('"ofelia_ev1"', '"ofelia_ev2"', '"ofelia_ev3"'):
        check("evento ofelia " + eid, eid in ev, True)
    check("inviti ofelia a scadenza", ev.count('"scade": True') >= 3, True)
    cal = _leggi("calendario.rpy")
    check("Prossimamente rimosso", "Prossimamente" in cal, False)
    check("cal_vars ofelia", '"ofelia_affinity": store.ofelia_affinity' in cal, True)
    for lbl in ("impegno_ofelia", "impegno_ofelia_aede", "impegno_ofelia_caino"):
        check("label " + lbl, "label " + lbl + ":" in ev, True)
    fin = _route("ofelia")
    for lbl in ("ofelia_fiaccolata", "ofelia_fiaccolata_caino", "ofelia_fiaccolata_aede"):
        check("label " + lbl, "label " + lbl + ":" in fin, True)
    check("mano di Ofelia alza il sospetto", "aede_sospetto += 2" in fin, True)
    check("mano di Aede gioca cap5", "call cap5" in fin, True)
    check("ofelia_ev4 fisso V/26", '"luna": 5, "giorno": 26' in ev, True)
    for lbl in ("ofelia_climax", "ofelia_routing", "ofelia_poly_aede_routing",
                "ofelia_good", "ofelia_good_caino", "ofelia_good_aede",
                "ofelia_bad_tempesta", "ofelia_neutral"):
        check("label " + lbl, "label " + lbl + ":" in fin, True)
    check("good ofelia soglie",
          (rl.ofelia_good(12, 1), rl.ofelia_good(11, 0), rl.ofelia_good(12, 2)),
          (True, False, False))
    check("tempesta prima del good",
          rl.finale_ofelia_poly_aede(2, 20, 0, 20, True, True, True),
          "ofelia_bad_tempesta")
    check("cartello route", "TANTO BELLA QUANTO LETALE" in fin, True)
    poly = fin.split("label ofelia_poly_aede_routing:")[1].split("\nlabel ")[0]
    check("fallback poly include good Aede",
          "jump expression cal_finale" in poly
          and rl.finale_ofelia_poly_aede(0, 5, 0, 13, True, True, True)
          == "good_end", True)
    ae = _leggi(os.path.join("routes", "aede_finali.rpy"))
    check("innesto poly nel climax Aede", 'route_seconda == "aede"' in ae, True)


def check_galleria_finali():
    """Galleria: ogni finale registrato e' sbloccato in un solo punto."""
    import glob
    import re
    gal = _leggi("finali_galleria.rpy")
    ids = re.findall(r'^\s*\("(\w+)",\s*"[^"]+",\s*"\w+",\s*"[^"]+"\),?$',
                     gal, re.M)
    check("FINALI ha 26 voci", len(ids), 26)
    check("id FINALI unici", len(set(ids)), len(ids))
    tutto = ""
    for f in glob.glob(os.path.join(HERE, "..", "game", "**", "*.rpy"),
                       recursive=True):
        if os.path.basename(f) == "finali_galleria.rpy":
            continue
        tutto += open(f, encoding="utf-8").read() + "\n"
    for fid in ids:
        check(f"sblocca_finale({fid}) una volta",
              tutto.count(f'sblocca_finale("{fid}")'), 1)
        lab = ("icaro_bro_end" if fid in ("icaro_bro_listino",
                                          "icaro_bro_conti") else fid)
        corpo = ""
        for parte in ("\n" + tutto).split(f"\nlabel {lab}:")[1:2]:
            corpo = parte.split("\nlabel ")[0]
        check(f"sblocca_finale({fid}) nel label {lab}",
              f'sblocca_finale("{fid}")' in corpo, True)
    check("screen galleria_finali", "screen galleria_finali" in gal, True)
    check("persistent.finali_visti",
          "default persistent.finali_visti = set()" in gal, True)
    check("bottone Finali nel main menu",
          'ShowMenu("galleria_finali")' in _leggi("screens.rpy"), True)


def check_segnali():
    """Segnali al giocatore: scena primo mancato, righe diario, notify Druso."""
    import re
    of = _route("ofelia")
    m = re.search(r"^label ofelia_scadenza_prima:\n(.*?)(?=^\S)",
                  of + "\nX", re.M | re.S)
    check("label ofelia_scadenza_prima", m is not None, True)
    corpo = m.group(1).rstrip().splitlines() if m else [""]
    check("ofelia_scadenza_prima finisce con return",
          corpo[-1].strip(), "return")
    check("call_in_new_context al primo mancato",
          'renpy.call_in_new_context("ofelia_scadenza_prima")' in of
          and 'esito == "prima"' in of
          and rlz.ofelia_esiti_scadenza(["ofelia_ev1"], 0, False) == ["prima"],
          True)
    cal = _leggi("calendario.rpy")
    for t in ("Ti guarda come si guarda un conto che non torna.",
              "Ha aspettato una volta. Non aspetterà la seconda.",
              "Ti ha segnato nel registro delle cose che non perdona. "
              "Una riga sola. Per ora."):
        check("diario: " + t[:30], t in cal, True)
    dr = _route("druso")
    check("notify Druso se la segna",
          'renpy.notify("Druso se la segna.")' in dr, True)


# Deviazioni nuove (spec 2026-10-22-route-finali-origliati, punto 1b):
# (route, id, predecessore, luna_min)
DEVIAZIONI = [
    ("druso", "druso_quaderno", "druso_ev1", 2),
    ("druso", "druso_udienza", "druso_ev2", 3),
    ("icaro", "icaro_debito_altrui", "icaro_int1", 2),
    ("icaro", "icaro_febbre", "icaro_ev2", 3),
    ("ofelia", "specchio_ofelia", "ofelia_ev1", 2),
    ("ofelia", "ballo_pretendenti", "ofelia_ev2", 3),
]


def _voce_registry(src, eid):
    """Testo del dict del registry con "id": eid (fino alla graffa)."""
    i = src.find('"id": "%s"' % eid)
    if i < 0:
        return None
    return src[i:src.find("},", i)]


def check_deviazioni():
    import glob
    tutto = ""
    for f in glob.glob(os.path.join(HERE, "..", "game", "**", "*.rpy"),
                       recursive=True):
        tutto += open(f, encoding="utf-8").read()
    for route, eid, prima, luna in DEVIAZIONI:
        ev = _leggi(os.path.join("routes", route + "_eventi.rpy"))
        voce = _voce_registry(ev, eid)
        check("deviazione %s nel registry" % eid, voce is not None, True)
        if voce is None:
            continue
        check("deviazione %s luna_min" % eid,
              '"luna_min": %d' % luna in voce, True)
        check("deviazione %s dopo %s" % (eid, prima),
              '"%s" in v["visti"]' % prima in voce, True)
        check("deviazione %s muore col cuore" % eid,
              '"scelta_cuore" not in v["visti"]' in voce, True)
        check("label %s" % eid, "label %s:" % eid in tutto, True)
        # Nessuna cond esistente dipende dalla deviazione.
        check("nessuno richiede %s" % eid,
              '"%s" in v["visti"]' % eid in tutto, False)
        if route == "ofelia":
            check("%s non conta come mancato" % eid,
                  eid.startswith("ofelia_") or '"scade"' in voce, False)


def _corpo_label(src, label):
    return src.split("label %s" % label, 1)[1].split("\nlabel ", 1)[0]


def check_revisione_finale():
    """Correzioni della revisione finale (route-finali-origliati)."""
    orig = _leggi(os.path.join("routes", "origliati.rpy"))
    for lbl in ("orig_caino_druso", "orig_caino_ofelia"):
        check(lbl + " registra i fatti",
              "conseguenze_aggiorna()" in _corpo_label(orig, lbl), True)
    dru = _route("druso")
    check("druso_passeggero: accordo di genere",
          "mi è car[fin]" in _corpo_label(dru, "druso_passeggero"), True)
    check("niente trent'anni di Druso", "trent'anni di rime" in dru, False)
    cai = _leggi(os.path.join("routes", "caino_finali.rpy"))
    check("caino_passeggero: niente promozione dopo la sospensione",
          "più in alto" in _corpo_label(cai, "caino_passeggero"), False)
    gal = _leggi("finali_galleria.rpy")
    riga = gal.split('"icaro_passeggero"', 1)[1].split(")", 1)[0]
    check("indizio icaro_passeggero raggiungibile",
          "invito di un altro" in riga, False)
    eco = _corpo_label(_leggi(os.path.join("routes", "echi.rpy")),
                       "echi_druso_quaderno")
    i = eco.find("sfida dei versi")
    check("eco quaderno: sfida dei versi solo se vista",
          i > 0 and '"druso_luna5" in eventi_visti' in eco[:i], True)


def main():
    check_segnali()
    check_wiring()
    check_incroci()
    check_capienza_inviti()
    check_label_esistenti()
    check_store_picklabile()
    check_economia_punti()
    check_economia_scudi()
    check_prerequisiti_sequenza()
    check_congelamento_route_attiva()
    check_eventi_aede()
    check_eventi_caino()
    check_eventi_druso()
    check_eventi_icaro()
    check_eventi_ofelia()
    check_snodi()
    check_galleria_finali()
    check_deviazioni()
    check_revisione_finale()
    test_sequenza()
    test_fisso()
    test_inviti()
    test_pool()
    test_scadenza()
    test_scadenza_ofelia()
    test_cuore()
    test_doni()
    test_casuali()
    if FAILURES:
        print(f"{len(FAILURES)} FALLITI: {FAILURES}")
        sys.exit(1)
    print("tutti i casi ok")


if __name__ == "__main__":
    main()
