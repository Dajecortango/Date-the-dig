# Capitoli scalabili — piano di implementazione

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** trasformare Date the Dignitas in una raccolta di capitoli indipendenti. Malandrini diventa il capitolo 1 senza cambiare il gioco, e un capitolo nuovo si aggiunge con una cartella e una registrazione.

**Architecture:** un registro puro (`game/capitoli_logic.py`) descrive ogni capitolo: ingresso, funzioni usate, finali, tabelle di regia/audio/feedback, cast del menu. Lo store contiene solo l'id (`capitolo_corrente`). Il codice comune (`regia_logic`, luce, effetti, audio, feedback, screens, menu) legge le tabelle dal capitolo corrente invece che da costanti con nomi di Malandrini. Malandrini vive in `game/capitoli/malandrini/`, che è anche un package Python per i suoi moduli puri. Gli asset stanno in `game/images|gui|audio/<capitolo>/`.

**Tech Stack:** Ren'Py 8.3.7, Python 3, test con script `py -3 -I -X utf8` (niente pytest).

**Spec:** `docs/superpowers/specs/2026-10-23-capitoli-scalabili-design.md`

## Global Constraints

- Comandi di verifica (Git Bash, dalla radice del repo):
  - Lint: `./tools/renpy-8.3.7-sdk/lib/py3-windows-x86_64/python.exe ./tools/renpy-8.3.7-sdk/renpy.py . lint </dev/null`, deve dire `Lint is not a substitute for thorough testing` e nessun errore.
  - Test: `for t in tests/test_*.py; do py -3 -I -X utf8 "$t" </dev/null; done 2>&1 | grep -E "^FAIL|Traceback"`, nessuna riga.
- Nessuna rinomina di label, variabili di store o `persistent` di Malandrini.
- Nessun cambio di testo, bilanciamento o comportamento di gioco in Malandrini.
- Nel codice comune non compaiono nomi di Malandrini (personaggi, sfondi, variabili). Unica eccezione: la registrazione in `game/capitoli/malandrini/capitolo.rpy`.
- Lo store contiene solo stringhe di id di capitolo, mai oggetti `Capitolo` (regola pickle del progetto).
- I nomi di immagini, label e id dei finali sono unici in tutto il gioco. I capitoli nuovi usano un prefisso (`<id>_`).
- Commit: **solo quando l'utente lo chiede** (regola di memoria del progetto). I passi "Commit" preparano lo stage e il messaggio, e si eseguono solo su richiesta.
- Branch di lavoro: `feat/capitoli`, creato da `feat/route-ofelia`.
- I `.rpyc` vecchi si cancellano dopo gli spostamenti: la compatibilità dei salvataggi beta non serve.

## Review Focus

1. Caricamento di un salvataggio e rollback a metà Malandrini: `capitolo_corrente` torna `"malandrini"`, e HUD borsa/calendario e pulsanti del menu di gioco ci sono subito. Test in Task 6.
2. `persistent.ultimo_capitolo` punta a un capitolo non più registrato (es. il capitolo finto rimosso): il menu principale ripiega sul primo capitolo, senza crash. Test in Task 1 (`capitolo_menu`).
3. `persistent.finali_visti` contiene id di un capitolo non registrato: la galleria e i contatori li ignorano. Test in Task 1 (`finali_contati`).
4. Un capitolo senza tabelle di regia, audio o feedback: niente effetti, tinte, ambiente o popup, e nessun crash. Test in Task 4 (tabelle vuote) e Task 10 (capitolo finto).
5. Telefono (variante `small`): le carte di scelta del capitolo restano leggibili e cliccabili. Verifica manuale in Task 7 con `config.variants = ["small", "touch"]` temporaneo.

---

### Task 1: Registro puro dei capitoli

**Files:**
- Create: `game/capitoli_logic.py`
- Test: `tests/test_capitoli.py` (stesso stile degli altri test: funzione `check(nome, ottenuto, atteso)`, stampa `ok`/`FAIL`)

