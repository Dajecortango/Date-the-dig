# Route riordinate, finali "passeggeri", dialoghi origliati, scelte chiare — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Split Druso/Icaro/Ofelia into the Aede/Caino file schema, add 2 scenes per route, add 4 "passeggero" endings, 3 overheard conversations, and clearer menu options without breaking the Trama history.

**Architecture:** Ren'Py game; pure logic in `game/*_logic.py` (importable by tests), content in `.rpy` hooked through registries (`EVENTI`, `FATTI`, `ECHI`, `ECO_DOPO_LABELS`, `FINALI`). Tests are plain scripts (`py -3 -I tests/<file>.py`) that call the pure modules and grep `.rpy` text.

**Tech Stack:** Ren'Py 8.3.7 (SDK in `tools/`), Python 3, `lint.ps1`.

**Spec:** `docs/superpowers/specs/2026-10-22-route-finali-origliati-design.md` — read it before any task.

## Global Constraints

- No `git commit`/`push` unless the user asks (user rule). Where a task says "Checkpoint", run the verification and stop; do not commit.
- Existing event order and `cond` chains unchanged. New events only Lune II-IV; existing fixed dates untouched.
- New scenes: ±1 affinity max, once per scene. Overheard scenes: 0 affinity.
- No numeric stats visible.
- Existing scenes are not rewritten. Only exception: option text in Task 11.
- Prose: load skill `writing-vn-scenes` before writing any scene; load `character-sim` before touching `EVENTI`, thresholds, routing.
- Gender-neutral protagonist markup: `[fin]`, `[il_t]`, `[un_t]`, `[figlio_t]`, `[fratello_t]` as in existing files.
- Every task ends with: all `tests/*.py` green and `lint.ps1` clean.

Run all tests (from repo root, Git Bash):
```bash
for f in tests/test_*.py; do py -3 -I "$f" > /dev/null || echo "FAIL $f"; done
```
Expected: no output. Lint: `powershell -File lint.ps1` → report with no errors.

## Review Focus

1. Old save loaded after the file split: lands at a label boundary, route variables intact, game continues (manual check, Task 12).
2. `.rpyc` left behind for a deleted `.rpy` → duplicate labels at launch. Task 2-4 check `ls game/routes/*_route.rpyc` is empty.
3. Init order drift after the split (EVENTI/ATTIVITA/hooks order) → calendar shows invites in a different order. Pinned by `tests/test_ordine_init.py` (Task 1).
4. Persistent history with old option text after Task 11 → Trama shows the same menu twice or loses the "◇ other run" marks. Pinned by tests in Task 10.
5. Overheard scene firing when both characters froze you out, or twice per run. Pinned by `origliato_ok` tests (Task 9).

---

### Task 1: Init-order baseline test

**Files:**
- Create: `tests/test_ordine_init.py`

**Interfaces:**
- Produces: `ordine_init() -> list[str]` (inside the test) — tokens in Ren'Py load order: for each `.rpy` under `game/` sorted by path relative to `game/` (forward slashes, plain string sort), in line order: every `"id": "<x>"` inside an `EVENTI.extend(`/`EVENTI.append(` block → `"EV:<x>"`, every `ATTIVITA[...]` append/extend line → `"AT:<file-independent first quoted id>"`, every `<name>_hooks.append(<fn>)` → `"HK:<name>:<fn>"`.

- [ ] **Step 1:** Write `tests/test_ordine_init.py` with `ordine_init()` and a `BASELINE` list produced by running it once on the current tree (paste the printed list as a literal). Test asserts `ordine_init() == BASELINE`, prints `"ordine init ok"`, exits 1 on mismatch with the first differing index.
- [ ] **Step 2:** Run `py -3 -I tests/test_ordine_init.py` → `ordine init ok`.
- [ ] **Step 3:** Checkpoint (all tests, lint).

### Task 2: Split Druso

