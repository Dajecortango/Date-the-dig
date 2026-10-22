# Estetica e animazioni (pacchetto 2) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Breathing, ground shadows, Druso's landing, living firelight, new context particles, storm snow, canal glints, slower intimate text, animated day card, flying coins, and hand-placed `muovi`/`ricordo`/`lento` where they make sense.

**Architecture:** Pure rules and numbers in `game/regia_logic.py` (tested by `tests/test_regia.py`); Ren'Py wiring extends the existing systems: `luce_personaggio`/`fondo_fx`/`_lu_definisci_sprite` (`game/luce.rpy`), `effetti_scena` (`game/effetti.rpy`), helpers in `game/regia.rpy`, `borsa_hud` (`game/borsa.rpy`), `cartello_data` (`game/calendario.rpy`), assets from `make_gui.py`.

**Tech Stack:** Ren'Py 8.3.7, Python 3, PIL (make_gui.py).

**Spec:** `docs/superpowers/specs/2026-10-22-estetica-animazioni-design.md` — read it first.

## Global Constraints

- Scene text never changes; only regia lines are added (`$ muovi(...)`, `with ricordo`, `$ lento()`, `$ tempesta()`).
- Everything off with "Animazioni: No" (`mm_movimento_ridotto()`) and while skipping (`renpy.is_skipping()`).
- `renpy.variant("small")`: new particle counts halved; breathing redraw 15 fps instead of 30.
- Visual state outside the store (NoRollback classes), never saved.
- Commits: the user asks for them explicitly; do not commit unless asked.
- Every task ends green: `for f in tests/test_*.py; do py -3 -I "$f" > /dev/null || echo "FAIL $f"; done` (no output) and `powershell -File lint.ps1` clean.

## Review Focus

1. Android performance with breathing + particles + flicker together (one redraw loop per sprite): expect no visible stutter on `small`.
2. "Animazioni: No" mid-scene: every new effect stops at once, sprites at rest (zoom 1, no offset).
3. Rollback/load during a coin flight or day-card flip: no stuck overlay, counter shows the real value.
4. `scene` after `tempesta()`/`lento()`: both reset; a load mid-scene does not leave text slow forever.
5. Druso entering while already on screen with another tag change (expression swap) must not re-trigger `tonfo`.

---

### Task 1: Pure rules in regia_logic

**Files:** Modify `game/regia_logic.py`; Test `tests/test_regia.py`

**Interfaces (Produces):**
- `MOVIMENTI`: `furia`, `furioso`, `minaccioso` → `"trema"` (others unchanged).
- `RESPIRO_AMPIEZZA = 0.006`, `RESPIRO_PERIODO = 4.2`; `respiro(t: float, fase: float) -> float` zoom in [1.0, 1.006]; `fase_per(tag: str) -> float` in [0, 1), deterministic, differs for aede/caino/druso/icaro/ofelia.
- `FUOCO = ("studio_glauco", "corridoio_ceppo", "cala_notte")` plus `vicoli_zefiro` only at "sera"; `fuoco_per(bg, slot) -> bool`; `fiamma(t: float) -> float` in [0.97, 1.03], sum of 2–3 sines 0.3–0.8 Hz; `velo_fuoco(t) -> float` alpha in [0.02, 0.06] from the same noise.
- `EFFETTI_CONTESTO = [(contesto, bg, effetto, modo)]` with rows: (`"corte"`, `"sala_svelo"`, `"foglie"`, `"sostituisci"`), (`"fumeria"`, `"vicoli_zefiro"`, `"fumo_pipa"`, `"sostituisci"`), (`"athlion"`, `"arena_athlion"`, `"scintille"`, `"aggiungi"`), (`"ofelia_ev3"`, `"arena_athlion"`, `"scintille"`, `"aggiungi"`). Builder confirms ids (`cal_contesto` values) by grep and adds Icaro fumeria event ids that open on `vicoli_zefiro` in fumeria.
- `effetti_per(bg: str|None, slot: str|None, contesto: str|None, piove: bool, tempesta: bool) -> tuple[str, ...]`: base effect from the existing `EFFETTI_SFONDI` rules (move that table into regia_logic as `EFFETTI_SFONDI` with same rows; effetti.rpy then reads `rgl.EFFETTI_SFONDI`), `neve` → `neve_fitta` when `tempesta`, `vicoli_zefiro` adds `luccichii` unless `piove`, then apply first matching `EFFETTI_CONTESTO` row (sostituisci replaces base, aggiungi appends). Order of tuple = draw order.
- `monete_per(delta: int) -> int`: delta 0 → 0; +1..+2 → 2; +3..+5 → 3; +6..+9 → 4; ≥10 → 5; negative: −1..−2 → 1, −3..−5 → 2, ≤−6 → 3.
- `LENTO_CPS = 0.7`.

