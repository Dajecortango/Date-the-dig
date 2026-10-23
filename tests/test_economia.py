"""Verifica gli usi degli Scudi (economia_logic.py) e la coerenza di
economia_extra.rpy (reazioni ai doni, label registrate, sprite), in
game/capitoli/malandrini/.

Uso: py -3 -I tests/test_economia.py
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.join(HERE, "..", "game")
# Cartella del capitolo Malandrini, relativa a GAME.
MAL_REL = os.path.join("capitoli", "malandrini")
sys.path.insert(0, HERE)
from percorsi import prepara_import  # noqa: E402
prepara_import()

import economia_logic as ecl  # noqa: E402

FAILURES = []

GUSTI = {
    "aede": ("pietra", "fiori"), "ofelia": ("spillone", "fiori"),
    "caino": ("idromele", "vino"), "druso": ("taccuino", "ballate"),
    "icaro": ("erba", "dadi"),
}
DONI = ["pietra", "spillone", "idromele", "taccuino", "erba", "vino",
        "fiori", "dadi", "ballate"]


def check(nome, got, atteso):
    ok = got == atteso
    if not ok:
        FAILURES.append(nome)
    print(f"{'PASS' if ok else 'FAIL'}: {nome}: {got!r} (atteso {atteso!r})")


def leggi(rel):
    with open(os.path.join(GAME, rel), encoding="utf-8") as f:
        return f.read()


def test_soffiate():
    check("soffiata: tutti tranne caino prima dell'Adunanza",
          ecl.soffiata_candidati(GUSTI, set(), [], set(), set()),
          ["aede", "ofelia", "druso", "icaro"])
    check("soffiata: caino dopo l'Adunanza",
          "caino" in ecl.soffiata_candidati(GUSTI, set(), [], set(), {"adunanza"}),
          True)
    check("soffiata: esclusi doni dati, gia' rivelati, congelati",
          ecl.soffiata_candidati(GUSTI, {"aede"}, ["ofelia"], {"icaro"},
                                 {"adunanza"}),
          ["caino", "druso"])
    check("soffiata: nessuno", ecl.soffiata_candidati(
        GUSTI, set(GUSTI), [], set(), {"adunanza"}), [])


def test_debito():
    check("debito: offerto a borsa vuota",
          ecl.debito_offribile(0, None, 2, set()), True)
    check("debito: non con 3 Scudi", ecl.debito_offribile(0, None, 3, set()), False)
    check("debito: non due volte",
          ecl.debito_offribile(0, "saldato", 0, set()), False)
    check("debito: non con debito aperto",
          ecl.debito_offribile(6, None, 0, set()), False)
    check("debito: non da Icaro congelato",
          ecl.debito_offribile(0, None, 0, {"icaro"}), False)
    sc = ecl.debito_scadenza(10)
    check("debito: scadenza a 9 slot", sc, 19)
    check("debito: non saldabile nello slot del prestito",
          ecl.debito_saldabile(6, sc, 10, 8), False)
    check("debito: saldabile dopo", ecl.debito_saldabile(6, sc, 11, 6), True)
    check("debito: saldabile all'ultimo slot", ecl.debito_saldabile(6, sc, 19, 6), True)
    check("debito: non saldabile senza Scudi", ecl.debito_saldabile(6, sc, 12, 5), False)
    check("debito: non saldabile se scaduto", ecl.debito_saldabile(6, sc, 20, 9), False)
    check("debito: scaduto dopo la scadenza", ecl.debito_scaduto(6, sc, 20), True)
    check("debito: non scaduto alla scadenza", ecl.debito_scaduto(6, sc, 19), False)
    check("debito: chiuso non scade", ecl.debito_scaduto(0, sc, 30), False)
    check("debito: restituzione 6", (ecl.DEBITO_PRESTITO, ecl.DEBITO_RESTITUZIONE), (5, 6))
    check("debito: slot restanti", ecl.slot_restanti(sc, 15), 4)


def test_scommessa():
    check("scommessa: vinta raddoppia", ecl.scommessa_delta(3, 0.2), 3)
    check("scommessa: persa", ecl.scommessa_delta(2, 0.5), -2)


def test_rpy():
    src = leggi(os.path.join(MAL_REL, "economia_extra.rpy"))
    eco = leggi(os.path.join(MAL_REL, "economia.rpy"))
    imgs = os.listdir(os.path.join(GAME, "images", "malandrini"))
    reaz = re.findall(r'\("(\w+)", "(\w+)"\): \("(\w+)", \[', src)
    attese = {(c, d) for c, g in GUSTI.items() for d in DONI if d not in g}
    check("doni: 35 reazioni neutre", len(attese), 35)
    check("doni: tutte le reazioni neutre presenti",
          sorted(attese - {(c, d) for c, d, _e in reaz}), [])
    check("doni: niente reazioni per preferito/detestato",
          sorted({(c, d) for c, d, _e in reaz} - attese), [])
    for c, d, e in reaz:
        check(f"doni: sprite {c} {e} esiste", f"{c} {e}.webp" in imgs, True)
    for c, g in GUSTI.items():
        check(f"doni: gusti {c} allineati a economia.rpy",
              '"%s": ("%s", "%s")' % (c, g[0], g[1]) in eco, True)
    tutto = src + leggi(os.path.join(MAL_REL, "routes", "ricordi.rpy"))
    for att, lbl in re.findall(r'ECO_DOPO_LABELS\.append\(\((None|"\w+"), "(\w+)"\)\)', tutto):
        check(f"eco dopo: label {lbl}(att_id) esiste",
              re.search(r"^label %s\(att_id\):" % lbl, tutto, re.M) is not None, True)
        check(f"eco dopo: {lbl} non usa il prefisso echi_", lbl.startswith("echi_"), False)
    for nome in re.findall(r"^default (\w+)", tutto, re.M):
        check(f"default {nome} unico nel gioco", _conta_default(nome), 1)


def _conta_default(nome):
    n = 0
    for radice, _d, files in os.walk(GAME):
        for f in files:
            if f.endswith(".rpy"):
                with open(os.path.join(radice, f), encoding="utf-8") as fh:
                    n += len(re.findall(r"^default %s\b" % nome, fh.read(), re.M))
    return n


def main():
    test_soffiate()
    test_debito()
    test_scommessa()
    test_rpy()
    if FAILURES:
        print(f"{len(FAILURES)} FALLITI: {FAILURES}")
        sys.exit(1)
    print("tutti i casi ok")


if __name__ == "__main__":
    main()