**Interfaces:**
- Produces:
  - `class Capitolo` con attributi: `id: str`, `numero: int`, `titolo: str`, `sottotitolo: str`, `ingresso: str` (label), `copertina: str|None`, `funzioni: frozenset[str]`, `finali: list[tuple(fid, titolo, gruppo, indizio)]`, `gruppi_finali: list[str]`, `cast_menu: list|None`, `affinita: list[tuple(var, ritratto, nome)]`, `regia: object|None` (modulo con le tabelle di Task 4), `ambienti: dict`, `ambiente_pioggia: dict`, `ambiente_arrivo: dict`, `entrate: dict[tag, (movimento, ritardo)]`, `ritratto: callable|None`, `dopo_caricamento: list[callable]`.
  - `registra(**campi) -> Capitolo`: campi mancanti con default vuoti (`frozenset()`, `[]`, `{}`, `None`).
  - `elenco() -> list[Capitolo]`, ordinato per `numero`.
  - `ottieni(cid) -> Capitolo|None`.
  - `ha(cid, funzione) -> bool`: False se `cid` è sconosciuto.
  - `capitolo_menu(ultimo) -> Capitolo|None`: `ottieni(ultimo)` oppure il primo di `elenco()`, oppure None se il registro è vuoto.
  - `capitolo_di_finale(fid) -> Capitolo|None`.
  - `finali_contati(cid, visti) -> (int visti, int totali)`: conta solo i finali di quel capitolo.
  - `svuota()`: solo per i test.
- Registro a livello di modulo (`_REGISTRO`), riempito a init e mai salvato.

- [ ] **Step 1: Write the failing test** `tests/test_capitoli.py`, con questi controlli:
  - `registra(id="a", numero=2, ...)` e `registra(id="b", numero=1, ...)`, poi `[c.id for c in elenco()] == ["b", "a"]`.
  - Registrare di nuovo `id="a"` solleva `ValueError`.
  - Un id di finale già usato da un altro capitolo solleva `ValueError`.
  - `ha("a", "borsa")` è True con `funzioni={"borsa"}`; `ha("zzz", "borsa")` è False.
  - `capitolo_menu("zzz").id == "b"`; con registro vuoto `capitolo_menu("a") is None`.
  - `finali_contati("a", {"a_fine", "x_estraneo"}) == (1, 2)` con due finali in "a".
  - `capitolo_di_finale("a_fine").id == "a"`; `capitolo_di_finale("nessuno") is None`.
- [ ] **Step 2: Run test to verify it fails.** `py -3 -I -X utf8 tests/test_capitoli.py`. Atteso: `ModuleNotFoundError: capitoli_logic`.
- [ ] **Step 3: Implement** `game/capitoli_logic.py` con le interfacce sopra. `Capitolo` è un oggetto semplice con `__slots__`, senza lambda nei campi di default.
- [ ] **Step 4: Run test to verify it passes.** Lo stesso comando: tutte le righe `ok`.
- [ ] **Step 5: Commit (solo su richiesta).** `git checkout -b feat/capitoli`; messaggio `feat: registro puro dei capitoli`.

### Task 2: Package Python di Malandrini

**Files:**
- Create: `game/capitoli/__init__.py`, `game/capitoli/malandrini/__init__.py` (vuoti, con un commento di una riga).
- Move (`git mv`): `game/{calendario,routing,relazioni,economia,conseguenze,minigiochi}_logic.py` dentro `game/capitoli/malandrini/`.
- Modify: gli `import` in `game/calendario.rpy`, `game/economia_extra.rpy`, `game/conseguenze.rpy`, `game/minigiochi.rpy`.
- Create: `tests/percorsi.py`
- Modify: tutti i `tests/test_*.py` che importano quei moduli o leggono file di Malandrini.