- [ ] **Step 1:** Add tests: MOVIMENTI furia→trema, rabbia still avanza; respiro(0, 0)==1.0, max over a period ≤ 1.006+1e-9 and ≥ 1.0059; fase_per distinct for the 5 tags; fiamma within bounds over 0..30 s step 0.05 and |fiamma(t+0.05)-fiamma(t)| < 0.01; velo_fuoco within bounds; fuoco_per(vicoli, "sera") True / ("mattina") False; effetti_per cases: (`esterno_neve`, …, tempesta=True) → `("neve_fitta",)`; vicoli sera → `("fumo", "luccichii")`; vicoli rain → `("pioggia",)`; corte+sala_svelo → `("foglie",)`; ofelia_ev3+cala_notte → `("lanterne",)` (context ignored on other bg); athlion+arena → `("nevischio", "scintille")`; fumeria+vicoli sera → `("fumo_pipa", "luccichii")`; unknown bg → `()`. monete_per table above. Run → FAIL.
- [ ] **Step 2:** Implement. Run → PASS. Full suite green.

### Task 2: Sprites — breathing, firelight, trema/muovi, Druso tonfo, shadow

**Files:** Modify `game/luce.rpy`, `game/regia_logic.py` (if a helper is needed), `make_gui.py`; Test `tests/test_regia.py` (grep checks)

**Interfaces:**
- `luce_personaggio(tag)`: zoom = movement zoom × `rgl.respiro(time, rgl.fase_per(tag))` (respiro 1.0 when fermo/skipping); tint brightness × `rgl.fiamma(time)` when `rgl.fuoco_per(bg, slot)`; return redraw `1/30` (`1/15` on small) instead of 0.1 when breathing is active.
- `_lu_curva` gains `"tonfo"`: yoffset `+10*s` then back, zoom `1.0 + 0.02*s` (s = sin(pi*k)).
- Druso: in `_lu_interazione`, when `"druso"` is in scene now and was not in the previous interaction's scene set, set `_lu.mov["druso"] = ("tonfo", now + 0.3)` (start after the 0.3 s slide; `_lu_movimento` treats a future start as not yet moving). Track previous set in `_LuceStato` (`self.presenti`).
- `muovi(tag: str, nome: str) -> None` (global, in luce.rpy): no-op if fermo/skipping/tag not shown; respects `rgl.MOVIMENTO_PAUSA` like automatic moves.
- Shadow: `make_gui.py` new function `ombra_sprite()` → `game/gui/ombra_sprite.png` 520×70, black ellipse alpha ~0.35 Gaussian-blurred, called from the main build list. In `_lu_definisci_sprite`, non-bg images become `Fixed(Transform("gui/ombra_sprite.png", xalign=0.5, yalign=1.0, yoffset=35), At(fn, luce_personaggio(tag)), xysize=renpy.image_size(fn))` (shadow first = behind; not tinted). If `renpy.image_size` at init is unavailable, read size with the file's header via `renpy.loader` + PIL-free fallback: ruling + ledger.
- `fondo_fx`: when `rgl.fuoco_per(bg, slot)` and not fermo, add a warm `#ffb066` layer with alpha `rgl.velo_fuoco(t)` behind sprites (e.g. `trans.matrixcolor` brightness tint on the bg, or composite); keep redraw 1/30 while active.

