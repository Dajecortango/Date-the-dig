---
name: renpy-lint
description: Use when closing any edit to .rpy or *_logic.py files, before claiming work done or committing — which lint and test commands to run, and which test covers which file.
---

# Verifica Ren'Py: lint + test giusti

## Comandi (verificati, dalla radice del repo)
- Lint: `./tools/renpy-8.3.7-sdk/lib/py3-windows-x86_64/python.exe ./tools/renpy-8.3.7-sdk/renpy.py . lint`
- Un test: `py -3 -I -X utf8 tests/test_X.py`
- Tutti: `for t in tests/test_*.py; do py -3 -I -X utf8 "$t" </dev/null; done 2>&1 | grep -E "^FAIL|Traceback"` (nessuna riga = ok)

## Quale test per quale file
| File toccato | Test da lanciare |
|---|---|
| `calendario.rpy`, `calendario_logic.py`, EVENTI/ATTIVITA | `test_calendario.py` + `test_ordine_init.py` |
| `routing_logic.py`, soglie, finali, `*_finali.rpy` | `test_routing.py` (+ `test_routing_caino.py` per Caino) |
| Punti (`+=`), cond eventi, doni, mercato, slot | `test_raggiungibilita.py` (~130 s) — vedi skill sim-semestre |
| `routes/*_eventi.rpy`, `*_route.rpy` | per contenuto: punti → `test_raggiungibilita.py`; flag/soglie usati dai finali → anche `test_routing.py`; entrambi se tocca entrambi |
| `economia*.rpy`, `economia_logic.py`, scudi | `test_economia.py` |
| `conseguenze.rpy` (FATTI/ECHI) | `test_conseguenze.py` |
| `minigiochi*.rpy` | `test_minigiochi.py` |
| Dialoghi nuovi (seconda persona al protagonista) | `test_genere.py` |
| Nomi propri, luoghi, lore | `test_lore.py` — vedi skill lore-continuity |
| `regia_logic.py`, luce/regia | `test_regia.py` |
| Audio citato nelle scene | `test_audio.py` |
| `capitoli_logic.py`, registro capitoli | `test_capitoli.py` |
| `protagonista.rpy` (sanitize/genere) | `test_sanitize.py` |
| Route spostate/rinominate | `test_ordine_init.py` |

Dubbio su quali toccare = lancia tutti (il loop sopra, pochi minuti).

## Regole
- Lint + test DOPO ogni blocco di modifiche, PRIMA di dire "fatto". Mai "da sistemare poi".
- Un FAIL va capito, non zittito: se il test è obsoleto aggiornalo nello stesso turno, se il codice è rotto correggi il codice.
- Lint pulito = zero righe di errore prima del riepilogo "The game contains…".
- Errori lint tipici: label citata ma inesistente (`call`/`jump` a scena rinominata), immagine/audio mancante, screen con proprietà sconosciuta.

## Errori comuni
- Lanciare `renpy.exe . lint` senza percorso python SDK: usa il comando esatto sopra (fonte: README "Verifiche").
- Saltare `test_raggiungibilita.py` dopo un ritocco "piccolo" ai punti: è l'unico che vede l'economia intera.
- Dimenticare `-X utf8`: alcuni test stampano caratteri accentati e muoiono su cp1252.
