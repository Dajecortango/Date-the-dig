"""Verifica il motore puro del calendario (game/calendario_logic.py).

Uso: py -3 -I tests/test_calendario.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "game"))

import calendario_logic as cl  # noqa: E402

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


def check_eventi_druso():
    ev = open(os.path.join(HERE, "..", "game", "routes", "druso_route.rpy"),
              encoding="utf-8").read()
    for eid in ('"druso_ev1"', '"druso_ev2"', '"druso_ev3"', '"druso_ev4"'):
        check("evento druso " + eid, eid in ev, True)
    check("druso_ev4 richiede ev3", '"druso_ev3" in v["visti"]' in ev, True)
    check("druso_ev4 muore dopo scelta_cuore",
          '"scelta_cuore" not in v["visti"]' in ev, True)
    for lbl in ("impegno_druso", "druso_fiaccolata", "druso_climax",
                "druso_good", "druso_neutral", "druso_bad"):
        check("label " + lbl, "label " + lbl + ":" in ev, True)
    check("passi falsi solo per uomini",
          'player_gender == "m"' in ev and "druso_passi_falsi" in ev, True)


def check_eventi_icaro():
    ev = open(os.path.join(HERE, "..", "game", "routes", "icaro_route.rpy"),
              encoding="utf-8").read()
    for eid in ('"icaro_ev1"', '"icaro_ev2"', '"icaro_ev3"'):
        check("evento icaro " + eid, eid in ev, True)
    for lbl in ("impegno_icaro", "impegno_bro", "icaro_fiaccolata",
                "icaro_climax", "icaro_good", "icaro_bro_end"):
        check("label " + lbl, "label " + lbl + ":" in ev, True)
    check("gate di genere sul climax",
          'player_gender == "m"' in ev and "icaro_bro_end" in ev, True)
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
    check("candidata ofelia soglia 8", "store.ofelia_affinity >= 8" in ev, True)
    check("coppie poly", '"ofelia+aede"' in ev and '"ofelia+caino"' in ev, True)
    check("route_seconda impostata", "route_seconda =" in ev, True)
    check("aede_cap6 anche da seconda", 'v["route_seconda"] == "aede"' in ev, True)
    cap6 = ev.split('"id": "aede_cap6"')[1].split("},")[0]
    check("aede_cap6 salta se sospetto", 'v["aede_sospetto"] < 2' in cap6, True)
    cal = _leggi("calendario.rpy")
    check("cal_vars aede_sospetto", '"aede_sospetto": store.aede_sospetto' in cal, True)
    check("dispatch ofelia", ev.count('cal_route == "ofelia"') >= 2, True)


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
    check("screen ritorna id non dict", 'Return(("evento", inv["id"]))' in cal, True)
    check("niente dict evento in _return", 'Return(("evento", ev))' in cal, False)
    check("loop usa cal_fisso_id", "cal_fisso_id" in cal, True)
    check("niente cal_evento_corrente", "cal_evento_corrente" in cal, False)
    check("niente inviti_fatti", "inviti_fatti" in cal, False)
    check("info inviti espone scade", '"scade": bool(e.get("scade", False))' in cal, True)
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
    check("druso: good end (13) raggiungibile", druso_max >= 13, True)
    dr = _leggi(os.path.join("routes", "druso_route.rpy"))
    check("druso good end soglia 13", "druso_affinity >= 13" in dr, True)
    check("icaro: good end (10) raggiungibile", icaro_max >= 10, True)
    ic2 = _leggi(os.path.join("routes", "icaro_route.rpy"))
    check("icaro good end soglia 10", "icaro_affinity >= 10" in ic2, True)
    sn = _leggi(os.path.join("routes", "snodi.rpy"))
    check("soglie druso 9F/11M", "(9 if f else 11)" in sn, True)
    check("soglie icaro 7F/6M", "(7 if f else 6)" in sn, True)
    ofelia_max = _max_punti("ofelia_affinity")
    check("ofelia: impegno (8) raggiungibile", ofelia_max >= 8, True)
    check("ofelia: good end (11) raggiungibile", ofelia_max >= 11, True)
    # Percorso segreto con Aede: corte/eventi pre-cuore danno al massimo 9,
    # la mano di Aede sulla Calà +1, il climax di Aede non tocca Ofelia ma
    # ev4 (+2) si'. Budget 9 + 1 + 2 = 12: il good (>= 11) tollera un errore
    # solo se anche il ramo "mano di Aede" premia Ofelia.
    fin = _leggi(os.path.join("routes", "ofelia_finali.rpy"))
    fiac_aede = fin.split("label ofelia_fiaccolata_aede:")[1].split("\nlabel ")[0]
    ramo_aede = fiac_aede.split("call cap5")[1].split('"Prendere la mano di Ofelia"')[0]
    check("ofelia: mano di Aede premia la discrezione",
          "ofelia_affinity += 1" in ramo_aede, True)
    ic = _leggi(os.path.join("routes", "icaro_route.rpy"))
    for soglia in (">= 2", ">= 4", ">= 6"):
        check("icaro scala eventi " + soglia,
              '"icaro_affinity"] ' + soglia in ic.replace("v[", "["), True)


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
    of = _leggi(os.path.join("routes", "ofelia_route.rpy"))
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


def test_scadenza():
    a = {"id": "of1", "scade": True}
    b = {"id": "ae1"}
    c = {"id": "of2", "scade": True}
    check("scadenza: scelto altro", cl.inviti_ignorati([a, b], "ae1"), ["of1"])
    check("scadenza: scelto lei", cl.inviti_ignorati([a, b], "of1"), [])
    check("scadenza: attivita'", cl.inviti_ignorati([a, b, c], None), ["of1", "of2"])
    check("scadenza: nessuna", cl.inviti_ignorati([b], None), [])


def check_eventi_ofelia():
    ev = _leggi(os.path.join("routes", "ofelia_route.rpy"))
    check("hook scadenza registrato",
          "cal_inviti_ignorati_hooks.append(ofelia_scadenza)" in ev, True)
    check("congela a 2 mancati", "ofelia_mancati >= 2" in ev, True)
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
    fin = _leggi(os.path.join("routes", "ofelia_finali.rpy"))
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
          "ofelia_affinity >= 11 and ofelia_mancati <= 1" in fin, True)
    check("tempesta prima del good", fin.index("aede_sospetto >= 2") <
          fin.index("label ofelia_good_aede:"), True)
    check("cartello route", "TANTO BELLA QUANTO LETALE" in fin, True)
    check("fallback poly include good Aede",
          "jump good_end" in fin.split("label ofelia_poly_aede_routing:")[1]
          .split("\nlabel ")[0], True)
    ae = _leggi(os.path.join("routes", "aede_finali.rpy"))
    check("innesto poly nel climax Aede", 'route_seconda == "aede"' in ae, True)


def main():
    check_wiring()
    check_incroci()
    check_label_esistenti()
    check_store_picklabile()
    check_economia_punti()
    check_prerequisiti_sequenza()
    check_congelamento_route_attiva()
    check_eventi_aede()
    check_eventi_caino()
    check_eventi_druso()
    check_eventi_icaro()
    check_eventi_ofelia()
    check_snodi()
    test_sequenza()
    test_fisso()
    test_inviti()
    test_pool()
    test_scadenza()
    if FAILURES:
        print(f"{len(FAILURES)} FALLITI: {FAILURES}")
        sys.exit(1)
    print("tutti i casi ok")


if __name__ == "__main__":
    main()
