# Date the Dig — Visual Novel Ren'Py — Design: Route di Aede

Data: 2026-10-19. Stato: bozza approvata a voce dal committente, in revisione builder.

## Intento e perché

Dating sim / visual novel pura (solo testo, scelte, immagini — nessun gameplay
extra) ambientata nel mondo di Yr, nel Nord governato dalla Famiglia Dignitas.
L'ambientazione proviene da due manuali del committente: "Il Nord - La Guida" e
"La Famiglia Dignitas - La Guida" (PDF in `c:\Users\DPACCHIAROTT\Downloads\`;
testo estratto in file di lavoro). Il committente vuole partire piccolo: UNA
sola route completa (Aede), le altre arriveranno dopo. Motore: Ren'Py,
gratuito e open-source, adatto a principianti.

Prima release = demo giocabile con la route di Aede completa, dall'inizio ai
tre finali.

## Obiettivi

- Route di Aede completa e rigiocabile: prologo, 6 capitoli, climax, 3 finali.
- Scrittura in italiano, coerente con il lore dei due manuali (nomi, luoghi,
  usanze, riti citati correttamente).
- Struttura di progetto Ren'Py pulita e pronta a ricevere route future senza
  rifattorizzare (script separati per route, variabili con namespace).
- Durata target di una run: 30–60 minuti di lettura.

## Non-obiettivi

- Seconda route (love interest maschile): rinviata, ma la struttura deve
  prevederla (menu di selezione implicito tramite scene comuni → aggancio route).
- Minigiochi, mappe, gestione risorse, stat visibili: esclusi. VN pura.
- Doppiaggio, musica originale: fuori scope (placeholder o silenzio).
- Localizzazione in altre lingue.

## Anti-obiettivi (fallimento anche se "funziona")

- Lore contraddetto (es. un Dignitas che rivela il passato senza conseguenze,
  nomi o gerarchie sbagliate).
- Troppi personaggi/ramificazioni: il pericolo n.1 per chi inizia. Cast
  parlante massimo: 5–6 personaggi.
- Tsundere ridotta a macchietta: Aede deve avere un arco credibile
  (ostilità → incrinature → fiducia), non solo insulti-poi-rossore.

## Ambientazione (sintesi vincolante)

- Mondo: **Yr**. Regione: il Nord (Hammergrad + Collifreddi), unificato dalla
  **Famiglia Dignitas** — casata SENZA legami di sangue, si entra per
  **Adozione** rinunciando per giuramento a nome e vita precedenti (rivelarli
  è tabù assoluto). Stemma: leone dorato. Religione: il Caos, Asi protettore
  **Draken il Mutevole**, albero sacro **Yr-Drazul**.
- Capitale: **Zefiro** ("Città delle Lanterne", sei Contrade), sede del potere
  **Rocca Tempesta**. Capofamiglia: **Lenora Dignitas** (a vita).
- Gerarchia: Figlio → Filius Maior → Autarca (54, ognuno guida un Ceppo; 63
  Ceppi in 9 Rami, uno per Primarca) → Consiglio degli Autarchi → Capofamiglia.
- Ogni membro ha tre nomi: Primo (dall'Autarca), Secondo (scelto da sé), Terzo
  (dai fratelli).
- Feste/riti utilizzabili come scene: **Lo Svelo** (festa in maschera,
  trasgressioni di ceto concesse), **Athlion** (gara atletica annuale),
  **Fiaccolata della Calà** (leggenda: coppia che percorre la Calà mano nella
  mano si amerà per sempre), **Adunanza** annuale con il **Dono** (richiesta
  libera al Capofamiglia), **Ballo delle Candele Spente** (precedente storico
  cupo, ideato da Lenora).
- Tono: low fantasy nordico, politico e cupo ma vitale; soprannaturale
  discreto (Caos, presagi, Leoni Bianchi) mai invadente.

## Personaggi

### Protagonista
- **Nome scelto dal giocatore** a inizio partita (input Ren'Py; il nome
  inserito è il suo Primo Nome da Dignitas). Default se lascia vuoto: "Elio".
- Mezzo anonimo: volto mai mostrato, nessuno sprite, POV prima persona,
  personalità neutra plasmata dalle scelte. Genere: maschile (concordanze
  italiane).
- Giovane Dignitas adottato da poco nel **Ceppo di Briseide Ippodamia** ("la
  madre degli orfani") — Ceppo neutrale e benvoluto: libertà di movimento tra
  i Rami senza appartenenza di fazione.
- Il suo passato pre-adozione non viene mai mostrato nemmeno al giocatore:
  il giuramento vale anche per lui ed è tema portante della route.

### Aede — love interest (route di questa release)
- **Figlia adottiva del Ceppo di Glauco Severo** (Autarca presente nel lore).
- Assassina temibile, scaltra e veloce di mano. "Piccolo gioiello" del padre:
  Glauco la difende sempre, a prescindere dalle atrocità che commette.
- Archetipo: **tsundere**. Ostile, tagliente, orgogliosa; le incrinature
  emergono solo guadagnate.
- Aspetto (da immagine di riferimento fornita dal committente,
  `aede_black.jpg`): capelli rosso fiamma lunghi e mossi, occhi grigio-verdi,
  abito nero con sopravveste in broccato rosso, bottoni e catenelle d'oro,
  collana di gemme blu.

### Comprimari (cast massimo)
- **Glauco Severo** — Autarca, padre adottivo di Aede. Gatekeeper della route:
  cortese in superficie, letale se percepisce minaccia alla figlia. Decide il
  bad end "per mano del padre".
- **Briseide Ippodamia** — Autarca del protagonista, mentore caldo ma esigente.
  Fonte di incarichi che muovono la trama.
- 1–2 fratelli/sorelle di Ceppo del protagonista come spalla comica/consiglio
  (il builder può definirli; nomi inventati coerenti col lore, non Autarchi
  esistenti).

## Struttura narrativa

### Prologo
Il protagonista, adottato da poche settimane, arriva a Rocca Tempesta per
**Lo Svelo** (festa in maschera). Input nome giocatore. Primo incontro con
Aede: in maschera, lei lo scambia per un bersaglio (o lo borseggia — al
builder la scelta della variante migliore) e finisce con una lama alla sua
gola. Scintilla tsundere: lei furiosa per l'errore, lui unico testimone di
uno sbaglio della "perfetta" figlia di Glauco. Il segreto condiviso aggancia
la route.

### Capitoli 1–6 (eventi, un'ambientazione forte ciascuno)
Ogni capitolo: 1 scena principale con Aede + 1 scena di contorno (Ceppo,
intrighi dei Rami), 2–4 scelte di cui almeno 1 con effetto su `aede_affinity`
o su un flag. Canovaccio proposto (il builder può riordinare 2–5):

1. **L'incarico** — Briseide presta il protagonista al Ceppo di Glauco per una
   consegna delicata. Aede lo scorta: diffidenza, prime schermaglie.
2. **Athlion** — gara atletica. Aede compete per orgoglio del Ceppo; scelta su
   come sostenerla (tifo aperto / aiuto discreto / sfidarla).
3. **Intrigo tra Rami** — i due incastrati in un ricatto tra Ceppi rivali;
   collaborazione forzata, prima incrinatura (Aede ride, o protegge il
   protagonista d'istinto).
4. **Il lavoro di Aede** — il protagonista vede cosa fa davvero: eliminazione
   su commissione. Scelta morale chiave (orrore / accettazione / domanda
   sincera). Qui la route può virare verso il bad end.
5. **Fiaccolata della Calà** — scena romantica cardine. La leggenda degli
   amanti; percorrere o no la Calà insieme. Quasi-confessione interrotta.
6. **Il giuramento** — Aede sfiora il tabù: vorrebbe dire chi era prima.
   Scelta decisiva: fermarla (rispetto del giuramento) / ascoltarla /
   rivelare qualcosa di sé. Glauco osserva.

### Climax
Glauco ordina ad Aede un'eliminazione che tocca il protagonista (bersaglio:
lui stesso o qualcuno del suo Ceppo — al builder). Conflitto lealtà
padre/sentimento. L'esito dipende da `aede_affinity` + flag delle scelte
chiave (capitoli 4 e 6).

### Finali
- **Good end** (affinità alta + flag giusti): Aede disobbedisce o trova la
  terza via; i due diventano coppia. Chiusura: i due percorrono la Calà mano
  nella mano.
- **Neutral end** (affinità media): Aede esegue l'ordine risparmiando il
  protagonista con un inganno; restano amici, con malinconia.
- **Bad end** (affinità bassa o scelte sbagliate): due varianti — **lama di
  Aede** (lei esegue, fredda) o **mano di Glauco** (lui interviene di
  persona). Schermata di morte con citazione del lore (il Margine /
  Drakengrad).

## Meccaniche

- Ren'Py, VN pura: `say`, `menu`, sprite, sfondi, transizioni. Niente stat
  visibili al giocatore.
- Variabili: `aede_affinity` (intero, parte da 0), flag booleani per scelte
  chiave (`flag_segreto_svelo`, `flag_accetta_lavoro`, `flag_giuramento`, ...).
  Prefisso `aede_` / `flag_` per convivere con route future.
- Soglie finali: il builder le calibra; requisito: good end NON ottenibile
  scegliendo sempre l'opzione "gentile" in automatico — almeno una scelta
  controintuitiva (da tsundere: la risposta che rispetta il suo orgoglio
  batte quella sdolcinata).
- Salvataggi/rollback/skip: default Ren'Py, nessuna personalizzazione.

## Asset

- **Sprite Aede**: generati dal committente con AI a partire dal riferimento
  `aede_black.jpg` (abito nero). Servono: posa base + 4–6 espressioni
  (neutra, irritata, sorpresa, imbarazzata/rossore, sorriso raro, furia).
  Finché mancano: placeholder (silhouette o immagine unica).
- **Sfondi**: 6–8 (Rocca Tempesta sala festa, cortile/arena Athlion, vicoli di
  Zefiro, la Calà di notte, studio di Glauco, camera/corridoio del Ceppo,
  esterno innevato). Committente li genera con AI; placeholder ammessi.
- **Sprite comprimari**: Glauco e Briseide, 1–2 espressioni ciascuno;
  placeholder ammessi.
- **GUI**: tema Ren'Py di default ricolorato (palette: nero/oro/rosso, dal
  leone dorato Dignitas). Niente GUI custom complessa.
- **Musica/SFX**: fuori scope; struttura `audio/` predisposta.

## Vincoli

- Lingua del gioco: italiano.
- Tutto il testo di gioco scritto dal builder dev'essere coerente con la
  sintesi d'ambientazione qui sopra; in dubbio, consultare i riassunti dei
  manuali (o i PDF).
- Progetto Ren'Py in questa cartella (`date the dig`), struttura standard
  Ren'Py (`game/`, `script.rpy` minimo, route in `game/routes/aede.rpy` o
  file dedicato).
- Contenuti: romance e violenza da dark fantasy sì (assassini, morte del
  protagonista nei bad end); niente contenuto esplicito sessuale.

## Decisioni prese dal committente

- Solo route Aede in questa release; route maschile in seguito.
- Protagonista mezzo anonimo, maschile, senza sprite, nome scelto dal
  giocatore.
- Tre esiti della route: coppia / amici / morte per mano di Aede o Glauco.
- Motore Ren'Py, VN pura.

## Decisioni di design prese da me (Claude) e approvate implicitamente

- Ceppo del protagonista: Briseide Ippodamia. Ceppo di Aede: Glauco Severo.
- Prologo allo Svelo; Fiaccolata della Calà come scena romantica cardine.
- Default nome protagonista: "Elio".

## Decisioni post-revisione builder (mie, da revisione del 2026-10-19)

- Il prologo (Lo Svelo) appartiene alla route di Aede, non a un tronco
  comune. `script.rpy` contiene solo setup + input nome + salto alla route:
  una futura route maschile aggiungerà un proprio ingresso (1 label di bivio)
  senza riscrivere nulla.
- La prima release esce con placeholder. L'integrazione dell'arte finale del
  committente è fase successiva; il README conterrà la specifica tecnica
  degli asset (PNG con trasparenza, sprite 700×1400, sfondi 1920×1080, nomi
  file esatti) perché il committente generi immagini direttamente usabili.
- In caso di conflitto tra questa spec e i manuali PDF fa fede la spec
  (approvata dal committente); le divergenze trovate vengono solo annotate.

## Lasciato al builder

- Testi completi di scene e dialoghi (il canovaccio sopra è vincolante solo
  per prologo, cap. 1, cap. 6, climax e finali; cap. 2–5 riordinabili o
  sostituibili con eventi equivalenti purché coerenti col lore).
- Nomi e caratterizzazione dei 1–2 fratelli di Ceppo.
- Calibrazione soglie di affinità e numero esatto di scelte per capitolo.
- Dettagli tecnici Ren'Py (label, screen, transizioni, organizzazione file)
  entro i vincoli sopra.
- Scelta variante del primo incontro (bersaglio scambiato vs borseggio).
