# Pacchetto grafico — punti 5, 6, 11, 14, 15, 21, 22, 23, 25, 26, 27, 28, 31, 32, 33, 34, 35 (design)

Data: 2026-10-22. Stato: approvato dal committente ("procedi pure").
Origine: lista "40 consigli grafici". Il committente ha scelto i punti sopra.
Il punto 20 (sigilli per personaggio) è stato tolto dal committente.
Il committente permette di modificare i file delle route (righe `show`,
`scene`, `with` e battute) per i punti che lo richiedono (14, 23, 34, 35).

## Intento

Il gioco ha già un'identità forte: tema rosso-oro-nero, Cinzel con
EB Garamond, transizione diagonale, particelle per sfondo, carosello del
cast e layout mobile. Questo pacchetto non cambia lo stile. Serve a dare
più vita e più regia alla scena: chi parla si vede, la luce dei luoghi
tocca i personaggi, le emozioni muovono gli sprite, la camera sottolinea
i momenti forti e le interfacce entrano in scena invece di comparire.

## Obiettivi
- Più leggibilità: chi parla, che cosa è pensiero, testo leggibile su
  ogni sfondo.
- Più atmosfera: luce dei luoghi sugli sprite, nuove particelle,
  profondità di campo.
- Più regia: micro-movimenti, transizioni con un significato, camera.
- UI più viva: menu principale, scelte, calendario, cartello del giorno,
  Borsa.

## Non-obiettivi
- Niente nuovi sfondi, sprite, espressioni o CG disegnati (punti non scelti).
- Niente `layeredimage`, niente sbattere di palpebre (punti 8, 9 non scelti).
- Niente sigilli per personaggio nella namebox (punto 20, tolto).
- Il testo delle scene non cambia. Il punto 23 cambia solo *chi* dice una
  riga di narrazione (narratore oppure `pensiero`), mai le parole.

## Anti-obiettivi (fallimento anche se "funziona")
- Movimento che stanca: scosse, zoom o tremolii a ogni battuta. Ogni
  effetto deve restare raro abbastanza da pesare.
- Qualcosa che ignora la preferenza "Animazioni: No"
  (`mm_movimento_ridotto()`). Con "No", ogni effetto di questo pacchetto è
  fermo o istantaneo; colori e contorni restano.
- Calo di prestazioni su Android (variant `small`/`touch`).
- Sprite che perdono la posizione (center/right/left) dopo un effetto.
- Rollback o caricamento che lasciano uno stato visivo sbagliato (camera
  zoomata, sfocatura rimasta, sprite scuro).

## Vincoli
- Ren'Py 8.3.7 (`camera`, `matrixcolor`, `blur`, ATL `function` disponibili).
- Stato solo visivo fuori dallo store quando possibile (pattern
  `NoRollback` già usato in `effetti.rpy`, `feedback.rpy`, `borsa.rpy`).
- Asset generati da script, come oggi: immagini in `make_gui.py`, suoni in
  `make_audio.py`. Sono segnaposto sostituibili.
- La logica pura (mappe sfondo→tinta, espressione→movimento, scelta della
  transizione) sta in un modulo `*_logic.py` testabile con
  `py -3 -I tests/test_*.py`, come gli altri moduli.
- Il lint di Ren'Py deve restare pulito. I test esistenti devono passare.
- Niente commit senza richiesta esplicita del committente.

## Parti

### A. Luce dei personaggi (11 + 15)
Un solo meccanismo calcola il `matrixcolor` di ogni sprite.
- **Tinta del luogo (15)**: una mappa sfondo → tinta tenue. Proposta:
  neve: blu freddo; Calà di notte: arancio caldo; vicoli di sera:
  blu scuro; studio di Glauco e corridoio del Ceppo: candela calda;
  arena: sole caldo; sala dello Svelo: oro. Sfondo senza voce nella mappa:
  nessuna tinta. Si tingono solo gli sprite: gli sfondi restano come
  sono (scelta del redattore: tingerli cambierebbe lo stile). La forza è
  una miscela di circa il 15-20% verso il colore della tinta: si sente,
  ma non snatura la pelle.
- **Chi non parla si scurisce (11)**: con 2 o più sprite in scena, quando
  parla un personaggio con sprite, gli altri scendono a circa il 75% di
  luminosità, con un passaggio di 0.2 s. Quando parlano il narratore, il
  protagonista (`pc`), `pensiero` o un personaggio senza sprite in scena,
  tutti restano a luce piena. Con uno sprite solo, niente scurimento.
