# Capitolo __TITOLO__ (`__ID__`)

Generato da `nuovo_capitolo.py`. Cosa c'e' qui:

- `capitolo.rpy`: registra il capitolo nel registro `rcap` (init 10).
- `inizio.rpy`: la label d'ingresso `__ID___inizio` (cartello, genere, nome, una riga, un finale).
- `finali.rpy`: la lista dei finali per la galleria.
- `variabili.rpy`: esempio di store con nome (`default __ID__.affinita = 0`).

## Passi

1. Scrivi la storia in `inizio.rpy` e in nuovi file di questa cartella.
2. Aggiungi i finali in `finali.rpy` (id, titolo, gruppo, indizio) e sbloccali con `$ sblocca_finale("<id>")`.
3. Registra solo cio' che serve in `capitolo.rpy` (`funzioni`, `cast_menu`, `affinita`, `regia`, `ambienti`, `ritratto`, `schede`...); i campi non dati restano vuoti. Per il feedback sulle affinita' i nomi con punto sono ammessi: `affinita=[("__ID__.affinita", "<ritratto>", "<Nome>")]`. Se usi `cast_menu`, ogni chiave deve avere la sua voce in `schede`.
4. Lint (`renpy.py . lint`) e test (`tests/test_*.py`) puliti prima di chiudere.

## Regola dei prefissi

Immagini, label e id dei finali sono unici in tutto il gioco: ogni nome nuovo comincia con `__ID___`
(`__ID___inizio`, `__ID___fine`, `bg __ID___strada`...). Le variabili vanno nello store `__ID__`.

## Cartelle degli asset

Create vuote (con un `.gitkeep`, da togliere quando ci metti i file):

- `game/images/__ID__/`
- `game/gui/__ID__/`
- `game/audio/__ID__/`