**Files:**
- Create: `game/routes/druso_core.rpy`, `druso_atto1.rpy`, `druso_atto2.rpy`, `druso_eventi.rpy`, `druso_finali.rpy`
- Delete: `game/routes/druso_route.rpy`, `game/routes/druso_route.rpyc`
- Modify: `tests/test_routing.py` (WIRING), `tests/test_calendario.py:118,761`, `esporta_dialoghi.py` (`ROUTE["03_druso"]`)

**Interfaces:**
- Produces: label names unchanged. Files per spec table 1a:
  - core: header comment, `default`s, `init python` with `druso_passo_falso` only.
  - eventi: `init python` with `EVENTI.extend([...])` (verbatim), `impegno_druso`.
  - atto1: `druso_ev1`, `druso_int1`, `druso_ev2`, `druso_int2`.
  - atto2: `druso_ev3`, `druso_int3`, `druso_ev4`, `druso_luna5`, `druso_fiaccolata`, `druso_luna6`.
  - finali: `druso_climax`, `druso_good`, `druso_neutral`, `druso_bad`.

- [ ] **Step 1:** Move text by cut/paste of whole label blocks (byte-identical lines, keep section comment headers). Copy file header style from `caino_atto1.rpy` ("# Route Druso — Atto 1: ...").
- [ ] **Step 2:** Update test and export paths to the new file holding each label/registry.
- [ ] **Step 3:** Delete old `.rpy` and `.rpyc`. Verify `ls game/routes/druso_route*` → no such file.
- [ ] **Step 4:** `py -3 -I tests/test_ordine_init.py` → `ordine init ok` (core/eventi sort between `ceppo`/`echi` exactly as `druso_route` did; if not, the test says where).
- [ ] **Step 5:** Verify no text lost: `cat` of the 5 new files has the same non-blank, non-comment line multiset as `git show HEAD:game/routes/druso_route.rpy` (one-off `diff <(…|sort) <(…|sort)`), expected empty.
- [ ] **Step 6:** Checkpoint.

### Task 3: Split Icaro

Same as Task 2 for `icaro_route.rpy`.
- core: `default`s, `icaro_gelosia` + `cal_post_evento_hooks.append(icaro_gelosia)` (keep after `EVENTI.extend` in load order: if Task 1 test fails, put the hook in `icaro_eventi.rpy` after the registry).
- eventi: registry, `impegno_icaro`, `impegno_bro`.
- atto1: ev1, int1, ev2, int2. atto2: ev3, int3, bro_affari, bro_colpo, fiaccolata, luna5, luna6.
- finali: climax, good, neutral, bad, bro_end.
- Update `tests/test_routing.py` WIRING (two lines), `tests/test_calendario.py:137,291`, `esporta_dialoghi.py` `ROUTE["04_icaro"]`. Delete `.rpy`/`.rpyc`. Steps 4-6 as Task 2.

### Task 4: Split Ofelia

Same as Task 2 for `ofelia_route.rpy` + `ofelia_finali.rpy`.
- core: `define ofelia`, `default`s, `ATTIVITA["pomeriggio"].append(("corte", ...))`, `ofelia_scadenza` + hook append.
- eventi: registry, `ofelia_scadenza_prima`, `impegno_ofelia`, `impegno_ofelia_caino`, `impegno_ofelia_aede`.
- atto1: `att_corte_1..3`, `ofelia_ev1`, `ofelia_ev2`, `interludio_ofelia_1`, `interludio_ofelia_2`.
- atto2: `ofelia_ev3`, `ofelia_ev4`, `interludio_ofelia_luna6`, the three `ofelia_fiaccolata*` labels (from `ofelia_finali.rpy`).
- finali: keep file name `ofelia_finali.rpy`, now holding climax, routing, finals only.
- Delete `ofelia_route.rpy`/`.rpyc`. Update `tests/test_calendario.py:352,664,743` and 272/682 if labels moved, `esporta_dialoghi.py` `ROUTE["05_ofelia"]`. Steps 4-6 as Task 2.

### Task 5: Routing of "passeggero" endings

**Files:**
- Modify: `game/routing_logic.py:112-161`
- Test: `tests/test_routing.py` (SCENARI)

