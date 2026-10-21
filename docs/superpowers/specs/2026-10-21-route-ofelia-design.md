# Route Ofelia — "Tanto bella quanto letale" (design)

Data: 2026-10-21. Stato: approvata dal committente.

Profilo canonico: `docs/profili/ofelia.md`. Si innesta sul calendario dei
Malandrini (`2026-10-20-malandrini-calendario-design.md`) senza toccarne le
date fisse.

## Concept

Ofelia, figlia di Glauco Severo, sorella di Aede e Ascadeo. Difficoltà 4/5.
È l'unica route in cui il protagonista non è l'unico pretendente: Ofelia ha
una corte, e tu sei un nome tra tanti finché non dimostri di non essere un
interesse passeggero. È anche l'unica route che ammette il poliamore, solo con
Aede e con Caino.

Il difetto costa al giocatore: Ofelia è spietata con i sentimenti altrui. Ti
usa per far ingelosire un rivale (evento 2) e non avvisa quando ti cerca. Il
good end rinegozia il difetto, non lo cancella: resta letale, ma sceglie.

## Scelte del committente (vincolanti)

- Nome route: "Tanto bella quanto letale".
- Poliamore con Aede: **solo da parte di Ofelia**. Ofelia accetta di
  condividerti con la sorella; Aede non lo sa e non lo accetterebbe (profilo
  Aede: niente poliamore). Tensione e rischio di bad end.
- Poliamore con Caino: dichiarato (scelta del builder: per Caino è un
  contratto a tre, nel suo registro).
- Meccanica: **route doppia** alla scelta del cuore.

## Lucchetto: inviti a scadenza

Meccanicamente nuovo (gli altri: prova a metà, trappola d'ingresso, passi
falsi, gelosia).

- Gli inviti di Ofelia hanno `"scade": True`: valgono un solo slot.
- Se l'invito è mostrato nel pianificatore e il giocatore sceglie altro:
  `ofelia_mancati += 1`, `ofelia_affinity -= 1`, notifica diegetica.
  L'invito resta nel registry e ricompare al prossimo slot compatibile.
- `ofelia_mancati >= 2` → `congelate.add("ofelia")`: interesse passeggero.
- Motore: funzione pura `inviti_ignorati(mostrati, scelto_id)` in
  `calendario_logic.py` (ritorna gli id degli inviti con `scade` non scelti),
  testata; il loop chiama un hook `cal_inviti_ignorati_hooks` con quegli id.
- Dopo la scelta del cuore la scadenza vale solo se Ofelia è route attiva o
  seconda (altrimenti i suoi inviti non compaiono comunque).

## Territorio

Attività nuova, pomeriggio: `("corte", "La corte di Ofelia", "ofelia",
["att_corte_1", "att_corte_2", "att_corte_3"])`. Ricevimenti nella serra di
Rocca Tempesta, tra pretendenti. Ogni scena ±1 una-tantum. Descrizione nel
pianificatore e riga di fallback in `ATTIVITA_DESC` / `CAL_FALLBACK`.
Sostituisce il riquadro "Ofelia — Prossimamente".

## Eventi a soglia (Lune I-IV)

| id | Luna min | Slot | Cond | Punti |
|---|---|---|---|---|
| `ofelia_ev1` — il pretendente scartato in pubblico | 1 | pomeriggio | `ofelia_affinity >= 2` | +2 |
| `ofelia_ev2` — ti usa per ingelosire un rivale | 2 | sera | `>= 4` e `ofelia_ev1` visto | +2 |
| `ofelia_ev3` — il duello all'alba, lei tira sul serio | 3 | mattina | `>= 6`, `ofelia_ev2` visto, `scelta_cuore` non visto | +2 |

Tutti con `"scade": True`.

## Economia

- Massimo alla scelta del cuore: territorio +3, eventi +6 = **9**. Soglia
  impegno: **8** (al massimo un punto perso).
- Lune V-VI: Fiaccolata +1, `ofelia_ev4` (Luna V, dopo la Fiaccolata) +2,
  scelta finale nel climax ±1. Massimo **13**.
