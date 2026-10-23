---
name: character-sim
description: Use when adding or changing calendar events, invitations, affinity thresholds, route gates, endings conditions, or a new datable character in the Malandrini chapter — anything touching EVENTI, ATTIVITA, affinità or congelate.
---

# Character sim: eventi, affinità, lucchetti

> Queste regole valgono per Malandrini. Per un capitolo nuovo parti da `modelli/capitolo/LEGGIMI.md` (e `nuovo_capitolo.py`).

## Architettura (file)
- Motore puro: `game/capitoli/malandrini/calendario_logic.py` (testato in `tests/test_calendario.py`)
- Logica pura delle route: `game/capitoli/malandrini/routing_logic.py` (`rl`: soglie del cuore e dei good end, routing di tutti i finali, coppia poly, passi falsi di Druso; testato in `tests/test_routing.py`) e `game/capitoli/malandrini/relazioni_logic.py` (`rlz`: scadenza inviti di Ofelia, doni, eventi casuali). I .rpy chiamano queste funzioni (`jump expression cal_finale`): soglie e condizioni si cambiano SOLO lì.
- Loop + registry: `game/capitoli/malandrini/calendario.rpy` (`EVENTI`, `ATTIVITA`, screen `pianificazione`)
- Eventi per route: `game/capitoli/malandrini/routes/*_eventi.rpy`, `*_route.rpy`; snodi comuni: `snodi.rpy`
- Profili personaggi: `docs/profili/*.md`; spec: `docs/superpowers/specs/2026-10-20-malandrini-calendario-design.md`

## Struttura del semestre — NON violarla
- Lune I-IV: fase libera (eventi a soglia). **Scelta del cuore: fisso IV/28 sera** (`ev_scelta_cuore`): il candidato scelto gioca la sua mini-scena `impegno_*` → `route_attiva`.
- Lune V-VI: solo route attiva. **Fiaccolata V/14** e **climax VI/21** sono FISSI con dispatch su `route_viva()` in snodi.rpy — mai eventi a soglia del personaggio.
- Un invito di capitolo "alto" muore con la scelta: cond `"scelta_cuore" not in v["visti"]`.
- Quindi **mai `luna_min >= 5` per un invito a soglia**: dopo IV/28 la fase libera non esiste.

## Registrare un evento
```python
{"id": "druso_ev4", "label": "druso_ev4", "tipo": "invito", "char": "druso",
 "titolo": "Testo mostrato nel pianificatore",
 "luna_min": 3, "slot": "sera",            # slot: mattina|pomeriggio|sera|None
 "cond": lambda v: v["druso_affinity"] >= 6 and "druso_ev3" in v["visti"]},
```
- SEMPRE il prerequisito `"<evento precedente>" in v["visti"]` (niente capitoli fuori ordine).
- `v` espone: affinità, `visti`, `congelate`, `player_gender`, `route_attiva`, flag (vedi `cal_vars()`).
- **REGOLA PICKLE**: i dict evento (con lambda) vivono solo nel registry a init. Mai assegnarli a variabili store, mai in `Return(...)` di una screen: si passa l'`id` (stringa). Violarla = "Could not pickle" al primo salvataggio.

## Economia dei punti — calcola, non stimare
- Scene territorio: ±1, una-tantum. Eventi: +1/+2.
- Massimo teorico = somma dei massimi `+=` per label (il test `check_economia_punti` in tests/test_calendario.py la calcola con `_max_punti`).
- OGNI soglia nuova va verificata contro quel massimo, e il test aggiornato. Aggiungere +2 a una route cambia la distanza dal good end: ribilancia le soglie nello stesso edit, non "da controllare poi".
- Soglie attuali scelta del cuore (`rl.cuore_soglie`): aede 8, caino 10, druso 9F/11M, icaro 7F/6M, ofelia 8. Good end (alzati di 1 per il dono preferito, `game/capitoli/malandrini/economia.rpy`): aede>=13(+flag), caino>=13(+2 cond), druso>=15+coraggio, icaro>=13+coperto, ofelia>=12 + mancati==0 (passeggero con 1 mancato, bad sotto 8) (tutte in `rl.GOOD` e nelle `rl.finale_*`). I doni hanno un label per personaggio (`dono_<char>`, un `+= 1` ciascuno) così `_max_punti` li conta. I numeri veri sono nei file e in `check_economia_punti`: in dubbio, fidati del test.

## Lucchetti e congelamento
- Ogni route ha UN lucchetto meccanicamente diverso (Aede: prova a metà; Caino: trappola d'ingresso; Druso: passi falsi se uomo; Icaro: smascherarlo/gelosia; Ofelia: inviti a scadenza, `"scade": True`, hook `cal_inviti_ignorati_hooks`). Un personaggio nuovo richiede un lucchetto nuovo, non un clone.
- Route doppia: `route_seconda` ("aede"|"caino"|None) è una stringa picklabile; `route_seconda_viva()` in snodi.rpy dice se è ancora viva. Poly solo Ofelia+Aede (segreta) o Ofelia+Caino (dichiarata).
- Chiudere una route: `congelate.add("char")` — gli inviti spariscono da soli.
- Gate di genere: cond su `v["player_gender"]`; romance Icaro solo "f", linea Bro "m".

## Checklist di chiusura (sempre, nello stesso turno)
1. `py -3 -I tests/test_calendario.py` (aggiorna i check: id evento, economia, label esistenti)
2. `"./tools/renpy-8.3.7-sdk/renpy.exe" . lint`
3. Label di scena finisce con `return`