- Approccio suggerito: definire le immagini degli sprite in un loop
  `init python` come `At(file, luce_personaggio(tag))`. Il transform usa
  una `function` che legge chi parla (da una callback delle Character) e
  lo sfondo in scena. Evitare `config.speaking_attribute`: gli sprite sono
  immagini semplici e non hanno l'attributo. L'approccio finale spetta al
  builder, purché le posizioni restino intatte.

### B. Micro-movimenti emotivi (14)
- Transform riusabili in `regia.rpy`: `sobbalzo` (sorpresa, salto breve),
  `arretra` (imbarazzo, indietro e un poco più piccolo), `avanza`
  (rabbia, avanti e un poco più grande), `trema` (paura, tremolio breve).
  Tutti tornano alla posa di partenza e conservano la posizione.
- **Automatico**: quando uno sprite già in scena cambia espressione verso
  una della mappa, parte il movimento. Proposta di mappa:
  sorpresa/sorpreso → sobbalzo; imbarazzata/imbarazzato → arretra;
  rabbia/furia/furioso/irritata/irritato → avanza. Alla prima entrata in
  scena non parte niente.
- **A mano**: nelle route si possono usare i transform per i momenti
  scritti (paura, uno shock senza cambio di espressione).
- Tetto: lo stesso sprite non ripete un movimento entro circa 3 battute.

### C. Profondità di campo (5)
- Transform/funzione `intimo` per sfocare lo sfondo (`blur` circa 6, con un
  passaggio di 0.4 s) e un'altra per toglierla. Si sfoca solo lo sfondo,
  mai gli sprite.
- Uso a mano nelle route: momenti intimi e confessioni, da 3 a 5 per route
  (Aede, Caino, Druso, Icaro, Ofelia). La sfocatura si toglie da sola a
  ogni `scene`.

