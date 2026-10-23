# Capitoli scalabili — design

Data: 2026-10-23. Stato: proposta, da approvare.

## Intento

Date the Dignitas diventa una raccolta di **capitoli**. Ogni capitolo è
un'avventura indipendente con cast, route, finali, sfondi, sprite e audio
propri. Il primo capitolo è **Malandrini** (tutto il gioco attuale). Seguiranno
altri capitoli in luoghi diversi, con personaggi diversi e soprattutto asset
nuovi. Il luogo e le meccaniche del capitolo 2 non sono ancora decisi.

Obiettivo: aggiungere un capitolo deve voler dire **creare una cartella e
registrarlo in un punto solo**, senza toccare i file di Malandrini né quelli
di altri capitoli.

## Decisioni dell'utente

- Ogni capitolo è un'altra avventura: niente protagonista, scelte o
  affinità portate da un capitolo all'altro.
- Il cast di ogni capitolo è diverso. Il luogo forse è diverso (non deciso).
- Tutti i capitoli sono liberi da subito: nessuno sblocco in sequenza.
- Il gioco è già in beta tra amici (Android), ma **la compatibilità dei
  salvataggi non serve**: per la nuova versione gli amici reinstallano il
  gioco da zero (salvataggi e finali sbloccati si perdono, accettato).

## Obiettivi

1. Struttura delle cartelle per capitolo (codice, immagini, audio, GUI del
   capitolo).
2. Registro dei capitoli: un solo punto dove un capitolo si dichiara (id,
   titolo, label d'ingresso, copertina, funzioni che usa).
3. Menu principale: "Start" apre la scelta del capitolo. Con un solo capitolo
   registrato la schermata c'è comunque (mostra Malandrini e, opzionale, uno
   slot "Prossimamente").
4. Le parti generiche restano comuni: box del dialogo, preferenze,
   accessibilità, regia (`regia.rpy`), effetti, luce, feedback affinità,
   storia, salvataggi.
5. Le parti di Malandrini diventano del capitolo: calendario, borsa ed
   economia, cronache/diario/trama, conseguenze, minigiochi, galleria dei
   finali (voci), cast del menu.
6. Gli HUD e i pulsanti specifici (borsa, calendario, Diario, Cronache, Trama,
   Borsa nel menu di gioco) appaiono solo quando il capitolo in corso li usa.
7. Galleria dei finali divisa per capitolo (schede o sezioni).
8. Modello per un capitolo nuovo (scheletro copiabile + istruzioni), e skill
   di progetto aggiornate ai nuovi percorsi.

## Non-obiettivi

- Nessun contenuto del capitolo 2: niente scene, personaggi o asset nuovi.
- Nessuna riscrittura del motore del calendario per renderlo generico "a
  parametri" adesso. Resta di Malandrini; se il capitolo 2 lo vorrà, si
  estrae allora (vedi "Lasciato al builder").
- Nessun cambio di testo, bilanciamento o comportamento di gioco in
  Malandrini.

## Anti-obiettivi (fallimento anche se "funziona")

- Un giocatore di Malandrini che nota differenze nel gioco (a parte la
  schermata di scelta del capitolo).
- Un capitolo nuovo che, per esistere, richiede modifiche dentro i file di
  Malandrini.
- Riferimenti ai personaggi di Malandrini (aede, caino…) in codice comune.

## Vincoli tecnici

### Salvataggi

Niente compatibilità con i salvataggi della beta (reinstallazione). Quindi i
file `.rpy` si spostano liberamente con `git mv`; i `.rpyc` vecchi si
cancellano e si ricompila.

Restano comunque queste regole, per non rompere il gioco:

- **Niente rinomine di label o variabili di Malandrini**: non serve, e
  label e variabili sono citati in molti file e nei test (`capitolo1`,
  `cal_loop`, `aede_affinity`, `route_attiva`, `eventi_visti`…). Restano
  nello store globale.
- Gli stati `NoRollback` già presenti (`_bo`, `_fb`, `_fx_cache`…) restano
  fuori dai salvataggi solo perché sono assegnati una volta in init e mai
  riassegnati: mantenere questa regola.
- I moduli Python puri (`calendario_logic.py`, `routing_logic.py`,
  `relazioni_logic.py`, `economia_logic.py`, `conseguenze_logic.py`,
  `minigiochi_logic.py`) sono di Malandrini: si possono spostare in un
  package del capitolo, aggiornando import e `sys.path` dei test.
- Nuova variabile `default capitolo_corrente = "malandrini"`.
- I `config.after_load_callbacks` di Malandrini (es.
  `_conseguenze_migra_salvataggio`) girano solo quando
  `capitolo_corrente == "malandrini"`.
- Da qui in poi, dopo l'uscita della nuova versione, la compatibilità dei
  salvataggi torna a valere: la struttura nuova deve permettere di
  aggiungere capitoli senza spostare file di quelli esistenti.

### Persistent

