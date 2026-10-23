---
name: writing-vn-scenes
description: Use when writing or editing any .rpy scene, dialogue, label, menu or ending in game/capitoli/malandrini/routes — new events, activity variants, route chapters, finali — or when the user asks for "grade A" visual novel prose.
---

# Scene da visual novel di grado A (Date the Dignitas)

> Queste regole valgono per Malandrini. Per un capitolo nuovo parti da `modelli/capitolo/LEGGIMI.md` (e `nuovo_capitolo.py`).

## Principio
Ogni scena si gioca: scelte che cambiano qualcosa, regia a schermo, zero spiegoni. La prosa è in italiano, frasi brevi, sensoriale.

## Prima di scrivere — verifica gli asset (non inventarli MAI)
```
ls "game/images/malandrini" "game/images/comune"    # sprite e bg esistenti, SOLO questi
```
Sprite oggi: aede (furia, imbarazzata, irritata, neutra, rabbia, sorpresa, sorriso, triste), caino (freddo, furioso, neutro, sarcastico, sorpreso, tenero), ofelia (neutra, rabbia, imbarazzata, compiaciuta), glauco (deluso, furioso, minaccioso, neutro), druso (ghigno, imbarazzato, irritato, neutro, serio, sorpreso), icaro (furbo, imbarazzato, irritato, neutro, sereno, sorpreso), briseide (neutra — placeholder). Bg: nero, sala_svelo, corridoio_ceppo, vicoli_zefiro, studio_glauco, arena_athlion, cala_notte, esterno_neve, consiglio, palestra. Niente bg taverna/fumeria: si usa vicoli_zefiro. Un'espressione che non c'è → usa la più vicina, non inventare il nome.

## Regia (convenzioni in game/regia.rpy)
- Cambio espressione, stesso personaggio in scena: `with qdiss`
- Momenti teneri/sorrisi rari: `with dissolve` (il contrasto è il punto)
- Colpi, schiaffi, TESCHIO, shock: `with vpunch` / `with hpunch` su riga propria
- Lama, morte, rivelazione fulminea: `with lampo`
- Entrata fragorosa (Druso): `show druso ghigno at left with easeinleft`
- Comprimari a `left`; personaggio della route al centro
- Momenti solenni: `centered "{cps=20}...{/cps}"`

## Prosa
- Battuta max 2-3 righe di textbox; narrazione max 2 frasi per blocco
- Varianti di genere SEMPRE: `[fin]`, `[figlio_t]`, `[un_t]`, `[fratello_t]`… (vedi game/protagonista.rpy)
- Voce dal profilo in `docs/profili/*.md` — e i PREMI seguono il profilo, non la morale: a Druso le risposte irriverenti e maleducate PIACCIONO (+1), le suppliche no (-1); Icaro premia silenzio e occhio per i dettagli; Caino premia chi ricorda ciò che dice.
- `pc` = protagonista (definito in game/capitoli/malandrini/routes/aede_core.rpy); personaggi: aede, caino, ofelia, druso, icaro, briseide, glauco, vanna, corrado (vanna/corrado senza sprite: solo voce)

## Menu
2-4 opzioni, ognuna con esito diverso (testo + eventuale ±1 affinità). Mai opzione morta. Scene territorio: ±1 massimo, una tantum (anti-grind).

## Dopo aver scritto — SEMPRE
```
"./tools/renpy-8.3.7-sdk/renpy.exe" . lint
py -3 -I tests/test_calendario.py
```
Scena nuova in un pool → aggiungila alla tupla in `ATTIVITA` e il label finisce con `return` (mai jump di catena).

## Errori tipici
| Errore | Fix |
|---|---|
| Sprite/bg inventato (`druso minaccioso`) | Solo asset in lista sopra |
| Premio "morale" invece che da profilo | Rileggi docs/profili |
| Battutone da 5 righe | Spezza: il box è di 2-3 righe |
| Scena che finisce con jump | `return`: il calendario riprende il controllo |
