"""Logica pura delle route: scelta del cuore e routing dei finali.

Nessun import Ren'Py: importabile dal gioco (init python) e dai test.
Le funzioni prendono valori semplici (o il dict di cal_vars()) e
restituiscono chiavi o nomi di label. Unica fonte delle soglie: i .rpy
le leggono da qui, i test le verificano qui.
"""

# Scelta del cuore (IV/28): affinita' minima per essere candidati.
# L'ordine delle chiavi e' l'ordine del menu e lo spareggio a pari margine.
CUORE_VAR = {"aede": "aede_affinity", "caino": "caino_fiducia",
             "druso": "druso_affinity", "icaro": "icaro_affinity",
             "ofelia": "ofelia_affinity"}

# Good end (alzati di 1 per il dono preferito, economia.rpy).
GOOD = {"aede": 13, "caino": 13, "druso": 15, "icaro": 13, "ofelia": 12}

# Altre soglie dei finali.
AEDE_BAD = 3                # sotto: bad end (Glauco se il segreto e' tradito)
CAINO_TRAPPOLE_GOOD = 1     # good: trappole <= 1
CAINO_MEMORIA_GOOD = 2      # good: memoria >= 2
CAINO_DRUSO_SEGRETO = 2     # finale segreto: legame con Druso >= 2
CAINO_BAD = 5               # bad: fiducia < 5 ...
CAINO_TRAPPOLE_BAD = 3      # ... o trappole >= 3
DRUSO_NEUTRAL = 8
ICARO_NEUTRAL = 6
ICARO_BRO = 6               # Bro "listino": affinita' >= 6 e impegnato
OFELIA_MANCATI_MAX = 0      # good Ofelia: nessun invito mancato
OFELIA_MANCATI_GELO = 2     # al secondo mancato Ofelia congela
OFELIA_BAD = 8              # sotto la soglia del cuore a fine route: bad
AEDE_SOSPETTO_TEMPESTA = 2  # poly segreto scoperto: tempesta
# Epilogo, personaggi non scelti: riga "alta" a soglia del cuore
# (cuore_soglie), riga "media" da qui, sotto la riga "bassa".
EPILOGO_MEDIA = {"aede": 4, "caino": 6, "druso": 5, "icaro": 4, "ofelia": 4}


def cuore_soglie(f):
    """Soglie della scelta del cuore; f = protagonista donna."""
    return {"aede": 8, "caino": 10, "druso": (9 if f else 11),
            "icaro": (7 if f else 6), "ofelia": 8}


def cuore_classifica(v):
    """[(char, margine sulla soglia del cuore)] dei non congelati, dal piu'
    alto; a pari margine vale l'ordine di CUORE_VAR. v = cal_vars()."""
    soglie = cuore_soglie(v["player_gender"] == "f")
    out = [(c, v[CUORE_VAR[c]] - soglie[c]) for c in CUORE_VAR
           if c not in v["congelate"]]
    out.sort(key=lambda t: -t[1])
    return out


def cuore_candidati(v):
    """Personaggi sopra soglia e non congelati, nell'ordine di CUORE_VAR."""
    soglie = cuore_soglie(v["player_gender"] == "f")
    return [c for c in CUORE_VAR
            if v[CUORE_VAR[c]] >= soglie[c] and c not in v["congelate"]]


def rivali_cuore(v):
    """I due candidati del cuore piu' alti, se almeno due sono sopra soglia;
    altrimenti None."""
    sopra = [c for c, m in cuore_classifica(v) if m >= 0]
    return sopra[:2] if len(sopra) >= 2 else None


def cuore_opzioni(cands, nomi):
    """Voci del menu del cuore: (testo, chiave). Oltre ai singoli, le coppie
    del poliamore se Ofelia e l'altro (Aede o Caino) sono entrambi candidati."""
    opz = [(nomi[c], c) for c in cands]
    if "ofelia" in cands:
        for altro in ("aede", "caino"):
            if altro in cands:
                opz.append(("Ofelia e " + nomi[altro], "ofelia+" + altro))
    return opz


def risolvi_coppia(impegno_of, impegno_altro, altro):
    """Esito dell'impegno a tre: (route_attiva, route_seconda), oppure None
    se nessuno dei due ha accettato (le route restano come sono)."""
    if impegno_of and impegno_altro:
        return ("ofelia", altro)
    if impegno_of:
        return ("ofelia", None)
    if impegno_altro:
        return (altro, None)
    return None


def route_viva(route_attiva, congelate):
    """Route attiva e non congelata nel frattempo; altrimenti None."""
    if route_attiva and route_attiva not in congelate:
        return route_attiva
    return None


def route_seconda_viva(route_attiva, route_seconda, congelate):
    """Seconda route del poliamore (solo con Ofelia viva), se non congelata;
    altrimenti None."""
    if route_viva(route_attiva, congelate) != "ofelia":
        return None
    if route_seconda and route_seconda not in congelate:
        return route_seconda
    return None


