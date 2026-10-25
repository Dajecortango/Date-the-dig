---
name: sim-semestre
description: Use when changing anything the semester economy can feel — event points (+=), thresholds, event cond/luna_min/slot, gifts, market, territory scenes, new events or chains — or when test_raggiungibilita.py fails.
---

# Simulatore del semestre: usarlo, non aggirarlo

## Cos'è
`tests/sim_semestre.py` = simulazione esaustiva (DFS con memoizzazione) del semestre Malandrini. Punti, registry, doni, mercato e soglie li legge dai sorgenti (.rpy e `routing_logic`): niente tabelle di punti a mano. Solo il CABLAGGIO del loop (una manciata di frammenti di calendario/economia/route) è modellato a mano — l'elenco esatto è la lista `COERENZA` in test_raggiungibilita.py. `tests/test_raggiungibilita.py` lo usa per provare, per protagonista f e m, che ogni invito è giocabile, le soglie del cuore e dei good/bad end sono raggiungibili, e le coppie poly arrivano al good.

## Comandi (verificati)
- Verifica completa: `py -3 -I -X utf8 tests/test_raggiungibilita.py` (~130 s — normale, non interromperlo)
- Riepilogo esplorativo (massimi per personaggio): `py -3 -I -X utf8 tests/sim_semestre.py`

Lancia la verifica DOPO ogni modifica a punti, cond, soglie, doni, mercato — nello stesso turno. Soglia nuova senza sim = bilanciamento a occhio, vietato (vedi skill character-sim, "Economia dei punti").

## Se fallisce: tre famiglie di FAIL
1. **Soglia irraggiungibile / bad non raggiungibile** — l'economia è sbilanciata davvero. Ribilancia punti o soglie nello stesso edit (soglie SOLO in `routing_logic.py`), poi rilancia.
2. **`analisi dei label senza anomalie` FAIL** — l'analizzatore non ha capito un costrutto che tocca variabili tracciate (`TRACK` in sim_semestre.py). Preferisci i costrutti supportati: `$ x += n`, `+= mgl.delta(...)`, `congelate.add(...)`, `eco_spendi`, `druso_passo_falso`, `rivali_sposta`, menu/if/call/jump semplici. Solo se il costrutto nuovo serve davvero: estendi l'analizzatore (sim_semestre.py / `tests/percorsi.py`), non silenziare l'anomalia.
3. **COERENZA FAIL** — hai cambiato una riga sorgente che il simulatore modella a mano (lista `COERENZA` in test_raggiungibilita.py: frammenti testuali di calendario.rpy, economia.rpy, ofelia_core.rpy, icaro_eventi.rpy, druso_core.rpy, snodi.rpy). Aggiorna INSIEME il frammento in COERENZA e il pezzo di modello corrispondente, mai solo la stringa.

## Limiti del modello (ottimistici, documentati nel docstring di sim_semestre.py)
Flag scritti in un evento non passano ai successivi (entrambi i rami aperti), `rea_noti()` sempre True, debito con Icaro / casi casuali / echi non modellati. Se la tua meccanica nuova vive in questi buchi, il sim non la vede: dillo esplicitamente all'utente invece di dichiarare "verificato".

## Errori comuni
- Fidarsi del riepilogo di sim_semestre.py al posto del test: solo test_raggiungibilita.py controlla le soglie.
- Variabile numerica nuova che pesa sui finali ma non in `TRACK`: il sim la ignora — aggiungila a TRACK e al routing nel modello.
- "Il FAIL è del simulatore, non del gioco": quasi sempre è COERENZA o anomalia, cioè il modello va aggiornato, non il FAIL ignorato.
