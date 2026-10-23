"""Motore puro del calendario dei Malandrini.

Nessun import Ren'Py: importabile sia dal gioco (init python) sia dai test.
Un "momento" e' una tupla (luna, giorno, slot). Un evento e' un dict con
chiavi: id, label, tipo ("fisso"|"invito"), char, e per i fissi luna/giorno/
slot, per gli inviti luna_min/slot (None = qualsiasi), cond opzionale
(callable(vars) -> bool).
"""

SLOTS = ("mattina", "pomeriggio", "sera")


def genera_sequenza(calendario):
    """Lista ordinata dei momenti giocabili: giorni/slot non elencati non
    esistono (il tempo in mezzo si salta)."""
    seq = []
    for luna in sorted(calendario):
        for giorno in calendario[luna]:
            for slot in giorno["slots"]:
                seq.append((luna, giorno["giorno"], slot))
    return seq


def _cond_ok(evento, vars):
    cond = evento.get("cond")
    return cond is None or bool(cond(vars))


def trova_fisso(momento, eventi, vars, visti):
    """Primo evento fisso del momento, con cond vera e non ancora visto."""
    luna, giorno, slot = momento
    for ev in eventi:
        if (ev["tipo"] == "fisso"
                and ev["luna"] == luna and ev["giorno"] == giorno
                and ev["slot"] == slot
                and ev["id"] not in visti
                and _cond_ok(ev, vars)):
            return ev
    return None


def trova_inviti(momento, eventi, vars, visti):
    """Inviti disponibili nel momento: luna raggiunta, slot compatibile,
    cond vera, non visti, personaggio non congelato."""
    luna, _giorno, slot = momento
    congelate = vars.get("congelate", set())
    out = []
    for ev in eventi:
        if (ev["tipo"] == "invito"
                and ev["luna_min"] <= luna
                and ev.get("slot") in (None, slot)
                and ev["id"] not in visti
                and ev.get("char") not in congelate
                and _cond_ok(ev, vars)):
            out.append(ev)
    return out


def pesca_variante(pool_ids, visti):
    """Prima variante del pool non vista; None = pool esaurito."""
    for vid in pool_ids:
        if vid not in visti:
            return vid
    return None


def inviti_ignorati(mostrati, scelto_id):
    """Id degli inviti a scadenza mostrati nello slot e non scelti
    (scelto_id None = il giocatore ha preso un'attivita')."""
    return [m["id"] for m in mostrati
            if m.get("scade") and m["id"] != scelto_id]
