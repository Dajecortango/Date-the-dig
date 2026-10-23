"""Raggiungibilita' del semestre: simulazione esaustiva (tests/sim_semestre.py)
su calendario, catene, slot, inviti a scadenza, territori, doni e minigiochi,
con i punti ricavati dai .rpy.

Controlla, per protagonista donna e uomo:
- ogni invito dei cinque personaggi di route e' giocabile in una partita
  dedicata a quel personaggio (cuore scelto e route viva);
- il massimo a IV/28 raggiunge la soglia del cuore (rl.cuore_candidati,
  quindi anche rl.CUORE_REQUISITI) e il massimo finale la soglia del good
  (Icaro uomo: rl.ICARO_BRO; Ofelia: senza inviti mancati);
- dalla soglia del cuore, scegliendo male dopo il cuore, si arriva sotto le
  soglie dei bad end (e nella fascia dei neutral), route ancora viva;
  per Caino anche con le trappole (rl.CAINO_TRAPPOLE_BAD);
- le coppie Ofelia+Aede e Ofelia+Caino raggiungono entrambe il good.

Uso: py -3 -I -X utf8 tests/test_raggiungibilita.py
"""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sim_semestre as ss  # noqa: E402
import routing_logic as rl  # noqa: E402

FAILURES = []
GENERI = ("f", "m")


def check(nome, ok, dettaglio=""):
    if not ok:
        FAILURES.append(nome)
    print(f"{'PASS' if ok else 'FAIL'}: {nome}" + (f": {dettaglio}" if dettaglio else ""))


# Coerenza: cio' che il simulatore modella a mano deve esistere ancora nei
# sorgenti cosi' com'e'. Se un frammento sparisce, il modello va rivisto.
COERENZA = [
    ("calendario.rpy", "cal_label = cl.pesca_variante(cal_pool or [], eventi_visti)"),
    ("calendario.rpy", "call eco_dopo_attivita(att_id, cal_att_char)"),
    ("calendario.rpy", "call dono_check(cal_sel_char)"),
    ("calendario.rpy", "evs = cl.trova_inviti(momento, EVENTI, cal_vars(), store.eventi_visti)"),
    ("calendario.rpy", "if e.get(\"char\") in (None, store.route_attiva,"),
    ("calendario.rpy", "\"flag_accetta_lavoro\": store.flag_accetta_lavoro,"),
    ("economia.rpy", "call expression \"dono_\" + char"),
    ("economia.rpy", "dono_tenuto = mercato_scelta"),
    ("economia.rpy", "for k in MERCATO_LUNE.get(cal_luna, MERCATO_LUNE[1])"),
    ("economia.rpy", "lambda v: v[\"scudi\"] >= 2 and v[\"dono_tenuto\"] is None))"),
    ("economia.rpy", "store.scudi = max(0, store.scudi - n)"),
    ("economia.rpy", "if char:\n        call dono_check(char)"),
    (os.path.join("routes", "ofelia_core.rpy"), "rlz.ofelia_esiti_scadenza("),
    (os.path.join("routes", "ofelia_core.rpy"), "store.ofelia_affinity -= 1"),
    (os.path.join("routes", "ofelia_core.rpy"), "cal_inviti_ignorati_hooks.append(ofelia_scadenza)"),
    (os.path.join("routes", "icaro_eventi.rpy"), "and ev.get(\"char\") not in (None, \"icaro\")"),
    (os.path.join("routes", "icaro_eventi.rpy"), "and store.icaro_affinity >= ICARO_GELOSIA"),
    (os.path.join("routes", "icaro_eventi.rpy"), "and store.route_attiva is None"),
    (os.path.join("routes", "druso_core.rpy"), "store.druso_affinity -= 1"),
    (os.path.join("routes", "snodi.rpy"), "for char, delta in ((scelto, 1), (lasciato, -1)):"),
    (os.path.join("routes", "snodi.rpy"), "cuore_lista = cuore_candidati()"),
    (os.path.join("routes", "snodi.rpy"), "$ cuore_coppia = rl.risolvi_coppia(impegno_of, impegno_altro, cuore_altro)"),
    (os.path.join("routes", "snodi.rpy"), "if impegno_esito:\n        $ route_attiva = cuore_scelto"),
]