**Interfaces:**
- Produces:
  - Negli `.rpy`: `from capitoli.malandrini import routing_logic as rl` (stessi alias di oggi: `cl`, `rl`, `rlz`, `ecl`, `csl`, `mgl`).
  - `tests/percorsi.py` espone `HERE`, `GAME`, `MAL` (`game/capitoli/malandrini`) e `prepara_import()`, che inserisce `GAME` e `MAL` in `sys.path`. Così i test continuano a fare `import routing_logic as rl`.
  - Le funzioni di lettura dei test (`_leggi`, `leggi`) accettano percorsi relativi a `MAL` per i file di Malandrini. Il percorso nuovo serve dopo Task 5; in questo task cambia solo il `sys.path`.

- [ ] **Step 1: Spike.** Dopo il `git mv` e il cambio degli import, esegui il lint. Se Ren'Py non importa il package (errore `ImportError`/`ModuleNotFoundError` su `capitoli.malandrini`), torna indietro: tieni i moduli in `game/` con il prefisso `malandrini_` nel nome file (es. `malandrini_routing_logic.py`), import `import malandrini_routing_logic as rl`, e annota la scelta in `ASSETS.md` (Task 9). Il resto del piano non cambia.
- [ ] **Step 2: Aggiorna i test** con `from percorsi import prepara_import; prepara_import()` al posto dei `sys.path.insert(...)`.
- [ ] **Step 3: Verifica.** Lint pulito; test senza `FAIL`/`Traceback`.
- [ ] **Step 4: Commit (solo su richiesta).** Messaggio `refactor: moduli puri di Malandrini in un package del capitolo`.

### Task 3: API dei capitoli in Ren'Py e registrazione di Malandrini

**Files:**
- Create: `game/capitoli.rpy` (API comune; la screen di scelta del capitolo arriva in Task 7)
- Create: `game/capitoli/malandrini/capitolo.rpy`
- Modify: `game/routes/chapter1.rpy` (label `capitolo1`)

**Interfaces:**
- Consumes: `capitoli_logic` (Task 1).
- Produces, in `game/capitoli.rpy`:
  - `init -20 python`: `import capitoli_logic as rcap`.
  - `default capitolo_corrente = "malandrini"`, `default persistent.ultimo_capitolo = "malandrini"`.
  - `capitolo()`: restituisce `rcap.ottieni(store.capitolo_corrente)` (può essere None).
  - `capitolo_ha(funzione) -> bool`: False al menu principale.
  - `entra_capitolo(cid)`: imposta `store.capitolo_corrente` e `persistent.ultimo_capitolo`.
  - Un `config.after_load_callbacks` comune che chiama i `dopo_caricamento` del capitolo corrente.
- Produces, in `capitolo.rpy`:
  - `init 10 python: rcap.registra(id="malandrini", numero=1, titolo="Malandrini", sottotitolo="Sei Lune a Rocca Tempesta", ingresso="capitolo1", copertina=None, funzioni={"calendario", "borsa", "diario", "cronache", "trama"}, ...)`.
  - Campi ancora vuoti: si riempiono nei task 4-8.
- `capitolo1`: prima riga `$ entra_capitolo("malandrini")`.

- [ ] **Step 1: Test.** In `tests/test_capitoli.py`, leggendo i sorgenti:
  - `capitolo.rpy` contiene `id="malandrini"` e `ingresso="capitolo1"`;
  - il corpo di `label capitolo1:` contiene `entra_capitolo("malandrini")`.
- [ ] **Step 2: Run.** Il test fallisce.
- [ ] **Step 3: Implement.** Sposta `_conseguenze_migra_salvataggio` da `config.after_load_callbacks` a `dopo_caricamento` della registrazione. La sua chiamata va resa sicura anche quando la registrazione gira prima del caricamento.
- [ ] **Step 4: Verifica.** Test e lint puliti.
- [ ] **Step 5: Commit (solo su richiesta).** Messaggio `feat: API dei capitoli e registrazione di Malandrini`.

### Task 4: Codice comune senza nomi di Malandrini

