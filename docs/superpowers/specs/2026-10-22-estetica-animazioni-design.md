# Estetica e animazioni — pacchetto 2 (design)

Data: 2026-10-22. Stato: approvato dal committente ("va bbene"). Punti 1, 3, 11, 12, 15, 17, 20, 21,
22, 23, 29, 33, 35 della lista "40 consigli estetici" (richiesta del
committente: "fai 1, 3, 11, 12, 15, 17, 20, 21, 22, 23, 29, 33, 35"; per 1
e 3: "dove hanno senso").

## Punto di partenza (già nel gioco, commit a541f57)

- `game/luce.rpy`: ogni sprite `images/<tag> <espressione>` è ridefinito come
  `At(file, luce_personaggio(tag))`. La funzione fa tinta del luogo,
  luce ridotta a chi ascolta (**punto 12: già fatto**, nessun lavoro) e
  movimenti automatici al cambio d'espressione (`sobbalzo`, `arretra`,
  `avanza`; mappa `MOVIMENTI` in `regia_logic.py`). Stato fuori dallo store
  (`_LuceStato`, NoRollback).
- `game/regia.rpy`: transizioni `stacco`, `salto_tempo`, `shock`,
  `ricordo`, `lampo`, `lampo_oro`; camera; `intimo()`. Le `scene ... with
  fade/dissolve` diventano già in automatico `stacco` o `salto_tempo`
  (`rgl.transizione_scene`).
- `game/effetti.rpy`: particelle per sfondo (layer `effetti`, `SnowBlossom`
  in `FxOrologio`), registro `EFFETTI_SFONDI`, fabbriche `FX_FABBRICHE`.
  Immagini da `make_gui.py` (`particelle_effetti`).
- `game/borsa.rpy`: HUD della Borsa con contatore che scorre e suono moneta.
- `game/calendario.rpy`: `screen cartello_data` (cartello che si srotola,
  ceralacca, suono del sigillo); immagini `gui/luna_1..6.png`.
- Logica pura in `game/regia_logic.py`, test in `tests/test_regia.py`.

## Vincoli per tutto il pacchetto

- Il testo delle scene non cambia. Nelle scene si aggiungono solo righe di
  regia (`$ muovi(...)`, `with ricordo`, `$ lento()`).
- Tutto si spegne con "Animazioni: No" (`mm_movimento_ridotto()`) e in skip
  (`renpy.is_skipping()`), come il resto della regia.
- Su telefono (`renpy.variant("small")`) le particelle nuove sono la metà,
  come già fa la pioggia.
- Stato visivo fuori dallo store (NoRollback) come `luce.rpy`: niente nei
  salvataggi.
- Regole e numeri in `regia_logic.py` (puri, testati in
  `tests/test_regia.py`); i `.rpy` li applicano.
- Si estende quello che c'è (registry, `luce_personaggio`, `effetti_scena`,
  `make_gui.py`), niente sistemi paralleli.

## Personaggi

### 1. Movimenti dove hanno senso
- `MOVIMENTI`: `furia`, `furioso` e `minaccioso` passano a `trema`
  (oggi `furia`/`furioso` = `avanza`; `rabbia` e `irritat*` restano
  `avanza`).
- Nuovo `$ muovi(tag, nome)` in `luce.rpy`: fa partire un movimento sullo
  sprite già in scena senza toccare la posizione (scrive `_lu.mov`). Rispetta
  la pausa `MOVIMENTO_PAUSA` e "Animazioni: No".
- Uso nelle scene, "dove ha senso": momenti senza cambio d'espressione ma con
  un gesto fisico chiaro nel testo (un colpo incassato, un passo verso
  qualcuno, uno scatto). Criterio per chi costruisce: al massimo uno ogni
  ~10 righe per personaggio, mai su righe con `vpunch`/`hpunch` già presenti
  (lo schermo trema già). Lista dei punti scelti nel resoconto finale.

