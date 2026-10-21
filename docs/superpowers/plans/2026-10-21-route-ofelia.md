# Route Ofelia "Tanto bella quanto letale" Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rendere giocabile la route di Ofelia nel calendario dei Malandrini, con lucchetto a inviti a scadenza e route doppia (poliamore) con Aede (segreto) o Caino (dichiarato).

**Architecture:** Il motore puro (`game/calendario_logic.py`) guadagna una sola funzione generica (`inviti_ignorati`); tutto il resto vive in due file di route nuovi (`ofelia_route.rpy`, `ofelia_finali.rpy`) più ritocchi agli snodi (`snodi.rpy`) e al loop (`calendario.rpy`). La route doppia è una seconda variabile di store, `route_seconda`, letta dal filtro inviti e dai dispatch di Fiaccolata e climax.

**Tech Stack:** Ren'Py 8.3.7 (`tools/renpy-8.3.7-sdk`), Python 3 per i test (`py -3 -I`).

**Spec:** `docs/superpowers/specs/2026-10-21-route-ofelia-design.md` (profilo: `docs/profili/ofelia.md`)

## Global Constraints

- Nome route: "Tanto bella quanto letale". Difficoltà 4/5.
- Poliamore solo con Aede (Aede NON sa e NON accetta) e con Caino (dichiarato). Mai con Druso/Icaro.
- Soglie: impegno `ofelia_affinity >= 8`; good `ofelia_affinity >= 11` e `ofelia_mancati <= 1`; congelamento a `ofelia_mancati >= 2`; bad tempesta a `aede_sospetto >= 2`.
- Punti: scene territorio ±1 una-tantum; `ofelia_ev1-3` +2 ciascuno; Fiaccolata +1; `ofelia_ev4` +2; climax ±1. Max 9 alla scelta del cuore, 13 a fine semestre.
- Date fisse del semestre intoccabili; nessun invito a soglia con `luna_min >= 5`.
- REGOLA PICKLE: nessun dict con lambda nello store o in `Return(...)`.
- Ogni label di scena finisce con `return`. Solo sprite/bg esistenti (`ls game/images`): Ofelia ha `neutra`, `rabbia`, `imbarazzata`, `compiaciuta`; la serra usa `bg sala_svelo` come placeholder.
- Testi: skill `writing-vn-scenes` (varianti di genere `[fin]`, `[figlio_t]`…, battute max 2-3 righe, regia di `regia.rpy`). Voce dal profilo `docs/profili/ofelia.md`: letale, elegante, sarcastica, riservata, imprevedibile.
- Niente `git commit` senza richiesta esplicita dell'utente: i passi "verifica" sostituiscono i commit.
- Verifica di ogni task: `py -3 -I tests/test_calendario.py` → `tutti i casi ok`; `py -3 -I tests/test_routing.py` → `6/6 scenari ok`; `"./tools/renpy-8.3.7-sdk/renpy.exe" . lint` senza errori.

## Review Focus

- Invito di Ofelia mostrato in uno slot dove il giocatore sceglie un ALTRO invito o un'attività: conta come mancato; se sceglie l'invito di Ofelia, nessun mancato. Due inviti di Ofelia nello stesso slot sono impossibili per cond a catena, ma `inviti_ignorati` deve comunque restituirli entrambi (test Task 1).
- Ofelia congelata (`mancati >= 2`) o a route attiva altrui: i suoi inviti non compaiono, quindi non generano altri mancati (test Task 2: hook ignora id non di Ofelia e non conta oltre il congelamento).
- Route doppia con un impegno fallito: deve restare attiva solo la route riuscita, `route_seconda = None` (test Task 4 su stringhe del label).
- Poly con Aede seconda congelata dal vicolo (cap4) dopo l'impegno: `route_seconda_viva()` deve restituire None e i dispatch cadere sui rami di Ofelia sola (test Task 4/6).
- Salvataggio a metà semestre con `route_seconda` impostata: è una stringa, picklabile; `cal_inviti` contiene solo dict semplici con `scade` booleano (test Task 1 su `cal_inviti_info`).

