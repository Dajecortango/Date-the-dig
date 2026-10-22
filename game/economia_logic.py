"""Logica pura degli usi degli Scudi (game/economia_extra.rpy): soffiate,
debito con Icaro, scommessa in palestra. Nessuna dipendenza da Ren'Py.
Test: py -3 -I tests/test_economia.py
"""

SOFFIATA_COSTO = 2
OTTONE_COSTO = 2
ORFANI_COSTO = 2
SCOMMESSA_MAX = 3

DEBITO_PRESTITO = 5      # Scudi ricevuti
DEBITO_RESTITUZIONE = 6  # Scudi da rendere
DEBITO_SLOT = 9          # slot del calendario per restituire
DEBITO_SOGLIA = 3        # Icaro presta solo a chi ha meno di 3 Scudi

ORDINE = ("aede", "ofelia", "caino", "druso", "icaro")


def soffiata_candidati(gusti, doni_dati, soffiate, congelate, visti):
    """Personaggi di cui il garzone puo' rivelare il dono preferito: non
    ancora un dono con punti, non gia' rivelati, non congelati. Caino solo
    dopo l'Adunanza (prima e' un nome e basta)."""
    out = []
    for c in ORDINE:
        if c not in gusti or c in doni_dati or c in soffiate or c in congelate:
            continue
        if c == "caino" and "adunanza" not in visti:
            continue
        out.append(c)
    return out


def debito_offribile(debito, esito, scudi, congelate):
    """Icaro presta una volta sola per partita, a chi ha la borsa vuota."""
    return (debito == 0 and esito is None and scudi < DEBITO_SOGLIA
            and "icaro" not in congelate)


def debito_scadenza(idx):
    return idx + DEBITO_SLOT


def debito_saldabile(debito, scadenza, idx, scudi):
    """Saldo puntuale: debito aperto, non scaduto, non contratto in questo
    stesso slot, Scudi sufficienti."""
    return (debito > 0 and idx <= scadenza and idx != scadenza - DEBITO_SLOT
            and scudi >= debito)


def debito_scaduto(debito, scadenza, idx):
    return debito > 0 and idx > scadenza


def slot_restanti(scadenza, idx):
    return max(0, scadenza - idx)


def scommessa_delta(posta, tiro):
    """tiro in [0, 1): sotto 0.5 Druso vince e la posta raddoppia (+posta),
    altrimenti la posta e' persa (-posta)."""
    return posta if tiro < 0.5 else -posta