- [ ] **Step 1:** Grep tests: `"tonfo"` in `_lu_curva`; `def muovi(` in luce.rpy; `rgl.respiro(` and `rgl.fiamma(` in luce.rpy; `ombra_sprite.png` in luce.rpy and `def ombra_sprite` in make_gui.py; `rgl.velo_fuoco(` in luce.rpy. Run → FAIL.
- [ ] **Step 2:** Implement; run `py -3 make_gui.py` (regenerates gui; confirm `git status game/gui` shows only `ombra_sprite.png` added/changed, else ruling). Tests PASS, lint clean.
- [ ] **Step 3:** Manual feel note in ledger: what cannot be judged from code (breathing amplitude, shadow look).

### Task 3: Particles — foglie, fumo_pipa, scintille, luccichii, neve_fitta, tempesta()

**Files:** Modify `game/effetti.rpy`, `game/regia.rpy`, `make_gui.py`, `game/routes/aede_finali.rpy` (one line); Test `tests/test_regia.py`

**Interfaces:**
- `make_gui.py` `particelle_effetti()` adds `fx_foglia.png` (leaf/petal, ~22×14, green and a pink variant may be a tint), `fx_scintilla.png` (~10×10 bright gold core), `fx_luccichio.png` (~14×6 soft white streak).
- Fabbriche: `foglie` (SnowBlossom slow fall, slight drift, rotation not available → two sizes), `fumo_pipa` (denser/lower than `_fx_fumo`: count ~12, yspeed −14..−6, alpha 0.4), `scintille` (upward fast, few: count 10), `luccichii` (horizontal=True slow drift in bottom quarter: use a Fixed with yalign 1.0 ysize 270 container), `neve_fitta` (≈2× `_fx_neve` counts, faster, plus `Solid("#ffffff", alpha 0.04)`). Counts halved on small.
- `effetto_corrente()` returns tuple from `rgl.effetti_per(bg, slot, store.cal_contesto, piove_ora(), store.regia_tempesta)`; `effetto_displayable` caches by tuple and composes a `Fixed` of the factories in order.
- `regia.rpy`: `default regia_tempesta = False`; `tempesta()` sets True; `_regia_scene` also sets it False.
- `aede_finali.rpy` `label climax`: `$ tempesta()` on the line after `scene bg esterno_neve with fade`.

- [ ] **Step 1:** Grep tests: factories registered for the 5 names in `FX_FABBRICHE`; `rgl.effetti_per(` used in effetti.rpy; `regia_tempesta = False` reset in `_regia_scene`; `$ tempesta()` in `climax`; make_gui generates the 3 images. Run → FAIL.
- [ ] **Step 2:** Implement; `py -3 make_gui.py`; tests PASS; lint clean.

### Task 4: lento()

**Files:** Modify `game/regia.rpy`; Test `tests/test_regia.py`

**Interfaces:** `default regia_lento = False`; `lento()` / `fine_lento()`; `_regia_scene` resets it; `config.say_arguments_callback` (chain any existing one) adds `what_slow_cps_multiplier=rgl.LENTO_CPS` to kwargs when `store.regia_lento` and not `mm_movimento_ridotto()`... (lento is pacing, not motion: keep it active regardless of Animazioni — Ruling allowed if builder disagrees). Verify in 8.3.7 by grepping the SDK (`tools/renpy-8.3.7-sdk/renpy/character.py` for `slow_cps_multiplier` / `what_` kwargs handling); if unsupported, fallback `config.say_menu_text_filter` prepending `{cps=*0.7}` only for say (ledger ruling).

- [ ] **Step 1:** Grep tests: `def lento(`, reset in `_regia_scene`, `say_arguments_callback` wiring present. Run → FAIL. **Step 2:** Implement → PASS, lint.

### Task 5: Day card

