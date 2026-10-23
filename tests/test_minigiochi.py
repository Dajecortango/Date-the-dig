"""Verifica la logica dei minigiochi (minigiochi_logic.py) e il
cablaggio in minigiochi.rpy (game/capitoli/malandrini/).

Uso: py -3 -I tests/test_minigiochi.py
"""
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.join(HERE, "..", "game")
sys.path.insert(0, HERE)
from percorsi import prepara_import  # noqa: E402
prepara_import()

import minigiochi_logic as mgl  # noqa: E402

FAILURES = []


def check(nome, got, atteso):
    ok = got == atteso
    if not ok:
        FAILURES.append(nome)
    print(f"{'PASS' if ok else 'FAIL'}: {nome}: {got!r} (atteso {atteso!r})")


def test_duello():
    check("segnali: almeno 6", len(mgl.SEGNALI_DUELLO) >= 6, True)
    mosse = [m for _t, m in mgl.SEGNALI_DUELLO]
    check("segnali: mosse valide", set(mosse) <= set(mgl.MOSSE), True)
    check("segnali: ogni mossa almeno 2 volte",
          all(mosse.count(m) >= 2 for m in mgl.MOSSE), True)
    check("segnali: testi unici", len({t for t, _m in mgl.SEGNALI_DUELLO}),
          len(mgl.SEGNALI_DUELLO))
    ok = True
    for seed in range(200):
        s = mgl.pesca_segnali(random.Random(seed))
        ok &= len(s) == 3 and len(set(s)) == 3
    check("segnali: 3 distinti per partita", ok, True)
    check("duello 3 -> vinto", mgl.esito_duello(3), "vinto")
    check("duello 2 -> vinto", mgl.esito_duello(2), "vinto")
    check("duello 1 -> perso", mgl.esito_duello(1), "perso")
    check("duello 0 -> perso", mgl.esito_duello(0), "perso")


def test_carte():
    ok = True
    posizioni = set()
    for seed in range(200):
        mani, idx = mgl.pesca_mani(random.Random(seed))
        posizioni.add(idx)
        ok &= len(mani) == 3 and len(set(mani)) == 3
        ok &= mani[idx] in mgl.MANI_TRUCCATE
        ok &= sum(m in mgl.MANI_TRUCCATE for m in mani) == 1
    check("carte: una sola mano truccata, al suo indice", ok, True)
    check("carte: la truccata cade in ogni posizione", posizioni, {0, 1, 2})
    check("carte: gesti puliti e truccati disgiunti",
          set(mgl.MANI_PULITE) & set(mgl.MANI_TRUCCATE), set())


def test_registri():
    ok = True
    cardia = True
    errate = set()
    for seed in range(300):
        righe, err = mgl.genera_registro(random.Random(seed))
        errate.add(err)
        ok &= len(righe) == 5
        ok &= [mgl.riga_giusta(r) for r in righe].count(False) == 1
        ok &= not mgl.riga_giusta(righe[err])
        ok &= all(r["totale"] > 0 for r in righe)
        ok &= len({r["nome"] for r in righe}) == 5
        cardia &= sum(r["nome"] == mgl.CARDIA for r in righe) == 1
    check("registri: 5 righe, una sola sbagliata", ok, True)
    check("registri: sempre una riga del Ceppo di Cardia", cardia, True)
    check("registri: l'errore cade in ogni riga", errate, {0, 1, 2, 3, 4})
    r = {"nome": "X", "voci": [1, 2, 3], "totale": 6}
    check("registri: testo riga", mgl.riga_testo(r), "X:  1 + 2 + 3 = 6")


def test_druso():
    tipi_ok = all(sorted(k for _t, k in b["risposte"]) == ["buona", "cattiva", "debole"]
                  for b in mgl.BATTUTE_DRUSO)
    check("druso: ogni battuta ha buona, debole, cattiva", tipi_ok, True)
    check("druso: almeno 3 battute", len(mgl.BATTUTE_DRUSO) >= 3, True)
    ok = True
    for seed in range(100):
        bb = mgl.pesca_battute(random.Random(seed))
        ok &= len(bb) == 3 and len({b["battuta"] for b in bb}) == 3
    check("druso: 3 battute distinte", ok, True)
    check("druso: silenzio vale come debole", mgl.VALORE_RISPOSTA["silenzio"],
          mgl.VALORE_RISPOSTA["debole"])
    check("druso: tempo ~6 s", 5 <= mgl.DRUSO_TEMPO <= 7, True)
    check("botta 3 -> vinta", mgl.esito_botta(3), "vinta")
    check("botta 2 -> vinta", mgl.esito_botta(2), "vinta")
    check("botta 1 -> pari", mgl.esito_botta(1), "pari")
    check("botta 0 -> pari", mgl.esito_botta(0), "pari")
    check("botta -1 -> persa", mgl.esito_botta(-1), "persa")
    check("botta -3 -> persa", mgl.esito_botta(-3), "persa")


def test_delta():
    check("delta: sempre entro +-1", all(abs(d) <= 1 for d in mgl.DELTA.values()), True)
    check("delta: lasciato = 0",
          [mgl.delta(g, "lasciato") for g in ("duello", "carte", "registri", "botta")],
          [0, 0, 0, 0])


def test_cablaggio():
    with open(os.path.join(GAME, "capitoli", "malandrini", "minigiochi.rpy"), encoding="utf-8") as f:
        src = f.read()
    for label in ("att_spada_duello", "att_fumeria_carte", "att_registri_conti",
                  "att_taverna_botta"):
        check("label %s" % label, re.search(r"^label %s:" % label, src, re.M) is not None, True)
        righe = []
        for riga in src.split("label %s:" % label, 1)[1].splitlines()[1:]:
            if riga.strip() and not riga[0].isspace():
                break
            righe.append(riga)
        corpo = "\n".join(righe)
        check("%s: finisce con return" % label, corpo.rstrip().splitlines()[-1].strip(), "return")
        check("%s: Lascia andare" % label, '"lascia"' in corpo, True)
    pool = re.findall(r'pool_aggiungi\("(\w+)", "(\w+)", 1\)', src)
    check("pool: attivita'", sorted(a for a, _l in pool),
          ["fumeria", "registri", "spada", "spada_p", "taverna"])
    fatti = re.findall(r'\{"id": "(mg_\w+)", "char": "(\w+)"', src)
    check("fatti: almeno uno per minigioco",
          {c for _i, c in fatti}, {"aede", "icaro", "caino", "druso"})
    usate = set(re.findall(r'\bv\["(\w+)"\]', src))
    blocco = re.search(r"CONSEGUENZE_VARS\.extend\(\[(.*?)\]\)", src, re.S).group(1)
    check("fatti: variabili esportate", sorted(usate - set(re.findall(r'"(\w+)"', blocco))), [])
    for n in usate:
        check("default %s" % n, re.search(r"^default %s\b" % n, src, re.M) is not None, True)


def main():
    test_duello()
    test_carte()
    test_registri()
    test_druso()
    test_delta()
    test_cablaggio()
    if FAILURES:
        print("\n%d FALLITI: %s" % (len(FAILURES), ", ".join(FAILURES)))
        sys.exit(1)
    print("\nTutto ok.")


if __name__ == "__main__":
    main()
