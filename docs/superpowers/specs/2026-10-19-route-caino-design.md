# Date the Dig — Design: Route di Caino ("La legge del cuore")

Capitolo I "Malandrini", seconda route. Committente ha fornito descrizione
(2026-10-19); questa spec la struttura. Nota lore: il Caino del manuale
(Primo Arconte onorifico) è reinterpretato dal committente: qui è figlio di
Lenora, fratello di Druso e Icaro — fa fede il committente.

## Personaggio

- **Caino**, figlio di Lenora Dignitas, fratello di Druso e Icaro. Forte,
  abile spadaccino, grande ballerino. **Arconte della Proprietà**, membro di
  spicco della Famiglia. Farebbe di tutto per il potere. Sorriso facile,
  perde la pazienza raramente. Il **tradimento** è parte centrale del
  personaggio; è un **calcolatore**. Vince gli scontri verbali con la
  sicurezza di un politico ammanicato, anche (soprattutto) quando ha torto.
  Non avvezzo ai sentimenti: scetticismo reciproco da smantellare pezzo per
  pezzo; conquistata la fiducia, amante presente e totale.
- **Druso**: fratello, rapporto fortissimo — scherzano a botte sui genitali
  urlando "TESCHIO". Comprimario con ruolo da possibile switch (finale
  segreto).
- Aspetto (foto riferimento): capelli scuri raccolti a codino con rasatura,
  barba curata, mantello di pelliccia nera, tunica ruggine broccata con
  cinghie di cuoio, bracciali d'arme.

## Meccaniche distintive (richieste dal committente)

1. **Test di memoria**: Caino è attento ai dettagli e mette alla prova la
   memoria del giocatore. I dettagli vengono seminati nelle scene e
   richiesti in menu successivi (3 quiz).
2. **Trappole di sarcasmo**: Caino dice cazzate con sicurezza assoluta; il
   giocatore non deve cadere nei tranelli (3 trappole: assecondarlo = caduta).
3. Scena obbligatoria: palestra con Druso — "TESCHIO" + Caino che fa alzate
   laterali con due blocchi di marmo da 24 chili l'uno.
4. Dialoghi centrali, scontri verbali da politico.

## Variabili

`caino_fiducia` (int), `caino_memoria` (quiz corretti), `caino_trappole`
(trappole cadute), `caino_druso` (legame con Druso), flag di scena.

## Finali (ordine di routing)

1. **Good — "La legge del cuore"**: fiducia >= 12 e trappole <= 1 e
   memoria >= 2. La breccia è completa: sceglie l'amore sopra la scalata,
   amante presente che farebbe di tutto.
2. **Segreto — "Teschio"**: caino_druso >= 3 e fiducia < 12. Lo switch:
   Druso si fa avanti; Caino concede con sarcasmo fraterno.
3. **Bad — "La pedina"**: fiducia < 5 oppure trappole >= 3. Caino ti ha
   usato: capro espiatorio davanti al Consiglio, esilio/Segrete Silenti.
   Nessuna morte: il suo tradimento è politico, più freddo di una lama.
4. **Neutral — "Soci"**: tutto il resto. Alleanza di potere senza amore.

## Struttura

- Prologo: Adunanza a Rocca Tempesta. Caino nota il Figlio di Briseide.
  Semina: odia il vino di Glostok, beve solo idromele di Rurikstad; anello
  con sigillo del drago al mignolo destro. Trappola 1: elogia il Ballo
  delle Candele Spente (fu un massacro ideato da sua madre).
- Cap 1 — La Proprietà: incarico amministrativo. Quiz 1 (vino/idromele).
- Cap 2 — La palestra: TESCHIO + marmo 24 kg. Semina: debito di Druso (40
  Scudi). Occasione druso+1. Trappola 2 ("Druso è il preferito di nostra
  madre, lo dico senza invidia").
- Cap 3 — Il ballo: Caino grande ballerino. Quiz 2 (l'anello). Danza ±.
  Occasione druso+1.
- Cap 4 — Il tradimento: Caino brucia un alleato (Filius del Ceppo di
  Cardia) per una carica. Scelta morale. Semina: il nome dell'alleato.
- Cap 5 — La breccia: scetticismo reciproco. Trappola 3 (finta confessione
  in sarcasmo). Scelta chiave di sincerità.
- Cap 6 — La prova: offre potere condiviso vs amore. Quiz 3 (l'unica cosa
  che ha detto di odiare). Occasione druso+1 (Druso ti avverte).
- Climax — Il Consiglio: congiura; Caino deve scegliere se usarti. Routing.

## Asset

- Sprite Caino (placeholder finché il committente non genera): neutro
  (sorriso facile), sarcastico, freddo, sorpreso, tenero, furioso.
- Sprite Druso: neutro, ghigno. Sfondi nuovi placeholder: `bg palestra`,
  `bg consiglio`. Riuso: sala_svelo (Adunanza/ballo), corridoio_ceppo,
  vicoli_zefiro.

## Lasciato al builder

Testi completi, calibrazione punti, dettagli delle scene entro il canovaccio.