**Files:**
- Create: `game/capitoli/malandrini/regia_tabelle.py`. Riceve da `regia_logic.py` `TINTE`, `TINTE_SOLO_SERA`, `FONDI_ROUTE`, `FONDO_SEMESTRE`, `FUOCO`, `FUOCO_SOLO_SERA`, `EFFETTI_SFONDI` ed `EFFETTI_CONTESTO`. Aggiunge `EFFETTI_ASCIUTTO = (("vicoli_zefiro", "luccichii"),)`, che oggi è il caso `bg == "vicoli_zefiro" and not piove` scritto direttamente nel codice.
- Modify: `game/regia_logic.py`. Ogni funzione che usava quelle tabelle riceve `tab` come ultimo parametro (un modulo o oggetto con quegli attributi, oppure None):
  - `tinta_per(bg, slot, tab)`;
  - `fuoco_per(bg, slot, tab)`;
  - `effetti_per(bg, slot, contesto, piove, tempesta, tab)`;
  - `fondo_menu(ultimo, finali, tab)`.

  Con `tab=None` restituiscono "niente" (`None` / `()` / `(None, ...)` come il caso "nessuna corrispondenza" di oggi).
- Modify:
  - `game/effetti.rpy`, `game/luce.rpy`, `game/regia.rpy`, `game/menu_cast.rpy`, `game/borsa.rpy` (chiamate a `rgl.*`): passano `capitolo_regia()`. È una nuova funzione in `game/capitoli.rpy`, che restituisce `capitolo().regia` oppure None.
  - `game/audio.rpy`: `AMBIENTI`, la sostituzione della pioggia e la campana sulla Calà diventano `capitolo().ambienti`, `ambiente_pioggia` (bg -> file) e `ambiente_arrivo` (file -> suono). Il codice audio resta comune.
  - `game/luce.rpy`: il tonfo di Druso diventa generico, `for tag, (mov, ritardo) in capitolo().entrate.items()`. `DRUSO_RITARDO` passa nella registrazione di Malandrini: `entrate={"druso": ("tonfo", 0.3)}`.
  - `game/feedback.rpy`: `FEEDBACK_AFFINITA` diventa `capitolo().affinita`. Le righe `image side ...` vanno in `game/capitoli/malandrini/ritratti.rpy`.
  - `game/capitoli/malandrini/capitolo.rpy`: compila `regia=regia_tabelle`, `ambienti`, `ambiente_pioggia`, `ambiente_arrivo`, `entrate` e `affinita` con i valori di oggi.
- Test: `tests/test_regia.py` (aggiorna le chiamate passando `regia_tabelle`), `tests/test_audio.py`.

**Interfaces:**
- Consumes: `capitolo()` (Task 3).
- Produces: `capitolo_regia()`, e le firme `rgl.*` sopra.

- [ ] **Step 1: Write the failing tests.** In `tests/test_regia.py`:
  - `effetti_per("esterno_neve", None, None, False, False, None) == ()`;
  - `tinta_per("vicoli_zefiro", "sera", None) is None`;
  - i casi esistenti passano `regia_tabelle` e danno gli stessi risultati di oggi.

  Nuovo controllo "codice comune pulito": nessuno dei file comuni contiene i nomi elencati. I file sono `game/regia_logic.py`, `effetti.rpy`, `luce.rpy`, `audio.rpy`, `feedback.rpy`, `regia.rpy`, `screens.rpy` e `capitoli.rpy`. I nomi sono `aede`, `caino`, `druso`, `icaro`, `ofelia`, `vicoli_zefiro`, `cala_notte` e `esterno_neve`. Le parole si cercano intere e senza distinguere maiuscole; i commenti sono esclusi. `screens.rpy` entra nel controllo in Task 6.
- [ ] **Step 2: Run.** I test falliscono.
- [ ] **Step 3: Implement** come descritto in Files.
- [ ] **Step 4: Verifica.** Test e lint puliti. Prova manuale con `Avvia Date the Dignitas.bat`: neve su `esterno_neve`, tinta della sera nei vicoli, ambiente audio e tonfo di Druso uguali a prima.
- [ ] **Step 5: Commit (solo su richiesta).** Messaggio `refactor: regia, audio, luce e feedback leggono le tabelle del capitolo`.