**Interfaces:**
- Produces ending ids (also label names): `aede_passeggero`, `caino_passeggero`, `druso_passeggero`, `icaro_passeggero`. Signatures of `finale_*` unchanged.

- [ ] **Step 1:** Add SCENARI (expected values):
```python
("aede: 13 senza giuramento -> passeggero", _aede(13, True, True, False), "aede_passeggero"),
("aede: 13 lavoro rifiutato -> passeggero", _aede(13, True, False, True), "aede_passeggero"),
("aede: 12 senza giuramento -> neutral", _aede(12, True, True, False), "neutral_end"),
("caino: fiducia 13, trappole 2 -> passeggero", rl.finale_caino(13, 2, 2, 0), "caino_passeggero"),
("caino: fiducia 13, memoria 1 -> passeggero", rl.finale_caino(13, 0, 1, 0), "caino_passeggero"),
("caino: fiducia 13, trappole 3 -> bad", rl.finale_caino(13, 3, 2, 0), "caino_bad_end"),
("druso: 16 senza coraggio -> passeggero", rl.finale_druso(16, False), "druso_passeggero"),
("icaro: 13 non coperto -> passeggero", _icaro(aff=13, coperto=False), "icaro_passeggero"),
("icaro: 13 congelata -> passeggero", _icaro(aff=13, congelate=("icaro",)), "icaro_passeggero"),
("icaro: uomo 13 non coperto -> bro", _icaro(gender="m", aff=13, coperto=False), "icaro_bro_end"),
("poly aede: of non good, aede 13 senza giuramento", _poly_aede(of=5, giuramento=False), "aede_passeggero"),
```
  Change the existing "druso: 16 senza coraggio -> neutral" expectation to `druso_passeggero`; review any existing scenario whose inputs now hit a new branch and update it, noting each in the task report.
