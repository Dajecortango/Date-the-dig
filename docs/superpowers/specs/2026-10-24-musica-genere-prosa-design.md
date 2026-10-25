# Musica, accordo di genere, prosa — pacchetto 3 (design)

Data: 2026-10-24. Stato: approvato dal committente ("9,10,11,12,13,29,31,
inoltre voglio che quando un personaggio si riferisce al protagonista i verbi
cambino a seconda se e' un uomo o una donna").

## Vincoli

- Nessun cambio di logica di gioco: calendario, affinita', economia intatti.
- Testi: cambiano solo dove serve l'accordo di genere (tutto il gioco) e nel
  pass di prosa su `aede_atto1.rpy` (punto 29): stesse scelte, stessi label,
  stessi fatti/variabili toccati.
- Audio segnaposto sintetici (convenzione del progetto), sostituibili con gli
  stessi nomi file. Script ElevenLabs pronto per generare le versioni vere
  (serve `ELEVENLABS_API_KEY`).
- Tutto il nuovo audio rispetta skip (`renpy.is_skipping()`) e i cursori del
  mixer; la musica usa il canale `music` standard (cursore gia' nelle
  Preferenze).

## Musica (9, 12, 13)

- Nuovo campo `musiche` del capitolo (capitoli_logic.py): nome -> file ogg.
  Malandrini: `aede`, `caino`, `druso`, `icaro`, `ofelia` (leitmotiv per
  route), `calendario` (pianificatore e attivita'), `finale` (climax e
  finali). File in `game/audio/malandrini/tema_<nome>.ogg`.
- `game/musica.rpy` (comune): `musica(nome)` suona il tema del capitolo con
  dissolvenza incrociata (fadein/fadeout 2.0 — punto 12); se il tema e' gia'
  in onda o il file manca, non fa nulla. `musica_stop(fadeout)` ferma.
  `musica_silenzio()` = stop rapido (1.0) per il silenzio pilotato (13).
  Al menu principale la musica si spegne (callback come audio.rpy).
- Aggancio centrale nel calendario (cal_loop): prima del pianificatore
  `musica("calendario")`; quando parte un evento con `char` che ha un tema,
  `musica(char)`; eventi senza char non cambiano la musica.
- Climax (13): nei file `*_finali.rpy`, `musica("finale")` all'inizio del
  climax e `musica_silenzio()` 2-3 battute prima del momento chiave; il tema
  riparte sul finale scelto.

## Effetti e sting (10, 11)

- `affetto_su/giu.ogg` gia' agganciati in feedback.rpy: si rigenerano come
  sting musicali (2 note su / 2 note giu'، stessa scala del tema calendario).
- `make_musica_elevenlabs.py` (radice): con `ELEVENLABS_API_KEY` genera i 7
  temi (music API) e rigenera gli effetti (sound effects API): moneta,
  sigillo, campana, lama, colpo, carta, scelta, affetto_su, affetto_giu.
  Converte in ogg con lo stesso ffmpeg di make_audio.py. Senza chiave lo
  script spiega come fare login (`npx -y @elevenlabs/cli@latest onboard init`).

## Accordo di genere (richiesta nuova)

- Meccanismo esistente: `[fin]` (-o/-a) + variabili in protagonista.rpy.
  Si aggiungono le varianti mancanti che escono dall'audit (es. `signore_t`).
- Audit su tutti i `.rpy` del capitolo: participi/aggettivi al maschile
  rivolti al protagonista ("sei arrivato", "ti credevo pronto", "benvenuto",
  vocativi "ragazzo/amico") -> `[fin]` o variabile.
- `tests/test_genere.py`: scanner dei pattern sospetti (seconda persona +
  participio/aggettivo in -o) con whitelist esplicita per le battute rivolte
  a personaggi maschili (Caino, Druso, Icaro, ecc.).

## Prosa (29)

- Pass "grade A" (skill writing-vn-scenes) su `aede_atto1.rpy`: prologo e
  capitoli 1-3. Nessun cambio a label, menu, variabili, fatti.

## Lore (31)

- `tests/test_lore.py`: grafie canoniche da docs/lore.md (Cala', Svelo,
  Ceppo, nomi propri, Lune) cercate nei `.rpy`: grafie sbagliate = FAIL.
- Fix delle incoerenze trovate.