def test_coerenza():
    print("-- coerenza modello / sorgenti")
    for rel, frammento in COERENZA:
        testo = ss.TESTI[os.path.join(ss.MAL, rel)]
        check(f"{rel} contiene {frammento.splitlines()[0][:60]!r}", frammento in testo)
    corpo = ss.LABEL_TESTO.get("ev_scelta_cuore", "")
    for lab in ss.IMPEGNO.values():
        check(f"ev_scelta_cuore chiama {lab}", "call " + lab in corpo)
    for e in ss.EVENTI:
        if e["label"] not in ss.LABELS:
            check(f"label dell'evento {e['id']}", False, e["label"] + " inesistente")
    for a, (_ch, pool, _c, _s) in ss.POOL.items():
        for lab in pool:
            if lab not in ss.LABELS:
                check(f"label del pool {a}", False, lab + " inesistente")
    for ch in ss.CHARS:
        check(f"dono_{ch} esiste", "dono_" + ch in ss.LABELS)
    # Il modello deve vedere punti veri: ogni personaggio ha inviti con
    # punti (protezione contro un analizzatore che non conta piu' nulla).
    base = {ss.VAR[c]: 20 for c in ss.CHARS}
    base.update(scudi=3, caino_trappole=0, aede_sospetto=0, druso_passi_falsi=0, ofelia_mancati=0,
                route_attiva=None, route_seconda=None, player_gender="f",
                congelate=frozenset(), eventi_visti=frozenset(), cal_luna=1,
                dono_tenuto=None)
    for ch in ss.CHARS:
        i = ss.TI[ss.VAR[ch]]
        tot = sum(max(d[i] for d, _c, _m in ss.esiti_label(e["label"], base))
                  for e in ss.EVENTI if e.get("char") == ch and e["tipo"] == "invito")
        check(f"inviti di {ch} con punti (somma dei massimi {tot})", tot > 0)


def _valore(t, gender):
    """Soglia del good (Icaro uomo: Bro listino)."""
    if t == "icaro" and gender == "m":
        return rl.ICARO_BRO
    return rl.GOOD[t]


def _obj_max(t):
    def obj(f):
        ok_extra = t != "ofelia" or f["mancati"] <= rl.OFELIA_MANCATI_MAX
        return (f["alive"], ok_extra, f["aff"][t])
    return obj


def test_massimi():
    print("-- massimi a IV/28 e finali")
    for g in GENERI:
        soglie = rl.cuore_soglie(g == "f")
        for t in ss.CHARS:
            r = ss.run([t], g, seq=ss.PRE, al_cuore=True,
                       obj=lambda f, t=t: (t in f["candidati"], f["aff"][t]))
            check(f"{g} {t}: candidato al cuore a IV/28",
                  r[0][0] and r[0][1] >= soglie[t],
                  f"max {r[0][1]}, soglia {soglie[t]}")
            r = ss.run([t], g, route=t, obj=_obj_max(t))
            soglia = _valore(t, g)
            check(f"{g} {t}: massimo finale >= {soglia}",
                  r[0][0] and r[0][1] and r[0][2] >= soglia,
                  f"max {r[0][2]} (route viva {r[0][0]}, extra {r[0][1]})")


def test_inviti():
    print("-- inviti giocabili")
    for t in ss.CHARS:
        mancano = {e["id"] for e in ss.EVENTI
                   if e["tipo"] == "invito" and e.get("char") == t}
        totale = len(mancano)
        for g in GENERI:
            while mancano:
                r = ss.run([t], g, route=t,
                           obj=lambda f, m=frozenset(mancano), t=t:
                           (f["alive"], len(m & f["visti"]), f["aff"][t]))
                nuovi = mancano & r[1]["visti"] if r[0][0] else set()
                if not nuovi:
                    break
                mancano -= nuovi
        check(f"{t}: {totale - len(mancano)}/{totale} inviti giocabili su route",
              not mancano, "mai giocabili: " + ", ".join(sorted(mancano)) if mancano else "")


def _cuori(t, g):
    """Stati alla scelta del cuore da cui ripartire: candidato con
    l'affinita' piu' bassa, con meno scene viste, con meno scene sue."""
    def sue(f):
        return sum(1 for x in f["visti"]
                   if ss.EV.get(x, {}).get("char") == t
                   or any(x in p for c, p, _c, _s in ss.POOL.values() if c == t))
    out = []
    for crit in (lambda f: -f["aff"][t], lambda f: -len(f["visti"]), lambda f: -sue(f)):
        r = ss.run([t], g, seq=ss.PRE, al_cuore=True, sempre_passa=True,
                   obj=lambda f, crit=crit: (t in f["candidati"], crit(f)))
        if r[0][0]:
            out.append(r[1]["stato"])
    return out


