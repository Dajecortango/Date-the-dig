"""Verifica il routing dei finali leggendo le condizioni reali da aede_finali.rpy.

Uso: python -I tests/test_routing.py
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FINALI = os.path.join(HERE, "..", "game", "routes", "aede_finali.rpy")


def load_branches():
    """Estrae [(condizione_python, label_destinazione), ...] dal blocco if/elif/else."""
    with open(FINALI, encoding="utf-8") as f:
        src = f.read()
    block = src.split("# Routing finali")[1]
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
        if eval(cond, {}, vars):  # condizioni scritte da noi nel .rpy, non input esterno
            return dest
    raise AssertionError("nessun ramo preso")


SCENARI = [
    # (nome, affinity, segreto, lavoro, giuramento, finale atteso)
    ("run perfetta", 16, True, True, True, "good_end"),
    ("run sdolcinata (cap6 ascoltarla blocca il good)", 9, True, True, False, "neutral_end"),
    ("run ostile, segreto tradito", -11, False, False, False, "bad_end_glauco"),
    ("run fredda, segreto mantenuto", -4, True, False, True, "bad_end_aede"),
    ("affinita' max con lavoro rifiutato (8 = massimo reale)", 8, True, False, True, "neutral_end"),
    ("run mai ostile, affinita' bassa ma non negativa", 4, True, True, False, "neutral_end"),
]


def main():
    branches = load_branches()
    assert len(branches) == 4, f"attesi 4 rami, trovati {len(branches)}: {branches}"
    assert branches[0][1] == "good_end", "il good end va controllato per primo"
    failures = 0
    for nome, aff, seg, lav, giu, atteso in SCENARI:
        got = route(
            branches,
            aede_affinity=aff,
            flag_segreto_svelo=seg,
            flag_accetta_lavoro=lav,
            flag_giuramento=giu,
        )
        ok = got == atteso
        failures += 0 if ok else 1
        print(f"{'PASS' if ok else 'FAIL'}: {nome} -> {got} (atteso {atteso})")
    if failures:
        sys.exit(1)
    print(f"{len(SCENARI)}/{len(SCENARI)} scenari ok")


if __name__ == "__main__":
    main()
