"""Minigiochi di territorio: logica pura (nessun import Ren'Py).

Generazione con un rng passato da fuori (renpy.random nel gioco,
random.Random(seed) nei test) e valutazione degli esiti.
Integrazione e scene: minigiochi.rpy (accanto). Test: tests/test_minigiochi.py.
"""

## Duello con Aede ###########################################################
# Il segnale dice cosa sta per fare Aede:
#   attacca          -> "parata"
#   si chiude        -> "finta"   (la finta apre una guardia chiusa)
#   finta / si scopre -> "fendente"

MOSSE = ("fendente", "parata", "finta")

SEGNALI_DUELLO = [
    ("Il peso le scivola sul piede avanti. Le spalle si abbassano.", "parata"),
    ("Stringe l'elsa fino a sbiancare le nocche. Gli occhi ti cercano il fianco.", "parata"),
    ("Accorcia il respiro, come chi sta per gridare.", "parata"),
    ("Arretra di mezzo passo e alza la guardia sopra la fronte. Aspetta.", "finta"),
    ("La lama le resta ferma davanti al petto, punta ai tuoi occhi. Non si muove.", "finta"),
    ("Si mette di taglio, il gomito stretto al corpo. Un muro.", "finta"),
    ("La punta disegna un cerchio lento, troppo lento. Vuole che la guardi.", "fendente"),
    ("Sposta lo sguardo a sinistra, apposta. Il polso va a destra.", "fendente"),
    ("Ha aperto la guardia per sistemarsi una ciocca. Un battito solo.", "fendente"),
]


def pesca_segnali(rng, n=3):
    """n segnali distinti, nell'ordine estratto."""
    return rng.sample(SEGNALI_DUELLO, n)


def esito_duello(punti):
    return "vinto" if punti >= 2 else "perso"


## Carte con Icaro ###########################################################

MANI_PULITE = [
    "Mescola piano, le carte piatte sul panno. Le dita non si fermano mai.",
    "Tiene il mazzo con tutta la mano, come un pane. Taglia una volta sola.",
    "Distribuisce in fretta, il polso sciolto. Il fumo della pipa gli sale dritto.",
    "Batte il mazzo sul tavolo due volte, per pareggiare gli angoli.",
    "Le carte gli scorrono tra i pollici in un ventaglio pulito, poi si richiudono.",
    "Mescola guardando te, non le carte. Sorride appena.",
]

MANI_TRUCCATE = [
    "Il mignolo resta sotto il mazzo un attimo di troppo, mentre taglia.",
    "La prima carta esce un soffio più lenta delle altre. Il pollice la trattiene.",
    "Si gratta il sopracciglio col dorso della mano che tiene il mazzo.",
    "L'anello gira verso il palmo, proprio quando distribuisce a sé stesso.",
    "Taglia due volte, ma la seconda metà torna sopra. Le dita fanno un ponte.",
    "Posa la pipa con la sinistra. La destra, intanto, sfiora il fondo del mazzo.",
]


def pesca_mani(rng, n=3):
    """(descrizioni, indice della mano truccata)."""
    pulite = rng.sample(MANI_PULITE, n - 1)
    truccata = rng.choice(MANI_TRUCCATE)
    idx = rng.randrange(n)
    mani = pulite[:idx] + [truccata] + pulite[idx:]
    return mani, idx


## Registri di Caino #########################################################

CARDIA = "Ceppo di Cardia"
DEBITORI = [
    "Mulino di Porta Bassa", "Tintori del Canale", "Forno di Zefiro",
    "Osteria del Ponte", "Contrada Marcassa", "Cordai del Molo",
    "Vetrai di Via Lunga",
]


