"""Verifica che ogni file audio citato dal gioco esista in game/audio/.

Uso: py -3 -I tests/test_audio.py
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.join(HERE, "..", "game")

FAILURES = []


def check(nome, got, atteso):
    ok = got == atteso
    if not ok:
        FAILURES.append(nome)
    print(f"{'PASS' if ok else 'FAIL'}: {nome}: {got!r} (atteso {atteso!r})")


def main():
    citati = set()
    for radice, _d, files in os.walk(GAME):
        for n in files:
            if n.endswith(".rpy"):
                with open(os.path.join(radice, n), encoding="utf-8") as f:
                    citati |= set(re.findall(r'"(audio/[\w./-]+\.ogg)"', f.read()))
    check("audio citato dal gioco", len(citati) > 0, True)
    # Gli ambienti vivono nella registrazione del capitolo, non in audio.rpy.
    with open(os.path.join(GAME, "capitoli", "malandrini", "capitolo.rpy"),
              encoding="utf-8") as f:
        mal = set(re.findall(r'"(audio/[\w./-]+\.ogg)"', f.read()))
    for rel in ("audio/malandrini/amb_vento.ogg", "audio/malandrini/amb_pioggia.ogg", "audio/malandrini/campana.ogg"):
        check(f"{rel} nel capitolo Malandrini", rel in mal, True)
    for rel in sorted(citati):
        check(f"esiste {rel}", os.path.exists(os.path.join(GAME, rel)), True)
    if FAILURES:
        print(f"{len(FAILURES)} FALLITI: {FAILURES}")
        sys.exit(1)
    print("tutti i casi ok")


if __name__ == "__main__":
    main()