### 11. Respiro
- Dentro `luce_personaggio`: zoom 1.0 → 1.006 e ritorno, periodo ~4.2 s,
  fase diversa per tag (così due sprite non respirano all'unisono).
- Si somma al movimento (zoom moltiplicato). Fermo con "Animazioni: No",
  in skip, e mentre lo sprite è oscurato? No: respira sempre, è vivo.
- Costo: oggi la funzione si ridisegna ogni 0.1 s da ferma; col respiro
  serve un ridisegno ~30 fps. Su "small" 15 fps.
- Ancoraggio: lo sprite resta poggiato in basso (il respiro non lo solleva).

### 15. Entrata di Druso
- Automatica, nessuna scena toccata: ogni volta che `druso` entra in una
  scena (tag nuovo tra quelli mostrati) parte il movimento `tonfo`. È il
  suo marchio, quindi vale a ogni entrata, non una volta per partita (lo
  stato visivo non va nei salvataggi). (Scelta di Claude.)
  Il movimento:
  schiacciamento verso il basso e rimbalzo (yoffset +10 → 0, zoom 1.02 →
  1.0, ~0.35 s), a fine scivolata. Solo per Druso.
- Suono: nessuno (le sue entrate hanno già il loro ritmo di testo).

### 17. Ombra a terra
- Ellisse morbida scura sotto i piedi di ogni sprite, generata da
  `make_gui.py` (`gui/ombra_sprite.png`, ~520×70, nero al 35% sfumato).
- Montata nella ridefinizione degli sprite di `luce.rpy`, dietro lo sprite,
  centrata in basso. Non prende la tinta e non respira.
- Gli sprite hanno i piedi sul bordo dello schermo: dell'ombra si vede solo
  la metà superiore. Va bene così (non si alzano gli sprite); l'immagine è
  disegnata perché la mezza ellisse si legga come ombra. (Scelta di Claude.)

### 3. `ricordo` dove ha senso
- `with ricordo` sulle `scene`/`show` che aprono un ricordo o un flashback
  vero (il narratore rivive un momento passato), non sugli echi di
  pettegolezzo. Candidati da verificare: `routes/ricordi.rpy`, gli echi che
  rievocano una scena vissuta insieme, i passaggi "mi torna in mente".
- Lista dei punti nel resoconto finale. `transizione_scene` non tocca
  `ricordo` (solo `fade`/`dissolve`): nessuna modifica lì.

## Luoghi

### 20. Luce viva
- Sfondi col fuoco (`studio_glauco`, `corridoio_ceppo`, `cala_notte`,
  `vicoli_zefiro` di sera): la tinta degli sprite tremola di ±3% con un
  rumore lento (somma di 2-3 sinusoidi, 0.3-0.8 Hz), non un lampeggio.
- Sullo sfondo: velo caldo (`#ffb066`) dietro gli sprite, nella
  trasformazione dello sfondo (`fondo_fx` in `luce.rpy`), non sul layer
  `effetti` (scalderebbe due volte gli sprite). Alfa che oscilla 0.02-0.06
  con lo stesso rumore. (Scelta di Claude.)

### 21. Particelle nuove, per contesto
- Nuovo registro `EFFETTI_CONTESTO`: righe (contesto, sfondo, effetto,
  modo). Vale solo se **anche lo sfondo** corrisponde: lo stesso evento può
  cambiare luogo a metà (es. `ofelia_ev3` va dall'arena alla Calà) e
  l'effetto non deve seguirlo. Modo `"aggiungi"` (si somma all'effetto
  dello sfondo) o `"sostituisci"`. (Scelta di Claude.)
  - corte di Ofelia (attività `corte` e scene della serra) su
    `sala_svelo`: `foglie` (foglie verdi e petali che scendono piano),
    **sostituisce** la `polvere` dorata (la serra non è la sala dello Svelo);
  - fumeria (attività `fumeria`, eventi di Icaro in fumeria) su
    `vicoli_zefiro`: `fumo_pipa` (più denso e basso), **sostituisce** il
    `fumo` di sera; i `luccichii` restano;
  - arena (evento `athlion`, duello `ofelia_ev3`) su `arena_athlion`:
    `scintille`, **si aggiunge** al `nevischio`.
- Il contesto è `cal_contesto` (id di evento o di attività). Chi costruisce
  verifica gli id esatti.
- `effetto_corrente` può restituire più effetti insieme (tupla), così
  scintille + nevischio e luccichii + fumo convivono.

### 22. Neve fitta nei climax
- Solo nel climax vero, non nei finali né nell'epilogo (che restano nello
  stesso contesto `luna6_climax`). Segnale: `$ tempesta()` scritto nei
  label di climax subito dopo la `scene bg esterno_neve` (oggi uno solo:
  `climax` in `aede_finali.rpy`); ogni `scene` lo spegne, come `intimo()`.
  (Scelta di Claude.)
