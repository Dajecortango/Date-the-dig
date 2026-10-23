"""Motore puro delle conseguenze: scelte registrate, fatti, echi, albero.

Nessun import Ren'Py: importabile sia dal gioco (init python) sia dai test.
Un fatto e' un dict con chiavi: id, char, testo, avviso (o None), cond
(callable(vars) -> bool). Un eco e' un dict con chiavi: id, fatto, luoghi
(id di attivita'), label, cond opzionale.
"""

# Slot da lasciar passare prima che un fatto torni come eco: il
# pettegolezzo ha bisogno di tempo per viaggiare.
ECO_RITARDO = 2


def firma_menu(contesto, voci):
    """Identita' stabile di un menu: contesto + didascalia o prima opzione.
    voci = [(testo, selezionabile)]; la didascalia ha selezionabile False."""
    didascalie = [t for t, ok in voci if not ok]
    opzioni = [t for t, ok in voci if ok]
    chiave = didascalie[0] if didascalie else (opzioni[0] if opzioni else "")
    return "%s|%s" % (contesto or "inizio", chiave)


def contesto_di(firma):
    return firma.split("|", 1)[0]


def registra_scelta(scelte, viste, scelte_storiche, firma, opzioni, scelta):
    """Aggiorna scelte (partita), viste (firma -> opzioni in ordine) e
    scelte_storiche (set di (firma, testo)). Idempotente: rigiocare la
    stessa scelta in rollback non cambia niente."""
    elenco = viste.setdefault(firma, [])
    for o in opzioni:
        if o not in elenco:
            elenco.append(o)
    if scelta is not None:
        scelte[firma] = scelta
        scelte_storiche.add((firma, scelta))


def scelto(scelte, contesto, prefisso):
    """True se in questa partita, nel contesto, e' stata scelta un'opzione
    che comincia con prefisso."""
    for firma, testo in scelte.items():
        if contesto_di(firma) == contesto and testo.startswith(prefisso):
            return True
    return False


def nuovi_fatti(fatti, vars, noti):
    """Id dei fatti con cond vera non ancora in noti, nell'ordine del
    registry."""
    return [f["id"] for f in fatti
            if f["id"] not in noti and bool(f["cond"](vars))]


def pesca_eco(echi, luogo, noti, visti, ora, vars, ritardo=ECO_RITARDO):
    """Primo eco del luogo non ancora visto, col fatto noto da almeno
    ritardo slot (noti: id -> (contesto, momento)). None se nessuno."""
    for e in echi:
        if e["id"] in visti or luogo not in e["luoghi"]:
            continue
        nato = noti.get(e["fatto"])
        if nato is None or ora - nato[1] < ritardo:
            continue
        cond = e.get("cond")
        if cond is None or cond(vars):
            return e["id"]
    return None


def stato_nodo(eid, visti_partita, visti_storici):
    if eid in visti_partita:
        return "vissuto"
    if eid in visti_storici:
        return "altrove"
    return "ignoto"


def opzioni_nodo(eid, scelte, viste, scelte_storiche):
    """Menu del nodo: [(didascalia, [(testo, stato)])] con stato in
    'scelta' (questa partita), 'passata' (altre partite), 'mai'."""
    out = []
    for firma, opzioni in viste.items():
        if contesto_di(firma) != eid:
            continue
        righe = []
        for o in opzioni:
            if scelte.get(firma) == o:
                righe.append((o, "scelta"))
            elif (firma, o) in scelte_storiche:
                righe.append((o, "passata"))
            else:
                righe.append((o, "mai"))
        out.append((firma.split("|", 1)[1], righe))
    return out


def albero(nodi, visti_partita, visti_storici, scelte, viste,
           scelte_storiche, noti, fatti):
    """nodi = [(id, titolo, luna)] nell'ordine del racconto. Ritorna
    [(id, titolo, luna, stato, menu, fatti_del_nodo)]; fatti_del_nodo =
    testi dei fatti nati in quel nodo.
    I menu si mostrano solo per i nodi visti almeno una volta."""
    testi = {f["id"]: f["testo"] for f in fatti}
    out = []
    for eid, titolo, luna in nodi:
        stato = stato_nodo(eid, visti_partita, visti_storici)
        menu = ([] if stato == "ignoto"
                else opzioni_nodo(eid, scelte, viste, scelte_storiche))
        nati = [testi[fid] for fid, (ctx, _ora) in noti.items()
                if ctx == eid and fid in testi]
        out.append((eid, titolo, luna, stato, menu, nati))
    return out


def fatti_sciolti(nodi, noti, fatti, char):
    """Fatti del personaggio nati fuori dai nodi (attivita', incroci)."""
    ids_nodi = {n[0] for n in nodi}
    return [f["testo"] for f in fatti
            if f["char"] == char and f["id"] in noti
            and noti[f["id"]][0] not in ids_nodi]


def origliato_id(a, b):
    """Id della scena origliata di una coppia, indipendente dall'ordine."""
    return "orig_" + "_".join(sorted((a, b)))


def origliato_ok(visti, congelate, luna, a, b, primi):
    """Due personaggi parlano di te mentre non ci sei: solo in Lune II-IV,
    se entrambi ti conoscono (primo evento della loro route visto), se
    almeno uno dei due non ti ha chiuso la porta, una volta per partita."""
    return (2 <= luna <= 4
            and primi[a] in visti and primi[b] in visti
            and not (a in congelate and b in congelate)
            and origliato_id(a, b) not in visti)


# Opzioni di menu riscritte (vecchio testo -> nuovo). Lo storico delle
# partite gia' giocate si migra con migra_storico, cosi' l'albero della
# Trama non perde le scelte. Riempita dall'audit delle scelte approvato.
OPZIONI_RINOMINATE = {
    "Restituirlo chiuso": "Restituirgli il foglio senza leggerlo",
    "Prenderla": "Prendere la chiave del magazzino",
    "Rifiutarla": "Lasciargli la chiave",
    "Aspettare ancora": "Rimandare il saldo dei sei Scudi",
}


def rinomina_firma(firma, mappa):
    """Firma con la chiave (didascalia o prima opzione) rinominata."""
    contesto, _, chiave = firma.partition("|")
    if chiave in mappa:
        return "%s|%s" % (contesto, mappa[chiave])
    return firma


def migra_storico(scelte, viste, scelte_storiche, mappa):
    """In place: firme e testi vecchi -> nuovi in scelte (partita), viste
    (firma -> opzioni in ordine) e scelte_storiche (set di (firma, testo)).
    Le liste di viste si uniscono senza doppioni, nell'ordine di comparsa.
    Idempotente."""
    if not mappa:
        return
    nuove_scelte = {}
    for firma, testo in scelte.items():
        nuove_scelte[rinomina_firma(firma, mappa)] = mappa.get(testo, testo)
    scelte.clear()
    scelte.update(nuove_scelte)
    nuove_viste = {}
    for firma, opzioni in viste.items():
        elenco = nuove_viste.setdefault(rinomina_firma(firma, mappa), [])
        for o in opzioni:
            o = mappa.get(o, o)
            if o not in elenco:
                elenco.append(o)
    viste.clear()
    viste.update(nuove_viste)
    nuove_storiche = {(rinomina_firma(f, mappa), mappa.get(t, t))
                      for f, t in scelte_storiche}
    scelte_storiche.clear()
    scelte_storiche.update(nuove_storiche)
