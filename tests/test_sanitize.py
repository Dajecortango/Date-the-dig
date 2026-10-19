"""Verifica sanitize_name estraendo la funzione reale da aede_core.rpy.

Uso: python -I tests/test_sanitize.py
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CORE = os.path.join(HERE, "..", "game", "routes", "aede_core.rpy")


def load_sanitize():
    with open(CORE, encoding="utf-8") as f:
        src = f.read()
    m = re.search(r"(    def sanitize_name.*?return raw\n)", src, re.S)
    assert m, "sanitize_name non trovata in aede_core.rpy"
    code = "\n".join(line[4:] for line in m.group(1).splitlines())
    ns = {}
    exec(code, ns)  # codice nostro dal .rpy, non input esterno
    return ns["sanitize_name"]


CASI = [
    ("", "Elio"),
    ("   ", "Elio"),
    (None, "Elio"),
    ("{b}Ciao", "bCiao"),
    ("[player_name]", "player_name"),
    ("  Rurik  ", "Rurik"),
]


def check_wiring():
    """script.rpy deve davvero passare l'input per sanitize_name."""
    script = os.path.join(HERE, "..", "game", "script.rpy")
    with open(script, encoding="utf-8") as f:
        src = f.read()
    i_input = src.find("renpy.input")
    i_san = src.find("player_name = sanitize_name(player_name)")
    assert i_input != -1 and i_san != -1 and i_san > i_input, \
        "sanitize_name non collegata all'input in script.rpy"
    print("PASS: sanitize_name collegata in script.rpy")


def main():
    check_wiring()
    fn = load_sanitize()
    failures = 0
    for raw, atteso in CASI:
        got = fn(raw)
        ok = got == atteso
        failures += 0 if ok else 1
        print(f"{'PASS' if ok else 'FAIL'}: {raw!r} -> {got!r} (atteso {atteso!r})")
    if failures:
        sys.exit(1)
    print(f"{len(CASI)}/{len(CASI)} casi ok")


if __name__ == "__main__":
    main()
