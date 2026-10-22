# Pacchetto "40 consigli" — punti 3-8, 10-21, 24, 30 (design)

Data: 2026-10-22. Stato: approvato dal committente ("fai 3,4,5,6,7,8,10,11,12,
13,14,15,16,17,18,19,20,21,24,30").

Vincoli che valgono per tutto (da 2026-10-22-conseguenze-design.md e dalla
spec del calendario):
- L'ordine dei capitoli delle route non cambia. Niente eventi narrativi a
  caso: ogni evento nuovo ha una `cond` esplicita sullo stato.
- Eventi a soglia/inviti nuovi solo in Lune I-IV. Date fisse esistenti intatte.
- Scene di territorio: ±1 affinità al massimo, una tantum.
- Nessuna statistica numerica visibile (gli Scudi sono denaro, non stat).
- Le scene esistenti non si riscrivono: si aggancia da file nuovi
  (registry EVENTI, FATTI, ECHI, pool delle attività, hook).

## Audio (3, 4, 5)
- `make_audio.py` sintetizza (numpy + ffmpeg) effetti e ambienti in
  `game/audio/` (ogg). Segnaposto originali, sostituibili con file veri.
- Canale `ambiente` (loop, mixer proprio) scelto dallo sfondo in scena:
  camino (corridoio, studio), vento (neve, Calà + campane), strada (vicoli),
  sala (palestra, consiglio, sala dello Svelo), folla (arena).
- Effetti: monete quando cambiano gli Scudi, lama sul `with lampo`, colpo su
  `vpunch`/`hpunch` (config.with_callback), campane alla Fiaccolata
  (ambiente della Calà).
- Preferenze: cursore "Volume ambiente" accanto a musica ed effetti.

## Avvisi unificati (24)
- Un solo canale: l'overlay del feedback (feedback.rpy). Gli avvisi delle
  conseguenze ci entrano come voce con ◆ e testo "Nella Trama: ...".
- Se nella stessa interazione lo stesso personaggio ha già una riga di
  affinità, l'avviso della conseguenza non si ripete.

## Clessidra (30)
- Inviti a scadenza (`scade`) nel pianificatore: icona `gui/clessidra.png`
  accanto al titolo e riga "Non aspetterà" nel pannello.

## Economia (18, 19, 20, 21)
- Usi degli Scudi, offerte una tantum a fine attività:
  soffiata in città (2 Scudi: il gusto di un personaggio per i doni),
  un boccale a Ottone (2: un indizio sul Ceppo di Cardia), offerta alla cassa
  degli orfani ai riti (2: fatto ripreso da Briseide), scommessa su Druso in
  palestra (1-3, l'unico caso permesso: è un azzardo dichiarato).
- Debito con Icaro: prestito in fumeria (5 Scudi, restituzione 6 entro una
  Luna e mezza). Saldato o insoluto = fatto; insoluto = Icaro -1 e eco.
  Il debito si vede nella Borsa.
- Doni: reazione propria per ogni coppia (personaggio, dono) anche nel caso
  neutro (registry `DONI_REAZIONI`).
- Ricordi che contano: tenerne uno sblocca una scena breve (eco) in cui
  mostrarlo cambia una battuta e lascia un fatto.

## Narrativa (6, 7, 8, 10, 11, 12, 13)
- Eventi reattivi (6): 3 inviti in Lune III-IV su combinazioni di fatti di
  route diverse, mai al posto di un capitolo.
- Il mondo va avanti (7): gli inviti offerti e mai presi prima della scelta
  del cuore diventano fatti ("ci è andato qualcun altro"), ripresi da echi
  in Luna V-VI e nell'epilogo.
- Più echi (8): almeno 3 per personaggio.
- Vanna e Corrado (10): arco in 3 scene (Lune II, III, V) con una scelta che
  decide il loro "un anno dopo".
- Briseide a metà semestre (13): evento fisso III/25 sera che commenta fino a
  due fatti accumulati.
- Code delle rivalità (11): nell'epilogo, se c'è stata la rivalità di IV/18 e
  uno dei due è stato scelto, una riga per chi è rimasto fuori.
- Un anno dopo (12): blocco dopo Luna VII con il destino del Ceppo e del
  mondo secondo i fatti (Vanna e Corrado, Briseide, Lenora, Zefiro).

## Minigiochi (14, 15, 16, 17)
- Quattro scene di territorio nuove, con un minigioco breve, saltabile
  ("Lascia andare": esito neutro), a pulsanti grandi per il touch:
  duello con Aede (spada: leggere il segnale, scegliere fendente/parata/finta),
  carte con Icaro (fumeria: trovare la mano truccata), registri di Caino
  (trovare la riga sbagliata), botta e risposta con Druso (taverna: risposta
  a tempo). Esito = fatto + ±1 una tantum secondo il profilo.

## Estensione (per chi aggiunge contenuti)
- `FATTI.extend`, `ECHI.extend`, `CONSEGUENZE_VARS.append` dai propri file.
- `pool_aggiungi(att_id, label, indice)` inserisce una scena nel pool di
  un'attività (init 5).
- `invito_perso(eid)`: True se l'invito è stato offerto e mai preso prima
  della scelta del cuore.
- Inviti con chiave `ritratto` per i comprimari (es. "vanna").
- `epilogo_coda`: label chiamata dall'epilogo prima della chiusura.
- `ECO_DOPO_LABELS`: label chiamate a fine attività (att_id, label).
