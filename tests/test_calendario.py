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


def check_congelamento_route_attiva():
    """I2: route attiva ma congelata -> niente giuramento ne' climax romance."""
    sn = _leggi(os.path.join("routes", "snodi.rpy"))
    check("dispatch usa route_viva", "route_viva()" in sn, True)
    check("aede_cap6 esclude congelata",
          '"aede" not in v["congelate"]' in sn, True)


def check_incroci():
    ev = _leggi(os.path.join("routes", "incroci.rpy"))
    for eid in ('"trio_lenora"', '"incrocio_palestra"', '"incrocio_carte"'):
        check("evento incrocio " + eid, eid in ev, True)


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
    check_snodi()
    test_sequenza()
    test_fisso()
    test_inviti()
    test_pool()
    if FAILURES:
        print(f"{len(FAILURES)} FALLITI: {FAILURES}")
        sys.exit(1)
    print("tutti i casi ok")


if __name__ == "__main__":
    main()