def _dopo_cuore(t, g, obj, riuscito, mode_post="all"):
    """Miglior obj dopo il cuore, partendo dalla soglia del cuore. Prima da
    pochi stati al cuore (veloce); se non basta, ricerca congiunta su tutto
    il semestre (prima del cuore verso l'alto con "passa" sempre offerto,
    dopo il cuore mode_post)."""
    best = None
    for st in _cuori(t, g):
        r = ss.run([t], g, route=t, mode="all", clamp_cuore=True, inizio=st, obj=obj)
        if best is None or r[0] > best[0]:
            best = r
    if best is None or not riuscito(best[0]):
        r = ss.run([t], g, route=t, mode="max", mode_post=mode_post,
                   clamp_cuore=True, sempre_passa=True, obj=obj)
        if best is None or r[0] > best[0]:
            best = r
    return best


def test_finali_bassi():
    print("-- bad e neutral raggiungibili dalla soglia del cuore")
    bad = {"aede": rl.AEDE_BAD, "caino": rl.CAINO_BAD, "druso": rl.DRUSO_NEUTRAL,
           "icaro": rl.ICARO_NEUTRAL, "ofelia": rl.OFELIA_BAD}
    for g in GENERI:
        for t in ss.CHARS:
            soglia_bad = rl.ICARO_BRO if (t == "icaro" and g == "m") else bad[t]
            nome_bad = "bro conti" if (t == "icaro" and g == "m") else "bad"
            r = _dopo_cuore(t, g, lambda f, t=t: (f["alive"], -f["aff"][t]),
                            lambda p, s=soglia_bad: p[0] and -p[1] < s, "min")
            minimo = -r[0][1] if r and r[0][0] else None
            check(f"{g} {t}: {nome_bad} (< {soglia_bad}) raggiungibile",
                  minimo is not None and minimo < soglia_bad,
                  f"minimo finale {minimo} dalla soglia del cuore "
                  f"{rl.cuore_soglie(g == 'f')[t]}")
            if t == "icaro" and g == "m":
                continue
            lo, hi = bad[t], rl.GOOD[t]

            def neutro(f, t=t, lo=lo, hi=hi):
                ok = lo <= f["aff"][t] < hi
                if t == "caino":
                    ok = ok and f["trap"] < rl.CAINO_TRAPPOLE_BAD
                return (f["alive"], ok)
            r = _dopo_cuore(t, g, neutro, lambda p: p == (True, True))
            check(f"{g} {t}: neutral ({lo}..{hi - 1}) raggiungibile",
                  bool(r) and r[0] == (True, True))
        # Caino: bad per trappole, route viva.
        r = ss.run(["caino"], g, route="caino", mode="maxtrap",
                   obj=lambda f: (f["alive"], f["trap"]))
        check(f"{g} caino: bad per trappole (>= {rl.CAINO_TRAPPOLE_BAD}) su route viva",
              r[0][0] and r[0][1] >= rl.CAINO_TRAPPOLE_BAD, f"max trappole {r[0][1]}")


def test_coppie():
    print("-- poliamore")
    for altro in ("aede", "caino"):
        for g in GENERI:
            def obj(f, altro=altro):
                extra = f["mancati"] <= rl.OFELIA_MANCATI_MAX
                if altro == "aede":
                    extra = extra and f["sosp"] < rl.AEDE_SOSPETTO_TEMPESTA
                manca = (min(f["aff"]["ofelia"] - rl.GOOD["ofelia"], 0)
                         + min(f["aff"][altro] - rl.GOOD[altro], 0))
                return (f["alive"], extra, manca, f["aff"]["ofelia"], f["aff"][altro])
            r = ss.run(["ofelia", altro], g, route="ofelia", seconda=altro,
                       mode="somma", obj=obj)
            ok = r[0][0] and r[0][1] and r[0][2] == 0
            check(f"{g} ofelia+{altro}: entrambi al good", ok,
                  f"ofelia {r[0][3]}/{rl.GOOD['ofelia']}, {altro} {r[0][4]}/"
                  f"{rl.GOOD[altro]} (route viva {r[0][0]}, mancati/sospetto ok {r[0][1]})")


def main():
    t0 = time.time()
    test_coerenza()
    test_massimi()
    test_inviti()
    test_finali_bassi()
    test_coppie()
    check("analisi dei label senza anomalie", not ss.ANOMALIE, "; ".join(ss.ANOMALIE))
    print(f"({time.time() - t0:.1f} s)")
    if FAILURES:
        print(f"{len(FAILURES)} FALLITI: {FAILURES}")
        sys.exit(1)
    print("tutti i casi ok")


if __name__ == "__main__":
    main()