### Task 5: Spostare i file `.rpy` di Malandrini

**Files (`git mv`):**
- `game/routes/` -> `game/capitoli/malandrini/routes/`
- In `game/capitoli/malandrini/`: `calendario.rpy`, `borsa.rpy`, `economia.rpy`, `economia_extra.rpy`, `cronache.rpy`, `conseguenze.rpy`, `minigiochi.rpy`, `nuova_partita.rpy`.
- `game/finali_galleria.rpy` si divide:
  - in `game/capitoli/malandrini/finali.rpy` vanno la lista `FINALI` e `GALLERIA_ROUTE`;
  - in `game/finali_galleria.rpy` (comune) restano i `default persistent.*`, `sblocca_finale` e la screen.
- `game/menu_cast.rpy` si divide:
  - `MM_CAST` passa nella registrazione (`cast_menu=`);
  - in `game/menu_cast.rpy` resta il motore del carosello, che legge `mm_cast()`. `mm_cast()` è definita lì e restituisce `rcap.capitolo_menu(persistent.ultimo_capitolo).cast_menu or []`. `MM_N` diventa `len(mm_cast())`.
- Delete: tutti i `game/**/*.rpyc` e `game/cache/`. Ren'Py li rigenera.
- Modify: `tests/test_ordine_init.py` (vedi Step 1), i percorsi in tutti i test (`MAL` di Task 2), `esporta_dialoghi.py` (percorsi `capitoli/malandrini/routes/...`).

**Interfaces:**
- Consumes: `tests/percorsi.MAL` (Task 2), `cast_menu`/`finali` della registrazione (Task 3).
- Produces: `FINALI` resta il nome della lista di Malandrini, e la registrazione la passa come `finali=FINALI, gruppi_finali=GALLERIA_ROUTE`. Per questo la registrazione resta a `init 10`.

- [ ] **Step 1: Test dell'ordine di init.** `BASELINE` resta identica. `_file_rpy()` cammina già tutto `game/`, quindi l'ordine relativo di Malandrini resta uguale. Aggiungi un secondo controllo: nessun file sotto `game/capitoli/` ha blocchi `init python` a priorità 0 che usano nomi definiti a priorità 0 in file comuni che ora si ordinano dopo (`effetti`, `feedback`, `finali_galleria`, `gui`, `luce`, `menu_cast`, `regia`, `screens`). Il controllo è pratico: lint pulito più l'avvio del gioco fino al primo giorno. Ogni `NameError` all'avvio si corregge con una priorità esplicita (`init 1 python`), non spostando codice comune.
- [ ] **Step 2: Sposta i file**, cancella `.rpyc` e `cache`, aggiorna i percorsi nei test.
- [ ] **Step 3: Verifica.** Lint e test puliti. `py -3 -I -X utf8 esporta_dialoghi.py` produce copioni identici a quelli di prima: `git diff --stat dialoghi/` è vuoto. Fa eccezione la cartella di uscita, che cambia in Task 11.
- [ ] **Step 4: Commit (solo su richiesta).** Messaggio `refactor: Malandrini in game/capitoli/malandrini`.

### Task 6: Funzioni del capitolo (HUD, menu di gioco, callback)

**Files:**
- Modify:
  - `game/capitoli/malandrini/borsa.rpy`: `borsa_hud`, `borsa_monete` e `_bo_controlla` funzionano solo se `capitolo_ha("borsa")`.
  - `game/screens.rpy`:
    - il pulsante rapido `"borsa"` compare solo con `capitolo_ha("borsa")`;
    - in `navigation`, Diario, Cronache, Trama e Borsa compaiono solo con `capitolo_ha("diario"|"cronache"|"trama"|"borsa")`;
    - in `file_slots`, il ritratto usa `rcap.ottieni(FileJson(slot, "capitolo") or "malandrini").ritratto`;
    - entra nel controllo "codice comune pulito" di Task 4.
  - `game/capitoli/malandrini/calendario.rpy`: `cal_json_route` scrive anche `d["capitolo"] = store.capitolo_corrente`. La registrazione aggiunge `ritratto=cal_portrait`.
  - Ogni altro `config.start_interact_callbacks`, `overlay_screens` o `after_load_callbacks` dentro `game/capitoli/malandrini/` controlla `capitolo_ha(...)` oppure `store.capitolo_corrente == "malandrini"`.
