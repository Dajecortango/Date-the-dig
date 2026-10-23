"""Percorsi comuni dei test e preparazione di sys.path."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.normpath(os.path.join(HERE, "..", "game"))
MAL = os.path.join(GAME, "capitoli", "malandrini")


def prepara_import():
    for p in (GAME, MAL):
        if p not in sys.path:
            sys.path.insert(0, p)
