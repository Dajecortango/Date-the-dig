# Route riordinate, finali "passeggeri", dialoghi origliati, scelte chiare (design)

Data: 2026-10-22. Stato: approvato dal committente ("vai"). Punti 1, 2, 4 e 12 della seconda
lista di 40 consigli (richiesta del committente: "fai 1, 2, 4, 12").

Vincoli che valgono per tutto (ereditati da
`2026-10-22-conseguenze-design.md` e `2026-10-22-pacchetto-40-consigli-design.md`):
- L'ordine dei capitoli/eventi esistenti di ogni route non cambia. Niente
  eventi narrativi a caso: ogni evento nuovo ha una `cond` esplicita.
- Eventi nuovi solo in Lune II-IV. Date fisse esistenti intatte.
- Nessuna statistica numerica visibile.
- Le scene esistenti non si riscrivono (eccezione dichiarata: il testo delle
  opzioni di menu del punto 12). Il resto si aggancia da file nuovi o
  spostati (registry `EVENTI`, `FATTI`, `ECHI`, `ECO_DOPO_LABELS`,
  `pool_aggiungi`).
- Prosa: segue la skill `writing-vn-scenes` (voce dei personaggi, `[fin]`,
  `[il_t]` ecc. per il genere del protagonista). Eventi e soglie: skill
  `character-sim`.
- Niente commit senza richiesta esplicita del committente.

## Punto 1 — Druso, Icaro, Ofelia: ordine e contenuto

### 1a. Ordine dei file (decisione del committente: sì)

Stesso schema di Aede e Caino: `*_core`, `*_atto1`, `*_atto2`, `*_eventi`,
`*_finali`. Spostamento puro: nessuna label rinominata, nessuna riga di testo
cambiata. I test restano validi, e restano validi anche i salvataggi fatti
tra una scena e l'altra. Un salvataggio fatto a metà di una scena spostata
riparte dal punto riconosciuto più vicino: accettato dal committente, da
scrivere nelle note di versione.

| Route | core | atto1 | atto2 | eventi | finali |
|---|---|---|---|---|---|
| Druso (`druso_route.rpy`) | default, `druso_passo_falso` | ev1, int1, ev2, int2 | ev3, int3, ev4, luna5, fiaccolata, luna6 | registry `EVENTI`, `impegno_druso` | climax, good, neutral, bad (+ nuovo, punto 2) |
| Icaro (`icaro_route.rpy`) | default, `icaro_gelosia` + hook | ev1, int1, ev2, int2 | ev3, int3, bro_affari, bro_colpo, fiaccolata, luna5, luna6 | registry `EVENTI`, `impegno_icaro`, `impegno_bro` | climax, good, neutral, bad, bro_end (+ nuovo) |
| Ofelia (`ofelia_route.rpy` + `ofelia_finali.rpy`) | `define`, default, `ofelia_scadenza` + hook, attività "corte" | corti 1-3, ev1, ev2, interludi 1-2 | ev3, ev4, interludio luna6, fiaccolate (da `ofelia_finali`) | registry `EVENTI`, `ofelia_scadenza_prima`, i tre impegni | climax, routing, finali (resto di `ofelia_finali`) |

Attenzione per chi costruisce:
- Ren'Py carica i blocchi `init` a pari priorità in ordine alfabetico di
  file. L'ordine degli elementi in `EVENTI` (e in `ATTIVITA`, negli hook)
  deve restare identico a prima: verificarlo con un confronto prima/dopo
  (dump degli id dal gioco o test dedicato).
- Cancellare i vecchi `.rpy` **e i loro `.rpyc`**: un `.rpyc` orfano viene
  ancora caricato e duplica le label.
- `esporta_dialoghi.py` associa i file alle route: aggiornarlo e rigenerare
  `dialoghi/`.
- Se l'export Android o `lint.ps1` elencano file per nome, aggiornarli.

### 1b. Contenuto nuovo (decisione del committente: sì, ordine + scene nuove)