- Test: `tests/test_capitoli.py`.

- [ ] **Step 1: Test** (lettura dei sorgenti):
  - ogni `config.overlay_screens.append` e `config.start_interact_callbacks.append` sotto `game/capitoli/malandrini/` si riferisce a una funzione o screen che contiene `capitolo_ha(` o `capitolo_corrente`;
  - `screens.rpy` contiene `capitolo_ha("borsa")`.
- [ ] **Step 2: Run.** Il test fallisce.
- [ ] **Step 3: Implement.**
- [ ] **Step 4: Verifica (Review Focus 1).** Test e lint puliti. Prova manuale:
  - nuova partita fino a Luna I;
  - salva su un menu, torna al menu principale, ricarica: HUD borsa, calendario e pulsanti Diario/Cronache/Trama/Borsa presenti;
  - fai rollback di qualche riga: niente sparisce.
- [ ] **Step 5: Commit (solo su richiesta).** Messaggio `feat: HUD e menu di gioco solo per i capitoli che li usano`.

### Task 7: Scelta del capitolo e menu principale

**Files:**
- Modify:
  - `game/capitoli.rpy`: screen `scegli_capitolo()` (`tag menu`, dentro `use game_menu(_("Capitoli"))`). Una carta per ogni `rcap.elenco()` con:
    - copertina, oppure il fondo del cast se manca;
    - `"CAPITOLO " + numero romano`, titolo, sottotitolo;
    - `"Finali: v / t"` da `rcap.finali_contati`.

    L'azione della carta è `Start(c.ingresso)`. In fondo, una carta "Prossimamente" non cliccabile. Lo stile è quello del menu attuale (pergamena, oro, `gui.accent_color`). Nella variante `small` le carte vanno in colonna e sono alte almeno 120 px.
  - `game/screens.rpy`, `navigation`: `textbutton _("Start") action ShowMenu("scegli_capitolo")`.
  - `game/script.rpy`, `label start`:
    - con un solo capitolo registrato: `jump expression rcap.elenco()[0].ingresso`;
    - altrimenti: `call screen scegli_capitolo`, poi `jump expression _return`. In quel caso la screen restituisce l'ingresso con `Return(c.ingresso)` quando non è al menu principale.
  - `game/menu_cast.rpy`, `mm_fondo()`: usa `rcap.capitolo_di_finale(persistent.ultimo_finale)` e passa le sue `regia`/`finali` a `rgl.fondo_menu`. Con `cast_menu` vuoto il carosello non si disegna.
- Test: `tests/test_capitoli.py`.

- [ ] **Step 1: Test** (lettura dei sorgenti):
  - `navigation` contiene `ShowMenu("scegli_capitolo")`;
  - `screen scegli_capitolo` esiste;
  - `label start` non contiene più `jump capitolo1`.
- [ ] **Step 2: Run.** Il test fallisce.
- [ ] **Step 3: Implement.**
- [ ] **Step 4: Verifica (Review Focus 2 e 5).** Lint pulito, poi prove manuali:
  - Start -> scegli capitolo -> Malandrini parte da "CAPITOLO I".
  - Imposta per un avvio `persistent.ultimo_capitolo = "inesistente"` dalla console (shift+O): il menu mostra il cast di Malandrini.
  - Avvia con `config.variants = ["small", "touch"]` temporaneo in `options.rpy` e controlla la leggibilità delle carte. Poi togli la riga.
- [ ] **Step 5: Commit (solo su richiesta).** Messaggio `feat: schermata di scelta del capitolo`.

### Task 8: Galleria dei finali per capitolo

