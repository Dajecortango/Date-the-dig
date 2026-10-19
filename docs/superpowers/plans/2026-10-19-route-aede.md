# Route Aede (Date the Dig) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Demo Ren'Py giocabile della visual novel "Date the Dig": route completa di Aede (prologo, 6 capitoli, climax, 3 finali) in italiano.

**Architecture:** Progetto Ren'Py standard. `script.rpy` tiene solo setup e aggancio route; tutta la route Aede vive in `game/routes/aede_*.rpy` (un file per blocco narrativo). Variabili con prefisso `aede_`/`flag_` per convivere con route future. Asset placeholder generati via script Python (PIL), sostituibili dal committente.

**Tech Stack:** Ren'Py SDK 8.3.7 (scaricato in `tools/`, gitignored), Python/PIL per placeholder, git.

**Spec:** `docs/superpowers/specs/2026-10-19-route-aede-design.md`

## Global Constraints

- Lingua di gioco: italiano. Nomi lore esatti: Yr, Famiglia Dignitas, Zefiro, Rocca Tempesta, Lenora Dignitas, Glauco Severo, Briseide Ippodamia, Draken il Mutevole, Yr-Drazul, Lo Svelo, Athlion, Fiaccolata della Calà, il Margine, Drakengrad.
- Protagonista: nome scelto dal giocatore (default "Elio"), maschile, nessuno sprite, POV prima persona.
- Cast parlante massimo 5–6 personaggi.
- VN pura: solo say/menu/sprite/sfondi. Nessuna stat visibile.
- Niente contenuto sessuale esplicito; violenza dark fantasy ammessa.
- Good end NON raggiungibile scegliendo sempre l'opzione più "gentile": le opzioni che rispettano l'orgoglio di Aede valgono più di quelle sdolcinate.
- Durata run: 30–60 min lettura (≈ 8.000–15.000 parole di testo di gioco).
- Ogni capitolo: 2–4 menu, di cui ≥1 tocca `aede_affinity` o un flag.

## Review Focus

- Nome giocatore vuoto o solo spazi all'input → deve diventare "Elio" (test in Task 2).
- Nome giocatore con caratteri speciali/parentesi graffe (es. `{b}`) → niente crash di interpolazione Ren'Py (test in Task 2).
- Percorso bad end raggiungibile davvero: run con affinità minima termina in bad end, non in neutral (test in Task 6).
- Good end bloccato senza i flag chiave anche con affinità alta (test in Task 6).
- Rollback/skip Ren'Py attraverso i menu non corrompe `aede_affinity` (usare solo `$ aede_affinity += n` dentro i menu, mai logica fuori label; verifica lint + playthrough in Task 7).

---

### Task 1: Setup progetto e SDK

**Files:**
- Create: `.gitignore`, `tools/` (SDK scaricato, gitignored), `game/script.rpy`, `game/options.rpy`, `game/gui.rpy`, `game/screens.rpy` (da template SDK), `lint.ps1`
- Create: `README.md` (una riga: come lanciare)

**Interfaces:**
- Produces: comando lint funzionante: `powershell -File lint.ps1` → "Lint is not finding any problems"; struttura `game/` standard.

- [ ] **Step 1: git init + .gitignore**

```
tools/
game/saves/
game/cache/
*.rpyc
*.bak
```

Run: `git init` nella cartella progetto; commit iniziale con design doc e piano.

- [ ] **Step 2: Scarica Ren'Py SDK 8.3.7**

Run: scaricare `https://www.renpy.org/dl/8.3.7/renpy-8.3.7-sdk.zip` in `tools/`, estrarre in `tools/renpy-8.3.7-sdk/`.
Expected: esiste `tools/renpy-8.3.7-sdk/renpy.exe` (o `renpy.sh`). Download ~80MB: usare timeout lungo.

- [ ] **Step 3: Crea skeleton progetto**

Il gioco vive DENTRO questa cartella: creare `game/` con `script.rpy`, `options.rpy`, `gui.rpy`, `screens.rpy` copiati dal template del SDK (`tools/renpy-8.3.7-sdk/templates/` o progetto generato via `renpy.exe . create`). In `options.rpy`: `config.name = "Date the Dig"`, `build.name = "DateTheDig"`, `config.version = "0.1"`.