def genera_registro(rng, n=5, voci=3):
    """n righe di decime: dict(nome, voci, totale). Una riga ha il totale
    sbagliato; una e' sempre il Ceppo di Cardia. Ritorna (righe, idx_errata)."""
    nomi = rng.sample(DEBITORI, n - 1)
    nomi.insert(rng.randrange(n), CARDIA)
    errata = rng.randrange(n)
    righe = []
    for i, nome in enumerate(nomi):
        parti = [rng.randint(4, 48) for _ in range(voci)]
        totale = sum(parti)
        if i == errata:
            delta = rng.choice([-10, -9, -2, -1, 1, 2, 9, 10])
            totale += delta
        righe.append({"nome": nome, "voci": parti, "totale": totale})
    return righe, errata


def riga_testo(r):
    return "%s:  %s = %d" % (r["nome"], " + ".join(str(x) for x in r["voci"]),
                             r["totale"])


def riga_giusta(r):
    return sum(r["voci"]) == r["totale"]


## Botta e risposta con Druso ################################################
# Premi dal profilo: irriverenza = buona, ritirata/supplica = cattiva.

VALORE_RISPOSTA = {"buona": 1, "debole": 0, "cattiva": -1, "silenzio": 0}
DRUSO_TEMPO = 6.0

BATTUTE_DRUSO = [
    {"battuta": "Novellin[fin], hai la faccia di chi conta le pecore per addormentarsi. E perde il conto.",
     "risposte": [
         ("«Le conto per te: sei l'unico che bela.»", "buona"),
         ("«Dormo benissimo, grazie.»", "debole"),
         ("«Non stasera, Druso. Ti prego.»", "cattiva")]},
    {"battuta": "Dicono che la Famiglia ti abbia preso per pietà. Io dico per scommessa. Persa.",
     "risposte": [
         ("«Allora siamo in due: tua madre ha scommesso su di te.»", "buona"),
         ("«Chi lo dice?»", "debole"),
         ("«Hai ragione, non merito il posto.»", "cattiva")]},
    {"battuta": "Ho scritto un sonetto su di te. Quattordici versi, tredici insulti. Il quattordicesimo è la rima.",
     "risposte": [
         ("«Tredici? Ti sei stancato presto. Come sempre.»", "buona"),
         ("«Leggimelo, dai.»", "debole"),
         ("«Non leggerlo davanti a tutti, per favore.»", "cattiva")]},
    {"battuta": "Paghi tu da bere, vero? Chi non sa parlare, almeno paghi.",
     "risposte": [
         ("«Pago io. Così almeno qualcuno ti ascolta: l'oste.»", "buona"),
         ("«Facciamo a metà.»", "debole"),
         ("«Va bene, va bene. Pago io, basta che smetti.»", "cattiva")]},
    {"battuta": "Il tuo Ceppo ti ha mandato qui per imparare. Lezione uno: stai zitt[fin] quando parlo io.",
     "risposte": [
         ("«Lezione due: parli tanto perché nessuno ti risponde.»", "buona"),
         ("«E la lezione due?»", "debole"),
         ("«Scusa. Non volevo interromperti.»", "cattiva")]},
]


def pesca_battute(rng, n=3):
    """n battute distinte, ognuna con le risposte mescolate."""
    out = []
    for b in rng.sample(BATTUTE_DRUSO, n):
        risp = list(b["risposte"])
        rng.shuffle(risp)
        out.append({"battuta": b["battuta"], "risposte": risp})
    return out


def esito_botta(punti):
    if punti >= 2:
        return "vinta"
    if punti <= -1:
        return "persa"
    return "pari"


## Esiti -> affinita' (max +-1, una tantum) ##################################

DELTA = {
    ("duello", "vinto"): 1, ("duello", "perso"): 0,
    ("carte", "taciuto"): 1, ("carte", "detto"): 0, ("carte", "sviato"): 0,
    ("registri", "trovato"): 1, ("registri", "sbagliato"): -1,
    ("botta", "vinta"): 1, ("botta", "pari"): 0, ("botta", "persa"): 0,
}


def delta(gioco, esito):
    """Variazione di affinita'; "lasciato" e sconosciuti = 0."""
    return DELTA.get((gioco, esito), 0)