Due scene nuove per route, in Lune II-IV, come `tipo: "invito"` nel
registry di quella route. Si innestano **tra** eventi esistenti come
deviazione facoltativa: la `cond` della scena nuova richiede l'evento
precedente già visto, ma nessun evento esistente richiede la scena nuova
(la catena originale non cambia). Muoiono con la scelta del cuore
(`"scelta_cuore" not in v["visti"]`) come gli interludi.

Economia: ±1 affinità al massimo, una sola volta per scena. Ogni scena
lascia almeno un fatto in `FATTI` (con avviso se la scelta pesa) e un eco
in `ECHI` dove un personaggio che può saperlo lo ricorda.

Temi (proposta di Claude, il committente non li ha scelti; chi costruisce può
cambiarli restando nel carattere):

- **Druso — "Il quaderno"** (Luna II-III, dopo `druso_ev1`): trovi il quaderno
  dei versi seri, quelli che non legge mai in taverna. Leggerlo, restituirlo
  chiuso, o restituirlo dicendogli che l'hai letto. Fatto ripreso nella sfida
  dei versi di Luna V.
- **Druso — "L'udienza"** (Luna III-IV, dopo `druso_ev2`): Lenora lo convoca;
  lui ti chiede di aspettarlo fuori. Esce diverso. Tu scegli se chiedere,
  distrarlo, o restare zitt[fin]. Prepara il climax davanti al Consiglio.
- **Icaro — "Il debito di un altro"** (Luna II-III, dopo `icaro_int1`): una
  riscossione da una famiglia che non può pagare. Icaro condona di nascosto e
  ti chiede di non averlo visto. Lega con `flag_icaro_coperto` solo come
  fatto, non come condizione.
- **Icaro — "La febbre"** (Luna III-IV, dopo `icaro_ev2`): Icaro malato che
  rifiuta aiuto e continua a contare. Restare, chiamare qualcuno, o
  andartene come chiede. Linea "Bro" per il protagonista uomo: stessa scena,
  battute da socio.
- **Ofelia — "Lo specchio"** (Luna II-III, dopo `ofelia_ev1`): Ofelia si prepara
  per un ricevimento e ti chiede un parere onesto, che non vuole davvero.
- **Ofelia — "Il ballo dei pretendenti"** (Luna III-IV, dopo `ofelia_ev2`): a
  un ricevimento ti chiede di scegliere tu il pretendente da umiliare.
  Rifiutarti, sceglierne uno, o sceglierti. Le scene nuove di Ofelia hanno id
  che **non** iniziano per `ofelia_` e niente `scade` (come gli interludi),
  così l'hook `ofelia_scadenza` non le conta come mancati.

Effetti collaterali già previsti dal sistema e accettati: gli inviti nuovi di
Druso e Ofelia contano per `icaro_gelosia` come qualunque altro invito.