- `persistent.finali_visti` resta **un solo insieme** con gli id esistenti.
  Gli id dei finali dei capitoli nuovi usano un
  prefisso del capitolo (es. `c2_...`) per non collidere.
- Gli altri `persistent` di Malandrini (`prologo_visto`, `trama_visti`,
  `fatti_storici`, `avvisi_conseguenze`, `opzioni_viste/scelte`,
  `ultimo_finale`) mantengono il nome (citati da codice e test). `opzioni_viste/scelte` sono
  per-label: comuni senza danno se i label restano unici.
- Nuovo `persistent.ultimo_capitolo` (default `"malandrini"`) per decidere
  quale cast/fondo mostra il menu principale.

### Ordine di init

`tests/test_ordine_init.py` verifica che l'ordine dei registry (`EVENTI`,
`ATTIVITA`, hook del calendario) non cambi quando i file vengono spostati:
Ren'Py esegue gli `init` a pari priorità in ordine di percorso. Lo
spostamento dei file cambia anche la posizione di `calendario.rpy`,
`conseguenze.rpy`, `economia*.rpy` ecc. rispetto ai file comuni
(`capitoli/...` si ordina tra `calendario` ed `effetti`). Prima di spostare:
elencare le dipendenze init a priorità 0 tra file (chi usa nomi definiti da
chi), dare priorità esplicite dove serve, ed estendere
`test_ordine_init.py` oltre a `EVENTI`/`ATTIVITA`/hook. Il test va aggiornato
al nuovo percorso e deve passare.

### Immagini e audio

- Ren'Py ricava il nome di un'immagine dal nome del file, ignorando la
  cartella: `game/images/malandrini/aede neutra.webp` resta `aede neutra`.
  Spostare le immagini nelle sottocartelle è quindi sicuro.
- Conseguenza: **i nomi delle immagini devono essere unici in tutto il
  gioco**. Immagini comuni (`bg nero`) vanno in `game/images/comune/`. Un
  capitolo nuovo non deve riusare nomi di Malandrini.
- I percorsi espliciti (`"gui/cast_aede.webp"`, `"audio/amb_cala.ogg"`,
  `gui/fx_*.png`, `gui/luna_*.png`, `gui/portrait_*.png`…) invece cambiano
  se i file si spostano: aggiornare ogni riferimento, e gli script che li
  generano (`make_gui.py`, `make_audio.py`, `make_bg.py`,
  `make_placeholders.py`).

### Varianti mobile, Android, test

- La build Android (`build_apk.ps1`, `make_android.py`) deve continuare a
  funzionare con i nuovi percorsi. Stesso package
  (`com.dajecortango.datethedignitas`) e stessa chiave (`android.keystore`),
  `numeric_version` incrementata; gli amici reinstallano.
- Tutti i test in `tests/` passano; `lint` pulito.
- `esporta_dialoghi.py` aggiornato: copioni divisi per capitolo
  (`dialoghi/malandrini/...`).

## Struttura proposta

```
game/
  script.rpy                 # label start -> scelta capitolo
  capitoli.rpy               # registro + API (vedi sotto)
  screens.rpy, gui.rpy, options.rpy, regia.rpy, effetti.rpy, luce.rpy,
  feedback.rpy, audio.rpy    # comuni (audio.rpy: canale e motore; le
                             #   tabelle sfondo->loop diventano per capitolo)
  images/comune/             # bg nero, ecc.
  gui/                       # GUI comune
  capitoli/
    malandrini/
      capitolo.rpy           # registrazione del capitolo
      calendario.rpy, borsa.rpy, economia*.rpy, cronache.rpy,
      conseguenze.rpy, minigiochi.rpy, menu_cast.rpy (parte cast),
      finali.rpy (voci FINALI), nuova_partita.rpy
      routes/                # tutti i file di game/routes/
      images/                # sprite e bg di Malandrini
      gui/                   # cast_*, portrait_*, luna_*, borsa, scudo…
      audio/                 # amb_*, campana…
modelli/capitolo/           # scheletro copiabile (fuori da game/, così
                             # Ren'Py non lo carica né lo impacchetta)
```

Nota: Ren'Py carica le immagini solo da `game/images/` (e sottocartelle) per
la definizione automatica. Se `capitoli/malandrini/images/` non viene letta
automaticamente, usare `game/images/malandrini/` oppure registrare la
cartella (`config.images_directory` è una sola stringa: in quel caso
definire le immagini con un piccolo loop in `init` sui file del capitolo).
Scelta al builder, purché i nomi immagine restino identici.

## Registro dei capitoli

Un capitolo si dichiara una volta, in `capitoli/<id>/capitolo.rpy`.
`registra_capitolo` è definita a `init -20`; la registrazione gira a
`init 10`, dopo i blocchi a priorità 0 che definiscono `MM_CAST` e `FINALI`:

```python
init 10 python:
    registra_capitolo(
        id="malandrini",
        numero=1,
        titolo="Malandrini",
        sottotitolo="Sei Lune a Rocca Tempesta",
        ingresso="capitolo1",          # label d'ingresso (esistente)
        copertina="gui/capitoli/malandrini.webp",
        funzioni={"calendario", "borsa", "cronache", "trama", "diario"},
        cast_menu=MM_CAST,             # opzionale: cast del menu principale
    )
```

API comune (in `game/capitoli.rpy`):

- `registra_capitolo(...)`: aggiunge al registro, ordinato per `numero`.
- `capitolo_corrente` (store, `default "malandrini"`).
- `capitolo_ha(funzione)`: True se il capitolo in corso usa quella funzione.
  Gli overlay (`borsa_hud`, `borsa_monete`), i callback di interazione
  (`_bo_controlla`, ambiente audio, regole effetti per sfondo) e i pulsanti
  del menu di gioco (Diario, Cronache, Trama, Borsa) si attivano solo con
  `capitolo_ha(...)`.
- Hook per capitolo: tabelle sfondo -> ambiente audio, sfondo -> effetti,
  FINALI, sfondo del menu dopo un finale. Il codice comune legge le tabelle
  del capitolo corrente invece di costanti globali.
- `label avvia_capitolo(id)`: imposta `capitolo_corrente` e
  `persistent.ultimo_capitolo`, poi `jump` all'ingresso.

## Menu principale

- "Start" apre `screen scegli_capitolo`: una carta per capitolo registrato
  (copertina, numero, titolo, sottotitolo, numero di finali visti / totali).
  Uno slot "Prossimamente" opzionale, non cliccabile.
- Il carosello del cast mostra il cast di `persistent.ultimo_capitolo`
  (oggi sempre Malandrini). Un capitolo senza `cast_menu` mostra solo il
  fondo del menu.
- "Continua" resta com'è.
- La schermata dei salvataggi mostra il capitolo del salvataggio (aggiungere
  `capitolo` al json dello slot accanto a `route`); i salvataggi vecchi
  senza campo valgono come Malandrini.

## Galleria dei finali

- `FINALI` diventa un registro per capitolo.
- La galleria mostra una sezione per capitolo (o schede se più di uno ha
  finali). Con un solo capitolo appare uguale a oggi più il titolo del
  capitolo.

## Modello per un capitolo nuovo

`modelli/capitolo/` (alla radice: `tools/` è in `.gitignore`) contiene uno scheletro minimo funzionante:
`capitolo.rpy` con la registrazione, un label d'ingresso con scelta genere e
nome, una scena di prova, `finali.rpy` con un finale, cartelle vuote per
immagini, gui e audio, e un `LEGGIMI.md` con i passi:

1. Copiare la cartella in `game/capitoli/<id>/`.
2. Scegliere un prefisso per label, variabili, immagini e id dei finali
   (unicità globale: Ren'Py ha un solo spazio dei nomi).
3. Registrare il capitolo.
4. Lint e test.

Facoltativo: uno script `nuovo_capitolo.py <id>` che copia e rinomina il
modello. Le variabili dei capitoli nuovi stanno in uno store con nome
(`default c2.affinita = ...`), così non collidono con lo store globale di
Malandrini.

## Documentazione e skill

- `character-sim`, `writing-vn-scenes`, `game-brainstorm`: aggiornare
  percorsi (`game/capitoli/malandrini/routes/...`) e chiarire che le regole
  scritte sono di Malandrini.
- `ASSETS.md`: nuova struttura delle cartelle e regola dei nomi unici.
- README: come aggiungere un capitolo.

## Verifica

- Lint pulito; tutti i test in `tests/` passano (aggiornati ai percorsi).
- Salvare e ricaricare una partita di Malandrini nella versione nuova (a
  metà calendario e su un menu): riprende nello stesso punto.
- Prova manuale: nuova partita di Malandrini dalla scelta del capitolo fino
  al primo giorno del calendario; HUD borsa e calendario presenti.
- Prova con il modello: copiare il modello come capitolo finto, avviarlo,
  verificare che borsa e calendario non appaiano, poi rimuoverlo.
- Build Android avviabile.

## Lasciato al builder

- Ordine dei passi e suddivisione in commit (consigliati piccoli e
  verificabili: prima registro e menu, poi spostamenti di file, poi asset).
- Se spostare i moduli `.py` puri in un package o lasciarli in `game/`.
- Cartella esatta delle immagini (`game/images/malandrini/` o dentro la
  cartella del capitolo) purché i nomi restino identici.
- Aspetto della schermata di scelta del capitolo, nello stile del menu
  attuale (pergamena, oro, ceralacca).
- Estrarre il calendario come motore comune: **non ora**. Se il capitolo 2
  lo vorrà, si parametrizza (registry `EVENTI`/`ATTIVITA` per capitolo,
  `CAL_AFF_VAR`, soglie) in un lavoro a parte.
