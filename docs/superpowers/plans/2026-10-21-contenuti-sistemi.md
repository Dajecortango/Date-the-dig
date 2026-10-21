# Contenuti, sistemi, UI e test — piano

> Richiesta utente: punti 1, 6, 7, 8, 10, 12, 13, 14, 15, 16, 17, 18, 20, 21,
> 30, 31 della lista di consigli. Design del builder (domande saltate).
> Branch `feat/route-ofelia`, niente commit.

**Verifica di ogni blocco:** `py -3 -I tests/test_calendario.py` → `tutti i casi ok`;
`py -3 -I tests/test_routing.py` → `6/6 scenari ok` (o più scenari dopo il
Blocco E); `"./tools/renpy-8.3.7-sdk/renpy.exe" . lint` senza errori.
Regole: `.claude/skills/writing-vn-scenes/SKILL.md`,
`.claude/skills/character-sim/SKILL.md`, `.claude/skills/game-brainstorm/SKILL.md`.
Canone: `docs/lore.md` (dopo il Blocco A). Asset: solo esistenti o generati in
PIL da `make_gui.py`. Niente `git commit/add/stash`. Pulire `__pycache__/`,
`errors.txt`, `traceback.txt`, script temporanei.

Eventi fissi già occupati (non riusare): I/1 sera, II/8 sera, III/10 pomeriggio,
IV/28 sera, V/6 sera, V/14 sera, V/20 sera, V/20 pomeriggio, V/26 pomeriggio,
V/26 sera, VI/5 pomeriggio, VI/5 sera, VI/12 sera, VI/21 sera.

---

## Blocco A — Canone (punto 1)
`docs/lore.md`: mondo (Yr, Nord, Rocca Tempesta, Zefiro, Calà, Famiglia
Dignitas, Ceppi/Rami/Autarchi/Arconti, Virtù, giuramento e nome di prima,
TESCHIO), personaggi canonici e comprimari, e una sezione "Dettagli introdotti
nelle scene" che elenca con file:label ciò che è stato inventato in scena
(Ottone, Lisandro del Ramo di Iperione, Teucro e Milone del Ramo di Vittoria,
Ascadeo e il libro delle scommesse, il fiore blu di Glauco, la stanza delle
sorelle, la pagina col sigillo del drago e "Proprietà del defunto", il gatto
Lisandro di Druso, ecc.), marcando le incoerenze trovate. Solo lettura del
codice + un file di docs.

## Blocco B — Storia (punti 6, 7, 8, 10, 13)
- **6 Lenora e Pandora:** evento fisso comune "L'udienza di Lenora" su
  **III/16 sera** (nuovo file `game/routes/lenora.rpy`): la Capofamiglia riceve
  i Figli adottivi dell'anno; Caino, Druso e Icaro presenti; Pandora in
  cameo. Battute che cambiano in base a chi frequenti di più. Sprite: niente
  per Lenora/Pandora (voce e narrazione), i figli con i loro sprite. 0 punti.
- **7 Incroci:** 3 scene nuove in `game/routes/incroci.rpy` tra personaggi
  (Druso+Icaro, Aede+Ofelia, Caino+Ofelia), agganciate al calendario come
  quelle esistenti in quel file (leggerlo per lo schema). 0 punti.
- **8 Bro di Icaro:** 2 scene solo per protagonista uomo in
  `game/routes/icaro_route.rpy` (affari insieme, un colpo da ladri), inviti
  `char: icaro` con cond `player_gender == "m"` e catena di prerequisiti. 0 punti.
- **10 Epilogo:** in `game/routes/snodi.rpy`, dopo il climax in `ev_luna6`,
  `call epilogo_semestre`: "Luna VII", breve, una riga per ogni personaggio
  non scelto in base alla sua affinità/congelamento, e una per la route attiva.
  Prima della fine, nessun nuovo finale in galleria.
- **13 Rivalità:** evento fisso **IV/18 sera** in `snodi.rpy`: se almeno due
  candidati sono sopra la soglia della scelta del cuore, scena di tensione tra
  i due più alti (varianti per coppia, generica come fallback). 0 punti.