- [ ] **Step 4: lint.ps1**

```powershell
& "$PSScriptRoot\tools\renpy-8.3.7-sdk\renpy.exe" "$PSScriptRoot" lint
```

Run: `powershell -File lint.ps1`
Expected: output termina con "Lint is not finding any problems."

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "feat: skeleton progetto Ren'Py Date the Dig"
```

### Task 2: Framework route — personaggi, variabili, input nome

**Files:**
- Create: `game/routes/aede_core.rpy`
- Modify: `game/script.rpy`

**Interfaces:**
- Produces: Characters `aede` ("Aede", colore #c0392b), `glauco` ("Glauco Severo", #6b6b6b), `briseide` ("Briseide Ippodamia", #b8860b), `pc` (dinamico `[player_name]`); variabili `default aede_affinity = 0`, `default flag_segreto_svelo = False`, `default flag_accetta_lavoro = False`, `default flag_giuramento = False`; label `prologo` (stub); funzione `sanitize_name(raw)` in python early → str.
- Consumes: skeleton Task 1.

- [ ] **Step 1: Definisci personaggi e default in `aede_core.rpy`**

`define` per i 4 Character, `default` per le variabili sopra. Due comprimari fratelli di Ceppo del protagonista: definire qui `define vanna = Character("Vanna")` e `define corrado = Character("Corrado")` (nomi inventati, non-Autarchi, coerenti col lore).

- [ ] **Step 2: Input nome con sanificazione**

In `script.rpy`, `label start`: `$ player_name = renpy.input("Come ti chiama la Famiglia? (Primo Nome)", length=20)` poi `$ player_name = sanitize_name(player_name)`. `sanitize_name`: strip; se vuoto → "Elio"; rimuovere `{`, `}`, `[`, `]`. Poi `jump prologo`.

- [ ] **Step 3: Test automatico sanificazione**

Creare `game/routes/aede_core.rpy` con la funzione in `init python`; test via lint + script Python standalone `tests/test_sanitize.py` che importa la stessa logica (funzione pura duplicata in `game/python/namesan.py` NON serve: tenere la funzione in un blocco `init python` e testarla con un piccolo harness: copiare la funzione in `tests/test_sanitize.py` è vietato — invece eseguire: `tools/renpy-8.3.7-sdk/renpy.exe . lint` + verifica manuale in Task 7). Assert minimi da verificare a mano in gioco: "" → Elio; "  " → Elio; "{b}Ciao" → bCiao.

- [ ] **Step 4: Lint**

Run: `powershell -File lint.ps1` → nessun problema.

- [ ] **Step 5: Commit**

```bash
git commit -am "feat: framework route Aede (personaggi, variabili, input nome)"
```

### Task 3: Asset placeholder e GUI

**Files:**
- Create: `game/images/` (sprite + sfondi placeholder), `make_placeholders.py` (root, eseguito una volta)
- Modify: `game/gui.rpy` (palette)

**Interfaces:**
- Produces: immagini nominate che TUTTE le scene useranno:
  sprite: `aede neutra`, `aede irritata`, `aede sorpresa`, `aede imbarazzata`, `aede sorriso`, `aede furia`, `glauco neutro`, `glauco minaccioso`, `briseide neutra` (file `game/images/aede neutra.png` ecc.);
  sfondi: `bg sala_svelo`, `bg arena_athlion`, `bg vicoli_zefiro`, `bg cala_notte`, `bg studio_glauco`, `bg corridoio_ceppo`, `bg esterno_neve`, `bg nero`.
- Consumes: niente.

- [ ] **Step 1: Script placeholder**

`make_placeholders.py` con PIL: sprite 700×1400 PNG (silhouette colorata + nome espressione scritto sopra; Aede rosso #c0392b, Glauco grigio, Briseide oro), sfondi 1920×1080 (colore pieno + etichetta). Base sprite Aede: può incollare `aede_black.jpg` ridimensionata se presente in `Downloads`, altrimenti silhouette.

- [ ] **Step 2: Esegui e verifica**

Run: `python make_placeholders.py`
Expected: 17 PNG in `game/images/`, nomi esatti come sopra.

- [ ] **Step 3: Palette GUI**

In `gui.rpy`: `gui.accent_color = '#d4af37'` (oro), `gui.main_menu_background`/`game_menu_background` scuri (#0d0d0d), hover oro, testo #f0e6d2. Titolo menu: "Date the Dig".

- [ ] **Step 4: Lint**

Run: `powershell -File lint.ps1` → nessun problema (lint verifica anche riferimenti immagine nelle scene già scritte).

- [ ] **Step 5: Commit**

```bash
git commit -am "feat: placeholder sprite/sfondi e palette GUI nero-oro"
```

### Task 4: Prologo + Capitoli 1–3

**Files:**
- Create: `game/routes/aede_atto1.rpy` (label `prologo`, `cap1`, `cap2`, `cap3`)
- Modify: `game/routes/aede_core.rpy` (rimuovere stub `prologo`)

**Interfaces:**
- Consumes: Characters/variabili Task 2, immagini Task 3.
- Produces: label `prologo` → `cap1` → `cap2` → `cap3` → `jump cap4`. Al termine del prologo `flag_segreto_svelo` settato dalla scelta; `aede_affinity` range atteso a fine cap3: 0–6.

- [ ] **Step 1: Scrivi il prologo (~1.200 parole)**

Canovaccio vincolante (spec): Lo Svelo a Rocca Tempesta, maschere; Aede scambia il protagonista per il suo bersaglio, lama alla gola, errore scoperto. Menu finale (decide `flag_segreto_svelo`): a) "Il tuo segreto muore con me" → `flag_segreto_svelo = True`, `aede_affinity += 2`; b) scherzarci su → +1; c) minacciare di riferire a Glauco → −2. Variante scelta: bersaglio scambiato (non borseggio) — più forte per lo scontro iniziale.

- [ ] **Step 2: Capitolo 1 — L'incarico (~1.000 parole)**

Briseide presta il protagonista al Ceppo di Glauco Severo; consegna scortata da Aede nei vicoli di Zefiro. 2 menu; uno con opzione che rispetta l'orgoglio di lei (+2) vs opzione servizievole (0) vs lamentarsi (−1). Prima apparizione `glauco minaccioso` in chiusura.

- [ ] **Step 3: Capitolo 2 — Athlion (~1.000 parole)**

Menu su come sostenerla: tifo plateale (0), aiuto discreto (+2), sfidarla in gara (+2 e battuta tsundere), ignorarla (−2).

- [ ] **Step 4: Capitolo 3 — Intrigo tra Rami (~1.200 parole)**

Ricatto tra Ceppi rivali, collaborazione forzata, prima incrinatura (Aede ride o lo protegge d'istinto). 2 menu, ±2 ciascuno.

- [ ] **Step 5: Lint**

Run: `powershell -File lint.ps1` → nessun problema.

- [ ] **Step 6: Commit**

```bash
git commit -am "feat: prologo e capitoli 1-3 route Aede"
```

### Task 5: Capitoli 4–6

**Files:**
- Create: `game/routes/aede_atto2.rpy` (label `cap4`, `cap5`, `cap6`)

**Interfaces:**
- Consumes: come Task 4.
- Produces: `cap4` setta `flag_accetta_lavoro`; `cap6` setta `flag_giuramento`; `cap6` termina con `jump climax`. Range affinità fine cap6 per run "perfetta": ≥ 12.

- [ ] **Step 1: Capitolo 4 — Il lavoro di Aede (~1.200 parole)**

Il protagonista la vede uccidere su commissione. Menu morale chiave: a) orrore/condanna → −3, `flag_accetta_lavoro = False`; b) accettazione fredda → +1, True; c) domanda sincera ("Chi era per te?") → +3, True. Tono: nessuna giustificazione facile; Glauco difende la figlia "a prescindere".

- [ ] **Step 2: Capitolo 5 — Fiaccolata della Calà (~1.200 parole)**

Leggenda degli amanti; menu: percorrere la Calà mano nella mano (richiede `aede_affinity >= 8` per sbloccarsi, altrimenti lei rifiuta con battuta) / camminare accanto senza toccarla (+1) / restare indietro (−2). Quasi-confessione interrotta (da Corrado o Vanna).

- [ ] **Step 3: Capitolo 6 — Il giuramento (~1.200 parole)**

Aede sfiora il tabù del passato. Menu decisivo: a) fermarla rispettando il giuramento → `flag_giuramento = True`, +2 (controintuitivo: la scelta "romantica" di ascoltarla è quella sbagliata); b) ascoltarla → False, +1 e Glauco osserva dall'ombra; c) rivelare qualcosa di sé → False, −1. Chiusura: convocazione dal Ceppo di Glauco.

- [ ] **Step 4: Lint + commit**

Run: `powershell -File lint.ps1` → ok.

```bash
git commit -am "feat: capitoli 4-6 route Aede"
```

### Task 6: Climax e finali

**Files:**
- Create: `game/routes/aede_finali.rpy` (label `climax`, `good_end`, `neutral_end`, `bad_end_aede`, `bad_end_glauco`)

**Interfaces:**
- Consumes: variabili/flag; immagini.
- Produces: fine del gioco (`return` dopo ogni finale). Routing esatto:
  - `good_end`: `aede_affinity >= 12 and flag_giuramento and flag_accetta_lavoro`
  - `bad_end_glauco`: `flag_segreto_svelo == False and aede_affinity < 6`
  - `bad_end_aede`: `aede_affinity < 6` (con segreto mantenuto)
  - `neutral_end`: tutto il resto.

- [ ] **Step 1: Climax (~800 parole)**

Glauco ordina ad Aede l'eliminazione del protagonista (bersaglio: lui stesso — più diretto per la demo). Scena nello studio di Glauco poi esterno neve. Un ultimo menu cosmetico (come affronti la lama: parole / silenzio / mano tesa) che cambia solo testo, non routing.

- [ ] **Step 2: Routing finali**

In coda a `climax`, `if/elif/else` ESATTAMENTE nell'ordine: good → bad_glauco → bad_aede → neutral (ordine sopra; good controllato per primo).

- [ ] **Step 3: Quattro finali (~400 parole ciascuno)**

Good: Aede disobbedisce, terza via davanti a Glauco; chiusura sulla Calà mano nella mano. Neutral: inganno che lo risparmia, amicizia malinconica. Bad Aede: esecuzione fredda, citazione del Margine. Bad Glauco: interviene il padre, citazione Drakengrad. Dopo ogni bad end: schermata `bg nero` con testo "FINE — Il Nord non perdona" e `return`.

- [ ] **Step 4: Verifica routing con run forzate**

Run: lancio gioco con console dev (`config.developer = True` già nel template), 4 run usando skip + console per forzare variabili (`aede_affinity = 0` ecc.) e verificare i 4 finali raggiunti. In più: run "sempre gentile/sdolcinata" deve dare neutral, NON good.
Expected: 5 esiti corretti.

- [ ] **Step 5: Lint + commit**

```bash
git commit -am "feat: climax e quattro finali route Aede"
```

### Task 7: Rifinitura e verifica completa

**Files:**
- Modify: eventuali fix emersi; `README.md` (istruzioni lancio complete + specifica tecnica asset per il committente: PNG con trasparenza, sprite 700×1400, sfondi 1920×1080, elenco esatto dei 17 nomi file da Task 3)

**Interfaces:**
- Consumes: tutto.

- [ ] **Step 1: Playthrough completo manuale**

Run: `tools/renpy-8.3.7-sdk/renpy.exe .` — una run good-end reale senza console, testando: input nome vuoto → "Elio"; nome con `{b}` → nessun crash; rollback attraverso 2 menu → affinità coerente (ripetere scelta → stesso valore).
Expected: nessuna eccezione Ren'Py, finale good raggiunto con le scelte giuste.

- [ ] **Step 2: Lint finale**

Run: `powershell -File lint.ps1` → "Lint is not finding any problems." + word count del lint ≥ 8.000 parole dialogo.

- [ ] **Step 3: Commit finale**

```bash
git commit -am "feat: demo route Aede completa e verificata"
```
