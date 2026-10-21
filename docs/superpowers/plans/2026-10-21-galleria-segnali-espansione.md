# Galleria finali, segnali al giocatore, espansione Druso/Icaro — piano

> Utente: "parti subito e finisci le task" (domande saltate). Le scelte di
> design qui sotto sono del builder. Branch `feat/route-ofelia`, niente commit.

**Goal:** (6) galleria dei finali persistente con indizi; (4) segnali diegetici
per le meccaniche nascoste; (2) Druso e Icaro più lunghi e con più peso.

**Verifica di ogni task:** `py -3 -I tests/test_calendario.py` → `tutti i casi ok`;
`py -3 -I tests/test_routing.py` → `6/6 scenari ok`;
`"./tools/renpy-8.3.7-sdk/renpy.exe" . lint` senza errori.
Regole: `.claude/skills/writing-vn-scenes/SKILL.md`, `.claude/skills/character-sim/SKILL.md`.
Niente `git commit/add/stash`.

---

### Task A: Galleria dei finali (punto 6)

**Files:** Create `game/finali_galleria.rpy`; Modify `game/screens.rpy`
(navigation: bottone "Finali" solo nel main menu, accanto a "Load"), ogni label
di finale (sotto); Test `tests/test_calendario.py` (`check_galleria_finali()`).

- `FINALI`: lista di tuple `(id, titolo, route, indizio)` in `init python`, una
  per finale. 22 finali oggi:
  - aede: `good_end`, `neutral_end`, `bad_end_aede`, `bad_end_glauco`
  - caino: `caino_good_end`, `caino_secret_end`, `caino_bad_end`, `caino_neutral_end`
  - druso: `druso_good`, `druso_neutral`, `druso_bad`
  - icaro: `icaro_good`, `icaro_neutral`, `icaro_bad`, `icaro_bro_end` ×2 (id
    `icaro_bro_listino`, `icaro_bro_conti`: due cartelli nello stesso label)
  - ofelia: `ofelia_good`, `ofelia_good_caino`, `ofelia_good_aede`,
    `ofelia_bad_tempesta`, `ofelia_neutral`
  - semestre: `finale_neutro_semestre`
  `titolo` = testo del cartello `centered` (es. "IL CUORE PROVOCATORE");
  `indizio` = una riga in italiano che orienta senza spoilerare la condizione
  esatta (es. "Tienigli testa fino al Consiglio, e non tirarti indietro sulle mura.").
- `default persistent.finali_visti = set()`; `sblocca_finale(fid)` aggiunge e
  chiama `renpy.save_persistent()`.
- Ogni label di finale chiama `$ sblocca_finale("<id>")` subito prima del
  `centered` del cartello.
- Screen `galleria_finali` (`tag menu`, `use game_menu(_("Finali"), scroll="viewport")`):
  contatore "N / 22", gruppi per route; sbloccato → titolo in oro; bloccato →
  "???" + indizio in grigio.
- Test: ogni id di `FINALI` compare in esattamente un `sblocca_finale("id")` nei
  .rpy; ogni label elencato sopra contiene `sblocca_finale`; `len(FINALI) == 22`
  (aggiornare se il Task C aggiunge finali).

### Task B: Segnali al giocatore (punto 4)

**Files:** Modify `game/routes/ofelia_route.rpy`, `game/calendario.rpy`
(`diario_rapporti`), `game/routes/druso_route.rpy` (solo `druso_passo_falso`);
Create label di spiegazione in `ofelia_route.rpy`; Test `tests/test_calendario.py`.

- Primo invito di Ofelia scaduto: oltre alla notifica, una scena breve
  (`label ofelia_scadenza_prima`, 2-4 righe di narrazione + una battuta di
  Ofelia riportata da Vanna o un biglietto) chiamata con
  `renpy.call_in_new_context("ofelia_scadenza_prima")` dentro `ofelia_scadenza`,
  solo al primo mancato (`ofelia_mancati == 1`). Spiega in-world: Ofelia non
  ripete gli inviti, chi manca due volte esce dalla corte.
- Diario (`diario_rapporti`), righe condizionali che sovrascrivono il testo di
  affinità (non numeri):
  - Aede: se `route_seconda == "aede"` e `aede_sospetto >= 1` → "Ti guarda come
    si guarda un conto che non torna."
  - Ofelia: se `ofelia_mancati == 1` e non congelata → "Ha aspettato una volta.
    Non aspetterà la seconda."
  - Druso: se `player_gender == "m"` e `druso_passi_falsi == 1` e non congelato
    → "Ti ha segnato nel registro delle cose che non perdona. Una riga sola. Per ora."
- `druso_passo_falso`: al primo passo falso `renpy.notify("Druso se la segna.")`
  (se non c'è già una notifica).
- Test: le tre stringhe/condizioni presenti; label `ofelia_scadenza_prima`
  esiste e finisce con `return`.

### Task C: Espansione Druso (punto 2)

**Files:** Modify `game/routes/druso_route.rpy`, `game/finali_galleria.rpy`
(indizi), `tests/test_calendario.py`.

- Nuovo evento fisso Luna V: `{"id": "druso_luna5", "label": "druso_luna5",
  "tipo": "fisso", "char": "druso", "luna": 5, "giorno": 6, "slot": "sera",
  "cond": route_attiva == "druso" and "druso" not in congelate}`. Taverna, sfida
  di versi con un poeta rivale di un altro Ramo che umilia Druso in pubblico;
  il giocatore sceglie come stargli accanto. Menu 3 opzioni, max `+= 1`.
  Sprite: `druso` (ghigno, imbarazzato, irritato, neutro, serio, sorpreso).
- `druso_climax` riscritto più lungo (~25-35 righe): Consiglio del Ramo di
  Lenora, la madre fuori scena; il giocatore ha una scelta prima del verdetto
  (parlare per lui / lasciarlo parlare / smontare la cosa con una battuta), max
  `+= 1`, e la scelta colora il finale. Poi routing.
- Soglia good: alza di quanti punti nuovi massimi aggiungi (oggi 13 → 15 se
  +1 evento e +1 climax). Aggiorna `check_economia_punti` (stringa soglia e
  raggiungibilità).
- Finali `druso_good`, `druso_neutral`, `druso_bad`: epilogo più lungo
  (+6-10 righe ciascuno), conservando cartelli e `sblocca_finale`.

### Task D: Espansione Icaro (punto 2)

**Files:** Modify `game/routes/icaro_route.rpy`, `game/finali_galleria.rpy`
(indizi), `tests/test_calendario.py`.

- Nuovo evento fisso Luna V: `icaro_luna5` V/26 sera, cond
  `route_attiva == "icaro"` e non congelato (vale per romance e Bro).
  "La partita grossa": Icaro gioca un piatto enorme contro uomini di un altro
  Ramo; bara, e qualcuno se ne accorge. Il giocatore: coprirlo con discrezione /
  smascherare l'avversario / restare in silenzio. Max `+= 1`. Sprite icaro
  (furbo, imbarazzato, irritato, neutro, sereno, sorpreso).
- `icaro_climax` riscritto più lungo (~25-35 righe) con una scelta prima del
  verdetto, max `+= 1`; il gate di genere e il ramo Bro restano identici.
- Soglia good `icaro_affinity >= 10` → alzata dei punti nuovi (es. 12).
  Aggiorna i check in `check_economia_punti` (stringa e raggiungibilità; anche
  la scelta del cuore 7F/6M resta invariata).
- Finali `icaro_good`, `icaro_neutral`, `icaro_bad`, `icaro_bro_end`: epiloghi
  più lunghi, cartelli e `sblocca_finale` invariati.