## Blocco C — Sistemi (punti 12, 15, 16, 17)
- **15 Scudi:** `default scudi = 5`. Si guadagnano: registri +2, commissioni in
  città +1, eventi casuali (vedi 17) ±; si spendono: taverna (offrire un giro,
  -1, cambia il testo), mercato (regali). Mostrati solo nel diario
  ("Borsa: N Scudi") e nel pianificatore in piccolo. File `game/economia.rpy`.
- **16 Regali:** nuova attività pomeriggio "Il mercato coperto" (`citta`
  resta): compri un oggetto tra 3-4 (costo 2-4 Scudi). Ogni personaggio
  (Aede, Caino, Ofelia, Druso, Icaro) ha un oggetto preferito e uno detestato
  (dal profilo). Dono: alla successiva scena di territorio/evento del
  personaggio, prompt "Dare il regalo?" → reazione scritta; preferito +1,
  detestato -1, neutro 0; **al massimo un regalo con punti per personaggio
  per semestre** (flag). Per non cambiare la difficoltà, alza di 1 la soglia del
  good end di ogni route (Aede 12→13 in `aede_finali.rpy`, Caino 12→13,
  Druso 15→16, Icaro 12→13, Ofelia 11→12) e aggiorna `test_routing.py` /
  `check_economia_punti`. Soglie della scelta del cuore invariate.
- **12 Varianti attività:** le scene di territorio esaurite oggi mostrano una
  riga fissa (`CAL_FALLBACK`): sostituiscila con varianti brevi che cambiano
  in base all'affinità del personaggio del territorio (bassa/media/alta), 0 punti.
- **17 Eventi casuali in città:** l'attività "Commissioni in città" pesca,
  oltre al pool una-tantum, da 6 piccoli eventi casuali (`renpy.random`,
  rollback-safe), ognuno una volta sola: borseggiatore, mercante truffato,
  rissa, ritrovamento, ecc.; ±Scudi, 0 affinità.

## Blocco D — UI (punti 14, 18, 30, 31)
- **14 Cronache (enciclopedia):** screen "Cronache" (dal diario e dal menu
  di gioco): voci su personaggi, luoghi, Ceppi, sbloccate quando l'evento/label
  che le rivela è visto (`eventi_visti` o `renpy.seen_label`); voci da
  `docs/lore.md`. File `game/cronache.rpy`.
- **18 Nuova partita+:** (a) scelte già fatte in partite precedenti con un
  segno discreto (Ren'Py `i.chosen` nella screen `choice`); (b) se il prologo
  è già stato visto (persistent), all'inizio offri "Salta il prologo"
  impostando lo stato come dopo lo Svelo; (c) con almeno un finale sbloccato,
  1-2 righe extra in punti chiave (es. scelta del cuore: Vanna nota il déjà-vu).
- **30 Effetti di scena:** overlay di particelle che si attiva in base allo
  sfondo mostrato (`renpy.showing("bg ...")`): neve su `esterno_neve`, lanterne
  che salgono su `cala_notte`, fumo leggero su `vicoli_zefiro` di sera, polvere
  dorata su `sala_svelo`. Rispetta `mm_movimento_ridotto()`. File `game/effetti.rpy`.
- **31 Menu rapido:** icone grandi a sigillo (PIL) al posto del testo piccolo,
  con tooltip in italiano; stesse azioni.

## Blocco E — Test (punti 20, 21)
- Estrai la logica pura che oggi vive solo in .rpy dove serve per testarla
  (es. condizioni di routing dei finali di Ofelia/Druso/Icaro, `cuore_opzioni`,
  scadenza degli inviti, regali) in moduli Python puri sotto `game/`
  (come `calendario_logic.py`), usati dal gioco e dai test.
- Test di comportamento in `tests/`: scadenza inviti (conteggio, congelamento a
  2, id non di Ofelia ignorati), opzioni della scelta del cuore e risoluzione
  della coppia, routing dei finali di Ofelia/Druso/Icaro/Bro, limite dei
  regali, eventi casuali una-tantum.
- `tests/test_routing.py`: scenari per Ofelia (sola, +Caino, +Aede, tempesta),
  Druso, Icaro (romance e Bro).
