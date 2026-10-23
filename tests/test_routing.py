"""Verifica il routing dei finali: chiama le funzioni pure di
game/routing_logic.py (le stesse che i .rpy usano con `jump expression`) e
controlla che ogni climax le usi davvero.

Uso: py -3 -I tests/test_routing.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROUTES = os.path.join(HERE, "..", "game", "routes")
sys.path.insert(0, os.path.join(HERE, "..", "game"))

import routing_logic as rl  # noqa: E402


def _aede(aff, segreto, lavoro, giuramento):
    return rl.finale_aede(aff, giuramento, lavoro, segreto)


def _ofelia(of=12, mancati=0, seconda=None, caino=0):
    return rl.finale_ofelia(of, mancati, seconda, caino)


def _poly_aede(sospetto=0, of=12, mancati=0, aede=13, giuramento=True,
               lavoro=True, segreto=True):
    return rl.finale_ofelia_poly_aede(sospetto, of, mancati, aede,
                                      giuramento, lavoro, segreto)


def _icaro(gender="f", aff=13, coperto=True, congelate=()):
    return rl.finale_icaro(gender, aff, coperto, set(congelate))


SCENARI = [
    # Aede (soglie e ordine invariati: good -> glauco -> aede -> neutral)
    ("aede: run perfetta, soglia esatta (13 = 12 + dono)",
     _aede(13, True, True, True), "good_end"),
    ("aede: run sdolcinata (cap6 ascoltarla blocca il good)",
     _aede(9, True, True, False), "neutral_end"),
    ("aede: run ostile, segreto tradito", _aede(-11, False, False, False),
     "bad_end_glauco"),
    ("aede: run fredda, segreto mantenuto", _aede(-4, True, False, True),
     "bad_end_aede"),
    ("aede: affinita' max con lavoro rifiutato", _aede(9, True, False, True),
     "neutral_end"),
    ("aede: 13 senza giuramento -> passeggero",
     _aede(13, True, True, False), "aede_passeggero"),
    ("aede: 13 lavoro rifiutato -> passeggero",
     _aede(13, True, False, True), "aede_passeggero"),
    ("aede: 12 senza giuramento -> neutral",
     _aede(12, True, True, False), "neutral_end"),
    ("ofelia + Aede: fallback passeggero di Aede",
     _poly_aede(of=5, giuramento=False), "aede_passeggero"),
    ("aede: vecchia soglia 12 con tutti i flag non basta",
     _aede(12, True, True, True), "neutral_end"),

    # Ofelia (good >= 12 e nessun mancato; passeggero >= 12 con un mancato;
    # bad sotto 8; poly Caino solo con Caino >= 13)
    ("ofelia sola: good a soglia esatta", _ofelia(12, 0), "ofelia_good"),
    ("ofelia sola: un mancato -> passeggero", _ofelia(14, 1),
     "ofelia_passeggero"),
    ("ofelia sola: 11 non basta", _ofelia(11, 0), "ofelia_neutral"),
    ("ofelia sola: neutral a soglia bad", _ofelia(8, 1), "ofelia_neutral"),
    ("ofelia sola: sotto 8 -> bad", _ofelia(7, 0), "ofelia_bad"),
    ("ofelia + Caino: un mancato -> passeggero", _ofelia(14, 1, "caino", 20),
     "ofelia_passeggero"),
    ("ofelia + Caino: good a tre", _ofelia(12, 0, "caino", 13),
     "ofelia_good_caino"),
    ("ofelia + Caino: Caino a 12 -> good sola", _ofelia(12, 0, "caino", 12),
     "ofelia_good"),
    ("ofelia + Caino congelato (seconda None) -> good sola",
     _ofelia(12, 0, None, 20), "ofelia_good"),
    ("ofelia + Caino: Ofelia sotto soglia -> neutral",
     _ofelia(11, 0, "caino", 20), "ofelia_neutral"),
    ("ofelia + Aede: good a due", _poly_aede(), "ofelia_good_aede"),
    ("ofelia + Aede: tempesta batte tutto", _poly_aede(sospetto=2),
     "ofelia_bad_tempesta"),
    ("ofelia + Aede: sospetto 1 non e' tempesta", _poly_aede(sospetto=1),
     "ofelia_good_aede"),
    ("ofelia + Aede: Aede senza giuramento -> good sola (coda amara)",
     _poly_aede(giuramento=False), "ofelia_good"),
    ("ofelia + Aede: Ofelia giu', fallback good Aede",
     _poly_aede(of=11), "good_end"),
    ("ofelia + Aede: due mancati, fallback good Aede",
     _poly_aede(mancati=2), "good_end"),
    ("ofelia + Aede: un mancato, fallback good Aede",
     _poly_aede(mancati=1), "good_end"),
    ("ofelia + Aede: fallback neutral", _poly_aede(of=5, aede=9),
     "neutral_end"),
    ("ofelia + Aede: fallback bad Glauco",
     _poly_aede(of=5, aede=2, segreto=False), "bad_end_glauco"),
    ("ofelia + Aede: fallback bad Aede", _poly_aede(of=5, aede=2),
     "bad_end_aede"),

    # Druso (good: coraggio e >= 15; neutral >= 8)
    ("druso: good a soglia esatta", rl.finale_druso(15, True), "druso_good"),
    ("druso: 15 senza coraggio -> passeggero", rl.finale_druso(15, False),
     "druso_passeggero"),
    ("druso: 14 senza coraggio -> neutral", rl.finale_druso(14, False),
     "druso_neutral"),
    ("druso: coraggio a 14 -> neutral", rl.finale_druso(14, True),
     "druso_neutral"),
    ("druso: neutral a soglia esatta", rl.finale_druso(8, False),
     "druso_neutral"),
    ("druso: bad", rl.finale_druso(7, True), "druso_bad"),
    ("druso: uomo, primo passo falso avvisa",
     rl.druso_passo_falso("m", 0), (1, True, False)),
    ("druso: uomo, secondo passo falso congela",
     rl.druso_passo_falso("m", 1), (2, False, True)),
    ("druso: donna, passi falsi non contano",
     rl.druso_passo_falso("f", 1), (1, False, False)),

    # Icaro romance (solo donna): good >= 13 + coperto + non congelato
    ("icaro: good a soglia esatta", _icaro(), "icaro_good"),
    ("icaro: 13 senza coprirlo -> passeggero", _icaro(coperto=False),
     "icaro_passeggero"),
    ("icaro: congelato (gelosia) -> passeggero",
     _icaro(congelate=["icaro"]), "icaro_passeggero"),
    ("icaro: 12 senza coprirlo -> neutral", _icaro(aff=12, coperto=False),
     "icaro_neutral"),
    ("icaro: uomo 13 non coperto -> bro",
     _icaro(gender="m", aff=13, coperto=False), "icaro_bro_end"),
    ("icaro: 12 -> neutral", _icaro(aff=12), "icaro_neutral"),
    ("icaro: neutral a soglia esatta", _icaro(aff=6, coperto=False),
     "icaro_neutral"),
    ("icaro: bad", _icaro(aff=5), "icaro_bad"),
    # Icaro Bro (uomo): sempre icaro_bro_end, poi listino o conti
    ("bro: uomo sempre al finale Bro, anche a 20",
     _icaro("m", 20, True), "icaro_bro_end"),
    ("bro: uomo sempre al finale Bro, anche a 0",
     _icaro("m", 0, False), "icaro_bro_end"),
    ("bro: impegnato a 6 -> listino", rl.finale_bro(6, True),
     "icaro_bro_listino"),
    ("bro: impegnato a 5 -> conti", rl.finale_bro(5, True), "icaro_bro_conti"),
    ("bro: non impegnato -> conti", rl.finale_bro(15, False),
     "icaro_bro_conti"),
]


def _leggi(nome):
    with open(os.path.join(ROUTES, nome), encoding="utf-8") as f:
        return f.read()


def _corpo(src, label):
    return src.split("label %s:" % label)[1].split("\nlabel ")[0]


# Ogni climax deve delegare a routing_logic (niente soglie copiate nei .rpy).
WIRING = [
    ("aede_finali.rpy", "climax", "rl.finale_aede("),
    ("caino_finali.rpy", "caino_climax", "rl.finale_caino("),
    ("druso_finali.rpy", "druso_climax", "rl.finale_druso("),
    ("icaro_finali.rpy", "icaro_climax", "rl.finale_icaro("),
    ("icaro_finali.rpy", "icaro_bro_end", "rl.finale_bro("),
    ("ofelia_finali.rpy", "ofelia_routing", "rl.finale_ofelia("),
    ("ofelia_finali.rpy", "ofelia_poly_aede_routing",
     "rl.finale_ofelia_poly_aede("),
]


def main():
    failures = 0
    for nome, got, atteso in SCENARI:
        ok = got == atteso
        failures += 0 if ok else 1
        print(f"{'PASS' if ok else 'FAIL'}: {nome} -> {got} (atteso {atteso})")
    for f, label, chiamata in WIRING:
        ok = chiamata in _corpo(_leggi(f), label)
        failures += 0 if ok else 1
        print(f"{'PASS' if ok else 'FAIL'}: wiring {label} usa {chiamata}")
    if failures:
        print(f"{failures} FALLITI")
        sys.exit(1)
    print(f"{len(SCENARI)}/{len(SCENARI)} scenari ok, "
          f"{len(WIRING)}/{len(WIRING)} wiring ok")


if __name__ == "__main__":
    main()
