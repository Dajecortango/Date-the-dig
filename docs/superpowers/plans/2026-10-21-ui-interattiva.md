# UI interattiva e presentazione — piano

> Richiesta utente: punti 1,2,3,4,5,6,7,8,11,12,13 della lista di consigli UI.
> Design del builder (domande saltate). Branch `feat/route-ofelia`, niente commit.
> Stile: GUI Dignitas rosso-oro-nero (`make_gui.py`: costanti NERO, ORO, ROSSO;
> font e stili in `gui.rpy` / `screens.rpy`). Ren'Py 8.3.7.

**Verifica di ogni blocco:** `py -3 -I tests/test_calendario.py` → `tutti i casi ok`;
`py -3 -I tests/test_routing.py` → `6/6 scenari ok`;
`"./tools/renpy-8.3.7-sdk/renpy.exe" . lint` senza errori né warning nuovi.
Asset grafici nuovi: solo generati con PIL da funzioni aggiunte a `make_gui.py`
(eseguire solo le funzioni nuove, non `main()` intero). Niente `git commit/add/stash`.

---

### Blocco M — Menu principale (punti 1, 2, 3)

1. **Personaggi cliccabili.** `menu_front()` in `make_gui.py` torna a produrre solo
   pannello + pergamena (niente cast); rigenerare `mm_front.png` e `main_menu.png`.
   Il cast diventa parte della screen `main_menu` (nuovo file
   `game/menu_cast.rpy`): stessa fila e stesse posizioni/scale di oggi
   (Aede 772/0.62, Ofelia 964/0.60, Caino 1226/0.56, Icaro 1519/0.52,
   Druso 1736/0.58; centro x / scala, piedi al bordo basso; stessa ombra sfocata).
   Ogni personaggio è un `imagebutton` (focus mask sull'alpha):
   hover → leggero schiarimento/alone oro + riquadro con nome, nome route e una
   battuta tipica; click → screen `scheda_personaggio(char)` (modal, stile
   game_menu): ritratto grande, nome route, difficoltà (x/5), 2-3 righe dal
   profilo (`docs/profili/*.md`, Caino dalla sua spec), finali sbloccati di quel
   personaggio dalla galleria (`FINALI`, `persistent.finali_visti`).
   Route: Aede "Tempesta d'amore" 3/5; Ofelia "Tanto bella quanto letale" 4/5;
   Caino "La legge del cuore" (dal cartello del good end) difficoltà dalla spec;
   Druso "Il cuore provocatore" 4/5 (5/5 da uomo); Icaro "Untouchable" 5/5.
2. **Menu vivo.** Respiro ATL sugli sprite del cast (zoom/yoffset minimi, periodi
   sfasati); neve leggera (`SnowBlossom` con fiocco generato in PIL,
   `gui/fiocco.png`) sopra il pattern e sotto il pannello; parallasse leggera del
   cast col mouse (pochi pixel, transform function con `renpy.get_mouse_pos`).
   Tutto disattivabile: rispettare la preferenza `_preferences.reduce_motion`
   se disponibile, altrimenti nessun obbligo.
3. **Continua.** Nel main menu, primo pulsante "Continua" se esiste un
   salvataggio: carica il più recente (`renpy.newest_slot()` + `FileLoad(..., slot=True)`).

### Blocco G — Durante il gioco (punti 4, 5, 6, 7, 11)

4. **Ritorno visivo sulle scelte.** Overlay generico (screen in
   `config.overlay_screens`, nuovo file `game/feedback.rpy`) che confronta
   periodicamente le affinità di store (`aede_affinity`, `caino_fiducia`,
   `druso_affinity`, `icaro_affinity`, `ofelia_affinity`) con l'ultimo valore
   visto; su variazione: ritratto del personaggio che pulsa in un angolo +
   riga breve ("Aede se lo ricorderà." / "Aede non lo dimenticherà." per i cali),
   ~2 s, poi sparisce. Nessun numero. Non deve scattare al caricamento di un
   salvataggio né all'inizio partita (inizializza lo snapshot senza mostrare).
   Lo snapshot non deve finire nei salvataggi come fonte di verità (variabili
   con `_` o non-store).
5. **Data animata.** Il `centered "{cps=30}[LUNE_NOMI...] — giorno ..."` in
   `cal_loop` diventa una screen `cartello_data(luna, giorno, festa)`: pergamena
   (generata in PIL, `gui/cartello_data.png`) che si srotola (ATL crop/zoom),
   nome della Luna, giorno, ◆ se il giorno ha un evento fisso con cond vera
   (stessa logica di `cal_strip`). Click o ~2.5 s per proseguire.
6. **Menu di scelta.** Screen `choice`: hover con allargamento lieve + bordo oro.
   Supporto argomento di menu `(peso=True)` → diamante rosso accanto alla scelta.
   Marcare `peso=True` nelle scelte di impegno (`impegno_*`) e nelle scelte dei
   climax di ogni route.
7. **Ritratto accanto al box.** Side image per chi parla: `image side <char>` dai
   `gui/portrait_<char>.png` (Aede, Caino, Ofelia, Druso, Icaro) e
   `image="<char>"` nelle `Character(...)` relative. Nessun ritratto per gli
   altri.
11. **Transizioni a tema.** Nuove `define` in `game/regia.rpy`: uno stacco a tema
    per i cambi scena (es. `ImageDissolve` con maschera diagonale generata in PIL)
    e `lampo_oro` (Fade color oro) per momenti solenni; impostare
    `config.after_load_transition`, `config.end_game_transition` e
    `config.intra_transition`. Usare `lampo_oro` sui cartelli dei finali (prima
    del `centered` dei good end). Non riscrivere tutte le `with fade` delle scene.

### Blocco P — Pianificatore, salvataggi, preferenze (punti 8, 12, 13)

8. **Pianificatore** (`screen pianificazione` in `game/calendario.rpy`): hover su
   attività/invito con personaggio → pannello laterale con ritratto grande e
   descrizione; inviti con `scade` → piccola clessidra animata (ATL, immagine
   PIL `gui/clessidra.png`) al posto/accanto a "Solo adesso"; in testa una luna
   (fase per Luna I-VI, PIL) accanto al nome della Luna.
12. **Salvataggi** (`file_slots` in `screens.rpy`): ogni slot mostra `save_name`
   (data di gioco, già impostata in `cal_loop`) e il ritratto della route attiva
   (salvata via `config.save_json_callbacks` → `FileJson(slot, "route")`).
13. **Accessibilità** (`preferences`): slider grandezza testo
   (`Preference("font size", ...)`) e velocità testo (già presente? verificare;
   se c'è, lasciarla), con etichette in italiano coerenti con le altre.
