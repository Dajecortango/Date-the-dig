"""Logica pura delle relazioni: inviti a scadenza di Ofelia, doni, eventi
casuali in citta'.

Nessun import Ren'Py: importabile dal gioco (init python) e dai test.
"""

# Inviti a scadenza ###########################################################

OFELIA_GELO = 2  # al secondo invito mancato Ofelia congela


def ofelia_esiti_scadenza(ids, mancati, congelata):
    """Esiti, in ordine, degli inviti lasciati scadere: un elemento per ogni
    invito di Ofelia che conta come mancato (-1 affinita', +1 mancati).
    "prima" = primo mancato (scena di avviso), "gelo" = Ofelia congela,
    "altro" = mancato senza conseguenze speciali. Gli id che non iniziano
    per "ofelia_" (interludi, altri personaggi) non contano; da congelata,
    nemmeno i suoi."""
    esiti = []
    for eid in ids:
        if not eid.startswith("ofelia_") or congelata:
            continue
        mancati += 1
        if mancati >= OFELIA_GELO:
            esiti.append("gelo")
            congelata = True
        elif mancati == 1:
            esiti.append("prima")
        else:
            esiti.append("altro")
    return esiti


# Doni ########################################################################

def dono_valuta(gusti, char, chiave):
    """"ama" | "odia" | "neutro". gusti = {char: (preferito, detestato)}."""
    ama, odia = gusti[char]
    return "ama" if chiave == ama else "odia" if chiave == odia else "neutro"


def dono_offribile(dono_tenuto, char, doni_dati, congelate):
    """Si propone il dono se ne hai uno e il personaggio non e' congelato.
    Anche a chi ha gia' ricevuto un dono con punti (doni_dati): li' vale
    come neutro (dono_consegna), cosi' il dono non resta bloccato in borsa
    e il mercato torna disponibile."""
    return dono_tenuto is not None and char not in congelate


def dono_consegna(gusti, char, chiave, doni_dati=frozenset()):
    """(esito, segna): segna = il personaggio va aggiunto a doni_dati. Solo
    un dono con punti (preferito o detestato) per personaggio per semestre;
    il neutro non consuma il diritto. Chi e' gia' in doni_dati riceve
    sempre un neutro (0 punti)."""
    if char in doni_dati:
        return "neutro", False
    esito = dono_valuta(gusti, char, chiave)
    return esito, esito != "neutro"


# Eventi casuali in citta' ####################################################

CITTA_PROB = 0.4


def pesca_citta(casi, visti, da_pool, rnd):
    """Evento casuale una-tantum o variante del pool. Se ci sono casi non
    visti: pool esaurito (da_pool None) o tiro < CITTA_PROB -> un caso a
    caso tra i liberi. Altrimenti la variante del pool (None se esaurito).
    rnd: oggetto con random() e choice() (renpy.random nel gioco); random()
    si tira solo se il pool ha ancora una variante."""
    liberi = [c for c in casi if c not in visti]
    if liberi and (da_pool is None or rnd.random() < CITTA_PROB):
        return rnd.choice(liberi)
    return da_pool
