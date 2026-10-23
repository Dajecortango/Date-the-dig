---
name: game-brainstorm
description: Use when ideating new game content for Date the Dignitas — a new route, datable character, chapter, mechanic, festival or ending — before any design doc or code.
---

# Game brainstorm (studio interno Dignitas)

## Principio
Niente idee a ruota libera: ogni proposta nasce già vincolata a lore, struttura del semestre ed economia dei punti. Un'idea che ignora i vincoli è lavoro da rifare.

> Queste regole valgono per Malandrini. Per un capitolo nuovo parti da `modelli/capitolo/LEGGIMI.md` (e `nuovo_capitolo.py`).

## Leggi PRIMA di proporre
1. `docs/superpowers/specs/2026-10-20-malandrini-calendario-design.md` — struttura: Lune, date fisse, scelta del cuore, snodi
2. `docs/profili/*.md` — personaggi canonici (e menzioni: Pandora, Lenora, Ascadeo)
3. `game/capitoli/malandrini/routes/snodi.rpy` + `game/capitoli/malandrini/calendario.rpy` — cosa è fisso vs a soglia
4. Lore: Famiglia Dignitas, Nord di Yr, Rocca Tempesta, Ceppi/Rami/Autarchi/Arconti, le Virtù, il giuramento (il nome di prima è tabù), TESCHIO

## Vincoli strutturali (chi li viola riprogetta)
- Date fisse del semestre: Svelo I/1, Adunanza II/8, Athlion III/10, scelta del cuore IV/28, Fiaccolata V/14, climax VI/21. La Fiaccolata e il climax sono dispatch su route attiva: una route nuova vi AGGIUNGE una variante, non un proprio evento a soglia.
- Eventi a soglia solo in Lune I-IV. L'impegno è la mini-scena chiamata dalla scelta del cuore, mai dentro un altro evento.
- Ogni route: territorio (slot + attività), 3 eventi a soglia in ordine, impegno, variante Fiaccolata, climax, 3-4 finali.

## Formato della proposta (tutte le voci, sennò è incompleta)
1. **Concept** — chi è, contrappeso nel cast (cosa copre che gli altri non coprono)
2. **Lucchetto** — meccanicamente DIVERSO dagli esistenti (prova a metà / trappola d'ingresso / passi falsi / gelosia / inviti a scadenza sono presi)
3. **Territorio** — slot e attività, senza rubare quelli altrui (spada=Aede, registri=Caino, palestra+taverna=Druso, fumeria sera=Icaro, corte/serra=Ofelia)
4. **Eventi** — 3, mappati su Lune I-IV, con soglie
5. **Economia** — tabella punti: massimo ottenibile per Luna vs soglie. Le soglie DEVONO essere raggiungibili (territorio ±1 una-tantum, eventi +1/+2); il 5/5 è "zero errori", mai "matematicamente impossibile"
6. **Finali** — condizioni in termini di variabili reali
7. **Budget** — scene da scrivere + asset mancanti (sprite, bg) con nomi file. Prima di dichiarare un asset "mancante", verifica con `ls "game/images/malandrini"` e `ls "game/gui/malandrini"`: elenca solo ciò che manca davvero

## Anti-cliché
- Il difetto del personaggio deve costare qualcosa al giocatore, non essere decorativo
- Niente "brava ragazza/o" puro: nel Nord tutti pagano un prezzo (Aede uccide, Caino tradisce, Druso è codardo, Icaro bara)
- Il good end rinegozia il difetto, non lo cancella

## Output
Proposta → `docs/superpowers/specs/` se approvata. Mai saltare da idea a codice senza spec.