**Files:** Modify `game/calendario.rpy` (screen `cartello_data` + its call site + transforms); Test `tests/test_calendario.py` or `tests/test_regia.py` (grep)

**Interfaces:** `screen cartello_data(luna, giorno, festa=False, giorno_prec=None, luna_prec=None)`; call site passes previous day/luna from `cal_ultimo_giorno` before it is overwritten (read it first). Number flip: old number text with transform `giorno_esce` (ease-out 0.35 s, yoffset 0→−24, alpha 1→0), new with `giorno_entra` (yoffset 24→0, alpha 0→1), both inside a clipped `fixed` (xysize to the text line). Only when `giorno_prec` is not None and differs; otherwise static. New Luna (`luna_prec` not None and `luna_prec != luna`): above the name, `gui/luna_<luna_prec>.png` dissolves into `gui/luna_<luna>.png` (0.6 s) with a small gold glow, then stays. All static with Animazioni No / skipping.

- [ ] **Step 1:** Grep tests: screen signature has `giorno_prec`, `luna_prec`; transforms `giorno_esce`, `giorno_entra` exist; call passes them. Run → FAIL. **Step 2:** Implement → PASS, lint.

### Task 6: Flying coins

**Files:** Modify `game/borsa.rpy`; Test `tests/test_regia.py` (grep) — numbers already tested in Task 1.

**Interfaces:** On a scudi change detected in `_bo_controlla` (delta ≠ 0, not rollback, not fermo/skipping): `_bo.volo = (rgl.monete_per(delta), sign, start_time)`. New overlay screen `borsa_monete` (zorder 56, in `config.overlay_screens`) shows `n` coins (`gui/scudo.png` zoom 0.45): gain → from (960, 900) along an arc to the pill (x ≈ 1920−28−pill width/2, y ≈ 44), stagger 0.06 s, flight 0.55 s ease-in-out (ATL `ease` on xpos/ypos + a mid-flight `yoffset` arc via two-stage ease); loss → from the pill falling 120 px and fading 0.5 s. Counter start (`_bo.t0`) delayed by 0.55 s on gains so it ticks when the first coin lands. Screen hides itself after the last coin (timer). Reset on load/rollback (`_bo_reset`).

- [ ] **Step 1:** Grep tests: `rgl.monete_per(` in borsa.rpy; `screen borsa_monete` and its overlay registration; reset clears `volo`. Run → FAIL. **Step 2:** Implement → PASS, lint.

### Task 7: Scene pass — muovi, ricordo, lento

**Files:** Modify scenes under `game/routes/` (regia lines only); Test `tests/test_regia.py`

- [ ] **Step 1:** Load skill `writing-vn-scenes`. Criteria (spec §1, §3, §29):
  - `$ muovi(tag, nome)`: physical gesture in text without expression change; ≤ 1 per ~10 lines per character; never on a line adjacent to `vpunch`/`hpunch`; tag must be on screen.
  - `with ricordo`: only where the narrator relives a past moment (flashback), not gossip echoes.
  - `$ lento()`: impegni (scelta del cuore), confession beats of climaxes, good and passeggero endings; placed right before the first slow line; relies on `scene` reset (add `$ fine_lento()` if the slow stretch ends mid-scene).
- [ ] **Step 2:** Test: every `muovi("x", ...)` line's tag x is shown earlier in the same label (simple scan: a `show x` before it in the label body); every `muovi` name is one of sobbalzo/arretra/avanza/trema/tonfo; `lento()` present in each `impegno_*` label. Run → FAIL before edits.
- [ ] **Step 3:** Edit scenes. Record the list (file:label, what) in the ledger. Tests PASS, lint clean; `py -3 esporta_dialoghi.py` (regia lines are not dialogue; output must be unchanged except none).

### Task 8: Wrap-up
- [ ] Full suite + lint. Regenerate `dialoghi/` (expect no change). Report to the user with the feel-check list (things only visible in play: breathing amplitude, shadows, firelight, coins, day card, Android fps) and offer a commit.