**Files:**
- Modify: `game/finali_galleria.rpy`, screen `galleria_finali`.
  - Per ogni capitolo in `rcap.elenco()` che ha finali: titolo del capitolo e contatore `rcap.finali_contati`, poi i gruppi `c.gruppi_finali` come oggi.
  - In cima il totale, che somma solo i finali dei capitoli registrati.
- Test: `tests/test_capitoli.py`, più il controllo esistente sul numero di finali (28) in `tests/test_routing.py`/`test_calendario.py`.

- [ ] **Step 1: Test.** La screen non usa più `FINALI` direttamente (cerca `rcap.elenco()` e `finali_contati` nel suo corpo).
- [ ] **Step 2: Run.** Il test fallisce.
- [ ] **Step 3: Implement.**
- [ ] **Step 4: Verifica (Review Focus 3).** Lint pulito. Prova manuale: dalla console `persistent.finali_visti.add("zz_estraneo")`; la galleria mostra lo stesso conteggio di prima.
- [ ] **Step 5: Commit (solo su richiesta).** Messaggio `feat: galleria dei finali divisa per capitolo`.

### Task 9: Asset per capitolo

**Files:**
- Move (`git mv`):
  - `game/images/*.webp` -> `game/images/malandrini/`, tranne `bg nero.webp` -> `game/images/comune/`;
  - in `game/gui/malandrini/`, i file usati solo da codice di Malandrini: `cast_*`, `portrait_*`, `luna_*`, `scudo*`, `borsa_pillola.png`, `ceralacca*.png`, `cartello_data.png`, `clessidra.png`;
  - in `game/audio/malandrini/`: `amb_*.ogg`, `campana.ogg`, `moneta.ogg`.
  - Regola: un file con anche un solo riferimento nel codice comune resta dov'è. Verifica con `grep -rn "<nome>" game --include=*.rpy`.
- Modify:
  - ogni percorso esplicito `"gui/..."` e `"audio/..."` dei file spostati (codice di Malandrini e registrazione);
  - `make_gui.py`, `make_audio.py`, `make_bg.py`, `make_placeholders.py`: cartelle di uscita per quei file;
  - `ASSETS.md`: nuova struttura e regola dei nomi unici.
- Test: `tests/test_capitoli.py`.

- [ ] **Step 1: Test.**
  - Ogni stringa `"gui/..."`/`"audio/..."` letterale nei `.rpy` punta a un file che esiste (i pattern con `%s`/`[...]` si controllano per i casi noti: `portrait_<char>`, `cast_<char>`, `luna_1..6`).
  - Nessun nome di immagine è definito due volte sotto `game/images/`: stesso nome file in due sottocartelle = FAIL.
- [ ] **Step 2: Run.** Il test passa già sul primo controllo e fallisce dopo uno spostamento parziale: serve da guardia.
- [ ] **Step 3: Sposta e aggiorna.** `py -3 -I -X utf8 make_gui.py` riscrive i file nelle nuove cartelle senza ricreare quelli vecchi in `game/gui/`.
- [ ] **Step 4: Verifica.** Test e lint puliti (il lint segnala le immagini mancanti). Prova manuale: menu principale con il cast, il pianificatore con ritratti e lune, la borsa con le monete e il suono, l'ambiente sulla Calà con la campana.
- [ ] **Step 5: Commit (solo su richiesta).** Messaggio `refactor: asset di Malandrini in sottocartelle del capitolo`.

### Task 10: Modello di capitolo nuovo

**Files:**
- Create in `modelli/capitolo/`:
  - `capitolo.rpy`: `init 10 python: rcap.registra(id="__ID__", numero=__NUMERO__, titolo="__TITOLO__", ingresso="__ID___inizio", finali=__ID___FINALI, gruppi_finali=["__TITOLO__"])`.
  - `inizio.rpy`: `label __ID___inizio:` con `$ entra_capitolo("__ID__")`, cartello centrato, scelta genere (`set_gender`), nome (`sanitize_name`), una riga e un finale `$ sblocca_finale("__ID___fine")`, poi `return`.
  - `finali.rpy`: `__ID___FINALI = [("__ID___fine", "FINE", "__TITOLO__", "Arriva in fondo.")]`.
  - `variabili.rpy`: esempio di store con nome (`default __ID__.affinita = 0`).
  - `LEGGIMI.md`: i passi della spec, più la regola dei prefissi e le cartelle `game/images|gui|audio/__ID__/`.
