"""Grafie canoniche del lore (docs/lore.md) nei file di gioco.

Ogni voce: (nome canonico, regex delle grafie sbagliate). Una grafia nuova
sbagliata in un .rpy/.py di game/ = FAIL. Il canone vive in docs/lore.md;
se il canone cambia, aggiornare lì e qui.

Uso: py -3 -I tests/test_lore.py
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.join(HERE, "..", "game")

SBAGLIATE = [
    ("Allmän", re.compile(r"Allm[aà]n\b")),
    ("la Calà", re.compile(r"\bCala\b")),
    ("Columna Lactaria", re.compile(r"Colonna Lactaria|Columna Lattaria")),
    ("Rocca Tempesta", re.compile(r"Roccatempesta|Rocca tempesta")),
    ("Yr-Drazul", re.compile(r"(?<!Yr-)Drazul")),
    ("Athlion", re.compile(r"Athlon\b|Atlion|Atlhion")),
    ("Hammergrad", re.compile(r"Hammergard")),
    ("Rurikstad", re.compile(r"Rurikstadt")),
    ("Glostok", re.compile(r"Glostock")),
    ("Collifreddi", re.compile(r"Colli [Ff]reddi|Collifredi\b")),
    ("Briseide", re.compile(r"Briseida\b")),
    ("Ippodamia", re.compile(r"Ippodamea|Ipodamia")),
    ("Zefiro", re.compile(r"Zeffiro")),
    ("Eburnea", re.compile(r"Eburnia")),
    ("Mercuzio", re.compile(r"Mercutio")),
    ("Lenora", re.compile(r"Leonora")),
    ("Draken", re.compile(r"Drakken")),
    ("Malacorte", re.compile(r"Mala [Cc]orte|Malacorta")),
    ("Gunnari", re.compile(r"\bGunar[io]\b|Gunnarr|Gunnaris\b")),
    ("Altafresia", re.compile(r"Alta [Ff]resia|Altafrisia")),
    ("Helograd", re.compile(r"Heliograd|Hellograd")),
    ("Rundeberg", re.compile(r"Runde[nr]berg|Rundberg")),
    ("Proserpina", re.compile(r"Proserpine\b|Prosperina")),
    # Nomi rinominati dal committente (2026-10-28): le grafie vecchie non tornano.
    ("Epiro / Lisandra (ex Lisandro)", re.compile(r"\bLisandro\b")),
    ("Pallante (ex Teucro)", re.compile(r"\bTeucro\b")),
    ("Bia (ex Milone)", re.compile(r"\bMilone\b")),
    ("sigillo di Lenora: corona", re.compile(r"corvo su un ramo")),
    # Il grido del Codice e' sempre maiuscolo: "TESCHIO!".
    # "del Teschio!" a fine frase e' il Codice, non il grido.
    ("TESCHIO!", re.compile(r"(?<!del )\bTeschio!")),
]


def main():
    errori = []
    for radice, dirs, files in os.walk(GAME):
        if "tl" in dirs:
            dirs.remove("tl")  # traduzioni di sistema, non lore
        for nome in files:
            if not nome.endswith((".rpy", ".py")):
                continue
            percorso = os.path.join(radice, nome)
            with open(percorso, encoding="utf-8") as f:
                for num, riga in enumerate(f, 1):
                    for canonico, pat in SBAGLIATE:
                        if pat.search(riga):
                            errori.append("%s:%d: atteso %r: %s" % (
                                os.path.relpath(percorso, HERE), num,
                                canonico, riga.strip()[:80]))
    for e in errori:
        print("FAIL:", e)
    if errori:
        print("%d FALLITI" % len(errori))
        sys.exit(1)
    print("tutti i casi ok")


if __name__ == "__main__":
    main()
