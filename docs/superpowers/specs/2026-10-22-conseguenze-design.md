# Albero delle conseguenze e mondo reattivo (design)

Data: 2026-10-22. Stato: approvato dal committente ("mi piace la tua proposta,
ma le route devono avere senso logico e gli eventi non vanno arrangiati a
caso: puoi procedere").

## Intento

Oggi ogni route è una catena di eventi a soglia e le scelte muovono quasi
solo affinità nascoste: il resto del mondo non se ne accorge. Obiettivo: le
scelte lasciano **fatti** che il mondo ricorda, che tornano come **echi** in
altre scene, e che il giocatore vede in un **albero delle conseguenze**.

## Vincolo del committente: niente eventi a caso

- L'ordine degli eventi di ogni route NON cambia. Le catene `cond` esistenti
  (cap1 → cap2 → ...) restano: sono la logica del racconto.
- Niente estrazioni casuali di eventi narrativi. Il caso resta solo dove c'è
  già (commissioni in città).
- La reattività viene dallo stato: un eco scatta solo se il fatto che racconta
  è già successo, in un'altra scena, e da almeno due slot (il pettegolezzo ha
  bisogno di tempo per viaggiare).
- Chi racconta un eco deve poterlo sapere: chi era presente, chi frequenta il
  luogo, o chi raccoglie pettegolezzi per mestiere (Vanna, Corrado, Ottone).

## Fase 1 (questa consegna)

### Registro delle scelte (automatico)
- `define menu = conseguenze_menu`: ogni menu del gioco passa da un wrapper
  di `renpy.display_menu` che registra la scelta. Zero modifiche alle scene.
- Firma del menu: contesto + didascalia (o prima opzione). Il contesto è
  l'evento o la scena del calendario in corso (`cal_contesto`).
- `scelte_partita` (store): firma → testo scelto in questa partita.
- `persistent.opzioni_viste` / `persistent.opzioni_scelte`: le opzioni viste e
  scelte in tutte le partite, per l'albero.

### Fatti
- Registry `FATTI` in `game/conseguenze.rpy`: id, personaggio, testo per
  l'albero, avviso, condizione sullo stato (variabili esistenti o scelte).
- I fatti si derivano dalle variabili già scritte dalle scene: nessuna scena
  cambia per produrli.
- Dopo ogni evento e attività il motore registra i fatti nuovi in
  `fatti_noti` (id → contesto e momento in cui sono nati).

### Avviso
- "Caino se ne ricorderà." con `renpy.notify` quando nasce un fatto con
  avviso. Disattivabile da Preferenze ("Avvisi delle conseguenze").

### Echi
- Registry `ECHI`: id, fatto richiesto, attività in cui può comparire, label.
- A fine attività del calendario il motore gioca al massimo un eco idoneo,
  una volta sola per partita. Scene di 2-5 righe in `game/routes/echi.rpy`.

### Albero delle conseguenze (schermata "Trama")
- Dal menu di gioco e dal diario. Una scheda per route più "Comune".
- Nodi = eventi del registry nell'ordine del racconto. Stato: vissuto in
  questa partita (◆), vissuto in un'altra partita (◇), mai visto (— ? —).
- Sotto ogni nodo: le scelte del nodo. Scelta di questa partita in oro,
  scelte di altre partite attenuate, opzioni viste e mai scelte in grigio.
- Sotto ogni nodo: i fatti nati lì. Route congelata: riga "La porta si è
  chiusa".

## Fasi successive (da spec dedicata prima del codice)

- **Eventi reattivi tra route**: eventi a soglia su combinazioni di fatti
  (es. debito con Icaro + amicizia con Caino), sempre in Lune I-IV, sempre con
  `cond` esplicita e in coda alla catena della route, mai al posto di un cap.
- **Il mondo va avanti**: inviti ignorati che producono un fatto ("ci è andato
  qualcun altro") ripreso in Luna V-VI.
- **Minigiochi di territorio** (duello con Aede per primo): esito = fatto,
  non solo punti. Brevi, saltabili, giocabili su touch.

## Anti-goals

- Riordinare o randomizzare i capitoli delle route.
- Echi che rivelano cose che chi parla non può sapere.
- Statistiche numeriche visibili (l'albero mostra scelte e fatti, mai punti).
