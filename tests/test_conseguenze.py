"""Verifica il motore delle conseguenze (conseguenze_logic.py) e la
coerenza dei registry FATTI/ECHI in conseguenze.rpy (game/capitoli/malandrini/).

Uso: py -3 -I tests/test_conseguenze.py
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.join(HERE, "..", "game")
# Cartella del capitolo Malandrini, relativa a GAME.
MAL_REL = os.path.join("capitoli", "malandrini")
sys.path.insert(0, HERE)
from percorsi import prepara_import  # noqa: E402
prepara_import()

import conseguenze_logic as csl  # noqa: E402

FAILURES = []


def check(nome, got, atteso):
    ok = got == atteso
    if not ok:
        FAILURES.append(nome)
    print(f"{'PASS' if ok else 'FAIL'}: {nome}: {got!r} (atteso {atteso!r})")


def leggi(rel):
    with open(os.path.join(GAME, rel), encoding="utf-8") as f:
        return f.read()


def tutti_rpy():
    out = {}
    for radice, _d, files in os.walk(GAME):
        for n in files:
            if n.endswith(".rpy"):
                p = os.path.join(radice, n)
                with open(p, encoding="utf-8") as f:
                    out[os.path.relpath(p, GAME)] = f.read()
    return out


# --- Motore puro ---------------------------------------------------------

def test_firma():
    check("firma con didascalia",
          csl.firma_menu("adunanza", [("Domanda?", False), ("A", True), ("B", True)]),
          "adunanza|Domanda?")
    check("firma senza didascalia", csl.firma_menu("x", [("A", True)]), "x|A")
    check("firma fuori calendario", csl.firma_menu(None, [("A", True)]), "inizio|A")


def test_registra():
    scelte, viste, storiche = {}, {}, set()
    csl.registra_scelta(scelte, viste, storiche, "e|D", ["A", "B"], "B")
    csl.registra_scelta(scelte, viste, storiche, "e|D", ["A", "B"], "B")
    check("registra: scelta partita", scelte, {"e|D": "B"})
    check("registra: idempotente", viste, {"e|D": ["A", "B"]})
    csl.registra_scelta({}, viste, storiche, "e|D", ["A", "C"], "A")
    check("registra: opzione nuova in coda", viste["e|D"], ["A", "B", "C"])
    check("registra: storiche", storiche, {("e|D", "A"), ("e|D", "B")})
    check("scelto per prefisso", csl.scelto({"e|D": "«Era un massacro»"}, "e", "«Era"), True)
    check("scelto altro contesto", csl.scelto({"e|D": "«Era»"}, "f", "«Era"), False)


FATTI_T = [
    {"id": "a", "char": "x", "testo": "A", "avviso": None, "cond": lambda v: v["n"] >= 1},
    {"id": "b", "char": "x", "testo": "B", "avviso": "x", "cond": lambda v: v["n"] >= 2},
]


def test_fatti():
    check("nuovi fatti", csl.nuovi_fatti(FATTI_T, {"n": 2}, {}), ["a", "b"])
    check("fatti gia noti esclusi", csl.nuovi_fatti(FATTI_T, {"n": 2}, {"a": ("e", 0)}), ["b"])
    check("nessun fatto", csl.nuovi_fatti(FATTI_T, {"n": 0}, {}), [])


ECHI_T = [
    {"id": "e1", "fatto": "a", "luoghi": ("riti",), "label": "l1"},
    {"id": "e2", "fatto": "b", "luoghi": ("riti", "citta"), "label": "l2",
     "cond": lambda v: v["ok"]},
]


def test_echi():
    noti = {"a": ("ev", 5), "b": ("ev", 5)}
    check("eco troppo presto", csl.pesca_eco(ECHI_T, "riti", noti, set(), 6, {"ok": True}), None)
    check("eco dopo il ritardo", csl.pesca_eco(ECHI_T, "riti", noti, set(), 7, {"ok": True}), "e1")
    check("eco gia visto", csl.pesca_eco(ECHI_T, "riti", noti, {"e1"}, 7, {"ok": True}), "e2")
    check("eco con cond falsa", csl.pesca_eco(ECHI_T, "citta", noti, set(), 9, {"ok": False}), None)
    check("eco luogo sbagliato", csl.pesca_eco(ECHI_T, "spada", noti, set(), 9, {"ok": True}), None)
    check("eco senza fatto", csl.pesca_eco(ECHI_T, "riti", {}, set(), 9, {"ok": True}), None)


def test_albero():
    nodi = [("n1", "Uno", "Luna I"), ("n2", "Due", "Luna I"), ("n3", "Tre", "Luna II")]
    viste = {"n1|D": ["A", "B", "C"], "n3|E": ["X"]}
    storiche = {("n1|D", "A"), ("n1|D", "B")}
    alb = csl.albero(nodi, {"n1"}, {"n1", "n2"}, {"n1|D": "A"}, viste, storiche,
                     {"a": ("n1", 3), "b": ("att_x", 4)}, FATTI_T)
    check("albero: stati", [n[3] for n in alb], ["vissuto", "altrove", "ignoto"])
    check("albero: opzioni del nodo", alb[0][4],
          [("D", [("A", "scelta"), ("B", "passata"), ("C", "mai")])])
    check("albero: nodo ignoto senza menu", alb[2][4], [])
    check("albero: fatti del nodo", alb[0][5], ["A"])
    check("fatti sciolti", csl.fatti_sciolti(nodi, {"a": ("n1", 3), "b": ("att_x", 4)}, FATTI_T, "x"), ["B"])


# --- Coerenza dei registry -----------------------------------------------

def check_registry():
    src = leggi(os.path.join(MAL_REL, "conseguenze.rpy"))
    rpy = tutti_rpy()
    tutto = "\n".join(rpy.values())

    fatti = re.findall(r'\{"id": "(\w+)", "char": (?:"\w+"|None),\s*"testo"', tutto)
    check("FATTI: id unici", len(fatti), len(set(fatti)))

    blocco_vars = re.search(r"CONSEGUENZE_VARS = \[(.*?)\]", src, re.S).group(1)
    vars_ok = set(re.findall(r'"(\w+)"', blocco_vars))
    vars_ok |= set(re.findall(r'CONSEGUENZE_VARS\.append\("(\w+)"\)', tutto))
    for blocco in re.findall(r"CONSEGUENZE_VARS\.extend\(\[(.*?)\]\)", tutto, re.S):
        vars_ok |= set(re.findall(r'"(\w+)"', blocco))
    vars_ok |= {"visti", "congelate", "scelte", "noti", "perso", "luna"}
    usate = set(re.findall(r'\bv\["(\w+)"\]', src))
    check("FATTI: variabili lette tutte esportate", sorted(usate - vars_ok), [])
    for n in sorted(vars_ok - {"visti", "congelate", "scelte", "noti", "perso", "luna"}):
        if not re.search(r"^default %s\b" % n, tutto, re.M):
            FAILURES.append("default " + n)
            print(f"FAIL: variabile senza default: {n}")

    # Ogni prefisso di _scelto deve esistere come opzione di menu nel gioco.
    for ctx, pref in re.findall(r'_scelto\(v, "(\w+)", "([^"]+)"\)', tutto):
        trovato = re.search(r'^\s+"%s' % re.escape(pref), tutto, re.M) is not None
        check(f"scelta esistente: {ctx} {pref}", trovato, True)

    echi = re.findall(r'\{"id": "(\w+)", "fatto": "(\w+)",\s*"luoghi": \(([^)]*)\), "label": "(\w+)"', tutto)
    check("ECHI: letti dal registry", len(echi) > 0, True)
    attivita = set(re.findall(r'\(\s*"(\w+)", "[^"]+", (?:"\w+"|None),', tutto))
    for eid, fatto, luoghi, label in echi:
        check(f"eco {eid}: fatto esistente", fatto in fatti, True)
        check(f"eco {eid}: label esistente",
              re.search(r"^label %s:" % label, tutto, re.M) is not None, True)
        for l in re.findall(r'"(\w+)"', luoghi):
            check(f"eco {eid}: luogo {l} e' un'attivita'", l in attivita, True)
    echi_src = rpy[os.path.join(MAL_REL, "routes", "echi.rpy")]
    for label in re.findall(r"^label (echi_\w+):", tutto, re.M):
        check(f"label {label} registrata in ECHI", label in [e[3] for e in echi], True)

    eventi = set(re.findall(r'\{"id": "(\w+)", "label"', tutto))
    titoli = re.search(r"TRAMA_TITOLI = \{(.*?)\n    \}", src, re.S).group(1)
    for eid in re.findall(r'"(\w+)":', titoli):
        check(f"titolo trama per evento esistente: {eid}", eid in eventi, True)


def test_origliati():
    primi = {"caino": "caino_cap1", "druso": "druso_ev1"}
    visti = {"caino_cap1", "druso_ev1"}
    ok = csl.origliato_ok
    check("origliato: Luna III, entrambi conosciuti",
          ok(visti, set(), 3, "caino", "druso", primi), True)
    check("origliato: Luna I no", ok(visti, set(), 1, "caino", "druso", primi), False)
    check("origliato: Luna V no", ok(visti, set(), 5, "caino", "druso", primi), False)
    check("origliato: uno non ti conosce",
          ok({"caino_cap1"}, set(), 3, "caino", "druso", primi), False)
    check("origliato: entrambi congelati",
          ok(visti, {"caino", "druso"}, 3, "caino", "druso", primi), False)
    check("origliato: uno solo congelato",
          ok(visti, {"druso"}, 3, "caino", "druso", primi), True)
    check("origliato: gia' visto",
          ok(visti | {"orig_caino_druso"}, set(), 3, "druso", "caino", primi),
          False)
    check("origliato: id indipendente dall'ordine",
          csl.origliato_id("druso", "caino"), "orig_caino_druso")


def test_rinomina():
    mappa = {"Prenderla": "Prendere la lama"}
    check("rinomina firma con prima opzione",
          csl.rinomina_firma("cap6|Prenderla", mappa), "cap6|Prendere la lama")
    check("rinomina firma con didascalia: invariata",
          csl.rinomina_firma("cap6|La neve cade.", mappa), "cap6|La neve cade.")
    scelte = {"cap6|Prenderla": "Prenderla", "x|Didascalia": "Prenderla"}
    viste = {"cap6|Prenderla": ["Prenderla", "Rifiutarla"],
             "cap6|Prendere la lama": ["Prendere la lama", "Rifiutarla"],
             "x|Didascalia": ["Prenderla", "Altro"]}
    storiche = {("cap6|Prenderla", "Prenderla"), ("x|Didascalia", "Altro")}
    csl.migra_storico(scelte, viste, storiche, mappa)
    check("migra: scelte_partita", scelte,
          {"cap6|Prendere la lama": "Prendere la lama",
           "x|Didascalia": "Prendere la lama"})
    check("migra: viste unite senza doppioni", viste,
          {"cap6|Prendere la lama": ["Prendere la lama", "Rifiutarla"],
           "x|Didascalia": ["Prendere la lama", "Altro"]})
    check("migra: storiche", storiche,
          {("cap6|Prendere la lama", "Prendere la lama"),
           ("x|Didascalia", "Altro")})
    prima = (dict(scelte), {k: list(v) for k, v in viste.items()}, set(storiche))
    csl.migra_storico(scelte, viste, storiche, mappa)
    check("migra: idempotente", (scelte, viste, storiche), prima)
    s2, v2, st2 = {"a|b": "b"}, {"a|b": ["b"]}, {("a|b", "b")}
    csl.migra_storico(s2, v2, st2, {})
    check("migra: mappa vuota non tocca niente", (s2, v2, st2),
          ({"a|b": "b"}, {"a|b": ["b"]}, {("a|b", "b")}))


ATTESE_RINOMINATE = {
    "Restituirlo chiuso": "Restituiscigli il foglio senza leggerlo",
    "Prenderla": "Prendi la chiave del magazzino",
    "Rifiutarla": "Lasciagli la chiave",
    "Aspettare ancora": "Rimandare il saldo dei sei Scudi",
    # Fase C: costo uniforme "(N Scudi)" nelle scelte che spendono.
    "Offrire un giro a tutto il tavolo": "Offrire un giro a tutto il tavolo (1 Scudo)",
    "Comprargli una lanterna nuova per il Ceppo": "Comprargli una lanterna nuova per il Ceppo (2 Scudi)",
    # Copione Caino aggiornato: opzioni all'imperativo, Aulo -> Eumene.
    "Restare in silenzio e sorridere": "Resta in silenzio e sorridi",
    "Fermare il servo: «L'Arconte beve idromele di Rurikstad.»": "Ferma il servo: «L'Arconte beve idromele di Rurikstad.»",
    "Prendere la coppa e ringraziare": "Prendi la coppa e ringrazia",
    "Aspettare di vedere se la beve": "Aspetta di vedere se beve",
    "Accettare e lasciarlo condurre": "Accetta e lascialo condurre",
    "Accettare, ma giocare a condurre io": "Accetta, ma punta a condurre tu",
    "Rifiutare con un inchino": "Rifiuta con un inchino",
    "Accettare la gara": "Accetta la gara",
    "Declinare con diplomazia": "Declina con diplomazia",
    "«Trentun anni. Concedigli l'esilio, non le Segrete.»": "«Dieci anni. Concedigli l'esilio, non le Segrete.»",
    "Tacere e lasciare decidere l'Arconte": "Taci e lascia decidere l'Arconte",
    "«Hai fatto bene. Aulo era un peso.»": "«Hai fatto bene. Eumene era un peso.»",
    "Tacere e bere": "Taci e bevi",
    "Bere in silenzio e restare": "Bevi in silenzio e resta con Druso",
    # Copione Aede aggiornato: opzioni all'imperativo e testi rivisti.
    "Tenere il passo in silenzio, senza chiedere nulla": "Tieni il passo in silenzio, senza chiedere nulla",
    "Chiederle cosa c'è dentro la cassetta": "Chiedile cosa c'è dentro la cassetta",
    "Lamentarmi del peso": "Lamentati del peso",
    "Tifare per lei a squarciagola": "Tifa per lei a squarciagola",
    "Aiutarla senza farmi vedere": "Aiutala senza farti vedere",
    "Iscrivermi alla corsa aperta e sfidarla": "Iscriviti alla corsa e sfidala",
    "Ignorare la gara e andarmene presto": "Ignora la gara e vai via presto",
    "«Non ancora. Non così.»": "«Non ancora. Non sono sicur[fin] di essere pront[fin].»",
    "«Il tuo Ceppo salda. Ho capito. Non ho visto niente.»": "«Il tuo Ceppo salda, ho capito. Non ho visto niente.»",
    "«Chi era per te, quest'uomo? Cosa ti costa, questo lavoro?»": "«Chi era per te quest'uomo? Quanto ti costa questo lavoro?»",
    "Prenderle la mano": "Prendile la mano",
    "Camminarle accanto, senza toccarla": "Camminale accanto, senza toccarla",
    "Restare qualche gradino indietro": "Resta qualche gradino indietro",
    "Fermarla. «Il tuo nome di prima è morto. Io voglio quella viva.»": "Fermala. «Il tuo nome di prima è morto. Io voglio quella viva.»",
    "Ascoltarla fino in fondo": "Ascoltala fino in fondo",
    "Fermarla e offrirle il mio, di passato": "Fermala e offrile il tuo passato",
    "Parlarle, un'ultima volta": "Parlale un'ultima volta",
    "Restare in silenzio e guardarla negli occhi": "Resta in silenzio e guardala negli occhi",
    "Tendere la mano, aperta": "Tendi la mano, aperta",
    # Copione parti comuni aggiornato: opzioni all'imperativo e testi rivisti.
    "Tacere, e chinare la testa": "Taci e china la testa",
    "Dare ragione ad Aede, a voce bassa": "Dai ragione ad Aede, a voce bassa",
    "Dare ragione a Ofelia, con un mezzo sorriso": "Dai ragione a Ofelia, con un mezzo sorriso",
    "Restare sedut[fin] accanto a Druso": "Resta sedut[fin] accanto a Druso",
    "Seguire Caino fuori": "Segui Caino fuori",
    "Sedermi al tavolo di Icaro, come se niente fosse": "Mi siedo al tavolo di Icaro, come se niente fosse",
    "Offrire a Caino la pipa di Icaro": "Offri a Caino la pipa di Icaro",
    "Brindare a tutti e due: «Ai figli di Lenora, uno per sera.»": "Brinda a tutti e due: «Ai figli di Lenora, uno per sera.»",
    "Proporre di giocarsela a carte": "Proponi di giocarsela a carte",
    "Andarmene, e lasciarli soli col tavolo": "Vattene e lasciali soli al tavolo",
    "Fermarmi da [rivali_a_nome]": "Fermati da [rivali_a_nome]",
    "Fermarmi da [rivali_b_nome]": "Fermati da [rivali_b_nome]",
    "Passare in mezzo, senza fermarmi": "Passa in mezzo, senza fermarti",
    "Ridere con Druso, forte": "Ridi con Druso, forte",
    "Aiutare Icaro a recuperare le monete, contandole": "Aiuta Icaro a recuperare le monete, contandole",
    "Citare il Codice del Teschio: «si dichiara PRIMA di colpire»": "Cita il Codice del Teschio: «si dichiara PRIMA di colpire»",
    "Applaudire lei: «Pulito. Insegnamelo.»": "Applaudi lei: «Pulito. Insegnamelo.»",
    "Tendere la mano a Druso con un verso: «Cadde il poeta, ma cadde rimando»": "Tendi la mano a Druso con un verso: «Cadde il poeta, ma cadde rimando»",
    "Restare neutrale: qui si rischia la pelle": "Resta neutrale: qui si rischia la pelle",
    "Tacere: al tavolo di Icaro, chi guarda non parla": "Taci: al tavolo di Icaro, chi guarda non parla",
    "Proporre il doppio o niente, mazzo nuovo e mescolo io": "Proponi il doppio o niente, mazzo nuovo e mescoli tu",
    "Leggere ad alta voce la pagina di Druso, cifra per cifra": "Leggi ad alta voce la pagina di Druso, cifra per cifra",
    "Chiudere il registro con una mano: «Non stamattina.»": "Chiudi il registro con una mano: «Non stamattina.»",
    "Chiedere a Ofelia come si legge un filo": "Chiedi a Ofelia come si legge un filo",
    "Dare ragione ad Aede: «Pesa diversa, si vede»": "Dai ragione ad Aede: «Pesa diversa, si vede»",
    "Restare in silenzio e guardare il piede di Aede": "Resta in silenzio e guarda il piede di Aede",
    "Contare a voce alta le bocche di calore, per Caino": "Conta a voce alta le bocche di calore, per Caino",
    "Prendere le parti di Ofelia: «La primavera non si tassa»": "Prendi le parti di Ofelia: «La primavera non si tassa»",
    "Chiedere a Caino quanto vale, a registro, un fiore che non fiorisce": "Chiedi a Caino quanto vale, a registro, un fiore che non fiorisce",
    "Eseguire senza discutere, fino a sbagliare di meno": "Esegui senza discutere, fino a sbagliare di meno",
    "Chiederle di mostrarmi il colpo, lentamente": "Chiedile di mostrarti il colpo, lentamente",
    "Lamentarmi del turno all'alba": "Lamentati del turno all'alba",
    "Colpire la moneta, non il bersaglio": "Colpisci la moneta, non il bersaglio",
    "Colpire il bersaglio, come da consegna": "Colpisci il bersaglio, come da consegna",
    "Ignorarlo e prendere uno scudo in silenzio": "Ignoralo e prendi uno scudo in silenzio",
    "Scusarmi e mettermi in fondo alla fila": "Scusati e mettiti in fondo alla fila",
    "Attaccare per primo, senza aspettare il segnale": "Attacca in anticipo, senza aspettare il segnale",
    "Aspettare il segnale, da regolamento": "Aspetta il segnale, da regolamento",
    "Rifiutare la lotta": "Rifiuta la lotta",
    "«Metrica zoppa. Il contenuto peggio. Bis.»": "«Metrica zoppa. Il contenuto arranca. BIS!»",
    "Applaudire educatamente": "Applaudi educatamente",
    "«Dichiara pure. Ma stanotte dormi con un occhio aperto.»": "«Parla pure. Ma stanotte dormi con un occhio aperto.»",
    "Cambiare discorso": "Cambia discorso",
    "Tacere e perdere l'ottavo Scudo con dignità": "Taci e perdi l'ottavo Scudo con dignità",
    "Sussurrare «bel taglio» a voce bassissima": "Sussurra «bel taglio» a voce bassissima",
    "Gridare al baro": "Grida al baro",
    "Sedermi e stare zitt[fin], godendomi la calma": "Mi siedo e sto zitt[fin], godendomi la calma",
    "Chiedergli quanto ha vinto stasera": "Chiedigli quanto ha vinto stasera",
    "Confessare che non la pulisco da una settimana": "Confessa che non la pulisci da una settimana",
    "«Druso Lenorio, poeta di taverna: rima con 'cena' e con 'vena', ma mai con 'sostanza'.»": "«Druso Lauro, poeta di taverna: rima con 'cena' e con 'vena', ma mai con denaro.»",
    "Rispondere con un verso sconcio, il più sporco che mi viene": "Rispondi con un verso sconcio, il più sporco che ti viene in mente",
    "Guardare e basta, com'è gratis": "Guarda e basta, è gratis",
    "Avvicinarmi, piano": "Mi avvicino, piano",
    "Andarmene. Quello che dicono di me, se lo tengano": "Me ne vado. Quello che dicono di me, se lo tengano",
    # Copioni Druso, Icaro e Ofelia aggiornati: opzioni all'imperativo e testi rivisti.
    "Rovesciargli il boccale addosso": "Rovesciagli il boccale addosso",
    "Prenderla e attaccarlo senza preavviso": "Prendila e attaccalo senza preavviso",
    "Sedermi accanto a lui e guardare gli altri": "Siediti accanto a lui a guardare gli altri",
    "«Vendimi pure. Ma ricorda che poi la leva si gira.»": "«Vendimi pure. Ma ricorda che poi la ruota gira.»",
    "Dirgli il nome: in fondo siamo amici": "Digli il nome: in fondo siamo amici",
    "Minacciarlo: se parla, lo denuncio al Consiglio": "Minaccialo: se parla, lo denunci al Consiglio",
    "Mangiare in silenzio e lasciarli scannare": "Mangia in silenzio e lasciali scannare",
    "Chiuderlo e porgerglielo. Senza una parola": "Chiudilo e porgiglielo. Senza una parola",
    "Rimetterlo sotto la panca prima che si avvicini": "Rimettilo sotto la panca prima che si avvicini",
    "Prendere il foglio senza ridere": "Prendi il foglio senza ridere",
    "Intervenire, adesso": "Intervieni subito",
    "Dargli retta e andarcene": "Dagli retta e andate via",
    "«Icaro, se racconti questa cosa, racconto io della tua pipa.»": "«Icaro, se racconti questa cosa, io racconto della tua pipa.»",
    "Ignorarlo e continuare la lezione": "Ignoralo e continua la lezione",
    "Prenderlo in giro: «Il coraggioso Druso e le sue ombre»": "Prendilo in giro: «Il coraggioso Druso e le sue ombre»",
    "Mettersi in silenzio al suo fianco": "Mettiti in silenzio al suo fianco",
    "Prenderlo per il braccio: «Andiamo. Non ne vale la pena.»": "Prendilo per il braccio: «Andiamo. Non ne vale la pena.»",
    "Restare al tavolo, in silenzio. Tocca a lui.": "Resta al tavolo, in silenzio. Tocca a lui.",
    "«Non portarti una poesia. Portati te stesso.»": "«Non portarti una poesia. Porta te stesso.»",
    "Strappargli la lettera e bruciarla sulla candela": "Strappagli la lettera e bruciala sulla candela",
    "Raccogliere una palla di neve e tirargliela in faccia": "Raccogli una palla di neve e tiragliela in faccia",
    "Sedermi accanto a lui e aspettare": "Siediti accanto a lui e aspetta",
    "Alzarmi e parlare per lui": "Alzati e parla per lui",
    "Restare sedut[fin], e guardarlo. La voce è sua": "Resta sedut[fin], e guardalo. La voce è sua",
    "Smontare la cosa con una battuta": "Smonta la cosa con una battuta",
    "«Ho contato ogni carta. Tutto regolare.» (mentire per lui)": "«Ho contato ogni carta. Tutto regolare.» (menti per lui)",
    "Tacere e guardare altrove": "Taci e guarda altrove",
    "Dare ragione al mercante": "Dai ragione al mercante",
    "Aggiungere una riga alla pagina di Druso": "Aggiungi una riga alla pagina di Druso",
    "Chiudere il registro senza leggere oltre": "Chiudi il registro senza leggere oltre",
    "«E ogni cosa qui dentro ha una storia. Raccontamene una.»": "«Se ogni cosa qui dentro ha una storia, raccontamene una.»",
    "Sollevare una tazza del servizio di Glostok, controluce": "Solleva una tazza del servizio di Glostok, controluce",
    "Indicare una lanterna e prendere la moneta con l'altra mano": "Indica una lanterna e prendi la moneta con l'altra mano",
    "Fargli una domanda vera, e prenderla mentre risponde": "Fagli una domanda vera, e prendi la moneta mentre risponde",
    "Rifiutare: «Non rubo ai soci.»": "Rifiuta: «Non rubo ai soci.»",
    "«Il pettine valeva mezzo Scudo. L'osso era di vacca, non di Glostok.»": "«Il pettine valeva mezzo Scudo, era dozzinale, non di Glostok.»",
    "Restare in silenzio e passargli la lanterna": "Resta in silenzio e passagli la lanterna",
    "Restare zitto, braccia conserte, e guardare l'uscita": "Resta zitto, braccia conserte, e guarda altrove",
    "Inventare un'offerta migliore, a un altro banco": "Inventa un'offerta migliore a un altro banco",
    "Indicare il bollo sotto un piattino: è ridipinto": "Indica lo stemma sotto un piattino: è ridipinto",
    "Fingermi ubriaco e chiedere la strada per il Becco Storto": "Fingiti ubriac[fin] e chiedi la strada per il Becco Storto",
    "Fingiti ubriaco e chiedi la strada per il Becco Storto": "Fingiti ubriac[fin] e chiedi la strada per il Becco Storto",
    "Restare fermo nell'ombra, senza respirare": "Resta ferm[fin] nell'ombra, senza respirare",
    "Resta fermo nell'ombra, senza respirare": "Resta ferm[fin] nell'ombra, senza respirare",
    "Fare un fischio basso, come quello dei lanternai": "Fai un fischio basso, come quello dei lanternai",
    "Rovesciare il bicchiere sul panno: carte fradice, mano nulla": "Rovescia il bicchiere sul panno: carte fradice, mano nulla",
    "«L'anello, Arconte. Il castone. Fa da specchio dall'inizio della sera.»": "«L'anello, Pallante. Il castone. Fa da specchio dall'inizio della sera.»",
    "Restare in silenzio. È la sua partita": "Resta in silenzio. È la sua partita",
    "Chiedergli cosa va scritto lì": "Chiedigli cosa va scritto lì",
    "Leggere il totale del semestre, come se niente fosse": "Leggi il totale del semestre, come se niente fosse",
    "Accendergli la pipa, senza chiedere": "Accendigli la pipa, senza chiedere",
    "Prendere la penna e continuare l'inventario al posto suo": "Prendi la penna e continua l'inventario al posto suo",
    "Andare a chiamare Corrado: lui sa di erbe": "Vai a chiamare Corrado: lui si intende di medicina",
    "Fare come chiede: andarmene e chiudere la porta": "Vai via e chiudi la porta",
    "«Ti fermi mezzo respiro prima di dire la verità. Mai prima di una bugia.»": "«Ti fermi mezzo respiro prima di dire la verità e mai prima di una bugia.»",
    "Prendergli la pipa, tirare una boccata, rendergliela. Senza una parola": "Prendigli la pipa, tira una boccata e rendigliela. Senza una parola",
    "Restare in silenzio, a guardare i fiori": "Resta in silenzio a guardare i fiori",
    "Dargli ragione: «Un orso, certo. Enorme.»": "Dagli ragione: «Un orso, certo. Enorme.»",
    "Svignarmela prima che mi tiri in mezzo": "Svignatela prima che ti tiri in mezzo",
    "Aiutarla a raccogliere gli steli tagliati": "Aiutala a raccogliere gli steli tagliati",
    "Ridere con gli altri: in fondo è teatro": "Ridi con gli altri: in fondo è teatro",
    "Fare un passo avanti: «Basta, Ofelia. Lascialo andare.»": "Fai un passo avanti: «Basta, Ofelia. Lascialo andare.»",
    "Restare immobile, senza ridere e senza intervenire": "Resta immobile, senza ridere e senza intervenire",
    "Stare al gioco, con stile: baciarle la mano come se fosse mia da sempre": "Stai al gioco, con stile: baciale la mano come se fosse tua da sempre",
    "Dirlo in faccia, piano: «Mi stai usando, Ofelia. Lo faccio volentieri, ma voglio che tu lo sappia.»": "Dille in faccia, piano: «Mi stai usando, Ofelia. Lo faccio volentieri, ma voglio che tu lo sappia.»",
    "Fare una scenata: «Io che ci faccio qui? Dimmelo davanti a lui!»": "Fai una scenata: «Io che ci faccio qui? Dimmelo davanti a lui!»",
    "Prendere la cote e affilare la lama in silenzio": "Prendi la cote e affila la lama in silenzio",
    "Leggere tutto, nota compresa": "Leggi tutto, nota compresa",
    "Leggere solo la cifra, e tacere la nota": "Leggi solo la cifra, non la nota",
    "Bruciarla alla torcia senza leggerla": "Bruciala con la torcia senza leggerla",
    "«Nessuno. Il tuo gioco, giocalo da sola.»": "«Nessuno. Gioca da sola.»",
    "Prendere le forbici: «Resto. Anche senza gentilezza.»": "Prendi le forbici: «Resto. Anche senza gentilezza.»",
    "Lasciarle le forbici: «Non ancora, Ofelia.»": "Lasciale le forbici: «Non ancora, Ofelia.»",
    "Reggere il suo sguardo: «Colpisci pure. Non chiederò pietà.»": "Reggi il suo sguardo: «Colpisci pure. Non chiederò pietà.»",
    "Arrendermi con eleganza: «Hai vinto. Ma ti è costato fatica, ammettilo.»": "Arrenditi con eleganza: «Hai vinto. Ma ti è costato fatica, ammettilo.»",
    "Chiedere pietà, ridendo, con le mani in alto": "Chiedi pietà, ridendo, con le mani in alto",
    "Prenderle la mano e scendere senza dire niente": "Prendile la mano e scendi senza dirle niente",
    "Baciarle la mano, come vuole il gesto": "Baciale la mano, come vuole il gesto",
    "Prendere entrambe le mani: «Che guardino.»": "Prendi entrambe le mani: «Che guardino.»",
    "Proporre di scendere a turno, per non dare spettacolo": "Proponi di scendere a turno, per non dare spettacolo",
    "Andare da Aede: stanotte la mano è sua": "Vai da Aede: stanotte la mano è sua",
    "Prendere la mano di Ofelia": "Prendi la mano di Ofelia",
    "Alla luce del sole: toglierle il velo e offrirle il braccio": "Alla luce del sole: toglile il velo e offrile il braccio",
    "Prendere la pergamena e porgerla a Ofelia, dal lato della candela": "Prendi la pergamena e porgila a Ofelia, dal lato della candela",
    "Rispondere a Glauco a testa alta: «Non firmo. Resta lei, e resto io.»": "Rispondi a Glauco a testa alta: «Non firmo. Resta lei, e resto io.»",
    "Prendere le sue difese: «Non decidete voi per lei.»": "Prendi le sue difese: «Non decidete voi per lei.»",
}


def check_rinominate():
    check("OPZIONI_RINOMINATE = audit approvato", csl.OPZIONI_RINOMINATE,
          ATTESE_RINOMINATE)
    tutto = "\n".join(tutti_rpy().values())
    opzioni = set(re.findall(r'^\s+"([^"]+)"(?: \(.*\))?(?: if .*)?:\s*$',
                             tutto, re.M))
    for vecchio, nuovo in csl.OPZIONI_RINOMINATE.items():
        check("opzione vecchia sparita: " + vecchio, vecchio in opzioni, False)
        check("opzione nuova presente: " + nuovo, nuovo in opzioni, True)
    # I prefissi letti dai FATTI devono ancora trovare un'opzione.
    for ctx, pref in re.findall(r'_scelto\(v, "(\w+)", "([^"]+)"\)', tutto):
        check("prefisso _scelto vivo: " + pref,
              any(o.startswith(pref) for o in opzioni), True)


def main():
    test_firma()
    test_registra()
    test_fatti()
    test_echi()
    test_albero()
    check_registry()
    test_origliati()
    test_rinomina()
    check_rinominate()
    if FAILURES:
        print(f"{len(FAILURES)} FALLITI: {FAILURES}")
        sys.exit(1)
    print("tutti i casi ok")


if __name__ == "__main__":
    main()
