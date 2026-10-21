# Malandrini a calendario — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Trasformare il Capitolo I "Malandrini" da 5 route separate a dating sim a calendario: ~6 mesi (6 Lune), giorni in slot mattina/pomeriggio/sera, attività che decidono chi frequenti, route sbloccate da affinità e lucchetti.

**Architecture:** Motore puro Python (`game/calendario_logic.py`, importabile sia da Ren'Py sia dai test) che genera la sequenza dei momenti giocabili e seleziona gli eventi; un file Ren'Py di integrazione (`game/calendario.rpy`) con registry eventi, loop e screen di pianificazione; i label esistenti di Aede/Caino diventano eventi registrati; contenuti nuovi per Druso/Icaro in `game/routes/`.

**Tech Stack:** Ren'Py 8.3.7 (SDK in `tools/renpy-8.3.7-sdk/`), Python 3.13 (`py -3`), test in stile `tests/test_sanitize.py` (script plain, `py -3 -I`), PIL per asset placeholder.

**Spec:** `docs/superpowers/specs/2026-10-20-malandrini-calendario-design.md` (leggerla prima: lucchetti, mappatura Lune, decisioni vincolanti).

## Global Constraints

- **NIENTE `git commit`/`push`**: regola del repo (memoria utente). Il piano non ha step di commit; l'utente committa quando vuole.
- Verifica standard dopo ogni task Ren'Py: `"./tools/renpy-8.3.7-sdk/renpy.exe" . lint` → zero errori (solo statistiche).
- Testi esistenti di Aede/Caino NON si riscrivono; solo ritocchi di raccordo (rimozione jump rigidi, aggancio al loop).
- Soglie finali esistenti letteralmente invariate (`aede_affinity>=12...`, `caino_fiducia>=12...`, cap5 `aede_affinity>=8`).
- Niente statistiche visibili; affinità mai mostrata a schermo.
- Scene territorio: pool una-tantum, ±1 affinità, max ~4-6 punti extra per personaggio a semestre.
- Lingua: italiano; convenzioni di regia come `game/regia.rpy` (qdiss/vpunch/lampo, posizioni left per comprimari).
- GUI: stile Dignitas esistente; ritratti `gui/portrait_*.png`; per sprite mancanti placeholder stile Caino.
- Voci dei personaggi: Druso e Icaro fedeli a `docs/profili/druso.md` e `docs/profili/icaro.md`.

## Review Focus

1. Pool attività esaurito → la scelta resta cliccabile e dà una riga breve di variante, mai crash né scena ripetuta coi punti. (test in Task 1 + Task 3)
2. Fine Luna IV senza nessuno sopra soglia → si arriva al finale neutro di Luna VI senza crash e senza climax altrui. (test in Task 1, scena in Task 8)
3. Pari merito di affinità alla scelta del cuore → decide il giocatore con un menu, mai l'ordine di registrazione. (Task 8)
4. Protagonista uomo su Icaro → nessun evento romance raggiungibile, solo linea Bro. (test in Task 1 con cond; contenuti Task 7)
5. Route congelata/chiusa (Aede cap4 "assassinio", Caino trappola Adunanza, Icaro possessività) → i suoi inviti spariscono dal pianificatore per sempre. (test in Task 1 su `congelate`)

Limite noto, da dire all'utente a fine lavoro: i salvataggi fatti prima della ristrutturazione non sono compatibili col nuovo capitolo.

---

### Task 1: Motore calendario puro

**Files:**
- Create: `game/calendario_logic.py`
- Test: `tests/test_calendario.py`

**Interfaces:**
- Produces (usati da Task 2+):
  - `SLOTS = ("mattina", "pomeriggio", "sera")`
  - `genera_sequenza(calendario) -> list[tuple[int, int, str]]` — input `{luna: [{"giorno": int, "slots": [str, ...]}, ...]}`; output lista ordinata di `(luna, giorno, slot)`. Giorni/slot non elencati semplicemente non esistono (= skip).
  - `trova_fisso(momento, eventi, vars, visti) -> dict | None` — primo evento con `tipo=="fisso"`, `(luna,giorno,slot)` uguali al momento, `cond(vars)` vera (cond assente = vera), `id not in visti`.
  - `trova_inviti(momento, eventi, vars, visti) -> list[dict]` — eventi `tipo=="invito"` con `slot` compatibile (`None` = qualsiasi), `luna_min <= luna`, cond vera, non visti, `char not in vars.get("congelate", set())`.
  - Evento = dict con chiavi: `id`, `label`, `tipo` (`"fisso"`|`"invito"`), `char` (str|None), `luna`, `giorno`, `slot` (per fissi), `luna_min`, `slot` (per inviti), `cond` (callable(vars)->bool, opzionale).
  - `pesca_variante(pool_ids, visti) -> str | None` — primo id del pool non in visti; `None` = pool esaurito (il chiamante mostra la riga di fallback).

- [ ] **Step 1: scrivi il test fallente** `tests/test_calendario.py`, stile `test_sanitize.py` (import diretto: `sys.path.insert(0, game/)`, `import calendario_logic as cl`). Casi:

```python
CAL = {1: [{"giorno": 3, "slots": ["mattina", "sera"]}, {"giorno": 9, "slots": ["pomeriggio"]}],
       2: [{"giorno": 1, "slots": ["sera"]}]}
# genera_sequenza: [(1,3,"mattina"),(1,3,"sera"),(1,9,"pomeriggio"),(2,1,"sera")] — ordine e skip
# trova_fisso: evento (1,3,"mattina") trovato; stesso id in visti -> None; cond falsa -> None
# trova_inviti: invito luna_min=1 slot "sera" appare solo a slot sera; char in congelate -> escluso;
#   cond su soglia (lambda v: v["aede_affinity"]>=2) con 1 -> escluso, con 2 -> incluso
# pesca_variante(["a","b"], {"a"}) == "b"; tutti visti -> None
```

- [ ] **Step 2: verifica che fallisca** — Run: `py -3 -I tests/test_calendario.py` — Expected: FAIL/traceback (modulo inesistente).
- [ ] **Step 3: implementa `game/calendario_logic.py`** — solo funzioni pure, nessun import Ren'Py.
- [ ] **Step 4: verifica che passi** — Run: `py -3 -I tests/test_calendario.py` — Expected: tutti PASS, exit 0.

### Task 2: Integrazione Ren'Py: registry, loop, screen pianificazione

**Files:**
- Create: `game/calendario.rpy`
- Modify: `game/routes/chapter1.rpy` (solo l'aggancio finale: dopo il prologo comune si entra nel loop; la screen `chapter_select` resta nel file ma non più raggiunta — la rimozione è in Task 9)

**Interfaces:**
- Consumes: Task 1 (`import calendario_logic as cl` in `init python`).
- Produces:
  - Defaults: `default cal_idx = 0`, `default eventi_visti = set()`, `default congelate = set()`, `default route_attiva = None`, `default druso_affinity = 0`, `default icaro_affinity = 0`, `default inviti_fatti = set()`
  - `CAL_GIORNI` (python, in `calendario.rpy`): calendario concreto — 6 Lune, 3-4 giorni giocabili ciascuna (scelta del builder: distribuire così che le date fisse della spec cadano su giorni esistenti).
  - `EVENTI` (python list): registry globale; i task successivi vi aggiungono voci con `EVENTI.append({...})` in blocchi `init python` dei propri file.
  - `ATTIVITA` (python dict): `{slot: [(id_attivita, etichetta, char|None, pool_labels)]}` — es. `("spada", "Addestramento di spada", "aede", ["att_spada_1", ...])`.
  - label `cal_loop` — il cuore: pesca fisso → `call` e marca visto; altrimenti `call screen pianificazione` → `call` del label scelto; avanza `cal_idx`; a cambio giorno mostra la riga di data ("Luna III, nono giorno") via `centered` breve; a fine sequenza `jump cal_fine_semestre` (Task 8).
  - label `cal_attivita(att_id)` — risolve pool con `cl.pesca_variante`; pool esaurito → una riga generica ("La giornata passa come tante...").
  - screen `pianificazione(momento, inviti, attivita)` — stile GUI Dignitas: testata con Luna/giorno/slot, bottoni attività; inviti in cima evidenziati con `gui/portrait_<char>.png` (fallback `portrait_locked.png` se non loadable, riuso del pattern di `chapter_select`); in fondo una riga fissa disabilitata "Ofelia — Prossimamente" con `portrait_locked.png` (spec: slot riservato).
- Vars dict per le cond: costruito nel loop da `store` (`{"aede_affinity": aede_affinity, "caino_fiducia": caino_fiducia, "druso_affinity": ..., "icaro_affinity": ..., "congelate": congelate, "player_gender": player_gender, "route_attiva": route_attiva, **flags}`).

- [ ] **Step 1: scrivi `calendario.rpy`** con 2 eventi fissi segnaposto (id `"test_fisso"`) e 2 attività segnaposto per smoke.
- [ ] **Step 2: lint** — Run: `"./tools/renpy-8.3.7-sdk/renpy.exe" . lint` — Expected: zero errori.
- [ ] **Step 3: smoke manuale scriptato** — aggiungi in fondo a `tests/test_calendario.py` un check `check_wiring()` stile sanitize: `calendario.rpy` contiene `label cal_loop`, `screen pianificazione`, `import calendario_logic`. Run: `py -3 -I tests/test_calendario.py` — Expected: PASS.
- [ ] **Step 4: rimuovi i segnaposto** quando Task 4 registra i primi eventi veri (nota per l'esecutore: lasciali finché non c'è contenuto reale).

### Task 3: Attività base e scene territorio generiche

**Files:**
- Create: `game/routes/attivita.rpy`
- Modify: `game/calendario.rpy` (riempire `ATTIVITA`)

**Interfaces:**
- Consumes: `ATTIVITA`, `cal_attivita`, pool da Task 2; `qdiss` da `regia.rpy`.
- Produces: label `att_spada_1..3` (Aede, ±1 `aede_affinity`), `att_scudo_1..3` (Druso mattina, ±1 `druso_affinity`), `att_studio_1..3` (lore Famiglia, nessun punto), `att_riti_1..3` (= gli attuali `interludio1/2/3` ricollocati: wrapper label che li chiama senza i `jump cap*` finali), `att_citta_1..2`, `att_taverna_1..3` (Druso sera), `att_fumeria_1..3` (Icaro sera, visibile solo di sera).

- [ ] **Step 1: scrivi le scene** — brevi (10-20 righe), con una scelta a 2-3 opzioni dove c'è il personaggio (±1); voci fedeli ai profili; gli interludi esistenti NON si copiano: wrapper che salta il jump finale (usa `call interludio1` dopo aver trasformato i loro `jump capN` finali in `return` — ritocco di raccordo ammesso).
- [ ] **Step 2: registra i pool in `ATTIVITA`** per slot (spada/studio mattina+pomeriggio, scudo mattina, riti pomeriggio, città pomeriggio, taverna+fumeria sera).
- [ ] **Step 3: lint** — Expected: zero errori.

### Task 4: Ricollocazione route Aede

**Files:**
- Modify: `game/routes/aede_atto1.rpy`, `aede_atto2.rpy`, `aede_finali.rpy` (solo jump di raccordo)
- Create: `game/routes/aede_eventi.rpy` (registry + mini-scena impegno)

**Interfaces:**
- Consumes: `EVENTI`, vars dict (Task 2).
- Produces: eventi registrati:
  - fisso `svelo` Luna I g1 sera → `prologo` (senza il `jump interludio1` finale: diventa `return`)
  - invito `aede_cap1` luna_min 1, cond `aede_affinity>=2` → `cap1`
  - fisso `athlion` Luna III → `cap2`
  - invito `aede_cap3` luna_min 3, cond `>=5` → `cap3`
  - invito `aede_cap4` luna_min 4, cond `>=7` → `cap4`; al ritorno, se `flag_accetta_lavoro==False` → `congelate.add("aede")`
  - mini-scena `impegno_aede` (nuova, ~15 righe: Aede, a modo suo, chiede se "questa cosa" ha un nome; bivio accetta/rifiuta; rifiuto → `congelate.add("aede")`)
  - cap5 (Fiaccolata) e cap6: chiamati da Task 8 dentro Luna V se `route_attiva=="aede"`; climax+finali Luna VI invariati.
- Tutti i `jump capN`/`jump interludioN` di fine scena nelle route Aede → `return` (il loop riprende il controllo).

- [ ] **Step 1: converti i jump in return** nei file Aede (lista: prologo→interludio1, interludio1→cap1, cap1→cap2, cap2→interludio2, interludio2→cap3, cap3→cap4, cap4→interludio3, interludio3→cap5, cap5→cap6, cap6→climax). Il routing interno di `aede_finali.rpy` (climax→finali) resta intatto.
- [ ] **Step 2: scrivi `aede_eventi.rpy`** con registry + `impegno_aede`.
- [ ] **Step 3: lint** — Expected: zero errori.
- [ ] **Step 4: estendi `tests/test_calendario.py`**: carica `EVENTI` statici? No — check testuale: `aede_eventi.rpy` registra gli id `svelo`, `aede_cap1`, `athlion`, `aede_cap3`, `aede_cap4`, `impegno_aede`; nessun `jump cap` residuo in `aede_atto1/atto2.rpy`. Run: `py -3 -I tests/test_calendario.py` — Expected: PASS.

### Task 5: Ricollocazione route Caino

**Files:**
- Modify: `game/routes/caino_atto1.rpy`, `caino_atto2.rpy`, `caino_finali.rpy` (jump di raccordo)
- Create: `game/routes/caino_eventi.rpy`

**Interfaces:**
- Consumes: come Task 4.
- Produces:
  - fisso `adunanza` Luna II → `caino_prologo`; al ritorno, se la scelta trappola è stata presa (`caino_trappole>=1` a fine prologo) → `congelate.add("caino")` (restano le attività scrivano senza romance: pool `att_registri_1..2`, nuovo, senza punti)
  - inviti `caino_cap1..cap6` luna_min 2..4, cond `caino_fiducia>=2/4/6/8/9/10` e `"caino" not in congelate`
  - mini-scena `impegno_caino` (nuova: due pergamene ancora sul tavolo, stavolta la domanda è esplicita; rifiuto → `congelate.add("caino")`)
  - climax+finali Luna VI invariati (incluso secret end Teschio, condizioni attuali).
- Jump da convertire: caino_prologo→caino_cap1→...→caino_cap6→caino_climax: fine scena → `return`; routing interno di `caino_finali.rpy` intatto.

- [ ] **Step 1: converti i jump**, **Step 2: scrivi `caino_eventi.rpy` + `att_registri`**, **Step 3: lint**, **Step 4: estendi il check testuale** (id `adunanza`, `caino_cap1..6`, `impegno_caino`; nessun `jump caino_cap` residuo). Expected: PASS + lint pulito.

### Task 6: Route Druso — "Il cuore provocatore"

**Files:**
- Create: `game/routes/druso_route.rpy` (eventi a soglia, impegno, climax, finali), registry in testa al file
- Modify: `game/calendario.rpy` solo se servono nuove attività

**Interfaces:**
- Consumes: `druso_affinity` (Task 2), pool territorio `att_scudo_*`/`att_taverna_*` (Task 3), sprite esistenti `druso ghigno/neutro` (placeholder), `portrait_locked` finché non c'è arte.
- Produces:
  - default `druso_passi_falsi = 0` (per uomo: 2 passi falsi → `congelate.add("druso")`)
  - inviti `druso_ev1` (poesia oscena alla taverna, luna_min 2, `druso_affinity>=3`), `druso_ev2` (la scommessa/leva, luna_min 3, `>=6`), `druso_ev3` (il momento di coraggio che stupisce lui stesso, luna_min 4, `>=9`)
  - `impegno_druso`: soglia `>=10` se `player_gender=="f"`, `>=12` se `"m"` (difficoltà 4/5 vs 5/5)
  - Luna V-VI (chiamati da Task 8): `druso_fiaccolata` (variante Calà), `druso_climax`, finali: `druso_good` (l'intesa senza provocazioni — il poema ispirato alla realtà), `druso_neutral` (compagni di bevute, niente di più), `druso_bad` (sei il cane che abbaia: ti archivia come leva).
- Meccanica lucchetto a rovescio nelle scelte: risposta che tiene testa +1, cedere/minacciare/piagnucolare -1 (e `druso_passi_falsi+=1` se uomo).

- [ ] **Step 1: scrivi le scene** (eventi 30-60 righe l'uno, climax+finali ~120 righe totali) — voce dal profilo: brat, provocatore, poeta sconcio, codardo che sorprende sé stesso; TESCHIO e la dinamica coi fratelli già stabilita in `caino_atto1.rpy` restano canone.
- [ ] **Step 2: registra eventi**, **Step 3: lint**, **Step 4: check testuale** (id presenti, soglie di genere distinte nel cond). Expected: PASS + lint pulito.

### Task 7: Route Icaro — "Untouchable" + variante Bro

**Files:**
- Create: `game/routes/icaro_route.rpy`
- Create: placeholder sprite `game/images/icaro neutro.png` (PIL, stile del placeholder di Caino: silhouette + testo "ICARO neutro"; script usa-e-getta nello scratchpad, NON nel repo)
- Modify: `make_gui.py` (riga `portrait_diamond("portrait_icaro.png", ...)` toni oro-verde rame per distinguerlo) + rigenera

**Interfaces:**
- Consumes: `icaro_affinity`, pool `att_fumeria_*` (Task 3), `player_gender`.
- Produces:
  - default `icaro_impegnato = False`
  - Ingresso: le prime due varianti fumeria sono fredde (ti ignora); `icaro_ev1` (il baro: te ne accorgi — coprirlo in pubblico `+2`, smascherarlo → `congelate.add("icaro")`) luna_min 2, `>=3` dalle varianti
  - `icaro_ev2` (gli averi: capisci il suo mondo materiale, luna_min 3, `>=6`), `icaro_ev3` (la serata placida: pipa, silenzio giusto, luna_min 4, `>=9`)
  - Romance SOLO `player_gender=="f"`: ogni evento romance ha cond con il genere; per `"m"` gli stessi slot servono la linea Bro (stessa trama, tono amicale, zero contatto fisico — lo detesta)
  - Possessività: dopo `icaro_ev2`, accettare un invito di un altro personaggio → `congelate.add("icaro")` per sempre (check nel loop di Task 2: evento `char != "icaro"` accettato e `icaro_affinity>=6` → congela; implementato qui come hook `icaro_gelosia(char)` chiamato da `cal_loop`)
  - `impegno_icaro`: soglia `>=13` (la più alta del gioco, 5/5); per `"m"`: `impegno_bro` soglia `>=8`
  - Luna V-VI: `icaro_fiaccolata` (+variante bro), `icaro_climax`, finali: `icaro_good` (l'eccezione che conferma ogni sua regola), `icaro_neutral` (socio di carte), `icaro_bad` (hai toccato ciò che è suo), `icaro_bro_end`.

- [ ] **Step 1: genera placeholder sprite** (script PIL nello scratchpad, output `game/images/icaro neutro.png` 600x1050 come gli altri) + `portrait_icaro` in `make_gui.py`, `py -3 make_gui.py`.
- [ ] **Step 2: scrivi le scene** — voce dal profilo: nonchalant, logico, schietto senza tatto, avaro, baro puntiglioso, pipa; mai compagnone.
- [ ] **Step 3: registra eventi + hook gelosia in `cal_loop`**, **Step 4: lint**, **Step 5: check testuale** (cond con `player_gender` su ogni evento romance; hook presente). Expected: PASS + lint pulito.

### Task 8: Snodi comuni: scelta del cuore, Fiaccolata, Luna VI, finale neutro

**Files:**
- Create: `game/routes/snodi.rpy`
- Modify: `game/calendario.rpy` (fine sequenza → `cal_fine_semestre`)

**Interfaces:**
- Consumes: `route_attiva`, `congelate`, affinità (Task 2), impegni (Task 4-7), `cap5`/`cap6`/`climax` Aede, `caino_climax`, label Druso/Icaro.
- Produces:
  - fisso `scelta_cuore` ultimo giorno Luna IV: raccoglie i candidati sopra soglia non congelati; 0 candidati → prosegue senza route; 1 → chiama il suo `impegno_*`; 2+ → menu esplicito al giocatore (pari merito deciso da lui), poi `impegno_*` del prescelto; accettato → `route_attiva = char`
  - fisso `fiaccolata` Luna V: dispatch su `route_attiva` — `"aede"`→`cap5` (poi `aede_cap6` come invito automatico pochi giorni dopo), `"caino"`→`fiaccolata_caino` (nuova, breve), `"druso"`→`druso_fiaccolata`, `"icaro"`→`icaro_fiaccolata`, `None`→`fiaccolata_neutra` (Vanna+Corrado, nuova, breve)
  - fisso `luna6_climax` Luna VI: dispatch — `"aede"`→`climax`, `"caino"`→`caino_climax`, `"druso"`→`druso_climax`, `"icaro"`→`icaro_climax`/bro, `None`→`finale_neutro_semestre` (nuovo, breve: Briseide tira le somme, rimando)
  - `cal_fine_semestre`: fallback se la sequenza finisce senza climax → `finale_neutro_semestre`.

- [ ] **Step 1: scrivi `snodi.rpy`** (dispatch + 3 scene nuove brevi: `fiaccolata_caino`, `fiaccolata_neutra`, `finale_neutro_semestre`).
- [ ] **Step 2: lint**, **Step 3: check testuale** (dispatch copre i 4 char + None in entrambi gli snodi). Expected: PASS + lint pulito.

### Task 9: Nuovo ingresso capitolo + pulizia

**Files:**
- Modify: `game/routes/chapter1.rpy` — `label capitolo1`: resta sesso+nome+background Briseide; poi `jump cal_loop` (lo Svelo è il primo evento fisso). `screen chapter_select` e `label capitolo1_dispatch` rimossi; `CAP1_ROUTES` resta come dato per futuri usi o viene rimosso (scelta dell'esecutore).
- Modify: `game/script.rpy` — commento aggiornato.

- [ ] **Step 1: modifica chapter1.rpy**, **Step 2: lint** — Expected: zero errori.
- [ ] **Step 3: run completo test** — Run: `py -3 -I tests/test_calendario.py && py -3 -I tests/test_sanitize.py` — Expected: tutti PASS (attenzione: `test_sanitize.check_wiring` richiede che `renpy.input` e `sanitize_name` restino in `chapter1.rpy`).

### Task 10: Verifica finale

- [ ] **Step 1:** `"./tools/renpy-8.3.7-sdk/renpy.exe" . lint` → zero errori.
- [ ] **Step 2:** entrambi i test script → PASS.
- [ ] **Step 3:** smoke di percorso: grep che ogni `label` registrato in un evento esista (`EVENTI` label vs `label X:` nei .rpy) — aggiungi check finale in `tests/test_calendario.py`.
- [ ] **Step 4:** riepilogo all'utente: cosa giocare per provare (percorso rapido Aede), limite salvataggi vecchi, contenuti Ofelia ancora bloccati, sprite Druso/Icaro placeholder.
