# Capitolo I "Malandrini" — ristrutturazione a calendario (design)

Data: 2026-10-20. Stato: in approvazione.

## Intento

Il Capitolo I passa da 5 route separate e stagne a una vita condivisa in stile
dating sim classico: il protagonista, Figlio adottivo di Briseide, vive circa
sei mesi a Rocca Tempesta giorno dopo giorno. Le giornate sono fatte delle
attività di un Dignitas — addestramento di spada e scudo, studio della storia
della Famiglia, riti e usanze del Ceppo dell'Autarca che lo ha adottato
(Briseide) — e scegliere come passare il tempo significa scegliere chi
frequentare. Le route (2 donne: Aede, Ofelia; 3 uomini: Caino, Druso, Icaro)
emergono dalla frequentazione, non da un menu iniziale.

## Scelte del committente (vincolanti)

- Durata: circa 6 mesi in-world.
- Giornata in tre slot: mattina / pomeriggio / sera. Slot senza nulla di
  saliente si saltano; giorni interi vuoti si saltano.
- Nessuna statistica numerica da coltivare (niente Spada/Scudo/Erudizione
  visibili). Resta solo l'affinità nascosta per personaggio.
- All'inizio incontri i personaggi nei loro luoghi; più avanti sono loro a
  cercarti (missioni, inviti, bevute).
- Ofelia: superato dalla spec 2026-10-21-route-ofelia-design.md.
- Lucchetti di accesso per route: come da sezione "Lucchetti" (approvati).

## Struttura temporale

- Sei "Lune" (mesi), da Luna I a Luna VI. Il calendario è elastico: si giocano
  solo i giorni salienti (2-5 per Luna), il resto è salto di tempo narrato
  ("Le settimane passano, il callo della spada cresce...").
- Date fisse del semestre (feste/eventi già scritti o da scrivere):
  - Luna I — Lo Svelo (prologo comune, scena esistente del corridoio: primo
    incontro con Aede per tutti).
  - Luna II — L'Adunanza (scena esistente: prova di Caino sul Ballo delle
    Candele Spente; è il lucchetto d'ingresso della sua route).
  - Luna III — L'Athlion (scena esistente con branch Aede; occasione anche per
    Druso, territorio palestra).
  - Luna V — La Fiaccolata della Calà. Evento fisso per tutti. Se la route
    attiva è Aede: scena cap5 esistente. Per ogni altra route attiva (Caino,
    Druso, Icaro/Bro): variante breve nuova sulla Calà, nella voce del
    personaggio (scena nuova, a budget). Nessuna route attiva: breve scena di
    atmosfera con Vanna e Corrado. [scelta del builder]
  - Luna VI — chiusura: climax della route attiva (scene esistenti per
    Aede/Caino, nuove per Druso/Icaro) o finale neutro.

## Loop di gioco

