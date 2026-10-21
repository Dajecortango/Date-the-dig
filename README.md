# Date the Dignitas

Visual novel (dating sim) in italiano ambientata nel mondo di Yr, nel Nord della Famiglia Dignitas. Motore: Ren'Py. Prima release: route di Aede completa (prologo, 6 capitoli + 3 interludi, climax, 4 finali: good / neutral / 2 bad).

## Come lanciare

1. Scarica [Ren'Py SDK 8.3.7](https://www.renpy.org/dl/8.3.7/renpy-8.3.7-sdk.zip) ed estrailo in `tools/renpy-8.3.7-sdk/` (cartella gitignored).
2. Avvia il gioco: `tools\renpy-8.3.7-sdk\renpy.exe .`

## Verifiche

- Lint: `powershell -File lint.ps1`
- Test routing finali: `python -I tests/test_routing.py`
- Test input nome: `python -I tests/test_sanitize.py`

## Specifica asset (per sostituire i placeholder)

Le immagini vivono in `game/images/`. Per sostituire un placeholder basta sovrascrivere il PNG con lo stesso identico nome file.

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

- `game/script.rpy` — entry point: input nome, salto alla route.
- `game/routes/aede_core.rpy` — personaggi, variabili, `sanitize_name`.
- `game/routes/aede_atto1.rpy` — prologo, capitoli 1–3.
- `game/routes/aede_interludi.rpy` — interludi 1–3.
- `game/routes/aede_atto2.rpy` — capitoli 4–6.
- `game/routes/aede_finali.rpy` — climax, routing, 4 finali.
- `docs/superpowers/specs/` — design document. `docs/superpowers/plans/` — piano.

Una route futura aggiunge i propri file in `game/routes/` e un bivio in `script.rpy`.