---

### Task 1: Motore — inviti a scadenza

**Files:**
- Modify: `game/calendario_logic.py` (nuova funzione in coda)
- Modify: `game/calendario.rpy` (`cal_inviti_info`, `cal_loop`, screen `pianificazione`, nuova lista hook)
- Test: `tests/test_calendario.py`

**Interfaces:**
- Produces: `inviti_ignorati(mostrati: list[dict], scelto_id: str | None) -> list[str]` — id degli elementi di `mostrati` con `m.get("scade")` vero e `m["id"] != scelto_id`, nell'ordine di `mostrati`.
- Produces: `cal_inviti_ignorati_hooks = []` (init -10 in `calendario.rpy`): lista di `fn(ids: list[str]) -> None`.
- Produces: `cal_inviti_info` include la chiave `"scade": bool(e.get("scade", False))`.

- [ ] **Step 1: Test che fallisce** — in `tests/test_calendario.py`, `test_scadenza()` registrato in `main()`:

```python
def test_scadenza():
    a = {"id": "of1", "scade": True}
    b = {"id": "ae1"}
    c = {"id": "of2", "scade": True}
    check("scadenza: scelto altro", cl.inviti_ignorati([a, b], "ae1"), ["of1"])
    check("scadenza: scelto lei", cl.inviti_ignorati([a, b], "of1"), [])
    check("scadenza: attivita'", cl.inviti_ignorati([a, b, c], None), ["of1", "of2"])
    check("scadenza: nessuna", cl.inviti_ignorati([b], None), [])
```

e in `check_store_picklabile()`:

```python
    check("info inviti espone scade", '"scade": bool(e.get("scade", False))' in cal, True)
    check("loop chiama hook scadenza", "cal_inviti_ignorati_hooks" in cal, True)
```

- [ ] **Step 2:** `py -3 -I tests/test_calendario.py` → FAIL (`AttributeError: ... inviti_ignorati`).
- [ ] **Step 3: Implementa** `inviti_ignorati` in `calendario_logic.py` (docstring nello stile del file). In `calendario.rpy`: lista `cal_inviti_ignorati_hooks = []` accanto a `cal_post_evento_hooks`; chiave `scade` in `cal_inviti_info`; in `cal_loop`, subito dopo `call screen pianificazione(...)`, un blocco python che calcola `scelto = _return[1] if _return[0] == "evento" else None`, poi `ign = cl.inviti_ignorati(cal_inviti, scelto)` e chiama ogni hook con `ign` se non vuota. Nella screen, sotto `inv["titolo"]`, se `inv.get("scade")`: `text "Solo adesso" size 17 color "#8f7f5c"` (vbox con il titolo).
- [ ] **Step 4:** test + lint → PASS.

### Task 2: Ofelia — core, territorio, hook dei mancati

**Files:**
- Create: `game/routes/ofelia_route.rpy`
- Modify: `game/calendario.rpy` (`cal_vars`, `diario_rapporti`, rimozione riquadro "Prossimamente" righe ~350-358, `ATTIVITA_DESC`, `CAL_FALLBACK`)
- Modify: `game/screens.rpy` (`CHAR_COLORS`: `"Ofelia": "#7d3c98"`)
- Test: `tests/test_calendario.py` (`check_eventi_ofelia()` nuovo, in `main()`)

**Interfaces:**
- Consumes: `cal_inviti_ignorati_hooks` (Task 1).
- Produces (store): `ofelia_affinity = 0`, `ofelia_mancati = 0`, `route_seconda = None`, `aede_sospetto = 0`; `define ofelia = Character("Ofelia", color="#7d3c98")`.
- Produces: `cal_vars()` con chiavi `ofelia_affinity`, `ofelia_mancati`, `route_seconda`.
- Produces: `ofelia_scadenza(ids)` registrata in `cal_inviti_ignorati_hooks`; attività `("corte", "La corte di Ofelia", "ofelia", ["att_corte_1", "att_corte_2", "att_corte_3"])` in `ATTIVITA["pomeriggio"]`.