1. A inizio giorno saliente: schermata di pianificazione (screen Ren'Py) con
   gli slot del giorno e le attività disponibili per slot.
2. Attività base: addestramento di spada, addestramento di scudo/lotta,
   studio della storia della Famiglia, riti del Ceppo di Briseide (il brodo,
   gli orfani, le cucine — le scene con Vanna/Corrado/Briseide, inclusi gli
   attuali interludi), commissioni in città (Zefiro), taverna (sera),
   sala da gioco/fumeria (sera).
3. Ogni attività apre una scena breve. Se l'attività è territorio di un
   personaggio, l'incontro fa salire (o scendere) l'affinità via scelte.
4. A soglie di affinità scattano gli eventi personali: le scene di route già
   scritte (Aede cap1-6, Caino cap1-6) ricollocate sul calendario, più gli
   inviti ("Druso ti aspetta alla taverna") che appaiono come scelte speciali
   evidenziate nella pianificazione, con ritratto.
5. Ripetere un'attività già vista senza evento nuovo = variante breve o salto
   automatico. Mai la stessa scena identica due volte (anti-grind).

## Territori

| Personaggio | Dove | Quando |
|---|---|---|
| Aede | addestramento di spada | mattina/pomeriggio |
| Caino | lavoro sui registri della Proprietà (solo dopo sblocco Adunanza) | pomeriggio |
| Druso | palestra (scudo/lotta) e taverna | mattina / sera |
| Icaro | sala da gioco e fumeria | solo sera |
| Ofelia | la corte di Ofelia (serra) | pomeriggio |

## Lucchetti (approvati dal committente)

- **Aede** — accessibile a entrambi i generi dal giorno 1 (territorio: spada).
  Difficoltà media. Lucchetto a metà percorso: il cap4 esistente ("Il lavoro
  di Aede", il vicolo). Rispondere "assassinio" (`flag_accetta_lavoro=False`)
  congela la route a livello amicizia: niente eventi a soglia successivi,
  niente impegno, niente climax — il climax di Luna VI si gioca solo con
  route attiva. I bad end restano raggiungibili solo dentro la route attiva,
  con le condizioni attuali. [scelta del builder]
- **Caino** — assente dalle attività quotidiane. Ingresso: farsi notare
  all'Adunanza (data fissa, Luna II, scena esistente). "Risposta sbagliata" =
  cadere nella trappola delle Candele Spente ("Magnifica davvero",
  `caino_trappole+1`): la route non si apre per il semestre — nessun invito ai
  registri, restano solo scene scrivano senza romance. Le altre due risposte
  aprono la route. [scelta del builder] Entrambi i generi.
- **Druso** — accessibile subito, lucchetto a rovescio: affinità sale solo
  tenendogli testa colpo su colpo; cedere, minacciare o piagnucolare la fa
  scendere. Donna 4/5; uomo 5/5 (più prove, zero passi falsi ammessi).
  Route "Il cuore provocatore".
- **Icaro** — romance solo per protagonista donna; protagonista uomo sblocca
  la variante "Bro" (stessa trama, finale platonico). Ingresso doppio: solo
  di sera, e ti ignora finché non ti dimostri util[e/i] o capace di capire il
  suo mondo (es. accorgersi che bara alle carte senza smascherarlo in
  pubblico). Good ending più difficile del gioco (5/5). Possessivo: corteggiare
  altri dopo il suo evento di impegno chiude la route per sempre.
  Route "Untouchable" (nome provvisorio).
- **Ofelia** — inviti a scadenza (vedi spec 2026-10-21-route-ofelia-design.md).

## Esclusività e lock-in

- Lune I-III: fase libera, frequenti chi vuoi.
- Fine Luna IV: il personaggio sopra soglia con affinità più alta provoca
  l'evento di impegno ("scelta del cuore"): mini-scena NUOVA di raccordo, una
  per personaggio, breve, con bivio accetta/rifiuta (a budget; i cap esistenti
  non hanno questo bivio). Accettare = le Lune V-VI giocano il resto della sua
  route (scene esistenti per Aede e Caino); gli altri scalano a sfondo
  amicizia. [scelta del builder]
- Icaro per protagonista uomo: la variante "Bro" partecipa alla scelta del
  cuore come fratello giurato, occupa Lune V-VI da route attiva platonica,
  Fiaccolata inclusa (variante bro). [scelta del builder]
- Il finale segreto "Teschio" di Caino resta invariato e scatta solo dentro
  la route attiva di Caino (condizioni attuali: `caino_druso>=2`,
  `caino_fiducia<12`); con Druso route attiva non si applica. [scelta del
  builder]
- Rifiutare tutti o nessuna soglia raggiunta = finale neutro "Il semestre del
  novellino" (nuovo, breve): Briseide tira le somme, rimando al prossimo
  semestre.
- Icaro: la sua regola di possessività vale anche in fase libera dopo la sua
  soglia di interesse.

## Contenuti esistenti → destinazione

- `aede_atto1/atto2/interludi/finali`: Svelo = Luna I fisso; cap1 (consegna)
  = primo evento a soglia Aede (Luna I-II); cap2 = Athlion, Luna III fisso;
  cap3 = evento a soglia Luna III; cap4 (lucchetto) = Luna IV; impegno = fine
  Luna IV; cap5 = Fiaccolata, Luna V fisso; cap6 (giuramento) = Luna V, dopo
  la Fiaccolata; climax+finali = Luna VI. [scelta del builder, risolve la
  mappatura] Interludi = scene dei riti del Ceppo. I testi non si riscrivono:
  si ricollocano, con ritocchi di raccordo (aggancio calendario, rimozione dei
  jump rigidi cap→cap).
- `caino_atto1/atto2/finali`: Adunanza = Luna II fisso (gate); cap1-cap6 =
  eventi a soglia; climax+finali = Luna VI.
- Druso e Icaro: contenuto nuovo da scrivere seguendo i profili salvati in
  `docs/profili/druso.md` e `docs/profili/icaro.md` — incontri territorio
  (2-3 per Luna), eventi a soglia, evento di impegno, climax, 3-4 finali
  ciascuno. In più (a budget): mini-scene di impegno per Aede e Caino,
  varianti Fiaccolata per Caino/Druso/Icaro(+Bro), scena Fiaccolata neutra,
  finale neutro di semestre. Druso riusa le
  comparse già scritte (TESCHIO, taverna). Sprite non ancora disponibili:
  placeholder in stile Caino (silhouette con nome) finché non arriva l'arte.
- `chapter1.rpy` (hub `chapter_select`): sostituito dalla pianificazione a
  calendario. La scelta sesso/nome resta nel prologo comune.

## UI

- Screen pianificazione: Luna e giorno correnti, gli slot del giorno con le
  attività disponibili come bottoni (stile GUI Dignitas esistente); gli
  inviti/eventi speciali evidenziati con il ritratto del personaggio
  (ritratti esistenti; Ofelia/sprite mancanti = portrait_locked).
- Un rigo di data a ogni salto di tempo ("Luna III, nono giorno").
- Nessun contatore visibile di affinità.

## Variabili e motore (linee per il builder)

- Affinità/flag esistenti invariati (`aede_affinity`, `caino_fiducia`, ecc.);
  nuovi `druso_affinity`, `icaro_affinity` + flag di route.
- Architettura punteggi [scelta del builder]: le soglie e le condizioni dei
  finali esistenti restano letteralmente identiche. Le scene territorio sono
  varianti una-tantum (pool finito, mai ripetibili con punti): ciascuna muove
  l'affinità di ±1, per un extra massimo di ~4-6 punti a personaggio sul
  semestre. Così le soglie attuali (es. `aede_affinity>=12`,
  `caino_fiducia>=12`) restano selettive senza ricalibrarle; se in playtest
  risultassero banali o irraggiungibili, si tara il pool, non le soglie.
- Stato calendario: luna corrente, giorno, slot.
- Tabella eventi: lista di (condizione → label, once/ripetibile, slot/data
  fissa opzionale). Lo scheduler a inizio slot pesca: evento a data fissa >
  invito a soglia > scena territorio dell'attività scelta > variante
  breve/salto.
- I label esistenti restano i mattoni; il motore li chiama al posto dei jump
  in catena attuali.

## Non-goals

- Statistiche numeriche visibili.
- Contenuto Ofelia (ora in 2026-10-21-route-ofelia-design.md).
- Poliamore, salvo la route Ofelia (con Aede e Caino).
- Riscrittura dei testi esistenti di Aede/Caino.

## Anti-goals (fallimento anche se "funziona")

- Rompere i finali esistenti di Aede/Caino o il loro routing a flag.
- Grind: costringere a ripetere scene identiche per far salire l'affinità.
- Calendario burocratico: se un giorno non ha niente di saliente, non deve
  esistere a schermo.

## Lasciato al builder

- Numero esatto di giorni giocabili per Luna e distribuzione degli eventi.
- Dettaglio delle varianti brevi anti-grind.
- Struttura file (`game/routes/calendario.rpy`, spostamenti eventuali).
- Testi delle scene nuove (Druso, Icaro, finale neutro), fedeli ai profili.
- Fasatura del lavoro (motore prima, contenuti poi).