- Create: `nuovo_capitolo.py` alla radice. Uso: `py -3 -I -X utf8 nuovo_capitolo.py <id> <numero> "<titolo>"`. Copia `modelli/capitolo/` in `game/capitoli/<id>/` sostituendo i segnaposto, e crea le cartelle vuote degli asset. Si ferma con errore se `<id>` esiste già o non rispetta `^[a-z][a-z0-9_]*$`.
- Test: `tests/test_capitoli.py`.

- [ ] **Step 1: Test.** `nuovo_capitolo.crea(id, numero, titolo, destinazione)` su una cartella temporanea (`tempfile.mkdtemp()`):
  - nessun file creato contiene ancora `__ID__`, `__NUMERO__` o `__TITOLO__`;
  - `capitolo.rpy` contiene `id="prova"`;
  - chiamarla di nuovo solleva `FileExistsError`;
  - `crea("Prova!", ...)` solleva `ValueError`.
- [ ] **Step 2: Run.** Il test fallisce.
- [ ] **Step 3: Implement.** La funzione `crea(cid: str, numero: int, titolo: str, radice_game: str) -> str` (percorso creato) va in `nuovo_capitolo.py`; il `main` legge `sys.argv`.
- [ ] **Step 4: Verifica (Review Focus 4).**
  - `py -3 -I -X utf8 nuovo_capitolo.py prova 2 "Prova"`, poi lint pulito.
  - Prova manuale: lo Start mostra due carte. "Prova" parte, e non ci sono HUD borsa, calendario, effetti, ambiente o popup affinità. Il finale si sblocca e compare nella galleria sotto "Prova".
  - Rimuovi `game/capitoli/prova/` e le cartelle asset create. Al menu il cast è di Malandrini (`ultimo_capitolo` punta a "prova", ripiego di Review Focus 2).
  - Lint e test puliti.
- [ ] **Step 5: Commit (solo su richiesta).** Messaggio `feat: modello e script per un capitolo nuovo`.

### Task 11: Strumenti, documentazione, verifica finale

**Files:**
- Modify:
  - `esporta_dialoghi.py`: uscita in `dialoghi/malandrini/` (git mv dei `.txt` attuali), e struttura `CAPITOLI = {"malandrini": {...gruppi di oggi...}}` così un capitolo nuovo si aggiunge con una voce.
  - `.claude/skills/character-sim/SKILL.md`, `.claude/skills/writing-vn-scenes/SKILL.md`, `.claude/skills/game-brainstorm/SKILL.md`: percorsi nuovi (`game/capitoli/malandrini/...`, `game/images/malandrini/`), una riga "queste regole valgono per Malandrini", e il rimando a `modelli/capitolo/LEGGIMI.md` per un capitolo nuovo.
  - `README.md`: sezione "Aggiungere un capitolo".
  - `android.json`: `numeric_version` +1. Package e chiave restano invariati.

- [ ] **Step 1: Rigenera i copioni.** `py -3 -I -X utf8 esporta_dialoghi.py`. Il contenuto è identico a prima e cambia solo la cartella: `git diff -M --stat` mostra solo rinomine.
- [ ] **Step 2: Verifica finale.**
  - Lint e test puliti.
  - Partita di Malandrini dal menu fino alla scelta del cuore (con skip), con salvataggio e caricamento.
  - Galleria e menu come in Task 7-8.
  - Build Android: `build_apk.ps1` termina senza errori.
- [ ] **Step 3: Commit (solo su richiesta).** Messaggio `docs: strumenti e skill per i capitoli`.