- Good end: `ofelia_affinity >= 11` e `ofelia_mancati <= 1`.
- `check_economia_punti` verifica: max >= 8, max >= 11, soglie presenti nei
  file.

## Scelta del cuore e route doppia

- Nuove variabili: `ofelia_affinity = 0`, `ofelia_mancati = 0`,
  `route_seconda = None`, `aede_sospetto = 0`.
- `cuore_candidati()` include `"ofelia": ofelia_affinity >= 8`.
- Se `"ofelia"` è candidata insieme a `"aede"` e/o `"caino"`, il menu offre
  anche "Ofelia e Aede" / "Ofelia e Caino". Si giocano `impegno_ofelia_aede`
  o `impegno_ofelia_caino` (che include la scena di Ofelia) e poi l'impegno
  dell'altro. Riescono entrambi → `route_attiva = "ofelia"`,
  `route_seconda = "aede"|"caino"`. Ne fallisce uno → resta attiva solo la
  route riuscita (seconda = None).
- `cal_inviti_info`: a route attiva passano gli inviti di
  `route_attiva` e `route_seconda`.
- `route_viva()` invariata; nuova `route_seconda_viva()` (seconda non
  congelata).
- `cal_vars()` espone `ofelia_affinity`, `ofelia_mancati`, `route_seconda`.

## Fiaccolata (V/14)

- Ofelia sola: `ofelia_fiaccolata`.
- Ofelia + Caino: `ofelia_fiaccolata_caino`, a tre, dichiarata.
- Ofelia + Aede: `ofelia_fiaccolata_aede` — la Calà, due sorelle, una mano.
  Menu: mano di Aede (nessun sospetto, Ofelia +0) / mano di Ofelia
  (`aede_sospetto += 2`, Ofelia +1). Poi `aede_cap6` resta in calendario
  come oggi (cond su `route_attiva == "aede"` va estesa a
  `route_seconda == "aede"`).
- `aede_sospetto += 1` anche per ogni invito di Ofelia accettato in Luna V-VI
  con Aede seconda.

## Climax (VI/21) e finali

Dispatch in `ev_luna6`:
- Ofelia + Aede → `climax` di Aede (studio di Glauco) con innesto: Ofelia
  presente; il routing finale passa da `ofelia_poly_aede_routing`.
- Ofelia sola o + Caino → `ofelia_climax`.

Finali:
- **Tanto bella quanto letale** (good, sola): `ofelia_affinity >= 11`,
  `ofelia_mancati <= 1`, `route_seconda is None`.
- **Il contratto a tre** (good poly Caino): good di Ofelia +
  `caino_fiducia >= 12`.
- **Le figlie di Glauco** (good poly Aede, agrodolce): good di Ofelia + good
  di Aede (condizioni attuali: `aede_affinity >= 12 and flag_giuramento and
  flag_accetta_lavoro`) + `aede_sospetto < 2`.
- **La tempesta** (bad): `route_seconda == "aede"` e `aede_sospetto >= 2`.
  Aede scopre, furia; Glauco chiude il conto.
- **Interesse passeggero** (neutral): tutto il resto. Ofelia passa al
  pretendente successivo.
- Poly con condizioni dell'altro non soddisfatte → good sola di Ofelia con
  coda amara sull'altro.

## Budget

Scene (~16): `att_corte_1-3`, `ofelia_ev1-4`, `impegno_ofelia`,
`impegno_ofelia_caino`, `impegno_ofelia_aede`, `ofelia_fiaccolata`,
`ofelia_fiaccolata_caino`, `ofelia_fiaccolata_aede`, `ofelia_climax`, innesto
nel climax di Aede, 5 finali.

Asset: sprite Ofelia esistenti (neutra, rabbia, imbarazzata, compiaciuta),
`gui/portrait_ofelia.png` esistente. Mancanti: `bg serra` (placeholder
`bg sala_svelo`); opzionale `ofelia sorriso` (fallback `compiaciuta`).

## Anti-goals

- Rompere i finali esistenti di Aede/Caino o il loro routing.
- Poliamore con Druso o Icaro.
- Aede consenziente al poliamore (contraddice il suo profilo).
- Soglie irraggiungibili: il 4/5 è "un errore al massimo", non "impossibile".
