"""Accordo di genere verso il protagonista: scanner dei pattern sospetti.

Cerca nei dialoghi participi/aggettivi maschili in seconda persona che
dovrebbero usare [fin] o le variabili di protagonista.rpy ("sei arrivato",
"ti ho sottovalutato", "Zitto." a inizio battuta). Le battute rivolte a
personaggi maschili (Druso, Caino, Ottone, il corteggiatore di Ofelia...)
stanno nella WHITELIST: una voce per battuta, come sottostringa esatta.

Una riga nuova che scatta = o si mette [fin]/variabile, o (se e' rivolta a
un personaggio maschile) si aggiunge qui alla WHITELIST con un commento.

Uso: py -3 -I tests/test_genere.py
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROUTES = os.path.join(HERE, "..", "game", "capitoli")

# Participi dativi invarianti: con "ti ho <p.p.>" il participio non si
# accorda quando "ti" e' complemento di termine ("ti ho detto").
DATIVI = ("detto", "dato", "fatto", "chiesto", "insegnato", "mostrato",
          "mandato", "scritto", "letto", "offerto", "promesso", "giurato",
          "raccontato", "spiegato", "portato", "ordinato", "prestato",
          "pagato", "venduto", "lasciato", "indicato")

SOSPETTI = [
    re.compile(r"\b[Ss]ei \w+to\b"),
    re.compile(r"\b[Tt]i sei \w+to\b"),
    re.compile(r"\b[Tt]i ho (?!(?:%s)\b)\w+to\b" % "|".join(DATIVI)),
    re.compile(r"\b[Ee]ri \w+to\b"),
    re.compile(r"\b[Ss]arai \w+to\b"),
    re.compile(r'"Zitto[.,]'),
    re.compile(r'"Bravo[.,!]'),
    re.compile(r"\bsei (?:il|lo|un) nuovo\b"),
]

# Battute legittime: rivolte a personaggi maschili, o il "tu" non e' il
# protagonista. Sottostringa esatta della riga.
WHITELIST = (
    # Caino a Druso (cena dei fratelli, origliati in archivio).
    "sei svenuto alla vista di un'anatra sgozzata",
    "Ci sei seduto sopra da un minuto",
    # Ofelia al corteggiatore con le rose (serra, atto 1).
    "Ti sei preparato davanti allo specchio",
    # Caino a Ottone (dieci anni alla Proprieta').
    "Mia madre ti assunse. Io ti ho confermato",
    # Druso a Caino (cena dei fratelli).
    "Zitto, tu. Non dar[gli_t] idee",
    # Ofelia a Caino (patto a tre).
    "Ti ho visto arrossire sulla Calà",
    # Icaro a Caino (pipa alla fumeria).
    "Ti ho visto provarci e tossire",
)


def main():
    errori = []
    for radice, _d, files in os.walk(ROUTES):
        for nome in files:
            if not nome.endswith(".rpy"):
                continue
            percorso = os.path.join(radice, nome)
            with open(percorso, encoding="utf-8") as f:
                for num, riga in enumerate(f, 1):
                    testo = riga.strip()
                    # Solo righe di dialogo/narrazione (stringhe), non commenti.
                    if testo.startswith("#") or '"' not in testo:
                        continue
                    if any(w in riga for w in WHITELIST):
                        continue
                    for pat in SOSPETTI:
                        if pat.search(riga):
                            errori.append("%s:%d: %s [%s]" % (
                                os.path.relpath(percorso, HERE), num,
                                testo[:90], pat.pattern))
    for e in errori:
        print("FAIL:", e)
    if errori:
        print("%d FALLITI" % len(errori))
        sys.exit(1)
    print("tutti i casi ok")


if __name__ == "__main__":
    main()
