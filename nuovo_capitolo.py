"""Crea un capitolo nuovo dal modello in modelli/capitolo/.

Uso: py -3 -I -X utf8 nuovo_capitolo.py <id> <numero> "<titolo>"

Copia il modello in game/capitoli/<id>/ sostituendo __ID__, __NUMERO__ e
__TITOLO__, e crea le cartelle degli asset game/images|gui|audio/<id>/
(ognuna con un .gitkeep, cosi' git le tiene).
"""
import os
import re
import sys

RADICE = os.path.dirname(os.path.abspath(__file__))
MODELLO = os.path.join(RADICE, "modelli", "capitolo")
CARTELLE_ASSET = ("images", "gui", "audio")


def crea(cid, numero, titolo, radice_game):
    """Crea il capitolo e ritorna il percorso creato (radice_game/capitoli/<cid>)."""
    if not re.fullmatch(r"[a-z][a-z0-9_]*", cid or ""):
        raise ValueError("id non valido ([a-z][a-z0-9_]*): %r" % (cid,))
    if any(c in (titolo or "") for c in "\"\\{[\r\n"):
        raise ValueError("titolo non valido (niente virgolette, backslash, { [ o a capo): %r" % (titolo,))
    dest = os.path.join(radice_game, "capitoli", cid)
    if os.path.exists(dest):
        raise FileExistsError(dest)
    sost = (("__ID__", cid), ("__NUMERO__", str(int(numero))),
            ("__TITOLO__", titolo))
    for radice, _dirs, files in os.walk(MODELLO):
        rel = os.path.relpath(radice, MODELLO)
        cartella = dest if rel == "." else os.path.join(dest, rel)
        os.makedirs(cartella, exist_ok=True)
        for fn in files:
            with open(os.path.join(radice, fn), encoding="utf-8") as f:
                testo = f.read()
            for da, a in sost:
                testo = testo.replace(da, a)
            with open(os.path.join(cartella, fn.replace("__ID__", cid)),
                      "w", encoding="utf-8", newline="\n") as f:
                f.write(testo)
    for a in CARTELLE_ASSET:
        d = os.path.join(radice_game, a, cid)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, ".gitkeep"), "a").close()
    return dest


def main(argv):
    if len(argv) != 4:
        print('Uso: nuovo_capitolo.py <id> <numero> "<titolo>"')
        return 2
    try:
        dest = crea(argv[1], int(argv[2]), argv[3], os.path.join(RADICE, "game"))
    except (ValueError, FileExistsError) as e:
        print("Errore:", e)
        return 1
    print("Creato", dest)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