- [ ] **Step 1: Test che fallisce** — `check_eventi_ofelia()`:

```python
def check_eventi_ofelia():
    ev = _leggi(os.path.join("routes", "ofelia_route.rpy"))
    check("hook scadenza registrato",
          "cal_inviti_ignorati_hooks.append(ofelia_scadenza)" in ev, True)
    check("congela a 2 mancati", "ofelia_mancati >= 2" in ev, True)
    check("territorio corte", '"corte", "La corte di Ofelia", "ofelia"' in ev, True)
    for lbl in ("att_corte_1", "att_corte_2", "att_corte_3"):
        check("label " + lbl, "label " + lbl + ":" in ev, True)
    cal = _leggi("calendario.rpy")
    check("Prossimamente rimosso", "Prossimamente" in cal, False)
    check("cal_vars ofelia", '"ofelia_affinity": store.ofelia_affinity' in cal, True)
```

- [ ] **Step 2:** test → FAIL (file mancante).
- [ ] **Step 3: Implementa.** Intestazione del file nello stile di `druso_route.rpy` (nome route, 4/5, lucchetto, poly con Aede/Caino). `ofelia_scadenza(ids)`: per ogni id che inizia con `"ofelia_"`, se `"ofelia" not in store.congelate`: `ofelia_mancati += 1`, `ofelia_affinity -= 1`, `renpy.notify("Ofelia non aspetta nessuno.")`; a `ofelia_mancati >= 2` → `congelate.add("ofelia")` e `renpy.notify("Per Ofelia sei già un nome tra tanti.")`. `ATTIVITA_DESC["corte"] = "La serra, i pretendenti, e lei che sceglie."`; `CAL_FALLBACK["corte"] = "Fiori d'inverno, pretendenti in fila. Oggi Ofelia non ha guardato nessuno. Nemmeno me."`. Diario: riga Ofelia con soglie (8 "Ti concede un ballo che rifiuta a tutti. Non lo dirà mai.", 4 "Ricorda il tuo nome. Lo usa come una lama.", 1 "Ti conta tra i pretendenti. In fondo alla fila."). Tre scene territorio (`bg sala_svelo`), ognuna con un menu che dà `ofelia_affinity += 1` alla risposta che non la adula e `-= 1` a quella da pretendente qualunque; ciascuna, se `route_seconda == "aede"`, fa `aede_sospetto += 1` (la sorella sente dire che passi in serra).
- [ ] **Step 4:** test + lint → PASS.

### Task 3: Eventi a soglia 1-3

**Files:**
- Modify: `game/routes/ofelia_route.rpy`
- Test: `tests/test_calendario.py` (`check_eventi_ofelia`, `check_economia_punti`, `check_prerequisiti_sequenza`)

**Interfaces:**
- Consumes: `ofelia_affinity`, `"scade"` (Task 1-2).
- Produces: eventi `ofelia_ev1` (luna_min 1, pomeriggio, `>= 2`), `ofelia_ev2` (luna_min 2, sera, `>= 4` + ev1 visto), `ofelia_ev3` (luna_min 3, mattina, `>= 6` + ev2 visto + `"scelta_cuore" not in v["visti"]`), tutti `"scade": True`, `"char": "ofelia"`, label omonimi.

- [ ] **Step 1: Test che fallisce** — aggiungi:

```python
    # in check_eventi_ofelia
    for eid in ('"ofelia_ev1"', '"ofelia_ev2"', '"ofelia_ev3"'):
        check("evento ofelia " + eid, eid in ev, True)
    check("inviti ofelia a scadenza", ev.count('"scade": True') >= 3, True)
    # in check_economia_punti
    ofelia_max = _max_punti("ofelia_affinity")
    check("ofelia: impegno (8) raggiungibile", ofelia_max >= 8, True)
    check("ofelia: good end (11) raggiungibile", ofelia_max >= 11, True)
    # in check_prerequisiti_sequenza
    of = _leggi(os.path.join("routes", "ofelia_route.rpy"))
    check("ofelia_ev2 richiede ev1", '"ofelia_ev1" in v["visti"]' in of, True)
    check("ofelia_ev3 richiede ev2", '"ofelia_ev2" in v["visti"]' in of, True)
    check("ofelia_ev3 muore dopo scelta_cuore", '"scelta_cuore" not in v["visti"]' in of, True)
```

- [ ] **Step 2:** test → FAIL. (`good end (11)` resta FAIL fino a Task 5: atteso.)
- [ ] **Step 3: Scrivi le scene**, ognuna con un menu a 2-3 opzioni, massimo `+= 2`:
  - `ofelia_ev1` "Il pretendente scartato": in serra Ofelia umilia in pubblico un corteggiatore; premia chi non ride con la folla né la rimprovera (+2), punisce chi fa il cavaliere (−1).
  - `ofelia_ev2` "Il rivale": ti porta a una cena per far ingelosire un pretendente di rango. Il difetto costa: accetti di essere usato con stile (+2) o lo dici in faccia (+1, lei rispetta); scenata (−1).
  - `ofelia_ev3` "Il duello all'alba" (`bg arena_athlion`): tira sul serio; reggere senza chiedere pietà (+2), arrendersi con eleganza (+1).
- [ ] **Step 4:** test (salvo `good end (11)`) + lint → PASS.

### Task 4: Scelta del cuore e route doppia

**Files:**
- Modify: `game/routes/snodi.rpy` (`CUORE_NOMI`, `cuore_candidati`, `route_seconda_viva`, `ev_scelta_cuore`, cond di `aede_cap6`)
- Modify: `game/calendario.rpy` (`cal_inviti_info` filtro)
- Modify: `game/routes/ofelia_route.rpy` (impegni)
- Test: `tests/test_calendario.py` (`check_snodi`, `check_eventi_ofelia`, `check_congelamento_route_attiva`)

**Interfaces:**
- Produces: `route_seconda_viva() -> str | None` (seconda non congelata, solo se `route_viva() == "ofelia"`).
- Produces: `cuore_opzioni(cands: list[str]) -> list[tuple[str, str]]` in `snodi.rpy`: `(testo, chiave)` dove chiave è un personaggio o `"ofelia+aede"` / `"ofelia+caino"` (coppie solo se entrambi in `cands`).
- Produces: label `impegno_ofelia`, `impegno_ofelia_aede`, `impegno_ofelia_caino`; ciascuno imposta `impegno_esito`.

- [ ] **Step 1: Test che fallisce:**

```python
    # check_snodi
    check("candidata ofelia soglia 8", "store.ofelia_affinity >= 8" in ev, True)
    check("coppie poly", '"ofelia+aede"' in ev and '"ofelia+caino"' in ev, True)
    check("route_seconda impostata", "route_seconda =" in ev, True)
    check("aede_cap6 anche da seconda", 'v["route_seconda"] == "aede"' in ev, True)
    # check_congelamento_route_attiva
    check("seconda viva esclude congelata", "def route_seconda_viva" in sn, True)
    cal = _leggi("calendario.rpy")
    check("filtro inviti con seconda", "store.route_seconda" in cal, True)
    # check_eventi_ofelia
    for lbl in ("impegno_ofelia", "impegno_ofelia_aede", "impegno_ofelia_caino"):
        check("label " + lbl, "label " + lbl + ":" in ev, True)
```