### D. Nuove particelle (6)
Si aggiungono a `EFFETTI_SFONDI` e `FX_FABBRICHE` in `effetti.rpy`, con le
immagini generate da `make_gui.py`:
- braci che salgono: `bg studio_glauco`, `bg corridoio_ceppo`;
- nevischio mosso dal vento: `bg arena_athlion` (l'arena è innevata: la sabbia stonava; scelta presa durante il lavoro);
- pioggia: `bg vicoli_zefiro` negli slot non di sera, nei giorni di
  pioggia. Sono giorni deterministici dalla data (Luna, giorno), circa uno
  su tre, così il meteo è uguale in ogni partita. Di sera nei vicoli resta
  il fumo. Se l'audio lo permette, aggiungere un ambiente pioggia
  in `make_audio.py`.

### E. Testo e textbox (21, 22, 23, 25)
- **21 Continua**: il diamantino segue la fine del testo (stile
  `nestled`), con una piccola oscillazione verticale oltre alla pulsazione.
  In auto-avanzamento si mostra una variante (anello che si riempie o
  clessidra piccola).
- **22 Leggibilità**: contorno scuro sottile e ombra morbida al testo dei
  dialoghi, come già fatto per i nomi. Il risultato va verificato sulla
  neve e sulla sala dello Svelo, che sono gli sfondi più chiari.
- **23 Pensieri**: nuova `Character` `pensiero`, senza nome, con testo in
  corsivo e colore più tenue (circa `#c9bfa8`); la cronologia la mostra
  uguale. Nelle route le righe di narrazione che sono pura riflessione
  interiore (giudizio, ironia, domande a sé, ricordo) passano a
  `pensiero`. Le righe di azione e di descrizione restano al narratore.
  Esempio: "Due comandi su tre li sto rispettando." diventa pensiero;
  "Mi infilo in un corridoio laterale..." resta narrazione. Nel dubbio
  resta narrazione. Il testo non cambia. Il passaggio copre tutti i file
  di `game/routes/`, compresi quelli condivisi (snodi, attività, echi,
  origliati, epilogo...), per coerenza (scelta del redattore). Il
  committente non vuole rivedere l'elenco delle righe prima.
- **25 Entrata del box**: a ogni comparsa la textbox entra con fade e una
  salita di circa 20 px in circa 0.25 s
  (`config.window_show_transition`/`window_hide_transition`). Con
  movimento ridotto si usa solo il fade.

### F. Menu principale (26, 27)
- **26**: alla prima apertura i personaggi del carosello entrano in
  sequenza (uno ogni 0.1 s circa), la polvere dorata scende e il titolo
  ha un bagliore che respira. Dopo l'entrata il carosello funziona come
  oggi. Con movimento ridotto tutto è già al suo posto.
- **27**: si salva `persistent.ultimo_finale`. Il menu apre il carosello
  sul personaggio di quel finale e mette come fondo, dietro il pannello, lo
  sfondo legato alla route, sfocato e scurito. Proposta: Aede → Calà di
  notte, Caino → corridoio del Ceppo, Druso → palestra, Icaro → vicoli,
  Ofelia → consiglio. Ogni finale di una route, anche il suo finale
  neutro, usa lo sfondo e il personaggio di quella route. Solo
  `finale_neutro_semestre`, che non ha route, mette la neve come fondo e
  lascia il carosello sul centro di oggi (scelta del redattore). Senza
  finali visti il menu resta com'è oggi.

### G. Scelte (28)
- All'hover: spostamento di circa 10 px a destra, bagliore oro dietro il
  bottone e suono breve (nuovo effetto in `make_audio.py`).
- All'apertura del menu le scelte entrano in cascata (0.05 s una
  dall'altra).
- Quello che c'è già (◆ rosso, fogliolina "già vista") resta com'è.

### H. Calendario e cartello (31, 32)
- **31**: la schermata di pianificazione entra come una pergamena che si
  srotola dall'alto. Le voci entrano in cascata e c'è un suono di carta.
  All'uscita fa il contrario, più veloce. Va sostituita la `Dissolve(0.2)`
  di oggi in `cal_loop`.
- **32**: nel cartello del giorno il nome della Luna diventa più grande.
  Dopo il testo cade un sigillo di ceralacca (da circa zoom 1.6 a 1.0, con
  un piccolo rimbalzo) e un suono sordo. Il sigillo si genera in
  `make_gui.py` (c'è già la funzione `sigillo`). Nei giorni con evento
  fisso il sigillo è rosso; negli altri giorni è più scuro e sobrio. Il
  ◆ esistente resta. Il tempo totale del cartello resta circa 2.5 s.

### I. Borsa (33)
- Quando gli Scudi cambiano, il numero scorre dal vecchio al nuovo valore
  in circa 0.6 s. Sullo scudo passa un luccichio. Il +N/−N di oggi resta.

### J. Regia: transizioni e camera (34, 35)
- **34 Vocabolario delle transizioni**, in `regia.rpy`:
  - cambio luogo: `stacco` (c'è già);
  - salto di tempo nello stesso luogo: nuova `salto_tempo` (nero più
    lungo, circa 1.2 s);
  - shock: nuova `shock` (pixellate o glitch breve);
  - ricordo o flashback, se presente: nuova `ricordo` (dissolve lento con
    bagliore chiaro).
  Nelle route le `scene ... with fade/dissolve` si riassegnano con una
  regola: sfondo diverso dal precedente → `stacco`; stesso sfondo →
  `salto_tempo`. Il "precedente" è la `scene` prima nello stesso label;
  per la prima `scene` di un label vale "diverso" (→ `stacco`).
  Restano come sono (scelte del redattore): le `scene bg nero with fade`
  (dissolvenze al nero prima di cartelli e finali) e le `with lampo`.
  `shock` e `ricordo` si mettono a mano nei momenti giusti.
  Le `with qdiss` e le `with dissolve` sugli sprite restano. Si può
  scrivere uno script una tantum per la riassegnazione, che non va lasciato
  nel gioco.
- **35 Camera** (istruzione `camera` di Ren'Py): transform `zoom_dentro`
  (verso il centro, circa 1.08, lento), `zoom_su(x)` (verso una posizione),
  `panoramica` (per i luoghi aperti all'inizio di un capitolo) e
  `camera_riposo`. La camera torna a riposo a ogni `scene` e dopo un
  caricamento o un rollback. Uso a mano nelle route: rivelazioni,
  confessioni e battuta chiave dei good end, da 3 a 6 per route. Con
  movimento ridotto la camera non si muove mai.

## Lasciato al builder
- Il meccanismo tecnico esatto di A e B, purché rispetti il comportamento
  descritto e gli anti-obiettivi.
- I valori fini (colori delle tinte, durate, intensità), entro le
  indicazioni sopra.
- Quali righe sono pensiero (23) e dove mettere sfocatura e camera (5, 35),
  entro le regole sopra.
- L'ordine di lavoro. Suggerimento: A, E (senza 23), G, H, I, F, D, B, C,
  J, poi 23. I passaggi che riscrivono le route (23, 34) vanno per
  ultimi, sullo stato più recente dei file.

## Verifica
- Test Python per le mappe e le regole pure (tinta per sfondo, movimento
  per espressione, giorni di pioggia, scelta della transizione).
- Lint di Ren'Py pulito.
- Prova a mano: una scena con due personaggi per ogni route, il menu
  principale con e senza finali visti, il calendario, un cambio di Scudi,
  "Animazioni: No", la variante mobile, un rollback e un caricamento a
  metà di uno zoom.