# Finali ######################################################################

def aede_good(aff, giuramento, lavoro):
    return aff >= GOOD["aede"] and bool(giuramento) and bool(lavoro)


def finale_aede(aff, giuramento, lavoro, segreto):
    """Ordine vincolante: good -> passeggero -> bad_glauco -> bad_aede ->
    neutral. Passeggero: affinita' da good, ma niente giuramento o lavoro."""
    if aede_good(aff, giuramento, lavoro):
        return "good_end"
    if aff >= GOOD["aede"]:
        return "aede_passeggero"
    if not segreto and aff < AEDE_BAD:
        return "bad_end_glauco"
    if aff < AEDE_BAD:
        return "bad_end_aede"
    return "neutral_end"


def finale_caino(fiducia, trappole, memoria, druso):
    """Ordine vincolante: good -> passeggero -> segreto -> bad -> neutral.
    Passeggero: fiducia da good, ma trappole o memoria fuori soglia (le
    trappole da bad restano bad)."""
    if (fiducia >= GOOD["caino"] and trappole <= CAINO_TRAPPOLE_GOOD
            and memoria >= CAINO_MEMORIA_GOOD):
        return "caino_good_end"
    if fiducia >= GOOD["caino"] and trappole < CAINO_TRAPPOLE_BAD:
        return "caino_passeggero"
    if druso >= CAINO_DRUSO_SEGRETO and fiducia < GOOD["caino"]:
        return "caino_secret_end"
    if fiducia < CAINO_BAD or trappole >= CAINO_TRAPPOLE_BAD:
        return "caino_bad_end"
    return "caino_neutral_end"


def finale_druso(aff, coraggio):
    """Ordine: good -> passeggero (affinita' da good, mai rischiato) ->
    neutral -> bad."""
    if coraggio and aff >= GOOD["druso"]:
        return "druso_good"
    if aff >= GOOD["druso"]:
        return "druso_passeggero"
    if aff >= DRUSO_NEUTRAL:
        return "druso_neutral"
    return "druso_bad"


def druso_passo_falso(gender, passi):
    """Passo falso con Druso (l'affinita' scende di 1 in ogni caso).
    -> (passi aggiornati, avvisa "se la segna", congela). Conta solo per un
    protagonista uomo: al primo l'avviso, al secondo Druso archivia."""
    if gender != "m":
        return passi, False, False
    passi += 1
    return passi, passi == 1, passi >= 2


def finale_icaro(gender, aff, coperto, congelate):
    """Uomo: sempre il finale Bro (il cui esito decide finale_bro)."""
    if gender == "m":
        return "icaro_bro_end"
    if aff >= GOOD["icaro"] and coperto and "icaro" not in congelate:
        return "icaro_good"
    if aff >= GOOD["icaro"]:
        return "icaro_passeggero"
    if aff >= ICARO_NEUTRAL:
        return "icaro_neutral"
    return "icaro_bad"


def finale_bro(aff, impegnato):
    """Quale dei due finali Bro: id della galleria."""
    if aff >= ICARO_BRO and impegnato:
        return "icaro_bro_listino"
    return "icaro_bro_conti"


def ofelia_good(aff, mancati):
    return aff >= GOOD["ofelia"] and mancati <= OFELIA_MANCATI_MAX


def finale_ofelia(aff, mancati, seconda_viva, caino_fiducia):
    """Ordine vincolante: good poly Caino -> good -> passeggero -> bad ->
    neutral. Passeggero: affinita' da good, ma un invito mancato (al
    secondo la route e' gia' congelata). Bad: sotto la soglia del cuore."""
    if (ofelia_good(aff, mancati) and seconda_viva == "caino"
            and caino_fiducia >= GOOD["caino"]):
        return "ofelia_good_caino"
    if ofelia_good(aff, mancati):
        return "ofelia_good"
    if aff >= GOOD["ofelia"]:
        return "ofelia_passeggero"
    if aff < OFELIA_BAD:
        return "ofelia_bad"
    return "ofelia_neutral"


# Finali di Ofelia raggiungibili dal climax di Aede (poly segreto).
OFELIA_POLY_AEDE = ("ofelia_bad_tempesta", "ofelia_good_aede", "ofelia_good")


def finale_ofelia_poly_aede(sospetto, of_aff, mancati, aede_aff,
                            giuramento, lavoro, segreto):
    """Ordine vincolante: tempesta -> good a due -> good sola (coda amara)
    -> routing di Aede."""
    if sospetto >= AEDE_SOSPETTO_TEMPESTA:
        return "ofelia_bad_tempesta"
    if ofelia_good(of_aff, mancati) and aede_good(aede_aff, giuramento, lavoro):
        return "ofelia_good_aede"
    if ofelia_good(of_aff, mancati):
        return "ofelia_good"
    return finale_aede(aede_aff, giuramento, lavoro, segreto)