Quantità: due scene per route, non di più (scelta del committente: "aggiungo
2 scene per route in Lune II-IV"). Non si insegue il numero di righe di Caino.
Le scene nuove sono di lunghezza simile agli eventi esistenti della stessa
route (35-45 righe).

Ricadute ("ripreso in...", "prepara..."): mai dentro scene esistenti. Si
fanno con un eco (`ECHI`) in Luna V-VI, a fine attività, dal personaggio che
può saperlo. Quindi "Il quaderno" torna in un eco dopo la sfida dei versi,
non dentro `druso_luna5`; "L'udienza" torna in un eco prima del climax.
(Scelta di Claude.)

## Punto 2 — Un finale "passeggero" per Aede, Caino, Druso, Icaro

### Tono (decisione del committente: "lo stesso feeling di Interesse passeggero di Ofelia")

Riferimento: `ofelia_neutral` in `ofelia_finali.rpy`.
- Niente morti, niente scenate. C'eri quasi: è mancato un passo.
- L'altro va avanti con eleganza; tu resti un bel ricordo, non una ferita.
- Struttura: una battuta che nomina il passo mancato, poi uno stacco di
  tempo ("Una Luna dopo..."), lui/lei visto da lontano che vive bene senza
  di te, un testimone che chiude (come Ascadeo che tira una riga), `centered`
  con titolo secco e due righe.
- Ofelia è esclusa: ha già `ofelia_neutral` e due finali agrodolci.

### Quando scatta (proposta di Claude, approvata nel playback)

L'affinità basterebbe per il finale buono, ma manca la condizione chiave
della route. Questi casi oggi cadono nel neutro (o nel bad per Caino).

| Route | Condizione nuova | Posizione nell'ordine |
|---|---|---|
| Aede | `aff >= GOOD["aede"]` e non (`giuramento` e `lavoro`) | subito dopo `good_end` |
| Caino | `fiducia >= GOOD["caino"]` e (`trappole > CAINO_TRAPPOLE_GOOD` o `memoria < CAINO_MEMORIA_GOOD`) e `trappole < CAINO_TRAPPOLE_BAD` | subito dopo `caino_good_end` (il bad per le trappole resta prioritario) |
| Druso | `aff >= GOOD["druso"]` e non `coraggio` | subito dopo `druso_good` |
| Icaro (donna) | `aff >= GOOD["icaro"]` e (non `coperto` o `"icaro" in congelate`) | subito dopo `icaro_good`; il Bro resta escluso |

Per Aede vale solo nel routing normale (`rl.finale_aede`); il ramo poly con
Ofelia (`finale_ofelia_poly_aede`) cade su `finale_aede` alla fine, quindi
eredita il finale nuovo: accettato.

Cosa è mancato, da nominare nella battuta chiave:
- Aede: non sei entrat[fin] nel suo mondo (niente giuramento o lavoro rifiutato).
- Caino: non ti sei fidat[fin] fino in fondo.
- Druso: non hai mai rischiato con lui.
- Icaro: hai tenuto i conti separati.

### Implementazione
- Una label nuova per route nel rispettivo `*_finali.rpy`, con
  `sblocca_finale("<id>")`.
- Una voce in `FINALI` (`finali_galleria.rpy`) per ciascuna, con indizio.
- Un ramo nuovo nelle funzioni `rl.finale_*` di `routing_logic.py`; casi
  nuovi in `tests/test_routing.py` per ogni ramo e per i confini (incluso
  Caino con trappole = `CAINO_TRAPPOLE_BAD`).
- I finali buoni non cambiano. Si restringe solo la zona del neutro.

## Punto 4 — Due di loro parlano di te (decisione del committente: tutti tranne Aede e Icaro)

Tre scene, coppie tra Caino, Druso e Ofelia. Il protagonista non partecipa:
sente. Un modo diverso per scena (il committente: "per caso, origliando, o
inventati altri modi").

| Coppia | Modo | Dove/quando | Aggancio |
|---|---|---|---|
| Caino e Druso | **per caso**: sei in archivio dietro gli scaffali, i due fratelli entrano nell'ufficio della Proprietà credendosi soli | dopo un'attività "registri" di Caino | `ECO_DOPO_LABELS` sull'attività registri |
| Caino e Ofelia | **origliando, per scelta**: li vedi appartarsi; menu "avvicinarti" / "andartene". Andartene = fatto "hai scelto di non sentire", ripreso più avanti. Origliare rischia di farti scoprire, secondo una condizione di stato (non casuale) decisa da chi costruisce | dopo un'attività dove entrambi possono trovarsi (serra/corte) | `ECO_DOPO_LABELS` |
| Druso e Ofelia | **di seconda mano**: Vanna al Ceppo te la racconta recitando le due voci a modo suo. Non sai quanto abbia inventato; un eco successivo di Druso o Ofelia conferma una frase e ne smentisce un'altra | Ceppo | `tipo: "invito"` con `ritratto: "vanna"` |

Regole:
- Lune II-IV. Una volta per partita.
- `cond`: ognuno dei due ha almeno un evento della propria route già visto
  (ti conoscono abbastanza da parlarne), e almeno uno dei due ha la route
  non congelata. Se uno dei due ti ha già chiuso la porta (congelata), la
  scena ha una variante in cui lo dice ("Ofelia ti ha già depennato").
  (Scelta di Claude.)
- Cosa dicono dipende da `fatti_noti` e dalle scelte con ciascuno
  (almeno 2 varianti di battuta per scena legate allo stato).
- Zero affinità. Lasciano un fatto ciascuna, ripreso da almeno un eco.
- Ogni discorso rispetta il vincolo degli echi: dicono solo ciò che possono
  sapere.
- File nuovo: `game/routes/origliati.rpy`.

## Punto 12 — Scelte più specifiche (decisione del committente: nessuna lista, decide il criterio)

### Criterio
Si riscrive un'opzione solo se, letta da sola sullo schermo, non dice cosa
stai decidendo. Tipicamente: verbo nudo o pronome senza referente
("Darglielo", "Prenderla", "Rifiutarla", "Inseguirlo") o "Sì"/"No".
Forma nuova: verbo + intenzione, breve (≤ 8 parole), nella voce del
protagonista. Esempio: "Prenderla" → "Prendere la lama, e il suo peso".

Non si toccano:
- le battute tra «» (sono voce, non descrizione);
- i menu di climax e finali, salvo casi davvero oscuri;
- le opzioni con `if` che distinguono due varianti della stessa scelta
  (vanno cambiate insieme, o niente).

### Processo
1. Chi costruisce produce un audit: tabella file:riga, opzione attuale,
   contesto in una riga, proposta. Su 317 opzioni ci si aspetta qualche
   decina di candidate.
2. **Il committente approva la tabella** prima di applicare.
3. Si applica solo il testo; la logica sotto l'opzione non cambia.

### Compatibilità con l'albero della Trama
`firma_menu` usa la didascalia o, in mancanza, la prima opzione; lo storico
(`persistent.opzioni_viste`, `persistent.opzioni_scelte`, `scelte_partita`)
salva i testi. Per non scollegare le partite già giocate:
- tabella `OPZIONI_RINOMINATE = {vecchio: nuovo}` in `conseguenze_logic.py`;
- normalizzazione vecchio → nuovo su firme e testi al caricamento di un
  salvataggio (`after_load`) e una volta sul `persistent` all'avvio;
- casi in `tests/test_conseguenze.py` (firma con prima opzione rinominata,
  storico misto).
- Se `FATTI` o altre condizioni leggono `scelte_partita` per testo,
  aggiornarle allo stesso modo.

## Non-obiettivi
- Riscrivere scene esistenti oltre al testo delle opzioni del punto 12.
- Dialoghi origliati con Aede o Icaro.
- Un finale "passeggero" per Ofelia o per la linea Bro.
- Cambiare soglie `GOOD` o il bilanciamento dei finali buoni.

## Anti-obiettivi (fallimento anche se "funziona")
- Un salvataggio vecchio che perde la route o lo storico della Trama.
- Scene nuove che spostano o saltano un evento esistente.
- Un personaggio che, origliato o in un eco, sa cose che non può sapere.
- Il finale nuovo che suona come un bad end: deve restare leggero.

## Lasciato a chi costruisce
- Nomi delle label e degli id nuovi (seguendo lo stile esistente).
- Testo delle scene e dei finali (con le skill di scrittura).
- Titoli e indizi in galleria; titoli degli inviti.
- Ordine di lavoro tra i quattro punti (consigliato: 1a prima di tutto,
  perché sposta i file su cui poggiano gli altri).

## Verifica
- `tests/*.py` tutti verdi (`py -3 -I tests/<file>.py`), con casi nuovi.
- `lint.ps1` pulito.
- Dump dell'ordine di `EVENTI` identico prima/dopo il punto 1a.
- `esporta_dialoghi.py` rigenerato.
- Prova manuale: un salvataggio della versione attuale si carica dopo i
  cambi, e la Trama mostra ancora lo storico.