- [ ] **Step 2:** test → FAIL.
- [ ] **Step 3: Implementa.** `ev_scelta_cuore` usa `cuore_opzioni`; se una sola opzione la sceglie senza menu (comportamento attuale). Ramo coppia: `call impegno_ofelia_<x>`; esito: entrambi riusciti → `route_attiva = "ofelia"`, `route_seconda = x`; riuscito solo uno → quella route attiva, `route_seconda = None`; nessuno → nulla. Impegni: `impegno_ofelia` (serra, sera; bivio accetta/rifiuta come `impegno_aede`, rifiuto → `congelate.add("ofelia")`). `impegno_ofelia_caino`: Ofelia propone il patto a tre davanti a Caino, Caino lo mette a registro; esiti separati in due variabili locali `impegno_of` / `impegno_altro`. `impegno_ofelia_aede`: Ofelia accetta "la sorella e te" ma impone il segreto ("Aede non divide. Io sì. Non farglielo sapere."); poi `call impegno_aede` per l'esito di Aede. Filtro inviti: `e.get("char") in (None, store.route_attiva, store.route_seconda)`.
- [ ] **Step 4:** test + lint → PASS. Verifica manuale con `tests/test_routing.py` invariato (6/6).

### Task 5: Fiaccolata a tre/a due mani e `ofelia_ev4`

**Files:**
- Create: `game/routes/ofelia_finali.rpy`
- Modify: `game/routes/snodi.rpy` (`ev_fiaccolata`)
- Modify: `game/routes/ofelia_route.rpy` (evento fisso `ofelia_ev4`)
- Test: `tests/test_calendario.py`

**Interfaces:**
- Consumes: `route_viva()`, `route_seconda_viva()` (Task 4); label `cap5` (Aede, esistente).
- Produces: label `ofelia_fiaccolata`, `ofelia_fiaccolata_caino`, `ofelia_fiaccolata_aede`, `ofelia_ev4`; evento `{"id": "ofelia_ev4", "tipo": "fisso", "char": "ofelia", "luna": 5, "giorno": 26, "slot": "pomeriggio", "cond": route_attiva == "ofelia" and "ofelia" not in congelate}`.

- [ ] **Step 1: Test che fallisce:**

```python
    # check_snodi
    check("dispatch ofelia", ev.count('cal_route == "ofelia"') >= 2, True)
    # check_eventi_ofelia
    fin = _leggi(os.path.join("routes", "ofelia_finali.rpy"))
    for lbl in ("ofelia_fiaccolata", "ofelia_fiaccolata_caino", "ofelia_fiaccolata_aede"):
        check("label " + lbl, "label " + lbl + ":" in fin, True)
    check("mano di Ofelia alza il sospetto", "aede_sospetto += 2" in fin, True)
    check("mano di Aede gioca cap5", "call cap5" in fin, True)
    check("ofelia_ev4 fisso V/26", '"luna": 5, "giorno": 26' in ev, True)
```

