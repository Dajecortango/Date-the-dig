"""Verifica il routing dei finali di Caino leggendo le condizioni reali.

Uso: python -I tests/test_routing_caino.py
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FINALI = os.path.join(HERE, "..", "game", "routes", "caino_finali.rpy")


def load_branches():
    with open(FINALI, encoding="utf-8") as f:
        src = f.read()
    block = src.split("# Routing")[1]
    branches = []
    pat = re.compile(r"(?:if|elif)\s+(.+?):\s*\n\s*jump\s+(\w+)|else:\s*\n\s*jump\s+(\w+)")
    for m in pat.finditer(block):
        if m.group(3):
            branches.append(("True", m.group(3)))
            break
        branches.append((m.group(1), m.group(2)))
    return branches


def route(branches, **vars):
    for cond, dest in branches:
        if eval(cond, {}, vars):  # condizioni nostre dal .rpy
            return dest
    raise AssertionError("nessun ramo preso")


SCENARI = [
    # (nome, fiducia, memoria, trappole, druso, atteso)
    ("run perfetta", 17, 3, 0, 1, "caino_good_end"),
    ("fiducia alta ma 2 trappole", 14, 3, 2, 0, "caino_neutral_end"),
    ("fiducia alta ma memoria 1", 13, 1, 0, 0, "caino_neutral_end"),
    ("legame Druso, fiducia media", 8, 1, 1, 3, "caino_secret_end"),
    ("fiducia bassa", 3, 0, 1, 0, "caino_bad_end"),
    ("tre trappole", 7, 2, 3, 0, "caino_bad_end"),
    ("via di mezzo", 8, 2, 1, 1, "caino_neutral_end"),
    ("good batte segreto", 13, 2, 1, 3, "caino_good_end"),
]


def main():
    branches = load_branches()
    assert len(branches) == 4, f"attesi 4 rami: {branches}"
    assert branches[0][1] == "caino_good_end", "good va controllato per primo"
    failures = 0
    for nome, fid, mem, tra, dru, atteso in SCENARI:
        got = route(branches, caino_fiducia=fid, caino_memoria=mem,
                    caino_trappole=tra, caino_druso=dru)
        ok = got == atteso
        failures += 0 if ok else 1
        print(f"{'PASS' if ok else 'FAIL'}: {nome} -> {got} (atteso {atteso})")
    if failures:
        sys.exit(1)
    print(f"{len(SCENARI)}/{len(SCENARI)} scenari ok")


if __name__ == "__main__":
    main()
