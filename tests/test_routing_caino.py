"""Verifica il routing dei finali di Caino (routing_logic.finale_caino, la
stessa funzione che caino_finali.rpy usa con `jump expression`).

Uso: python -I tests/test_routing_caino.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FINALI = os.path.join(HERE, "..", "game", "routes", "caino_finali.rpy")
sys.path.insert(0, os.path.join(HERE, "..", "game"))

import routing_logic as rl  # noqa: E402


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
    with open(FINALI, encoding="utf-8") as f:
        src = f.read()
    assert "rl.finale_caino(" in src, "caino_finali.rpy deve usare rl.finale_caino"
    failures = 0
    for nome, fid, mem, tra, dru, atteso in SCENARI:
        got = rl.finale_caino(fid, tra, mem, dru)
        ok = got == atteso
        failures += 0 if ok else 1
        print(f"{'PASS' if ok else 'FAIL'}: {nome} -> {got} (atteso {atteso})")
    if failures:
        sys.exit(1)
    print(f"{len(SCENARI)}/{len(SCENARI)} scenari ok")


if __name__ == "__main__":
    main()