- Effetto `neve_fitta` al posto di `neve`: circa il doppio dei fiocchi, più
  veloci, un velo bianco 0.04 in più.

### 23. Riflessi nei vicoli
- `bg vicoli_zefiro`: `luccichii`, punti di luce piccoli che scorrono piano
  in orizzontale nel quarto basso dello schermo e pulsano. È
  un'approssimazione dei canali ghiacciati (non c'è uno shader d'acqua).
  Non con la pioggia. Insieme al `fumo` di sera.

## Testo e interfaccia

### 29. Testo più lento nei momenti intimi
- `$ lento()` / `$ fine_lento()`: con `lento` attivo le battute scorrono
  al 70% della velocità scelta dal giocatore (moltiplicatore, non valore
  fisso). Ogni `scene` lo spegne, come `intimo()`.
- Implementazione: `config.say_arguments_callback` aggiunge
  `what_slow_cps_multiplier`; chi costruisce verifica che Ren'Py 8.3.7 lo
  accetti, altrimenti ripiega su un filtro che antepone `{cps=*0.7}`.
- Dove: impegni (scelta del cuore), confessioni dei climax, finali buoni e
  "passeggeri". Lista nel resoconto finale.
- Non tocca i `centered` dei finali (hanno già `{cps=20}`).

### 33. Cartello del giorno
- Il numero del giorno "gira": il vecchio esce verso l'alto, il nuovo entra
  dal basso (0.35 s, ease-out), mentre il cartello si srotola.
- Primo giorno di una Luna nuova: sopra il nome compare per l'occasione
  un'icona di luna (elemento temporaneo, il cartello degli altri giorni non
  cambia): la luna precedente (`gui/luna_<n-1>.png`) sfuma nella nuova, con
  un piccolo bagliore oro, poi l'icona resta fino alla chiusura del
  cartello. (Scelta di Claude.)
- Il cartello deve sapere il giorno precedente: lo passa `cal_giorno_segnato`
  o un parametro nuovo dello screen.

### 35. Monete che volano
- Quando gli Scudi salgono: da 2 a 5 monete (in base al guadagno, regola in
  `regia_logic`) partono dal centro basso dello schermo e volano in arco
  verso la pillola della Borsa, in fila (0.06 s tra una e l'altra, 0.55 s di
  volo, ease-in-out). Il contatore parte quando arriva la prima.
- Quando scendono: 1-3 monete escono dalla Borsa e cadono svanendo.
- Immagine: `gui/scudo.png` rimpicciolito (esiste già).

## Test (in `tests/test_regia.py`)

- `MOVIMENTI` aggiornata; curva `tonfo` (parte e torna a 0).
- Respiro: ampiezza massima 0.006, periodo, fase diversa per tag.
- Rumore della luce: dentro ±3%, continuo (salti piccoli tra frame vicini).
- Selezione effetti: contesto prima dello sfondo, più effetti insieme,
  niente luccichii con la pioggia, neve fitta solo nel climax.
- Monete: numero per delta (+1 → 2, grandi guadagni → 5, perdite 1-3).
- Lento: moltiplicatore 0.7 attivo/spento.
- Cablaggio (grep sui `.rpy`): `muovi` definito, `lento` spento da `scene`,
  effetti registrati nelle fabbriche, immagini nuove generate da
  `make_gui.py`.

## Non-obiettivi
- Punto 12 (già fatto).
- Riscrivere testo, aggiungere sprite o sfondi disegnati.
- Shader d'acqua veri.

## Anti-obiettivi
- Movimento ovunque: se ogni battuta si muove, niente si nota più.
- Cali di fps su Android (respiro + particelle + luce insieme).
- Effetti che restano accesi con "Animazioni: No".

## Lasciato a chi costruisce
- Valori fini delle curve (entro i limiti scritti), forme delle particelle.
- Scelta precisa dei punti per `muovi`, `ricordo`, `lento`, secondo i
  criteri sopra.