- [ ] **Step 2:** Run `py -3 -I tests/test_routing.py` → FAIL on new scenarios.
- [ ] **Step 3:** Add branches per spec table (placed right after each good branch; Caino's only when `trappole < CAINO_TRAPPOLE_BAD`). Update docstrings with the new order.
- [ ] **Step 4:** Run → all PASS.
- [ ] **Step 5:** Checkpoint (the game will not lint-jump yet to missing labels — Task 6 adds them; lint may warn: run lint after Task 6).

### Task 6: Write the four "passeggero" endings

**Files:**
- Modify: `game/routes/aede_finali.rpy`, `caino_finali.rpy`, `druso_finali.rpy`, `icaro_finali.rpy` (append one label each)
- Modify: `game/finali_galleria.rpy` (`FINALI`, one tuple each after the route's good end)

**Interfaces:**
- Consumes: ids from Task 5.
- Each label ends `$ sblocca_finale("<id>")`, `centered` title card, `return` (pattern: `ofelia_neutral`).

- [ ] **Step 1:** Load `writing-vn-scenes`. Re-read `ofelia_neutral` (`ofelia_finali.rpy`). Write each ending (20-35 lines) with the structure in spec §2 "Tono": key line naming the missing step (spec list), time cut, the character seen from afar living well, a witness who closes, title card. Pick variants on the state the climax already set (e.g. `icaro_climax_scelta`, `druso_consiglio`) where natural.
- [ ] **Step 2:** Add `FINALI` tuples `(id, "TITOLO", "Route", "indizio")`; indizio hints at the missing step without numbers.
- [ ] **Step 3:** Checkpoint incl. lint (no missing-label errors).

### Task 7: Two new scenes each for Druso and Icaro

**Files:**
- Modify: `game/routes/druso_eventi.rpy`, `icaro_eventi.rpy` (registry entries), `druso_atto1.rpy`/`druso_atto2.rpy`, `icaro_atto1.rpy`/`icaro_atto2.rpy` (labels)
- Modify: `game/routes/echi.rpy` (eco labels), FATTI/ECHI via `FATTI.extend`/`ECHI.extend` in each route's `*_eventi.rpy`
- Test: `tests/test_calendario.py` (new case)

**Interfaces:**
- Event ids / labels: `druso_quaderno`, `druso_udienza`, `icaro_debito_altrui`, `icaro_febbre`.
- Registry shape: `{"id", "label", "tipo": "invito", "char", "titolo", "luna_min", "slot", "cond"}`; `cond` = previous event in `v["visti"]` and `"scelta_cuore" not in v["visti"]`; `luna_min` per spec (quaderno 2 after `druso_ev1`, udienza 3 after `druso_ev2`, debito 2 after `icaro_int1`, febbre 3 after `icaro_ev2`). No existing `cond` references these ids.
- Each scene: one store var `<id>_esito` (default `None`), one fact `{"id": "fx_<id>", ...}` in FATTI, one eco in ECHI with `luoghi` where the teller can know (Druso: taverna; Icaro: fumeria), eco cond restricted to Lune V-VI via the eco's `cond` (`CAL_SEQUENZA[cal_idx][0] in (5, 6)`). Add `<id>_esito` to `CONSEGUENZE_VARS`.
- `icaro_febbre`: if `player_gender == "m"`, Bro lines (same choices).

- [ ] **Step 1:** Add test in `tests/test_calendario.py`: for each new id, registry entry exists in the route's eventi file, `luna_min` in 2..4, its `cond` text contains the predecessor id and `scelta_cuore`, and no other `cond` in `game/` mentions the new id. Run → FAIL.
- [ ] **Step 2:** Add registry entries, FATTI, ECHI, defaults.
- [ ] **Step 3:** Load `writing-vn-scenes`; write the 4 scenes (35-45 lines, one menu, ±1 affinity max on at most one option) and 4 eco labels (2-5 lines).
- [ ] **Step 4:** Run tests → PASS. `tests/test_ordine_init.py`: update BASELINE only by appending the new EV ids where they now appear (print diff, confirm only additions).
- [ ] **Step 5:** Checkpoint incl. lint.

### Task 8: Two new scenes for Ofelia

Same as Task 7 for Ofelia: ids `specchio_ofelia` (after `ofelia_ev1`, `luna_min` 2), `ballo_pretendenti` (after `ofelia_ev2`, `luna_min` 3). Ids must **not** start with `ofelia_`, no `"scade"` key (spec). Eco `luoghi`: `("corte",)`. Extend the Task 7 test with these ids plus: id does not start with `ofelia_` and entry has no `scade`.

### Task 9: Overheard conversations

**Files:**
- Create: `game/routes/origliati.rpy`
- Modify: `game/conseguenze_logic.py` (pure function)
- Test: `tests/test_conseguenze.py`

**Interfaces:**
- `origliato_ok(visti: set, congelate: set, luna: int, a: str, b: str, primi: dict) -> bool` in `conseguenze_logic.py`. True iff `2 <= luna <= 4`, `primi[a] in visti`, `primi[b] in visti`, not both `a` and `b` in `congelate`, and scene id `"orig_" + "_".join(sorted((a, b)))` not in `visti`.
- `PRIMI_ORIGLIATI = {"caino": "caino_cap1", "druso": "druso_ev1", "ofelia": "ofelia_ev1"}` in `origliati.rpy`.
- Scene ids/labels: `orig_caino_druso`, `orig_caino_ofelia`, `orig_druso_ofelia`. The first two are `ECO_DOPO_LABELS` entries `("registri", "orig_caino_druso")` and `("corte", "orig_caino_ofelia")`; each label takes `att_id`, returns at once unless `origliato_ok(...)`, else adds its id to `eventi_visti` and plays. The third is an `EVENTI` invite with `"ritratto": "vanna"`, `"char": None`, `luna_min` 2, `cond` calling `origliato_ok` (luna from `v` — add `"luna"` to `cal_vars()` in `calendario.rpy` if missing).
- Each scene: ≥2 line variants keyed on `fatti_noti`/route vars; a congelata variant when one of the two froze you out; one fact each (`fx_orig_*`); one eco each in ECHI. `orig_caino_ofelia`: menu avvicinarti / andartene; "andartene" sets `orig_caino_ofelia_esito = "via"` (fact "Hai scelto di non sentire"); being caught depends on state (e.g. `caino_trappole >= 2` or `ofelia_mancati >= 1`), never random.
- Add `orig_*_esito` vars to `CONSEGUENZE_VARS`.

- [ ] **Step 1:** Tests for `origliato_ok`: Luna 1 → False; Luna 5 → False; one `primi` missing → False; both congelate → False; one congelata → True; already in visti → False; happy path Luna 3 → True. Run → FAIL.
- [ ] **Step 2:** Implement `origliato_ok`. Run → PASS.
- [ ] **Step 3:** Load `writing-vn-scenes`; write `origliati.rpy` (3 scenes, 3 ecos, registry, FATTI). Speakers say only what they can know (spec anti-goal).
- [ ] **Step 4:** Update `tests/test_ordine_init.py` BASELINE (additions only). Checkpoint incl. lint.

### Task 10: Option-rename compatibility

**Files:**
- Modify: `game/conseguenze_logic.py`, `game/conseguenze.rpy`
- Test: `tests/test_conseguenze.py`

**Interfaces:**
- `OPZIONI_RINOMINATE: dict[str, str]` (old → new), empty until Task 11.
- `rinomina_firma(firma: str, mappa: dict) -> str` — renames the part after `|` if it is a key.
- `migra_storico(scelte: dict, viste: dict, scelte_storiche: set, mappa: dict) -> None` — in place: renames firme and option texts in all three; merges `viste` lists without duplicates, keeping first-seen order.
- In `conseguenze.rpy`: call `migra_storico` on `persistent.*` once at init (after `persistent` is available) and on `store.scelte_partita` via `config.after_load_callbacks.append(...)` (pattern: `borsa.rpy:102`).
- If any `FATTI` cond uses `_scelto(v, contesto, prefisso)` with a prefix that Task 11 changes, the prefix must still match the new text (test in Task 11).

- [ ] **Step 1:** Tests with a sample map `{"Prenderla": "Prendere la lama"}`: firma renamed; viste merged without duplicates when both old and new present; scelte_storiche pair renamed; empty map is a no-op; idempotent on second call. Run → FAIL.
- [ ] **Step 2:** Implement. Run → PASS. Checkpoint.

### Task 11: Clearer options — audit, approval, apply

**Files:**
- Create: `docs/superpowers/specs/2026-10-22-audit-scelte.md`
- Modify: `.rpy` menus listed in the approved audit; `game/conseguenze_logic.py` (`OPZIONI_RINOMINATE`)
- Test: `tests/test_conseguenze.py`

- [ ] **Step 1:** List every menu option (`grep -rn -E '^\s+"[^"]+"( \(.*\))?( if .*)?:\s*$' game --include=*.rpy`). Apply the spec §12 criterion. Write the audit table: `file:line | opzione attuale | contesto (1 riga) | proposta`. Exclude «» lines, climax/finali menus (unless truly opaque), and keep paired `if` variants together.
- [ ] **Step 2:** **Stop and ask the user to approve the table.** Apply only approved rows.
- [ ] **Step 3:** Edit option text only. Fill `OPZIONI_RINOMINATE` with exactly the applied rows.
- [ ] **Step 4:** Test: every key of `OPZIONI_RINOMINATE` no longer appears as an option in `game/**/*.rpy`, every value does; every `_scelto(..., "<prefix>")` prefix in `game/` still prefixes some option in its context file. Run → PASS.
- [ ] **Step 5:** Checkpoint.

### Task 12: Wrap-up

- [ ] **Step 1:** `py -3 esporta_dialoghi.py` → `dialoghi/` regenerated; new files appear under their routes.
- [ ] **Step 2:** All tests green, lint clean.
- [ ] **Step 3:** Manual (ask the user, or run via skill `run`): load an existing save from `game/saves`; open Trama; start a run to Luna II and confirm the new invites show.
- [ ] **Step 4:** Add a release note line (README or changelog where versions are noted) about mid-scene saves in Druso/Icaro/Ofelia restarting from the nearest point.
- [ ] **Step 5:** Report to the user; offer a commit (do not commit unasked).
