# Date the Dignitas

Visual novel (dating sim) in italiano ambientata nel mondo di Yr, nel Nord della Famiglia Dignitas. Motore: Ren'Py. Prima release: route di Aede completa (prologo, 6 capitoli + 3 interludi, climax, 4 finali: good / neutral / 2 bad).

Route di Ofelia "Tanto bella quanto letale" (difficoltà 4/5): corte e serra nel pomeriggio, inviti a scadenza, fiaccolate, climax e 5 finali (good, "Il contratto a tre", "Le figlie di Glauco", "La tempesta", "Interesse passeggero"). Si sblocca tramite la scelta del cuore; Ofelia può essere affiancata ad Aede (segreta) o Caino (dichiarato).

## Come lanciare

1. Scarica [Ren'Py SDK 8.3.7](https://www.renpy.org/dl/8.3.7/renpy-8.3.7-sdk.zip) ed estrailo in `tools/renpy-8.3.7-sdk/` (cartella gitignored).
2. Avvia il gioco: `tools\renpy-8.3.7-sdk\renpy.exe .`

## Verifiche

- Lint (SDK): `./tools/renpy-8.3.7-sdk/lib/py3-windows-x86_64/python.exe ./tools/renpy-8.3.7-sdk/renpy.py . lint`
- Un test: `py -3 -I -X utf8 tests/test_X.py`
- Tutti i test: `for t in tests/test_*.py; do py -3 -I -X utf8 "$t" </dev/null; done 2>&1 | grep -E "^FAIL|Traceback"` (nessuna riga = tutto ok)

## Specifica asset (per sostituire i placeholder)

Le immagini di Malandrini vivono in `game/images/malandrini/` (quelle comuni in `game/images/comune/`). Per sostituire un placeholder basta sovrascrivere il PNG con lo stesso identico nome file.

**Sprite personaggi** — PNG con sfondo trasparente, 600×1050 px (il gioco gira a 1920×1080; sprite ancorati in basso, quindi altezza massima 1080 px o la testa esce dallo schermo), personaggio centrato, inquadratura dalle ginocchia in su:

| File | Contenuto |
|---|---|
| `aede neutra.png` | Aede, espressione neutra/guardinga |
| `aede irritata.png` | Aede, irritata (tsundere) |
| `aede sorpresa.png` | Aede, colta di sorpresa |
| `aede imbarazzata.png` | Aede, rossore/imbarazzo |
| `aede sorriso.png` | Aede, sorriso raro e vero |
| `aede furia.png` | Aede, furia fredda (con lama) |
| `glauco neutro.png` | Glauco Severo, cortesia glaciale |
| `glauco minaccioso.png` | Glauco Severo, minaccia esplicita |
| `briseide neutra.png` | Briseide Ippodamia, calore materno |

Riferimento aspetto Aede: capelli rosso fiamma lunghi e mossi, occhi grigioverdi, abito nero con sopravveste in broccato rosso, bottoni e catenelle d'oro, collana di gemme blu.

**Sfondi** — PNG o JPG (se JPG, aggiornare l'estensione nei nomi), 1920×1080 px:

| File | Contenuto |
|---|---|
| `bg sala_svelo.png` | Salone in maschera a Rocca Tempesta, lanterne, arazzi col leone dorato |
| `bg arena_athlion.png` | Arena/campo della gara atletica |
| `bg vicoli_zefiro.png` | Vicoli di Zefiro, Città delle Lanterne |
| `bg cala_notte.png` | La Calà: scalinata di 300 gradini illuminata da lanterne, di notte |
| `bg studio_glauco.png` | Studio privato austero di Glauco Severo |
| `bg corridoio_ceppo.png` | Interno caldo della tenuta del Ceppo di Briseide |
| `bg esterno_neve.png` | Esterno delle mura di Zefiro sotto la neve, notte |
| `bg nero.png` | Nero pieno (schermate di fine) |

## Struttura

- `game/script.rpy` — entry point: scelta del capitolo (o ingresso diretto se ce n'e' uno solo).
- `game/capitoli.rpy`, `game/capitoli_logic.py` — registro e schermata dei capitoli.
- `game/protagonista.rpy` — genere, nome e varianti di testo del protagonista (`set_gender`, `sanitize_name`), comuni a tutti i capitoli.
- `game/capitoli/malandrini/routes/aede_core.rpy` — personaggi e variabili di Aede.
- `game/capitoli/malandrini/routes/aede_atto1.rpy` — prologo, capitoli 1–3.
- `game/capitoli/malandrini/routes/aede_interludi.rpy` — interludi 1–3.
- `game/capitoli/malandrini/routes/aede_atto2.rpy` — capitoli 4–6.
- `game/capitoli/malandrini/routes/aede_finali.rpy` — climax, routing, finali (anche "passeggero").
- Caino, Druso, Icaro, Ofelia: stesso schema per route — `<nome>_core.rpy`
  (variabili), `_atto1`/`_atto2` (scene), `_eventi` (registry del calendario,
  impegno, fatti ed echi), `_finali` (climax e finali).
- `game/capitoli/malandrini/routes/origliati.rpy` — dialoghi origliati tra Caino, Druso e Ofelia.
- `docs/superpowers/specs/` — design document. `docs/superpowers/plans/` — piano.

Una route futura di Malandrini aggiunge i propri file in `game/capitoli/malandrini/routes/`; un capitolo nuovo si crea come descritto sotto.

## Aggiungere un capitolo

1. `py -3 -I -X utf8 nuovo_capitolo.py <id> <numero> "<titolo>"` copia `modelli/capitolo/` in `game/capitoli/<id>/` e crea gli asset in `game/images/<id>/`, `game/gui/<id>/`, `game/audio/<id>/`.
2. Prefisso: ogni nome di immagine, label e id di finale del capitolo inizia con `<id>_` (devono essere unici in tutto il gioco).
3. Il capitolo si registra da solo in `capitolo.rpy` (init 10); il codice comune non nomina mai un capitolo.
4. Dialoghi: aggiungi una voce a `CAPITOLI` in `esporta_dialoghi.py` (copioni in `dialoghi/<id>/`).
5. Prima di chiudere: lint e test (vedi "Verifiche") puliti. Dettagli in `modelli/capitolo/LEGGIMI.md`.

## Note di versione

- 2026-10-22 — Le route di Druso, Icaro e Ofelia sono state divise in più
  file. Un salvataggio fatto a metà di una scena di queste route riparte dal
  punto riconosciuto più vicino (inizio scena o salvataggio precedente). I
  salvataggi fatti dal calendario non cambiano. Quattro testi di scelta
  sono stati riscritti: lo storico della Trama li riconosce comunque.
  In un'altra copia del progetto, cancellare i vecchi `game/routes/*_route.rpyc`
  (druso, icaro, ofelia): Ren'Py li caricherebbe ancora e troverebbe label doppie.
- 2026-10-23 — Capitoli: il gioco e' organizzato in capitoli
  (`game/capitoli/<id>/`); Malandrini e' il capitolo I. In un'altra copia del
  progetto cancellare i `.rpyc` orfani dei vecchi percorsi:
  `game/routes/*.rpyc`, `game/{calendario,borsa,economia,economia_extra,cronache,conseguenze,minigiochi,nuova_partita}.rpyc`
  e gli `*_logic.py` compilati / `__pycache__` in `game/`, altrimenti Ren'Py
  trova etichette doppie. I salvataggi beta non valgono piu': reinstallare.