- [ ] **Step 2:** test → FAIL.
- [ ] **Step 3: Implementa.** `ev_fiaccolata`: ramo `cal_route == "ofelia"` dispatcha su `route_seconda_viva()` (`"caino"` → `_caino`, `"aede"` → `_aede`, altrimenti sola). Punti: `ofelia_fiaccolata` +1; `ofelia_fiaccolata_caino` +1 Ofelia e `caino_fiducia += 1`; `ofelia_fiaccolata_aede` menu "mano di Aede" → `call cap5` (Ofelia +0) / "mano di Ofelia" → `ofelia_affinity += 1`, `aede_sospetto += 2` (Aede vede dall'alto della Calà, `aede rabbia`). `ofelia_ev4` (Luna V, pomeriggio): menu "di nascosto" (`+= 1`) / "alla luce del sole" (`+= 2`, e se `route_seconda == "aede"`: `aede_sospetto += 1`).
- [ ] **Step 4:** test (ora anche `good end (11)`) + lint → PASS.

### Task 6: Climax e finali

**Files:**
- Modify: `game/routes/ofelia_finali.rpy`
- Modify: `game/routes/snodi.rpy` (`ev_luna6`)
- Modify: `game/routes/aede_finali.rpy` (una riga prima del routing, ~riga 64)
- Test: `tests/test_calendario.py`, `tests/test_routing.py` (deve restare 6/6)

**Interfaces:**
- Consumes: `route_seconda_viva()`, label `climax` (Aede), condizioni good Aede/Caino esistenti.
- Produces: label `ofelia_climax`, `ofelia_routing`, `ofelia_poly_aede_routing`, finali `ofelia_good`, `ofelia_good_caino`, `ofelia_good_aede`, `ofelia_bad_tempesta`, `ofelia_neutral`.

- [ ] **Step 1: Test che fallisce:**

```python
    # check_eventi_ofelia
    for lbl in ("ofelia_climax", "ofelia_routing", "ofelia_poly_aede_routing",
                "ofelia_good", "ofelia_good_caino", "ofelia_good_aede",
                "ofelia_bad_tempesta", "ofelia_neutral"):
        check("label " + lbl, "label " + lbl + ":" in fin, True)
    check("good ofelia soglie",
          "ofelia_affinity >= 11 and ofelia_mancati <= 1" in fin, True)
    check("tempesta prima del good", fin.index("aede_sospetto >= 2") <
          fin.index("label ofelia_good_aede:"), True)
    check("cartello route", "TANTO BELLA QUANTO LETALE" in fin, True)
    ae = _leggi(os.path.join("routes", "aede_finali.rpy"))
    check("innesto poly nel climax Aede", 'route_seconda == "aede"' in ae, True)
```

- [ ] **Step 2:** test → FAIL.
- [ ] **Step 3: Implementa.**
  - `ev_luna6`: ramo `cal_route == "ofelia"`: se `route_seconda_viva() == "aede"` → `call climax` (Aede), altrimenti `call ofelia_climax`.
  - `aede_finali.rpy`, prima di `# Routing finali`: `if route_seconda == "aede": jump ofelia_poly_aede_routing` (Ofelia presente nello studio: una battuta sua prima del routing, `show ofelia neutra at left`).
  - `ofelia_poly_aede_routing` (ordine vincolante): `aede_sospetto >= 2` → `ofelia_bad_tempesta`; good Ofelia e `aede_affinity >= 12 and flag_giuramento and flag_accetta_lavoro` → `ofelia_good_aede`; good Ofelia → `ofelia_good` (coda amara su Aede); altrimenti → routing Aede esistente (`neutral_end`/bad come oggi, ricopiando le sue tre condizioni).
  - `ofelia_climax` (`bg studio_glauco`, Glauco e la figlia "imprevedibile al punto giusto": lei lo sfida per te; menu finale ±1) → `ofelia_routing`: good + `route_seconda_viva() == "caino"` + `caino_fiducia >= 12` → `ofelia_good_caino`; good → `ofelia_good`; altrimenti → `ofelia_neutral`.
  - Cartelli `centered`: `ofelia_good` "TANTO BELLA QUANTO LETALE"; `ofelia_good_caino` "IL CONTRATTO A TRE"; `ofelia_good_aede` "LE FIGLIE DI GLAUCO"; `ofelia_bad_tempesta` "LA TEMPESTA" (`aede furia`, `with lampo`); `ofelia_neutral` "INTERESSE PASSEGGERO".
- [ ] **Step 4:** test + `tests/test_routing.py` (6/6) + lint → PASS.

### Task 7: Documentazione di bordo

**Files:**
- Modify: `.claude/skills/character-sim/SKILL.md` (soglie: aggiungi "ofelia 8 / good >=11 + mancati<=1"; lucchetti: "Ofelia: inviti a scadenza"; route doppia `route_seconda`)
- Modify: `.claude/skills/writing-vn-scenes/SKILL.md` (personaggi: aggiungi `ofelia`)
- Modify: `.claude/skills/game-brainstorm/SKILL.md` (territori presi: aggiungi "corte/serra=Ofelia"; lucchetti presi: aggiungi "inviti a scadenza")
- Modify: `README.md` (route di Ofelia tra i contenuti)

- [ ] **Step 1:** Applica le righe sopra.
- [ ] **Step 2:** Verifica finale completa (Global Constraints) → tutto PASS.
