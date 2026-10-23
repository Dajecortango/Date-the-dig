"""Esporta i dialoghi del gioco in forma di copione, un file per route, in una cartella per capitolo.

Legge gli script .rpy di game/ e tiene solo cio che il giocatore legge:
battute, narrazione, cartelli `centered` e le risposte dei menu.
Niente comandi, condizioni o riferimenti al codice.

Uso: py -3 esporta_dialoghi.py   (scrive in dialoghi/<capitolo>/)
"""

import re
from pathlib import Path

RADICE = Path(__file__).parent
GIOCO = RADICE / "game"
USCITA = RADICE / "dialoghi"

# Route del capitolo I, "Malandrini" (relative a game/).
MAL = "capitoli/malandrini/routes/"

# Un capitolo nuovo si aggiunge con una voce: id -> {copione: [file in ordine di lettura]}.
# I copioni finiscono in dialoghi/<id>/.
CAPITOLI = {"malandrini": {
    "00_comune": [MAL + f for f in (
        "chapter1.rpy", "lenora.rpy", "snodi.rpy", "incroci.rpy", "attivita.rpy",
        "echi.rpy", "origliati.rpy")],
    "01_aede": [MAL + f for f in (
        "aede_core.rpy", "aede_atto1.rpy", "aede_interludi.rpy", "aede_eventi.rpy",
        "aede_atto2.rpy", "aede_finali.rpy")],
    "02_caino": [MAL + f for f in (
        "caino_core.rpy", "caino_atto1.rpy", "caino_eventi.rpy", "caino_atto2.rpy",
        "caino_finali.rpy")],
    "03_druso": [MAL + f for f in (
        "druso_core.rpy", "druso_atto1.rpy", "druso_eventi.rpy", "druso_atto2.rpy",
        "druso_finali.rpy")],
    "04_icaro": [MAL + f for f in (
        "icaro_core.rpy", "icaro_atto1.rpy", "icaro_eventi.rpy", "icaro_atto2.rpy",
        "icaro_finali.rpy")],
    "05_ofelia": [MAL + f for f in (
        "ofelia_core.rpy", "ofelia_atto1.rpy", "ofelia_eventi.rpy", "ofelia_atto2.rpy",
        "ofelia_finali.rpy")],
}}

RE_CHAR = re.compile(r'^define\s+(\w+)\s*=\s*Character\(\s*"([^"]*)"')
RE_LABEL = re.compile(r"^label\s+([\w.]+)")
RE_MENU = re.compile(r"^menu(\s+\w+)?\s*:")
RE_IF = re.compile(r"^(if|elif|else)\b\s*(.*?):$")
RE_SAY = re.compile(r'^(?:(\w+)(?:\s+[\w-]+)*\s+)?"((?:[^"\\]|\\.)*)"(.*)$')
RE_TAG = re.compile(r"\{[^}]*\}")
RE_VAR = re.compile(r"\[(\w+)\]")
# Testi che cambiano col genere scelto: maschile/femminile, come in protagonista.rpy.
VARIABILI = {
    "player_name": "<Nome>", "fin": "o/a", "figlio_t": "Figlio/a",
    "fratello_t": "fratellino/sorellina", "il_fratello_t": "il fratellino/la sorellina",
    "uomo_t": "uomo/donna", "un_t": "un/una", "Un_t": "Un/Una", "il_t": "il/la",
    "Il_t": "Il/La", "al_t": "al/alla", "gli_t": "gli/le", "lui_t": "lui/lei",
    "rivali_a_nome": "<Rivale 1>", "rivali_b_nome": "<Rivale 2>",
}


def personaggi():
    nomi = {"centered": None}
    for p in GIOCO.rglob("*.rpy"):
        for riga in p.read_text(encoding="utf-8").splitlines():
            m = RE_CHAR.match(riga.strip())
            if m:
                nomi[m.group(1)] = "TU" if m.group(2) == "[player_name]" else m.group(2).upper()
    return nomi


def pulisci(testo):
    testo = testo.replace('\\"', '"').replace("\\n", " ")
    testo = RE_TAG.sub("", testo)
    testo = RE_VAR.sub(lambda m: VARIABILI.get(m.group(1), m.group(0)), testo)
    return re.sub(r"\s+", " ", testo).strip()


def scena(label):
    return label.replace("_", " ").upper()


def copione(f, nomi):
    out = []
    blocchi = []  # indentazioni dei blocchi aperti (menu, risposte, varianti)
    in_label = False  # fuori dalle label c'e solo codice (init, python, screen)
    for grezza in (GIOCO / f).read_text(encoding="utf-8").splitlines():
        riga = grezza.strip()
        if not riga or riga.startswith("#"):
            continue
        ind = len(grezza) - len(grezza.lstrip())
        m = RE_LABEL.match(riga)
        if ind == 0:
            in_label = bool(m)
        if not in_label:
            continue
        while blocchi and ind <= blocchi[-1]:
            blocchi.pop()
        rientro = "    " * len(blocchi)

        if m:
            blocchi.clear()
            out.append(f"\n\n=== {scena(m.group(1))} ===\n")
            continue
        if RE_MENU.match(riga):
            out.append(f"\n{rientro}[SCELTA]")
            blocchi.append(ind)
            continue
        m = RE_IF.match(riga)
        if m:
            out.append(f"\n{rientro}[VARIANTE]")
            blocchi.append(ind)
            continue

        m = RE_SAY.match(riga)
        if not m:
            continue
        chi, testo, coda = m.group(1), pulisci(m.group(2)), m.group(3).strip()
        if chi is None and coda.endswith(":"):
            out.append(f"\n{rientro}> {testo}")
            blocchi.append(ind)
            continue
        if coda and not coda.startswith(("with", "(")) and coda != "nointeract":
            continue
        if chi is None:
            out.append(f"{rientro}{testo}")
        elif chi in nomi:
            nome = nomi[chi]
            out.append(f"{rientro}~ {testo} ~" if nome is None else f"{rientro}{nome}: {testo}")
    return out


def main():
    nomi = personaggi()
    for capitolo, copioni in CAPITOLI.items():
        cartella = USCITA / capitolo
        cartella.mkdir(parents=True, exist_ok=True)
        for route, files in copioni.items():
            righe = []
            for f in files:
                if (GIOCO / f).exists():
                    righe += copione(f, nomi)
            titolo = "PARTI COMUNI" if route == "00_comune" else "ROUTE " + route[3:].upper()
            testa = [
                f"DATE THE DIGNITAS — {titolo}",
                "",
                "NOME: battuta · testo semplice = narrazione · ~ testo ~ = cartello a schermo",
                "[SCELTA] seguita dalle risposte > possibili, con sotto cosa succede",
                "[VARIANTE] = testo che cambia in base alle scelte fatte prima",
                "<Nome> = nome scelto dal giocatore",
            ]
            (cartella / f"{route}.txt").write_text("\n".join(testa + righe) + "\n", encoding="utf-8")
            print(f"{capitolo}/{route}.txt: {len(righe)} righe")


if __name__ == "__main__":
    main()
