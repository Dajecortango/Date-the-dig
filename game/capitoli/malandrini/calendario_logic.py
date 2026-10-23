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


def momenti_fino_a(sequenza, idx, luna, giorno):
    """Giorni salienti (oggi compreso) da sequenza[idx] fino a (luna, giorno)
    escluso. 0 = il giorno e' oggi; None = gia' passato (o idx fuori)."""
    if idx >= len(sequenza):
        return None
    meta = (luna, giorno)
    oggi = sequenza[idx][:2]
    if oggi > meta:
        return None
    giorni = []
    for m in sequenza[idx:]:
        g = m[:2]
        if g >= meta:
            break
        if g not in giorni:
            giorni.append(g)
    return len(giorni)


def territorio_esaurito(pool_ids, visti, eco_pronto):
    """Voce del pianificatore senza niente di nuovo: pool finito e nessun
    eco pronto. Pool vuoto (ripetibili, mercato) = mai esaurito."""
    return (bool(pool_ids) and pesca_variante(pool_ids, visti) is None
            and not eco_pronto)


def riepilogo_luna(conteggi, luoghi):
    """Riga sui due luoghi piu' frequentati ("Una Luna di taverna e di
    serra."); a pari volte vince l'ordine di comparsa. None se nessuno."""
    per_luogo = []
    for aid, n in conteggi.items():
        nome = luoghi.get(aid)
        if nome is None:
            continue
        for voce in per_luogo:
            if voce[0] == nome:
                voce[1] += n
                break
        else:
            per_luogo.append([nome, n])
    if not per_luogo:
        return None
    primi = sorted(per_luogo, key=lambda v: -v[1])[:2]
    return "Una Luna di " + " e di ".join(v[0] for v in primi) + "."


def slot_da_saltare(luna, cuore_scelto, fisso, inviti, attivita, esauriti,
                    sempre_vive=(), dono_in_borsa=False, luna_da=5):
    """Lune V-VI (dopo la scelta del cuore): lo slot non esiste se non ha
    un fisso, nessun invito e nessuna attivita' con qualcosa di nuovo.
    attivita = id visibili nello slot, esauriti = quelli senza niente di
    nuovo; sempre_vive = id che non si saltano mai (mercato, commissioni:
    Scudi e doni restano scelte vere). Con un dono in borsa non si salta
    (il territorio esaurito puo' ancora consegnarlo)."""
    if luna < luna_da or not cuore_scelto or dono_in_borsa:
        return False
    if fisso is not None or inviti:
        return False
    return all(a in esauriti and a not in sempre_vive for a in attivita)
